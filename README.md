# Private Network Service Platform — Phase I

Computer Networks course project for four students on four macOS laptops. The backend stays simple; the project demonstrates DNS → TCP → TLS → HTTP, nginx load balancing, caching and packet analysis on a private LAN.

## Team and machine roles

| Mac | Member | Enrollment | Role | Private IP / service port |
| --- | --- | --- | --- | --- |
| 1 | Aryan Kinha | 2401020013 | Private DNS + test client | `10.7.23.16`, UDP/TCP 53 |
| 2 | Divyanshu Singh | 2401010161 | nginx edge, TLS termination, round-robin load balancer | `10.7.20.249`, TCP 80 / 443 |
| 3 | Jatin Verma | 2401010200 | Backend A | `10.7.16.92`, TCP 3001 |
| 4 | Jatin Kumar Singh | 2401010199 | Backend B + test client | `10.7.22.187`, TCP 3002 |

Mac 1 and Mac 4 can act as clients without adding a fifth laptop. Divyanshu, Jatin Verma and Jatin Kumar Singh use Aryan's DNS according to the team's confirmation. The final application is accessed by domain name.

## Architecture

```mermaid
flowchart LR
    subgraph lan["Private LAN — four Macs"]
        dns["Mac 1 · Aryan Kinha<br/>DNS + client<br/>10.7.23.16:53"]
        edge["Mac 2 · Divyanshu Singh<br/>nginx / TLS / load balancer<br/>10.7.20.249:443"]
        a["Mac 3 · Jatin Verma<br/>Backend A<br/>10.7.16.92:3001"]
        b["Mac 4 · Jatin Kumar Singh<br/>Backend B + client<br/>10.7.22.187:3002"]
        dns -->|"Client HTTPS after DNS lookup"| edge
        b -->|"DNS query · UDP 53"| dns
        dns -.->|"A answer · edge IP · TTL 30"| b
        b -->|"Client HTTPS · TCP 443"| edge
        edge -->|"HTTP · TCP 3001"| a
        edge -->|"HTTP · TCP 3002"| b
    end
```

`app.team.test` and `api.team.test` both resolve to the edge. TLS ends at nginx; the edge-to-backend links use plaintext HTTP. DNS is a separate lookup, not a proxy through which the application request travels.

## Verification status — 5 October 2026

- Team-confirmed: all three other Macs use Aryan's DNS; four separate Macs run the four roles.
- Verified from Aryan's Mac: both DNS names resolve to `10.7.20.249` with TTL 30; all other Macs answer ping; direct backends return HTTP 200 and their correct `X-Backend` identifiers.
- After nginx was reloaded, the smoke test verified DNS, HTTP A/B distribution, and HTTPS on 443 using `HTTPS_CA_CERT=tls/edge.crt`. HTTPS negotiated TLS 1.3 and HTTP/2, with responses from both backends. The default client trust store still rejects the certificate; system/browser trust and remaining packet/cache evidence are pending.
- The self-signed certificate for both DNS names is installed on the edge and validated with explicit certificate trust. Public certificate: `tls/edge.crt`; private key: `tls/edge.key` (ignored by Git). Client system trust is still pending.
- Remote interface, MAC address, gateway/prefix, resolver output and all-pairs ping evidence still need collection on the other Macs. Controlled failure demonstrations remain pending.

Actual results are in [initial checks](evidence/phase1/live-verification-2026-10-05.md) and [HTTPS retry](evidence/phase1/working-verification-2026-10-05.md). Do not present expected output as a completed test.

## Phase I requirements

| Assignment task | What to demonstrate | Documentation |
| --- | --- | --- |
| A · LAN | Full interface/IP/prefix/gateway/MAC inventory; ping between every pair | [Architecture](docs/architecture.md) |
| B · DNS | Both private names; at least two other Macs use Mac 1 as resolver | [DNS guide](dnsmasq/README.md) |
| C · Backends | `/`, `/api/status`, `X-Backend`, LAN binding, ports 3001/3002 | [Runbook](docs/project-playbook-and-troubleshooting.md) |
| D · Edge | nginx upstreams and repeated responses from A and B | [Demo commands](docs/demo-commands.md) |
| E · TLS | Trusted HTTPS by name, no `curl -k`, handshake explanation | [TLS setup](docs/tls-setup.md) |
| F · Caching | Cache-Control and cache hit or conditional 304 | [Demo commands](docs/demo-commands.md) |
| G · Packets | DNS, complete TCP handshake, TLS, ports and HTTP headers | [Evidence](evidence/phase1/README.md) |

Section 6.3 also requires wrong DNS, wrong DNS answer, one backend stopped, both backends stopped, and wrong destination port. [Failure plan](docs/phase1-failure-tests.md) includes restoration steps. Backup DNS, firewall isolation and edge migration belong to Phase II and are outside this deliverable.

## Run and verify

On Mac 3: `./scripts/run-backend.sh A`. On Mac 4: `./scripts/run-backend.sh B`.

```bash
dig app.team.test
dig api.team.test
curl -v https://app.team.test/api/status
curl -I https://app.team.test/api/cache
curl -i -H 'If-None-Match: "cn-cache-v1"' https://app.team.test/api/cache
```

These HTTPS commands are the target demonstration once TLS installation and trust are complete. HTTP/1.1 is required; HTTP/2 is optional if supported. HTTP/3 and email protocols are explanation-only.

## Files and evaluation

- [Architecture and inventory](docs/architecture.md)
- [Configuration and troubleshooting runbook](docs/project-playbook-and-troubleshooting.md)
- [TLS certificate installation](docs/tls-setup.md)
- [Demo commands](docs/demo-commands.md)
- [Submission checklist mapped to the assignment](docs/form-submission-checklist.md)
- [Team presentation script](docs/phase1-video-script.md)
- [Evidence and screenshot guide](evidence/phase1/README.md)

The source assignment is `CN_Project_Doc.pdf`, Sections 3, 4, 6, 9 and Review 1 in Section 10. Review 1 totals 50 marks: 40 for the team and 10 for individual viva. Old cloned screenshots/logs are preserved under `evidence/reference-original/` and are not this team's evidence. No five-minute video limit or specific submission form is imposed by the supplied PDF; confirm any additional faculty instructions separately.

## Smoke test

```bash
./scripts/smoke-test.sh team.test
# Explicit trust for the project certificate, while keeping hostname validation:
HTTPS_CA_CERT=tls/edge.crt ./scripts/smoke-test.sh team.test
```

The script checks DNS, existing HTTP requests, a verbose HTTPS request and HTTPS response headers. It exits on failures and prints success only after every request succeeds. [Latest smoke-test results](evidence/phase1/https-smoke-test-2026-10-05.md).
