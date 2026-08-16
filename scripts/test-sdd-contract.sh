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
for impact in logic route schema api security runtime integration architecture evaluation governance; do
  assert_quick_fix no 1 "$impact"
done

for path in \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/evaluation.md" \
  "governance/define-quality.md" \
  "governance/runtime-capabilities.md" \
  "integrations/README.md" \
  "bootstrap/profiles.json" \
  "bootstrap/bootstrap_project.py" \
  "docs/bootstrap-profiles.md" \
  "docs/plans/wb-007-agent-evaluation-trajectory-assurance.md" \
  "scripts/test-bootstrap-profiles.py" \
  "scripts/test-profile-restore.py" \
  "scripts/test-runtime-conformance.py" \
  "scripts/test-evaluation-contracts.py" \
  "template/AGENTS.md" \
  "template/CLAUDE.md" \
  "template/.agent/ROSTER.md" \
  "template/.agent/active-work-block.json" \
  "template/.agent/active-work-block.default.json" \
  "template/.agent/hooks/hard_stop_policy.py" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/.claude/hooks/work_block_gate.py" \
  "template/.claude/hooks/assurance_gate.py" \
  "template/docs/architecture/README.md" \
  "template/docs/templates/work-block-template.md" \
  "template/docs/templates/spec-drift-report-template.md" \
  "template/docs/templates/integration-admission-template.md" \
  "template/docs/templates/evaluation-plan-template.json" \
  "template/docs/templates/evaluation-report-template.json" \
  "template/docs/templates/trajectory-event-template.json" \
  "template/docs/templates/repair-record-template.md" \
  "template/docs/templates/combined-assurance-report-template.md" \
  "template/scripts/validate-installation-profile.py" \
  "template/scripts/repair-lifecycle.py" \
  "template/scripts/validate-evaluation.py" \
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
require_contains "template/.agent/workflows/sdd-protocol.md" '2C.*Agent Evaluation'
require_contains "template/.agent/workflows/sdd-protocol.md" '2D.*Specification Drift Audit'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Review gate:.*CHANGES_REQUIRED'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Verification verdict:.*READY.*BLOCKED.*UNVERIFIED'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Evaluation verdict:.*READY.*BLOCKED.*UNVERIFIED'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Drift gate:.*READY.*BLOCKED.*UNVERIFIED'
require_contains "template/.agent/workflows/sdd-protocol.md" 'observable events only'
require_contains "template/.agent/workflows/sdd-protocol.md" 'private chain-of-thought'

# Framework self-hosting workflow must preserve normal reversible Git authority.
require_file ".agent/workflows/sdd-protocol.md"
require_contains ".agent/workflows/sdd-protocol.md" 'approved Work Block/write-set, including staging, local commits, and normal'
require_absent_pattern ".agent/workflows/sdd-protocol.md" 'staging, commit, or push'

# Define-quality is one evidence prerequisite before Critic/Write Gate.
require_contains "governance/define-quality.md" 'Executable Define-Quality Prerequisite'
require_contains "governance/define-quality.md" '"define_quality"'
require_contains "governance/define-quality.md" 'Managed / Assured / Distributed.*required'
require_contains "governance/define-quality.md" 'required=false.*configuration contradiction'
require_contains "governance/define-quality.md" 'schema-v3'
require_contains "governance/define-quality.md" 'runtime-neutral'
require_contains "governance/define-quality.md" 'Only `type=requirement` tasks count as'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Define-quality prerequisite:'
require_contains "template/.agent/workflows/sdd-protocol.md" 'aggregate Define-quality prerequisite when applicable'
require_contains "template/.agent/workflows/sdd-protocol.md" 'required=false.*cannot disable'
require_contains "template/.agent/workflows/sdd-protocol.md" 'non-blank requirements-review'
assert_before "template/.agent/workflows/sdd-protocol.md" 'Resolve the aggregate Define-quality prerequisite' 'Run Critic function'
require_contains "template/.agent/active-work-block.json" '"define_quality"'
require_contains "template/.agent/active-work-block.json" '"requirements_review"'
require_contains "template/.agent/active-work-block.json" '"traceability"'
require_contains "template/.agent/active-work-block.json" '"consistency_analysis"'
require_contains "template/.agent/active-work-block.default.json" '"define_quality"'
require_contains "template/.codex/hooks/pre_tool_use_policy.py" 'validate_define_quality'
require_contains "template/.claude/hooks/work_block_gate.py" 'validate_define_quality'
require_contains "template/scripts/validate-installation-profile.py" 'EXPECTED_DEFAULT_DEFINE_QUALITY'

