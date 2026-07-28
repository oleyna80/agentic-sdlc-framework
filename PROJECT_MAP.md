# Project Map

Human-readable navigation for the Agentic SDLC Framework. Use it to locate
authority, installation composition, runtime/integration adapters, active work,
and evidence without loading the full repository.

<!-- release-state
completed_work_blocks:
  - docs/plans/wb-001-runtime-neutral-control-plane.md
  - docs/plans/wb-002-runtime-neutral-template-convergence.md
  - docs/plans/wb-003-codex-native-agents-and-gates.md
  - docs/plans/wb-004-integration-adapter-normalization.md
  - docs/plans/wb-005-profile-aware-bootstrap-conformance.md
  - docs/plans/wb-006-bootstrap-restore-hardening.md
  - docs/plans/wb-007-agent-evaluation-trajectory-assurance.md
  - docs/plans/wb-008-post-merge-ssot-release-gate.md
  - docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md
active_work_block: null
-->

## Architecture

The framework has five coordinated layers:

1. **Governance Core** — authority, lifecycle, artifacts, runtime capabilities,
   evaluation, release state, assurance, and closeout under `governance/`.
2. **Runtime Adapters** — Codex, Claude Code, OpenCode, and generic execution
   mappings under `runtimes/`.
3. **Integration Adapters** — optional bridges, MCP, and audited file transport
   under `integrations/` and `handoff/`.
4. **Project Artifacts and Evidence** — specifications, decisions, plans,
   evaluation plans, observable events, reports, memory, and Work Block state.
5. **Installation Composition** — `bootstrap/profiles.json` selects which runtime
   implementation surfaces and skills are copied into a generated project.

Installation composition, release-state evidence, evaluation evidence, and
provider snapshots do not grant authority or integration admission. Accepted
architectural direction:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Authority Order

1. Explicit Owner instruction for the active Work Block.
2. Active workspace `AGENTS.md` and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation/evaluation plans and write-set.
6. Active task decomposition.
7. Review, verification, evaluation, drift, integration, release-state, and
   closeout evidence.
8. Durable engineering memory.
9. Operational logs, runtime memory, generated context, integrations, examples.

Runtime settings, prompts, plugins, models, tools, judges, scores, installation
profiles, provider artifacts, and hosting-platform state implement, measure, or
transport the model. They do not override it.

## Evaluation Assurance

`governance/evaluation.md` defines three evidence classes:

- deterministic tests for objectively checkable behavior;
- output evaluation against an approved rubric;
- observable trajectory evaluation for tool, gate, check, retry, side-effect,
  and evidence events.

Trajectory assurance never requires private chain-of-thought, hidden reasoning,
or model scratchpads. An LM judge cannot prove deterministic correctness, waive
failing checks, or open write/integration/deployment/Hard Stop gates.

Generated projects receive evaluation plan/report/event templates,
`scripts/validate-evaluation.py`, and dedicated evaluation evidence boundaries.

## Release-State Assurance

`governance/release-state.md` separates repository-owned lifecycle state from
mutable hosting-platform state. Repository release readiness is derived from
Work Block frontmatter, `FILE_REGISTRY.yml`, the machine-readable block in this
map, and approved closeout evidence.

`scripts/validate-release-state.py` fails closed when completed/active Work
Blocks, map, registry, or closeout disagree. Hosting-platform lifecycle is
external operational metadata and is queried when needed.

## Risk-Tiered Repair Assurance

NDR is a `Controlled` submode, not a new profile. It admits only deterministic,
reversible CI/bootstrap/runtime-validation repairs with exact allowlists, one
repair record, bounded implementation/correction accounting, deterministic
checks, and independent combined assurance.

