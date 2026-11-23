#!/bin/bash
# Manage a dedicated anchor. Run as an administrator on a backend host.
set -euo pipefail
(( EUID == 0 )) || { echo "Run with sudo on the backend Mac" >&2; exit 1; }
umask 077
pf=/sbin/pfctl
anchor=com.apple/cn-project-phase2
state=/var/db/cn-project-pf
action="${1:-status}"
mkdir -p -m 700 "$state"
lock="$state/lock"
mkdir "$lock" || { echo "Firewall operation already in progress" >&2; exit 1; }
trap 'rmdir "$lock"' EXIT
case "$action" in
    apply)
        rules="$2"
        [[ "$rules" == /* && -f "$rules" ]] || exit 2
        "$pf" -sr | grep -F 'anchor "com.apple/*"' >/dev/null
        snapshot="$(mktemp "$state/candidate.XXXXXX")"
        cp "$rules" "$snapshot"
        "$pf" -a "$anchor" -nf "$snapshot"
        if [[ ! -e "$state/original.rules" ]]; then
            "$pf" -a "$anchor" -sr > "$state/original.tmp"
            "$pf" -s info > "$state/original.info"
            mv "$state/original.tmp" "$state/original.rules"
        fi
        if [[ ! -s "$state/token" ]]; then
            output="$("$pf" -E 2>&1)"
            printf '%s\n' "$output"
            token="$(printf '%s\n' "$output" | awk '/Token[[:space:]]*:/ {print $NF}')"
            [[ "$token" =~ ^[0-9]+$ ]] || { echo "Could not read the enable token" >&2; exit 1; }
            printf '%s\n' "$token" > "$state/token"
        fi
        "$pf" -a "$anchor" -f "$snapshot"
        "$pf" -a "$anchor" -vsr
        echo "Verify allowed and denied connections from the controller." ;;
    status)
        "$pf" -s info
        "$pf" -a "$anchor" -vsr ;;
    rollback)
        if [[ -f "$state/original.rules" ]]; then
            "$pf" -a "$anchor" -nf "$state/original.rules"
            "$pf" -a "$anchor" -f "$state/original.rules"
            if [[ -s "$state/token" ]]; then
                "$pf" -X "$(cat "$state/token")"
                mv "$state/token" "$state/token.released"
            fi
            "$pf" -a "$anchor" -sr | diff - "$state/original.rules"
            mv "$state/original.rules" "$state/original.rules.restored"
        fi ;;
    *) exit 2 ;;
esac
