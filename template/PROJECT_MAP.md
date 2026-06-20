# Project Map

This file is the first human-authored map for `{{PROJECT_NAME}}`. It helps
humans and agents orient before reading the full project.

## Purpose

`{{PROJECT_NAME}}` uses the Agentic SDLC scaffold to run scoped Work Blocks with
explicit roles, approved write-sets, review, verification, and durable logs.

## Authority Model

When files conflict, use this order:

1. Explicit Owner instruction for the current task.
2. `AGENTS.md` in this project.
3. Approved Work Block plan and write-set.
4. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`.
5. Runtime-specific policy files such as `.codex/critic.md`,
   `.codex/write-gate.md`, `.claude/settings.json`, hooks, and agent prompts.
6. Reference docs, examples, logs, and generated/discovery artifacts.

Generated or discovery artifacts may help locate information, but they do not
override normative instructions, Owner decisions, or approved scope.

## Operating Modes

Start with the smallest mode that can safely deliver the Work Block:

- **Minimal Codex-only**: one local agent, scope control, logs, review,
  verification, no Claude Code, no MCP, no handoff.
- **Standard Codex SDLC**: full Work Block flow with reusable skills and
  stronger closeout evidence.
- **Claude Code Team Runtime**: Claude Code acts as its own local team with
  agents, hooks, skills, memory, and provider configuration.
- **Codex -> Claude Code Handoff**: Codex delegates scoped work to Claude Code
  as an external team through file-based handoff.
- **Codex model routing overlay**: optional user-level Codex profiles keep
  strong models on orchestration/critic decisions and cheaper or local models
  on bounded executor tasks. Real provider settings stay outside the generated
  project unless the team deliberately adds private local config.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `AGENTS.md` | normative | Root operating rules for agents in this project. |
| `PROJECT_MAP.md` | normative | Human-readable project map. |
| `FILE_REGISTRY.yml` | normative | Machine-readable key file/path registry. |
| `.codex/` | normative runtime | Codex write gate, critic contract, and hooks. |
| `.agent/` | normative routing | Runtime-neutral roster, workflows, gates, and skills. |
| `.agent/workflows/sdd-protocol.md` | normative | Canonical lifecycle contract and stage semantics. |
| `.claude/` | runtime-specific | Claude Code agents, hooks, skills, settings, and memory. |
| `memory_bank/` | mixed | Durable project context, decisions, logs, and external team reports. |
| `docs/` | mixed | Plans, specs, tasklists, reports, templates, and references. |
| `docs/templates/{verification-report,closeout-report}-template.md` | normative | Verification evidence and success/reporting-only closeout contracts. |
| `scripts/` | project-specific | Bootstrap and project automation scripts. |
| source directories | project-specific | Application or service code. See `AGENTS.md`. |

## Generated, Log, and Local-Only Boundaries

- `docs/plans/**` and `docs/reports/**` are Work Block evidence and reports;
  the current approved plan matters more than older plans.
- `docs/templates/**` are reusable coordination and Work Block templates.
- `memory_bank/orchestrator-log.md`, `memory_bank/review-log.md`, and
  `memory_bank/external-team-log.md` are evidence logs, not current authority.
- `.claude/agent-memory/**` is project-local agent memory unless deliberately
  reviewed for publication.
- `.env*`, credentials, provider tokens, caches, build output, and local
  machine state must not be committed.
- Future graph/discovery outputs should be treated as derived context only.

## New-Session Bootstrap

For project work, read in this order:

1. `AGENTS.md`
2. `PROJECT_MAP.md`
3. `FILE_REGISTRY.yml`
4. `docs/session-bootstrap.md`
5. The current task or Work Block plan
6. `git status --short --branch`
7. Relevant diffs and target files

Do not assume memory from a previous session is current when repository files
are cheap to verify.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a major directory;
- changes authority, write gates, review gates, or verification gates;
- changes generated/local-only boundaries;
- adds a new runtime layer, profile, or project-specific governance rule.
