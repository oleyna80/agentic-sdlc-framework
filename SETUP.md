# SETUP.md - Agentic SDLC Framework Setup Guide

For AI agents and human maintainers bootstrapping a new project from this
framework.

## Quick Start

```bash
./bootstrap.sh /path/to/new-project "My Project" my-project
cd /path/to/new-project
```

This copies the template, creates the generated project `.gitignore`, replaces
placeholders, installs core skills into both runtime locations, and verifies the
workflow layer by running `scripts/bootstrap.sh` inside the generated project.
You can rerun `bash scripts/bootstrap.sh` later as a health check after moving
or restoring the workspace.

## Architecture Layers

The scaffold has three separable layers:

1. **Agentic SDLC core**: root `AGENTS.md`, `.agent/`, `skills/`, `docs/`, and
   `memory_bank/`. Codex or another capable agent can run the SDLC directly
   from this layer using its own tools, subagents, rules, and verification.
2. **Codex <-> Claude Code handoff**: framework-level `handoff/` dispatcher for
   cases where Codex delegates a scoped Work Block to Claude Code as an
   independent external team.
3. **Claude Code runtime team**: `.claude/` agents, hooks, settings, MCP
   access, and per-agent memory. This layer is Claude Code-specific and can run
   its own orchestrator/subagent process behind the handoff contract.

## Choose Your Operating Mode

The layers are independent. Start with the smallest mode that matches the
project, then add the others only when the Work Block needs them.

### Mode 1: Codex-only SDLC

Use this when Codex, or another capable agent, should run the SDLC directly.

Read first:

```text
AGENTS.md
.agent/ROSTER.md
.codex/write-gate.md
.codex/critic.md
memory_bank/orchestrator-log.md
memory_bank/review-log.md
```

Expected behavior:

- Stage 0 states expected final result, scope, skills, subagent strategy,
  verification plan, execution log, and retrospective plan.
- Non-trivial decisions are checked by the Codex critic contract when triggers
  match.
- Implementation stays inside the approved write-set.
- Closeout records verification evidence and any process lessons.

### Mode 2: Claude Code team runtime

Use this when Claude Code should manage its own project-local orchestrator,
subagents, hooks, MCP tools, and per-agent memory.

Read first:

```text
CLAUDE.md
.claude/settings.json
.claude/agents/
.claude/hooks/
.claude/skills/
.claude/agent-memory/
```

Expected behavior:

- Claude Code reads `AGENTS.md` before tool use.
- Hooks enforce hard stops, critic gate, verification gate, and typecheck
  behavior where applicable.
- Agents use `model: inherit`; provider/model routing comes from the active
  Claude Code environment.
- Per-agent memory remains project-local unless deliberately published.

### Mode 3: Codex -> Claude Code swarm

Use this when Codex remains the control tower but delegates a scoped Work Block
to Claude Code as an independent external team.

Read first in the framework repository:

```text
handoff/README.md
handoff/templates/claude-team-task-template.md
skills/handoff-live-smoke/SKILL.md
```

Read first in the generated project:

```text
memory_bank/external-team-log.md
```

Expected behavior:

- Codex writes a task file with `project_root`, `allowed_scope`,
  `forbidden_scope`, objective, context, and response contract.
- The handoff runner moves tasks through `queue/`, `active/`, `done/`, or
  `failed/` and writes logs/status files.
- Claude Code works as an external team; Codex observes the delivery result and
  summary log rather than controlling every internal step.
- Scope audit includes ignored local-first paths such as `.agent/` and
  `memory_bank/`.

## Smoke Checks

Run these before trusting a new installation.

### Scaffold health check

```bash
cd /path/to/generated-project
bash scripts/bootstrap.sh
```

Expected result:

```text
Workflow layer: OK
```

Warnings about missing `node_modules/` or `DATABASE_URL` are normal for a fresh
scaffold before project-specific setup.

### Framework publication check

From this repository:

```bash
bash scripts/validate-publication.sh
```

Expected result:

```text
Publication validation OK
```

### Live handoff smoke

Use only when Claude Code CLI and provider environment are configured.

1. Bootstrap a throwaway generated project.
2. From the framework repository, follow `handoff/README.md#smoke-task`.
3. Use the framework `skills/handoff-live-smoke/SKILL.md` as the checklist.
   The generated project also receives a local copy at
   `.agent/skills/handoff-live-smoke/SKILL.md`.

Expected result:

