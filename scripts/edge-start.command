#!/bin/bash
# Executed by the logged-in owner's Terminal when SSH cannot start LAN nginx.
set -euo pipefail
home="$HOME/cn-project"
exec >>"$home/logs/edge-terminal-start.log" 2>&1
date
unset SSH_CONNECTION SSH_CLIENT SSH_TTY
"$home/bin/node.sh" start edge
