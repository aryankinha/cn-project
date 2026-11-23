#!/bin/bash
# Standalone verification from a configured lab client. No SSH or inventory is needed.
set -euo pipefail
domain="${1:-team.test}"
curl_args=(--noproxy '*' --http1.1 --silent --show-error --connect-timeout 3 --max-time 10)
if [[ -n "${HTTPS_CA_CERT:-}" ]]; then
    [[ -r "$HTTPS_CA_CERT" ]] || { echo "Cannot read HTTPS_CA_CERT" >&2; exit 1; }
    curl_args+=(--cacert "$HTTPS_CA_CERT")
fi

header() { awk -v name="$1" 'tolower($1) == name ":" {sub(/^[^:]*:[[:space:]]*/, ""); print; exit}'; }
response() { curl "${curl_args[@]}" -D - -o /dev/null "$@" | tr -d '\r'; }
expect_status() {
    [[ "$1" == "HTTP/1.1 $2 "* ]] || { printf 'Expected HTTP %s\n%s\n' "$2" "$1" >&2; exit 1; }
}

for name in "app.$domain" "api.$domain"; do
    dscacheutil -q host -a name "$name" | awk '/^ip_address:/ { print; found=1 } END { exit !found }'
    result="$(response "http://$name/api/status")"
    expect_status "$result" 301
    [[ "$(header location <<< "$result")" == "https://$name/api/status" ]]
    result="$(response "https://$name/api/status")"
    expect_status "$result" 200
    printf '%s\n' "$result"
done

url="https://app.$domain/api"
previous=
for attempt in {1..6}; do
    result="$(response "$url/status")"
    expect_status "$result" 200
    backend="$(header x-backend <<< "$result")"
    edge="$(header x-edge <<< "$result")"
    [[ -n "$edge" && ( "$backend" == A || "$backend" == B ) && "$backend" != "$previous" ]] ||
        { printf 'Expected A/B rotation; previous=%s edge=%s backend=%s\n' "$previous" "$edge" "$backend" >&2; exit 1; }
    previous="$backend"
    printf 'Request %s: %s backend %s\n' "$attempt" "$edge" "$backend"
done

result="$(response "$url/cache")"
expect_status "$result" 200
tag="$(header etag <<< "$result")"
[[ -n "$tag" && "$(header cache-control <<< "$result")" == *"max-age=60"* ]]
result="$(response -H "If-None-Match: $tag" "$url/cache")"
expect_status "$result" 304
printf '%s\nSmoke test passed\n' "$result"
