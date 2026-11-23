# Final demonstration commands

Run these from the checkout on Mac 1. For the exact owner-side prerequisites,
restoration commands and packet frames, keep the [runbook](phase2-runbook.md)
and [evidence index](../evidence/phase2/README.md) open. Run `./scripts/demo.sh`
for the menu and `./scripts/demo.sh present` to rehearse the read-only walkthrough.

| Step | Show |
| --- | --- |
| 1–2 | Open the [topology](architecture.md), then run `./scripts/demo.sh present` for live roles and status. Use `./scripts/demo.sh baseline` for the full directed ping matrix. |
| 3–5 | Run `./scripts/smoke-test.sh team.test` from a configured client and show DNS, trusted HTTPS and both backend IDs. |
| 6–7 | Open the indexed LAN capture and show the DNS answer, TCP handshake and TLS records. Show the matching HTTP headers and cache 304 in the smoke output. |
| 8 | Run `./scripts/demo.sh D` to stop A, show B-only responses and verify A returns. |
| 9 | Run the selected A, B, C and E demonstrations using the runbook. Macs 3 and 4 must apply the C rules first. On Mac 1, run `sudo -v` and then `./scripts/demo.sh B --flush` for the cache-flush step. |
| 10 | Use `./scripts/demo.sh diagnose` for the faculty fault. The rehearsal is `./scripts/demo.sh F`. |
| 11 | Walk through [viva preparation](viva-preparation.md). |

The [Phase 1 failure checklist](phase1-failure-tests.md) gives the intentional
failure and recovery commands for Section 6.3.
