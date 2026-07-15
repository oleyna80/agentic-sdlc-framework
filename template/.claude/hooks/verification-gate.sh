#!/usr/bin/env bash
# Verification Gate hook - blocks final closeout until verification status is
# evidence-backed for the current Work Block.
set -euo pipefail

GATE_FILE=".agent/verification-gate.md"

MEMORY_DIR="memory_bank"
[ -d "memory-bank" ] && [ -f "memory-bank/orchestrator-log.md" ] && MEMORY_DIR="memory-bank"
LOG_FILE="$MEMORY_DIR/orchestrator-log.md"

deny() {
  local reason="$1"
  jq -n --arg reason "$reason" '{
    decision: "block",
    reason: $reason
  }'
  exit 0
}

field() {
  local name="$1"
  grep -i "^${name}:" "$GATE_FILE" 2>/dev/null \
    | head -1 \
    | sed -E "s/^${name}:[[:space:]]*//I" \
    | xargs \
    || true
}

relative_path() {
  local path="$1"
  local cwd
  cwd=$(pwd)
  path="${path#./}"
  case "$path" in
    "$cwd"/*) path="${path#"$cwd"/}" ;;
  esac
  printf '%s' "$path"
}

is_placeholder() {
  local value="$1"
  [ -z "$value" ] && return 0
  case "$value" in
    "["*"]"|PENDING|pending|none|NONE) return 0 ;;
    *) return 1 ;;
  esac
}

require_report_file() {
  local field_name="$1"
  local label="$2"
  local report_path
  report_path=$(field "$field_name")

  is_placeholder "$report_path" \
    && deny "Verification gate: ${label} requires ${field_name} to point to a report under docs/reports/."

  report_path=$(relative_path "$report_path")
  case "$report_path" in
    docs/reports/*) ;;
    *) deny "Verification gate: ${field_name} must be under docs/reports/, got '${report_path}'." ;;
  esac

  [ -s "$report_path" ] \
    || deny "Verification gate: ${field_name} report does not exist or is empty: ${report_path}."
}

require_log_entry() {
  local needle="$1"
  local label="$2"

  [ -f "$LOG_FILE" ] \
    || deny "Verification gate: ${label} requires orchestrator-log entry. ${LOG_FILE} not found."

  grep -q "^|.*${wb_id}.*${needle}" "$LOG_FILE" 2>/dev/null \
    || deny "Verification gate: ${label} missing orchestrator-log entry for ${wb_id}: ${needle}."
}

[ -f "$GATE_FILE" ] \
  || deny "Verification gate: .agent/verification-gate.md is missing. Resolve verification before final closeout."

status=$(field "Status")
wb_id=$(field "Work Block")
verification_tier=$(field "Verification Tier")
new_domain=$(field "New Domain")
sensitive_domains=$(field "Sensitive Domains" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')
verifier_verdict=$(field "Claude Verifier Verdict")
verifier=$(field "Verifier")
required_verifier_isolation=$(field "Required Verifier Isolation" | tr '[:upper:]' '[:lower:]')
verifier_isolation=$(field "Verifier Isolation" | tr '[:upper:]' '[:lower:]')
gpt_verifier_status=$(field "GPT Verifier Status")
gpt_verifier_reason=$(field "GPT Verifier Reason")
gpt_degraded_reason=$(field "GPT Verifier Degraded Reason")
quick_fix=$(field "Quick-Fix")
stage3_mode=$(field "Stage 3 Mode")

[ -n "$wb_id" ] || deny "Verification gate: Work Block is required before closeout."

isolation_rank() {
  case "$1" in
    same-session-degraded) printf '1' ;;
    independent-readonly-root) printf '2' ;;
    os-isolated) printf '3' ;;
    *) return 1 ;;
  esac
}

require_verifier_isolation() {
  local required_rank actual_rank

  required_rank=$(isolation_rank "$required_verifier_isolation") \
    || deny "Verification gate: Required Verifier Isolation is ${required_verifier_isolation:-missing}. Use same-session-degraded, independent-readonly-root, or os-isolated."
  actual_rank=$(isolation_rank "$verifier_isolation") \
    || deny "Verification gate: Verifier Isolation is ${verifier_isolation:-missing}. Use same-session-degraded, independent-readonly-root, or os-isolated."
  [ "$actual_rank" -ge "$required_rank" ] \
    || deny "Verification gate: Verifier Isolation (${verifier_isolation}) is below Required Verifier Isolation (${required_verifier_isolation})."

  case "$verifier" in
    subagent)
      [ "$actual_rank" -ge 2 ] \
        || deny "Verification gate: same-session native subagent verification is advisory and cannot close READY. Use an independent readonly root or OS isolation."
      ;;
    ct-inline)
      [ "$sensitive_domains" = "none" ] \
        || deny "Verification gate: ct-inline is only allowed for Sensitive Domains: none."
      [ "$verifier_isolation" = "same-session-degraded" ] \
        || deny "Verification gate: ct-inline must record Verifier Isolation: same-session-degraded."
      ;;
    PENDING|pending|"["*|"") deny "Verification gate: Verifier is ${verifier:-missing}. Set Verifier: subagent or ct-inline before closeout." ;;
    *) deny "Verification gate: invalid Verifier '${verifier}'. Use subagent or ct-inline." ;;
  esac

  if [ "$verification_tier" = "full" ] || [ "$verification_tier" = "FULL" ]; then
    [ "$actual_rank" -ge 2 ] \
      || deny "Verification gate: Full tier requires at least independent-readonly-root verifier isolation."
  fi

  case ",$sensitive_domains," in
    *,credentials,*|*,live-data,*|*,deploy,*|*,external-provider,*)
      [ "$actual_rank" -ge 3 ] \
        || deny "Verification gate: Sensitive Domains (${sensitive_domains}) require os-isolated verifier isolation."
      ;;
    *,auth,*|*,payments,*|*,db-schema,*|*,middleware,*|*,hooks,*|*,runtime-config,*)
      [ "$actual_rank" -ge 2 ] \
        || deny "Verification gate: Sensitive Domains (${sensitive_domains}) require at least independent-readonly-root verifier isolation."
      ;;
  esac
}

gpt_verifier_required=0
case "$verification_tier" in
  full|FULL) gpt_verifier_required=1 ;;
  lite|standard|LITE|STANDARD|"") ;;
  PENDING|pending) deny "Verification gate: Verification Tier is PENDING. Classify verification tier before closeout." ;;
  *) deny "Verification gate: invalid Verification Tier '${verification_tier}'. Use lite, standard, or full." ;;
esac
case "$new_domain" in
  true|TRUE|yes|YES) gpt_verifier_required=1 ;;
  false|FALSE|no|NO|"") ;;
  PENDING|pending) deny "Verification gate: New Domain is PENDING. Classify domain status before closeout." ;;
  *) deny "Verification gate: invalid New Domain '${new_domain}'. Use true or false." ;;
esac

case "$sensitive_domains" in
  none|NONE) ;;
  PENDING|pending|"") deny "Verification gate: Sensitive Domains is ${sensitive_domains:-missing}. Use none or a comma-separated subset of auth,payments,db-schema,middleware,hooks,runtime-config,deploy,credentials,live-data,external-provider." ;;
  *)
    IFS=',' read -r -a sensitive_domain_items <<< "$sensitive_domains"
    for sensitive_domain in "${sensitive_domain_items[@]}"; do
      sensitive_domain=$(printf '%s' "$sensitive_domain" | xargs)
      case "$sensitive_domain" in
        auth|payments|db-schema|middleware|hooks|runtime-config|deploy|credentials|live-data|external-provider) gpt_verifier_required=1 ;;
        *) deny "Verification gate: invalid Sensitive Domains value '${sensitive_domain}'. Use none or auth,payments,db-schema,middleware,hooks,runtime-config,deploy,credentials,live-data,external-provider." ;;
      esac
    done
    ;;
esac
case "$verifier_verdict" in
  BLOCKED|UNVERIFIED) gpt_verifier_required=1 ;;
  READY|PENDING|"") ;;
  *) deny "Verification gate: invalid Claude Verifier Verdict '${verifier_verdict}'. Use READY, BLOCKED, UNVERIFIED, or PENDING." ;;
esac

case "$gpt_verifier_status" in
  NOT_REQUIRED)
    [ "$gpt_verifier_required" -eq 0 ] \
      || deny "Verification gate: GPT verifier is required by trigger; NOT_REQUIRED is not allowed."
    is_placeholder "$gpt_verifier_reason" \
      && deny "Verification gate: GPT Verifier Reason is required when GPT Verifier Status is NOT_REQUIRED."
    ;;
  READY)
    require_report_file "GPT Verifier Report" "GPT verifier READY"
    ;;
  DEGRADED)
    [ "$gpt_degraded_reason" = "review-degraded:codex-mcp-unavailable" ] \
      || deny "Verification gate: GPT verifier DEGRADED requires GPT Verifier Degraded Reason: review-degraded:codex-mcp-unavailable."
    require_log_entry "review-degraded:codex-mcp-unavailable" "GPT verifier DEGRADED"
    ;;
  PENDING|"") deny "Verification gate: GPT Verifier Status is ${gpt_verifier_status:-missing}. Resolve GPT verifier decision before closeout." ;;
  *) deny "Verification gate: invalid GPT Verifier Status '${gpt_verifier_status}'. Use NOT_REQUIRED, READY, or DEGRADED." ;;
esac

case "$status" in
  READY)
    require_report_file "Verification Report" "verification READY"
    require_verifier_isolation
    case "$verifier_verdict" in
      READY)
        [ "$stage3_mode" = "success-closeout" ] \
          || deny "Verification gate: READY verdict requires Stage 3 Mode: success-closeout."
        ;;
      BLOCKED|UNVERIFIED)
        [ "$stage3_mode" = "reporting-only" ] \
          || deny "Verification gate: ${verifier_verdict} verdict requires Stage 3 Mode: reporting-only."
        ;;
      PENDING|"") deny "Verification gate: Claude Verifier Verdict is ${verifier_verdict:-missing}. Record verifier verdict before closeout." ;;
      *) deny "Verification gate: invalid Claude Verifier Verdict '${verifier_verdict}'. Use READY, BLOCKED, or UNVERIFIED." ;;
    esac
    exit 0
    ;;

  SKIPPED)
    [ "$quick_fix" = "true" ] \
      || deny "Verification gate: SKIPPED is only allowed when Quick-Fix is true."
    [ "$verifier_verdict" = "READY" ] \
      || deny "Verification gate: SKIPPED verifier dispatch still requires an inline READY verdict."
    [ "$stage3_mode" = "success-closeout" ] \
      || deny "Verification gate: inline READY verification requires Stage 3 Mode: success-closeout."
    require_verifier_isolation
    require_report_file "Verification Report" "inline verification READY"
    require_log_entry "verification: SKIPPED" "verification SKIPPED"
    exit 0
    ;;

  *)
    deny "Verification gate: .agent/verification-gate.md status is ${status:-missing}. Complete verification before final closeout."
    ;;
esac
