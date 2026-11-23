# Phase 2 report

**Lab date:** 24 November 2026, IST. **Scope:** the team’s four Macs and the original GitHub repository. The Phase 1 evidence from October remains in its original folder.

## Changes from Phase 1

The controller renders matching DNS records and role-specific configurations,
stages a single Git revision on all four Macs, validates files on their target,
and records pre-change snapshots. Mac 1 executes locally. Macs 2–4 use the
existing authenticated SSH identities. nginx has equivalent primary and standby
configs with edge IDs, upstream logs, passive failure handling, and a dedicated
liveness endpoint. Backend A and B use independent process control. The backend
cache response has one shared representation while backend identity remains
visible in its header. Dependency setup is separate from service startup.

The deployment reused the installed certificate and key on both edges. The
live certificate covers app.team.test and api.team.test, expires
23 November 2027 at 17:47 UTC, and has the same SHA-256 fingerprint on both
edges. The certificate check used hostname-preserving pinned requests and the
client’s normal certificate verification. No certificate or key replacement
was needed.

## Results and troubleshooting

See [the evidence index](../evidence/phase2/README.md) for run results and recovery
logs. The strongest operational issue was exposed by the troubleshooting drill:
after an SSH-started nginx master on Mac 2, curl completed TLS but received 502.
The worker logs showed “No route to host” for both upstreams, while direct curl
from Mac 2 reached both backends. Starting the same validated nginx configuration
from the logged-in owner’s Terminal restored upstream traffic. The node
controller now uses the logged-in owner's Terminal when starting a stopped edge
over SSH. Routine refreshes preserve a healthy master for unchanged files and
reload it when nginx configuration changes.

## Learning by extension

**A · Backup DNS.** A cached success alone provides weak failover evidence. The
test stops the primary resolver, checks that it gives no answer, and captures
the backup's reply to a fresh system lookup on Mac 4 before verifying ordinary
HTTPS and primary DNS recovery.

**B · TTL.** A DNS server can serve the new IP while a client still connects to
the old one. A controlled test must start with a fresh cache entry and timestamp
the change on both DNS servers. Manually flushing the cache is a separate,
privileged demonstration.

**C · Isolation.** Mac 3 and Mac 4 need distinct policies because they host
separate backend ports. New TCP connections from the off-host client and from
the authorized edge are necessary evidence. A scoped pf anchor and saved enable
token allow rollback while preserving unrelated rules.

**D · Failover.** nginx can retry a failed upstream connection on the healthy
backend. The failure window also influences the first few requests after
restart. The test observes re-entry before measuring steady-state alternation.

**E · Edge migration.** The hostname remains the same while clients use
different edge addresses based on their cache state. The standby's loopback
path to A and LAN path to B are independent checks. The app record can move
while the API record remains on the primary.

**F · Diagnosis.** Demonstrating the first failing layer and proving recovery
are separate observations. A refused TCP connection identifies where to look
first. After a restart, a healthy TLS handshake combined with 502 shifts the
investigation to nginx's upstream path.

## Evaluation and reproducibility

The [runbook](phase2-runbook.md) maps the live demonstration order to commands
and operator roles. The [architecture](architecture.md) identifies the role,
protocol and failure boundary of each host. The inventory and private
baseline snapshots stay on Mac 1 and can be displayed locally as required.
The evidence index distinguishes observed behavior from steps requiring local
administrator participation.

## Deployment status and open acceptance checks

All four Macs activated runtime revision ec69be92e1eb. Mac 1 serves primary
DNS and runs the controller. Mac 2 serves backup DNS and the primary edge.
Mac 3 serves Backend A and the standby edge. Mac 4 serves Backend B and was the
second working test client during live verification. The final application
check passed after all controlled failures restored their baseline. The LAN
capture was decoded and its DNS, TCP and TLS fields were asserted.

A, D, E and F passed. The TTL expiry portion of B passed. The manual cache
flush and C's apply, deny and rollback checks need local administrator
participation. Direct HTTP to both backend ports from Mac 1 was still open.
The separate standby firewall profile also needs an integrated retest after
the owners enable it. The firewall policy files passed staged syntax checks.

The Phase 1 protocol and application checks passed. Four controlled failure
behaviors were observed, with the wrong-client-DNS test still requiring an
owner to select and restore the client DNS settings. Directed ping was 9/12.
Mac 1's firewall and stealth mode were enabled, consistent with the inbound
ICMP results. DNS from the other Macs to Mac 1 continued to work. The firewall
setting was preserved. A second client other than Mac 1 should complete the
team resolver and trust setup for the course checklist. Mac 4 already meets
those client checks and Mac 3 is the prepared candidate.

