#!/usr/bin/env bash
# bootstrap.sh — Scaffold a new project from the Agentic SDLC Framework.
# Usage: ./bootstrap.sh <target-dir> [project-name] [project-slug]
set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:?Usage: $0 <target-directory> [project-name] [project-slug]}"
PROJECT_NAME="${2:-My Project}"
PROJECT_SLUG="${3:-$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')}"

escape_sed_replacement() {
  printf '%s' "$1" | sed -e 's/[\/&\]/\&/g'
}

PROJECT_NAME_ESC="$(escape_sed_replacement "$PROJECT_NAME")"
PROJECT_SLUG_ESC="$(escape_sed_replacement "$PROJECT_SLUG")"
TARGET_DIR_ESC="$(escape_sed_replacement "$TARGET_DIR")"

if [ -d "$TARGET_DIR" ] && [ "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]; then
  echo "Error: $TARGET_DIR exists and is not empty"
  exit 1
fi

echo "==> Scaffolding project: $PROJECT_NAME ($PROJECT_SLUG)"
echo "    Target: $TARGET_DIR"

# 1. Copy the generated-project template.
echo "==> Copying project template..."
mkdir -p "$TARGET_DIR"
cp -r "$FRAMEWORK_DIR/template/." "$TARGET_DIR/"
if [ -f "$TARGET_DIR/project.gitignore" ]; then
  mv "$TARGET_DIR/project.gitignore" "$TARGET_DIR/.gitignore"
fi

# 2. Install control-plane, runtime, and integration documentation.
# Copy directory contents rather than directory nodes so a future resume-safe
# installer cannot create governance/governance or similar nested paths.
echo "==> Installing governance, runtime, and integration adapters..."
mkdir -p "$TARGET_DIR/governance" "$TARGET_DIR/runtimes" "$TARGET_DIR/integrations"
cp -r "$FRAMEWORK_DIR/governance/." "$TARGET_DIR/governance/"
cp -r "$FRAMEWORK_DIR/runtimes/." "$TARGET_DIR/runtimes/"
cp -r "$FRAMEWORK_DIR/integrations/." "$TARGET_DIR/integrations/"

# 3. Replace project placeholders across the scaffold and copied contracts.
echo "==> Replacing placeholders..."
find "$TARGET_DIR" -type f \( -name "*.md" -o -name "*.json" -o -name "*.sh" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*.py" \) \
  -exec sed -i \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME_ESC/g" \
    -e "s/{{PROJECT_SLUG}}/$PROJECT_SLUG_ESC/g" \
    -e "s/{{PROJECT_ROOT}}/$TARGET_DIR_ESC/g" \
    -e "s/{{SOURCE_DIRS}}/src\/*, app\/*/g" \
    -e "s/{{TECH_STACK}}/to be defined/g" \
    {} +

# 4. Copy the default portable skill baseline.
echo "==> Copying core skills..."
CORE_SKILLS="architecture-discovery technical-discovery task-decomposition project-estimation scoped-coder verifier reviewer spec-drift-audit systematic-debugging webapp-testing memory-bank-manager ssot-sync-closeout subagent-mission-brief agent-operations-review output-skill scoped-commit-guard shell-context-guard orchestrator-log context-snapshot merge-protocol critic-review codex-verification handoff-live-smoke security-audit-triage security-verification-gate"
mkdir -p "$TARGET_DIR/.agent/skills" "$TARGET_DIR/.claude/skills"
for skill in $CORE_SKILLS; do
  if [ -d "$FRAMEWORK_DIR/skills/$skill" ]; then
    cp -r "$FRAMEWORK_DIR/skills/$skill" "$TARGET_DIR/.agent/skills/"
    cp -r "$FRAMEWORK_DIR/skills/$skill" "$TARGET_DIR/.claude/skills/"
  fi
done

# 5. Replace placeholders in installed skills too.
find "$TARGET_DIR/.agent/skills" "$TARGET_DIR/.claude/skills" -name "SKILL.md" -exec sed -i \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME_ESC/g" \
    -e "s/{{PROJECT_SLUG}}/$PROJECT_SLUG_ESC/g" \
    -e "s/{{PROJECT_ROOT}}/$TARGET_DIR_ESC/g" \
    {} + 2>/dev/null || true

# 6. Make runtime hooks and project scripts executable.
chmod +x "$TARGET_DIR/.agent/hooks/"*.py 2>/dev/null || true
chmod +x "$TARGET_DIR/.claude/hooks/"*.sh "$TARGET_DIR/.claude/hooks/"*.py 2>/dev/null || true
chmod +x "$TARGET_DIR/.codex/hooks/"*.py 2>/dev/null || true
chmod +x "$TARGET_DIR/scripts/"*.sh 2>/dev/null || true

# 7. Run generated-project verification.
echo "==> Running bootstrap verification..."
if [ -f "$TARGET_DIR/scripts/bootstrap.sh" ]; then
  bash "$TARGET_DIR/scripts/bootstrap.sh"
fi

echo ""
echo "==> Done! Project scaffolded at $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  cd $TARGET_DIR"
echo "  git init && git add -A && git commit -m 'Initial scaffold from Agentic SDLC Framework'"
echo ""
echo "Then customize:"
echo "  1. Read AGENTS.md and select a governance profile in the first Work Block"
echo "  2. Confirm the active runtime adapter and capability snapshot"
echo "  3. Review source-directory and technology placeholders"
echo "  4. Keep plugins, MCP servers, and external runtimes disabled until admitted"
echo "  5. Review and smoke-test project-local hooks and permission files"
echo "  6. Add project-specific security and verification commands"
echo "  7. Keep operational memory local; promote only durable evidence-backed knowledge"
