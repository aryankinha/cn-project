# Phase I required failures — Section 6.3

Status: pending coordinated execution. Complete after the baseline trusted HTTPS demo works. Keep original configuration copies, change one thing at a time, and restore immediately after recording each test. The PDF specifies these failures; it does not authorize silently changing other members' services.

| Failure | Controlled action | Expected observation | Restoration / evidence |
| --- | --- | --- | --- |
| Wrong DNS on a client | Temporarily select an agreed non-project DNS resolver on a test client | Private lookup fails while direct IP ping still works; DNS-layer fault | Restore 10.7.23.16, clear cache if needed, show plain dig works |
| DNS record points to wrong IP | Aryan temporarily changes the app record to an agreed unused LAN IP | Lookup returns wrong IP; HTTPS cannot reach intended edge; directory correctness differs from connectivity | Restore 10.7.20.249, restart dnsmasq, account for TTL/cache, verify recovery |
| One backend stopped | Jatin Verma stops his Backend A process | Edge may continue via B with configured passive failover; record errors as well as successes | Relaunch `./scripts/run-backend.sh A`; allow fail_timeout, show A/B distribution resumes |
| Both backends stopped | Both backend owners stop their project processes | DNS and edge TCP/TLS remain available; nginx returns upstream failure, typically 502 | Relaunch A and B; show HTTP 200 through trusted HTTPS |
| Wrong destination port | Request the same domain on a confirmed closed TCP port | DNS/IP reachability works, TCP is refused or times out; TLS/HTTP cannot begin | Restore correct URL and demonstrate HTTPS success |

Use the terminal running each backend to stop it with Ctrl-C. Avoid killing unidentified processes. Keep nginx running for the backend failures. Do not use 443 as the deliberately wrong port until 443 has been proved working in the baseline.

For every test store command output or screenshots, date/time, client identity, changed setting, measured result, layer explanation and recovery proof. A connection refusal found during setup is troubleshooting evidence, not proof of a deliberately performed failure with a healthy baseline.
