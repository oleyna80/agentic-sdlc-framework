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
4. **Integration and Transport Layers** — plugins, MCP, and audited file handoff
   under runtime/integration-specific paths. These are optional execution
   mechanisms, not governance authority.

The accepted decision is:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Authority Order

When sources conflict, use this order:

1. Explicit Owner instruction for the active Work Block.
2. Active workspace `AGENTS.md` and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation plan and write-set.
6. Active task decomposition.
7. Review, verification, drift, and closeout evidence.
8. Durable engineering memory.
9. Operational logs, runtime memory, generated context, and examples.

Runtime-specific settings, hooks, prompts, plugins, model routing, and tools
implement this authority model. They do not override it.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifacts, and capability negotiation |
| `runtimes/` | runtime adapters | Runtime-specific mappings, capability state, limitations, and smoke guidance |
| `docs/architecture/decisions/` | normative decisions | Accepted architectural decisions and review triggers |
| `docs/plans/` | active/log | Work Blocks, implementation plans, and migration evidence |
| `README.md` | normative | Public overview and first entry point |
| `SETUP.md` | normative | Installation and current runtime setup guide |
| `PROJECT_MAP.md` | normative | Human-readable repository navigation |
| `FILE_REGISTRY.yml` | normative | Machine-readable key-file registry |
| `docs/profiles.md` | normative | Governance, runtime, integration, and model profile selection |
| `template/AGENTS.md` | template | Runtime-neutral generated-project operating contract |
| `template/PROJECT_MAP.md` | template | Runtime-neutral generated-project navigation |
| `template/FILE_REGISTRY.yml` | template | Generated-project authority and path registry |
| `template/.agent/ROSTER.md` | template | Logical roles, skills, runtime binding, and isolation |
| `template/.agent/workflows/sdd-protocol.md` | template | Define / Execute / Assure / Close lifecycle |
| `template/.codex/` | runtime compatibility | Current Codex policy, critic, configuration, and write-gate material |
| `template/.claude/` | runtime compatibility | Current Claude Code agents, hooks, skills, settings, and memory |
| `template/docs/engineering-memory/` | template | Durable project-memory starters |
| `skills/` | normative library | Portable skill source and metadata catalog |
| `scripts/test-sdd-contract.sh` | normative test | Portable SDLC contract drift detection |
| `scripts/validate-governance.sh` | normative test | Governance structure validation |
| `.github/workflows/framework-contracts.yml` | CI | Runs shell syntax and framework contract checks |
| `framework/` | reference | Background knowledge, lessons learned, and migration sources |
| `handoff/` | advanced transport | Audited file-based Codex → Claude Code handoff and recovery |
| `examples/` | example | Synthetic scenarios; never mandatory policy |
| `archive/` | local/private | Ignored private material; not public framework content |

## Runtime Adapters

| Runtime | Path | Current status |
|---|---|---|
| Codex | `runtimes/codex/` | Adapter boundary defined; native agents/hooks are WB-003 |
| Claude Code | `runtimes/claude-code/` | Existing implementation retained pending adapter normalization |
| OpenCode | `runtimes/opencode/` | Experimental until target-environment smoke tests pass |
| Generic sequential agent | `runtimes/generic/` | Portable baseline with no native orchestration assumptions |

Model names and provider profiles belong in runtime/user configuration. Logical
roles and authority belong in the governance core.

## Current Migration Work

Completed architecture foundation:

- `docs/plans/wb-001-runtime-neutral-control-plane.md`

Canonical active Work Block:

- `docs/plans/wb-002-runtime-neutral-template-convergence.md`

Compatibility alias only:

- `docs/plans/wb-002-normalize-portable-sdlc-contracts.md`

WB-002 has migrated the generated-project contracts to:

- stable logical roles;
- specification-first SSOT;
- Define / Execute / Assure / Close;
- separate Critic, Reviewer, Verifier, and Specification Drift functions;
- governance/runtime/integration/model separation;
- portable governance and runtime documentation installed by bootstrap;
- structural and disposable-scaffold checks in GitHub Actions.

Remaining planned Work Blocks:

1. WB-003 — Codex-native custom agents and executable write/scope gates.
2. WB-004 — explicit integration adapters for Claude Code plugins, MCP,
   OpenCode, and file handoff.
3. WB-005 — profile-aware bootstrap and cross-runtime conformance tests.

## Generated, Reference, Log, and Local Boundaries

- `governance/**` is normative architecture.
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
3. The active Work Block under `docs/plans/`.
4. Relevant accepted decisions under `docs/architecture/decisions/`.
5. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` when navigation/authority is needed.
6. Relevant runtime adapter only when execution details are needed.
7. Current git state, diff, and target files.
8. Reference knowledge and operational logs only when relevant.

For generated-project work, follow that project's `AGENTS.md`, approved
specification, active Work Block, and progressive session bootstrap.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a top-level directory;
- changes authority, SSOT, lifecycle, review, verification, or closeout rules;
- changes generated/reference/log/local boundaries;
- adds or retires a runtime or integration adapter;
- changes publication requirements or active migration architecture.
