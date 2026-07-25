#!/usr/bin/env bash
# Validate that the framework is safe and coherent enough for public release.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0

fail() {
  echo "FAIL: $*"
  FAIL=1
}

ok() {
  echo "OK: $*"
}

require_file() {
  local path="$1"
  if [ -f "$ROOT/$path" ]; then
    ok "$path"
  else
    fail "missing $path"
  fi
}

require_absent() {
  local path="$1"
  if [ -e "$ROOT/$path" ]; then
    fail "$path must not exist in the publishable scaffold"
  else
    ok "$path absent"
  fi
}

require_line() {
  local path="$1"
  local pattern="$2"
  if grep -qx -- "$pattern" "$ROOT/$path"; then
    ok "$path contains standalone line: $pattern"
  else
    fail "$path missing standalone line: $pattern"
  fi
}

echo "==> Publication validation: $ROOT"

for path in \
  "README.md" \
  "SETUP.md" \
  "PROJECT_MAP.md" \
  "FILE_REGISTRY.yml" \
  "LICENSE" \
  "THIRD_PARTY_NOTICES.md" \
  "CONTRIBUTING.md" \
  "SECURITY.md" \
  "CHANGELOG.md" \
  "PUBLICATION_CHECKLIST.md" \
  "bootstrap.sh" \
  "skills/catalog.yml" \
  "governance/README.md" \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/runtime-capabilities.md" \
  "runtimes/README.md" \
  "runtimes/codex/README.md" \
  "runtimes/claude-code/README.md" \
  "runtimes/opencode/README.md" \
  "runtimes/generic/README.md" \
  "integrations/README.md" \
  "integrations/claude-code-codex-plugin/README.md" \
  "integrations/mcp/README.md" \
  "integrations/file-handoff/README.md" \
  "docs/profiles.md" \
  "docs/session-bootstrap.md" \
  "docs/mcp-tool-policy.md" \
  "docs/plans/wb-004-integration-adapter-normalization.md" \
  "handoff/README.md" \
  "handoff/templates/runtime-task-template.md" \
  "handoff/templates/claude-team-task-template.md" \
  "handoff/runner/handoff-runner.sh" \
  "handoff/runner/parallel-runner.sh" \
  "handoff/runner/sanitize-env.sh" \
  "handoff/runner/watch-queue.sh" \
  "scripts/test-sdd-contract.sh" \
  "scripts/test-integration-contracts.py" \
  "scripts/test-codex-adapter.py" \
  "scripts/test-codex-hard-stops.py" \
  "scripts/validate-governance.sh" \
  "template/project.gitignore" \
  "template/AGENTS.md" \
  "template/CLAUDE.md" \
  "template/PROJECT_MAP.md" \
  "template/FILE_REGISTRY.yml" \
  "template/.agent/ROSTER.md" \
  "template/.agent/active-work-block.json" \
  "template/.agent/hooks/hard_stop_policy.py" \
  "template/.agent/workflows/sdd-protocol.md" \
  "template/.mcp.json" \
  "template/.claude/settings.json" \
  "template/.claude/hooks/work_block_gate.py" \
  "template/.claude/hooks/assurance_gate.py" \
  "template/.claude/hooks/critic-gate.sh" \
  "template/.claude/hooks/hard-stop.sh" \
  "template/.claude/hooks/typecheck.sh" \
  "template/.claude/hooks/verification-gate.sh" \
  "template/.claude/agents/solution-architect.md" \
  "template/.claude/agents/critic.md" \
  "template/.claude/agents/scoped-coder.md" \
  "template/.claude/agents/reviewer.md" \
  "template/.claude/agents/verifier.md" \
  "template/.codex/hooks.json" \
  "template/.codex/hooks/hard_stop_policy.py" \
  "template/.codex/hooks/pre_tool_use_policy.py" \
  "template/.codex/hooks/stage0_write_gate.py" \
  "template/.codex/hooks/subagent_context.py" \
  "template/opencode.json" \
  "template/.opencode/agents/architect.md" \
  "template/.opencode/agents/critic.md" \
  "template/.opencode/agents/coder.md" \
  "template/.opencode/agents/reviewer.md" \
  "template/.opencode/agents/verifier.md" \
  "template/docs/templates/work-block-template.md" \
  "template/docs/templates/spec-drift-report-template.md" \
  "template/docs/templates/integration-admission-template.md" \
  "template/scripts/bootstrap.sh"; do
  require_file "$path"
done

for path in \
  "template/.gitignore" \
  "template/.claude/agents/gpt-critic.md" \
  "template/.claude/agents/gpt-verifier.md" \
  "template/.claude/agents/codex-reviewer.md" \
  "template/.claude/agent-memory/gpt-critic/MEMORY.md" \
  "template/.claude/agent-memory/gpt-verifier/MEMORY.md" \
  "template/.claude/agent-memory/codex-reviewer/MEMORY.md"; do
  require_absent "$path"
