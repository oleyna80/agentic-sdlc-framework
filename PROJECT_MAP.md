# Project Map

This is the first human-authored navigation map for the Agentic SDLC Framework.
It helps humans and agents locate authority, completed migration work, runtime
adapters, and reference material without loading the entire repository.

## Architectural Direction

The framework is a runtime-neutral control plane with four separable layers:

1. **Governance Core** — authority, lifecycle, artifacts, capability
   negotiation, assurance, and closeout under `governance/`.
2. **Runtime Adapters** — Codex, Claude Code, OpenCode, and generic execution
   mappings under `runtimes/`.
3. **Project Scaffold** — generated `AGENTS.md`, `.agent/`, skills, docs, and
   memory conventions under `template/`.
4. **Integration and Transport Layers** — plugins, MCP, and audited file handoff.
   These are optional execution mechanisms, not governance authority.

Accepted architecture decision:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Authority Order

1. Explicit Owner instruction for the active Work Block.
2. Active workspace `AGENTS.md` and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation plan and write-set.
6. Active task decomposition.
7. Review, verification, drift, and closeout evidence.
8. Durable engineering memory.
9. Operational logs, runtime memory, generated context, and examples.

Runtime settings, hooks, prompts, plugins, model routing, and tools implement this
model. They do not override it.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifacts, and capability negotiation |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded-mode guidance |
| `docs/architecture/decisions/` | normative decisions | Accepted architecture decisions and review triggers |
| `docs/plans/` | evidence/log | Work Blocks and migration closeout evidence |
| `README.md` | normative | Public overview and first entry point |
| `SETUP.md` | normative | Installation and runtime setup guide |
| `PROJECT_MAP.md` | normative | Human-readable repository navigation |
| `FILE_REGISTRY.yml` | normative | Machine-readable authority/path registry |
| `docs/profiles.md` | normative | Governance, runtime, integration, and model profile selection |
| `template/AGENTS.md` | template | Runtime-neutral generated-project operating contract |
| `template/.agent/workflows/sdd-protocol.md` | template | Define / Execute / Assure / Close lifecycle |
| `template/.agent/active-work-block.json` | template gate | Executable, fail-closed Work Block state for supporting runtimes |
| `template/.codex/` | Codex adapter | Custom agents, config, hooks, compatibility guidance, and write guardrails |
| `template/.claude/` | Claude Code adapter | Existing agents, hooks, skills, settings, and memory pending WB-004 normalization |
| `skills/` | normative library | Portable skill source and metadata catalog |
| `scripts/test-sdd-contract.sh` | contract test | Portable SDLC drift detection |
| `scripts/test-codex-adapter.py` | adapter test | Codex TOML/JSON parsing and executable gate fixtures |
| `scripts/validate-governance.sh` | contract test | Governance structure validation |
| `.github/workflows/framework-contracts.yml` | CI evidence | Contract, publication, adapter, and disposable-scaffold checks |
| `handoff/` | integration adapter | Audited file-based cross-runtime handoff and recovery |
| `framework/` | reference | Background knowledge and migration sources |
| `examples/` | example | Synthetic scenarios; never mandatory policy |
| `archive/` | local/private | Ignored private material |

## Runtime Adapters

| Runtime | Path | Current status |
|---|---|---|
| Codex | `runtimes/codex/` | Native custom-agent and executable-gate baseline implemented and CI-validated |
| Claude Code | `runtimes/claude-code/` | Existing implementation retained pending explicit adapter/integration normalization |
| OpenCode | `runtimes/opencode/` | Experimental until target-environment smoke tests pass |
| Generic sequential agent | `runtimes/generic/` | Portable fallback with no native orchestration assumptions |

Model names and provider profiles belong in runtime/user configuration. Logical
roles and authority belong in the Governance Core.

## Migration Work

Completed:

1. `docs/plans/wb-001-runtime-neutral-control-plane.md`
   - runtime-neutral control-plane architecture and adapter boundaries.
2. `docs/plans/wb-002-runtime-neutral-template-convergence.md`
   - logical roles, specification-first SSOT, portable lifecycle, Review,
     Verification, Drift, profiles, progressive bootstrap, and contract CI.
3. `docs/plans/wb-003-codex-native-agents-and-gates.md`
   - Codex custom agents, machine-readable Work Block gate, `PreToolUse`,
     `SubagentStart`, fixture tests, and generated-project smoke validation.

Compatibility alias:

- `docs/plans/wb-002-normalize-portable-sdlc-contracts.md`

Planned as separate review scopes:

1. WB-004 — normalize Claude Code plugins, MCP, OpenCode, and file handoff as
   explicit integration adapters.
2. WB-005 — profile-aware bootstrap and cross-runtime conformance tests.

There is no active implementation Work Block after WB-003 closeout. The current
PR remains draft for human review of the combined WB-001 through WB-003 release.

## Boundaries

- `governance/**` is normative architecture.
- `runtimes/**`, `.codex/**`, and `.claude/**` implement runtime behavior and
  cannot redefine core authority.
- `docs/architecture/decisions/**` is normative when accepted.
- `docs/plans/**` records current or historical Work Blocks; only an explicitly
  active approved plan controls implementation scope.
- `docs/engineering-memory/**` contains durable evidence-backed knowledge.
- `memory_bank/**` and runtime agent memory are operational state.
- `framework/**` is reference unless deliberately promoted.
- handoff queues/logs, external reports, and generated maps are evidence, not
  authority.
- secrets, credentials, provider tokens, caches, downloaded plugins, build
  output, and machine-local state must not become public content.

## Framework Read Order

For governance or architecture work:

1. Active workspace `AGENTS.md`, when present.
2. Relevant `governance/` document.
3. Active Work Block, if one exists.
4. Relevant accepted architecture decision.
5. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` when navigation is needed.
6. Relevant runtime adapter only for execution mechanics.
7. Current git state, diff, and target files.
8. Reference knowledge and operational logs only when relevant.

For generated-project work, follow its `AGENTS.md`, approved specification,
active Work Block, and progressive session bootstrap.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a major repository zone;
- changes authority, SSOT, lifecycle, assurance, or closeout rules;
- changes generated/reference/log/local boundaries;
- adds or retires a runtime or integration adapter;
- changes active migration state or publication requirements.
