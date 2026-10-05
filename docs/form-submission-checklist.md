# Phase I checklist and project review

Reviewed against all 12 pages of `CN_Project_Doc.pdf`, especially Sections 6.1–6.3, 9 and Review 1 in Section 10, on 5 October 2026. Checked boxes indicate saved evidence or completed repository work. Unchecked boxes indicate evidence or live evaluation work that remains; team confirmation alone is not direct verification.

The Phase I working-system gate is demonstrated from Aryan's Mac: resolve the private name, validate HTTPS and receive both backend responses through the edge. The complete mandatory evidence/failure checklist is still incomplete. Successful checks below were collected in the earlier live session, not rerun during this file cleanup.

| Mac | Member | Enrollment | Role | Private IP / service port |
| --- | --- | --- | --- | --- |
| 1 | Aryan Kinha | 2401020013 | Private DNS + test client | `10.7.23.16`, UDP/TCP 53 |
| 2 | Divyanshu Singh | 2401010161 | nginx edge, TLS termination, round-robin load balancer | `10.7.20.249`, TCP 80 / 443 |
| 3 | Jatin Verma | 2401010200 | Backend A | `10.7.16.92`, TCP 3001 |
| 4 | Jatin Kumar Singh | 2401010199 | Backend B + test client | `10.7.22.187`, TCP 3002 |

## A — Private LAN and topology

- [x] Four Macs, named owners, enrollment numbers, service roles and IP/port table documented.
- [x] Network topology and protocol request-flow diagrams included in [architecture](architecture.md).
- [x] Aryan inventory: 10.7.23.16/19, mask 255.255.224.0, gateway 10.7.0.1, interface en0, MAC 2e:a3:0c:b9:e7:1a.
- [x] Mac 1 reached Macs 2, 3 and 4 by ping; the edge sample had packet loss, which is documented.
- [ ] Record interface, prefix/mask, gateway and MAC address from each of Macs 2–4.
- [ ] Save ping results for the remaining machine pairs/directions. Mac 1 results alone do not prove full pairwise reachability.

## B — Private DNS

- [x] dnsmasq configuration includes app.team.test and api.team.test → 10.7.20.249, TTL 30.
- [x] Both names verified with dig; Aryan's default resolver works.
- [x] DNS answer, query/response and TTL evidence saved.
- [x] Final application requests use domain names; direct IP requests are backend diagnostics.
- [ ] Save default-resolver settings and plain dig results on at least two other Macs. The team confirmed all three use Aryan's DNS, but remote logs are unavailable.

## C — Backend A and Backend B

- [x] Minimal shared REST source in [backend/app.py](../backend/app.py).
- [x] Launch helper selects A/3001 or B/3002; source binds to 0.0.0.0.
- [x] Both backends are LAN-accessible and return 200 for `/` and `/api/status`.
- [x] JSON identifies the backend and responses contain X-Backend A/B.
- [x] Dependency file and launch instructions included.

## D — Edge and load balancing

- [x] Divyanshu's Mac 2 is the edge; both upstream IPs/ports match the architecture.
- [x] Template matches the team-supplied configuration, including HTTP/2 and edge-Mac certificate paths.
- [x] Repeated HTTPS responses show B/A/B/A/B/A; final HTTP smoke requests show B/A/B/A/B.
- [x] Local nginx syntax/certificate-loading validation passed after local path substitution.
- [ ] Independently export the loaded remote configuration (`nginx -T`) for reproducibility; the supplied snippet is retained as team-provided configuration, not a remote inspection.

## E — HTTPS and TLS

- [x] Self-signed RSA-2048/SHA-256 certificate generated with both domain SANs.
- [x] Certificate/key match, validity, fingerprint and hostname checks recorded.
- [x] Edge serves HTTPS on 443 with TLS 1.2/1.3; plain curl on Aryan's Mac validates the certificate without -k or an explicit CA override.
- [x] HTTP/1.1 tested; HTTP/2 negotiated successfully.
- [x] TLS installation/trust notes included; private key remains local, ignored by Git and mode 600.
- [ ] Verify trust on every other Mac used as a client. Browser evidence is optional when valid curl evidence is used, but other client trust is not established by Aryan's result.

## F — HTTP caching

- [x] `/api/cache` supplies Cache-Control: public, max-age=60 and ETag: "cn-cache-v1".
- [x] Live response headers saved using HEAD.
- [x] Matching If-None-Match returns 304; this satisfies the conditional-response alternative to a fresh cache-hit demo.
- [ ] During viva, explain a fresh cache hit, conditional revalidation and a full response; curl does not automatically cache these requests.

