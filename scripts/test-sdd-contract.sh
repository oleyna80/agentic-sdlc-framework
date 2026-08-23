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

mandatory_provider_semantics_present() {
  local path="$1"
  local target="$path"
  if [[ "$target" != /* ]]; then
    target="$ROOT/$target"
  fi

  awk '
    # Inspect one normalized prose statement. The predicate deliberately uses
    # independent concepts instead of word-order regexes: provider review,
    # provider prerequisite, and verification prerequisite mandates are all
    # forbidden whichever order ordinary prose uses.
    function forbidden_statement(statement,    line, modal, provider, assurance, prerequisite, imperative_prerequisite, imperative_provider_assurance, negated, provider_mandate, prerequisite_mandate) {
      line = tolower(statement)
      gsub(/[[:space:]]+/, " ", line)

      # A negative statement must not be mistaken for a mandate. Statements
      # are inspected separately so one negative sentence cannot exempt a
      # later positive mandate in the same prose unit.
      negated = (line ~ /(does not|do not|cannot|can not|never)[[:space:]]+(require|requires|need|needs|install|installation|authenticate|authentication|configure|configuration|ask|request|issue|replace|grant|create|treat|claim|substitute)/ ||
        line ~ /(is|are|be)[[:space:]]+not[[:space:]]+(mandatory|required|needed)/ ||
        line ~ /not[[:space:]]+(mandatory|required|needed)/ ||
        line ~ /no[[:space:]]+(provider|codex|additional[[:space:]-]model|second[[:space:]-]model).*(review|verification|execution|installation|install|authentication|authenticate|auth|configuration|configure|mcp|transport|prerequisite)/)
      if (negated) {
        return 0
      }

      modal = (line ~ /(^|[^[:alpha:]])(must|mandatory|required|requires|require|needs|need)([^[:alpha:]]|$)/ ||
        line ~ /depends[[:space:]]+on/)
      provider = line ~ /(provider|codex|additional[[:space:]-]model|second[[:space:]-]model)/
      assurance = line ~ /(review|verification|execution)/
      prerequisite = line ~ /(installation|install|authentication|authenticate|auth|configuration|configure|mcp|transport|prerequisite)/
      # Direct imperative prerequisites are mandates even without a separate
      # modal word. Common polite and purpose-clause introductions do not
      # change that imperative meaning.
      imperative_prerequisite = (line ~ /^[[:space:]]*((please|kindly)[[:space:]]+)?(install|authenticate|configure)([^[:alpha:]]|$)/ || line ~ /^[[:space:]]*to[[:space:]]+(verify|review|execute|perform[[:space:]]+verification)[^,]*,[[:space:]]*((please|kindly)[[:space:]]+)?(install|authenticate|configure)([^[:alpha:]]|$)/ || line ~ /^[[:space:]]*before[[:space:]]+(verification|review|execution)[^,]*,[[:space:]]*((please|kindly)[[:space:]]+)?(install|authenticate|configure)([^[:alpha:]]|$)/)

      # Direct provider-assurance imperatives are mandates even without modal
      # wording. This remains intentionally narrow: only the approved purpose,
      # courtesy, verb, provider alias, and assurance-action forms match.
      imperative_provider_assurance = (line ~ /^[[:space:]]*(to[[:space:]]+verify,[[:space:]]+)?((please|kindly)[[:space:]]+)?(ask|request)[[:space:]]+((a|an)[[:space:]]+)?(provider|codex|additional[[:space:]-]model|second[[:space:]-]model)[[:space:]]+to[[:space:]]+(review|verify|perform[[:space:]]+verification)([^[:alpha:]]|$)/)

      provider_mandate = provider && assurance && modal
      prerequisite_mandate = prerequisite && (modal || imperative_prerequisite) && (assurance || provider)
      return provider_mandate || prerequisite_mandate || imperative_provider_assurance
    }

    # Inspect contrast clauses independently: a negated first clause must not
    # suppress a positive mandate following ordinary ", but" or ", however"
    # prose. This deliberately does not turn the guard into a general parser.
    function inspect_contrast_clauses(statement,    remainder, clause) {
      remainder = statement
      while (match(remainder, /,[[:space:]]*(but|however)([[:space:],]|$)/)) {
        clause = substr(remainder, 1, RSTART - 1)
        if (forbidden_statement(clause)) {
          return 1
        }
        remainder = substr(remainder, RSTART + RLENGTH)
      }
      return forbidden_statement(remainder)
    }

    # Units are prose paragraphs or one complete list item. Split their
    # normalized text into sentences and semicolon-delimited clauses, then
    # ordinary contrast clauses, so unrelated claims do not combine and a
    # negative clause cannot exempt a later positive mandate while line
    # wrapping remains visible.
    function inspect(unit,    text, remainder, end, statement) {
      text = unit
      gsub(/[[:space:]]+/, " ", text)
      remainder = text
      while (match(remainder, /[.!?]+|;/)) {
        end = RSTART + RLENGTH - 1
        statement = substr(remainder, 1, end)
        if (inspect_contrast_clauses(statement)) {
          return 1
        }
        remainder = substr(remainder, end + 1)
      }
      return inspect_contrast_clauses(remainder)
    }

    function flush_unit() {
      if (unit != "" && inspect(unit)) {
        found = 1
      }
      unit = ""
      in_list_item = 0
    }

    function is_list_item(line) {
      return line ~ /^[[:space:]]*([-*+][[:space:]]+|[0-9]+[.)][[:space:]]+)/
    }

    # Return the leading fence run after at most three literal spaces, while
    # retaining its delimiter character and run length for a later compatible
    # close check. An opener may have an information-string tail; a closer may
    # have whitespace only after its run.
    function fence_run(line,    trimmed, char, run_length) {
      trimmed = line
      sub(/^ {0,3}/, "", trimmed)
      char = substr(trimmed, 1, 1)
      if (char != "`" && char != "~") {
        return 0
      }
      run_length = 0
      while (substr(trimmed, run_length + 1, 1) == char) {
        run_length++
      }
      if (run_length < 3) {
        return 0
      }
      fence_character = char
      fence_length = run_length
      fence_tail = substr(trimmed, run_length + 1)
      return 1
    }

    {
      line = $0

      if (!in_fence && fence_run(line)) {
        flush_unit()
        open_fence_character = fence_character
        open_fence_length = fence_length
        in_fence = 1
        next
      }
      if (in_fence) {
        if (fence_run(line) && fence_character == open_fence_character && fence_length >= open_fence_length && fence_tail ~ /^[[:space:]]*$/) {
          in_fence = 0
        }
        next
      }
      if (line ~ /^[[:space:]]*$/) {
        flush_unit()
        next
      }
      if (line ~ /^[[:space:]]{0,3}#{1,6}([[:space:]]|$)/) {
        flush_unit()
        next
      }
      if (is_list_item(line)) {
        flush_unit()
        sub(/^[[:space:]]*([-*+][[:space:]]+|[0-9]+[.)][[:space:]]+)/, "", line)
        unit = line
        in_list_item = 1
        next
      }
      if (unit == "") {
        unit = line
      } else {
        unit = unit " " line
      }
    }
    END {
      flush_unit()
      exit(found ? 0 : 1)
    }
  ' "$target"
}

require_absent_mandatory_provider_semantics() {
  local path="$1"
  if mandatory_provider_semantics_present "$path"; then
    fail "$path contains mandatory provider-review or provider-prerequisite semantics"
  fi
}

assert_provider_semantics_fixture() {
  local expected="$1"
  shift
  local fixture
  fixture="$(mktemp)"
  printf '%s\n' "$@" > "$fixture"

  if mandatory_provider_semantics_present "$fixture"; then
    actual="forbidden"
  else
    actual="allowed"
  fi
  rm -f "$fixture"
  [ "$actual" = "$expected" ] || fail "provider-semantics fixture expected $expected, got $actual"
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

# WB-SKILL-002A: exercise the exact bounded-prose predicate against ordinary
# Markdown wrapping and hard statement boundaries. The contract remains scoped
# to the target skill below; these fixtures only prove the predicate itself.
assert_provider_semantics_fixture forbidden "Provider review is mandatory."
assert_provider_semantics_fixture forbidden "Mandatory provider verification."
assert_provider_semantics_fixture forbidden "Mandatory review by a provider."
assert_provider_semantics_fixture forbidden "Verification is required by Codex."
assert_provider_semantics_fixture forbidden "Provider review is" "mandatory."
assert_provider_semantics_fixture forbidden "Provider" "review is mandatory."
assert_provider_semantics_fixture forbidden "Installation is required" "before verification."
assert_provider_semantics_fixture forbidden "Must install" "Codex."
assert_provider_semantics_fixture forbidden "Install Codex."
assert_provider_semantics_fixture forbidden "Authenticate with Codex before verification."
assert_provider_semantics_fixture forbidden "Authenticate with Codex before" "verification."
assert_provider_semantics_fixture forbidden "Please install Codex before verification."
assert_provider_semantics_fixture forbidden "To verify, install Codex."
assert_provider_semantics_fixture forbidden "Before verification, install Codex."
assert_provider_semantics_fixture forbidden "Before review, authenticate with Codex."
assert_provider_semantics_fixture forbidden "Before execution, configure Codex."
assert_provider_semantics_fixture forbidden "Ask Codex to review the implementation."
assert_provider_semantics_fixture forbidden "To verify, please request an additional model to perform verification."
assert_provider_semantics_fixture forbidden "Kindly ask a provider to verify the implementation."
assert_provider_semantics_fixture forbidden "To verify," "request second model to" "review the implementation."
assert_provider_semantics_fixture forbidden "Provider review is not mandatory; however, Provider review is mandatory."
assert_provider_semantics_fixture forbidden "Provider review is not mandatory, but Codex review is mandatory."
assert_provider_semantics_fixture forbidden "- Provider review is" "  mandatory."
assert_provider_semantics_fixture forbidden "- Provider review is" "mandatory."
assert_provider_semantics_fixture forbidden "- Provider" "review is mandatory."
assert_provider_semantics_fixture forbidden "- Installation is required" "before verification."
assert_provider_semantics_fixture forbidden "- Provider review is not mandatory; however, Provider review is mandatory."
assert_provider_semantics_fixture forbidden "- Provider review is not mandatory, but Codex review is mandatory."
assert_provider_semantics_fixture allowed "Provider execution is optional." "This skill does not grant provider authority."
assert_provider_semantics_fixture allowed "Provider review is not mandatory."
assert_provider_semantics_fixture allowed "Installation is not required before verification."
assert_provider_semantics_fixture allowed "Do not install Codex."
assert_provider_semantics_fixture allowed "Do not ask Codex to review the implementation."
assert_provider_semantics_fixture allowed "A provider does not replace required Reviewer assurance."
assert_provider_semantics_fixture allowed "Provider review is" "" "mandatory."
assert_provider_semantics_fixture allowed "Ask Codex to" "" "review the implementation."
assert_provider_semantics_fixture allowed "- Provider review is" "- mandatory."
assert_provider_semantics_fixture allowed "# Provider review is mandatory."
assert_provider_semantics_fixture allowed '```text' "Provider review is mandatory." '```'
assert_provider_semantics_fixture allowed '````text' "Provider review is mandatory." '```' '````'
assert_provider_semantics_fixture allowed '```text' "Provider review is mandatory." '~~~' '```'
assert_provider_semantics_fixture allowed '```text' "Provider review is mandatory." '``` not-a-close' '```'
# Each prohibited imperative follows an invalid closer but precedes the valid
# compatible closer. A toggle-only parser would expose it as prose and fail;
# the compatible-fence parser must continue treating it as fenced content.
assert_provider_semantics_fixture allowed '````text' "allowed code" '```' "Ask Codex to review the implementation." '````'
assert_provider_semantics_fixture allowed '```text' "allowed code" '~~~' "Ask Codex to review the implementation." '```'
assert_provider_semantics_fixture allowed '```text' "allowed code" '``` not-a-close' "Ask Codex to review the implementation." '```'
assert_provider_semantics_fixture allowed '```text' "Provider review is mandatory."
assert_provider_semantics_fixture forbidden '````text' "allowed code" '````' "Ask Codex to review the implementation."
assert_provider_semantics_fixture forbidden '```text' "allowed code" '````' "Ask Codex to review the implementation."

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
require_contains "governance/define-quality.md" 'required=false'
require_contains "governance/define-quality.md" 'configuration contradiction'
require_contains "governance/define-quality.md" 'schema-v3'
require_contains "governance/define-quality.md" 'runtime-neutral'
require_contains "governance/define-quality.md" 'Only `type=requirement` tasks count as'
require_contains "template/.agent/workflows/sdd-protocol.md" 'Define-quality prerequisite:'
require_contains "template/.agent/workflows/sdd-protocol.md" 'aggregate Define-quality prerequisite when applicable'
require_contains "template/.agent/workflows/sdd-protocol.md" 'required=false'
require_contains "template/.agent/workflows/sdd-protocol.md" 'cannot disable'
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

# WB-SKILL-001: routed role procedures and direct runtime adapters use the
# current governance vocabulary rather than retired runtime-local authority.
for path in \
  "skills/critic-review/SKILL.md" \
  "skills/scoped-coder/SKILL.md" \
  "skills/reviewer/SKILL.md" \
  "skills/verifier/SKILL.md" \
  "template/.claude/agents/critic.md" \
  "template/.claude/agents/scoped-coder.md" \
  "template/.claude/agents/reviewer.md" \
  "template/.claude/agents/verifier.md" \
  "template/.codex/AGENTS.md" \
  "template/.codex/critic.md" \
  "template/.codex/instructions.md"; do
  require_file "$path"
  require_absent_pattern "$path" 'Control Tower|Stage 0[.]5|Structural Authority Model|[.]claude/skills/(critic|reviewer|verifier)/scripts'
done

require_contains "skills/critic-review/SKILL.md" 'APPROVE.*SUPPLEMENT.*RECONSIDER'
require_contains "skills/critic-review/SKILL.md" 'RECONSIDER.*Define'
require_contains "skills/scoped-coder/SKILL.md" 'approved write-set'
require_contains "skills/scoped-coder/SKILL.md" 'local commits'
require_contains "skills/scoped-coder/SKILL.md" 'feature-branch pushes'
require_contains "skills/reviewer/SKILL.md" 'READY.*CHANGES_REQUIRED.*BLOCKED.*UNVERIFIED'
require_contains "template/.claude/agents/reviewer.md" 'READY.*CHANGES_REQUIRED.*BLOCKED.*UNVERIFIED'
require_contains "skills/verifier/SKILL.md" 'reproducible'
require_contains "template/.codex/AGENTS.md" 'governance/lifecycle.md'

# WB-SKILL-002: codex-verification is an optional runtime-adapter advisory
# procedure. These checks intentionally inspect only the current target skill;
# historical provider-specific evidence and unrelated legacy surfaces remain
# outside this contract boundary.
require_file "skills/codex-verification/SKILL.md"
require_contains "skills/codex-verification/SKILL.md" 'Authority, lifecycle, scope, and assurance selection remain with governing'
require_contains "skills/codex-verification/SKILL.md" 'contracts and the active Work Block'
require_contains "skills/codex-verification/SKILL.md" 'Additional provider execution is optional scoped evidence'
require_contains "skills/codex-verification/SKILL.md" 'If optional execution is unavailable, record an inspection gap'
require_contains "skills/codex-verification/SKILL.md" 'does not issue a project verdict'
require_absent_pattern "skills/codex-verification/SKILL.md" 'Control Tower|Stage 0[.]5|gpt-critic|gpt-verifier'
require_absent_pattern "skills/codex-verification/SKILL.md" 'Prerequisites|npm install|codex login|mcp-server'
# This case-insensitive guard scans only the target skill. It detects mandatory
# provider-review and provider-prerequisite concepts regardless of word order.
require_absent_mandatory_provider_semantics "skills/codex-verification/SKILL.md"

# WB41-R1: direct runtime adapters must retain the critical semantics they restate.
require_contains "template/.codex/AGENTS.md" 'Define.*Execute.*Assure.*Close'
require_contains "template/.codex/AGENTS.md" 'APPROVE.*SUPPLEMENT.*RECONSIDER'
require_contains "template/.codex/AGENTS.md" 'functional verdict is'
require_contains "template/.codex/AGENTS.md" 'distinct from operational gate state'
require_contains "template/.codex/AGENTS.md" 'Reviewer returns.*READY.*CHANGES_REQUIRED.*BLOCKED.*UNVERIFIED'
require_contains "template/.codex/AGENTS.md" 'returns.*READY.*BLOCKED.*UNVERIFIED.*reproducible evidence'
require_contains "template/.codex/AGENTS.md" 'ordinary reversible edits, tests, staging, local'
require_contains "template/.codex/AGENTS.md" 'feature-branch pushes'
require_contains "template/.codex/AGENTS.md" 'only when the'
require_absent_pattern "template/.codex/AGENTS.md" 'Verifier.*(sole|exclusive).*(blocker|authority|gate)|only Verifier'
require_absent_pattern "template/.codex/AGENTS.md" 'Do not stage, commit, or push[^.]*explicit Owner approval'
require_contains "template/.claude/agents/scoped-coder.md" 'staging, local commits, normal'
require_contains "template/.claude/agents/scoped-coder.md" 'feature-branch pushes'
require_contains "template/.claude/agents/scoped-coder.md" 'permitted only when the'

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
