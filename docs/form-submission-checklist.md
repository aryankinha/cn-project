# Final submission checklist

Use Sections 6–10 of the supplied course brief. The final presentation is a
live demonstration and individual viva. Keep the project configuration,
report, and indexed evidence available during the evaluation.

| Requirement | Submission material | Latest verified status |
| --- | --- | --- |
| Topology, role and IP inventory, protocol flow | [Architecture](architecture.md), live `./scripts/demo.sh who` and `./scripts/demo.sh baseline` | Four hosts inventoried. The recorded directed ping matrix was 9/12. Mac 1 stealth mode explains the three inbound failures. |
| Config bundle and backend source | [DNS guide](../dnsmasq/README.md), [TLS notes](tls-setup.md), [runbook](phase2-runbook.md), committed nginx and pf templates and Flask source | Four-node deployment verified. Keep the live inventory and TLS private keys local. |
| Phase 1 DNS, HTTPS, balancing, caching, packet flow | [Final smoke](../evidence/phase2/final-smoke.txt), [evidence index](../evidence/phase2/README.md) | Both names, both backends, trusted HTTP/1.1, conditional 304, and LAN packet evidence verified. Mac 4 is the verified additional client. Mac 3 still needs its project DNS and trust configuration verified. |
| Phase 1 five failure scenarios | [Failure checklist](phase1-failure-tests.md) | Four observed. Intentional wrong-client-DNS and recovery still require confirmation. |
| Phase 2 A and B | [Backup DNS](../evidence/phase2/extension-a.txt), [TTL and manual flush](../evidence/phase2/extension-b-manual-flush.txt) | Passed with verified recovery. |
| Phase 2 C | [Isolation instructions and evidence](../evidence/phase2/README.md) | The current direct probes still reached both backend ports from Mac 1. Run the owner-assisted deny/allow/rollback demonstration and save the results. |
| Phase 2 D, E and F | [Evidence index](../evidence/phase2/README.md) | Backend failover, DNS cutover with recovery, and troubleshooting passed. Repeat the standby path with the authorized firewall profile during the joint C/E check. |
| Final report and presentation | [Final report](phase2-report.md), [demo sequence](demo-commands.md), [viva preparation](viva-preparation.md) | Materials are indexed. Each member participates and answers viva questions. |

Use the [runbook](phase2-runbook.md) to collect any outstanding evidence
before marking the corresponding row complete on the submission form.