## G — Complete protocol flow and transport explanation

- [x] Final 58-packet capture saved as [phase1-final-flow.pcapng](../evidence/phase1/phase1-final-flow.pcapng).
- [x] DNS query/answer and edge IP shown; DNS TTL details screenshot included.
- [x] Edge SYN → SYN-ACK → ACK shown, with client ephemeral port 54008 and server 443.
- [x] TLS 1.2 ClientHello/SNI, ServerHello, Certificate, ChangeCipherSpec and encrypted records visible.
- [x] Additional TLS 1.3 stream captured; its encrypted certificate is not mislabeled as plaintext.
- [x] Request/response headers saved using verbose curl; A/B response identifiers and cache headers recorded.
- [x] Four real Wireshark screenshots included; filtered-view frame renumbering explained in [evidence index](../evidence/phase1/README.md).
- [ ] Each member must explain socket pairs, sequence/ACK numbers, TCP reliability, receive window and retransmission using the recorded packets.

## Section 6.3 — Required failures and recovery

These are Phase I requirements even though Phase II later extends resilience. Expected outcomes in the [failure guide](phase1-failure-tests.md) are not measured results.

- [ ] Wrong DNS server configured on a client: show lookup failure despite IP reachability, then restore the resolver and verify recovery. A public-resolver NXDOMAIN probe is saved but does not show changing the client setting.
- [ ] Wrong served DNS IP: show successful lookup to the incorrect address and failed application access, then restore the record and verify recovery.
- [ ] Stop Backend A: record edge behavior with B only; restart A and verify A/B recovery.
- [ ] Stop both backends: show DNS/TLS at the edge still work while the application returns an upstream failure; restart both and verify 200.
- [ ] Wrong destination port: the saved port-65534 refusal demonstrates the failure; add a complete paired IP-reachability/correct-port recovery record for the controlled demonstration.
- [x] Negative diagnostic outputs and a later successful healthy baseline are retained separately.

No authenticated remote-control session is configured for the other Macs, so the remote inspection and backend stop/restart requirements could not be completed from this Mac.

## Section 9 — Deliverables and review readiness

- [x] Architecture document: topology, team/IP/service table and request flow.
- [x] Configuration bundle: DNS template, nginx template, TLS setup and backend launch instructions.
- [x] Complete backend source and helper scripts available locally; a zip is an allowed sharing option, so a commit is not required by this review.
- [x] Evidence index links successful DNS/HTTP/TLS/cache results, captures and four screenshots.
- [x] 5:00 [command/Wireshark video](../video/README.md) with subtitles and no audio; current timeouts and missing controlled failures are explicit.
- [x] Structured [demo commands](demo-commands.md), [speaking script](phase1-video-script.md) and troubleshooting runbook included.
- [ ] Complete missing remote evidence and controlled failure demonstrations before claiming every Phase I requirement is satisfied.
- [ ] All four members participate in the live review and can explain every component independently.
- [ ] Deliver the repository/zip by the faculty's requested method and make evidence easy to locate within 30 seconds.

HTTP/3 and email protocols are explanation-only. Backup DNS, DNS TTL migration experiments, backend firewall isolation, standby-edge cutover and the Phase II final report are outside this Phase I checklist. No five-minute video limit or separate submission form is imposed by this PDF.

## Cleanup completed

Removed files that are unnecessary for this team's Phase I submission:

- Old cloned `evidence/reference-original/` screenshots and outputs.
- Empty placeholder `evidence/task-a/` through `task-g/` folders.
- Unfiltered `evidence/local-raw/` captures.
- Superseded initial/HTTP/TLS-retry captures and the extra direct-Backend-A handshake screenshot.
- Stale `evidence/phase1/demo-command-output.md` pointer to early failures.

Kept final source/configuration/scripts, certificate and local key, local team settings, four required screenshots, architecture image, the final TLS capture, the capture behind the DNS screenshots, successful verification logs and historical text logs documenting actual failures. Updated stale runbook statements and removed links to deleted files. No Git commit was created.

## Review 1 marks

| Area | Marks |
| --- | --- |
| LAN + private DNS (A+B) | 10 |
| REST + reverse proxy + balancing (C+D) | 10 |
| HTTPS/TLS (E) | 8 |
| Packet analysis (G) | 7 |
| Caching + transport understanding (F) | 5 |
| Individual viva | 10 |
| Total | 50 |

See the [full results report](phase1-results.md) for the saved working-system outcomes and limits.