done

require_line ".gitignore" "archive/"
require_line ".gitignore" "node_modules/"
require_line ".gitignore" ".env"
require_line "template/project.gitignore" ".agent/"
require_line "template/project.gitignore" "memory_bank/"
require_line "template/project.gitignore" ".claude/agent-memory/"
require_line "template/project.gitignore" ".codex/"
require_line "template/project.gitignore" "node_modules/"
require_line "template/project.gitignore" ".env"

CORE_SKILLS="$(sed -n 's/^CORE_SKILLS="\(.*\)"$/\1/p' "$ROOT/bootstrap.sh")"
if [ -z "$CORE_SKILLS" ]; then
  fail "unable to read CORE_SKILLS from bootstrap.sh"
else
  for skill in $CORE_SKILLS; do
    require_file "skills/$skill/SKILL.md"
  done
fi

if command -v python3 >/dev/null 2>&1; then
  python3 - "$ROOT" <<'PY' || fail "JSON/YAML/public configuration validation failed"
import json
import pathlib
import sys
import yaml

root = pathlib.Path(sys.argv[1])

for relative in ("FILE_REGISTRY.yml", "template/FILE_REGISTRY.yml", "skills/catalog.yml"):
    path = root / relative
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{relative} must parse to a mapping")

for relative in (
    ".claude/settings.json",
    "template/.claude/settings.json",
    "template/.mcp.json",
    "template/.agent/active-work-block.json",
    "template/.codex/hooks.json",
    "template/opencode.json",
):
    path = root / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{relative} must parse to an object")

mcp = json.loads((root / "template/.mcp.json").read_text(encoding="utf-8"))
if mcp != {"mcpServers": {}}:
    raise SystemExit("template/.mcp.json must remain empty by default")

claude = json.loads((root / "template/.claude/settings.json").read_text(encoding="utf-8"))
if any(key in claude for key in ("enabledMcpjsonServers", "permissions", "autoMode")):
    raise SystemExit("template Claude settings must not pre-enable external integrations")
expected_agents = {"solution-architect", "critic", "reviewer", "scoped-coder", "verifier"}
if set(claude.get("agents", {})) != expected_agents:
    raise SystemExit("template Claude settings logical agent set mismatch")

opencode = json.loads((root / "template/opencode.json").read_text(encoding="utf-8"))
if opencode.get("mcp") != {} or opencode.get("plugin") != []:
    raise SystemExit("template OpenCode must not enable MCP/plugins")
if opencode.get("permission", {}).get("external_directory") != "deny":
    raise SystemExit("template OpenCode must deny external_directory")

catalog = yaml.safe_load((root / "skills/catalog.yml").read_text(encoding="utf-8"))
catalogued = []
for definition in catalog.get("domains", {}).values():
    if not isinstance(definition, dict) or not isinstance(definition.get("skills"), list):
        raise SystemExit("invalid skill catalog domain")
    catalogued.extend(definition["skills"])
actual = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
if set(catalogued) != actual or len(catalogued) != len(set(catalogued)):
    raise SystemExit("skill catalog coverage mismatch")

print("JSON/YAML public configuration OK")
PY
  ok "JSON/YAML public configuration"
else
  fail "python3 not found; cannot validate public configuration"
fi

BYTECODE="$(find "$ROOT" -path "$ROOT/archive" -prune -o \( -name '*.pyc' -o -name '__pycache__' \) -print)"
if [ -n "$BYTECODE" ]; then
  echo "$BYTECODE"
  fail "generated Python bytecode/cache files found"
else
  ok "no Python bytecode/cache files in public paths"
fi

PRIVATE_MARKERS='azursystech|choushop|178\.156\.212\.10|/home/dmitrii|/home/azur|oleyna80|home-dmitrii'
PRIVATE_HITS="$(grep -RInE \
  --exclude-dir=.git \
  --exclude-dir=archive \
  --exclude-dir=active \
  --exclude-dir=done \
  --exclude-dir=failed \
  --exclude-dir=logs \
  --exclude-dir=parallel \
  --exclude-dir=queue \
  --exclude-dir=runtime \
  --exclude=validate-publication.sh \
  "$PRIVATE_MARKERS" "$ROOT" || true)"
if [ -n "$PRIVATE_HITS" ]; then
  echo "$PRIVATE_HITS"
  fail "private project markers found in public paths"
else
  ok "no known private project markers in public paths"
fi

ABSOLUTE_HOME_MARKERS='/(home|Users)/[A-Za-z0-9._-]+/'
ABSOLUTE_HOME_HITS="$(grep -RInE \
  --exclude-dir=.git \
  --exclude-dir=archive \
  --exclude-dir=active \
  --exclude-dir=done \
  --exclude-dir=failed \
  --exclude-dir=logs \
  --exclude-dir=parallel \
  --exclude-dir=queue \
  --exclude-dir=runtime \
  --exclude=validate-publication.sh \
  "$ABSOLUTE_HOME_MARKERS" "$ROOT" || true)"
