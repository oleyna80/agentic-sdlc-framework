#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK="$ROOT/template/.githooks/commit-msg"
COUNT=0
TMP_ROOT="$(mktemp -d -t wb-gov-001-XXXXXX)"
trap 'rm -rf "$TMP_ROOT"' EXIT
GLOBAL_CONFIG="$TMP_ROOT/global.gitconfig"
printf '[wb-fixture]\n\tsentinel = unchanged\n' > "$GLOBAL_CONFIG"
export GIT_CONFIG_GLOBAL="$GLOBAL_CONFIG"
export GIT_CONFIG_NOSYSTEM=1
GLOBAL_CONFIG_BEFORE="$(sha256sum "$GLOBAL_CONFIG" | awk '{print $1}')"

assert_success() { "$@" >/dev/null 2>&1 || { echo "FAIL: $*" >&2; exit 1; }; COUNT=$((COUNT + 1)); }
assert_failure() { if "$@" >/dev/null 2>&1; then echo "FAIL unexpectedly passed: $*" >&2; exit 1; fi; COUNT=$((COUNT + 1)); }
write_state() {
  local repo="$1" id="$2" mode="$3" gate="${4:-READY}"
  python3 - "$repo/.agent/active-work-block.json" "$id" "$mode" "$gate" <<'PY'
import json, pathlib, sys
path, work_block_id, mode, gate = sys.argv[1:]
value = {"schema_version": 3, "work_block_id": work_block_id,
         "closeout_mode": mode, "write_gate": {"status": gate}}
pathlib.Path(path).write_text(json.dumps(value) + "\n", encoding="utf-8")
PY
}
message() { printf 'fixture commit\n\n%s\n' "$1" > "$2"; }
hook_check() { (cd "$1" && python3 .githooks/commit-msg "$2"); }

new_repo() {
  local repo="$TMP_ROOT/$1"
  mkdir -p "$repo/.agent" "$repo/.githooks"
  cp "$HOOK" "$repo/.githooks/commit-msg"
  chmod +x "$repo/.githooks/commit-msg"
  git -C "$repo" init -q
  git -C "$repo" config user.name "WB Fixture"
  git -C "$repo" config user.email "wb-fixture@example.invalid"
  cp "$ROOT/template/.agent/active-work-block.default.json" "$repo/.agent/active-work-block.json"
  git -C "$repo" config core.hooksPath .githooks
  printf '%s\n' "$repo"
}

repo="$(new_repo matrix)"
msg="$TMP_ROOT/message.txt"
message "" "$msg"; assert_success hook_check "$repo" "$msg"; COUNT=$((COUNT + 0))
write_state "$repo" "WB-EXAMPLE" pending READY
message "Work-Block: WB-EXAMPLE" "$msg"; assert_success hook_check "$repo" "$msg"
message "" "$msg"; assert_failure hook_check "$repo" "$msg"
message "Work-Block: WB-WRONG" "$msg"; assert_failure hook_check "$repo" "$msg"
message $'Work-Block: WB-EXAMPLE\nWork-Block: WB-EXAMPLE' "$msg"; assert_failure hook_check "$repo" "$msg"
message "Work-Block:" "$msg"; assert_failure hook_check "$repo" "$msg"
write_state "$repo" "WB-FROZEN" pending BLOCKED
message "Work-Block: WB-FROZEN" "$msg"; assert_success hook_check "$repo" "$msg"
message "" "$msg"; assert_failure hook_check "$repo" "$msg"
write_state "$repo" "WB-CLOSED" success-closeout
message "" "$msg"; assert_success hook_check "$repo" "$msg"
write_state "$repo" "WB-REPORT" reporting-only
message "" "$msg"; assert_success hook_check "$repo" "$msg"
write_state "$repo" "" pending
message "" "$msg"; assert_success hook_check "$repo" "$msg"
printf '{broken\n' > "$repo/.agent/active-work-block.json"; assert_failure hook_check "$repo" "$msg"
printf '{"schema_version":2,"work_block_id":"WB-X","closeout_mode":"pending"}\n' > "$repo/.agent/active-work-block.json"; assert_failure hook_check "$repo" "$msg"
printf '{"schema_version":3,"work_block_id":7,"closeout_mode":"pending"}\n' > "$repo/.agent/active-work-block.json"; assert_failure hook_check "$repo" "$msg"
write_state "$repo" "WB-A" pending READY
message "work-block: WB-A" "$msg"; assert_failure hook_check "$repo" "$msg"

project="$TMP_ROOT/generated"
assert_success "$ROOT/bootstrap.sh" --profile core "$project" "Fixture Project" fixture-project
git -C "$project" init -q
git -C "$project" config user.name "WB Fixture"
git -C "$project" config user.email "wb-fixture@example.invalid"
before_hooks="$(git -C "$project" config --local --get core.hooksPath 2>/dev/null || true)"
assert_success bash "$project/scripts/bootstrap.sh"
after_hooks="$(git -C "$project" config --local --get core.hooksPath 2>/dev/null || true)"
[ "$before_hooks" = "$after_hooks" ] || { echo "FAIL: default bootstrap changed hooksPath" >&2; exit 1; }
COUNT=$((COUNT + 1))
assert_failure bash "$project/scripts/bootstrap.sh" --check-git-hooks
assert_success bash "$project/scripts/bootstrap.sh" --install-git-hooks
COUNT=$((COUNT + 1))
[ "$(git -C "$project" config --local --get core.hooksPath)" = ".githooks" ] || exit 1
COUNT=$((COUNT + 1))
assert_success bash "$project/scripts/bootstrap.sh" --check-git-hooks
write_state "$project" "WB-REAL" pending READY
assert_failure git -C "$project" commit --allow-empty -m "real fixture rejection"
assert_success git -C "$project" commit --allow-empty --no-verify -m "real fixture bypass"
message "Work-Block: WB-REAL" "$project/commit-msg.txt"
assert_success git -C "$project" commit --allow-empty -F "$project/commit-msg.txt"
COUNT=$((COUNT + 1))

GLOBAL_CONFIG_AFTER="$(sha256sum "$GLOBAL_CONFIG" | awk '{print $1}')"
[ "$GLOBAL_CONFIG_BEFORE" = "$GLOBAL_CONFIG_AFTER" ] || {
  echo "FAIL: bootstrap changed disposable global Git config" >&2
  exit 1
}
COUNT=$((COUNT + 1))

echo "PASS commit↔Work Block linkage fixtures: $COUNT assertions"
