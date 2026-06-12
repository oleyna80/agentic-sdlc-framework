#!/usr/bin/env bash
# Validate that the framework is safe and coherent enough for public release.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0

fail() {
  echo "FAIL: $*"
  FAIL=1
}

ok() {
  echo "OK: $*"
}

require_file() {
  local path="$1"
  if [ -f "$ROOT/$path" ]; then
    ok "$path"
  else
    fail "missing $path"
  fi
}

require_absent() {
  local path="$1"
  if [ -e "$ROOT/$path" ]; then
    fail "$path must not exist in the publishable scaffold"
  else
    ok "$path absent"
  fi
}

echo "==> Publication validation: $ROOT"

for path in \
  "README.md" \
  "SETUP.md" \
  "LICENSE" \
  "THIRD_PARTY_NOTICES.md" \
  "CONTRIBUTING.md" \
  "SECURITY.md" \
  "CHANGELOG.md" \
  "PUBLICATION_CHECKLIST.md" \
  "bootstrap.sh" \
  "template/project.gitignore" \
  "template/.agent/ROSTER.md" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/.agent/skills/README.md" \
  "template/.claude/agent-memory/solution-architect/MEMORY.md" \
  "template/.claude/agent-memory/verifier/MEMORY.md" \
  "template/.claude/skills/README.md" \
  "template/.codex/write-gate.md" \
  "template/docs/plans/README.md" \
  "template/docs/specs/README.md" \
  "template/docs/tasklist/README.md" \
  "template/docs/reports/README.md"; do
  require_file "$path"
done

require_absent "template/.gitignore"

if grep -qx 'archive/' "$ROOT/.gitignore"; then
  ok "archive/ is ignored"
else
  fail "archive/ is not ignored in root .gitignore"
fi

BYTECODE="$(
  find "$ROOT" \
    -path "$ROOT/archive" -prune -o \
    \( -name '*.pyc' -o -name '__pycache__' \) -print
)"
if [ -n "$BYTECODE" ]; then
  echo "$BYTECODE"
  fail "generated Python bytecode/cache files found"
else
  ok "no Python bytecode/cache files in public paths"
fi

PRIVATE_MARKERS='azursystech|178\.156\.212\.10|/home/dmitrii|oleyna80|home-dmitrii'
if command -v rg >/dev/null 2>&1; then
  PRIVATE_HITS="$(rg -n -i "$PRIVATE_MARKERS" "$ROOT" -g '!archive/**' -g '!scripts/validate-publication.sh' || true)"
else
  PRIVATE_HITS="$(grep -RInE --exclude-dir=archive --exclude=validate-publication.sh "$PRIVATE_MARKERS" "$ROOT" || true)"
fi
if [ -n "$PRIVATE_HITS" ]; then
  echo "$PRIVATE_HITS"
  fail "private project markers found in public paths"
else
  ok "no known private project markers in public paths"
fi

for script in \
  "$ROOT/bootstrap.sh" \
  "$ROOT/template/scripts/bootstrap.sh" \
  "$ROOT/template/.claude/hooks/hard-stop.sh" \
  "$ROOT/template/.claude/hooks/typecheck.sh" \
  "$ROOT/scripts/validate-publication.sh"; do
  bash -n "$script" || fail "bash syntax failed: $script"
done
ok "bash syntax checks completed"

if command -v python3 >/dev/null 2>&1; then
  python3 -B -c 'import ast, pathlib, sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())' "$ROOT/template/.codex/hooks/stage0_write_gate.py" || fail "Python syntax failed"
  ok "Python hook syntax checks"
else
  echo "WARN: python3 not found; skipped Python hook compile"
fi

SMOKE_DIR="${TMPDIR:-/tmp}/agentic-sdlc-framework-smoke-$$"
"$ROOT/bootstrap.sh" "$SMOKE_DIR" "Smoke & Project" "smoke-project"

if command -v rg >/dev/null 2>&1; then
  PLACEHOLDERS="$(rg -n '\{\{' "$SMOKE_DIR" || true)"
else
  PLACEHOLDERS="$(grep -RIn '{{' "$SMOKE_DIR" || true)"
fi
if [ -n "$PLACEHOLDERS" ]; then
  echo "$PLACEHOLDERS"
  fail "unresolved placeholders found in smoke project"
else
  ok "smoke project placeholders replaced"
fi

SMOKE_BYTECODE="$(
  find "$SMOKE_DIR" \( -name '*.pyc' -o -name '__pycache__' \) -print
)"
if [ -n "$SMOKE_BYTECODE" ]; then
  echo "$SMOKE_BYTECODE"
  fail "bytecode copied into smoke project"
else
  ok "no bytecode copied into smoke project"
fi

rm -rf "$SMOKE_DIR"

if [ "$FAIL" -ne 0 ]; then
  echo "==> Publication validation failed"
  exit 1
fi

echo "==> Publication validation OK"
