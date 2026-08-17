#!/usr/bin/env bash
# Validate the runtime-neutral governance core, Define quality, adapters,
# release-state SSOT, and dependency-free compatibility fixtures owned by
# framework governance.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0

ok() {
  echo "OK: $*"
}

fail() {
  echo "FAIL: $*"
  FAIL=1
}

require_file() {
  local path="$1"
  if [ -f "$ROOT/$path" ]; then
    ok "$path"
  else
    fail "missing $path"
  fi
}

for path in \
  "governance/README.md" \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/define-quality.md" \
  "governance/evaluation.md" \
  "governance/release-state.md" \
  "governance/runtime-capabilities.md" \
  "runtimes/README.md" \
  "runtimes/codex/README.md" \
  "runtimes/claude-code/README.md" \
  "runtimes/opencode/README.md" \
  "runtimes/generic/README.md" \
  "docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md" \
  "docs/plans/wb-001-runtime-neutral-control-plane.md" \
  "docs/plans/wb-007-agent-evaluation-trajectory-assurance.md" \
  "docs/plans/wb-008-post-merge-ssot-release-gate.md" \
  "scripts/validate-define-traceability.py" \
  "scripts/test-define-traceability.py" \
  "scripts/validate-release-state.py" \
  "scripts/test-release-state-contracts.py" \
  "skills/impeccable/scripts/design-parser.mjs" \
  "skills/impeccable/scripts/test-design-parser.mjs" \
  "README.md" \
  "PROJECT_MAP.md" \
  "FILE_REGISTRY.yml"; do
  require_file "$path"
done

for path in \
  "README.md" \
  "PROJECT_MAP.md" \
  "FILE_REGISTRY.yml"; do
  if grep -q "governance/" "$ROOT/$path" && grep -q "runtimes/" "$ROOT/$path"; then
    ok "$path references governance and runtimes"
  else
    fail "$path must reference governance/ and runtimes/"
  fi
done

if command -v python3 >/dev/null 2>&1; then
  python3 - "$ROOT/FILE_REGISTRY.yml" <<'PY' || fail "FILE_REGISTRY.yml validation failed"
import pathlib
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required") from exc

path = pathlib.Path(sys.argv[1])
data = yaml.safe_load(path.read_text(encoding="utf-8"))

if not isinstance(data, dict):
    raise SystemExit("registry must parse to a mapping")

for key in (
    "version",
    "scope",
    "architecture",
    "statuses",
    "define_quality",
    "migration_state",
    "release_state",
    "entries",
):
    if key not in data:
        raise SystemExit(f"missing top-level key: {key}")

required_entries = {
    "governance/**",
    "governance/authority.md",
    "governance/lifecycle.md",
    "governance/artifacts.md",
    "governance/define-quality.md",
    "governance/evaluation.md",
    "governance/release-state.md",
    "governance/runtime-capabilities.md",
    "runtimes/**",
    "runtimes/codex/**",
    "runtimes/claude-code/**",
    "runtimes/opencode/**",
    "runtimes/generic/**",
    "scripts/validate-define-traceability.py",
    "scripts/test-define-traceability.py",
    "scripts/validate-release-state.py",
    "scripts/test-release-state-contracts.py",
    "template/scripts/validate-define-traceability.py",
    "template/scripts/validate-evaluation.py",
    "template/docs/templates/requirements-quality-review-template.md",
    "template/docs/templates/traceable-tasklist-template.md",
}

entries = set(data["entries"])
missing = sorted(required_entries - entries)
if missing:
    raise SystemExit(f"registry missing entries: {missing}")

print("governance registry YAML OK")
PY
  ok "FILE_REGISTRY.yml governance/Define/evaluation/release-state entries"
  python3 "$ROOT/scripts/test-define-traceability.py" || fail "Define traceability fixtures failed"
  python3 "$ROOT/scripts/validate-release-state.py" --root "$ROOT" || fail "release-state validation failed"
  python3 "$ROOT/scripts/test-release-state-contracts.py" || fail "release-state fixtures failed"
else
  fail "python3 not found; cannot validate FILE_REGISTRY.yml and Define fixtures"
fi

if command -v node >/dev/null 2>&1; then
  node --check "$ROOT/skills/impeccable/scripts/design-parser.mjs" || fail "Impeccable DESIGN.md parser syntax failed"
  node --check "$ROOT/skills/impeccable/scripts/test-design-parser.mjs" || fail "Impeccable DESIGN.md parser fixture syntax failed"
  node "$ROOT/skills/impeccable/scripts/test-design-parser.mjs" || fail "Impeccable DESIGN.md parser compatibility failed"
  if [ "$FAIL" -eq 0 ]; then
    ok "Impeccable DESIGN.md parser compatibility"
  fi
else
  fail "node not found; cannot validate Impeccable DESIGN.md parser compatibility"
fi

for path in \
  "governance/README.md" \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/define-quality.md" \
  "governance/evaluation.md" \
  "governance/release-state.md" \
  "governance/runtime-capabilities.md"; do
  if grep -Eqi "api[_-]?key|access[_-]?token|private[_-]?key|password[[:space:]]*:" "$ROOT/$path"; then
    fail "possible credential material in $path"
  else
    ok "$path has no obvious credential markers"
  fi
done

if ! grep -q "private chain-of-thought" "$ROOT/governance/evaluation.md"; then
  fail "evaluation governance must explicitly exclude private chain-of-thought"
else
  ok "evaluation governance excludes private chain-of-thought"
fi

if ! grep -q "requirements-quality review" "$ROOT/governance/define-quality.md" || \
   ! grep -q "validate-define-traceability.py" "$ROOT/governance/define-quality.md"; then
  fail "Define quality governance must define requirements review and structural traceability"
else
  ok "Define quality governance defines requirements review and traceability"
fi

if ! grep -q "does not grant source-write authority" "$ROOT/governance/define-quality.md"; then
  fail "Define quality governance must keep source-write authority separate"
else
  ok "Define quality governance keeps source-write authority separate"
fi

if ! grep -q "mutable external operational metadata" "$ROOT/governance/release-state.md"; then
  fail "release-state governance must define the external GitHub-state boundary"
else
  ok "release-state governance defines external GitHub-state boundary"
fi

if [ "$FAIL" -ne 0 ]; then
  echo "==> Governance validation failed"
  exit 1
fi

echo "==> Governance validation: OK"
