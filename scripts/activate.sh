#!/bin/bash
set -euo pipefail
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:$PATH"
home="$HOME/cn-project"
mode="$1"
stage="$2"
[[ "$stage" == "$home"/releases/* ]] || exit 2
source "$stage/node.env"
control="$home/bin/node.sh"
backup="$stage/previous"
files=(node.env bin/node.sh bin/client.sh bin/firewall.sh)
dns_files=(dnsmasq/dnsmasq.conf dnsmasq/project.hosts)
edge_files=(nginx/nginx.conf nginx/cn-project.conf)
backend_files=(backend/app.py backend/requirements.txt firewall/strict.pf firewall/standby.pf)

has() { [[ " $ROLES " == *" $1 "* ]]; }
has dns && files+=("${dns_files[@]}")
has edge && files+=("${edge_files[@]}" bin/edge-start.command)
has backend && files+=("${backend_files[@]}")

validate() {
    mkdir -p "$home"/{run,logs}
    for path in "${files[@]}"; do
        test -s "$stage/$path" || { echo "Staged file missing or empty: $path" >&2; return 1; }
        case "$path" in bin/*) bash -n "$stage/$path" ;; esac
    done
    if has dns; then dnsmasq --test --conf-file="$stage/dnsmasq/dnsmasq.conf"; fi
    if has edge; then
        test -r "$home/tls/edge.crt" && test -r "$home/tls/edge.key"
        sed "s|include cn-project.conf;|include $stage/nginx/cn-project.conf;|" \
          "$stage/nginx/nginx.conf" > "$stage/nginx/validate.conf"
        nginx -p "$home/" -c "$stage/nginx/validate.conf" -t
    fi
    if has backend; then
        for profile in strict standby; do
            /sbin/pfctl -a com.apple/cn-project-phase2 -nf "$stage/firewall/$profile.pf"
        done
        venv="$home/backend/.venv"
        if [[ ! -x "$venv/bin/python" ]]; then python3 -m venv "$venv"; fi
        if ! "$venv/bin/python" -B -c 'from importlib.metadata import version; assert version("flask") == "3.0.3"'; then
            "$venv/bin/python" -m pip install -r "$stage/backend/requirements.txt"
        fi
        "$venv/bin/python" -m pip check
        "$venv/bin/python" -B -c 'import runpy,sys; runpy.run_path(sys.argv[1])' "$stage/backend/app.py"
    fi
}

publish() {
    local from="$1" to="$2" tmp
    mkdir -p "$(dirname "$to")"
    tmp="$(mktemp "$to.XXXXXX")"
    cp "$from" "$tmp"
    if [[ "$to" == "$home/bin/"* ]]; then chmod 700 "$tmp"; fi
    mv "$tmp" "$to"
}

changed() {
    ! cmp -s "$backup/$1" "$home/$1"
}

activate_services() {
    if has backend; then
        if ! "$control" status backend; then "$control" start backend
        elif changed backend/app.py || changed backend/requirements.txt; then "$control" restart backend
        fi
    fi
    if has edge; then
        if ! "$control" status edge; then "$control" start edge
        elif changed nginx/nginx.conf || changed nginx/cn-project.conf; then "$control" reload edge
        fi
    fi
    if has dns; then
        if ! "$control" status dns; then "$control" start dns
        elif changed dnsmasq/dnsmasq.conf; then "$control" restart dns
        fi
    fi
    "$control" health
}

rollback() {
    local path service failed=0
    test -f "$backup/ready" || return 1
    for service in $ROLES; do
        if [[ "$service" == edge ]] && grep -qx edge "$backup/active"; then continue; fi
        "$control" stop "$service" || failed=1
    done
    for path in "${files[@]}"; do
        if [[ -f "$backup/$path" ]]; then publish "$backup/$path" "$home/$path" || failed=1
        elif [[ -f "$home/$path" ]]; then unlink "$home/$path" || failed=1
        fi
    done
    for service in $(cat "$backup/active"); do
        if [[ -x "$control" ]]; then
            if [[ "$service" == edge ]] && "$control" status edge; then
                "$control" reload edge || failed=1
            else
                "$control" start "$service" || failed=1
            fi
        else
            "$home/bin/cn.sh" "$service" start || failed=1
        fi
    done
    return "$failed"
}

case "$mode" in
    validate) validate ;;
    activate)
        validate
        mkdir "$backup"
        : > "$backup/active"
        for service in $ROLES; do
            if [[ -x "$control" ]]; then
                if "$control" status "$service"; then echo "$service" >> "$backup/active"; fi
            elif [[ -x "$home/bin/cn.sh" ]] && "$home/bin/cn.sh" "$service" status | grep -q ' up '; then
                echo "$service" >> "$backup/active"
            fi
        done
        for path in "${files[@]}"; do
            if [[ -f "$home/$path" ]]; then
                mkdir -p "$backup/$(dirname "$path")"
                cp -p "$home/$path" "$backup/$path"
            fi
        done
        touch "$backup/ready"
        trap 'rc=$?; trap - EXIT; if ((rc)); then rollback || echo "ROLLBACK INCOMPLETE: $NODE" >&2; fi; exit "$rc"' EXIT
        for path in "${files[@]}"; do
            if [[ "$path" == dnsmasq/project.hosts && -e "$home/$path" ]]; then continue; fi
            publish "$stage/$path" "$home/$path"
        done
        activate_services
        echo "Activated $NODE using $stage"
        ;;
    rollback) rollback ;;
    *) exit 2 ;;
esac