if [ -n "$ABSOLUTE_HOME_HITS" ]; then
  echo "$ABSOLUTE_HOME_HITS"
  fail "user-specific absolute home paths found in public paths"
else
  ok "no user-specific absolute home paths in public paths"
fi

for script in \
  "$ROOT/bootstrap.sh" \
  "$ROOT/scripts/test-sdd-contract.sh" \
  "$ROOT/scripts/validate-governance.sh" \
  "$ROOT/scripts/validate-publication.sh" \
  "$ROOT/template/scripts/bootstrap.sh" \
  "$ROOT/template/.claude/hooks/critic-gate.sh" \
  "$ROOT/template/.claude/hooks/hard-stop.sh" \
  "$ROOT/template/.claude/hooks/typecheck.sh" \
  "$ROOT/template/.claude/hooks/verification-gate.sh" \
  "$ROOT/handoff/runner/cleanup.sh" \
  "$ROOT/handoff/runner/handoff-runner.sh" \
  "$ROOT/handoff/runner/install-systemd-user-service.sh" \
  "$ROOT/handoff/runner/parallel-runner.sh" \
  "$ROOT/handoff/runner/sanitize-env.sh" \
  "$ROOT/handoff/runner/watch-queue.sh"; do
  bash -n "$script" || fail "bash syntax failed: $script"
done
ok "bash syntax checks completed"

if command -v python3 >/dev/null 2>&1; then
  python3 - "$ROOT" <<'PY' || fail "Python syntax failed"
from pathlib import Path
import sys

root = Path(sys.argv[1])
paths = [
    root / "scripts/test-codex-adapter.py",
    root / "scripts/test-codex-hard-stops.py",
    root / "scripts/test-integration-contracts.py",
    root / "template/.agent/hooks/hard_stop_policy.py",
    root / "template/.claude/hooks/work_block_gate.py",
    root / "template/.claude/hooks/assurance_gate.py",
    root / "template/.codex/hooks/hard_stop_policy.py",
    root / "template/.codex/hooks/pre_tool_use_policy.py",
    root / "template/.codex/hooks/stage0_write_gate.py",
    root / "template/.codex/hooks/subagent_context.py",
]
for path in paths:
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
print("Python syntax OK")
PY
  ok "Python syntax checks"
fi

python3 "$ROOT/scripts/test-integration-contracts.py" || fail "integration adapter contracts failed"
python3 "$ROOT/scripts/test-codex-adapter.py" || fail "Codex adapter contracts failed"
python3 "$ROOT/scripts/test-codex-hard-stops.py" || fail "Codex Hard Stop fixtures failed"
bash "$ROOT/scripts/test-sdd-contract.sh" || fail "SDLC contract tests failed"
bash "$ROOT/scripts/validate-governance.sh" || fail "governance validation failed"

SMOKE_DIR="${TMPDIR:-/tmp}/agentic-sdlc-framework-smoke-$$"
rm -rf "$SMOKE_DIR"
"$ROOT/bootstrap.sh" "$SMOKE_DIR" "Smoke & Project" "smoke-project"

PLACEHOLDERS="$(grep -RIn '{{' "$SMOKE_DIR" || true)"
if [ -n "$PLACEHOLDERS" ]; then
  echo "$PLACEHOLDERS"
  fail "unresolved placeholders found in smoke project"
else
  ok "smoke project placeholders replaced"
fi

for path in \
  "integrations/README.md" \
  "integrations/mcp/README.md" \
  "runtimes/opencode/README.md" \
  ".agent/hooks/hard_stop_policy.py" \
  ".claude/hooks/work_block_gate.py" \
  ".claude/hooks/assurance_gate.py" \
  "opencode.json" \
  ".opencode/agents/coder.md"; do
  [ -f "$SMOKE_DIR/$path" ] || fail "smoke project missing $path"
done

for path in \
  ".claude/agents/gpt-critic.md" \
  ".claude/agents/gpt-verifier.md" \
  ".claude/agents/codex-reviewer.md"; do
  [ ! -e "$SMOKE_DIR/$path" ] || fail "smoke project contains retired path $path"
done

for pattern in ".agent/" "memory_bank/" ".claude/agent-memory/" ".codex/" ".env"; do
  if grep -qx -- "$pattern" "$SMOKE_DIR/.gitignore"; then
    ok "smoke .gitignore contains standalone line: $pattern"
  else
    fail "smoke .gitignore missing standalone line: $pattern"
  fi
done

rm -rf "$SMOKE_DIR"

if [ "$FAIL" -ne 0 ]; then
  echo "==> Publication validation failed"
  exit 1
fi

echo "==> Publication validation OK"