# Work Block binds governance separately from runtime/model/isolation/integration.
require_contains "template/docs/templates/work-block-template.md" 'Governance Profile:'
require_contains "template/docs/templates/work-block-template.md" 'Define Quality Prerequisite'
require_contains "template/docs/templates/work-block-template.md" 'Requirements Review Evidence:'
require_contains "template/docs/templates/work-block-template.md" 'Traceability Evidence:'
require_contains "template/docs/templates/work-block-template.md" 'Consistency Analysis Evidence:'
require_contains "template/docs/templates/work-block-template.md" 'Approved Specification:'
require_contains "template/docs/templates/work-block-template.md" 'Approved Evaluation Plan:'
require_contains "template/docs/templates/work-block-template.md" 'Runtime Capability Snapshot'
require_contains "template/docs/templates/work-block-template.md" 'Integration Profile and Admission'
require_contains "template/docs/templates/work-block-template.md" 'Approved Integration IDs:'
require_contains "template/docs/templates/work-block-template.md" 'Admission Records:'
require_contains "template/docs/templates/work-block-template.md" 'Data Sent Externally:'
require_contains "template/docs/templates/work-block-template.md" 'Integration Smoke Evidence:'
require_contains "template/docs/templates/work-block-template.md" 'Function Bindings'
require_contains "template/docs/templates/work-block-template.md" 'Review Gate:'
require_contains "template/docs/templates/work-block-template.md" 'Verification Verdict:'
require_contains "template/docs/templates/work-block-template.md" 'Evaluation Verdict:'
require_contains "template/docs/templates/work-block-template.md" 'Agent Evaluation'
require_contains "template/docs/templates/work-block-template.md" 'Trajectory Requirements:'
require_contains "template/docs/templates/work-block-template.md" 'No Hidden Reasoning:'
require_contains "template/docs/templates/work-block-template.md" 'Drift Gate:'
require_contains "template/docs/templates/work-block-template.md" 'Specification Drift Audit'
require_contains "template/docs/templates/work-block-template.md" 'Navigation and Documentation Impact'
require_contains "template/docs/templates/work-block-template.md" 'Commit / Publication Scope'
require_contains "template/docs/templates/work-block-template.md" 'Execution Log'
require_contains "template/docs/templates/work-block-template.md" 'Specification and SSOT Sync'
require_contains "template/docs/templates/work-block-template.md" 'Knowledge and Retrospective'
require_contains "template/docs/templates/integration-admission-template.md" 'Logical functions served:'
require_contains "template/docs/templates/integration-admission-template.md" 'Data Boundary'
require_contains "template/docs/templates/integration-admission-template.md" 'Secret and Authentication Boundary'

# Specification and architecture outrank implementation/evaluation plans and tasklists.
assert_before "template/AGENTS.md" 'approved specification' 'approved implementation and evaluation plans'
assert_before "template/.agent/workflows/sdd-protocol.md" 'approved specification' 'approved implementation and evaluation plans'
assert_before "template/docs/templates/work-block-template.md" 'Approved Specification:' 'Derived Implementation Plan:'

# Portable project facts must remain explicit when bootstrap cannot know them.
require_contains "template/AGENTS.md" 'Primary source roots: `to be defined`'
require_absent_pattern "template/AGENTS.md" 'Primary source roots: `src[/][*], app[/][*]`'
require_contains "bootstrap/bootstrap_project.py" 'SOURCE_DIRS.*to be defined'

