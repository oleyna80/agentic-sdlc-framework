#!/usr/bin/env bash
# Public framework validation wrapper.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EMPTY_GIT_CONFIG="$(mktemp)"
trap 'rm -f "$EMPTY_GIT_CONFIG"' EXIT
export GIT_CONFIG_GLOBAL="$EMPTY_GIT_CONFIG"

python3 "$ROOT/scripts/validate_publication.py" "$@"
python3 "$ROOT/scripts/test-profile-restore.py"
