#!/usr/bin/env bash
# Smoke-test the Claude Code critic and verification gate decision boundaries.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CRITIC_HOOK_SRC="$ROOT/template/.claude/hooks/critic-gate.sh"
VERIFICATION_HOOK_SRC="$ROOT/template/.claude/hooks/verification-gate.sh"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required for critic-gate tests"
}

make_case_dir() {
  local dir="$1"
  mkdir -p "$dir/.agent" "$dir/.claude/hooks" "$dir/memory_bank" "$dir/src" "$dir/docs/reports"
  cp "$CRITIC_HOOK_SRC" "$dir/.claude/hooks/critic-gate.sh"
  cp "$VERIFICATION_HOOK_SRC" "$dir/.claude/hooks/verification-gate.sh"
  chmod +x "$dir/.claude/hooks/critic-gate.sh" "$dir/.claude/hooks/verification-gate.sh"
  printf '# Orchestrator Log\n\n| Work Block | Event |\n|---|---|\n' > "$dir/memory_bank/orchestrator-log.md"
  printf '# Critic Report\n\nVerdict: APPROVE\n' > "$dir/docs/reports/critic-WB-smoke.md"
  printf '# GPT Critic Report\n\nVerdict: APPROVE\n' > "$dir/docs/reports/gpt-critic-WB-smoke.md"
  printf '# Verification Report\n\nVerdict: READY\n' > "$dir/docs/reports/verification-WB-smoke.md"
  printf '# GPT Verifier Report\n\nVerdict: READY\n' > "$dir/docs/reports/gpt-verifier-WB-smoke.md"
}

