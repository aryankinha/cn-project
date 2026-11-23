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