Integration Stabilization is a bounded execution envelope. The Framework
Contracts workflow fails closed on unknown paths and keeps required contract
families active. Its non-required `provider-snapshot` job records the current
`contracts` job identity and result as point-in-time `PARTIAL` evidence, or
`UNVERIFIED` when evidence cannot be bound. The artifact has `authority: none`;
ruleset-required checks remain the sole live merge authority.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifacts, evaluation, release-state, and capability contracts |
| `governance/evaluation.md` | normative | Deterministic, output, and observable trajectory assurance |
| `governance/release-state.md` | normative | Repository SSOT reconciliation and hosting-platform boundary |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded mode |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `bootstrap/profiles.json` | installation manifest | Components, skill sets, aliases, and required generated paths |
| `bootstrap/bootstrap_project.py` | scaffold engine | Validates profile, stages atomically, installs skills, records state |
| `docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md` | latest completed Work Block | NDR, Integration Stabilization, CI routing, and provider evidence semantics |
| `docs/reports/closeout/wb-009-risk-tiered-repair-lifecycle.md` | latest closeout | Repository success-closeout for WB-009 |
| `docs/evals/` | evaluation evidence | Approved plans, benchmarks/fixtures, and observable event evidence |
| `docs/reports/evaluations/` | evaluation evidence | Per-criterion results, gaps, risks, and verdicts |
| `template/scripts/validate-evaluation.py` | generated validator | Plan/report consistency and Work Block closeout binding |
| `template/scripts/repair-lifecycle.py` | generated validator | NDR eligibility, repair records, and combined assurance contracts |
| `scripts/validate-release-state.py` | repository validator | Work Block, map, registry, closeout, and release-state consistency |
| `scripts/test-release-state-contracts.py` | contract test | Positive and adversarial release-state fixtures |
| `.github/workflows/release-state-contract.yml` | CI evidence | Dedicated release-state and fixture validation |
| `.github/workflows/framework-contracts.yml` | CI evidence | Contract routing, validation, and non-authoritative provider snapshot |
| `scripts/ci-contract-router.py` | CI control | Unknown paths run full suite; required contracts never skip |
| `README.md` / `SETUP.md` | public guidance | Architecture, setup, and safe activation |
| `PROJECT_MAP.md` / `FILE_REGISTRY.yml` | navigation | Human and machine path/authority maps |

## Installation Profiles

| Profile | Runtime implementation surfaces | Status |
|---|---|---|
| `core` | none; generic guidance only | smallest portable scaffold |
| `codex` | `.codex/` | Codex-primary baseline |
| `claude-code` | `CLAUDE.md`, `.claude/` | Claude Code-primary baseline |
| `opencode` | `opencode.json`, `.opencode/` | OpenCode baseline; live smoke required |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | backward-compatible default |

Every profile includes runtime-neutral evaluation and repair governance. Aliases:
`minimal`/`generic` → `core`; `full` → `multi-runtime`.

## Runtime and Integration Adapters

| Surface | Path | Default state |
|---|---|---|
| Codex | `runtimes/codex/`, conditional `.codex/` | selected by profile; authority from Work Block only |
| Claude Code | `runtimes/claude-code/`, conditional `.claude/` | Claude Code-primary baseline |
| OpenCode | `runtimes/opencode/`, conditional `.opencode/` | explicit permission baseline |
| Generic | `runtimes/generic/` | documented sequential fallback |
| Official Claude Code → Codex plugin | `integrations/claude-code-codex-plugin/` | optional admission |
| MCP | `integrations/mcp/` | disabled; exact server/tool admission required |
| File handoff | `integrations/file-handoff/` | disabled until configured |
| Existing handoff runner | `handoff/` | compatibility transport; no automatic service start |

External runtime invocation admission does not grant child-runtime write
authority.

## Migration Work

Completed:

1. WB-001 — runtime-neutral control plane.
2. WB-002 — portable template convergence.
3. WB-003 — Codex-native agents and gates.
4. WB-004 — integration adapter normalization.
5. WB-005 — profile-aware bootstrap and runtime conformance.
6. WB-006 — bootstrap restore hardening.
7. WB-007 — agent evaluation and trajectory assurance.
8. WB-008 — post-closeout SSOT reconciliation and release-state gate.
9. WB-009 — risk-tiered deterministic repair lifecycle and provider evidence.

No active implementation Work Block.

## Boundaries

- `governance/**` is normative and runtime-neutral.
- `bootstrap/**` controls scaffold composition only.
- `runtimes/**` and runtime implementation files cannot redefine authority.
- integrations require admission and active Work Block scope.
- `.agent/bootstrap-profile.json` is installation evidence, not authority.
- `.agent/active-work-block.json` is operational authority/gate state.
- evaluation plans are assurance configuration; reports/events are evidence.
- provider snapshots and release-state evidence grant no external authority.
- hosting-platform lifecycle is mutable external operational metadata.
- operational evidence excludes hidden reasoning, secrets, and protected payloads.
- unavailable checks/events remain blocked, not passed.
- specifications and accepted decisions remain above plans and evidence.

## Framework Read Order

1. workspace `AGENTS.md`, when present;
2. relevant `governance/` contracts;
3. active Work Block, when present;
4. approved specification and accepted architecture decisions;
5. implementation/evaluation plan;
6. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
7. installed runtime and admitted integration adapters;
8. current Git state, diff, target files, and evidence;
9. reference knowledge and operational logs only when relevant.

Update this map and `FILE_REGISTRY.yml` whenever authority, lifecycle,
evaluation, release state, profile composition, evidence boundaries, adapters,
migration state, or publication requirements change.