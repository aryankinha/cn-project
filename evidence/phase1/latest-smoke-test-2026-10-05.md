# Final smoke test — 5 October 2026

Client: Aryan Kinha, Mac 1. Run at approximately 02:58 IST. Default client certificate trust; no HTTPS_CA_CERT override and no insecure option. Exit code: 0.

```text
$ ./scripts/smoke-test.sh team.test
== 1. DNS resolution ==
10.7.20.249

== 2. HTTP through the load balancer (5 requests) ==
{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}


== 3. Response headers (Cache-Control, X-Backend) ==
HTTP/1.1 200 OK
Server: nginx/1.31.6
Date: Sun, 04 Oct 2026 21:28:08 GMT
Content-Type: application/json
Content-Length: 70
Connection: keep-alive
X-Backend: A
Cache-Control: no-store


== 4. HTTPS certificate validation and backend response ==
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* Connected to app.team.test (10.7.20.249) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [318 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
{ [122 bytes data]
* (304) (IN), TLS handshake, Unknown (8):
{ [47 bytes data]
* (304) (IN), TLS handshake, Certificate (11):
{ [914 bytes data]
* (304) (IN), TLS handshake, CERT verify (15):
{ [264 bytes data]
* (304) (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* (304) (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: O=CN Project Four Mac Team; CN=app.team.test
*  start date: Oct  4 20:58:49 2026 GMT
*  expire date: Oct  4 20:58:49 2027 GMT
*  subjectAltName: host "app.team.test" matched cert's "app.team.test"
*  issuer: O=CN Project Four Mac Team; CN=app.team.test
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://app.team.test/api/status
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: app.team.test]
* [HTTP/2] [1] [:path: /api/status]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET /api/status HTTP/2
> Host: app.team.test
> User-Agent: curl/8.7.1
> Accept: */*
> 
* Request completely sent off
< HTTP/2 200 
< server: nginx/1.31.6
< date: Sun, 04 Oct 2026 21:28:08 GMT
< content-type: application/json
< content-length: 70
< x-backend: B
< cache-control: no-store
< 
{ [70 bytes data]
* Connection #0 to host app.team.test left intact
{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}


== 5. HTTPS response headers (Cache-Control, X-Backend) ==
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:28:08 GMT
content-type: application/json
content-length: 70
x-backend: A
cache-control: no-store


Smoke test passed: DNS, HTTP and HTTPS requests succeeded.

```
