# Project Map

Human-readable navigation for the Agentic SDLC Framework. Use it to locate
authority, installation composition, runtime/integration adapters, active work,
and evidence without loading the full repository.

## Architecture

The framework has four authority/execution layers plus one installation layer:

1. **Governance Core** — authority, lifecycle, artifacts, capability negotiation,
   assurance, and closeout under `governance/`.
2. **Runtime Adapters** — Codex, Claude Code, OpenCode, and generic execution
   mappings under `runtimes/`.
3. **Integration Adapters** — optional bridges, MCP, and audited file transport
   under `integrations/` and `handoff/`.
4. **Project Artifacts and Evidence** — specifications, decisions, plans, frozen
   diffs, reports, memory promotion, and machine-readable Work Block state.
5. **Installation Composition** — `bootstrap/profiles.json` selects which runtime
   implementation surfaces and skills are copied into a generated project.

Installation composition does not grant authority or integration admission.
Accepted architectural direction:
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

Installation profiles, runtime settings, hooks, prompts, plugins, MCP servers,
models, and tools implement or compose this model. They do not override it.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifact, and capability contracts |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded mode |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `bootstrap/profiles.json` | installation manifest | Versioned components, skill sets, aliases, and profile composition |
| `bootstrap/bootstrap_project.py` | scaffold engine | Validates profile before target mutation, prunes runtime surfaces, installs skills, records state |
| `docs/bootstrap-profiles.md` | normative setup | Installation-profile usage, semantics, failure behavior, and extension rules |
| `docs/architecture/decisions/` | normative decisions | Accepted architecture direction and tradeoffs |
| `docs/plans/` | operational/evidence | Active and historical Work Blocks |
| `docs/reports/` | evidence | Critic, review, verification, drift, integration, and closeout reports |
| `README.md` | normative entrypoint | Public architecture and quick start |
| `SETUP.md` | normative setup | Safe scaffold/runtime/integration activation guidance |
| `PROJECT_MAP.md` | normative navigation | Human-readable framework map |
| `FILE_REGISTRY.yml` | normative navigation | Machine-readable path/authority registry |
| `docs/profiles.md` | normative selection | Governance, runtime, integration, model, and installation dimensions |
| `template/AGENTS.md` | template | Generated-project operating contract |
| `template/.agent/active-work-block.json` | template gate | Source-write, Hard Stop, integration, assurance, and closeout state |
| `template/.agent/hooks/` | shared gate implementation | Provider-neutral consequential-action guards |
| `template/scripts/validate-installation-profile.py` | generated validator | Verifies selected and absent unselected scaffold paths, required path kinds, and the blocked default Work Block |
| `template/.codex/` | conditional Codex surface | Custom agents and Codex-specific wrappers/hooks |
| `template/.claude/` | conditional Claude Code surface | Logical-role agents, machine gates, hooks, skills, and memory |
| `template/opencode.json` / `template/.opencode/` | conditional OpenCode surface | Project permissions and logical-role subagents |
| `template/.mcp.json` | conditional inert integration surface | Empty MCP registry installed only by selected profile |
| `skills/` | normative library | Portable skill source and catalog |
| `scripts/test-sdd-contract.sh` | contract test | Portable SDLC, profile, and authority drift detection |
| `scripts/test-bootstrap-profiles.py` | profile test | Exact scaffold matrix, aliases, default, and fail-closed target fixtures |
| `scripts/test-runtime-conformance.py` | adapter conformance | Normalizes logical roles, implementation write authority, gates, and integration defaults |
| `scripts/test-integration-contracts.py` | integration test | Claude/OpenCode/MCP/handoff static and executable fixtures |
| `scripts/test-integration-admission-evidence.py` | integration test | Rejects external runtime ID without admission evidence |
| `scripts/test-codex-adapter.py` | adapter test | Codex configuration and machine write-gate fixtures |
| `scripts/test-codex-hard-stops.py` | adapter test | Consequential-operation and stale-approval fixtures |
| `scripts/validate-publication.sh` | publication wrapper | Routes to catalog-driven public validation |
| `scripts/validate_publication.py` | publication test | Inventory, manifests, configs, conformance, profile smoke, privacy, and syntax |
| `.github/workflows/framework-contracts.yml` | CI evidence | Full contract, profile matrix, conformance, and disposable-project validation |
| `handoff/` | transport implementation | Claude runner compatibility implementation plus portable task envelope |
| `framework/` | reference | Historical knowledge and migration sources |
| `examples/` | examples | Synthetic scenarios; never mandatory policy |
| `archive/` | local/private | Ignored private material |

