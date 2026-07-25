#!/usr/bin/env bash
# Public framework validation wrapper.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/validate_publication.py" "$@"
