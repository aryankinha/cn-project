# Final protocol capture attempt — 5 October 2026

```text
$ dig @10.7.23.16 app.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42997
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 12 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:53:43 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

```text
$ curl -sS --connect-timeout 5 --max-time 10 --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* Connected to app.team.test (10.7.20.249) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [225 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
{ [100 bytes data]
* TLSv1.2 (IN), TLS handshake, Certificate (11):
{ [911 bytes data]
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
{ [300 bytes data]
* TLSv1.2 (IN), TLS handshake, Server finished (14):
{ [4 bytes data]
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
} [37 bytes data]
* TLSv1.2 (OUT), TLS change cipher, Change cipher spec (1):
} [1 bytes data]
* TLSv1.2 (OUT), TLS handshake, Finished (20):
} [16 bytes data]
* TLSv1.2 (IN), TLS change cipher, Change cipher spec (1):
{ [1 bytes data]
* TLSv1.2 (IN), TLS handshake, Finished (20):
{ [16 bytes data]
* SSL connection using TLSv1.2 / ECDHE-RSA-CHACHA20-POLY1305 / [blank] / UNDEF
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
< date: Sun, 04 Oct 2026 21:23:43 GMT
< content-type: application/json
< content-length: 70
< x-backend: B
< cache-control: no-store
< 
{ [70 bytes data]
* Connection #0 to host app.team.test left intact
{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

Exit code: 0
```

```text
$ curl -sS --connect-timeout 5 --max-time 10 -v https://app.team.test/api/status
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
< date: Sun, 04 Oct 2026 21:23:44 GMT
< content-type: application/json
< content-length: 70
< x-backend: A
< cache-control: no-store
< 
{ [70 bytes data]
* Connection #0 to host app.team.test left intact
{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

