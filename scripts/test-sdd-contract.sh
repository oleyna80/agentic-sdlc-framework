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
for impact in logic route schema api security runtime architecture governance; do
  assert_quick_fix no 1 "$impact"
done

for path in \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/runtime-capabilities.md" \
  "template/AGENTS.md" \
  "template/.agent/ROSTER.md" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/docs/templates/work-block-template.md" \
  "template/docs/templates/spec-drift-report-template.md" \
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

# Work Block binds governance separately from runtime/model/isolation.
require_contains "template/docs/templates/work-block-template.md" 'Governance Profile:'
require_contains "template/docs/templates/work-block-template.md" 'Approved Specification:'
require_contains "template/docs/templates/work-block-template.md" 'Runtime Capability Snapshot'
require_contains "template/docs/templates/work-block-template.md" 'Function Bindings'
require_contains "template/docs/templates/work-block-template.md" 'Review Gate:'
require_contains "template/docs/templates/work-block-template.md" 'Verification Verdict:'
require_contains "template/docs/templates/work-block-template.md" 'Drift Gate:'
require_contains "template/docs/templates/work-block-template.md" 'Specification Drift Audit'

# Specification and architecture outrank implementation plans/tasklists.
assert_before "template/AGENTS.md" 'approved specification' 'approved implementation plan'
assert_before "template/.agent/workflows/sdd-protocol.md" 'approved specification' 'approved implementation plan'
assert_before "template/docs/templates/work-block-template.md" 'Approved Specification:' 'Derived Implementation Plan:'

# Stable logical roles; provider/model names are integration details only.
for role in Owner Orchestrator Architect Critic Coder Reviewer Verifier; do
  require_contains "template/AGENTS.md" "[|] $role [|]"
done
require_contains "template/.agent/ROSTER.md" 'Runtime-specific agent names, models, plugins'
require_contains "template/.agent/ROSTER.md" 'spec-drift-audit'
require_absent_pattern "template/AGENTS.md" 'GPT Critic|GPT Verifier|Codex Reviewer|mega-orchestrator'
require_absent_pattern "template/.agent/ROSTER.md" '^\| GPT Critic|^\| GPT Verifier|^\| Codex Reviewer'
require_absent_pattern "template/.agent/workflows/sdd-protocol.md" 'Claude critic|GPT critic|Claude verifier|GPT verifier'

# Portable drift contract.
require_contains "skills/spec-drift-audit/SKILL.md" 'Reviewer checks the quality'
require_contains "skills/spec-drift-audit/SKILL.md" 'Verifier checks observable behavior'
require_contains "skills/spec-drift-audit/SKILL.md" 'Drift Auditor checks agreement'
require_contains "skills/spec-drift-audit/SKILL.md" '`ALIGNED`'
require_contains "skills/spec-drift-audit/SKILL.md" '`ALIGNMENT_REQUIRED`'
require_contains "skills/spec-drift-audit/SKILL.md" '`BLOCKED`'
require_contains "skills/spec-drift-audit/SKILL.md" '`UNVERIFIED`'
require_contains "template/docs/templates/spec-drift-report-template.md" 'Alignment Matrix'
require_contains "skills/catalog.yml" 'spec-drift-audit'

# Bootstrap delivers the same portable contracts to generated projects.
require_contains "bootstrap.sh" 'cp -r.*governance.*TARGET_DIR/governance'
require_contains "bootstrap.sh" 'cp -r.*runtimes.*TARGET_DIR/runtimes'
require_contains "bootstrap.sh" 'CORE_SKILLS=.*spec-drift-audit'
require_contains "template/scripts/bootstrap.sh" 'governance/authority.md'
require_contains "template/scripts/bootstrap.sh" 'runtimes/generic/README.md'
require_contains "template/scripts/bootstrap.sh" 'spec-drift-audit/SKILL.md'

# Existing runtime enforcement remains a compatibility adapter.
require_contains "template/.agent/critic-gate.md" '^Approved Write-Set:'
require_contains "template/.agent/verification-gate.md" '^Required Verifier Isolation:'
require_contains "template/.agent/verification-gate.md" '^Verifier Isolation:'
require_contains "template/.claude/agents/verifier.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "skills/verifier/SKILL.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "template/docs/templates/closeout-report-template.md" 'REPORTING_ONLY'

# Reject old collapsed or provider-authoritative terminology in portable core.
for path in \
  "template/AGENTS.md" \
  "template/.agent/ROSTER.md" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/docs/templates/work-block-template.md" \
  "docs/profiles.md"; do
  require_absent_pattern "$path" 'Plan & Discover|Stage 2: Verify|Codex mega-orchestrator'
done

echo "OK: runtime-neutral SDLC protocol and direct consumers satisfy the contract checks"
