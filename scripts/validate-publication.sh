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
  "scripts/test-handoff-scope-audit.sh" \
  "template/project.gitignore" \
  "template/.agent/ROSTER.md" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/.agent/skills/README.md" \
  "template/.mcp.json" \
  "template/.claude/settings.json" \
  "template/.claude/agent-memory/codex-reviewer/MEMORY.md" \
  "template/.claude/agent-memory/critic/MEMORY.md" \
  "template/.claude/agent-memory/gpt-critic/MEMORY.md" \
  "template/.claude/agent-memory/gpt-verifier/MEMORY.md" \
  "template/.claude/agent-memory/reviewer/MEMORY.md" \
  "template/.claude/agent-memory/scoped-coder/MEMORY.md" \
  "template/.claude/agent-memory/solution-architect/MEMORY.md" \
  "template/.claude/agent-memory/verifier/MEMORY.md" \
  "template/.claude/agents/codex-reviewer.md" \
  "template/.claude/agents/critic.md" \
  "template/.claude/agents/gpt-critic.md" \
  "template/.claude/agents/gpt-verifier.md" \
  "template/.claude/agents/reviewer.md" \
  "template/.claude/agents/scoped-coder.md" \
  "template/.claude/agents/solution-architect.md" \
  "template/.claude/agents/verifier.md" \
  "template/.claude/hooks/critic-gate.sh" \
  "template/.claude/hooks/hard-stop.sh" \
  "template/.claude/hooks/typecheck.sh" \
  "template/.claude/hooks/verification-gate.sh" \
  "template/.claude/skills/README.md" \
  "template/.agent/critic-gate.md" \
  "template/.agent/verification-gate.md" \
  "template/.codex/write-gate.md" \
  "template/memory_bank/external-team-log.md" \
  "template/docs/plans/README.md" \
  "template/docs/specs/README.md" \
  "template/docs/tasklist/README.md" \
  "template/docs/reports/README.md" \
  "framework/knowledge/README.md" \
  "framework/knowledge/claude-code-cli.md" \
  "framework/knowledge/claude-code-global-bootstrap.md" \
  "handoff/.gitignore" \
  "handoff/README.md" \
  "handoff/active/.gitkeep" \
  "handoff/done/.gitkeep" \
  "handoff/failed/.gitkeep" \
  "handoff/logs/.gitkeep" \
  "handoff/parallel/.gitkeep" \
  "handoff/queue/.gitkeep" \
  "handoff/runtime/.gitkeep" \
  "handoff/runner/cleanup.sh" \
  "handoff/runner/handoff-runner.sh" \
  "handoff/runner/install-systemd-user-service.sh" \
  "handoff/runner/parallel-runner.sh" \
  "handoff/runner/sanitize-env.sh" \
  "handoff/runner/watch-queue.sh" \
  "handoff/systemd/agentic-sdlc-handoff.service.template" \
  "handoff/systemd/handoff.env.example" \
  "handoff/templates/claude-team-task-template.md"; do
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

PRIVATE_MARKERS='azursystech|choushop|178\.156\.212\.10|/home/dmitrii|oleyna80|home-dmitrii'
if command -v rg >/dev/null 2>&1; then
  PRIVATE_HITS="$(rg --hidden --no-ignore -n -i "$PRIVATE_MARKERS" "$ROOT" -g '!.git/**' -g '!archive/**' -g '!**/scripts/validate-publication.sh' || true)"
else
  PRIVATE_HITS="$(grep -RInE --exclude-dir=.git --exclude-dir=archive --exclude=validate-publication.sh "$PRIVATE_MARKERS" "$ROOT" || true)"
fi
if [ -n "$PRIVATE_HITS" ]; then
  echo "$PRIVATE_HITS"
  fail "private project markers found in public paths"
else
  ok "no known private project markers in public paths"
fi

for script in \
  "$ROOT/bootstrap.sh" \
  "$ROOT/scripts/test-critic-gate.sh" \
  "$ROOT/scripts/test-handoff-scope-audit.sh" \
  "$ROOT/template/scripts/bootstrap.sh" \
  "$ROOT/template/.claude/hooks/hard-stop.sh" \
  "$ROOT/template/.claude/hooks/typecheck.sh" \
  "$ROOT/template/.claude/hooks/verification-gate.sh" \
  "$ROOT/scripts/validate-publication.sh" \
  "$ROOT/handoff/runner/cleanup.sh" \
  "$ROOT/handoff/runner/handoff-runner.sh" \
  "$ROOT/handoff/runner/install-systemd-user-service.sh" \
  "$ROOT/handoff/runner/parallel-runner.sh" \
  "$ROOT/handoff/runner/sanitize-env.sh" \
  "$ROOT/handoff/runner/watch-queue.sh"; do
  bash -n "$script" || fail "bash syntax failed: $script"
done
ok "bash syntax checks completed"

"$ROOT/scripts/test-critic-gate.sh" || fail "critic gate smoke tests failed"
"$ROOT/scripts/test-handoff-scope-audit.sh" || fail "handoff scope audit smoke test failed"

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
