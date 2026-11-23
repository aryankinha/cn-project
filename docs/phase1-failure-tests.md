# Phase 1 controlled failures

Run `./scripts/demo.sh phase1` on Mac 1 during the demonstration window.
It exercises the four controller-managed scenarios below and verifies
recovery. For the client-only prerequisite, use the separate command after
the client owner has set up and deliberately changed the DNS profile.

| Scenario | Verify |
| --- | --- |
| Wrong served record | Both resolvers return the unintended address. Restore the record and verify normal HTTPS. |
| Backend A down | Requests remain HTTP 200 and identify only B. Restore A and verify both identities. |
| Both backends down | DNS resolves and TLS validates, while nginx returns 502. Restore both backends and verify 200. |
| Wrong destination port | The TCP connection is refused. Retry the correct port and verify trusted HTTPS. |

For **wrong client DNS**, first confirm a normal named request from Mac 3.
Have the owner select a resolver without the private zone and flush cached
answers. On Mac 1, run `./scripts/demo.sh phase1-client`. It requires a failed
system lookup and successful hostname-validated HTTPS pinned to the primary
edge, proving the network and service still work. Restore the team client
profile on Mac 3 and rerun `./scripts/demo.sh phase1-client --restored`.
See [client setup and restoration](phase2-runbook.md#resolver-setup).

[Controlled-run evidence](../evidence/phase2/phase1-controlled-failures.txt) ·
[Wrong-port and recovery evidence](../evidence/phase2/wrong-port.txt)
