# Project submission

## Report

- [IEEE-format report (PDF)](report/project-report.pdf)
- [LaTeX source](report/project-report.tex) and [topology figure](report/figures/topology.png)
- [Architecture and request flow](architecture.md), [course checklist](form-submission-checklist.md) and [presentation commands](demo-commands.md)

To rebuild the report, use a TeX distribution with [IEEEtran](https://ctan.org/pkg/ieeetran) installed.

```sh
cd docs/report
latexmk -pdf -interaction=nonstopmode -halt-on-error project-report.tex
```

## Evidence

| What to show | Files |
| --- | --- |
| DNS query, answer and TTL | [Query/response screenshot](../evidence/phase1/screenshots/dns-query-response.png) · [DNS answer details](../evidence/phase1/screenshots/dns-answer-details.png) |
| TCP and TLS handshakes | [TCP screenshot](../evidence/phase1/screenshots/tcp-three-way-handshake.png) · [TLS screenshot](../evidence/phase1/screenshots/tls-stream-overview.png) |
| One complete client LAN trace | [Wireshark capture](../evidence/phase2/20261124-004103+0530-lan-flow.pcapng) · [Frame summary and curl trace](../evidence/phase2/20261124-004103+0530-lan-flow.txt) |
| Earlier packet recordings | [Successful edge flow](../evidence/phase1/phase1-final-flow.pcapng) · [DNS response during an edge timeout](../evidence/phase1/phase1-dns-edge-timeout.pcapng) |
| HTTPS, backend rotation and HTTP 304 | [Application checks](../evidence/phase2/final-smoke.txt) · [TLS verification](../evidence/phase2/tls-verification.txt) |
| Reachability and controlled failures | [Directed pings](../evidence/phase2/baseline.txt) · [Controlled failures](../evidence/phase2/phase1-controlled-failures.txt) · [Wrong port and recovery](../evidence/phase2/wrong-port.txt) |
| DNS resilience | [Backup resolver](../evidence/phase2/extension-a.txt) · [TTL expiry and manual flush](../evidence/phase2/extension-b-manual-flush.txt) · [Standby cutover](../evidence/phase2/extension-e.txt) |
| Backend resilience and fault diagnosis | [Backend failover](../evidence/phase2/extension-d.txt) · [Diagnosis and recovery](../evidence/phase2/extension-f.txt) |
| Isolation and remaining checks | [Isolation attempt](../evidence/phase2/extension-c-attempt.txt) · [Direct backend probes](../evidence/phase2/firewall-probes.txt) · [Submission recheck](../evidence/phase2/submission-recheck.md) |

The Wireshark screenshots and the complete LAN trace come from different
recorded sessions. Use the frame numbers printed in the report with the
complete LAN trace. The [full evidence index](../evidence/phase2/README.md)
records test outcomes and outstanding owner-assisted checks.

## Reproduce and present

- [DNS and TLS setup](../dnsmasq/README.md) · [Certificate guidance](tls-setup.md) · [Deployment and recovery](phase2-runbook.md)
- [Configuration templates](../nginx) · [Firewall profile template](../firewall/backend.pf.template) · [Backend source](../backend/app.py)
- [Troubleshooting](troubleshooting.md) · [Viva preparation](viva-preparation.md)
