# Working-session verification — 5 October 2026

Actual output collected on Aryan’s Mac after the team restarted the edge. TLS verification is enabled.

## 1. dig @10.7.23.16 app.team.test +time=2 +tries=1

```text

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 50802
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 10 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:23:26 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## 2. dig @10.7.23.16 api.team.test +time=2 +tries=1

```text

; <<>> DiG 9.10.6 <<>> @10.7.23.16 api.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43454
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;api.team.test.			IN	A

;; ANSWER SECTION:
api.team.test.		30	IN	A	10.7.20.249

;; Query time: 3 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:23:26 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## 3. curl --connect-timeout 3 --max-time 10 -v https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* connect to 10.7.20.249 port 443 from 10.7.23.16 port 53164 failed: Connection refused
* Failed to connect to app.team.test port 443 after 47 ms: Couldn't connect to server

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* Closing connection
curl: (7) Failed to connect to app.team.test port 443 after 47 ms: Couldn't connect to server

Exit code: 7
```

## 4. curl --connect-timeout 3 --max-time 10 --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* connect to 10.7.20.249 port 443 from 10.7.23.16 port 53165 failed: Connection refused
* Failed to connect to app.team.test port 443 after 17 ms: Couldn't connect to server

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* Closing connection
curl: (7) Failed to connect to app.team.test port 443 after 17 ms: Couldn't connect to server

Exit code: 7
```

## 5. curl --connect-timeout 3 --max-time 10 -i https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 137 ms: Couldn't connect to server

Exit code: 7
```

## 6. curl --connect-timeout 3 --max-time 10 -i https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 30 ms: Couldn't connect to server

Exit code: 7
```

## 7. curl --connect-timeout 3 --max-time 10 -i https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 12 ms: Couldn't connect to server

Exit code: 7
```

## 8. curl --connect-timeout 3 --max-time 10 -i https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 126 ms: Couldn't connect to server

Exit code: 7
```

## 9. curl --connect-timeout 3 --max-time 10 -i https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 244 ms: Couldn't connect to server

Exit code: 7
```

## 10. curl --connect-timeout 3 --max-time 10 -i https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 128 ms: Couldn't connect to server

Exit code: 7
```

## 11. curl --connect-timeout 3 --max-time 10 -I https://app.team.test/api/cache

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 131 ms: Couldn't connect to server

Exit code: 7
```

## 12. curl --connect-timeout 3 --max-time 10 -i -H If-None-Match: "cn-cache-v1" https://app.team.test/api/cache

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 161 ms: Couldn't connect to server

Exit code: 7
```

## 13. curl --connect-timeout 3 --max-time 10 --http1.1 -I https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 79 ms: Couldn't connect to server

Exit code: 7
```

## 14. curl --connect-timeout 3 --max-time 10 --http2 -I https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to app.team.test port 443 after 43 ms: Couldn't connect to server

Exit code: 7
```