- task moves to `handoff/done/`
- `memory_bank/handoff-smoke.txt` contains `handoff smoke ok`
- `memory_bank/external-team-log.md` receives a concise delivery entry
- runner log exists in `handoff/logs/`
- scope audit does not report forbidden paths

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
orchestrator-log context-snapshot merge-protocol critic-review
codex-verification handoff-live-smoke security-audit-triage
security-verification-gate
```

Install each selected skill into the project-neutral routing layer and any
runtime-specific mirror that should load it:

```bash
for skill in <skill-list>; do
  cp -r skills/$skill /path/to/project/.claude/skills/
  cp -r skills/$skill /path/to/project/.agent/skills/
done
```

`.agent/skills/` is the project-neutral routing mirror used by the SDLC
contract. `.claude/skills/` is the Claude Code runtime path.

### Step 4: Configure Claude Code Runtime Hooks

The template includes Claude Code hooks for projects that enable the `.claude/`
runtime layer:

- `.claude/hooks/hard-stop.sh`: blocks dangerous commands before execution.
- `.claude/hooks/critic-gate.sh`: blocks edits outside the approved Work Block
  write-set until critic review is resolved or explicitly skipped.
- `.claude/hooks/typecheck.sh`: runs TypeScript checks after edits when relevant.

Make scripts executable if you copied files manually:

```bash
chmod +x .claude/hooks/*.sh scripts/*.sh
```

`hard-stop.sh` requires `jq`.

### Step 5: Set Up MCP Servers For Claude Code

The template includes `.mcp.json` with the Codex MCP server configured in
read-only mode for Claude Code GPT critic/verifier agents:

```json
{
  "mcpServers": {
    "codex": {
      "command": "codex",
      "args": ["--sandbox", "read-only", "--ask-for-approval", "never", "mcp-server"]
    }
  }
}
```

Add only the extra servers the project needs:

- `context7`: library documentation lookup
- `sequential-thinking`: complex problem analysis
- `playwright`: browser testing

Never commit MCP tokens or local credentials.

### Optional: Global Claude Code Bootstrap

Use a user-level Claude Code setup when the same workstation should run CC from
many projects with the same provider environment, global agents, and safety
hooks. Keep this separate from project-local scaffold files.

Recommended user files:

```text
~/.config/claude-code/env
~/.claude/settings.json
~/.claude/agents/
~/.claude/agent-memory/
~/.claude/hooks/
~/.claude/skills/
```

Rules:

- Store real provider keys only in `~/.config/claude-code/env` or another
  ignored user-owned env file with mode `600`.
- Source that env file from `~/.bashrc` before the non-interactive shell guard
  if Claude Code may be launched by scripts or editor terminals.
- Copy global agents, hooks, skills, and starter memory from
  `template/.claude/` only after creating backups of existing user files.
- Do not copy `settings.local.json.example` as an active local settings file.
- User-level hook commands must use absolute paths such as
  `bash /home/<user>/.claude/hooks/hard-stop.sh`.
- Project gates such as `critic-gate.sh` and `verification-gate.sh` should
  no-op outside Agentic SDLC projects, then enforce when `.agent/*-gate.md`
  files exist.

Project-local `.claude/settings.json` remains canonical for repository
governance. The global setup is a convenience layer for manual CC use and
cross-project bootstrap.

Detailed checklist:

```text
framework/knowledge/claude-code-global-bootstrap.md
```

### Handoff Runner

`handoff/` is a framework-level orchestration tool for Codex -> Claude Code
delegation. Use it when Codex is the control tower and Claude Code should act
as an independent external delivery team with its own internal orchestrator,
subagents, hooks, and logs.

Root `bootstrap.sh` does not copy `handoff/` into every generated project. Use
it from the framework repository, or copy it deliberately into a project only
when that project should own its own handoff queue, logs, and systemd service.

### Model Strategy

Claude Code agents use `model: inherit` by default. The current framework
expects the active Claude Code runtime/provider configuration to supply the
model, including DeepSeek-backed setups. Multi-model routing inside Claude Code
is deferred until a LiteLLM integration is tested and documented.

Codex keeps its own runtime configuration under `.codex/` when a project needs
project-local Codex overrides. The Codex layer is not secondary to Claude Code;
it is a separate adapter for running the same core SDLC contract.

### Step 6: Initialize Memory

Fill in `memory_bank/context.md` with current project focus.

The generated scaffold also includes:

- `memory_bank/progress.md`
- `memory_bank/decisions.md`
- `.claude/agent-memory/codex-reviewer/MEMORY.md`
- `.claude/agent-memory/critic/MEMORY.md`
- `.claude/agent-memory/gpt-critic/MEMORY.md`
- `.claude/agent-memory/gpt-verifier/MEMORY.md`
- `.claude/agent-memory/reviewer/MEMORY.md`
- `.claude/agent-memory/scoped-coder/MEMORY.md`
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
