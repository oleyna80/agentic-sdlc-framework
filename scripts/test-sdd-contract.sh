#!/usr/bin/env bash
# Detect drift between the canonical SDD protocol and its direct consumers.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

require_contains() {
  local path="$1"
  local pattern="$2"
  grep -Eq -- "$pattern" "$ROOT/$path" || fail "$path missing contract pattern: $pattern"
}

assert_quick_fix() {
  local expected="$1"
  local implementation_files="$2"
  local impact="$3"
  local actual="no"

  if [ "$implementation_files" -le 2 ] && [ "$impact" = "none" ]; then
    actual="yes"
  fi
  [ "$actual" = "$expected" ] || fail "Quick-Fix fixture files=$implementation_files impact=$impact expected=$expected got=$actual"
}

assert_quick_fix yes 2 none
assert_quick_fix no 3 none
for impact in logic route schema api security governance; do
  assert_quick_fix no 1 "$impact"
done

require_contains "template/.agent/workflows/sdd-protocol.md" 'Verification verdict:'
require_contains "template/.agent/workflows/sdd-protocol.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "template/docs/templates/work-block-template.md" 'Stage 3 Mode'
require_contains "template/.agent/critic-gate.md" '^Approved Write-Set:'
require_contains "template/.agent/verification-gate.md" '^Sensitive Domains:'
require_contains "template/.agent/verification-gate.md" '^Stage 3 Mode:'
require_contains "template/.agent/verification-gate.md" 'SKIPPED.*inline.*READY'
require_contains "template/.claude/agents/verifier.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "template/.claude/agents/gpt-verifier.md" 'DEGRADED'
require_contains "template/.claude/hooks/verification-gate.sh" 'SKIPPED verifier dispatch still requires an inline READY verdict'
require_contains "skills/verifier/SKILL.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "skills/merge-protocol/SKILL.md" 'authoritative verifier verdict is `READY`'
require_contains "template/memory_bank/review-log.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "template/docs/templates/closeout-report-template.md" 'REPORTING_ONLY'
require_contains "template/AGENTS.md" 'first-WB-in-domain OR auth/payments/DB-schema/middleware'
require_contains "template/AGENTS.md" 'Claude verifier BLOCKED/UNVERIFIED'
require_contains "template/AGENTS.md" 'budget is exceeded, log the overage; it does not disable a required GPT'
require_contains "template/AGENTS.md" 'only valid degraded condition; cost or budget does not qualify'
require_contains "template/AGENTS.md" 'review-degraded:codex-mcp-unavailable'
require_contains "template/CLAUDE.md" 'non-`READY` verifier verdict'
require_contains "template/CLAUDE.md" 'review-degraded:codex-mcp-unavailable'

CONSUMERS=(
  "template/.agent/workflows/sdd-protocol.md"
  "template/AGENTS.md"
  "template/CLAUDE.md"
  "framework/workflow/verification-tiers.md"
  "framework/workflow/agentic-sdlc-overview.md"
  "template/docs/templates/work-block-template.md"
  "template/docs/templates/tasklist-template.md"
  "template/docs/templates/consolidation-report-template.md"
  "template/.agent/verification-gate.md"
  "template/.claude/hooks/verification-gate.sh"
  "template/.claude/agents/gpt-verifier.md"
  "template/.claude/agents/verifier.md"
  "skills/verifier/SKILL.md"
  "skills/codex-verification/SKILL.md"
  "skills/context-snapshot/SKILL.md"
  "skills/merge-protocol/SKILL.md"
  "template/docs/templates/verification-report-template.md"
  "template/docs/templates/closeout-report-template.md"
)

STALE="$(grep -nE '(<|<=|at most|maximum of|up to|[^0-9])3 (planned )?(implementation )?files|READY[[:space:]]*/[[:space:]]*BLOCKED[[:space:]]*$|\"enum\"[[:space:]]*:[[:space:]]*\[\"READY\",[[:space:]]*\"BLOCKED\"\]' "${CONSUMERS[@]/#/$ROOT/}" || true)"
if [ -n "$STALE" ]; then
  echo "$STALE" >&2
  fail "stale SDD contract wording found"
fi

echo "OK: SDD protocol and direct consumers satisfy the contract checks"
