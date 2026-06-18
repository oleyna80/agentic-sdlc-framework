# Project Map

This file is the first human-authored map for the Agentic SDLC Framework
repository. It helps humans and agents orient before reading the full project.

## Purpose

This repository provides a project-agnostic Agentic SDLC scaffold with three
separable layers:

1. **Core SDLC layer**: runtime-neutral process, authority model, skills,
   memory bank conventions, Work Blocks, review, and verification.
2. **Inter-agent handoff layer**: file-based Codex -> Claude Code delegation
   with runner scripts, queue directories, logs, and scope audit.
3. **Claude Code team runtime layer**: Claude Code-specific agents, hooks,
   skills, and per-agent memory for teams that choose that runtime.

## Authority Model

When files conflict, use this order:

1. Explicit Owner instruction for the current task.
2. Active workspace `AGENTS.md` when present.
3. Approved Work Block plan and write-set.
4. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`.
5. Runtime-specific policy files such as `.codex/critic.md`,
   `.codex/write-gate.md`, `.claude/settings.json`, hooks, and agent prompts.
6. Reference docs, examples, logs, and generated/discovery artifacts.

Generated or discovery artifacts may help locate information, but they do not
override normative instructions, Owner decisions, or approved scope.

## Operating Modes

Use `docs/profiles.md` to choose the smallest sufficient mode:

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
  on bounded executor tasks. It does not change the authority model.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| active workspace `AGENTS.md` | normative | Operating rules for the current agent session when present. |
| `README.md` | normative | Public overview and first entry point. |
| `SETUP.md` | normative | Installation and runtime mode setup guide. |
| `PROJECT_MAP.md` | normative | Human-readable repository map. |
| `FILE_REGISTRY.yml` | normative | Machine-readable key file/path registry. |
| `docs/` | mixed | Onboarding, profiles, policies, plans, templates, and session bootstrap. |
| `template/AGENTS.md` | normative template | Primary generated-project operating contract. |
| `template/` | normative template | Files copied into generated projects. |
| `skills/` | normative library | Portable skill library copied into generated projects. |
| `framework/` | reference | Background knowledge and lessons learned. |
| `handoff/` | normative runtime | Handoff runner, queues, templates, and logs policy. |
| `examples/` | example | Synthetic scenario guides, not mandatory process. |
| `archive/` | local/private | Ignored material; not part of public publication. |

## Generated, Log, and Local-Only Boundaries

- `examples/**` are examples, not policy.
- `docs/templates/**` are reusable framework coordination templates.
- `docs/plans/**` are Work Block evidence and plans; the current approved plan
  matters more than older plans.
- `handoff/logs/**`, `handoff/done/**`, `handoff/failed/**`, and runtime status
  files are operational evidence, not authority.
- `archive/**`, `.env*`, credentials, provider tokens, caches, build output,
  and local machine state must not become public framework content.
- Future graph/discovery outputs such as `graphify-out/**` should be treated as
  derived context only.

## New-Session Bootstrap

For framework repository work, read in this order:

1. Active workspace `AGENTS.md` when present
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

- adds, moves, or removes a top-level directory;
- changes authority, write gates, review gates, or verification gates;
- changes generated/local-only boundaries;
- adds a new runtime layer, profile, or publication requirement.
