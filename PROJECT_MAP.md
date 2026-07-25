# Project Map

This is the first human-authored navigation map for the Agentic SDLC Framework.
It helps humans and agents locate authority, active work, runtime adapters, and
reference material without loading the entire repository.

## Architectural Direction

The framework is a runtime-neutral control plane with four separable layers:

1. **Governance Core** — authority, lifecycle, artifacts, capability
   negotiation, assurance, and closeout under `governance/`.
2. **Runtime Adapters** — Codex, Claude Code, OpenCode, and generic execution
   mappings under `runtimes/`.
3. **Project Scaffold** — generated `AGENTS.md`, `.agent/`, skills, docs, and
   memory conventions under `template/`.
4. **Integration and Transport Layers** — current Claude Code/Codex integration
   material and audited file handoff under `handoff/` and runtime-specific
   paths. These are optional execution mechanisms, not governance authority.

The accepted decision is:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Authority Order

When sources conflict, use this order:

1. Explicit Owner instruction for the active Work Block.
2. Active workspace `AGENTS.md` and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation plan and write set.
6. Active task decomposition.
7. Review, verification, drift, and closeout evidence.
8. Durable engineering memory.
9. Operational logs, runtime memory, generated context, and examples.

Runtime-specific settings, hooks, prompts, plugins, and model routing implement
this authority model. They do not override it.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative target | Runtime-neutral authority, lifecycle, artifacts, and capability negotiation |
| `governance/README.md` | normative target | Entry point for the control plane |
| `runtimes/` | runtime adapters | Runtime-specific mappings, capability state, smoke-test guidance |
| `docs/architecture/decisions/` | normative decisions | Accepted architectural decisions and review triggers |
| `docs/plans/` | active/log | Work Blocks, implementation plans, and migration evidence |
| active workspace `AGENTS.md` | normative project | Operating contract for the active generated project/session |
| `README.md` | normative | Public overview and first entry point |
| `SETUP.md` | normative | Installation and current runtime setup guide |
| `PROJECT_MAP.md` | normative | Human-readable repository navigation |
| `FILE_REGISTRY.yml` | normative | Machine-readable key-file registry |
| `docs/` | mixed | Onboarding, profiles, policy, plans, templates, and reports |
| `template/AGENTS.md` | template | Existing generated-project operating contract pending migration |
| `template/.agent/workflows/sdd-protocol.md` | template | Existing generated-project lifecycle pending normalization |
| `template/.codex/` | runtime compatibility | Current Codex policy, critic, configuration, and write-gate material |
| `template/.claude/` | runtime compatibility | Current Claude Code agents, hooks, skills, settings, and memory |
| `template/docs/engineering-memory/` | template | Durable project-memory starters |
| `skills/` | normative library | Portable skill source and metadata catalog |
| `framework/` | reference | Background knowledge, lessons learned, and migration sources |
| `handoff/` | advanced transport | Audited file-based Codex → Claude Code handoff and recovery |
| `examples/` | example | Synthetic scenarios; never mandatory policy |
| `archive/` | local/private | Ignored private material; not public framework content |

## Runtime Adapters

| Runtime | Path | Current status |
|---|---|---|
| Codex | `runtimes/codex/` | Migration target; current implementation remains in `template/.codex/` |
| Claude Code | `runtimes/claude-code/` | Existing implementation to normalize from `template/.claude/` |
| OpenCode | `runtimes/opencode/` | Experimental until target-environment smoke tests pass |
| Generic sequential agent | `runtimes/generic/` | Baseline with no native orchestration assumptions |

Model names and provider profiles belong in runtime/user configuration. Logical
roles and authority belong in the governance core.

## Current Migration Work

The active architectural Work Block is:
`docs/plans/wb-001-runtime-neutral-control-plane.md`.

This Work Block adds the new target structure while preserving existing
operational paths. Follow-up Work Blocks will:

1. normalize roles, SSOT, lifecycle, Reviewer, Verifier, and drift audit;
2. add Codex-native custom agents and executable gates;
3. reclassify Claude Code, official plugins, MCP, OpenCode, and file handoff as
   adapters/integrations;
4. add profile-aware bootstrap and cross-runtime conformance tests.

## Generated, Reference, Log, and Local Boundaries

- `governance/**` is normative target architecture.
- `runtimes/**` is runtime-specific adapter material and must not redefine core
  authority.
- `docs/architecture/decisions/**` is normative when status is `accepted`.
- `docs/plans/**` records active and historical Work Blocks; only the current
  approved plan controls the active implementation scope.
- `docs/engineering-memory/**` contains durable, evidence-backed project
  knowledge.
- `memory_bank/**` and runtime agent memory are operational state.
- `framework/**` is reference knowledge unless explicitly promoted.
- `examples/**` is illustrative only.
- `handoff/logs/**`, queue status, generated maps, and external reports are
  evidence, not authority.
- `.env*`, credentials, provider tokens, caches, downloaded plugins, build
  output, and machine-local state must not become public content.

## Framework-Repository Read Order

For architectural or governance changes:

1. Active workspace `AGENTS.md`, when present.
2. `governance/README.md` and the relevant governance document.
3. `PROJECT_MAP.md`.
4. `FILE_REGISTRY.yml`.
5. The active Work Block under `docs/plans/`.
6. Relevant accepted decisions under `docs/architecture/decisions/`.
7. Relevant runtime adapter only when execution details are needed.
8. Current git state, diff, and target files.
9. Reference knowledge and operational logs only when relevant.

For work limited to an existing generated-project/runtime implementation, follow
that project's current `AGENTS.md` and compatibility workflow until its template
has been migrated.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a top-level directory;
- changes authority, SSOT, lifecycle, review, verification, or closeout rules;
- changes generated/reference/log/local boundaries;
- adds or retires a runtime or integration adapter;
- changes publication requirements or active migration architecture.
