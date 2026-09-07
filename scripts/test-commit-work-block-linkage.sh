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

# --- Literal-key handling must ignore repository-local trailer remapping ---
write_state "$repo" "WB-EXAMPLE" pending READY
git -C "$repo" config trailer.foo.key Work-Block
message "Foo: WB-EXAMPLE" "$msg"; assert_failure hook_check "$repo" "$msg"
message "Work-Block: WB-EXAMPLE" "$msg"; assert_success hook_check "$repo" "$msg"
git -C "$repo" config --unset-all trailer.foo.key

git -C "$repo" config trailer.work-block.key Foo
message "Work-Block: WB-EXAMPLE" "$msg"; assert_success hook_check "$repo" "$msg"
message "Foo: WB-EXAMPLE" "$msg"; assert_failure hook_check "$repo" "$msg"
git -C "$repo" config --unset-all trailer.work-block.key

git -C "$repo" config trailer.separators '; '
message "Work-Block: WB-EXAMPLE" "$msg"; assert_success hook_check "$repo" "$msg"
message "Work-Block; WB-EXAMPLE" "$msg"; assert_failure hook_check "$repo" "$msg"
git -C "$repo" config --unset-all trailer.separators

# --- Read-only check invariance on fresh generated project ---
fresh_project="$TMP_ROOT/fresh-generated"
assert_success "$ROOT/bootstrap.sh" --profile core "$fresh_project" "Fresh Project" fresh-project
git -C "$fresh_project" init -q
git -C "$fresh_project" config user.name "WB Fixture"
git -C "$fresh_project" config user.email "wb-fixture@example.invalid"

# Remove operational files to prove --check-git-hooks does not create/restore them
rm -rf "$fresh_project/memory_bank" "$fresh_project/.agent/active-work-block.json" "$fresh_project/.agent/project-config.md"
[ ! -d "$fresh_project/memory_bank" ] || { echo "FAIL: memory_bank exists before check" >&2; exit 1; }
[ ! -f "$fresh_project/.agent/active-work-block.json" ] || { echo "FAIL: active-work-block.json exists before check" >&2; exit 1; }
[ ! -f "$fresh_project/.agent/project-config.md" ] || { echo "FAIL: project-config.md exists before check" >&2; exit 1; }
COUNT=$((COUNT + 3))

# 1. Check before hooks configuration must fail
assert_failure bash "$fresh_project/scripts/bootstrap.sh" --check-git-hooks

# 2. Configure local core.hooksPath and capture config hashes
git -C "$fresh_project" config --local core.hooksPath .githooks
LOCAL_CONFIG_BEFORE="$(sha256sum "$fresh_project/.git/config" | awk '{print $1}')"
GLOBAL_CONFIG_SNAPSHOT="$(sha256sum "$GLOBAL_CONFIG" | awk '{print $1}')"

# 3. Check must succeed and print deterministic output
check_out="$(bash "$fresh_project/scripts/bootstrap.sh" --check-git-hooks)"
[ "$check_out" = "  CHECKED: repository-local core.hooksPath=.githooks" ] || {
  echo "FAIL: unexpected check-git-hooks output: $check_out" >&2; exit 1;
}
COUNT=$((COUNT + 1))

# 4. Check must be strictly read-only: no operational files created, no configs mutated
[ ! -d "$fresh_project/memory_bank" ] || { echo "FAIL: check-git-hooks created memory_bank" >&2; exit 1; }
[ ! -f "$fresh_project/.agent/active-work-block.json" ] || { echo "FAIL: check-git-hooks created active-work-block.json" >&2; exit 1; }
[ ! -f "$fresh_project/.agent/project-config.md" ] || { echo "FAIL: check-git-hooks created project-config.md" >&2; exit 1; }
LOCAL_CONFIG_AFTER="$(sha256sum "$fresh_project/.git/config" | awk '{print $1}')"
[ "$LOCAL_CONFIG_BEFORE" = "$LOCAL_CONFIG_AFTER" ] || { echo "FAIL: check-git-hooks modified local git config" >&2; exit 1; }
GLOBAL_CONFIG_AFTER_CHECK="$(sha256sum "$GLOBAL_CONFIG" | awk '{print $1}')"
[ "$GLOBAL_CONFIG_SNAPSHOT" = "$GLOBAL_CONFIG_AFTER_CHECK" ] || { echo "FAIL: check-git-hooks modified global git config" >&2; exit 1; }
COUNT=$((COUNT + 5))

