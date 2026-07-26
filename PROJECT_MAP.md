# Project Map

Human-readable navigation for the Agentic SDLC Framework. Use it to locate
authority, installation composition, runtime/integration adapters, active work,
and evidence without loading the full repository.

## Architecture

The framework has five coordinated layers:

1. **Governance Core** — authority, lifecycle, artifacts, runtime capabilities,
   evaluation, assurance, and closeout under `governance/`.
2. **Runtime Adapters** — Codex, Claude Code, OpenCode, and generic execution
   mappings under `runtimes/`.
3. **Integration Adapters** — optional bridges, MCP, and audited file transport
   under `integrations/` and `handoff/`.
4. **Project Artifacts and Evidence** — specifications, decisions, plans,
   evaluation plans, observable events, reports, memory, and Work Block state.
5. **Installation Composition** — `bootstrap/profiles.json` selects which runtime
   implementation surfaces and skills are copied into a generated project.

Installation composition and evaluation evidence do not grant authority or
integration admission. Accepted architectural direction:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Authority Order

1. Explicit Owner instruction for the active Work Block.
2. Active workspace `AGENTS.md` and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation/evaluation plans and write-set.
6. Active task decomposition.
7. Review, verification, evaluation, drift, integration, and closeout evidence.
8. Durable engineering memory.
9. Operational logs, runtime memory, generated context, integrations, examples.

Runtime settings, prompts, plugins, models, tools, judges, scores, and installation
profiles implement or measure the model. They do not override it.

## Evaluation Assurance

`governance/evaluation.md` defines three evidence classes:

- deterministic tests for objectively checkable behavior;
- output evaluation against an approved rubric;
- observable trajectory evaluation for tool, gate, check, retry, side-effect,
  and evidence events.

Trajectory assurance never requires private chain-of-thought, hidden reasoning,
or model scratchpads. An LM judge cannot prove deterministic correctness, waive
failing checks, or open write/integration/deployment/Hard Stop gates.

Generated projects receive:

- `docs/templates/evaluation-plan-template.json`;
- `docs/templates/evaluation-report-template.json`;
- `docs/templates/trajectory-event-template.json`;
- `scripts/validate-evaluation.py`;
- `docs/evals/` and `docs/reports/evaluations/` boundaries.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifacts, evaluation, and capability contracts |
| `governance/evaluation.md` | normative | Deterministic, output, and observable trajectory assurance |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded mode |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `bootstrap/profiles.json` | installation manifest | Components, skill sets, aliases, and required generated paths |
| `bootstrap/bootstrap_project.py` | scaffold engine | Validates profile, stages atomically, installs skills, records state |
| `docs/plans/wb-007-agent-evaluation-trajectory-assurance.md` | active Work Block | Evaluation contract, generated validator, fixtures, CI, and closeout |
| `docs/evals/` | evaluation evidence | Approved plans, benchmarks/fixtures, and observable event evidence |
| `docs/reports/evaluations/` | evaluation evidence | Per-criterion results, gaps, risks, and verdicts |
| `template/scripts/validate-evaluation.py` | generated validator | Plan/report consistency and Work Block closeout binding |
| `scripts/test-evaluation-contracts.py` | contract test | Positive and adversarial evaluation fixtures |
| `scripts/validate_evaluation_publication.py` | publication test | Evaluation inventory, templates, manifest, smoke, and privacy boundary |
| `template/.agent/active-work-block.json` | template gate | Write, integration, review, verification, evaluation, drift, and closeout state |
| `template/.claude/hooks/assurance_gate.py` | runtime gate | Enforces evidence-backed closeout including required evaluation |
| `.github/workflows/framework-contracts.yml` | CI evidence | Full contract, profile, adapter, evaluation, and disposable-scaffold validation |
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

Every profile includes runtime-neutral evaluation governance and templates. Aliases:
`minimal`/`generic` → `core`; `full` → `multi-runtime`.

## Runtime and Integration Adapters

| Surface | Path | Default state |
|---|---|---|
| Codex | `runtimes/codex/`, conditional `.codex/` | selected by profile; authority from Work Block only |
| Claude Code | `runtimes/claude-code/`, conditional `.claude/` | selected by profile; closeout gate implemented |
| OpenCode | `runtimes/opencode/`, conditional `.opencode/` | selected by profile; explicit permission baseline |
| Generic | `runtimes/generic/` | always available as documented fallback |
| Official Claude Code → Codex plugin | `integrations/claude-code-codex-plugin/` | not installed; optional admission |
| MCP | `integrations/mcp/` | disabled; exact server/tool admission required |
| File handoff | `integrations/file-handoff/` | disabled until configured |
| Existing handoff runner | `handoff/` | compatibility transport; no automatic service start |

External runtime invocation admission does not grant child-runtime write authority.

## Migration Work

Completed:

1. WB-001 — runtime-neutral control plane.
2. WB-002 — portable template convergence.
3. WB-003 — Codex-native agents and gates.
4. WB-004 — integration adapter normalization.
5. WB-005 — profile-aware bootstrap and runtime conformance.
6. WB-006 — bootstrap restore hardening.

Active:

7. `docs/plans/wb-007-agent-evaluation-trajectory-assurance.md`
   - evaluation governance and artifact contracts;
   - generated plan/report/event templates;
   - plan/report/closeout validator;
   - observable trajectory and LM-judge boundaries;
   - regression, publication, and CI evidence.

PR #7 remains Draft until CI, final review, evaluation, drift, and closeout pass.

## Boundaries

- `governance/**` is normative and runtime-neutral.
- `bootstrap/**` controls scaffold composition only.
- `runtimes/**` and runtime implementation files cannot redefine authority.
- integrations require admission and active Work Block scope.
- `.agent/bootstrap-profile.json` is installation evidence, not authority.
- `.agent/active-work-block.json` is operational authority/gate state.
- evaluation plans are assurance configuration; reports/events are evidence.
- operational event evidence must exclude hidden reasoning, secrets, and protected payloads.
- unavailable checks/events remain blocked, not passed.
- specifications and accepted decisions remain above plans and evidence.

## Framework Read Order

1. workspace `AGENTS.md`, when present;
2. relevant `governance/` contract, including `evaluation.md` when applicable;
3. active Work Block;
4. approved specification and accepted architecture decisions;
5. implementation/evaluation plan;
6. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
7. installed runtime and admitted integration adapters;
8. current Git state, diff, target files, and evidence;
9. reference knowledge and operational logs only when relevant.

Update this map and `FILE_REGISTRY.yml` whenever authority, lifecycle,
evaluation, profile composition, evidence boundaries, adapters, migration state,
or publication requirements change.
