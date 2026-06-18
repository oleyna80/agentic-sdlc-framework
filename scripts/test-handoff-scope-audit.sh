#!/usr/bin/env bash
# Regression tests for handoff-runner scope audit.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/agentic-sdlc-scope-audit.XXXXXX")"
FAKE_BIN="$TMP_ROOT/bin"
RUNNER_OUT="$TMP_ROOT/runner.out"

cleanup() {
  rm -rf "$TMP_ROOT"
  rm -f "$ROOT"/handoff/queue/scope-audit-*."md"
  rm -f "$ROOT"/handoff/active/scope-audit-*."md"
  rm -f "$ROOT"/handoff/done/scope-audit-*."md"
  rm -f "$ROOT"/handoff/done/scope-audit-*-result.md
  rm -f "$ROOT"/handoff/failed/scope-audit-*."md"
  rm -f "$ROOT"/handoff/failed/scope-audit-*-result.md
  rm -f "$ROOT"/handoff/logs/session-scope-audit-*.log
  rm -rf "$ROOT"/handoff/runtime/scope-audit-*
}
trap cleanup EXIT

mkdir -p "$FAKE_BIN"

create_project() {
  local project_root="$1"

  mkdir -p "$project_root/memory_bank" "$project_root/.agent" "$project_root/.claude/agent-memory"
  cat > "$project_root/.gitignore" <<'GITIGNORE'
.agent/
.claude/
memory_bank/
.next/
tsconfig.tsbuildinfo
GITIGNORE
  git -C "$project_root" init -q
}

write_fake_claude() {
  local mode="$1"

  cat > "$FAKE_BIN/claude" <<FAKE_CLAUDE
#!/usr/bin/env bash
set -euo pipefail
case "$mode" in
  cc_process_allowed)
    mkdir -p memory_bank .agent .claude/agent-memory/verifier
    mkdir -p .next/cache
    printf 'external team log\n' > memory_bank/external-team-log.md
    printf 'orchestrator log\n' > memory_bank/orchestrator-log.md
    printf 'review log\n' > memory_bank/review-log.md
    printf 'critic gate\n' > .agent/critic-gate.md
    printf 'verification gate\n' > .agent/verification-gate.md
    printf 'verifier memory\n' > .claude/agent-memory/verifier/catalog-ux-patterns.md
    printf 'next cache\n' > .next/cache/noise.txt
    printf 'typescript build info\n' > tsconfig.tsbuildinfo
    ;;
  nested_allowed)
    mkdir -p memory_bank/deep/nested
    printf 'nested ok\n' > memory_bank/deep/nested/review-log.md
    ;;
  out_of_scope)
    mkdir -p memory_bank .agent
    printf 'allowed\n' > memory_bank/handoff-scope-allowed.txt
    printf 'outside\n' > .agent/outside-scope.txt
    ;;
  forbidden)
    printf 'secret=true\n' > .env
    ;;
  forbidden_build_artifact)
    mkdir -p .next/cache
    printf 'forbidden next cache\n' > .next/cache/noise.txt
    printf 'forbidden typescript build info\n' > tsconfig.tsbuildinfo
    ;;
  control_plane_tamper)
    mkdir -p memory_bank handoff/queue handoff/done
    printf 'allowed\n' > memory_bank/handoff-scope-allowed.txt
    printf 'queued injection\n' > handoff/queue/injected.md
    printf 'done injection\n' > handoff/done/injected-result.md
    ;;
  *)
    echo "unknown fake mode: $mode" >&2
    exit 2
    ;;
esac
printf 'fake claude complete\n'
FAKE_CLAUDE
  chmod +x "$FAKE_BIN/claude"
}

write_task() {
  local task_id="$1"
  local project_root="$2"
  local allowed_scope="$3"
  local forbidden_scope="$4"
  local task_file="$ROOT/handoff/queue/$task_id.md"

  {
    printf '%s\n' '---'
    printf 'task_id: %s\n' "$task_id"
    printf '%s\n' 'from: codex'
    printf '%s\n' 'to: claude'
    printf '%s\n' 'timeout_seconds: 30'
    printf 'project_root: %s\n' "$project_root"
    printf '%s\n' 'allowed_scope:'
    printf '%s\n' "$allowed_scope"
    printf '%s\n' 'forbidden_scope:'
    printf '%s\n' "$forbidden_scope"
    printf '%s\n' '---'
    printf '\n# Objective\n\nRun the fake Claude executable.\n'
  } > "$task_file"
}

run_case() {
  local task_id="$1"
  local expected_exit="$2"
  local project_root="$TMP_ROOT/$task_id-project"

  create_project "$project_root"
  write_task "$task_id" "$project_root" "$3" "$4"

  set +e
  PATH="$FAKE_BIN:$PATH" "$ROOT/handoff/runner/handoff-runner.sh" "$ROOT/handoff/queue/$task_id.md" > "$RUNNER_OUT" 2>&1
  local runner_exit=$?
  set -e

  if [ "$runner_exit" -ne "$expected_exit" ]; then
    cat "$RUNNER_OUT"
    echo "FAIL: expected runner exit $expected_exit for $task_id, got $runner_exit" >&2
    exit 1
  fi
}

