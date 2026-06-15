#!/usr/bin/env bash
# Regression test: scope audit must catch ignored local-first paths.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TASK_ID="scope-audit-$$"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/agentic-sdlc-scope-audit.XXXXXX")"
PROJECT_ROOT="$TMP_ROOT/project"
FAKE_BIN="$TMP_ROOT/bin"
TASK_FILE="$ROOT/handoff/queue/$TASK_ID.md"
RUNNER_OUT="$TMP_ROOT/runner.out"

cleanup() {
  rm -rf "$TMP_ROOT"
  rm -f \
    "$ROOT/handoff/queue/$TASK_ID.md" \
    "$ROOT/handoff/active/$TASK_ID.md" \
    "$ROOT/handoff/done/$TASK_ID.md" \
    "$ROOT/handoff/done/$TASK_ID-result.md" \
    "$ROOT/handoff/failed/$TASK_ID.md" \
    "$ROOT/handoff/failed/$TASK_ID-result.md"
  rm -f "$ROOT"/handoff/logs/session-"$TASK_ID"-*.log
  rm -rf "$ROOT"/handoff/runtime/"$TASK_ID"-*
}
trap cleanup EXIT

mkdir -p "$PROJECT_ROOT/memory_bank" "$PROJECT_ROOT/.agent" "$FAKE_BIN"
cat > "$PROJECT_ROOT/.gitignore" <<'GITIGNORE'
.agent/
memory_bank/
GITIGNORE
git -C "$PROJECT_ROOT" init -q

cat > "$FAKE_BIN/claude" <<'FAKE_CLAUDE'
#!/usr/bin/env bash
mkdir -p memory_bank .agent
printf 'allowed\n' > memory_bank/handoff-scope-allowed.txt
printf 'outside\n' > .agent/outside-scope.txt
printf 'fake claude complete\n'
FAKE_CLAUDE
chmod +x "$FAKE_BIN/claude"

cat > "$TASK_FILE" <<EOF
---
task_id: $TASK_ID
from: codex
to: claude
timeout_seconds: 30
project_root: $PROJECT_ROOT
allowed_scope:
  - memory_bank/handoff-scope-allowed.txt
forbidden_scope:
  - .env
---

# Objective

Run the fake Claude executable.
EOF

set +e
PATH="$FAKE_BIN:$PATH" "$ROOT/handoff/runner/handoff-runner.sh" "$TASK_FILE" > "$RUNNER_OUT" 2>&1
RUNNER_EXIT=$?
set -e

if [ "$RUNNER_EXIT" -ne 90 ]; then
  cat "$RUNNER_OUT"
  echo "FAIL: expected runner exit 90 for scope violation, got $RUNNER_EXIT" >&2
  exit 1
fi

if ! grep -q '^status=scope_failed$' "$RUNNER_OUT"; then
  cat "$RUNNER_OUT"
  echo "FAIL: expected status=scope_failed" >&2
  exit 1
fi

RESULT_FILE="$ROOT/handoff/failed/$TASK_ID-result.md"
[ -f "$RESULT_FILE" ] || {
  cat "$RUNNER_OUT"
  echo "FAIL: missing result file $RESULT_FILE" >&2
  exit 1
}

if ! grep -q 'outside_allowed_scope:.agent/outside-scope.txt' "$RESULT_FILE"; then
  cat "$RESULT_FILE"
  echo "FAIL: ignored .agent/ path was not reported as outside allowed scope" >&2
  exit 1
fi

if ! grep -q 'memory_bank/handoff-scope-allowed.txt' "$RESULT_FILE"; then
  cat "$RESULT_FILE"
  echo "FAIL: allowed changed path missing from scope audit output" >&2
  exit 1
fi

echo "OK: handoff scope audit catches ignored out-of-scope paths"
