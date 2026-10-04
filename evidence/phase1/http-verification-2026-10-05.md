# HTTP load balancing and caching — 5 October 2026

Actual plaintext HTTP evidence. HTTPS validation remains separate.

## Request 1: dig @10.7.23.16 app.team.test +time=2 +tries=1

```text

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2945
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 10 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:34:13 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## Request 2: curl -sS --connect-timeout 3 --max-time 8 -i http://app.team.test/api/status

```text
curl: (28) Failed to connect to app.team.test port 80 after 3005 ms: Timeout was reached

Exit code: 28
```

## Request 3: curl -sS --connect-timeout 3 --max-time 8 -i http://app.team.test/api/status

```text
curl: (28) Failed to connect to app.team.test port 80 after 3007 ms: Timeout was reached

Exit code: 28
```

## Request 4: curl -sS --connect-timeout 3 --max-time 8 -i http://app.team.test/api/status

```text
curl: (28) Failed to connect to app.team.test port 80 after 3005 ms: Timeout was reached

Exit code: 28
```

## Request 5: curl -sS --connect-timeout 3 --max-time 8 -i http://app.team.test/api/status

```text
curl: (28) Failed to connect to app.team.test port 80 after 3005 ms: Timeout was reached

Exit code: 28
```

## Request 6: curl -sS --connect-timeout 3 --max-time 8 -i http://app.team.test/api/status

```text
curl: (28) Failed to connect to app.team.test port 80 after 3006 ms: Timeout was reached

Exit code: 28
```

## Request 7: curl -sS --connect-timeout 3 --max-time 8 -i http://app.team.test/api/status

```text
curl: (28) Failed to connect to app.team.test port 80 after 3003 ms: Timeout was reached

Exit code: 28
```

## Request 8: curl -sS --connect-timeout 3 --max-time 8 -I http://app.team.test/api/cache

```text
curl: (28) Failed to connect to app.team.test port 80 after 3006 ms: Timeout was reached

Exit code: 28
```

## Request 9: curl -sS --connect-timeout 3 --max-time 8 -i -H If-None-Match: "cn-cache-v1" http://app.team.test/api/cache

```text
curl: (28) Failed to connect to app.team.test port 80 after 3006 ms: Timeout was reached

Exit code: 28
```

## Request 10: curl -sS --connect-timeout 3 --max-time 8 -i http://10.7.16.92:3001/

```text
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.12.5
Date: Sun, 04 Oct 2026 21:04:37 GMT
Content-Type: application/json
Content-Length: 89
X-Backend: A
Cache-Control: no-store
Connection: close

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","message":"Backend A is running"}

Exit code: 0
```

## Request 11: curl -sS --connect-timeout 3 --max-time 8 -i http://10.7.22.187:3002/

```text
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.13.1
Date: Sun, 04 Oct 2026 21:04:37 GMT
Content-Type: application/json
Content-Length: 89
X-Backend: B
Cache-Control: no-store
Connection: close

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","message":"Backend B is running"}

Exit code: 0
```

