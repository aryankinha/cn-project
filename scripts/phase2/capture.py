"""Collect a scoped DNS/TCP/TLS capture on Mac 4 and validate its contents."""
import base64
from datetime import datetime
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cnlib import Lab, ROOT, require, run

CAPTURE = r"""
set -euo pipefail
iface="$1"; primary="$2"; backup="$3"; edge="$4"; host="$5"
file="$(mktemp -t cn-pcap)"
trace="$(mktemp -t cn-trace)"
tcpdump -ni "$iface" -s 0 -U -w "$file" \
    "((host $primary or host $backup) and port 53) or (host $edge and tcp port 443)" \
    >"$trace" 2>&1 &
pid=$!
trap 'kill -INT "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; unlink "$file"; unlink "$trace"' EXIT
sleep 1
dig @"$primary" "$host" A +time=2 +tries=1 +noall +answer >&2
curl --noproxy '*' --http1.1 --tlsv1.2 --tls-max 1.2 -fsS --max-time 8 \
    -v -D - -o /dev/null "https://$host/api/status" >&2
kill -INT "$pid"
wait "$pid"
cat "$trace" >&2
base64 -i "$file"
"""


def main():
    lab = Lab()
    ts = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S%z")
    output = ROOT / "evidence/phase2" / f"{ts}-lan-flow"
    result = lab.on("mac4", ("bash", "-s", "--", lab.interface, lab.ips["mac1"],
                             lab.ips["mac2"], lab.ips["mac2"], lab.app),
                    data=CAPTURE, timeout=30)
    raw = output.with_suffix(".pcap")
    raw.write_bytes(base64.b64decode(result.stdout))
    tshark = shutil.which("tshark") or "/Applications/Wireshark.app/Contents/MacOS/tshark"
    capture = output.with_suffix(".pcapng")
    run((tshark, "-r", raw, "-F", "pcapng", "-w", capture))
    raw.unlink()
    summary = run((tshark, "-r", capture, "-Y", "dns or tcp.flags.syn == 1 or tls",
                   "-T", "fields", "-e", "frame.number", "-e", "tcp.stream", "-e", "ip.src",
                   "-e", "ip.dst", "-e", "_ws.col.Protocol", "-e", "_ws.col.Info"))
    output.with_suffix(".txt").write_text(result.stderr + "\n" + summary.stdout)
    for term in ("Standard query response", "[SYN]", "[SYN, ACK]", "Client Hello",
                 "Server Hello", "Certificate", "Application Data"):
        require(term in summary.stdout, f"Missing {term} in {capture}")
    print(capture)


if __name__ == "__main__":
    main()
