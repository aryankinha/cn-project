#!/bin/bash
set -euo pipefail
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:$PATH"
home="$HOME/cn-project"
source "$home/node.env"
action="${1:-status}"
selection="${2:-all}"
dns="$home/dnsmasq/dnsmasq.conf"
edge="$home/nginx/nginx.conf"
app="$home/backend/app.py"

owns() {
    local pid="$1" marker="$2" owner command
    [[ "$pid" =~ ^[1-9][0-9]*$ ]] || return 1
    owner="$(ps -p "$pid" -o uid= | tr -d ' ')" || return 1
    command="$(ps -p "$pid" -o command=)" || return 1
    [[ "$owner" == "$UID" && "$command" == *"$marker"* ]]
}

stop() {
    local signal="$1" attempt
    if owns "$pid" "$marker"; then
        kill "-$signal" "$pid"
        for attempt in {1..50}; do owns "$pid" "$marker" || return 0; sleep .2; done
        echo "$service did not stop" >&2
        return 1
    fi
}

operate() {
    local service="$1" verb="$2" pid marker file found attempt
    case "$service" in
        dns) marker="$dns"; file="$home/run/dnsmasq.pid" ;;
        edge) marker="$edge"; file="$home/run/nginx.pid" ;;
        backend) marker="$app"; file="$home/run/backend-$BACKEND_ID.pid" ;;
        *) return 2 ;;
    esac
    [[ " $ROLES " == *" $service "* ]] || { echo "$service is not assigned to $NODE" >&2; return 2; }
    pid="$(cat "$file" 2>/dev/null || true)"
    case "$verb" in
        status) owns "$pid" "$marker" && echo "$NODE $service up pid=$pid" || { echo "$NODE $service down"; return 1; } ;;
        stop) if [[ "$service" == edge ]]; then stop QUIT; else stop TERM; fi ;;
        reload)
            owns "$pid" "$marker" || return 1
            case "$service" in
                dns) kill -HUP "$pid" ;;
                edge) nginx -p "$home/" -c "$edge" -t && kill -HUP "$pid" ;;
                *) return 2 ;;
            esac ;;
        restart) operate "$service" stop; operate "$service" start ;;
        start)
            if owns "$pid" "$marker"; then return 0; fi
            case "$service" in
                dns) dnsmasq --test --conf-file="$dns"; dnsmasq --conf-file="$dns" ;;
                edge)
                    nginx -p "$home/" -c "$edge" -t
                    if [[ -n "${SSH_CONNECTION:-}" ]]; then
                        if [[ "$(stat -f %Su /dev/console)" != "$(id -un)" ]]; then
                            echo "Edge startup requires the owner to be logged into macOS" >&2
                            return 1
                        fi
                        /usr/bin/open -a Terminal "$home/bin/edge-start.command"
                        for attempt in {1..20}; do
                            if owns "$(cat "$file" 2>/dev/null || true)" "$marker"; then break; fi
                            sleep .5
                        done
                    else
                        nginx -p "$home/" -c "$edge"
                    fi ;;
                backend)
                    test -x "$home/backend/.venv/bin/python"
                    if lsof -tiTCP:"$BACKEND_PORT" -sTCP:LISTEN >/dev/null; then
                        echo "TCP $BACKEND_PORT already occupied" >&2; return 1
                    fi
                    BACKEND_ID="$BACKEND_ID" PORT="$BACKEND_PORT" nohup \
                      "$home/backend/.venv/bin/python" "$app" </dev/null \
                      >>"$home/logs/backend-$BACKEND_ID.log" 2>&1 &
                    for attempt in {1..30}; do
                        found="$(lsof -tiTCP:"$BACKEND_PORT" -sTCP:LISTEN | head -1 || true)"
                        if owns "$found" "$marker"; then printf '%s\n' "$found" > "$file"; return 0; fi
                        sleep .2
                    done
                    echo "Backend $BACKEND_ID did not bind" >&2; return 1 ;;
            esac
            operate "$service" status ;;
        health)
            operate "$service" status
            case "$service" in
                dns) dig @127.0.0.1 "app.$DOMAIN" A +time=2 +tries=1 +short | grep -E '^[0-9]+(\.[0-9]+){3}$' ;;
                edge) curl --noproxy '*' -fsS --max-time 5 --cacert "$home/tls/edge.crt" \
                    --resolve "app.$DOMAIN:443:127.0.0.1" "https://app.$DOMAIN/edge-health" | grep -Fx "edge $EDGE_ID ok" ;;
                backend) curl --noproxy '*' -fsS --max-time 5 -D - -o /dev/null \
                    "http://127.0.0.1:$BACKEND_PORT/api/status" | tr -d '\r' | grep -ix "X-Backend: $BACKEND_ID" ;;
            esac ;;
        *) echo "Use status, start, stop, restart, reload or health [dns|edge|backend]" >&2; return 2 ;;
    esac
}

if [[ "$selection" != all ]]; then operate "$selection" "$action"; exit; fi
rc=0
for service in $ROLES; do
    if [[ "$action" == status || "$action" == health ]]; then
        operate "$service" "$action" || rc=1
    else
        operate "$service" "$action"
    fi
done
exit "$rc"
