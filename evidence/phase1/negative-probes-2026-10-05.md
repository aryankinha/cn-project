# Diagnostic negative tests — 5 October 2026

Public-resolver and wrong-port probes; these do not modify the client DNS setting or replace the coordinated five failure demonstrations.

```text
$ dig @8.8.8.8 app.team.test +time=2 +tries=1

; <<>> DiG 9.10.6 <<>> @8.8.8.8 app.team.test +time=2 +tries=1
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 38179
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;app.team.test.			IN	A

;; AUTHORITY SECTION:
.			86393	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2026100401 1800 900 604800 86400

;; Query time: 16 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Oct 05 02:52:21 IST 2026
;; MSG SIZE  rcvd: 117


Exit code: 0
```

```text
$ curl -sS --connect-timeout 3 --max-time 5 -v https://app.team.test:65534/api/status
* Host app.team.test:65534 was resolved.
* IPv6: (none)
* IPv4: 10.7.20.249
*   Trying 10.7.20.249:65534...
* connect to 10.7.20.249 port 65534 from 10.7.23.16 port 53989 failed: Connection refused
* Failed to connect to app.team.test port 65534 after 1023 ms: Couldn't connect to server
* Closing connection
curl: (7) Failed to connect to app.team.test port 65534 after 1023 ms: Couldn't connect to server

Exit code: 7
```

```text
$ arp -n 10.7.20.249
? (10.7.20.249) at 46:a0:7a:97:77:9c on en0 ifscope [ethernet]

Exit code: 0
```

