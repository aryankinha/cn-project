# Fresh Phase I verification — 5 October 2026

Collected on Aryan Kinha’s DNS Mac. These are actual results; failures are preserved.

## dig @10.7.23.16 app.team.test +time=2 +tries=1

```text

; <<>> DiG 9.10.6 <<>> @10.7.23.16 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30959
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 13 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:22:06 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## dig @10.7.23.16 api.team.test +time=2 +tries=1

```text

; <<>> DiG 9.10.6 <<>> @10.7.23.16 api.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 55839
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;api.team.test.			IN	A

;; ANSWER SECTION:
api.team.test.		30	IN	A	10.7.20.249

;; Query time: 4 msec
;; SERVER: 10.7.23.16#53(10.7.23.16)
;; WHEN: Mon Oct 05 02:22:06 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## dig app.team.test +time=2 +tries=1

```text

; <<>> DiG 9.10.6 <<>> app.team.test +time=2 +tries=1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1167
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;app.team.test.			IN	A

;; ANSWER SECTION:
app.team.test.		30	IN	A	10.7.20.249

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon Oct 05 02:22:06 IST 2026
;; MSG SIZE  rcvd: 58


Exit code: 0
```

## curl --connect-timeout 2 --max-time 5 -v https://app.team.test/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host app.team.test:443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:443...
* connect to 10.7.20.249 port 443 from 10.7.23.16 port 53109 failed: Connection refused
* Failed to connect to app.team.test port 443 after 479 ms: Couldn't connect to server

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* Closing connection
curl: (7) Failed to connect to app.team.test port 443 after 479 ms: Couldn't connect to server

Exit code: 7
```

## curl --connect-timeout 2 --max-time 5 -v https://app.team.test:8443/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host app.team.test:8443 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:8443...
* connect to 10.7.20.249 port 8443 from 10.7.23.16 port 53112 failed: Connection refused
* Failed to connect to app.team.test port 8443 after 201 ms: Couldn't connect to server

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* Closing connection
curl: (7) Failed to connect to app.team.test port 8443 after 201 ms: Couldn't connect to server

Exit code: 7
```

## curl --connect-timeout 2 --max-time 5 -i http://10.7.16.92:3001/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    70  100    70    0     0    973      0 --:--:-- --:--:-- --:--:--   985
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.12.5
Date: Sun, 04 Oct 2026 20:52:06 GMT
Content-Type: application/json
Content-Length: 70
X-Backend: A
Cache-Control: no-store
Connection: close

{"backend":"A","hostname":"Jatins-MacBook-Pro-5.local","status":"ok"}

Exit code: 0
```

## curl --connect-timeout 2 --max-time 5 -i http://10.7.22.187:3002/api/status

```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    70  100    70    0     0    348      0 --:--:-- --:--:-- --:--:--   348
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.13.1
Date: Sun, 04 Oct 2026 20:52:06 GMT
Content-Type: application/json
Content-Length: 70
X-Backend: B
Cache-Control: no-store
Connection: close

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","status":"ok"}

Exit code: 0
```

## ifconfig en0

```text
en0: flags=8963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX,MULTICAST> mtu 1500
	options=6460<TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether 2e:a3:0c:b9:e7:1a
	inet6 fe80::cfc:dfb3:e363:46da%en0 prefixlen 64 secured scopeid 0xb 
	inet 10.7.23.16 netmask 0xffffe000 broadcast 10.7.31.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active

Exit code: 0
```

## route -n get default

```text
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

## ping -c 2 -W 1000 10.7.20.249

```text
PING 10.7.20.249 (10.7.20.249): 56 data bytes
64 bytes from 10.7.20.249: icmp_seq=0 ttl=64 time=163.232 ms
64 bytes from 10.7.20.249: icmp_seq=1 ttl=64 time=22.066 ms

--- 10.7.20.249 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 22.066/92.649/163.232/70.583 ms

Exit code: 0
```

## ping -c 2 -W 1000 10.7.16.92

```text
PING 10.7.16.92 (10.7.16.92): 56 data bytes
64 bytes from 10.7.16.92: icmp_seq=0 ttl=64 time=20.739 ms
64 bytes from 10.7.16.92: icmp_seq=1 ttl=64 time=7.305 ms

--- 10.7.16.92 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 7.305/14.022/20.739/6.717 ms

Exit code: 0
```

## ping -c 2 -W 1000 10.7.22.187

```text
PING 10.7.22.187 (10.7.22.187): 56 data bytes
64 bytes from 10.7.22.187: icmp_seq=0 ttl=64 time=49.286 ms
64 bytes from 10.7.22.187: icmp_seq=1 ttl=64 time=824.648 ms

--- 10.7.22.187 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.286/436.967/824.648/387.681 ms

Exit code: 0
```

