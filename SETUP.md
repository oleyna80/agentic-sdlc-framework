# SETUP.md - Agentic SDLC Framework Setup Guide

For AI agents and human maintainers bootstrapping a new project from this
framework.

## Quick Start

```bash
./bootstrap.sh /path/to/new-project "My Project" my-project
cd /path/to/new-project
bash scripts/bootstrap.sh
```

This copies the template, creates the generated project `.gitignore`, replaces
placeholders, installs core skills into both runtime locations, and verifies the
workflow layer.

## Manual Setup

### Step 1: Copy the Template

```bash
cp -r template/. /path/to/new-project/
mv /path/to/new-project/project.gitignore /path/to/new-project/.gitignore
```

### Step 2: Replace Placeholders

Replace these placeholders in `.md`, `.json`, `.sh`, `.yaml`, `.toml`, and `.py`
files:

| Placeholder | Description | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | Project display name | `My Project` |
| `{{PROJECT_SLUG}}` | Project slug for identifiers | `my-project` |
| `{{PROJECT_ROOT}}` | Filesystem root path | `/home/user/my-project` |
| `{{SOURCE_DIRS}}` | Source code directories | `src/*, app/*` |
| `{{TECH_STACK}}` | Primary technology stack | `Next.js, PostgreSQL, Tailwind` |

### Step 3: Install Core Skills

Core skills:

```text
architecture-discovery technical-discovery task-decomposition project-estimation
scoped-coder verifier reviewer systematic-debugging webapp-testing
memory-bank-manager ssot-sync-closeout subagent-mission-brief
agent-operations-review output-skill scoped-commit-guard shell-context-guard
```

Install each selected skill into both locations:

```bash
for skill in <skill-list>; do
  cp -r skills/$skill /path/to/project/.claude/skills/
  cp -r skills/$skill /path/to/project/.agent/skills/
done
```

`.claude/skills/` is the Claude Code runtime path. `.agent/skills/` is the
project-neutral routing mirror used by the SDLC contract.

### Step 4: Configure Hooks

The template includes:

- `.claude/hooks/hard-stop.sh`: blocks dangerous commands before execution.
- `.claude/hooks/typecheck.sh`: runs TypeScript checks after edits when relevant.

Make scripts executable if you copied files manually:

```bash
chmod +x .claude/hooks/*.sh scripts/*.sh
```

`hard-stop.sh` requires `jq`.

### Step 5: Set Up Optional MCP Servers

Copy `.mcp.json.example` to `.mcp.json` and configure only the servers the
project needs:

- `context7`: library documentation lookup
- `sequential-thinking`: complex problem analysis
- `playwright`: browser testing

Never commit MCP tokens or local credentials.

### Step 6: Initialize Memory

Fill in `memory_bank/context.md` with current project focus.

The generated scaffold also includes:

- `memory_bank/progress.md`
- `memory_bank/decisions.md`
- `.claude/agent-memory/solution-architect/MEMORY.md`
- `.claude/agent-memory/verifier/MEMORY.md`

Keep memory evidence-backed and project-local unless the Owner explicitly
approves publishing it.

### Step 7: Verify

```bash
bash scripts/bootstrap.sh
```

Expected result: every required workflow file prints `OK`, followed by
`Workflow layer: OK`.

## Project Types

### Fullstack SaaS

Use all core skills, add design skills for UI work, add security skills for
auth/payment/webhook flows, and enable Playwright MCP for browser verification.

### Backend API Service

Use core SDLC skills plus security audit and hardening skills. The TypeScript
hook is optional unless the service includes TypeScript.

### Static Site or Landing Page

Use scoped coding, verification, output, shell guard, closeout, and design
skills. Add Playwright MCP for responsive and visual checks.

### Open Source Library

Use core coding, review, debugging, output, commit guard, shell guard, and
tooling skills. Keep the generated local memory private unless intentionally
publishing governance docs.

## Local vs Team-Published Mode

Generated projects are local-first:

- `.agent/`
- `.codex/`
- `memory_bank/`
- `.claude/agent-memory/`

are ignored by the generated `.gitignore`.

For a team-published workflow, edit the generated `.gitignore` deliberately and
review each file for secrets, private decisions, credentials, and environment
data before committing.

## Troubleshooting

| Problem | Solution |
|---|---|
| `scripts/bootstrap.sh` fails | Check missing files output and copy the missing scaffold path from `template/`. |
| Placeholder not replaced | Run `grep -R "{{" .` in the generated project. |
| Hook not triggering | Verify `.claude/settings.json` and executable hook permissions. |
| Hard-stop hook fails | Install `jq` and rerun the command. |
| Skill not matched | Check `.agent/ROSTER.md` and `SKILL.md` trigger sections. |
| Claude skill unavailable | Ensure the skill exists under `.claude/skills/<name>/`. |
| MCP server unavailable | Verify `npx` can run the package and `.mcp.json` is valid JSON. |
