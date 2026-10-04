# Team-supplied nginx configuration update — 5 October 2026

The user supplied the configuration installed on Divyanshu Singh's load-balancer Mac (Mac 2, 10.7.20.249). The repository template now uses the supplied upstream endpoints, HTTP app-domain listener, HTTPS app/api listener, `http2 on`, TLS 1.2/1.3, cipher setting and absolute certificate paths under `/Users/divyanshusingh/Desktop/Private-Network-Service-Platform-/tls/`.

Backend comments were corrected to the documented team roles: Mac 3 is Jatin Verma (A); Mac 4 is Jatin Kumar Singh (B). No upstream endpoint was changed.

Local nginx validation succeeded at approximately 03:04 IST. For this check only, the two certificate paths were replaced with Aryan's local matching files, and the blocks were wrapped in a temporary `http {}` context. No server was started or reloaded.

```text
nginx: the configuration file /private/tmp/cn-updated-nginx.conf syntax is ok
nginx: configuration file /private/tmp/cn-updated-nginx.conf test is successful
```

This validates local syntax and certificate loading after path substitution. It does not independently verify remote filesystem permissions, the remote include layout, or an exported `nginx -T` configuration. Earlier live HTTPS and HTTP/2 results remain linked in the evidence index.
