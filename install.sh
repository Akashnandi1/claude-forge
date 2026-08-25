#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="install.py"
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/$TARGET" "$@"
fi
if command -v python >/dev/null 2>&1 && python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/$TARGET" "$@"
fi
printf 'ERROR: Python 3.11+ is required.\n' >&2
exit 1
