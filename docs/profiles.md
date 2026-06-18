# Framework Profiles

Start with the smallest profile that can safely deliver the Work Block. Upgrade
only when the task needs the extra process, tools, or independent review.

Before choosing a profile in a new session, read `PROJECT_MAP.md`,
`FILE_REGISTRY.yml`, and `docs/session-bootstrap.md`. The map and registry
explain the current project structure and authority boundaries; this profile
guide explains how much of the framework to activate for the task.

## Profile Summary

| Profile | Use When | Main Files | Avoid Initially |
|---|---|---|---|
| Level 1 - Minimal Codex-only | One local agent needs scope, logs, review, and verification | `AGENTS.md`, `.codex/`, `memory_bank/`, core skills | Claude Code, MCP, handoff, hooks |
| Level 2 - Standard Codex SDLC | Work needs full Work Blocks, reusable skills, and stronger closeout | Level 1 plus `.agent/`, `docs/`, selected `skills/` | External AI CLI delegation |
| Level 3 - Claude Code Team Runtime | Claude Code should run as its own orchestrator with agents, hooks, memory, and provider config | `CLAUDE.md`, `.claude/`, `.mcp.json`, `.agent/` | Automated handoff until CC works locally |
| Level 4 - Codex -> Claude Code Handoff | Codex should delegate a scoped Work Block to Claude Code as an external team | `handoff/`, handoff task template, `memory_bank/external-team-log.md` | Parallel swarms until single handoff is reliable |
| Advanced overlay - Codex model routing | Strong Codex reasoning should supervise cheaper executor models | User-level Codex profiles, optional custom agents, `framework/workflow/codex-model-routing.md` | Provider config in generated project templates |

## Level 1 - Minimal Codex-only

### Included

```text
AGENTS.md
.codex/write-gate.md
.codex/critic.md
memory_bank/orchestrator-log.md
memory_bank/review-log.md
docs/templates/work-block-template.md
.agent/skills/scoped-coder/
.agent/skills/reviewer/
.agent/skills/verifier/
```

### Expected Flow

```text
Stage 0 preflight -> scoped implementation -> reviewer/critic check ->
verification -> closeout log
```

### Smoke Check

```bash
bash scripts/bootstrap.sh
```

Expected result: `Workflow layer: OK`.

### Upgrade When

- tasks repeatedly need specialized skills;
- the project needs a reusable memory discipline;
- Work Blocks need standard closeout and publication evidence.

## Level 2 - Standard Codex SDLC

### Included

Everything in Level 1, plus:

```text
.agent/ROSTER.md
.agent/workflows/
.agent/skills/
docs/plans/
docs/specs/
docs/reports/
docs/tasklist/
memory_bank/context.md
memory_bank/progress.md
memory_bank/decisions.md
```

### Expected Flow

```text
Plan -> Spec -> Implementation -> Review -> Verification -> Closeout
```

Codex can use its own subagents when available. The Orchestrator still remains
accountable for scope, write-set, critic routing, and final evidence.

### Smoke Check

```bash
git status --short --branch
bash scripts/bootstrap.sh
```

### Upgrade When

- a second agent/runtime should review or implement independently;
- the Work Block benefits from Claude Code's native agents, hooks, or MCP
  integrations.

## Level 3 - Claude Code Team Runtime

### Included

Everything in Level 2, plus:

```text
CLAUDE.md
.claude/settings.json
.claude/agents/
.claude/hooks/
.claude/skills/
.claude/agent-memory/
.mcp.json
```

### Expected Flow

Claude Code acts as its own project-local team. It can run an orchestrator,
subagents, critic/verifier gates, and project-local memory. Agent definitions
use `model: inherit`; provider and model routing come from the active Claude
Code environment.

### Smoke Check

```bash
claude --version
bash scripts/bootstrap.sh
```

Then run a small read-only Claude Code task before allowing state-changing work.

### Upgrade When

- Codex should remain the control tower;
- Claude Code should be called for a scoped Work Block and return a result/log
  through files.

## Level 4 - Codex -> Claude Code Handoff

### Included

Level 2 or Level 3 project files, plus framework-level or project-local:

```text
handoff/README.md
handoff/runner/handoff-runner.sh
handoff/templates/claude-team-task-template.md
handoff/queue/
handoff/active/
handoff/done/
handoff/failed/
handoff/logs/
memory_bank/external-team-log.md
```

### Expected Flow

```text
Codex writes task -> runner starts Claude Code -> Claude Code works as external
team -> result/log written -> Codex reviews result -> closeout
```

### Smoke Check

Use `skills/handoff-live-smoke/SKILL.md` and `handoff/README.md#smoke-task`.

Expected result:

- task reaches `handoff/done/`;
- runner log exists;
- scope audit passes;
- `memory_bank/external-team-log.md` records the external team result.

## Advanced Overlay - Codex Model Routing

This is not a separate runtime level. It is an optional overlay for users who
want strong models only where they add clear value and cheaper models where the
task is bounded execution.

### Recommended Topology

```text
Codex mega-orchestrator
  -> Codex critic for decision review
  -> Claude Code teams for controlled implementation when needed
```

Use Codex for decomposition, architecture decisions, handoff acceptance, and
critic review. Use Claude Code teams for scoped implementation when their hooks,
logs, subagents, and project-local process make execution more controllable.

### Configuration Boundary

The base framework contains templates and policy only. Real provider settings,
API keys, proxy URLs, and local model endpoints belong in the user's runtime
configuration or the target project's private environment.

Do not commit provider credentials, `.env` files, or user-level Codex/Claude
Code runtime config into the framework.

### Suggested Codex Profiles

Keep real config in user-level Codex profiles such as:

```text
~/.codex/strong-review.config.toml
~/.codex/cheap-worker.config.toml
~/.codex/oss-local.config.toml
```

Use the strongest available model for Codex-Orchestrator decisions and Codex
Critic review. Use cheaper or local models only after a smoke task proves they
can handle the intended executor role.

See `framework/workflow/codex-model-routing.md` for the detailed policy.

## Profile Selection Rules

- Run the session bootstrap first; do not select a higher profile from stale
  memory alone.
- Prefer Level 1 for the first real Work Block in a new project.
- Use Level 2 when repeatable SDLC evidence matters.
- Use Level 3 only after Claude Code CLI and provider configuration work in the
  target shell.
- Use Level 4 only after a local Claude Code task has succeeded and the
  handoff runner has passed a smoke task.
- Use Codex model routing only as an overlay. It must not weaken critic,
  verification, write-gate, or secret-handling rules.
- Do not add a higher level because it is available. Add it because the Work
  Block needs independent execution, better observability, or stronger review.

## Publishing Agent State

Generated projects are local-first. If a team wants to publish `.agent/`,
`.codex/`, `.claude/agent-memory/`, or `memory_bank/`, review every file for:

- secrets and provider credentials;
- private client/project context;
- raw transcripts;
- local machine paths;
- generated logs;
- unreviewed agent conclusions.

Publish only reusable governance and evidence that the team deliberately wants
to share.
