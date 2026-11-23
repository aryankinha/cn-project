"""Report the earliest failing layer with source-specific evidence."""
import argparse
import sys

from cnlib import Lab, NODES, headers


def diagnose(lab, source="mac1", port=443):
    def fail(layer, detail):
        print(f"FIRST FAILING LAYER: {layer} — {detail}", flush=True)
        return layer

    ip = lab.on(source, ("ipconfig", "getifaddr", lab.interface), check=False).stdout.strip()
    if ip != lab.ips[source]:
        return fail("LAN", f"{source}/{lab.interface} address is {ip!r}; expected {lab.ips[source]}")
    for node in ("mac1", "mac2"):
        print(f"DNS {node}: {lab.query(node, lab.app, source=source)}")
    result = lab.on(source, ("dscacheutil", "-q", "host", "-a", "name", lab.app), display=True)
    addresses = [line.split()[1] for line in result.stdout.splitlines() if line.startswith("ip_address:")]
    if not addresses:
        return fail("DNS", "system resolver returned no address")
    target = addresses[0]
    if target not in (lab.ips["mac2"], lab.ips["mac3"]):
        return fail("DNS", f"{lab.app} points to unexpected address {target}")
    ping = lab.on(source, ("ping", "-q", "-c", "1", "-t", "2", target), check=False)
    print(f"ICMP exit={ping.returncode}; TCP will independently check reachability")
    tcp = lab.on(source, ("nc", "-vz", "-G", "3", target, port), check=False, display=True)
    if tcp.returncode:
        observation = tcp.stderr.strip() or tcp.stdout.strip()
        return fail("TCP", f"{target}:{port}: {observation}. Check the expected listener and network path.")
    response = lab.on(source, ("curl", "--noproxy", "*", "--http1.1", "-svS", "--max-time",
                      "8", "--resolve", f"{lab.app}:{port}:{target}", "-D", "-", "-o",
                      "/dev/null", f"https://{lab.app}:{port}/api/status"),
                      check=False, display=True)
    if response.returncode in (35, 51, 58, 59, 60, 77, 83, 90, 91):
        return fail("TLS", f"hostname/peer validation or handshake failed (curl {response.returncode})")
    if response.returncode:
        return fail("HTTP", f"request failed after the TCP check (curl {response.returncode}); inspect TLS trace")
    code, fields = headers(response)
    if code in (502, 503, 504):
        edge = "mac2" if target == lab.ips["mac2"] else "mac3"
        for backend, address in (("A", "127.0.0.1" if edge == "mac3" else lab.ips["mac3"]),
                                 ("B", lab.ips["mac4"])):
            result = lab.on(edge, ("curl", "--noproxy", "*", "-fsS", "--max-time", "4",
                                   f"http://{address}:{lab.ports[backend]}/api/status"),
                            check=False, display=True)
            print(f"{edge} → Backend {backend}: curl exit {result.returncode}")
        lab.on(edge, ("tail", "-n", "8", lab.runtime(edge) / "logs/nginx-error.log"),
               check=False, display=True)
        return fail("Upstream", f"edge returned HTTP {code}; compare backend probes with the upstream log")
    if code != 200 or fields.get("x-backend") not in ("A", "B"):
        return fail("HTTP", f"unexpected response HTTP {code} with headers {fields}")
    print(f"Healthy: {target} {fields.get('x-edge')} backend={fields.get('x-backend')}")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=NODES, default="mac1")
    parser.add_argument("--port", type=int, default=443)
    args = parser.parse_args()
    sys.exit(bool(diagnose(Lab(), args.source, args.port)))
