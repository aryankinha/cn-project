# Private Network Service Platform

Computer Networks course project covering Phase 1 and Phase 2 on a private
four-Mac LAN. Clients resolve `app.team.test` and `api.team.test`, connect to
nginx over HTTPS, and receive responses from one of two Flask backends.

| Mac | Owner | Roles |
| --- | --- | --- |
| 1 | Aryan Kinha | Primary DNS, deployment controller, test client |
| 2 | Divyanshu Singh | Backup DNS, primary edge |
| 3 | Jatin Verma | Standby edge, Backend A on TCP 3001 |
| 4 | Jatin Kumar Singh | Backend B on TCP 3002, test client |

DNS uses UDP and TCP 53. The edges redirect HTTP on TCP 80 to HTTPS on TCP
443 and forward HTTP to the backends. `X-Edge` identifies the serving edge
and `X-Backend` identifies the selected backend. See the
[architecture and request flow](docs/architecture.md).

## Run and verify

On Mac 1, configure `team/team.env` from [the example](team/team.env.example)
with the current LAN inventory. The renderer and controller use this file,
and Git ignores it. For a planned deployment, run:

```sh
./scripts/deploy.sh --check
./scripts/deploy.sh --all --dry-run
./scripts/deploy.sh --all
```

The last command stages and activates a committed revision. A fresh edge
needs the team TLS files provisioned first. For verification of an already
running system, use:

```sh
./scripts/demo.sh who
./scripts/demo.sh check
./scripts/smoke-test.sh team.test
```

The controller check verifies both resolvers and both edges over HTTP/1.1.
The standalone smoke test checks DNS, trusted HTTPS, backend rotation,
HTTP redirects and cache revalidation from the calling Mac. See the
[runbook](docs/phase2-runbook.md) for the controlled drills and their recovery steps.

## Submission

- [Checklist mapped to the course brief](docs/form-submission-checklist.md)
- [Phase 2 final report](docs/phase2-report.md) and [verification evidence](evidence/phase2/README.md)
- [Live demo commands](docs/demo-commands.md) and [viva preparation](docs/viva-preparation.md)
- [TLS setup](docs/tls-setup.md) and [troubleshooting](docs/troubleshooting.md)
- [Historical Phase 1 evidence](evidence/phase1/README.md)

The latest verified state includes both DNS servers and HTTPS edges,
backend rotation and failover, conditional HTTP caching, DNS TTL and
manual flush, DNS cutover, and the troubleshooting drill. The submission
checklist records the remaining live acceptance checks.
