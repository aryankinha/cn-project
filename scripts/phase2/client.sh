#!/bin/bash
# Run locally on the affected Mac with administrator authorization.
set -euo pipefail
(( EUID == 0 )) || { echo "Run with sudo on the affected Mac" >&2; exit 1; }
action="$1"
service="$2"
root=/var/db/cn-project-dns
[[ "$service" =~ ^[A-Za-z0-9_-]+$ ]] || exit 2
mkdir -p -m 700 "$root"
state="$root/$service"
case "$action" in
    apply)
        shift 2
        [[ "$#" == 2 ]] || exit 2
        for ip; do [[ "$ip" =~ ^[0-9]+(\.[0-9]+){3}$ ]] || exit 2; done
        if [[ ! -e "$state" ]]; then
            previous="$(networksetup -getdnsservers "$service")"
            if [[ "$previous" == *"aren't any DNS Servers"* ]]; then previous=Empty; fi
            printf '%s\n' "$previous" > "$state"
        fi
        networksetup -setdnsservers "$service" "$@" ;;
    restore)
        test -s "$state"
        saved=()
        while IFS= read -r address; do saved+=("$address"); done < "$state"
        networksetup -setdnsservers "$service" "${saved[@]}"
        mv "$state" "$state.restored" ;;
    flush) ;;
    *) exit 2 ;;
esac
dscacheutil -flushcache
killall -HUP mDNSResponder
networksetup -getdnsservers "$service"
