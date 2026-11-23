# Private DNS

Mac 1 and Mac 2 serve the same private names with a 30-second TTL. The
controller renders [the current template](phase2.conf.template) from
`team/team.env` and deploys the role-specific files. The original
`dnsmasq.conf.template` records the Phase 1 configuration.

Use `./scripts/demo.sh check` on Mac 1 to verify both names over UDP and TCP
against both DNS servers. Use `./scripts/demo.sh A` for backup DNS and the
[runbook](../docs/phase2-runbook.md) for client resolver setup, TTL testing,
cutover and recovery. The client uses the system resolver for application
requests. A direct dig query checks the selected server independently.
