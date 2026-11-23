# Phase 2 evidence index

Collected on the team LAN on 24 November 2026, IST. Git contains selected
command output with user-specific identifiers redacted in the text exports.
The full operator run logs and effective configuration snapshots are in the
ignored `evidence/local-raw/` directory on Mac 1. Historical evidence remains in
[Phase 1](../phase1/README.md).

| Check | Result | Evidence |
| --- | --- | --- |
| Four-node deployment | Runtime revision `ec69be92e1eb` activated on Mac 4, Mac 3, Mac 2, and Mac 1. Staged configs passed target syntax validation. | [Release log](deployment.txt) |
| Final baseline and regression | Both DNS servers and names, TCP/UDP 53, HTTP redirects, trusted HTTP/1.1, both backend IDs on each edge, cache headers, and conditional 304 passed. Directed ICMP passed 9/12. All three missed directions were toward Mac 1, which has firewall stealth mode enabled. | [Final application checks](final-smoke.txt), [inventory and directed pings](baseline.txt), [ICMP follow-up](icmp-triage.txt) |
| TLS | Both edges serve the original certificate for both SANs. Default trust passed on Mac 1 and Mac 4. Macs 2 and 3 rejected it as clients with their existing trust settings. | [Certificate details](tls-verification.txt), [remote trust probes](client-tls-trust.txt) |
| LAN protocol flow | Mac 4's trace contains the DNS answer in frame 2, SYN/SYN-ACK/ACK in frames 3–5, ClientHello in 6, visible TLS 1.2 Certificate in 9, ChangeCipherSpec in 11 and 13, and encrypted Application Data in 15 and 17. | [Capture](20261124-004103+0530-lan-flow.pcapng), [frame summary and curl trace](20261124-004103+0530-lan-flow.txt) |
| A · Backup DNS | Passed. Mac 1 dnsmasq stopped, Mac 4 captured the backup answer, normal HTTPS returned 200, and primary DNS recovered. | [A log](extension-a.txt) |
| B · TTL | Cached old answer and eventual expiry passed in both directions. Manual flush still requires Mac 1 administrator authorization. | [B log](extension-b.txt) |
| C · Isolation | Open. Mac 1 still received HTTP 200 directly on both backend ports. Both rendered profiles passed syntax validation. Owner apply/status/rollback and denial evidence are pending. | [C assertion](extension-c-attempt.txt), [both direct probes](firewall-probes.txt) |
| D · Failover | Passed. Eight B-only requests succeeded with A stopped. A rejoined, and both IDs rotated again. | [D log](extension-d.txt) |
| E · Edge cutover | Passed with the current LAN policy. The cached client reached the old edge, the fresh client reached the standby, and DNS and HTTPS converged back to Mac 2 after rollback. Recheck under the standby firewall profile after owner activation. | [E log](extension-e.txt) |
| F · Troubleshooting | Passed. The controlled primary edge outage was identified at TCP. The owner-session startup path restored trusted named HTTPS. | [F log](extension-f.txt) |
| Original Phase 1 failures | Wrong served A record, one backend stopped, both stopped with HTTP 502, and wrong destination port were observed. The combined run caught recovery warm-up, and the later baseline passed. A deliberate wrong-client-DNS change still needs owner participation. | [Controlled run](phase1-controlled-failures.txt), [wrong port and healthy retest](wrong-port.txt) |