# 5. Normal bootstrap restores operational files and leaves hooksPath untouched
before_hooks="$(git -C "$fresh_project" config --local --get core.hooksPath 2>/dev/null || true)"
assert_success bash "$fresh_project/scripts/bootstrap.sh"
after_hooks="$(git -C "$fresh_project" config --local --get core.hooksPath 2>/dev/null || true)"
[ "$before_hooks" = "$after_hooks" ] || { echo "FAIL: default bootstrap changed hooksPath" >&2; exit 1; }
[ -d "$fresh_project/memory_bank" ] || { echo "FAIL: default bootstrap did not create memory_bank" >&2; exit 1; }
[ -f "$fresh_project/.agent/active-work-block.json" ] || { echo "FAIL: default bootstrap did not create active-work-block.json" >&2; exit 1; }
[ -f "$fresh_project/.agent/project-config.md" ] || { echo "FAIL: default bootstrap did not create project-config.md" >&2; exit 1; }
COUNT=$((COUNT + 4))

# 6. Fingerprint verification: check does not modify existing operational files
MB_SUM_BEFORE="$(sha256sum "$fresh_project/memory_bank/context.md" | awk '{print $1}')"
AWB_SUM_BEFORE="$(sha256sum "$fresh_project/.agent/active-work-block.json" | awk '{print $1}')"
PC_SUM_BEFORE="$(sha256sum "$fresh_project/.agent/project-config.md" | awk '{print $1}')"
assert_success bash "$fresh_project/scripts/bootstrap.sh" --check-git-hooks
MB_SUM_AFTER="$(sha256sum "$fresh_project/memory_bank/context.md" | awk '{print $1}')"
AWB_SUM_AFTER="$(sha256sum "$fresh_project/.agent/active-work-block.json" | awk '{print $1}')"
PC_SUM_AFTER="$(sha256sum "$fresh_project/.agent/project-config.md" | awk '{print $1}')"
[ "$MB_SUM_BEFORE" = "$MB_SUM_AFTER" ] || { echo "FAIL: check-git-hooks modified memory_bank" >&2; exit 1; }
[ "$AWB_SUM_BEFORE" = "$AWB_SUM_AFTER" ] || { echo "FAIL: check-git-hooks modified active-work-block.json" >&2; exit 1; }
[ "$PC_SUM_BEFORE" = "$PC_SUM_AFTER" ] || { echo "FAIL: check-git-hooks modified project-config.md" >&2; exit 1; }
COUNT=$((COUNT + 4))

# --- Explicit install mode on unconfigured project ---
unconfigured_project="$TMP_ROOT/unconfigured-project"
assert_success "$ROOT/bootstrap.sh" --profile core "$unconfigured_project" "Unconfigured Project" unconfigured-project
git -C "$unconfigured_project" init -q
git -C "$unconfigured_project" config user.name "WB Fixture"
git -C "$unconfigured_project" config user.email "wb-fixture@example.invalid"
assert_failure bash "$unconfigured_project/scripts/bootstrap.sh" --check-git-hooks
assert_success bash "$unconfigured_project/scripts/bootstrap.sh" --install-git-hooks
[ "$(git -C "$unconfigured_project" config --local --get core.hooksPath)" = ".githooks" ] || exit 1
assert_success bash "$unconfigured_project/scripts/bootstrap.sh" --check-git-hooks
COUNT=$((COUNT + 3))

