#!/bin/bash
# Run from any CLIENT Mac to check DNS, HTTP and trusted HTTPS (Tasks A-E).
# Usage: ./scripts/smoke-test.sh team.test
# Uses the client's certificate trust store by default. To explicitly trust
# the project's self-signed certificate instead:
# HTTPS_CA_CERT=tls/edge.crt ./scripts/smoke-test.sh team.test
set -euo pipefail

DOMAIN="${1:-team.test}"
HTTPS_OPTIONS=()
if [ -n "${HTTPS_CA_CERT:-}" ]; then
  if [ ! -r "$HTTPS_CA_CERT" ]; then
    echo "ERROR: Cannot read HTTPS_CA_CERT: $HTTPS_CA_CERT" >&2
    exit 1
  fi
  HTTPS_OPTIONS=(--cacert "$HTTPS_CA_CERT")
fi

echo "== 1. DNS resolution =="
DNS_RESULT="$(dscacheutil -q host -a name "app.$DOMAIN" | awk '/ip_address:/{print $2}')"
if [ -z "$DNS_RESULT" ]; then
  echo "ERROR: macOS could not resolve app.$DOMAIN. Set this client's DNS to the DNS Mac's LAN IP (127.0.0.1 only on the DNS Mac) and remove public secondary resolvers." >&2
  exit 1
fi
printf '%s\n' "$DNS_RESULT"

echo ""
echo "== 2. HTTP through the load balancer (5 requests) =="
for i in 1 2 3 4 5; do
  curl --fail --silent --show-error --connect-timeout 3 --max-time 10 "http://app.$DOMAIN/api/status"
  echo ""
done

echo ""
echo "== 3. Response headers (Cache-Control, X-Backend) =="
curl --fail --silent --show-error --connect-timeout 3 --max-time 10 --head "http://app.$DOMAIN/api/status"

echo ""
echo "== 4. HTTPS certificate validation and backend response =="
# Keep hostname and certificate verification enabled; never use --insecure.
curl ${HTTPS_OPTIONS[@]+"${HTTPS_OPTIONS[@]}"} --fail --silent --show-error --verbose \
  --connect-timeout 3 --max-time 10 "https://app.$DOMAIN/api/status"
echo ""

echo ""
echo "== 5. HTTPS response headers (Cache-Control, X-Backend) =="
curl ${HTTPS_OPTIONS[@]+"${HTTPS_OPTIONS[@]}"} --fail --silent --show-error \
  --connect-timeout 3 --max-time 10 --head "https://app.$DOMAIN/api/status"

echo ""
echo "Smoke test passed: DNS, HTTP and HTTPS requests succeeded."
