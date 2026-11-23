"""Assertions and recoverable demonstrations for the deployed four-Mac lab."""
import argparse
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime
import io
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cnlib import Lab, NODES, ROOT, headers, operation_lock, require, run
from diagnose import diagnose
from dns import change
from smoke import series, smoke

STATE = ROOT / "team/.demo-state.json"


def who(lab):
    for node in NODES:
        print(f"{node}: {lab.users[node]} @ {lab.ips[node]}")
        lab.node(node, "status", display=True)


def baseline(lab):
    who(lab)
    failed = []
    for source in NODES:
        lab.on(source, ("ifconfig", lab.interface), display=True)
        for target in NODES:
            if target == source:
                continue
            ping = lab.on(source, ("ping", "-q", "-c", "2", "-t", "4", lab.ips[target]),
                          check=False, display=True)
            if ping.returncode or "2 packets received" not in ping.stdout:
                failed.append(f"{source} → {target}")
    smoke(lab)
    require(not failed, "Pairwise ping failed: " + ", ".join(failed))


def ip_cached(lab, node="mac1"):
    result = lab.on(node, ("dscacheutil", "-q", "host", "-a", "name", lab.app),
                    check=False, display=True, timeout=30)
    return next((line.split()[1] for line in result.stdout.splitlines()
                 if line.startswith("ip_address:")), None)


def scope(lab, node, action, service):
    lab.node(node, action, service, display=True)


def await_ip(lab, ip, node="mac1"):
    start = time.monotonic()
    while time.monotonic() - start <= lab.ttl + 35:
        observed = ip_cached(lab, node)
        print(f"{node} +{time.monotonic() - start:.1f}s system answer: {observed}", flush=True)
        if observed == ip:
            return
        time.sleep(2)
    raise RuntimeError(f"{node} never observed {ip}")


def edge(lab, edge_id, node="mac1"):
    code, fields = headers(lab.https(lab.app, source=node, display=True))
    require(code == 200 and fields.get("x-edge") == edge_id and
            fields.get("x-backend") in ("A", "B"), f"{node} expected HTTP 200 via {edge_id}: {fields}")


def backup_dns(lab):
    print("A · Stop primary DNS and verify a fresh backup answer and ordinary HTTPS.")
    scope(lab, "mac1", "health", "dns")
    scope(lab, "mac2", "health", "dns")
    # Let any existing Mac 4 system answer expire before starting the packet capture.
    time.sleep(lab.ttl + 2)
    try:
        scope(lab, "mac1", "stop", "dns")
        require(not lab.query("mac1", lab.app, source="mac4"), "Primary DNS still answered")
        require(lab.query("mac2", lab.app, source="mac4") == [(lab.ttl, lab.ips["mac2"])],
                "Backup DNS did not return the expected answer")
        result = lab.on("mac4", ("bash", "-s", "--", lab.interface, lab.ips["mac2"], lab.app),
                        data=BACKUP_CAPTURE, display=True, timeout=35)
        require("answer-from-backup" in result.stdout, "Capture did not prove a fresh backup reply")
        edge(lab, "edge1-mac2", "mac4")
    finally:
        scope(lab, "mac1", "start", "dns")
        require(lab.query("mac1", lab.app) == [(lab.ttl, lab.ips["mac2"])], "Primary DNS recovery failed")


BACKUP_CAPTURE = r"""
set -euo pipefail
iface="$1"; backup="$2"; host="$3"
trace="$(mktemp -t cn-dns)"
tcpdump --immediate-mode -ni "$iface" -U -s 0 -w "$trace" "udp and src host $backup and src port 53" >/dev/null 2>&1 &
pid=$!
trap 'kill -INT "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; unlink "$trace"' EXIT
sleep 1
dscacheutil -q host -a name "$host"
sleep 1
kill -INT "$pid"
wait "$pid"
tshark=/Applications/Wireshark.app/Contents/MacOS/tshark
answers="$("$tshark" -r "$trace" -Y "dns.flags.response == 1 && dns.qry.name == \"$host\" && dns.a == $backup" -T fields -e ip.src -e dns.qry.name -e dns.a)"
test -n "$answers"
printf '%s\n' "$answers"
echo answer-from-backup
"""


@contextmanager
def record_change(lab, target):
    before = lab.query("mac1", lab.app)
    require(len(before) == 1, "Cannot snapshot original app record")
    original = before[0][1]
    try:
        change(lab, lab.app, target)
        yield original
    finally:
        if lab.query("mac1", lab.app) == [(lab.ttl, target)]:
            change(lab, lab.app, original)
        for resolver in ("mac1", "mac2"):
            require(lab.query(resolver, lab.app) == [(lab.ttl, original)],
                    f"Recovery incomplete on {resolver}")