# Stable logical roles live in canonical authority; portable AGENTS routes to it.
require_contains "template/AGENTS.md" 'Role authority is defined by `governance/authority.md`'
require_contains "template/AGENTS.md" 'Operational routing is in'
require_contains "template/AGENTS.md" 'routine internal lifecycle transitions without repeated Owner approval'
for role in Owner Orchestrator Architect Critic Coder Reviewer Verifier; do
  require_contains "governance/authority.md" "^[|] $role [|]"
done
require_contains "template/.agent/ROSTER.md" 'Runtime-specific agent names, models, plugins'
require_contains "template/.agent/ROSTER.md" 'spec-drift-audit'
require_absent_pattern "template/AGENTS.md" 'GPT Critic|GPT Verifier|Codex Reviewer|mega-orchestrator'
require_absent_pattern "template/.agent/ROSTER.md" '^\| GPT Critic|^\| GPT Verifier|^\| Codex Reviewer'
require_absent_pattern "template/.agent/workflows/sdd-protocol.md" 'Claude critic|GPT critic|Claude verifier|GPT verifier'
require_absent_pattern "template/CLAUDE.md" 'gpt-critic|gpt-verifier|codex-reviewer|Claude agents remain the authoritative'
[ "$(awk 'NF { print; exit }' "$ROOT/template/CLAUDE.md")" = "@AGENTS.md" ] || \
  fail "template/CLAUDE.md first instruction must be @AGENTS.md"

# Portable review, verification, evaluation, and drift schemas use one vocabulary.
require_contains "governance/artifacts.md" 'verdict: `READY \| CHANGES_REQUIRED \| BLOCKED \| UNVERIFIED`'
require_contains "governance/artifacts.md" '`SKIPPED` is a review-gate state'
require_contains "governance/artifacts.md" 'Evaluation Report'
require_contains "governance/artifacts.md" 'verdict: `READY \| BLOCKED \| UNVERIFIED`'
for value in MISSING_IMPLEMENTATION UNSPECIFIED_IMPLEMENTATION STALE_PLAN STALE_TEST STALE_DOCUMENTATION SPEC_CHANGE_REQUIRED INSPECTION_GAP ALIGNMENT_REQUIRED; do
  require_contains "governance/artifacts.md" "\`$value\`"
done
require_absent_pattern "governance/artifacts.md" 'verdict: `APPROVE \| CHANGES_REQUIRED'
require_absent_pattern "governance/artifacts.md" '`documented_change`|`implementation_drift`|`documentation_drift`'

# Evaluation contract: observable events only, deterministic evidence cannot be judge-only.
require_contains "governance/evaluation.md" 'Deterministic Tests'
require_contains "governance/evaluation.md" 'Output Evaluation'
require_contains "governance/evaluation.md" 'Observable Trajectory Evaluation'
require_contains "governance/evaluation.md" 'must not require or claim access to private chain-of-thought'
require_contains "governance/evaluation.md" 'cannot by itself:'
require_contains "governance/evaluation.md" 'prove deterministic correctness'
require_contains "governance/evaluation.md" 'open a write, integration, deployment, or Hard Stop gate'
for verdict in READY BLOCKED UNVERIFIED; do
  require_contains "governance/evaluation.md" "\`$verdict\`"
done
require_contains "template/scripts/validate-evaluation.py" 'reject_hidden_reasoning'
require_contains "template/scripts/validate-evaluation.py" 'all_blocking_pass'
require_contains "template/scripts/validate-evaluation.py" 'success-closeout requires required evaluation'

# Portable drift contract.
require_contains "skills/spec-drift-audit/SKILL.md" 'Reviewer checks the quality'
require_contains "skills/spec-drift-audit/SKILL.md" 'Verifier checks observable behavior'
require_contains "skills/spec-drift-audit/SKILL.md" 'Drift Auditor checks agreement'
for value in ALIGNED ALIGNMENT_REQUIRED BLOCKED UNVERIFIED; do
  require_contains "skills/spec-drift-audit/SKILL.md" "\`$value\`"
done
require_contains "template/docs/templates/spec-drift-report-template.md" 'Alignment Matrix'
require_contains "skills/catalog.yml" 'spec-drift-audit'

