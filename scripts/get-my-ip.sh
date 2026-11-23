#!/bin/bash
# Inspect the active IPv4 route, or pass the lab interface explicitly.
set -euo pipefail
interface="${1:-$(route -n get -inet default 2>/dev/null | awk '/interface:/ { print $2; exit }')}"
[[ -n "$interface" ]] || { echo "No default IPv4 interface; pass the lab interface" >&2; exit 1; }
ipv4="$(ipconfig getifaddr "$interface")"
printf 'Interface: %s\nIPv4: %s\n' "$interface" "$ipv4"
ifconfig "$interface" | awk '/inet / { print "Netmask: " $4 } /ether / { print "MAC: " $2 }'
gateway="$(ipconfig getoption "$interface" router 2>/dev/null || true)"
[[ -n "$gateway" ]] || gateway="$(route -n get -inet default 2>/dev/null | awk '/gateway:/ { print $2; exit }')"
printf 'Gateway: %s\n' "$gateway"
