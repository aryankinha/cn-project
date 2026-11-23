"""Update a single record on both resolvers, with verified rollback."""
import argparse
import fcntl
import ipaddress
import sys

from cnlib import Lab, ROOT, operation_lock, require

RESOLVERS = ("mac1", "mac2")
WRITE = r"""
set -eu
file="$HOME/cn-project/dnsmasq/project.hosts"
tmp="$(mktemp "$file.XXXXXX")"
cat > "$tmp"
mv "$tmp" "$file"
"$HOME/cn-project/bin/node.sh" reload dns
"""


def change(lab, name, ip):
    address = ipaddress.IPv4Address(ip)
    require(address in lab.network and address not in (
        lab.network.network_address, lab.network.broadcast_address, lab.gateway
    ), "Record target must be a usable LAN address")
    require(name in (lab.app, lab.api), "Select app or api")
    lock = ROOT / "team/.dns.lock"
    with lock.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        files = {}
        expected_records = {}
        for node in RESOLVERS:
            files[node] = lab.on(node, ("cat", lab.runtime(node) / "dnsmasq/project.hosts")).stdout
            values = {}
            for host in (lab.app, lab.api):
                answers = lab.query(node, host)
                require(len(answers) == 1 and answers[0][0] == lab.ttl,
                        f"{node} has no single live {host} answer with TTL {lab.ttl}")
                values[host] = answers[0][1]
            expected_records[node] = values
        require(expected_records["mac1"] == expected_records["mac2"],
                "Authoritative DNS answers disagree. Reconcile the resolvers first.")
        original = expected_records["mac1"]
        desired = {**original, name: ip}
        text = "".join(f"{target} {host}\n" for host, target in desired.items())
        attempted = []
        try:
            for node in RESOLVERS:
                attempted.append(node)
                lab.on(node, ("bash", "-c", WRITE), data=text, display=True)
            verify(lab, desired)
        except (Exception, KeyboardInterrupt):
            for node in reversed(attempted):
                old = files[node].rstrip("\n") + "\n"
                lab.on(node, ("bash", "-c", WRITE), data=old, check=False, display=True)
            verify(lab, original)
            raise
        return original[name]


def verify(lab, records):
    for node in RESOLVERS:
        for host, ip in records.items():
            answers = lab.query(node, host)
            print(f"{node}: {host} {answers}", flush=True)
            require(answers == [(lab.ttl, ip)], f"{node} confirmation failed for {host}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("record", choices=("app", "api"))
    parser.add_argument("target", help="mac2, mac3, or a verified LAN IPv4 address")
    args = parser.parse_args()
    lab = Lab()
    try:
        with operation_lock():
            change(lab, f"{args.record}.{lab.domain}", lab.ips.get(args.target, args.target))
    except (RuntimeError, ValueError) as error:
        sys.exit(str(error))