# Installation composition is manifest-driven and independent from authority.
require_contains "bootstrap.sh" 'bootstrap/bootstrap_project.py'
require_contains "bootstrap/bootstrap_project.py" 'bootstrap/profiles.json'
require_contains "bootstrap/bootstrap_project.py" 'validate_catalog'
require_contains "bootstrap/bootstrap_project.py" '.agent/bootstrap-profile.json'
require_contains "bootstrap/bootstrap_project.py" 'Installation composition does not grant Work Block authority'
require_contains "bootstrap/profiles.json" '"default_profile": "multi-runtime"'
for profile in core codex claude-code opencode multi-runtime; do
  require_contains "bootstrap/profiles.json" "\"$profile\""
done
require_contains "bootstrap/profiles.json" '"minimal": "core"'
require_contains "bootstrap/profiles.json" '"full": "multi-runtime"'
require_contains "bootstrap/profiles.json" 'governance/evaluation.md'
require_contains "bootstrap/profiles.json" 'docs/architecture/README.md'
require_contains "bootstrap/profiles.json" 'scripts/validate-evaluation.py'
require_contains "template/scripts/bootstrap.sh" 'validate-installation-profile.py'
require_contains "template/scripts/bootstrap.sh" 'INSTALLATION_PROFILE'
require_contains "template/scripts/validate-installation-profile.py" 'required_paths'
require_contains "template/scripts/validate-installation-profile.py" 'forbidden_paths'
require_contains "template/scripts/validate-installation-profile.py" 'EXPECTED_DEFAULT_EVALUATION'
require_contains "template/scripts/validate-installation-profile.py" 'EXPECTED_DEFAULT_DEFINE_QUALITY'
require_contains "docs/bootstrap-profiles.md" 'Installation profiles control'
require_contains "docs/bootstrap-profiles.md" 'does not grant'

# Machine-readable gate is provider-neutral and exposes integration/assurance state.
require_contains "template/.agent/active-work-block.json" '"integrations"'
require_contains "template/.agent/active-work-block.json" '"approved"'
require_contains "template/.agent/active-work-block.json" '"admission_records"'
require_contains "template/.agent/active-work-block.json" '"assurance"'
require_contains "template/.agent/active-work-block.json" '"review"'
require_contains "template/.agent/active-work-block.json" '"verification"'
require_contains "template/.agent/active-work-block.json" '"evaluation"'
require_contains "template/.agent/active-work-block.json" '"rubric_revision"'
require_contains "template/.agent/active-work-block.json" '"benchmark_revision"'
require_contains "template/.agent/active-work-block.json" '"drift"'
require_contains "template/.agent/critic-gate.md" 'active-work-block.json'
require_contains "template/.agent/verification-gate.md" 'Review:.*PENDING'
require_contains "template/.agent/verification-gate.md" 'Verification:.*PENDING'
require_contains "template/.agent/verification-gate.md" 'Evaluation:.*PENDING'
require_contains "template/.agent/verification-gate.md" 'Drift:.*PENDING'

# Reviewer/verifier direct consumers retain portable verdicts.
require_contains "template/.claude/agents/verifier.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "skills/verifier/SKILL.md" 'READY.*BLOCKED.*UNVERIFIED'
require_contains "template/docs/templates/closeout-report-template.md" 'REPORTING_ONLY'
require_contains "governance/lifecycle.md" 'Narrow Deterministic Repair'
require_contains "governance/lifecycle.md" 'NDR is a mechanically constrained submode of `Controlled`'
require_contains "governance/lifecycle.md" 'at most three sequentially discovered eligible NDR items'
require_contains "governance/artifacts.md" 'dynamic Git or CI counters'
require_contains "template/AGENTS.md" 'Use `.agent/workflows/sdd-protocol.md` for the detailed lifecycle'
require_contains "template/.agent/workflows/sdd-protocol.md" 'one independent'
require_contains "template/docs/templates/repair-record-template.md" 'machine-readable'
require_contains "template/docs/templates/combined-assurance-report-template.md" 'Assurance isolation'
require_contains "bootstrap/profiles.json" 'scripts/repair-lifecycle.py'

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

echo "OK: runtime-neutral SDLC protocol and evaluation-aware direct consumers satisfy the contract checks"
