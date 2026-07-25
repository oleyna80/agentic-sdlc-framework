# Project Map

First human-readable map for `{{PROJECT_NAME}}`. It explains authority, major
repository zones, and what an agent should read next.

## Architecture

`{{PROJECT_NAME}}` uses a runtime-neutral Agentic SDLC control plane with four
separable layers:

1. **Governance Core** — authority, lifecycle, artifacts, risk gates, evidence,
   capability negotiation, and closeout.
2. **Portable workflow** — specifications, architecture decisions, Work Blocks,
   plans, tasks, reports, skills, and memory.
3. **Runtime adapters** — Codex, Claude Code, OpenCode, generic, or another
   approved execution runtime.
4. **Integration adapters** — optional plugins, MCP servers, external runtime
   CLIs, hosted tools, and audited file transport.

Runtime, model, or integration selection never changes governance authority.

## Authority Order

When artifacts conflict:

1. current Owner instruction or approved change request;
2. `AGENTS.md` and Governance Core for authority/process questions;
3. approved specification and acceptance criteria;
4. accepted architecture decisions and external contracts;
5. approved implementation plan and write-set;
6. active tasklist;
7. review, verification, drift, integration, and closeout evidence;
8. durable engineering memory;
9. runtime/integration policy, operational logs, generated output, and external
   reference material.

For product behavior, the approved specification is normative. Plans, tasklists,
runtime configs, integrations, and generated output must not silently override
it.

## Profiles

Each Work Block selects independently:

- **Governance profile:** Advisory, Controlled, Managed, Assured, Distributed.
- **Runtime profile:** Codex, Claude Code, OpenCode, generic, or another adapter.
- **Integration profile:** none, admitted official plugin, MCP, file handoff,
  hosted connector, direct CLI, or manual exchange.
- **Model class:** strong reasoning, balanced engineering, fast read-only,
  local executor, or project-defined.
- **Isolation:** actual boundary from same context to OS-isolated.

See `docs/profiles.md`, `runtimes/`, and `integrations/`.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `AGENTS.md` | normative | Compact project operating contract |
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifact, and capability contracts |
| `.agent/workflows/sdd-protocol.md` | normative | Define / Execute / Assure / Close semantics |
| `.agent/ROSTER.md` | normative | Logical roles, skill routing, runtime binding, isolation |
| `.agent/active-work-block.json` | operational gate | Specification, Git baseline, write-set, Hard Stops, integrations, assurance, closeout |
| `.agent/hooks/` | shared runtime policy | Provider-neutral consequential-action guards |
| `docs/specs/` | normative | Approved product and technical behavior |
| `docs/architecture/` | normative | Accepted architecture decisions and contracts |
| `docs/plans/` | derived/log | Approved plans and Work Blocks |
| `docs/tasklist/` | derived | Active task decomposition |
| `docs/reports/` | evidence | Critic, review, verification, drift, integration, and closeout evidence |
| `docs/engineering-memory/` | durable reference | Evidence-backed reusable decisions and reproducibility |
| `docs/templates/` | normative templates | Work Block, reports, and integration admission |
| `memory_bank/` | operational/local | Current focus, progress, pending decisions, runtime/team logs |
| `runtimes/` | runtime adapters | Capability, activation, limitation, and fallback guidance |
| `integrations/` | integration adapters | Optional bridge/tool/transport admission guidance |
| `.codex/` | Codex adapter | Project agents, config, hooks, and wrappers |
| `CLAUDE.md` / `.claude/` | Claude Code adapter | Runtime entry point, logical agents, hooks, skills, memory |
| `opencode.json` / `.opencode/` | OpenCode adapter | Instructions, permissions, and logical-role subagents |
| `.mcp.json` | inert integration config | Empty until an MCP server is admitted |
| `scripts/` | project-specific | Bootstrap, verification, and automation |
| source/test directories | source | Controlled by approved Work Block write-sets |

## Safe Integration Defaults

Generated projects start with:

- empty `.mcp.json`;
- no enabled plugin or external runtime bridge;
- empty OpenCode `mcp` and `plugin` collections;
- no provider-named authority agents;
- denied secret paths and external-directory access where supported;
- external runtime CLI calls requiring active Work Block integration approval;
- no handoff watcher or service auto-start.

Before activation, create:

`docs/templates/integration-admission-template.md`

The admission record identifies capabilities, exact tools, authority, data and
secret boundaries, side effects, Hard Stops, evidence, version, failure/recovery,
and disable procedure.

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

The lifecycle requires functions, not a fixed number of agents. Runtime-specific
agent names and integrations are bindings to these functions.

## Generated, Derived, and Local Boundaries

- specifications and accepted architecture decisions are normative;
- plans and tasklists are derived;
- reports are evidence, not requirement authority;
- engineering memory is durable only when evidence-backed and secret-free;
- `memory_bank/**` and runtime memory are operational/local by default;
- plugins, downloaded packages, provider auth, MCP credentials, handoff runtime
  state, browser sessions, and local IDE state are local;
- `.env*`, tokens, cookies, credentials, keys, live data, and private customer
  context must not be committed;
- generated build/discovery output has lower authority than current source and
  approved contracts.

## New-Session Read Strategy

Always for non-trivial work:

1. `AGENTS.md`;
2. active Work Block;
3. active specification and revision;
4. relevant architecture decisions;
5. repository status and current diff.

Read conditionally:

- relevant Governance Core contract;
- detailed SDLC protocol and role/skill roster;
- selected runtime adapter;
- selected integration adapter and admission record;
- relevant skills and engineering memory;
- operational logs when resuming work.

Do not load every registry, skill, runtime, integration, and memory file by
default.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a major directory;
- changes authority or source-of-truth order;
- changes lifecycle, integration, gate, or role semantics;
- adds or retires a runtime/integration adapter;
- changes normative, derived, evidence, generated, or local boundaries;
- changes the generated-project baseline.
