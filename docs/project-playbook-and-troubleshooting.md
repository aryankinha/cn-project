# Phase I setup and troubleshooting runbook

| Mac | Member | Enrollment | Role | Private IP / service port |
| --- | --- | --- | --- | --- |
| 1 | Aryan Kinha | 2401020013 | Private DNS + test client | `10.7.23.16`, UDP/TCP 53 |
| 2 | Divyanshu Singh | 2401010161 | nginx edge, TLS termination, round-robin load balancer | `10.7.20.249`, TCP 80 / 443 |
| 3 | Jatin Verma | 2401010200 | Backend A | `10.7.16.92`, TCP 3001 |
| 4 | Jatin Kumar Singh | 2401010199 | Backend B + test client | `10.7.22.187`, TCP 3002 |

## Working arrangement

All service hosts share the private LAN. Macs 2–4 use Aryan's DNS as confirmed by the team. Mac 1 uses loopback DNS. `team/team.env` stores local session addresses; [the example](../team/team.env.example) lists this topology. Recheck addresses after Wi-Fi changes.

## Start services

- Mac 1 / Aryan: inspect `/opt/homebrew/etc/dnsmasq.conf`, then `sudo brew services start dnsmasq` if it is stopped. Use [DNS guide](../dnsmasq/README.md).
- Mac 3 / Jatin Verma: run `./scripts/run-backend.sh A` from this repository.
- Mac 4 / Jatin Kumar Singh: run `./scripts/run-backend.sh B` from this repository.
- Mac 2 / Divyanshu: install the [TLS certificate](tls-setup.md), adapt the [nginx config](../nginx/nginx.conf.template), check `nginx -t`, and start/reload nginx. Keep an original configuration copy.

The backend launch script creates a virtual environment and installs Flask. Both instances run the same source with different BACKEND_ID and PORT, bound to `0.0.0.0`. Endpoints are `/`, `/api/status` and `/api/cache`.

## Diagnose in protocol order

1. **DNS:** `dig app.team.test` should use the intended resolver and return `10.7.20.249`. If an explicit `dig @10.7.23.16` works but normal resolution fails, inspect client DNS settings with `scutil --dns`.
2. **IP/TCP:** Ping checks host reachability, not service availability. Compare HTTP 80 and HTTPS 443. A refusal means no accepting listener or an active rejection; a timeout can mean filtering, sleep or reachability trouble. Ask Divyanshu to inspect `lsof -nP -iTCP:443 -sTCP:LISTEN` and `nginx -t`.
3. **TLS:** Once TCP works, use `curl -v` to inspect hostname, trust and certificate validation. Install the project's public certificate on the client. Do not bypass validation for the final demo.
4. **HTTP/upstream:** A 502 means nginx cannot successfully obtain an upstream response; inspect its error log and test each backend from Mac 2. Verify both correct IPs, ports and listeners before changing configuration.
5. **Caching:** `/api/cache` should supply cache headers and 304 on the matching ETag. Record actual deployed behavior; a source file in this clone does not prove the remote process is running the same version.

## Findings from this team's session

On 5 October 2026 both names resolved correctly; all remote hosts answered ping and both backend status endpoints returned HTTP 200. Initial HTTPS timed out, followed by connection refusals on 443 and 8443, while HTTP on 80 worked. This isolated the observed problem to the edge HTTPS listener/reachability before any TLS handshake, not to private DNS or backend availability. A certificate and deployment configuration were prepared; installation still requires Mac 2.

Previous-team post-mortems are not retained as claims about this team. Their old packet screenshots/logs are clearly labeled in the [reference archive](../evidence/reference-original/README.md).

## Packet capture

Use the [demo commands](demo-commands.md) and [evidence guide](../evidence/phase1/README.md). Local DNS on Aryan's Mac follows lo0; remote application traffic follows en0. Capture both to correlate the request flow. Save project-filtered packets for submission, keeping unrelated traffic out of the evidence bundle.

## Failure and recovery

Follow [the five coordinated Phase I failures](phase1-failure-tests.md). nginx's default balancing is round-robin. `max_fails` and `fail_timeout` implement passive handling based on real upstream attempts, not periodic health checks. See [official nginx documentation](https://nginx.org/en/docs/http/ngx_http_upstream_module.html). Report actual retries/errors; do not promise lossless failover before testing.

## Viva prompts

Explain why DNS and IP connectivity are independent; why ports identify services; what SYN/SYN-ACK/ACK establish; how ACKs and retransmission support reliable transfer; how TLS authenticates the edge; why HTTP headers are visible in curl but encrypted in HTTPS captures; how nginx selects a backend; and how fresh caching differs from conditional 304. TLS does not encrypt the plaintext upstream link in this topology.
