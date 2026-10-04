# Phase I demonstration commands

Run from the repository root. Save actual output with machine name, date, command and result. HTTPS steps depend on the [TLS installation](tls-setup.md).

## A — LAN inventory and reachability

On every Mac:

```bash
ifconfig
route -n get default
```

Record IPv4, mask/prefix, interface, MAC address and gateway. Ping each of the other three team IPs with `ping -c 4 <IP>`. This requires logs from all four Macs.

## B — Private DNS

On at least two other Macs configured to use Aryan's DNS:

```bash
scutil --dns
dig app.team.test
dig api.team.test
```

On any Mac, an explicit query is a useful diagnostic:

```bash
dig @10.7.23.16 app.team.test
dig @10.7.23.16 api.team.test
```

Expect edge `10.7.20.249`; record the actual TTL. Names and default-resolver behavior must also work without explicitly selecting a DNS server.

## C — Backends

Mac 3: `./scripts/run-backend.sh A`. Mac 4: `./scripts/run-backend.sh B`.

```bash
curl -i http://10.7.16.92:3001/
curl -i http://10.7.16.92:3001/api/status
curl -i http://10.7.22.187:3002/
curl -i http://10.7.22.187:3002/api/status
```

Direct backend access is diagnostic evidence. The final application demo uses the edge domain.

## D and E — Edge, trusted HTTPS and distribution

On Mac 2 inspect `nginx -T` (keep private-key contents out of logs). On a trusted client:

```bash
curl -v https://app.team.test/
curl --http1.1 -I https://app.team.test/api/status
for i in 1 2 3 4 5 6; do
  curl --connect-timeout 3 --max-time 10 -sS -D - https://app.team.test/api/status
  echo
done
```

Show successful certificate validation and both `X-Backend: A` and `X-Backend: B`. Other concurrent requests can affect strict alternation. HTTP/2 is optional: first check `curl -V` and nginx support, then try `curl --http2 -I https://app.team.test/api/status` and record the actual negotiated version.

## F — Cache headers and conditional response

```bash
curl -I https://app.team.test/api/cache
curl -i -H 'If-None-Match: "cn-cache-v1"' https://app.team.test/api/cache
```

Expect Cache-Control `public, max-age=60`, the ETag and a conditional 304 if deployed code matches the repository. curl does not automatically cache responses. A 304 is revalidation, not a fresh cache hit. A full new request returns a body. A browser fresh cache hit can avoid contacting the server while the representation remains fresh.

## G — One protocol flow in Wireshark

Capture `lo0` and `en0` on Aryan's Mac before running DNS and HTTPS commands. From Mac 4 use its LAN interface; this provides a cross-machine DNS query as well.

```bash
dig app.team.test
curl --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status
```

Save the pcapng. Select filters for this team's names/IPs, determine the actual TCP stream number, and take screenshots with the packet list and expanded details visible:

| Evidence | Display filter |
| --- | --- |
| DNS query/response | `dns.qry.name == "app.team.test"` |
| DNS answer / TTL | same filter; select the response and expand Answers |
| Edge TCP stream | `ip.addr == 10.7.20.249 && tcp.port == 443` then `tcp.stream eq N` |
| TLS | `tcp.stream eq N && tls` |

A SYN-only filter excludes the final ACK and cannot demonstrate the entire handshake. Record frame numbers, ephemeral client port, edge port, TCP sequence/ACK numbers, DNS transaction ID, SNI and negotiated TLS version. TLS 1.2 full handshake is useful for visible Certificate; TLS 1.3 hides it after ServerHello. HTTP headers are shown separately with curl because encrypted HTTPS payload is unreadable in an ordinary capture.

## Required failures

Follow [all five Phase I failure tests](phase1-failure-tests.md). Record before, after, affected layer and restoration; do not describe unperformed failures as successes.
