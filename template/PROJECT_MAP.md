# Project Map

First human-readable map for `{{PROJECT_NAME}}`. It explains authority, the
resolved installation profile, major repository zones, and what an agent should
read next.

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

Runtime, model, integration, or installation-profile selection never changes
governance authority.

## Installation Profile

Read first:

```text
.agent/bootstrap-profile.json
```

It records which runtime implementation surfaces and skills were installed by
bootstrap. It is installation evidence only. It does not grant Work Block
authority, integration admission, credentials, or side-effect permission.

Known profile families are documented in `docs/bootstrap-profiles.md` in the
framework source. A generated project may contain only a subset of these
implementation surfaces:

- `.codex/` for Codex;
- `CLAUDE.md` and `.claude/` for Claude Code;
- `opencode.json` and `.opencode/` for OpenCode;
- `.mcp.json` as an inert MCP configuration surface.

Absence of an unselected runtime surface is expected and must not be repaired by
copying files unless the Owner deliberately changes installation composition.

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

For product behavior, the approved specification is normative. Installation
state, runtime configs, integrations, plans, tasklists, and generated output must
not silently override it.

## Work Block Profiles

Each Work Block selects independently:

- **Governance profile:** Advisory, Controlled, Managed, Assured, Distributed.
- **Runtime profile:** one installed or otherwise approved runtime adapter.
- **Integration profile:** none or an admitted plugin, MCP tool, file handoff,
  hosted connector, direct CLI, or manual exchange.
- **Model class:** strong reasoning, balanced engineering, fast read-only,
  local executor, or project-defined.
- **Isolation:** actual boundary from same context to OS-isolated.

The installation profile constrains local availability; it does not make a
runtime or integration active.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `AGENTS.md` | normative | Compact project operating contract |
| `.agent/bootstrap-profile.json` | generated installation evidence | Resolved profile, components, skills, required path kinds, and forbidden fresh-scaffold paths |
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
| `runtimes/` | adapter documentation | Capability, activation, limitation, and fallback guidance for all supported runtimes |
| `integrations/` | adapter documentation | Optional bridge/tool/transport admission guidance |
| `.codex/` | conditional Codex surface | Present only when selected by installation profile |
| `CLAUDE.md` / `.claude/` | conditional Claude Code surface | Present only when selected by installation profile |
| `opencode.json` / `.opencode/` | conditional OpenCode surface | Present only when selected by installation profile |
| `.mcp.json` | conditional inert integration config | Present only in profiles that install the empty MCP registry |
| `scripts/bootstrap.sh` | health check | Validates the resolved installation profile, blocked default Work Block, and writes project config |
| `scripts/validate-installation-profile.py` | generated validator | Checks required selected surfaces, required path kinds, absent unselected surfaces, and blocked default invariants |
| source/test directories | source | Controlled by approved Work Block write-sets |

## Safe Integration Defaults

Regardless of installation profile:

- no plugin or external runtime bridge is enabled automatically;
- no provider-named authority agent is installed;
- external runtime CLI calls require active Work Block integration approval;
- no handoff watcher or service starts automatically;
- credentials remain local.

When present, `.mcp.json` is empty and OpenCode `mcp`/`plugin` collections are
empty. Before activation, create an admission record from:

`docs/templates/integration-admission-template.md`

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
- `.agent/bootstrap-profile.json` is generated installation evidence;
- engineering memory is durable only when evidence-backed and secret-free;
- `memory_bank/**` and runtime memory are operational/local by default;
- plugins, downloaded packages, provider auth, MCP credentials, handoff runtime
  state, browser sessions, and local IDE state are local;
- `.env*`, tokens, cookies, credentials, keys, live data, and private customer
  context must not be committed.

## New-Session Read Strategy

Always for non-trivial work:

1. `AGENTS.md`;
2. `.agent/bootstrap-profile.json` when runtime availability matters;
3. active Work Block;
4. active specification and revision;
5. relevant architecture decisions;
6. repository status and current diff.

Read conditionally:

- relevant Governance Core contract;
- detailed SDLC protocol and role/skill roster;
- an installed/approved runtime adapter;
- selected integration adapter and admission record;
- relevant skills and engineering memory;
- operational logs when resuming work.

Do not treat an absent unselected runtime surface as corruption.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- changes installation profile composition or generated profile state;
- adds, moves, or removes a major directory;
- changes authority or source-of-truth order;
- changes lifecycle, integration, gate, or role semantics;
- adds or retires a runtime/integration adapter;
- changes normative, derived, evidence, generated, or local boundaries.
