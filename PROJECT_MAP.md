# Project Map

Human-readable navigation for the Agentic SDLC Framework. Use it to locate
authority, completed migration work, runtime/integration adapters, and evidence
without loading the full repository.

## Architecture

The framework has four separable layers:

1. **Governance Core** — authority, lifecycle, artifacts, capability
   negotiation, assurance, and closeout under `governance/`.
2. **Runtime Adapters** — Codex, Claude Code, OpenCode, and generic execution
   mappings under `runtimes/` and generated runtime config under `template/`.
3. **Integration Adapters** — official bridges, MCP, and audited file transport
   under `integrations/` and `handoff/`.
4. **Project Artifacts and Evidence** — specifications, decisions, plans, frozen
   diffs, reports, memory promotion, and machine-readable gate state.

Accepted direction:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Authority Order

1. Explicit Owner instruction for the active Work Block.
2. Active workspace `AGENTS.md` and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation plan and write-set.
6. Active task decomposition.
7. Review, verification, drift, integration, and closeout evidence.
8. Durable engineering memory.
9. Operational logs, runtime memory, generated context, integrations, and
   examples.

Runtime settings, hooks, prompts, plugins, MCP servers, models, and tools
implement this model. They do not override it.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifact, and capability contracts |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded mode |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `docs/architecture/decisions/` | normative decisions | Accepted architecture direction and tradeoffs |
| `docs/plans/` | operational/evidence | Active and historical Work Blocks |
| `docs/reports/` | evidence | Critic, review, verification, drift, integration, and closeout reports |
| `README.md` | normative entrypoint | Public architecture and quick start |
| `SETUP.md` | normative setup | Safe runtime/integration activation guidance |
| `PROJECT_MAP.md` | normative navigation | Human-readable map |
| `FILE_REGISTRY.yml` | normative navigation | Machine-readable path/authority registry |
| `docs/profiles.md` | normative selection | Governance, runtime, integration, and model profiles |
| `docs/quickstart-minimal.md` | normative quickstart | Single-runtime, no-integration bounded workflow |
| `docs/mcp-tool-policy.md` | normative integration policy | Tool admission, permission, data, secret, and side-effect boundaries |
| `template/AGENTS.md` | template | Generated-project operating contract |
| `template/.agent/active-work-block.json` | template gate | Source-write, Hard Stop, integration, assurance, and closeout state |
| `template/.agent/hooks/` | shared gate implementation | Provider-neutral consequential-action guards |
| `template/.codex/` | Codex adapter | Custom agents and Codex-specific wrappers/hooks |
| `template/.claude/` | Claude Code adapter | Logical-role agents, machine gates, hooks, skills, and memory |
| `template/opencode.json` | OpenCode adapter | Project instructions and default permissions |
| `template/.opencode/agents/` | OpenCode adapter | Logical-role project subagents |
| `template/.mcp.json` | inert integration config | Empty generated MCP registry |
| `template/docs/templates/integration-admission-template.md` | template | Admission decision for plugins, MCP, runtimes, tools, and transports |
| `skills/` | normative library | Portable skill source and catalog |
| `scripts/test-sdd-contract.sh` | contract test | Portable SDLC and authority drift detection |
| `scripts/test-integration-contracts.py` | contract test | Claude/OpenCode/MCP/handoff static and executable fixtures |
| `scripts/test-integration-admission-evidence.py` | contract test | Rejects external runtime ID without admission evidence |
| `scripts/test-codex-adapter.py` | adapter test | Codex configuration and machine write-gate fixtures |
| `scripts/test-codex-hard-stops.py` | adapter test | Consequential-operation and stale-approval fixtures |
| `scripts/validate-governance.sh` | contract test | Governance structure and registry validation |
| `scripts/validate-publication.sh` | publication test | Public inventory, secrets/private paths, configs, gates, and scaffold smoke |
| `.github/workflows/framework-contracts.yml` | CI evidence | Full contract and disposable-project validation |
| `handoff/` | transport implementation | Current Claude runner plus portable task envelope and scope audit |
| `framework/` | reference | Historical knowledge and migration sources |
| `examples/` | examples | Synthetic scenarios; never mandatory policy |
| `archive/` | local/private | Ignored private material |

