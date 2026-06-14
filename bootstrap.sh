#!/usr/bin/env bash
# bootstrap.sh — Scaffold a new project from the Agentic SDLC Framework.
# Usage: ./bootstrap.sh <target-dir> [project-name] [project-slug]
set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:?Usage: $0 <target-directory> [project-name] [project-slug]}"
PROJECT_NAME="${2:-My Project}"
PROJECT_SLUG="${3:-$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')}"

escape_sed_replacement() {
  printf '%s' "$1" | sed -e 's/[\/&\\]/\\&/g'
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

# 1. Copy template
echo "==> Copying template..."
mkdir -p "$TARGET_DIR"
cp -r "$FRAMEWORK_DIR/template/." "$TARGET_DIR/"
if [ -f "$TARGET_DIR/project.gitignore" ]; then
  mv "$TARGET_DIR/project.gitignore" "$TARGET_DIR/.gitignore"
fi

# 2. Replace placeholders
echo "==> Replacing placeholders..."
find "$TARGET_DIR" -type f \( -name "*.md" -o -name "*.json" -o -name "*.sh" -o -name "*.yaml" -o -name "*.toml" -o -name "*.py" \) \
  -exec sed -i \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME_ESC/g" \
    -e "s/{{PROJECT_SLUG}}/$PROJECT_SLUG_ESC/g" \
    -e "s/{{PROJECT_ROOT}}/$TARGET_DIR_ESC/g" \
    -e "s/{{SOURCE_DIRS}}/src\/*, app\/*/g" \
    -e "s/{{TECH_STACK}}/to be defined/g" \
    {} +

# 3. Copy default skills (Core SDLC)
echo "==> Copying core skills..."
CORE_SKILLS="architecture-discovery technical-discovery task-decomposition project-estimation scoped-coder verifier reviewer systematic-debugging webapp-testing memory-bank-manager ssot-sync-closeout subagent-mission-brief agent-operations-review output-skill scoped-commit-guard shell-context-guard orchestrator-log context-snapshot merge-protocol critic-review codex-verification security-audit-triage security-verification-gate"
mkdir -p "$TARGET_DIR/.agent/skills" "$TARGET_DIR/.claude/skills"
for skill in $CORE_SKILLS; do
  if [ -d "$FRAMEWORK_DIR/skills/$skill" ]; then
    cp -r "$FRAMEWORK_DIR/skills/$skill" "$TARGET_DIR/.agent/skills/"
    cp -r "$FRAMEWORK_DIR/skills/$skill" "$TARGET_DIR/.claude/skills/"
  fi
done

# 4. Replace placeholders in skills too (belt-and-suspenders)
find "$TARGET_DIR/.agent/skills" "$TARGET_DIR/.claude/skills" -name "SKILL.md" -exec sed -i \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME_ESC/g" \
    -e "s/{{PROJECT_SLUG}}/$PROJECT_SLUG_ESC/g" \
    -e "s/{{PROJECT_ROOT}}/$TARGET_DIR_ESC/g" \
    {} + 2>/dev/null || true

# 5. Make hooks executable
chmod +x "$TARGET_DIR/.claude/hooks/"*.sh 2>/dev/null || true
chmod +x "$TARGET_DIR/scripts/"*.sh 2>/dev/null || true

# 6. Run bootstrap verification
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
echo "  1. Review AGENTS.md defaults for source directories and tech stack"
echo "  2. Copy additional skills from framework/skills/ as needed"
echo "  3. Configure MCP servers (.mcp.json)"
echo "  4. Set up project-specific security patterns"
echo "  5. Update memory_bank/context.md with current focus"
