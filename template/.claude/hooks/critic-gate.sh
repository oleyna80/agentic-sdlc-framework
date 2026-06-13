#!/usr/bin/env bash
# Critic Gate hook - blocks Edit/MultiEdit/Write until critic review is
# resolved for the current Work Block and requested file path.
set -euo pipefail

GATE_FILE=".agent/critic-gate.md"

MEMORY_DIR="memory_bank"
[ -d "memory-bank" ] && [ -f "memory-bank/orchestrator-log.md" ] && MEMORY_DIR="memory-bank"
LOG_FILE="$MEMORY_DIR/orchestrator-log.md"

payload=$(cat)
tool=$(printf '%s' "$payload" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
file_path=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // ""' 2>/dev/null || echo "")
session_id=$(printf '%s' "$payload" | jq -r '.session_id // ""' 2>/dev/null || echo "")

deny() {
  local reason="$1"
  jq -n --arg reason "$reason" '{
    continue: false,
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
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

approved_write_set() {
  awk '
    BEGIN { in_set = 0 }
    /^Approved[ -]Write-Set:/ || /^Approved write-set:/ {
      in_set = 1
      next
    }
    in_set && /^[[:space:]]*[-*][[:space:]]+/ {
      sub(/^[[:space:]]*[-*][[:space:]]+/, "")
      print
      next
    }
    in_set && /^[[:space:]]*$/ { next }
    in_set && /^[A-Za-z][A-Za-z -]*:/ { exit }
  ' "$GATE_FILE"
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

path_allowed() {
  local path="$1"
  local rel_path pattern
  rel_path=$(relative_path "$path")

  while IFS= read -r pattern; do
    pattern="${pattern%%#*}"
    pattern="$(printf '%s' "$pattern" | xargs)"
    [ -z "$pattern" ] && continue
    [ "$pattern" = "[to be defined per Work Block]" ] && continue

    case "$pattern" in
      */)
        [[ "$rel_path" == "$pattern"* ]] && return 0
        ;;
      *)
        [[ "$rel_path" == "$pattern" ]] && return 0
        [[ "$rel_path" == $pattern ]] && return 0
        ;;
    esac
  done < <(approved_write_set)

  return 1
}

case "$tool" in
  Edit|MultiEdit|Write) ;;
  *) exit 0 ;;
esac

rel_file_path=$(relative_path "$file_path")

# Control Tower must always be able to open/refresh the active gate and log.
case "$rel_file_path" in
  "$GATE_FILE"|"$LOG_FILE") exit 0 ;;
esac

[ -n "$file_path" ] || deny "Critic gate: Edit/MultiEdit/Write payload did not include tool_input.file_path."
[ -f "$GATE_FILE" ] || deny "Critic gate: .agent/critic-gate.md is missing. Complete Stage 0 Preflight with critic review decision before editing files."

status=$(field "Status")
wb_id=$(field "Work Block")
expires=$(field "Expires")
gate_session=$(field "Session")

[ -n "$wb_id" ] || deny "Critic gate: Work Block is required before repository edits."

if [ -n "$expires" ]; then
  today=$(date +%F)
  [[ "$expires" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] \
    || deny "Critic gate: Expires must use YYYY-MM-DD."
  [[ "$expires" < "$today" ]] \
    && deny "Critic gate: approval expired on ${expires}. Refresh Stage 0/0.5 before editing files."
fi

if [ -n "$gate_session" ] && [ "$gate_session" != "any" ]; then
  [ -n "$session_id" ] \
    || deny "Critic gate: Session is locked but hook payload has no session_id."
  [ "$gate_session" = "$session_id" ] \
    || deny "Critic gate: approval belongs to session ${gate_session}, current session is ${session_id}."
fi

path_allowed "$file_path" \
  || deny "Critic gate: ${rel_file_path} is outside the Approved Write-Set for ${wb_id}. If this file is intended, update Stage 0 approval by adding this line under Approved Write-Set in ${GATE_FILE}: - ${rel_file_path}"

case "$status" in
  READY)
    exit 0
    ;;

  SKIPPED)
    no_skip=$(field "No-Skip")
    [ "$no_skip" = "true" ] \
      && deny "Critic gate: this Work Block touches a new domain. SKIPPED is not allowed; launch critic agent."

    [ -f "$LOG_FILE" ] \
      || deny "Critic gate: SKIPPED requires orchestrator-log entry. ${LOG_FILE} not found."

    grep -q "^|.*${wb_id}.*critic: SKIPPED" "$LOG_FILE" 2>/dev/null \
      || deny "Critic gate: SKIPPED not authorized. No matching critic: SKIPPED Owner approval entry in orchestrator-log for ${wb_id}."

    skip_count=0
    while IFS= read -r line; do
      case "$line" in
        *"SKIPPED"*) skip_count=$((skip_count + 1)) ;;
        *"APPROVE"*|*"SUPPLEMENT"*|*"RECONSIDER"*) skip_count=0 ;;
      esac
    done < <(grep "critic:" "$LOG_FILE" 2>/dev/null || true)

    [ "$skip_count" -ge 3 ] \
      && deny "Critic gate: ${skip_count} consecutive SKIPs. Critic is mandatory for this Work Block."

    exit 0
    ;;

  *)
    deny "Critic gate: .agent/critic-gate.md status is ${status:-missing}. Launch critic agent or obtain Owner approval before editing files."
    ;;
esac
