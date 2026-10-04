# Phase I TLS certificate and nginx setup

Owner: Divyanshu Singh (Mac 2, 10.7.20.249). Domains: `app.team.test` and `api.team.test`.

## Certificate created for this team

`tls/edge.crt` is an RSA-2048, SHA-256 self-signed server certificate with SANs for both domains, serverAuth usage and CA:FALSE. Validity is 5 October 2026 to 5 October 2027 in IST. `tls/edge.key` is its private key, mode 600 and ignored by Git. The certificate fingerprint is:

```text
CB:36:4B:3F:99:C1:D3:57:B3:7E:D7:5B:5B:93:B8:70:94:8F:8E:59:21:3F:BB:01:44:7C:80:2A:8E:13:B0:79
```

This follows the assignment's self-signed certificate option. There is no local CA to distribute. Trust the public server certificate explicitly on every test-client Mac. Never share the private key with the client Macs or upload it to GitHub.

## Install on Divyanshu's Mac

Transfer `edge.crt` and `edge.key` directly to Mac 2 using a trusted local method. On Mac 2 place them in `~/cn-tls/`:

```bash
mkdir -p ~/cn-tls
chmod 700 ~/cn-tls
chmod 600 ~/cn-tls/edge.key
openssl x509 -in ~/cn-tls/edge.crt -noout -subject -dates -ext subjectAltName -fingerprint -sha256
```

Use [the prepared nginx config](../nginx/nginx.conf.template) inside nginx's existing `http {}` context (a Homebrew servers include is commonly suitable). Replace both `<EDGE_HOME>` placeholders with Divyanshu's real absolute home directory. Preserve a copy of the currently working configuration and replace the existing project server/upstream definitions rather than duplicating them. Check the actual include location with `nginx -T`.

```bash
nginx -t
sudo brew services restart nginx
lsof -nP -iTCP:443 -sTCP:LISTEN
```

Use 8443 if binding 443 is unavailable; record the chosen port everywhere and include it in URLs. The prepared config uses 443. HTTP/2 is optional; do not claim it until negotiated in a real test.

## Trust on each client Mac

Share only `edge.crt`, compare its SHA-256 fingerprint above, then import it in Keychain Access. Open the certificate, expand Trust, and set it to Always Trust for SSL. macOS may require the user's administrator authentication. Do this on Aryan's Mac and each other Mac used as a client. This trust applies to this project's certificate.

```bash
curl -v https://app.team.test/api/status
```

The acceptance test must resolve using the team DNS and succeed without `-k`, with hostname/certificate validation enabled. As a separate diagnostic, `curl --cacert tls/edge.crt -v https://app.team.test/api/status` explicitly trusts the exact public certificate; this does not prove the browser/system trust-store setup is complete.

## TLS packet evidence

```bash
curl --tlsv1.2 --tls-max 1.2 -v https://app.team.test/api/status
```

A fresh TLS 1.2 full handshake can expose Certificate and ChangeCipherSpec in the packet capture, as requested by Task G. Normal TLS 1.3 encrypts handshake messages after ServerHello, including Certificate; its compatibility ChangeCipherSpec is not key activation. Do not label encrypted TLS 1.3 records as visible certificates. Use the observed negotiated protocol and curl's certificate validation output. See [TLS 1.3 specification](https://www.rfc-editor.org/rfc/rfc8446) and [nginx upstream documentation](https://nginx.org/en/docs/http/ngx_http_upstream_module.html).

## Recreate only if needed

```bash
umask 077
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls/edge.key -out tls/edge.crt \
  -subj '/O=CN Project Four Mac Team/CN=app.team.test' \
  -addext 'subjectAltName=DNS:app.team.test,DNS:api.team.test' \
  -addext 'basicConstraints=critical,CA:FALSE' \
  -addext 'keyUsage=critical,digitalSignature,keyEncipherment' \
  -addext 'extendedKeyUsage=serverAuth'
```

Regeneration changes the fingerprint and requires clients to trust the replacement certificate. Certificate generation alone does not mean TLS is deployed.

## Latest live check — 5 October 2026

Plain curl and the final smoke test now succeed from Aryan's Mac using default certificate trust, with hostname validation enabled. The edge presents the team's certificate; TLS 1.2 and TLS 1.3 both work, with HTTP/2 negotiated. Earlier exit-60 logs are historical setup evidence. Browser trust and the other Macs' trust stores have not been independently checked.

See [final smoke output](../evidence/phase1/latest-smoke-test-2026-10-05.md) and [successful captured requests](../evidence/phase1/last-capture-requests-2026-10-05.md).
