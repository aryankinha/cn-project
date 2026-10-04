# Captured protocol-flow requests — 5 October 2026

All HTTPS requests use default client trust; no validation bypass.

```text
$ dig @10.7.23.16 app.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13749
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 8 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:47:55 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

```text
$ dig @10.7.23.16 api.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @10.7.23.16 api.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36482
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;api.team.test.			IN	A

;; ANSWER SECTION:
api.team.test.		30	IN	A	10.7.20.249

;; Query time: 2 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:47:55 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* ipv4 connect timeout after 2998ms, move on!
* Failed to connect to app.team.test port 443 after 3006 ms: Timeout was reached
* Closing connection
curl: (28) Failed to connect to app.team.test port 443 after 3006 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* ipv4 connect timeout after 2997ms, move on!
* Failed to connect to app.team.test port 443 after 3003 ms: Timeout was reached
* Closing connection
curl: (28) Failed to connect to app.team.test port 443 after 3003 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i https://app.team.test/api/status
curl: (28) Failed to connect to app.team.test port 443 after 3005 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i https://app.team.test/api/status
curl: (28) Failed to connect to app.team.test port 443 after 3004 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i https://app.team.test/api/status
curl: (28) Failed to connect to app.team.test port 443 after 3006 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i https://app.team.test/api/status
curl: (28) Failed to connect to app.team.test port 443 after 3002 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i https://app.team.test/api/status
curl: (28) Failed to connect to app.team.test port 443 after 3004 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i https://app.team.test/api/status
curl: (28) Failed to connect to app.team.test port 443 after 3003 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -I https://app.team.test/api/cache
curl: (28) Failed to connect to app.team.test port 443 after 3004 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 3 --max-time 8 -i -H If-None-Match: "cn-cache-v1" https://app.team.test/api/cache
curl: (28) Failed to connect to app.team.test port 443 after 3005 ms: Timeout was reached

Exit code: 28
```

