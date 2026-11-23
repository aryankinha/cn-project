#!/bin/bash
set -euo pipefail
exec python3 "$(dirname "$0")/phase2/demo.py" "$@"
