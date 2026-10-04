# Final root and caching verification — 5 October 2026

Client: Aryan Kinha, Mac 1. Default certificate trust; no bypass or explicit CA override.

```text
$ curl -sS --fail --connect-timeout 3 --max-time 10 -i https://app.team.test/
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:28:41 GMT
content-type: application/json
content-length: 89
x-backend: B
cache-control: no-store

{"backend":"B","hostname":"Jatins-MacBook-Pro-2.local","message":"Backend B is running"}

Exit code: 0
```

```text
$ curl -sS --connect-timeout 3 --max-time 10 -I https://app.team.test/api/cache
HTTP/2 200 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:28:41 GMT
content-type: application/json
content-length: 88
x-backend: A
etag: "cn-cache-v1"
cache-control: public, max-age=60


Exit code: 0
```

```text
$ curl -sS --connect-timeout 3 --max-time 10 -i -H 'If-None-Match: "cn-cache-v1"' https://app.team.test/api/cache
HTTP/2 304 
server: nginx/1.31.6
date: Sun, 04 Oct 2026 21:28:41 GMT
x-backend: B
etag: "cn-cache-v1"
cache-control: public, max-age=60


Exit code: 0
```
