#!/usr/bin/env bash
# Public framework validation wrapper.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/validate_publication.py" "$@"
python3 "$ROOT/scripts/test-profile-restore.py"