def ttl(lab, *, flush=False):
    print("B · Compare the authoritative change with a primed client's cached answer.")
    primary, standby = (lab.ips[node] for node in ("mac2", "mac3"))
    # Expire any entry left by earlier probes, then take a fresh system answer.
    time.sleep(lab.ttl + 2)
    require(ip_cached(lab) == primary, "Start with the primary record")
    with record_change(lab, standby):
        require(ip_cached(lab) == primary, "The old answer was not captured after the update")
        await_ip(lab, standby)
    if flush:
        require(ip_cached(lab) == standby, "Cached standby answer expired before the flush trial")
        command = ("sudo", "-n", lab.runtime("mac1") / "bin/client.sh", "flush", "Wi-Fi")
        run(command, display=True)
        require(ip_cached(lab) == primary, "Immediate post-flush lookup did not return the primary")
    else:
        print("Manual flush step still required. Run B --flush with an authorized local sudo session.")
        await_ip(lab, primary)
        edge(lab, "edge1-mac2")
        raise RuntimeError("TTL expiry verified; manual cache flush pending")
    await_ip(lab, primary)
    edge(lab, "edge1-mac2")


def direct(lab, source, backend):
    node = {"A": "mac3", "B": "mac4"}[backend]
    return lab.on(source, ("curl", "--noproxy", "*", "-sS", "--connect-timeout", "3",
                         "--max-time", "4", "-D", "-", "-o", "/dev/null",
                         f"http://{lab.ips[node]}:{lab.ports[backend]}/api/status"),
                  check=False, display=True)


def isolation(lab, restored=False, standby=False):
    print("C · Verify the primary edge, off-host client, and through-edge paths for both ports.")
    for backend in ("A", "B"):
        code, fields = headers(direct(lab, "mac2", backend))
        require(code == 200 and fields.get("x-backend") == backend, f"Mac 2 cannot reach {backend}")
        probe = direct(lab, "mac1", backend)
        if restored:
            code, fields = headers(probe)
            require(code == 200 and fields.get("x-backend") == backend, f"Rollback did not restore {backend}")
        else:
            require(probe.returncode == 28 and not probe.stdout,
                    f"Expected packet drop to {backend}; observed curl exit {probe.returncode}")
    series(lab, "edge1-mac2")
    if not restored:
        probe = direct(lab, "mac3", "B")
        if standby:
            code, fields = headers(probe)
            require(code == 200 and fields.get("x-backend") == "B", "Standby cannot reach Backend B")
            series(lab, "edge2-mac3", lab.ips["mac3"])
        else:
            require(probe.returncode == 28 and not probe.stdout,
                    "Strict profile must deny Mac 3's LAN hop to Backend B")
        print("Isolation behavior verified. Roll back on both backend Macs, then run C --restored.")


def failover(lab):
    print("D · Stop A and require every request to be served by B.")
    series(lab, "edge1-mac2")
    try:
        scope(lab, "mac3", "stop", "backend")
        series(lab, "edge1-mac2", only="B", count=8)
    finally:
        scope(lab, "mac3", "start", "backend")
        scope(lab, "mac3", "health", "backend")
        wait_for_backends(lab, {"A"})
        series(lab, "edge1-mac2")
    output = lab.on("mac2", ("tail", "-n", "22", lab.runtime("mac2") / "logs/nginx-access.log"))
    print(output.stdout)


def wait_for_backends(lab, expected):
    pending = set(expected)
    deadline = time.monotonic() + 35
    while pending and time.monotonic() < deadline:
        code, fields = headers(lab.https(lab.app, display=True))
        require(code == 200 and fields.get("x-edge") == "edge1-mac2",
                "Request failed during the recovery observation")
        if fields.get("x-backend") in pending:
            print(f"Backend {fields['x-backend']} rejoined the upstream pool")
            pending.remove(fields["x-backend"])
        elif pending:
            time.sleep(1)
    require(not pending, f"Failed to observe backend recovery for {sorted(pending)}")


def cutover(lab):
    print("E · Route fresh app lookups to Mac 3 while Mac 1 still has the primary answer.")
    primary, standby = (lab.ips[node] for node in ("mac2", "mac3"))
    series(lab, "edge2-mac3", standby)
    # Mac 4 stays idle during the wait. Only Mac 1 is primed before the update.
    time.sleep(lab.ttl + 3)
    require(ip_cached(lab) == primary, "Mac 1 did not cache the primary edge")
    try:
        with record_change(lab, standby):
            edge(lab, "edge1-mac2")
            edge(lab, "edge2-mac3", "mac4")
            for resolver in ("mac1", "mac2"):
                require(lab.query(resolver, lab.api) == [(lab.ttl, primary)], "API record changed during app cutover")
            await_ip(lab, standby)
            edge(lab, "edge2-mac3")
    finally:
        await_ip(lab, primary)
        edge(lab, "edge1-mac2")


def inject(lab):
    require(not STATE.exists(), "A previous fault still needs recovery (run fix)")
    require(diagnose(lab) is None, "Resolve baseline fault before practice")
    STATE.touch(mode=0o600, exist_ok=False)
    STATE.write_text(json.dumps({"node": "mac2", "service": "edge", "expected": "TCP"}))
    scope(lab, "mac2", "stop", "edge")


