#!/usr/bin/env bash
# Bootstrap verification: ensure required workflow layer paths exist.
# Run after cloning or restoring a workspace.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MISSING=0

echo "==> Bootstrap: verifying workflow layer at $ROOT"

for path in \
  ".gitignore" \
  ".agent/ROSTER.md" \
  ".agent/workflows/sdd-protocol.md" \
  ".agent/skills/README.md" \
  ".claude/agent-memory/solution-architect/MEMORY.md" \
  ".claude/agent-memory/verifier/MEMORY.md" \
  ".claude/skills/README.md" \
  ".codex/write-gate.md" \
  "docs/plans/README.md" \
  "docs/specs/README.md" \
  "docs/tasklist/README.md" \
  "docs/reports/README.md" \
  "memory_bank/context.md" \
  "memory_bank/progress.md" \
  "memory_bank/decisions.md"; do
  if [ ! -f "$ROOT/$path" ]; then
    echo "  MISSING: $path"
    MISSING=1
  else
    echo "  OK: $path"
  fi
done

if [ "$MISSING" -eq 1 ]; then
  echo "==> Workflow layer incomplete — review missing files above."
  exit 1
fi

echo "==> Workflow layer: OK"
