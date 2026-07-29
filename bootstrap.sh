#!/usr/bin/env bash
# bootstrap.sh — profile-aware Agentic SDLC project scaffold wrapper.
#
# Backward-compatible usage:
#   ./bootstrap.sh <target-dir> [project-name] [project-slug]
#
# Profile-aware usage:
#   ./bootstrap.sh --profile codex <target-dir> [project-name] [project-slug]
#   ./bootstrap.sh --list-profiles
set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$FRAMEWORK_DIR/bootstrap/bootstrap_project.py" "$@"
