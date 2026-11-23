# Phase 2 runbook

Run controller commands in the existing Git checkout on Mac 1. The deployed
role files live under each owner's `~/cn-project`. Mac 1 runs locally and the
others use existing non-interactive SSH with verified host keys.

## Deployment

```sh
./scripts/deploy.sh --check
./scripts/deploy.sh --all --dry-run
./scripts/deploy.sh --all
./scripts/demo.sh who
./scripts/demo.sh check
```

Use `./scripts/deploy.sh --node mac2` for a role-specific refresh. The
controller snapshots effective configuration, service identity, listeners,
resolver settings, and certificate metadata before activation. Private
snapshots are in the ignored `evidence/local-raw/` directory. The original
files and active-service list are retained inside each release's `previous/`
directory. Staging validates nginx against the cert and key already installed
on the edge. Backend dependency setup runs before activation.
A fresh edge must have the existing team TLS files provisioned by its owner
in the project TLS directory before staging can validate nginx. Keep private
keys out of release bundles and use protected owner-to-owner transfer only
when a new edge actually needs the key. The manual backend launcher accepts
a separate setup step (`./scripts/run-backend.sh --setup`) before A or B.


For manual release rollback on an affected node, set `release` to the
specific activated release directory under `~/cn-project/releases/`, then
run `bash "$release/activate.sh" rollback "$release"`. Verify the nodes
with `./scripts/demo.sh check`. Preserve the active edge master during config
rollback. A stopped nginx edge starts through the logged-in owner's Terminal
when the command comes from SSH. Check `~/cn-project/logs/edge-terminal-start.log`
if the owner session cannot start the process.

## Resolver setup

Macs 1 and 4 are the working baseline clients. On Mac 3 or Mac 2, inspect
`scutil --dns` and `networksetup -getdnsservers Wi-Fi` before changing the
client profile. Have the owner run the following with the two resolver IPv4
addresses from the controller inventory. This saves the previous per-service
setting. The service name is the macOS network service and can differ from the
interface name.

```sh
sudo "$HOME/cn-project/bin/client.sh" apply Wi-Fi PRIMARY_DNS BACKUP_DNS
sudo "$HOME/cn-project/bin/client.sh" restore Wi-Fi
```

Run only the apply line to configure a client. Use restore to undo it. Verify
a regular lookup and HTTPS request before using a newly configured client in
a drill. Review supplemental resolvers and VPN DNS separately. The script
changes DNS settings and flushes caches.

Macs 2 and 3 failed the default-trust client probe. If using either as the
additional course client, confirm the SHA-256 fingerprint of the public
`edge.crt` against the [TLS evidence](../evidence/phase2/tls-verification.txt).
Have the owner import that public certificate in Keychain Access and set
trust for SSL, then verify both names with plain curl. Mac 3 already has
the public certificate in `~/cn-project/tls/edge.crt`. Remove only the
project certificate’s trust entry if the owner later reverses that setup.

## Evaluation order

1. Show the architecture and `./scripts/demo.sh who`.
2. Run `./scripts/demo.sh baseline` for inventory, directed pings, DNS, HTTPS,
   round robin and cache checks. Record any failed direction separately.
3. Resolve the app name on a client and show the answering team resolver.
4. Open the app over trusted HTTPS.
5. Show both backend headers with `./scripts/demo.sh check`.
6. Open the saved LAN capture. Show DNS, SYN/SYN-ACK/ACK, TLS handshake and
   encrypted data. Use `python3 scripts/phase2/capture.py` for a new capture.
7. Show Cache-Control, ETag and 304 in the check log.
8. Run `./scripts/demo.sh D` for eight B-only requests and A recovery.
9. Run the DNS and isolation demonstrations below as selected by faculty.
10. Use `./scripts/demo.sh diagnose` to reason through the injected fault.
11. Answer the individual viva with the capture and service map ready.

## Extension commands and restoration

| Extension | Command on Mac 1 | Recovery and proof |
| --- | --- | --- |
| A | `./scripts/demo.sh A` | Restarts Mac 1 DNS after the Mac 4 packet-backed check. |
| B | `sudo -v` then `./scripts/demo.sh B --flush` in the same authorized terminal | Observes expiry, restores the original DNS record, flushes the local cache and immediately checks the restored answer. Without the flush option the script reports the manual step pending. |
| C | `./scripts/demo.sh C` after owner apply, then `./scripts/demo.sh C --restored` after owner rollback | Verifies allowed and denied access to both backend ports with ordinary HTTPS still working. |
| D | `./scripts/demo.sh D` | Restarts only A, waits for nginx to retry it and asserts round robin again. |
| E | `./scripts/demo.sh E` | Proves both standby upstreams before touching DNS, preserves the API record, restores app DNS and checks convergence back to Mac 2. |
| F | `./scripts/demo.sh F` | Stops the primary project nginx briefly, diagnoses TCP first, and restores named HTTPS. |

For C, owners run these on **both** Mac 3 and Mac 4. Keep the local terminal
available until the central test has completed. Collect backend-side capture
or live rule counters while the test runs.

```sh
sudo "$HOME/cn-project/bin/firewall.sh" apply "$HOME/cn-project/firewall/strict.pf"
sudo "$HOME/cn-project/bin/firewall.sh" status
sudo "$HOME/cn-project/bin/firewall.sh" rollback
```

For the final combined isolation and standby check, apply `standby.pf` on
Mac 3 and Mac 4, then run `./scripts/demo.sh C --standby` and repeat the cutover test. The difference
is the explicit Mac 3 LAN source on Mac 4's Backend B port. The firewall helper
uses a dedicated anchor and one saved pf enable token. Rollback restores the
saved anchor and releases that token. Existing connections can retain pf
state. Generate new TCP connections for verification. A timeout alone does
not establish the cause.

Use `python3 scripts/dns.py app mac2` to return the app record to the primary
when both resolvers currently agree and the app record has been changed.
If they disagree, inspect their saved hosts files and reconcile them before
resuming drills. Leave both edges running while clients converge. A DNS update
does not terminate a client connection that is already open.

For practice, run `./scripts/demo.sh break`, `diagnose`, `answer`, and
`fix` as separate subcommands of `demo.sh`. Keep the local drill state until
`fix` verifies healthy HTTPS. For the original Phase 1 failure drills, run the controller-managed scenarios and
the separate wrong-client-DNS command in the [Phase 1 failure checklist](phase1-failure-tests.md).