The [runbook](phase2-runbook.md) holds exact deployment, owner authorization,
demonstration and rollback commands. For a strict full-matrix ping retest,
the Mac 1 owner can temporarily turn off **Enable stealth mode** under
System Settings → Network → Firewall → Options, repeat the checks, then
restore the setting. [Apple Firewall options](https://support.apple.com/en-gb/guide/mac-help/-mh11783/mac)

## Delivery manifest

The machine-specific inventory is local and ignored. The Git file list below
is relative to the original Phase 1 commit. The commit list covers each
incremental implementation and documentation commit before the final evidence
commit.

### Files

- `.gitignore` — modified
- `README.md` — modified
- `backend/app.py` — modified
- `dnsmasq/phase2.conf.template` — added
- `docs/architecture.md` — modified
- `docs/phase2-report.md` — added
- `docs/phase2-runbook.md` — added
- `docs/troubleshooting.md` — added
- `docs/viva-preparation.md` — added
- `evidence/phase2/20261124-004103+0530-lan-flow.pcapng` — added
- `evidence/phase2/20261124-004103+0530-lan-flow.txt` — added
- `evidence/phase2/README.md` — added
- `evidence/phase2/baseline.txt` — added
- `evidence/phase2/client-tls-trust.txt` — added
- `evidence/phase2/deployment.txt` — added
- `evidence/phase2/extension-a.txt` — added
- `evidence/phase2/extension-b.txt` — added
- `evidence/phase2/extension-c-attempt.txt` — added
- `evidence/phase2/extension-d.txt` — added
- `evidence/phase2/extension-e.txt` — added
- `evidence/phase2/extension-f.txt` — added
- `evidence/phase2/final-smoke.txt` — added
- `evidence/phase2/firewall-probes.txt` — added
- `evidence/phase2/icmp-triage.txt` — added
- `evidence/phase2/phase1-controlled-failures.txt` — added
- `evidence/phase2/tls-verification.txt` — added
- `evidence/phase2/wrong-port.txt` — added
- `firewall/backend.pf.template` — added
- `nginx/phase2-master.conf.template` — added
- `nginx/phase2-site.conf.template` — added
- `scripts/activate.sh` — added
- `scripts/cnlib.py` — added
- `scripts/demo.sh` — added
- `scripts/deploy.py` — added
- `scripts/deploy.sh` — added
- `scripts/diagnose.py` — added
- `scripts/diagnose.sh` — added
- `scripts/dns.py` — added
- `scripts/edge-start.command` — added
- `scripts/node.sh` — added
- `scripts/phase2/capture.py` — added
- `scripts/phase2/client.sh` — added
- `scripts/phase2/demo.py` — added
- `scripts/phase2/firewall.sh` — added
- `scripts/render.py` — added
- `scripts/run-backend.sh` — modified
- `scripts/smoke.py` — added
- `team/team.env.example` — modified

### Incremental commits

- `e2074a3` chore: add validated four-Mac inventory
- `8f379b7` feat: stage, validate and deploy four-Mac role bundles
- `8be9623` feat: synchronize DNS records and diagnose connection layers
- `a71f37d` test: add four-Mac Phase 2 demos and regression assertions
- `33f75f4` test: capture LAN traffic and observe passive backend re-entry
- `33ab379` fix: recover nginx in the edge owner macOS session
- `5d42c1d` fix: correlate backup DNS packets and prime a fresh TTL observation
- `16251e3` fix: activate and validate the Terminal edge launcher
- `e144386` docs: add four-Mac runbook and viva preparation
- `8ebbdda` test: verify DNS, TCP and TLS capture fields
- `5afdd71` fix: serialize controller changes and verify standby firewall access
- `dddbaf2` fix: separate manual backend setup from service startup
- `5f3d4ce` test: syntax-check both firewall profiles during node staging
- `2f7e554` fix: preserve healthy services when the deployed files are unchanged
- `3047817` docs: document Phase 2 implementation and recovery findings
- `c6045b1` fix: support pre-deployment snapshots on fresh nodes
- `fed5a63` docs: record remaining client DNS and TLS trust setup
- `ec69be9` test: verify HTTP redirects and both backends after full recovery
- `8169930` fix: capture short LAN exchanges without BPF buffering
