# Final demonstration commands

Run these from the checkout on Mac 1. For the exact owner-side prerequisites,
restoration commands and packet frames, keep the [runbook](phase2-runbook.md)
and [evidence index](../evidence/phase2/README.md) open.

| Step | Show |
| --- | --- |
| 1–2 | Open the [topology](architecture.md), then run `./scripts/demo.sh who` and `./scripts/demo.sh baseline`. |
| 3–5 | Run `./scripts/smoke-test.sh team.test` from a configured client and show DNS, trusted HTTPS and both backend IDs. |
| 6–7 | Open the indexed LAN capture and show the DNS answer, TCP handshake and TLS records. Show the matching HTTP headers and cache 304 in the smoke output. |
| 8 | Run `./scripts/demo.sh D` to stop A, show B-only responses and verify A returns. |
| 9 | Run the selected A, B, C and E demonstrations using the runbook. C and the cache-flush portion of B need owner-side authorization. |
| 10 | Use `./scripts/demo.sh diagnose` for the faculty fault. The rehearsal is `./scripts/demo.sh F`. |
| 11 | Walk through [viva preparation](viva-preparation.md). |

The [Phase 1 failure checklist](phase1-failure-tests.md) gives the intentional
failure and recovery commands for Section 6.3.
