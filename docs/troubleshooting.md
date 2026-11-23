# Troubleshooting

Run `./scripts/diagnose.sh` from Mac 1, or pass `--source mac4` to check
the remote client. Keep the scope narrow and record the first repeatable failure.

| Observation | Next check |
| --- | --- |
| Interface or address differs from inventory | Compare interface, prefix, gateway and current DHCP lease. Validate the IP via a known host identity before editing inventory. |
| Direct queries work, system lookup fails | Compare Wi-Fi DNS, scoped resolvers and VPN overrides. Keep at least two project clients configured with both team resolvers. |
| The name resolves to an unexpected target | Query both project resolvers and compare the reported TTL and A record against the client cache. |
| TCP is refused | Confirm the destination port and the expected listener on the edge. |
| TCP times out | Check both sides of the path, including listener state, packet capture, and firewall counters. ICMP and TCP can disagree. |
| TLS fails | Check SAN for the name, validity period, trust path and the certificate served by the chosen edge. Preserve hostname validation with pinned diagnostics. |
| Edge returns 502/504 | Check the actual upstream addresses and path from the selected edge. Compare nginx error and access logs with direct backend status and backend-side captures. |
| SSH-started edge accepts HTTPS but cannot reach the LAN | The live Mac 2 workers showed “No route to host” while direct shell probes worked. The logged-in Terminal startup restored both backends. Use the deployed node controller with the owner's GUI session available. |
| A returned backend is absent briefly | Passive failure state is request-driven. Watch for A to rejoin, then verify sustained A/B distribution and check retry logs. |

Use `~/cn-project/bin/node.sh status` or `health` on the affected node.
Inspect `~/cn-project/logs/` for project service logs. Recheck ordinary
trusted HTTPS after any targeted repair.
