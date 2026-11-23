#!/bin/bash
# Manual backend entry point. The deployed service uses node.sh.
set -euo pipefail
cd "$(dirname "$0")/../backend"

case "${1:-}" in
    --setup)
        if [[ ! -x .venv/bin/python ]]; then python3 -m venv .venv; fi
        .venv/bin/python -m pip install -r requirements.txt
        .venv/bin/python -m pip check
        exit ;;
    A) port=3001 ;;
    B) port=3002 ;;
    *) echo "Usage: $0 --setup | A | B" >&2; exit 2 ;;
esac

if [[ ! -x .venv/bin/python ]]; then
    echo "Run $0 --setup before starting either backend." >&2
    exit 1
fi

BACKEND_ID="$1" PORT="$port" exec .venv/bin/python app.py
