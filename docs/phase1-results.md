# Phase I results — Aryan Kinha and team

Final verification: 5 October 2026, approximately 02:46–02:59 IST. All observations were collected from Aryan's Mac. The final DNS/HTTP/HTTPS smoke test passed, the root endpoint returned 200, and cache revalidation returned 304. The working service is verified; the complete Phase I submission evidence remains incomplete because remote inventory, resolver and controlled-failure evidence is unavailable.

## Team and architecture

| Member | Enrollment | Mac / role | LAN endpoint |
| --- | --- | --- | --- |
| Aryan Kinha | 2401020013 | Mac 1: private DNS and test client | 10.7.23.16:53 UDP/TCP |
| Divyanshu Singh | 2401010161 | Mac 2: nginx, TLS termination, round-robin edge | 10.7.20.249:80/443 TCP |
| Jatin Verma | 2401010200 | Mac 3: Backend A | 10.7.16.92:3001 TCP |
| Jatin Kumar Singh | 2401010199 | Mac 4: Backend B and test client | 10.7.22.187:3002 TCP |

![Four-Mac architecture](images/phase1-architecture.png)

Both app.team.test and api.team.test resolve to Divyanshu's edge with TTL 30. A client resolves the name, establishes TCP to port 443, validates the TLS certificate, and sends encrypted HTTP. nginx terminates TLS and forwards plaintext HTTP to one backend. Client roles share the four service Macs. The team confirmed the other three Macs use Aryan's DNS; their local resolver logs were not independently collected.

## Requirement-by-requirement outcome

| Phase I task | Actual result | Completion limit |
| --- | --- | --- |
| A: LAN | Aryan inventory: en0, 10.7.23.16/19, gateway 10.7.0.1, MAC 2e:a3:0c:b9:e7:1a. All three remote IPs answered ping. | Remote full inventory and remaining pairwise directions unverified. Edge two-packet sample had 50% loss. |
| B: DNS | Both names return 10.7.20.249, TTL 30. Aryan's default local resolver works. DNS packet answer and TTL screenshots saved. | Default resolver evidence from at least two other Macs unverified. |
| C: REST backends | Both `/` and `/api/status` return 200 directly on their LAN IPs with correct X-Backend A/B. | Confirms LAN accessibility; remote process/listener inventory not exported. |
| D: nginx/load balancing | Six HTTPS requests returned B, A, B, A, B, A. Final smoke HTTP requests returned B, A, B, A, B. | Actual loaded remote nginx config not exported. |
| E: TLS | Plain HTTPS validates hostname/certificate without -k or explicit CA override on Aryan's Mac; TLS 1.2 and 1.3 return 200. | Browser and other client trust stores unverified. |
| F: caching | `/api/cache` returns Cache-Control: public, max-age=60 and ETag: "cn-cache-v1"; matching If-None-Match returns 304. | A 304 is revalidation; no browser fresh-cache-hit claim. |
| G: packet analysis | 58-packet final capture contains DNS, full edge TCP handshake, TLS 1.2 visible certificate/CCS, encrypted data and TLS 1.3. Four reviewed Wireshark screenshots included. HTTP headers saved in client logs. | HTTPS headers cannot be read from the encrypted capture without decryption. |
| Section 6.3 failures | Public resolver returns NXDOMAIN; wrong port 65534 refuses. Healthy baseline succeeds afterward. | These probes do not complete the five controlled scenarios. Wrong client DNS setting, wrong served record, one backend stopped, both stopped and their recovery sequence remain unverified. |

HTTP/1.1 returned 200 and HTTP/2 was negotiated successfully. The api.team.test HTTPS endpoint also returned 200. Intermittent LAN/edge timeouts and retransmissions were observed before the final successful capture and smoke test; no definitive cause was established. The final successful result does not erase that instability.

## Certificate and configuration

The generated self-signed RSA-2048/SHA-256 certificate covers both private names, uses serverAuth and CA:FALSE, and is valid 5 October 2026–5 October 2027 IST. Its SHA-256 fingerprint is:

```text
CB:36:4B:3F:99:C1:D3:57:B3:7E:D7:5B:5B:93:B8:70:94:8F:8E:59:21:3F:BB:01:44:7C:80:2A:8E:13:B0:79
```

[Public certificate](../tls/edge.crt), [TLS setup](tls-setup.md) and [certificate/config verification](../evidence/phase1/tls-artifact-verification.md) are included. The matching private key is local, mode 600 and ignored by Git. The team installed the certificate on the edge; live HTTPS presents it. The prepared nginx template passed a local syntax check with substituted paths.

## Evidence to open during review

- [Full live rerun](../evidence/phase1/final-verification-2026-10-05.md)
- [Final passing smoke test](../evidence/phase1/latest-smoke-test-2026-10-05.md)
- [Latest default-trust root/cache checks](../evidence/phase1/latest-root-cache-2026-10-05.md)
- [Successful captured TLS requests](../evidence/phase1/last-capture-requests-2026-10-05.md)
- [Primary packet capture](../evidence/phase1/phase1-final-flow.pcapng)
- [Evidence index with frame analysis and all screenshots](../evidence/phase1/README.md)

![DNS answer and TTL](../evidence/phase1/screenshots/dns-answer-details.png)

![Complete edge TCP handshake](../evidence/phase1/screenshots/tcp-three-way-handshake.png)

![TLS handshake and encrypted application records](../evidence/phase1/screenshots/tls-stream-overview.png)

The fourth screenshot, [DNS query/response](../evidence/phase1/screenshots/dns-query-response.png), is also embedded in the evidence index. DNS screenshots use an earlier successful DNS exchange during an edge timeout; TCP/TLS screenshots use the final successful capture. Read-filtered Wireshark views renumber packets; the evidence index maps full-file frames precisely.

## Documentation delivered

README, four-Mac architecture and diagram, team configuration, DNS guide/template, nginx TLS template, TLS setup guide, smoke test, demo commands, presentation script, runbook, requirement checklist, failure-test guide and evidence index now describe this team. Original cloned screenshots and logs remain clearly labeled under `evidence/reference-original/`; actual historical outputs are preserved unchanged.

No remote-control credentials/session are configured for the other Macs, so remote-local inspection and stopping/restarting their backend processes could not be performed from here. Missing checks are explicitly marked rather than represented as completed. Phase II backup DNS, firewall isolation and migration remain outside this report.
