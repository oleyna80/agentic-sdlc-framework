#!/usr/bin/env bash
# Validate the runtime-neutral governance core and adapter navigation.
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
  "governance/runtime-capabilities.md" \
  "runtimes/README.md" \
  "runtimes/codex/README.md" \
  "runtimes/claude-code/README.md" \
  "runtimes/opencode/README.md" \
  "runtimes/generic/README.md" \
  "docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md" \
  "docs/plans/wb-001-runtime-neutral-control-plane.md" \
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

for key in ("version", "scope", "architecture", "statuses", "entries"):
    if key not in data:
        raise SystemExit(f"missing top-level key: {key}")

required_entries = {
    "governance/**",
    "governance/authority.md",
    "governance/lifecycle.md",
    "governance/artifacts.md",
    "governance/runtime-capabilities.md",
    "runtimes/**",
    "runtimes/codex/**",
    "runtimes/claude-code/**",
    "runtimes/opencode/**",
    "runtimes/generic/**",
}

entries = set(data["entries"])
missing = sorted(required_entries - entries)
if missing:
    raise SystemExit(f"registry missing entries: {missing}")

print("governance registry YAML OK")
PY
  ok "FILE_REGISTRY.yml governance entries"
else
  fail "python3 not found; cannot validate FILE_REGISTRY.yml"
fi

for path in \
  "governance/README.md" \
  "governance/authority.md" \
  "governance/lifecycle.md" \
  "governance/artifacts.md" \
  "governance/runtime-capabilities.md"; do
  if grep -Eqi "api[_-]?key|access[_-]?token|private[_-]?key|password[[:space:]]*:" "$ROOT/$path"; then
    fail "possible credential material in $path"
  else
    ok "$path has no obvious credential markers"
  fi
done

if [ "$FAIL" -ne 0 ]; then
  echo "==> Governance validation failed"
  exit 1
fi

echo "==> Governance validation: OK"