# --- Live commit enforcement and documented limitations in disposable active-WB repo ---
live_repo="$TMP_ROOT/live-active"
assert_success "$ROOT/bootstrap.sh" --profile core "$live_repo" "Live Repo" live-repo
git -C "$live_repo" init -q
git -C "$live_repo" config user.name "WB Fixture"
git -C "$live_repo" config user.email "wb-fixture@example.invalid"
assert_success bash "$live_repo/scripts/bootstrap.sh" --install-git-hooks

# Initial commit with inactive WB
printf 'initial\n' > "$live_repo/init.txt"
git -C "$live_repo" add "$live_repo/init.txt"
assert_success git -C "$live_repo" commit -m "initial commit"

# Create a separate branch with a commit lacking the trailer (for cherry-pick testing)
git -C "$live_repo" checkout -q -b feature-branch
printf 'feature content\n' > "$live_repo/feature.txt"
git -C "$live_repo" add "$live_repo/feature.txt"
assert_success git -C "$live_repo" commit -m "feature commit without trailer"
main_branch="$(git -C "$live_repo" rev-parse --abbrev-ref HEAD@{1} 2>/dev/null || echo "main")"
if ! git -C "$live_repo" rev-parse --verify "$main_branch" >/dev/null 2>&1; then
  main_branch="master"
fi
git -C "$live_repo" checkout -q "$main_branch"

# Activate Work Block
write_state "$live_repo" "WB-LIVE-001" pending READY

# 1. Ordinary git commit without trailer -> rejected
printf 'change 1\n' > "$live_repo/change1.txt"
git -C "$live_repo" add "$live_repo/change1.txt"
assert_failure git -C "$live_repo" commit -m "ordinary commit without trailer"

# 2. Ordinary git commit with exact trailer -> accepted
printf 'change 2\n' > "$live_repo/change2.txt"
git -C "$live_repo" add "$live_repo/change2.txt"
message "Work-Block: WB-LIVE-001" "$live_repo/msg.txt"
assert_success git -C "$live_repo" commit -F "$live_repo/msg.txt"

# 3. git commit --no-verify -> succeeds (documented cooperative bypass)
printf 'change 3\n' > "$live_repo/change3.txt"
git -C "$live_repo" add "$live_repo/change3.txt"
assert_success git -C "$live_repo" commit --no-verify -m "commit with --no-verify bypass"

# 4. git cherry-pick without trailer -> succeeds (documented enforcement limitation)
# Git cherry-pick does not invoke the commit-msg hook by default.
assert_success git -C "$live_repo" cherry-pick feature-branch
cp_msg="$(git -C "$live_repo" log -n 1 --format=%B)"
[ "$cp_msg" = "feature commit without trailer" ] || { echo "FAIL: unexpected cherry-pick commit message: $cp_msg" >&2; exit 1; }
COUNT=$((COUNT + 1))

# 5. git revert without trailer -> succeeds (documented enforcement limitation)
# Git revert --no-edit does not invoke the commit-msg hook by default.
assert_success git -C "$live_repo" revert --no-edit HEAD
rev_msg="$(git -C "$live_repo" log -n 1 --format=%s)"
case "$rev_msg" in
  Revert*) ;;
  *) echo "FAIL: unexpected revert commit subject: $rev_msg" >&2; exit 1 ;;
esac
COUNT=$((COUNT + 1))

# --- Global config invariant check ---
GLOBAL_CONFIG_AFTER="$(sha256sum "$GLOBAL_CONFIG" | awk '{print $1}')"
[ "$GLOBAL_CONFIG_BEFORE" = "$GLOBAL_CONFIG_AFTER" ] || {
  echo "FAIL: bootstrap changed disposable global Git config" >&2
  exit 1
}
COUNT=$((COUNT + 1))

echo "PASS commit↔Work Block linkage fixtures: $COUNT assertions"
