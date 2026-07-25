#!/usr/bin/env bash
# Detect drift between the runtime-neutral SDLC protocol and direct consumers.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

require_file() {
  local path="$1"
  [ -f "$ROOT/$path" ] || fail "missing $path"
}

require_contains() {
  local path="$1"
  local pattern="$2"
  grep -Eq -- "$pattern" "$ROOT/$path" || fail "$path missing contract pattern: $pattern"
}

require_absent_pattern() {
  local path="$1"
  local pattern="$2"
  if grep -Eq -- "$pattern" "$ROOT/$path"; then
    fail "$path contains forbidden/stale core pattern: $pattern"
  fi
}

assert_before() {
  local path="$1"
  local first_pattern="$2"
  local second_pattern="$3"
  local first_line second_line
  first_line="$(grep -nEm1 -- "$first_pattern" "$ROOT/$path" | cut -d: -f1 || true)"
  second_line="$(grep -nEm1 -- "$second_pattern" "$ROOT/$path" | cut -d: -f1 || true)"
  [ -n "$first_line" ] || fail "$path missing first ordering pattern: $first_pattern"
  [ -n "$second_line" ] || fail "$path missing second ordering pattern: $second_pattern"
  [ "$first_line" -lt "$second_line" ] || fail "$path must place '$first_pattern' before '$second_pattern'"
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
for impact in logic route schema api security runtime integration architecture governance; do
  assert_quick_fix no 1 "$impact"
done

for path in \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/runtime-capabilities.md" \
  "integrations/README.md" \
  "template/AGENTS.md" \
  "template/CLAUDE.md" \
  "template/.agent/ROSTER.md" \
  "template/.agent/active-work-block.json" \
  "template/.agent/hooks/hard_stop_policy.py" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/.claude/hooks/work_block_gate.py" \
  "template/.claude/hooks/assurance_gate.py" \
  "template/docs/templates/work-block-template.md" \
  "template/docs/templates/spec-drift-report-template.md" \
  "template/docs/templates/integration-admission-template.md" \
  "skills/spec-drift-audit/SKILL.md"; do
  require_file "$path"
done

# Canonical lifecycle and independent assurance functions.
require_contains "template/.agent/workflows/sdd-protocol.md" 'Stage 0.*Define'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Stage 1.*Execute'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Stage 2.*Assure'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Stage 3.*Close'
require_contains "template/.agent/workflows/sdd-protocol.md" '2A.*Independent Review'
require_contains "template/.agent/workflows/sdd-protocol.md" '2B.*Technical Verification'
require_contains "template/.agent/workflows/sdd-protocol.md" '2C.*Specification Drift Audit'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Review gate:.*CHANGES_REQUIRED'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Verification verdict:.*READY.*BLOCKED.*UNVERIFIED'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Drift gate:.*READY.*BLOCKED.*UNVERIFIED'

# Work Block binds governance separately from runtime/model/isolation/integration.
require_contains "template/docs/templates/work-block-template.md" 'Governance Profile:'
require_contains "template/docs/templates/work-block-template.md" 'Approved Specification:'
require_contains "template/docs/templates/work-block-template.md" 'Runtime Capability Snapshot'
require_contains "template/docs/templates/work-block-template.md" 'Integration Profile and Admission'
require_contains "template/docs/templates/work-block-template.md" 'Approved Integration IDs:'
require_contains "template/docs/templates/work-block-template.md" 'Admission Records:'
require_contains "template/docs/templates/work-block-template.md" 'Data Sent Externally:'
require_contains "template/docs/templates/work-block-template.md" 'Integration Smoke Evidence:'
require_contains "template/docs/templates/work-block-template.md" 'Function Bindings'
require_contains "template/docs/templates/work-block-template.md" 'Review Gate:'
require_contains "template/docs/templates/work-block-template.md" 'Verification Verdict:'
require_contains "template/docs/templates/work-block-template.md" 'Drift Gate:'
require_contains "template/docs/templates/work-block-template.md" 'Specification Drift Audit'
require_contains "template/docs/templates/integration-admission-template.md" 'Logical functions served:'
require_contains "template/docs/templates/integration-admission-template.md" 'Data Boundary'
require_contains "template/docs/templates/integration-admission-template.md" 'Secret and Authentication Boundary'

# Specification and architecture outrank implementation plans/tasklists.
assert_before "template/AGENTS.md" 'approved specification' 'approved implementation plan'
assert_before "template/.agent/workflows/sdd-protocol.md" 'approved specification' 'approved implementation plan'
assert_before "template/docs/templates/work-block-template.md" 'Approved Specification:' 'Derived Implementation Plan:'

# Stable logical roles; provider/model/integration names remain implementation details.
for role in Owner Orchestrator Architect Critic Coder Reviewer Verifier; do
  require_contains "template/AGENTS.md" "[|] $role [|]"
done
require_contains "template/.agent/ROSTER.md" 'Runtime-specific agent names, models, plugins'
require_contains "template/.agent/ROSTER.md" 'spec-drift-audit'
require_absent_pattern "template/AGENTS.md" 'GPT Critic|GPT Verifier|Codex Reviewer|mega-orchestrator'
require_absent_pattern "template/.agent/ROSTER.md" '^\| GPT Critic|^\| GPT Verifier|^\| Codex Reviewer'
require_absent_pattern "template/.agent/workflows/sdd-protocol.md" 'Claude critic|GPT critic|Claude verifier|GPT verifier'
require_absent_pattern "template/CLAUDE.md" 'gpt-critic|gpt-verifier|codex-reviewer|Claude agents remain the authoritative'

# Portable review, verification, and drift schemas use one vocabulary.
require_contains "governance/artifacts.md" 'verdict: `READY \| CHANGES_REQUIRED \| BLOCKED \| UNVERIFIED`'
require_contains "governance/artifacts.md" '`SKIPPED` is a review-gate state'
for value in MISSING_IMPLEMENTATION UNSPECIFIED_IMPLEMENTATION STALE_PLAN STALE_TEST STALE_DOCUMENTATION SPEC_CHANGE_REQUIRED INSPECTION_GAP ALIGNMENT_REQUIRED; do
  require_contains "governance/artifacts.md" "\`$value\`"
done
require_absent_pattern "governance/artifacts.md" 'verdict: `APPROVE \| CHANGES_REQUIRED'
require_absent_pattern "governance/artifacts.md" '`documented_change`|`implementation_drift`|`documentation_drift`'

# Portable drift contract.
require_contains "skills/spec-drift-audit/SKILL.md" 'Reviewer checks the quality'
require_contains "skills/spec-drift-audit/SKILL.md" 'Verifier checks observable behavior'
require_contains "skills/spec-drift-audit/SKILL.md" 'Drift Auditor checks agreement'
for value in ALIGNED ALIGNMENT_REQUIRED BLOCKED UNVERIFIED; do
  require_contains "skills/spec-drift-audit/SKILL.md" "\`$value\`"
done
require_contains "template/docs/templates/spec-drift-report-template.md" 'Alignment Matrix'
require_contains "skills/catalog.yml" 'spec-drift-audit'

# Bootstrap delivers governance, runtimes, integrations, and complete gate bundles.
require_contains "bootstrap.sh" 'cp -r.*governance.*TARGET_DIR/governance'
require_contains "bootstrap.sh" 'cp -r.*runtimes.*TARGET_DIR/runtimes'
require_contains "bootstrap.sh" 'cp -r.*integrations.*TARGET_DIR/integrations'
require_contains "bootstrap.sh" 'CORE_SKILLS=.*spec-drift-audit'
for pattern in \
  'governance/authority.md' \
  'runtimes/generic/README.md' \
  'integrations/README.md' \
  'spec-drift-audit/SKILL.md' \
  '.agent/hooks/hard_stop_policy.py' \
  '.claude/hooks/work_block_gate.py' \
  '.claude/hooks/assurance_gate.py' \
  'opencode.json' \
  '.opencode/agents/verifier.md'; do
  require_contains "template/scripts/bootstrap.sh" "$pattern"
done

# Machine-readable gate is provider-neutral and exposes integration/assurance state.
require_contains "template/.agent/active-work-block.json" '"integrations"'
require_contains "template/.agent/active-work-block.json" '"approved"'
require_contains "template/.agent/active-work-block.json" '"admission_records"'
require_contains "template/.agent/active-work-block.json" '"assurance"'
require_contains "template/.agent/active-work-block.json" '"review"'
require_contains "template/.agent/active-work-block.json" '"verification"'
require_contains "template/.agent/active-work-block.json" '"drift"'
require_contains "template/.agent/critic-gate.md" 'active-work-block.json'
require_contains "template/.agent/verification-gate.md" 'Review:.*PENDING'
require_contains "template/.agent/verification-gate.md" 'Verification:.*PENDING'
require_contains "template/.agent/verification-gate.md" 'Drift:.*PENDING'

# Reviewer/verifier direct consumers retain portable verdicts.
require_contains "template/.claude/agents/verifier.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "skills/verifier/SKILL.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "template/docs/templates/closeout-report-template.md" 'REPORTING_ONLY'

# Reject old collapsed or provider-authoritative terminology in portable core.
for path in \
  "template/AGENTS.md" \
  "template/CLAUDE.md" \
  "template/.agent/ROSTER.md" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/docs/templates/work-block-template.md" \
  "docs/profiles.md"; do
  require_absent_pattern "$path" 'Plan & Discover|Stage 2: Verify|Codex mega-orchestrator'
done

echo "OK: runtime-neutral SDLC protocol and direct consumers satisfy the contract checks"
