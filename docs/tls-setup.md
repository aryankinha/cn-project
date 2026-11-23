# Team TLS setup

The primary and standby edges serve the same team certificate for
`app.team.test` and `api.team.test`. The deployment validates the configured
certificate and key at `~/cn-project/tls/edge.crt` and
`~/cn-project/tls/edge.key` on each edge. Edge owners provision these before a
fresh deployment and keep the private key out of Git and release bundles.

Compare the public certificate fingerprint with the
[verified live certificate](../evidence/phase2/tls-verification.txt). If a
client needs trust configured, import only the matching public certificate
through Keychain Access and enable SSL trust. Verify using ordinary curl:

```sh
curl --http1.1 -fsS https://app.team.test/api/status
curl --http1.1 -fsS https://api.team.test/api/status
```

The [LAN capture](../evidence/phase2/README.md) contains a TLS 1.2 handshake
with a visible Certificate message. The tracked `tls/edge.crt` is the
historical Phase 1 certificate. Use the verified live certificate when
testing or provisioning the integrated deployment.
