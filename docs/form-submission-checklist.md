# Phase I deliverable checklist

Based on `CN_Project_Doc.pdf`, Sections 6 and 9 and Review 1 in Section 10. No separate form was provided; this is a requirements checklist, not invented submission answers.

| Mac | Member | Enrollment | Role | Private IP / service port |
| --- | --- | --- | --- | --- |
| 1 | Aryan Kinha | 2401020013 | Private DNS + test client | `10.7.23.16`, UDP/TCP 53 |
| 2 | Divyanshu Singh | 2401010161 | nginx edge, TLS termination, round-robin load balancer | `10.7.20.249`, TCP 80 / 443 |
| 3 | Jatin Verma | 2401010200 | Backend A | `10.7.16.92`, TCP 3001 |
| 4 | Jatin Kumar Singh | 2401010199 | Backend B + test client | `10.7.22.187`, TCP 3002 |

| Requirement | Current evidence / status |
| --- | --- |
| A: Four-machine topology | [Architecture](architecture.md) complete |
| A: All IPv4, prefixes, gateways, interfaces, MACs | Aryan verified; remote details pending |
| A: Pairwise ping | Mac 1→2/3/4 verified; other directions pending |
| B: app/api private DNS | Both verified, edge 10.7.20.249, TTL 30 |
| B: At least two other client resolver settings | Team-confirmed for all three; remote scutil/plain dig logs pending |
| C: Two LAN-accessible backends and identifiers | Direct status responses verified on 3001/3002; root endpoint responses verified |
| D: nginx and A/B load balancing | HTTP A/B alternation verified by latest smoke test; HTTPS A/B responses also observed |
| E: Certificate / trusted HTTPS | Certificate installed; plain HTTPS/default client trust verified on Aryan’s Mac; browser and other client trust unverified |
| F: Cache-Control and 304/cache hit | Live Cache-Control, ETag and conditional 304 verified |
| G: DNS/TCP/TLS/ports/HTTP headers | Fresh DNS and complete edge TCP/TLS captures; four reviewed Wireshark screenshots included |
| Section 6.3: Five failures + recovery | Wrong-resolver/closed-port probes saved; five controlled scenarios remain incomplete; [details](phase1-failure-tests.md) |
| Configuration bundle | DNS config, nginx config, TLS notes, source and launch scripts included; obtain actual loaded nginx config after setup |
| Evidence folder | Fresh results separated from cloned reference evidence |
| Structured live demonstration | [Commands](demo-commands.md) and [speaking script](phase1-video-script.md) |
| Every member understands all components | Prepare DNS, TCP, TLS, HTTP, caching and load balancing explanations |

See [full results and evidence links](phase1-results.md). Final smoke test passed; intermittent earlier LAN/edge timeouts are recorded.

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

Keep evidence discoverable within 30 seconds. Supply the repository/zip and any faculty-requested submission links only after actual collection. Do not invent timestamps, packet numbers, successful pings, certificate validation or failure results. Phase II extensions and its final report are outside this update.
