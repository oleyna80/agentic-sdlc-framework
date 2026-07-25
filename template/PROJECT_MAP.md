# Project Map

This file is the first human-readable map for `{{PROJECT_NAME}}`.
It explains authority, major repository zones, and what an agent should read next.

## Purpose

`{{PROJECT_NAME}}` uses a runtime-neutral Agentic SDLC control plane.

The project separates:

1. **Governance core** — authority, lifecycle, artifacts, risk gates, evidence, and closeout.
2. **Portable project workflow** — Work Blocks, specifications, plans, reports, skills, and memory.
3. **Runtime adapters** — Codex, Claude Code, OpenCode, generic agents, plugins, MCP, and handoff mechanisms.
4. **Project implementation** — application source, tests, infrastructure, and documentation.

Runtime or model selection never changes governance authority.

## Authority Order

When project artifacts conflict, resolve in this order:

1. current Owner instruction or approved change request;
2. approved specification;
3. accepted architecture decisions and external contracts;
4. approved implementation plan;
5. active tasklist;
6. `AGENTS.md` and the runtime-neutral governance contract for process/authority questions;
7. review, verification, drift, and closeout reports;
8. durable engineering memory;
9. runtime-specific policy and configuration;
10. operational logs, generated outputs, examples, and external reference material.

For agent behavior and permissions, `AGENTS.md` and `governance/` are normative.
For product behavior, the approved specification is normative.
Plans and tasklists are derived and must not silently override the specification.

## Profiles

Each Work Block selects independently:

- **Governance profile:** Advisory, Controlled, Managed, Assured, or Distributed.
- **Runtime profile:** Codex, Claude Code, OpenCode, generic, or another approved adapter.
- **Integration profile:** none, official plugin, MCP, file-based handoff, or manual handoff.
- **Model class:** strong reasoning, balanced engineering, fast read-only, local executor, or project-defined.
- **Isolation level:** same context through OS-isolated, as actually used.

See `docs/profiles.md` and `runtimes/`.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `AGENTS.md` | normative | Compact project operating contract and entry point. |
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifact, and capability contracts. |
| `.agent/workflows/sdd-protocol.md` | normative | Canonical generated-project stage and gate semantics. |
| `.agent/ROSTER.md` | normative | Logical roles, skill routing, runtime binding, and isolation guidance. |
| `docs/specs/` | normative product/technical | Approved requirements and observable contracts. |
| `docs/architecture/` or accepted decision paths | normative architecture | Accepted architecture constraints and decisions. |
| `docs/plans/` | derived/log | Approved implementation plans and Work Block evidence. |
| `docs/tasklist/` | derived | Active task decomposition derived from specifications and plans. |
| `docs/reports/` | evidence | Critic, review, verification, drift, consolidation, and closeout reports. |
| `docs/engineering-memory/` | durable reference | Evidence-backed decisions, source-of-truth chains, exceptions, and reproducibility. |
| `docs/templates/` | normative templates | Portable Work Block and report contracts. |
| `memory_bank/` | operational/local | Current focus, progress, decisions pending promotion, and agent delivery logs. |
| `runtimes/` | adapter documentation | Capability and fallback guidance for supported runtimes. |
| `.codex/` | runtime-specific | Codex configuration, agents, hooks, and compatibility policy. |
| `.claude/` | runtime-specific | Claude Code agents, hooks, skills, settings, and local memory. |
| `.mcp.json` | integration-specific | Approved MCP server configuration; no secrets. |
| `scripts/` | project-specific | Bootstrap, verification, and automation scripts. |
| source/test directories | project-specific | Implementation controlled by approved Work Block write-sets. |

## Core Lifecycle

```text
Define
  discovery -> architecture -> specification -> plan -> critic

Execute
  scoped implementation -> self-check -> frozen diff

Assure
  independent review -> technical verification -> specification drift audit

Close
  SSOT sync -> engineering memory -> closeout report
```

The lifecycle requires functions, not a fixed number of agents.

## Generated, Derived, and Local Boundaries

- `docs/specs/**` and accepted architecture decisions are normative.
- `docs/plans/**` and `docs/tasklist/**` are derived from approved intent.
- `docs/reports/**` are evidence; they do not silently redefine requirements.
- `docs/engineering-memory/**` is durable and committed only when evidence-backed and secret-free.
- `memory_bank/**` is operational context and may remain local.
- `.claude/agent-memory/**`, runtime caches, provider config, and local IDE state are local by default.
- `.env*`, tokens, credentials, private keys, live data, and private client context must not be committed.
- Generated build/discovery outputs are derived and lower authority than current source and approved contracts.

## New-Session Read Strategy

Use progressive disclosure.

Always for non-trivial work:

1. `AGENTS.md`;
2. active Work Block;
3. active specification and revision;
4. relevant architecture decisions;
5. repository status and current diff.

Read conditionally:

- `governance/*` for authority/lifecycle/artifact questions;
- `.agent/workflows/sdd-protocol.md` for detailed stage semantics;
- `.agent/ROSTER.md` for routing;
- the active runtime adapter;
- relevant skills;
- relevant engineering memory;
- operational logs when resuming interrupted work.

Do not load every registry, skill, runtime document, and memory log by default.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a major directory;
- changes authority or SSOT order;
- changes lifecycle gates or role authority;
- adds or retires a runtime/integration adapter;
- changes normative, derived, evidence, or local-only boundaries;
- changes the generated-project baseline.
