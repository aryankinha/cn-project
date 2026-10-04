# Longer-timeout TLS capture retry — 5 October 2026

```text
$ dig @10.7.23.16 app.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 22864
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 13 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:49:49 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

```text
$ curl -sS --connect-timeout 15 --max-time 25 --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* ipv4 connect timeout after 14992ms, move on!
* Failed to connect to app.team.test port 443 after 15002 ms: Timeout was reached
* Closing connection
curl: (28) Failed to connect to app.team.test port 443 after 15002 ms: Timeout was reached

Exit code: 28
```

```text
$ curl -sS --connect-timeout 10 --max-time 15 -v https://app.team.test/api/status
* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* ipv4 connect timeout after 9986ms, move on!
* Failed to connect to app.team.test port 443 after 10005 ms: Timeout was reached
* Closing connection
curl: (28) Failed to connect to app.team.test port 443 after 10005 ms: Timeout was reached

Exit code: 28
```