assert_result_contains() {
  local result_file="$1"
  local needle="$2"

  if ! grep -q "$needle" "$result_file"; then
    cat "$result_file"
    echo "FAIL: expected result to contain: $needle" >&2
    exit 1
  fi
}

assert_result_not_contains() {
  local result_file="$1"
  local needle="$2"

  if grep -q "$needle" "$result_file"; then
    cat "$result_file"
    echo "FAIL: expected result not to contain: $needle" >&2
    exit 1
  fi
}

TASK_ID="scope-audit-cc-process-$$"
write_fake_claude "cc_process_allowed"
run_case "$TASK_ID" 0 \
"  - memory_bank/external-team-log.md
  - memory_bank/orchestrator-log.md
  - memory_bank/review-log.md
  - .agent/critic-gate.md
  - .agent/verification-gate.md
  - .claude/agent-memory/**" \
"  - .env
  - .env.*"
RESULT_FILE="$ROOT/handoff/done/$TASK_ID-result.md"
assert_result_contains "$RESULT_FILE" '^status: complete$'
assert_result_contains "$RESULT_FILE" '== scope-audit =='
assert_result_contains "$RESULT_FILE" 'status=passed'
assert_result_contains "$RESULT_FILE" '.claude/agent-memory/verifier/catalog-ux-patterns.md'
assert_result_contains "$RESULT_FILE" 'memory_bank/review-log.md'
assert_result_not_contains "$RESULT_FILE" '.next/cache/noise.txt'
assert_result_not_contains "$RESULT_FILE" 'tsconfig.tsbuildinfo'

TASK_ID="scope-audit-nested-allowed-$$"
write_fake_claude "nested_allowed"
run_case "$TASK_ID" 0 \
"  - memory_bank/deep/**" \
"  - .env"
RESULT_FILE="$ROOT/handoff/done/$TASK_ID-result.md"
assert_result_contains "$RESULT_FILE" '^status: complete$'
assert_result_contains "$RESULT_FILE" 'memory_bank/deep/nested/review-log.md'
assert_result_not_contains "$RESULT_FILE" 'outside_allowed_scope:memory_bank'
assert_result_not_contains "$RESULT_FILE" 'outside_allowed_scope:memory_bank/deep'

TASK_ID="scope-audit-outside-$$"
write_fake_claude "out_of_scope"
run_case "$TASK_ID" 90 \
"  - memory_bank/handoff-scope-allowed.txt" \
"  - .env"
RESULT_FILE="$ROOT/handoff/failed/$TASK_ID-result.md"
assert_result_contains "$RESULT_FILE" '^status: scope_failed$'
assert_result_contains "$RESULT_FILE" 'outside_allowed_scope:.agent/outside-scope.txt'
assert_result_contains "$RESULT_FILE" 'memory_bank/handoff-scope-allowed.txt'

TASK_ID="scope-audit-forbidden-$$"
write_fake_claude "forbidden"
run_case "$TASK_ID" 90 \
"  - .env" \
"  - .env
  - .env.*"
RESULT_FILE="$ROOT/handoff/failed/$TASK_ID-result.md"
assert_result_contains "$RESULT_FILE" '^status: scope_failed$'
assert_result_contains "$RESULT_FILE" 'forbidden_scope:.env'

TASK_ID="scope-audit-forbidden-build-$$"
write_fake_claude "forbidden_build_artifact"
run_case "$TASK_ID" 90 \
"  - src/**" \
"  - .next/**
  - tsconfig.tsbuildinfo"
RESULT_FILE="$ROOT/handoff/failed/$TASK_ID-result.md"
assert_result_contains "$RESULT_FILE" '^status: scope_failed$'
assert_result_contains "$RESULT_FILE" 'forbidden_scope:.next/cache/noise.txt'
assert_result_contains "$RESULT_FILE" 'forbidden_scope:tsconfig.tsbuildinfo'

TASK_ID="scope-audit-control-plane-$$"
write_fake_claude "control_plane_tamper"
run_case "$TASK_ID" 90 \
"  - memory_bank/handoff-scope-allowed.txt" \
"  - .env"
RESULT_FILE="$ROOT/handoff/failed/$TASK_ID-result.md"
assert_result_contains "$RESULT_FILE" '^status: scope_failed$'
assert_result_contains "$RESULT_FILE" 'outside_allowed_scope:handoff/queue/injected.md'
assert_result_contains "$RESULT_FILE" 'outside_allowed_scope:handoff/done/injected-result.md'

echo "OK: handoff scope audit covers CC process files, out-of-scope files, and forbidden files"