## Installation Profiles

| Profile | Runtime implementation surfaces | Status |
|---|---|---|
| `core` | none; generic guidance only | smallest portable scaffold |
| `codex` | `.codex/` | Codex-primary baseline |
| `claude-code` | `CLAUDE.md`, `.claude/` | Claude Code-primary baseline |
| `opencode` | `opencode.json`, `.opencode/` | OpenCode baseline; live smoke still required |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | backward-compatible default |

Aliases: `minimal`/`generic` → `core`; `full` → `multi-runtime`.

Every generated project records resolved composition in
`.agent/bootstrap-profile.json`. This state has no authority over Work Blocks.

## Runtime Adapters

| Runtime | Path | Current status |
|---|---|---|
| Codex | `runtimes/codex/` | Native agents, machine write gate, shared Hard Stops, and explicit integration admission implemented |
| Claude Code | `runtimes/claude-code/` | Logical-role agents, shared machine gate, assurance gate, and opt-in integrations implemented |
| OpenCode | `runtimes/opencode/` | Project config and logical-role subagents implemented; read-only shell denies hardened; target smoke required |
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

External runtime invocation admission does not grant child-runtime write
authority.

## Migration Work

Completed:

1. `docs/plans/wb-001-runtime-neutral-control-plane.md`
2. `docs/plans/wb-002-runtime-neutral-template-convergence.md`
3. `docs/plans/wb-003-codex-native-agents-and-gates.md`
4. `docs/reports/reviews/pr-3-final-review.md`
5. `docs/plans/wb-004-integration-adapter-normalization.md`
6. `docs/reports/reviews/pr-4-final-review.md`
7. `docs/plans/wb-005-profile-aware-bootstrap-conformance.md`
8. `docs/reports/reviews/pr-5-final-review.md`
9. `docs/plans/wb-006-bootstrap-restore-hardening.md`
10. `docs/reports/reviews/pr-6-final-review.md`

Active: none.

## Boundaries

- `governance/**` is normative and runtime-neutral.
- `bootstrap/**` controls scaffold composition only; it cannot grant Work Block
  authority, runtime capability, or integration permission.
- `runtimes/**` documents adapters even when their executable surfaces were not
  selected in a generated project.
- `.codex/**`, `.claude/**`, `.opencode/**`, and `opencode.json` implement runtime
  behavior and cannot redefine authority.
- `integrations/**`, `.mcp.json`, plugins, external runtime CLIs, and `handoff/**`
  are optional mechanisms and require admission/Work Block scope.
- `.agent/bootstrap-profile.json` is generated installation evidence.
- `.agent/active-work-block.json` is operational authority/gate state.
- reports are evidence; plans are derived; specifications and accepted decisions
  remain normative.
- secrets, credentials, provider auth, runtime caches, downloaded plugins,
  handoff runtime state, build output, and machine-local configuration must not
  become public content.

## Framework Read Order

For governance or architecture work:

1. workspace `AGENTS.md`, when present;
2. relevant `governance/` contract;
3. active Work Block;
4. accepted architecture decision and specification;
5. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
6. `bootstrap/profiles.json` only when installation composition is relevant;
7. relevant runtime/integration adapter;
8. current Git state, diff, and target files;
9. reference knowledge and operational logs only when relevant.

For generated-project work, read `.agent/bootstrap-profile.json` before assuming
that a runtime implementation surface exists.

## Map Maintenance

Update this file and `FILE_REGISTRY.yml` when a change:

- adds or changes an installation profile/component/alias;
- changes authority, SSOT, lifecycle, assurance, integration, or closeout rules;
- changes generated/reference/evidence/local-state boundaries;
- adds or retires a runtime or integration adapter;
- changes active migration or publication requirements.
