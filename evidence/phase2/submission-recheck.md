# Submission recheck

Read-only checks on 24 November 2026, IST, after the recorded backup DNS and
manual cache-flush drills.

| Check | Observed |
| --- | --- |
| Four-Mac controller smoke | Both team DNS servers answered for both names over UDP and TCP. Both HTTPS edges returned alternating A/B identities with verified TLS. Both names redirected from HTTP to HTTPS. Cache revalidation returned 304. |
| Updated standalone smoke | Both names resolved and served HTTP/1.1 200. Six named requests alternated A/B, then cache revalidation returned 304. |
| Additional clients | Mac 4 listed both team resolvers and returned named HTTPS 200. Macs 2 and 3 still listed earlier resolver settings and failed ordinary lookup for the private app name. |
| Firewall baseline | Mac 1 and Mac 2 each received direct HTTP 200 from both backend ports. Both backend owners' SSH sessions required administrator authentication to inspect active pf state. No strict-profile denial and rollback run was available for this recheck. |
| Inbound ICMP | Pings from Macs 3 and 4 to Mac 1 again received no replies. Mac 1's earlier recorded stealth-mode setting explains the pattern. |
