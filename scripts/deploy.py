"""Stage every role bundle, validate on target, and activate with rollback."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from cnlib import Lab, NODES, ROLES, ROOT, SSH, operation_lock, require, run
from render import render
from smoke import smoke

PREFLIGHT = r"""
set -eu
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:$PATH"
test "$(id -un)" = "$1"
test "$HOME" = "$2"
test "$(ipconfig getifaddr "$3")" = "$4"
test "$(ipconfig getoption "$3" router)" = "$5"
printf 'Host %s | ' "$(id -un)"
sw_vers -productVersion
uname -m
ifconfig "$3" | awk '/inet / || /ether / {print}'
for tool in python3 openssl curl dig "$@"; do
    case "$tool" in dns) command -v dnsmasq;; edge) command -v nginx;;
        backend) command -v /sbin/pfctl;; python3|openssl|curl|dig) command -v "$tool";;
    esac
done
"""

SNAPSHOT = r"""
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:$PATH"
cd "$HOME/cn-project" || exit
networksetup -getdnsservers Wi-Fi
scutil --dns
for port in 53 80 443 3001 3002; do lsof -nP -iTCP:"$port" -sTCP:LISTEN; done
lsof -nP -iUDP:53
for file in run/*.pid; do
    if [ -f "$file" ]; then
        ps -p "$(cat "$file")" -o pid=,ppid=,user=,command=
    fi
done
launchctl list | awk '/dnsmasq|nginx|cn-project/'
for file in node.env dnsmasq/dnsmasq.conf dnsmasq/project.hosts \
    nginx/nginx.conf nginx/cn-project.conf backend/requirements.txt firewall/backend.pf; do
    if [ -f "$file" ]; then printf '\n--- %s ---\n' "$file"; cat "$file"; fi
done
if [ -f backend/app.py ]; then shasum -a 256 backend/app.py; fi
if [ -f nginx/nginx.conf ]; then nginx -p "$PWD/" -c "$PWD/nginx/nginx.conf" -T; fi
if [ -f tls/edge.crt ]; then openssl x509 -in tls/edge.crt -noout -fingerprint -sha256 -dates -ext subjectAltName; fi
/sbin/pfctl -s info 2>&1
exit 0
"""


def preflight(lab, nodes):
    errors = []
    for node in nodes:
        try:
            lab.on(node, ("bash", "-s", "--", lab.users[node], lab.runtime(node).parent,
                          lab.interface, lab.ips[node], lab.gateway, *ROLES[node]),
                   data=PREFLIGHT, display=True)
            print(f"{node} preflight passed", flush=True)
        except (OSError, subprocess.SubprocessError) as error:
            errors.append(f"{node}: {error}")
    require(not errors, "\n".join(errors))


def stage_files(lab, node, source, stage):
    lab.on(node, ("bash", "-c", 'umask 077; mkdir -p "$1"; mkdir "$2"', "_", stage.parent, stage))
    if node == "mac1":
        shutil.copytree(source, stage, dirs_exist_ok=True)
    else:
        command = ("scp", *SSH[1:], "-r", *(str(p) for p in source.iterdir()),
                   f"{lab.env[node.upper()]}:{stage}/")
        run(command, display=True)


def action(lab, node, stage, mode):
    lab.on(node, ("bash", stage / "activate.sh", mode, stage), display=True, timeout=180)


def main():
    parser = argparse.ArgumentParser()
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--all", action="store_true")
    target.add_argument("--check", action="store_true")
    target.add_argument("--node", choices=NODES)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    lab = Lab()
    nodes = (args.node,) if args.node else NODES
    preflight(lab, nodes)
    if args.check or args.dry_run:
        for node in nodes:
            print(f"{node}: {lab.runtime(node)} | {', '.join(ROLES[node])}")
        return
    with operation_lock():
        deploy(lab, nodes)


def deploy(lab, nodes):
    require(not run(("git", "-C", ROOT, "status", "--porcelain", "--untracked-files=no")).stdout.strip(),
            "Commit tracked implementation changes before deploying")
    rev = run(("git", "-C", ROOT, "rev-parse", "--short=12", "HEAD")).stdout.strip()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    release = f"{rev}-{stamp}"
    snapshots = ROOT / "evidence/local-raw" / release
    snapshots.mkdir(parents=True, mode=0o700)
    stages = {node: lab.runtime(node) / "releases" / release for node in nodes}
    for node in nodes:
        snapshot = lab.on(node, ("bash", "-s"), data=SNAPSHOT)
        file = snapshots / f"{node}.txt"
        file.touch(mode=0o600)
        file.write_text(snapshot.stdout + snapshot.stderr)
        print(f"{node} baseline saved to {file}")

    with tempfile.TemporaryDirectory(prefix="cn-release-") as directory:
        for node, stage in stages.items():
            source = Path(directory) / node
            render(lab, node, source)
            shutil.copy2(ROOT / "scripts/activate.sh", source)
            (source / "REVISION").write_text(rev + "\n")
            stage_files(lab, node, source, stage)
            action(lab, node, stage, "validate")

    completed = []
    try:
        for node in ("mac4", "mac3", "mac2", "mac1"):
            if node in stages:
                action(lab, node, stages[node], "activate")
                completed.append(node)
        # Passive health state can last ten seconds after a rolling backend restart.
        for attempt in range(3):
            try:
                smoke(lab)
                break
            except (RuntimeError, subprocess.SubprocessError):
                if attempt == 2:
                    raise
                time.sleep(6)
    except (Exception, KeyboardInterrupt):
        for node in reversed(completed):
            try:
                action(lab, node, stages[node], "rollback")
            except (OSError, subprocess.SubprocessError) as error:
                print(f"ROLLBACK INCOMPLETE on {node}: {error}", file=sys.stderr)
        raise
    print(f"Release {release} activated and verified on {', '.join(completed)}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        sys.exit(str(error))