write_gate() {
  local dir="$1"
  local status="$2"
  local topology="$3"
  local gpt="$4"
  local tier="${5:-lite}"
  local new_domain="${6:-false}"
  local critic_verdict="${7:-APPROVE}"

  cat > "$dir/.agent/critic-gate.md" <<EOF
Status: $status
Work Block: WB-smoke
Verification Tier: $tier
New Domain: $new_domain
Subagent Topology Status: $topology
Critic Verdict: $critic_verdict
Critic Report: docs/reports/critic-WB-smoke.md
GPT Critic Status: $gpt
GPT Critic Reason: no GPT critic trigger matched
GPT Critic Report: docs/reports/gpt-critic-WB-smoke.md
GPT Critic Degraded Reason: none

# Critic Gate

No-Skip: false

Approved Write-Set:
- src/**
EOF
}

write_verification_gate() {
  local dir="$1"
  local status="$2"
  local tier="$3"
  local new_domain="$4"
  local verifier_verdict="$5"
  local gpt="$6"
  local quick_fix="${7:-false}"

  cat > "$dir/.agent/verification-gate.md" <<EOF
Status: $status
Work Block: WB-smoke
Verification Tier: $tier
New Domain: $new_domain
Claude Verifier Verdict: $verifier_verdict
Verification Report: docs/reports/verification-WB-smoke.md
GPT Verifier Status: $gpt
GPT Verifier Reason: no GPT verifier trigger matched
GPT Verifier Report: docs/reports/gpt-verifier-WB-smoke.md
GPT Verifier Degraded Reason: none
Quick-Fix: $quick_fix
EOF
}

run_hook() {
  local dir="$1"
  local file_path="$2"
  local payload

  payload=$(printf '{"tool_name":"Edit","session_id":"smoke","tool_input":{"file_path":"%s"}}' "$file_path")
  (cd "$dir" && printf '%s' "$payload" | .claude/hooks/critic-gate.sh)
}

run_verification_hook() {
  local dir="$1"
  (cd "$dir" && printf '{}' | .claude/hooks/verification-gate.sh)
}

assert_denied_contains() {
  local dir="$1"
  local file_path="$2"
  local needle="$3"
  local output

  output="$(run_hook "$dir" "$file_path")"
  printf '%s' "$output" | grep -q '"permissionDecision": "deny"' \
    || fail "expected deny for $file_path, got: $output"
  printf '%s' "$output" | grep -q "$needle" \
    || fail "expected denial containing '$needle', got: $output"
}

assert_allowed_empty() {
  local dir="$1"
  local file_path="$2"
  local output

  output="$(run_hook "$dir" "$file_path")"
  [ -z "$output" ] || fail "expected allow with empty hook output, got: $output"
}

assert_verification_denied_contains() {
  local dir="$1"
  local needle="$2"
  local output

  output="$(run_verification_hook "$dir")"
  printf '%s' "$output" | grep -q '"decision": "block"' \
    || fail "expected verification deny, got: $output"
  printf '%s' "$output" | grep -q "$needle" \
    || fail "expected verification denial containing '$needle', got: $output"
}

assert_verification_allowed_empty() {
  local dir="$1"
  local output

  output="$(run_verification_hook "$dir")"
  [ -z "$output" ] || fail "expected verification allow with empty hook output, got: $output"
}

require_command jq

TMP_ROOT="${TMPDIR:-/tmp}/agentic-sdlc-critic-gate-smoke-$$"
trap 'rm -rf "$TMP_ROOT"' EXIT

CASE_DIR="$TMP_ROOT/case"
make_case_dir "$CASE_DIR"

write_gate "$CASE_DIR" "PENDING" "SINGLE_AGENT" "NOT_REQUIRED"
assert_denied_contains "$CASE_DIR" "src/app.py" "status is PENDING"

write_gate "$CASE_DIR" "READY" "SINGLE_AGENT" "PENDING"
assert_denied_contains "$CASE_DIR" "src/app.py" "GPT Critic Status"

write_gate "$CASE_DIR" "READY" "PENDING" "NOT_REQUIRED"
assert_denied_contains "$CASE_DIR" "src/app.py" "Subagent Topology Status"

write_gate "$CASE_DIR" "READY" "SINGLE_AGENT" "NOT_REQUIRED"
assert_denied_contains "$CASE_DIR" "README.md" "outside the Approved Write-Set"
assert_allowed_empty "$CASE_DIR" "src/app.py"
assert_allowed_empty "$CASE_DIR" ".agent/critic-gate.md"

rm "$CASE_DIR/docs/reports/critic-WB-smoke.md"
write_gate "$CASE_DIR" "READY" "SINGLE_AGENT" "NOT_REQUIRED"
assert_denied_contains "$CASE_DIR" "src/app.py" "Critic Report report does not exist"
printf '# Critic Report\n\nVerdict: APPROVE\n' > "$CASE_DIR/docs/reports/critic-WB-smoke.md"

write_gate "$CASE_DIR" "READY" "SINGLE_AGENT" "NOT_REQUIRED" "full" "false" "APPROVE"
assert_denied_contains "$CASE_DIR" "src/app.py" "GPT critic is required"

write_gate "$CASE_DIR" "READY" "SINGLE_AGENT" "READY" "full" "false" "APPROVE"
assert_allowed_empty "$CASE_DIR" "src/app.py"

mkdir -p "$CASE_DIR/.claude/agent-memory/critic"
assert_allowed_empty "$CASE_DIR" ".claude/agent-memory/critic/MEMORY.md"

write_verification_gate "$CASE_DIR" "PENDING" "lite" "false" "READY" "NOT_REQUIRED"
assert_verification_denied_contains "$CASE_DIR" "status is PENDING"

write_verification_gate "$CASE_DIR" "READY" "standard" "false" "READY" "NOT_REQUIRED"
assert_verification_allowed_empty "$CASE_DIR"

write_verification_gate "$CASE_DIR" "READY" "full" "false" "READY" "NOT_REQUIRED"
assert_verification_denied_contains "$CASE_DIR" "GPT verifier is required"

write_verification_gate "$CASE_DIR" "READY" "full" "false" "READY" "READY"
assert_verification_allowed_empty "$CASE_DIR"

write_verification_gate "$CASE_DIR" "READY" "full" "false" "READY" "DEGRADED"
assert_verification_denied_contains "$CASE_DIR" "GPT verifier DEGRADED requires"
sed -i 's/GPT Verifier Degraded Reason: none/GPT Verifier Degraded Reason: review-degraded:codex-mcp-unavailable/' "$CASE_DIR/.agent/verification-gate.md"
printf '| WB-smoke | review-degraded:codex-mcp-unavailable |\n' >> "$CASE_DIR/memory_bank/orchestrator-log.md"
assert_verification_allowed_empty "$CASE_DIR"

write_verification_gate "$CASE_DIR" "SKIPPED" "lite" "false" "PENDING" "NOT_REQUIRED" "true"
printf '| WB-smoke | verification: SKIPPED -- Quick-Fix -- docs-only |\n' >> "$CASE_DIR/memory_bank/orchestrator-log.md"
assert_verification_allowed_empty "$CASE_DIR"

echo "OK: critic/verification gate smoke tests passed"
