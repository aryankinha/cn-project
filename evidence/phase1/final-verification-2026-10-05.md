# Phase I full live rerun — 5 October 2026

Collected from Aryan Kinha’s Mac. Explicit-certificate commands validate the certificate and hostname; they do not prove client system/browser trust. Failures are preserved.

## DNS app explicit

```text
$ dig @10.7.23.16 app.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61690
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 15 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:46:14 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## DNS api explicit

```text
$ dig @10.7.23.16 api.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @10.7.23.16 api.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 27652
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;api.team.test.			IN	A

;; ANSWER SECTION:
api.team.test.		30	IN	A	10.7.20.249

;; Query time: 2 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:46:14 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## DNS default

```text
$ dig app.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> app.team.test +time=2 +tries=1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2845
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon Oct 05 02:46:14 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## HTTPS default trust

```text
$ curl -sS --connect-timeout 3 --max-time 8 -v https://app.team.test/api/status
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
< date: Sun, 04 Oct 2026 21:16:14 GMT
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

## TLS 1.2 full handshake

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* Connected to app.team.test (10.7.20.249) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [225 bytes data]
*  CAfile: tls/edge.crt
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
< date: Sun, 04 Oct 2026 21:16:15 GMT
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

## TLS 1.3 / HTTP2

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* Connected to app.team.test (10.7.20.249) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [318 bytes data]
*  CAfile: tls/edge.crt
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
< date: Sun, 04 Oct 2026 21:16:16 GMT
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

## HTTPS balancing 1

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://app.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:16 GMT
content-type: application/json
content-length: 70
x-backend: B
cache-control: no-store

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

Exit code: 0
```

## HTTPS balancing 2

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://app.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:18 GMT
content-type: application/json
content-length: 70
x-backend: A
cache-control: no-store

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

## HTTPS balancing 3

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://app.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:19 GMT
content-type: application/json
content-length: 70
x-backend: B
cache-control: no-store

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

Exit code: 0
```

## HTTPS balancing 4

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://app.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:20 GMT
content-type: application/json
content-length: 70
x-backend: A
cache-control: no-store

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

## HTTPS balancing 5

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://app.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:21 GMT
content-type: application/json
content-length: 70
x-backend: B
cache-control: no-store

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

Exit code: 0
```

## HTTPS balancing 6

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://app.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:21 GMT
content-type: application/json
content-length: 70
x-backend: A
cache-control: no-store

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

## Cache headers

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -I https://app.team.test/api/cache
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:21 GMT
content-type: application/json
content-length: 88
x-backend: B
etag: "cn-cache-v1"
cache-control: public, max-age=60


Exit code: 0
```

## Cache conditional

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i -H If-None-Match: "cn-cache-v1" https://app.team.test/api/cache
HTTP/2 304 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:21 GMT
x-backend: A
etag: "cn-cache-v1"
cache-control: public, max-age=60


Exit code: 0
```

## HTTP1.1

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt --http1.1 -I https://app.team.test/api/status
HTTP/1.1 200 OK
Server: nginx/1.31.6
Date: Sun, 04 Oct 2026 21:16:21 GMT
Content-Type: application/json
Content-Length: 70
Connection: keep-alive
X-Backend: B
Cache-Control: no-store


Exit code: 0
```

## API domain HTTPS

```text
$ curl -sS --connect-timeout 3 --max-time 8 --cacert tls/edge.crt -i https://api.team.test/api/status
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:16:22 GMT
content-type: application/json
content-length: 70
x-backend: A
cache-control: no-store

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

## Backend A /

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i http://10.7.16.92:3001/
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.12.5
Date: Sun, 04 Oct 2026 21:16:22 GMT
Content-Type: application/json
Content-Length: 89
X-Backend: A
Cache-Control: no-store
Connection: close

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","message":"Backend A is running"}

Exit code: 0
```

## Backend A /api/status

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i http://10.7.16.92:3001/api/status
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.12.5
Date: Sun, 04 Oct 2026 21:16:22 GMT
Content-Type: application/json
Content-Length: 70
X-Backend: A
Cache-Control: no-store
Connection: close

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

## Backend B /

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i http://10.7.22.187:3002/
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.13.1
Date: Sun, 04 Oct 2026 21:16:22 GMT
Content-Type: application/json
Content-Length: 89
X-Backend: B
Cache-Control: no-store
Connection: close

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","message":"Backend B is running"}

Exit code: 0
```

## Backend B /api/status

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i http://10.7.22.187:3002/api/status
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.13.1
Date: Sun, 04 Oct 2026 21:16:22 GMT
Content-Type: application/json
Content-Length: 70
X-Backend: B
Cache-Control: no-store
Connection: close

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

Exit code: 0
```

## LAN inventory

```text
$ ifconfig en0
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6460<TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether 2e:a3:0c:b9:e7:1a
	inet6 fe80::cfc:dfb3:e363:46da%en0 prefixlen 64 secured scopeid 0xb 
	inet 10.7.23.16 netmask 0xffffe000 broadcast 10.7.31.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active

Exit code: 0
```

## Gateway

```text
$ route -n get default
   route to: default
destination: default
       mask: default
    gateway: 10.7.0.1
  interface: en0
      flags: <UP,GATEWAY,DONE,STATIC,PRCLONING,GLOBAL>
 recvpipe  sendpipe  ssthresh  rtt,msec    rttvar  hopcount      mtu     expire
       0         0         0         0         0         0      1500         0 

Exit code: 0
```

## Resolvers

```text
$ scutil --dns
DNS configuration

resolver #1
  nameserver[0] : 127.0.0.1
  flags    : Request A records, Request AAAA records
  reach    : 0x00030002 (Reachable,Local Address,Directly Reachable Address)

resolver #2
  domain   : local
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300000

resolver #3
  domain   : 254.169.in-addr.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300200

resolver #4
  domain   : 8.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300400

resolver #5
  domain   : 9.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300600

resolver #6
  domain   : a.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300800

resolver #7
  domain   : b.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 301000

DNS configuration (for scoped queries)

resolver #1
  nameserver[0] : 127.0.0.1
  if_index : 11 (en0)
  flags    : Scoped, Request A records, Request AAAA records
  reach    : 0x00000000 (Not Reachable)

Exit code: 0
```

## Ping 10.7.20.249

```text
$ ping -c 2 -W 1000 10.7.20.249
PING 10.7.20.249 (10.7.20.249): 56 data bytes
64 bytes from 10.7.20.249: icmp_seq=0 ttl=64 time=70.539 ms

--- 10.7.20.249 ping statistics ---
2 packets transmitted, 1 packets received, 50.0% packet loss
round-trip min/avg/max/stddev = 70.539/70.539/70.539/nan ms

Exit code: 0
```

## Ping 10.7.16.92

```text
$ ping -c 2 -W 1000 10.7.16.92
PING 10.7.16.92 (10.7.16.92): 56 data bytes
64 bytes from 10.7.16.92: icmp_seq=0 ttl=64 time=7.025 ms
64 bytes from 10.7.16.92: icmp_seq=1 ttl=64 time=42.181 ms

--- 10.7.16.92 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 7.025/24.603/42.181/17.578 ms

Exit code: 0
```

## Ping 10.7.22.187

```text
$ ping -c 2 -W 1000 10.7.22.187
PING 10.7.22.187 (10.7.22.187): 56 data bytes
64 bytes from 10.7.22.187: icmp_seq=0 ttl=64 time=134.820 ms
64 bytes from 10.7.22.187: icmp_seq=1 ttl=64 time=28.127 ms

--- 10.7.22.187 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 28.127/81.474/134.820/53.346 ms

Exit code: 0
```