## Runtime Adapters

| Runtime | Path | Current status |
|---|---|---|
| Codex | `runtimes/codex/` | Native agents, machine write gate, shared Hard Stops, and explicit integration admission implemented |
| Claude Code | `runtimes/claude-code/` | Logical-role agents, shared machine gate, assurance gate, and opt-in integrations implemented |
| OpenCode | `runtimes/opencode/` | Project config and logical-role subagents implemented; target-environment smoke still required |
| Generic sequential | `runtimes/generic/` | Portable fallback with no native orchestration assumptions |

Model/provider routing remains private runtime configuration. It does not define
role authority.

## Integration Adapters

| Integration | Path | Default state |
|---|---|---|
| Official Claude Code → Codex plugin | `integrations/claude-code-codex-plugin/` | not installed; preferred optional bridge |
| MCP | `integrations/mcp/` | disabled; exact server/tool admission required |
| File handoff | `integrations/file-handoff/` | disabled until configured; portable envelope |
| Existing Claude handoff runner | `handoff/` | compatibility transport; no watcher/service auto-start |
| Direct external runtime CLI | shared Hard Stop + admission record | denied until ID and evidence path are active |

External runtime CLI invocations require an active/fresh Work Block, matching
integration ID, and concrete admission-evidence path. Admission does not grant
child-runtime write authority.

## Migration Work

Completed:

1. `docs/plans/wb-001-runtime-neutral-control-plane.md`
   - control-plane architecture and adapter boundaries.
2. `docs/plans/wb-002-runtime-neutral-template-convergence.md`
   - logical roles, specification-first SSOT, lifecycle, assurance, profiles,
     progressive bootstrap, and contract CI.
3. `docs/plans/wb-003-codex-native-agents-and-gates.md`
   - Codex custom agents, machine gate, layered hooks, tests, and scaffold smoke.
4. `docs/reports/reviews/pr-3-final-review.md`
   - final review of WB-001 through WB-003.
5. `docs/plans/wb-004-integration-adapter-normalization.md`
   - Claude Code plugin/MCP normalization, OpenCode executable baseline,
     provider-neutral shared gates, admission evidence, and portable handoff.
6. `docs/reports/reviews/pr-4-final-review.md`
   - final review of WB-004.

Planned:

7. WB-005 — profile-aware bootstrap and cross-runtime conformance tests.

No implementation Work Block is active after WB-004 closeout.

## Boundaries

- `governance/**` is normative and runtime-neutral.
- `runtimes/**`, `.codex/**`, `.claude/**`, and `.opencode/**` implement runtime
  behavior and cannot redefine authority.
- `integrations/**`, `.mcp.json`, plugins, external runtime CLIs, and `handoff/**`
  are optional mechanisms and require admission/Work Block scope.
- `docs/architecture/decisions/**` is normative when accepted.
- `docs/plans/**` controls implementation only when explicitly active/approved.
- `docs/reports/**` is evidence; it cannot rewrite requirements.
- `docs/engineering-memory/**` is durable evidence-backed knowledge.
- `memory_bank/**` and runtime agent memory are operational state.
- `framework/**` is reference unless deliberately promoted.
- secrets, credentials, provider auth, runtime caches, downloaded plugins,
  handoff runtime state, build output, and machine-local configuration must not
  become public content.

## Framework Read Order

For governance or architecture work:

1. workspace `AGENTS.md`, when present;
2. relevant `governance/` contract;
3. active Work Block, if one exists;
4. accepted architecture decision and specification;
5. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` for navigation;
6. relevant runtime adapter;
7. relevant integration adapter only when required;
8. current Git state, diff, and target files;
9. reference knowledge and operational logs only when relevant.

For generated-project work, follow `AGENTS.md`, the approved specification,
active Work Block, progressive bootstrap, and only the selected runtime/
integration adapters.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds, moves, or removes a major repository zone;
- changes authority, SSOT, lifecycle, assurance, integration, or closeout rules;
- changes generated/reference/evidence/local-state boundaries;
- adds or retires a runtime or integration adapter;
- changes active migration or publication requirements.
