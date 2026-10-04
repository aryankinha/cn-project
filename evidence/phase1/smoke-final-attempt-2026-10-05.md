# Latest smoke-test attempt — 5 October 2026

After the successful full live rerun, edge reachability degraded. This later result is retained to show current limitations.

```text
== 1. DNS resolution ==
10.7.20.249

== 2. HTTP through the load balancer (5 requests) ==
curl: (28) Failed to connect to app.team.test port 80 after 3006 ms: Timeout was reached
```
