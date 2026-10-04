# TLS artifacts — verification

Created and checked on 5 October 2026. This verifies local artifacts, not deployment or client system trust.

```text
$ openssl x509 -in tls/edge.crt -noout -subject -issuer -dates -ext subjectAltName -fingerprint -sha256
subject=O=CN Project Four Mac Team, CN=app.team.test
issuer=O=CN Project Four Mac Team, CN=app.team.test
notBefore=Oct  4 20:58:49 2026 GMT
notAfter=Oct  4 20:58:49 2027 GMT
X509v3 Subject Alternative Name: 
    DNS:app.team.test, DNS:api.team.test
sha256 Fingerprint=CB:36:4B:3F:99:C1:D3:57:B3:7E:D7:5B:5B:93:B8:70:94:8F:8E:59:21:3F:BB:01:44:7C:80:2A:8E:13:B0:79
```

```text
$ openssl verify -CAfile tls/edge.crt -verify_hostname app.team.test tls/edge.crt
tls/edge.crt: OK
```

```text
$ openssl verify -CAfile tls/edge.crt -verify_hostname api.team.test tls/edge.crt
tls/edge.crt: OK
```

Public keys from the certificate and private key match. Private key permissions are 0600, and `git check-ignore tls/edge.key` confirms Git exclusion.

The prepared nginx server/upstream blocks were placed in a temporary standalone configuration, with certificate paths adjusted to the local files. `nginx -t -e stderr -p /private/tmp/ -c /private/tmp/cn-nginx-check.conf` reported syntax OK and test successful. No nginx server was started or reconfigured on Aryan’s Mac. Divyanshu’s actual loaded configuration must be tested separately.