def recover(lab):
    require(STATE.exists(), "No recorded practice fault")
    state = json.loads(STATE.read_text())
    scope(lab, state["node"], "start", state["service"])
    require(diagnose(lab) is None, "Recovery incomplete; fault record retained")
    STATE.unlink()


def fault(lab):
    print("F · Diagnose a stopped primary edge and confirm recovery.")
    try:
        inject(lab)
        require(diagnose(lab) == "TCP", "Expected the first failing layer to be TCP")
    finally:
        if STATE.exists():
            recover(lab)


def phase1_client(lab, *, restored=False):
    client = "mac3"
    lab.on(client, ("networksetup", "-getdnsservers", "Wi-Fi"), display=True)
    if restored:
        require(ip_cached(lab, client) == lab.ips["mac2"], "Mac 3 did not recover normal DNS")
        edge(lab, "edge1-mac2", client)
    else:
        require(ip_cached(lab, client) is None, "Mac 3 can still resolve the private name")
        status, fields = headers(lab.https(lab.app, ip=lab.ips["mac2"], source=client, display=True))
        require(status == 200 and fields.get("x-edge") == "edge1-mac2",
                "Mac 3 could not reach the trusted primary edge with DNS bypassed")


def phase1_failures(lab, *, wrong_client=False):
    print("Phase 1 §6.3 · Run the wrong-record, backend and wrong-port scenarios.")
    if wrong_client:
        phase1_client(lab)
    with record_change(lab, lab.ips["mac1"]):
        await_ip(lab, lab.ips["mac1"])
        require(diagnose(lab) == "DNS", "Expected incorrect A record to be diagnosed")
    await_ip(lab, lab.ips["mac2"])
    failover(lab)
    try:
        for node in ("mac3", "mac4"):
            scope(lab, node, "stop", "backend")
        require(ip_cached(lab) == lab.ips["mac2"], "DNS should still work")
        require(headers(lab.https(lab.app, display=True))[0] == 502, "Expected HTTP 502 with both backends down")
        require(diagnose(lab) == "Upstream", "Expected upstream diagnosis")
    finally:
        for node in ("mac4", "mac3"):
            scope(lab, node, "start", "backend")
        time.sleep(10)
        wait_for_backends(lab, {"A", "B"})
        smoke(lab)
    require(diagnose(lab, port=65534) == "TCP", "Wrong-port check did not fail at TCP")
    require(diagnose(lab) is None, "Normal service did not recover")
    print("Four controller-managed scenarios passed. Use phase1-client for the owner-assisted DNS check and recovery.")


class Tee(io.TextIOBase):
    def __init__(self, terminal, evidence):
        self.terminal, self.evidence = terminal, evidence

    def write(self, text):
        self.terminal.write(text)
        return self.evidence.write(text)

    def flush(self):
        self.terminal.flush()
        self.evidence.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("who", "check", "baseline", "A", "B", "C", "D", "E", "F",
                                           "break", "answer", "fix", "diagnose", "phase1", "phase1-client"))
    parser.add_argument("--flush", action="store_true")
    parser.add_argument("--restored", action="store_true")
    parser.add_argument("--standby", action="store_true")
    parser.add_argument("--wrong-client", action="store_true")
    args = parser.parse_args()
    lab = Lab()
    steps = {"who": who, "check": smoke, "baseline": baseline, "A": backup_dns,
             "B": lambda lab: ttl(lab, flush=args.flush),
             "C": lambda lab: isolation(lab, restored=args.restored, standby=args.standby), "D": failover,
             "E": cutover, "F": fault, "break": inject, "fix": recover,
             "answer": lambda _: print(json.loads(STATE.read_text()) if STATE.exists() else "No active practice fault"),
             "diagnose": lambda lab: require(diagnose(lab) is None, "Diagnostic found a fault"),
             "phase1": lambda lab: phase1_failures(lab, wrong_client=args.wrong_client),
             "phase1-client": lambda lab: phase1_client(lab, restored=args.restored)}
    folder = ROOT / "evidence/phase2"
    folder.mkdir(exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S-%f%z")
    path = folder / f"{stamp}-{args.command}.log"
    with path.open("x") as log, redirect_stdout(Tee(sys.stdout, log)), redirect_stderr(Tee(sys.stderr, log)):
        print(f"{datetime.now().astimezone().isoformat()} | scenario={args.command}", flush=True)
        try:
            with operation_lock(allow_fault=args.command in ("answer", "diagnose", "fix", "who")):
                steps[args.command](lab)
        except (OSError, RuntimeError, subprocess.SubprocessError, KeyboardInterrupt) as error:
            print(f"INCOMPLETE: {error}", file=sys.stderr, flush=True)
            return 1
        finally:
            print(f"Evidence: {path}", flush=True)
        print("Requested checks passed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
