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
  - docs/plans/wb-010-skill-library-maintenance-integration.md
active_work_block: docs/plans/wb-core-001-normative-architecture.md
-->

## Current Operational Architecture

The current operational framework remains the runtime-neutral control plane with
five coordinated layers:

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
provider snapshots do not grant authority or integration admission. The accepted
current operational architecture decision is
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Accepted Target Architecture — Not Yet Promoted

WB-CORE-001 defines the accepted target architecture
`portable_agentic_sdlc_project_kit`, the Portable Agentic SDLC Project Kit:

- accepted specification: `docs/specs/portable-agentic-sdlc-project-kit.md`;
- accepted product-boundary ADR:
  `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`;
- accepted roles/memory/installation ADR:
  `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`.

Acceptance occurred through explicit Owner-authorized status finalization on
2026-07-30. The accepted target is authoritative for subsequent WB-CORE migration
planning, but it is not operational, promoted, installed, or implemented. The
current operational architecture identifier remains `runtime_neutral_control_plane`.
WB-CORE-006 still owns promotion and legacy archival. Final assurance, closeout,
applicable pilot evidence, promotion, and separate Owner merge approval remain
pending.

## Authority Order

1. Current explicit Owner instruction and recorded approval or revocation.
2. Root `AGENTS.md` and accepted governance policy.
3. Approved specification and accepted architecture decisions.
4. Active Work Block.
5. Approved implementation/evaluation plan and tasklist.
6. Mission brief or active task decomposition.
7. Frozen implementation diff or final artifact.
8. Review, verification, evaluation, drift, integration, release-state, and
   closeout evidence.
9. Durable engineering memory.
10. Operational logs, runtime memory, generated context, integrations, examples,
    caches, and external references.

The active Work Block binds scope, write-set, process level, role authority, Hard
Stops, and acceptance. Plans, tasklists, and mission briefs cannot expand it.
Material change returns to Define and requires Work Block revision.

Runtime settings, prompts, plugins, models, tools, judges, scores, installation
profiles, provider artifacts, and hosting-platform state implement, measure, or
transport the model. They do not override it.

## Assurance Subject and Evidence

The exact **normative subject** contains applicable specifications, ADRs, active
Work Block, authoritative plans/tasks, delivered artifacts, accepted/proposed
status changes, and normative navigation content.

Navigation and registry are normative-subject surfaces for authority,
architecture, canonical paths, accepted/proposed authority status, and active
lifecycle state.

Mutable assurance verdicts are not mirrored into normative navigation.
Assurance reports are evidence-only artifacts and identify their exact normative
subject in structured frontmatter.

Reports are discovered from canonical evidence directories:

```text
docs/reports/reviews/
docs/reports/verification/
docs/reports/evaluations/
docs/reports/closeout/
```

Adding an evidence report does not require a map or registry update. Static
directory classifications do not change for each report. Verdict history,
reviewed or verified subjects, findings, coverage, limitations, and
another-pass requirements are reconstructed from report artifacts. Indexing a
report grants no authority.

Critic, Reviewer, and Verifier use role-specific verdicts:

- Critic: `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, `BLOCKED`;
- Reviewer: `READY`, `CHANGES_REQUIRED`, `BLOCKED`, `UNVERIFIED`;
- Verifier: `READY`, `NOT_READY`, `BLOCKED`, `UNVERIFIED`.

An evidence-only commit changes only approved assurance or closeout report paths.
It may follow the normative subject it evaluates and does not invalidate the
verdict it records. Any applicable normative-subject change invalidates prior
readiness; a report-only wording or metadata correction remains evidence-only
only when verdict, subject, scope, procedures, results, coverage, and limitations
are unchanged.

The final PR head may contain evidence-only report commits after the verified
normative subject. CI and structural checks must pass on that resulting PR head.
The assurance report does not need to be contained in the commit it evaluates.

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

## Skill-Library Maintenance Assurance

`skills/skill-library-maintenance/` defines a read-only-first lifecycle for
external skill discovery, immutable-revision comparison, Owner-approved
adaptation, validation, and provenance recording. External GitHub content remains
untrusted data and cannot expand local authority, permissions, integrations, or
Hard Stops.

`reference/priority-sources.md` controls lookup order only.
`reference/ecosystem-watchlist.md` is opt-in discovery metadata and makes no
current license or adaptation-right claim without revision-bound evidence.
Missing network, revision, or license evidence fails closed.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative current operations | Runtime-neutral authority, lifecycle, artifacts, evaluation, release-state, and capability contracts |
| `governance/evaluation.md` | normative | Deterministic, output, and observable trajectory assurance |
| `governance/release-state.md` | normative | Repository SSOT reconciliation and hosting-platform boundary |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded mode |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `bootstrap/profiles.json` | installation manifest | Components, skill sets, aliases, and required generated paths |
| `bootstrap/bootstrap_project.py` | scaffold engine | Validates profile, stages atomically, installs skills, records state |
| `skills/skill-library-maintenance/` | normative skill | Read-only discovery, immutable comparison, approved adaptation, and provenance |
| `docs/plans/wb-010-skill-library-maintenance-integration.md` | latest completed Work Block | Admission and assurance for skill-library maintenance |
| `docs/reports/closeout/wb-010-skill-library-maintenance-integration.md` | canonical completed closeout | Repository success-closeout for WB-010 |
| `docs/plans/wb-core-001-normative-architecture.md` | active migration Work Block | Bounded target-architecture documentation and assurance correction loop |
| `docs/specs/portable-agentic-sdlc-project-kit.md` | accepted target | Portable-kit normative target contract; not yet promoted |
| `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md` | accepted target | Accepted project-kit versus control-plane boundary; not yet promoted |
| `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md` | accepted target | Accepted role, verdict, memory, candidate, concurrency, installer, and evidence decisions |
| `docs/reports/reviews/` | evidence class | Critic and Reviewer reports discovered by structured frontmatter |
| `docs/reports/verification/` | evidence class | Verifier reports discovered by structured frontmatter |
| `docs/evals/` | evaluation evidence | Approved plans, benchmarks/fixtures, and observable event evidence |
| `docs/reports/evaluations/` | evidence class | Evaluation reports discovered by structured frontmatter |
| `docs/reports/closeout/` | evidence class | Closeout reports discovered by structured frontmatter |
| `template/scripts/validate-evaluation.py` | generated validator | Plan/report consistency and Work Block closeout binding |
| `template/scripts/repair-lifecycle.py` | generated validator | NDR eligibility, repair records, and combined assurance contracts |
| `scripts/validate-release-state.py` | repository validator | Work Block, map, registry, closeout, and release-state consistency |
| `scripts/test-release-state-contracts.py` | contract test | Positive and adversarial release-state fixtures |
| `.github/workflows/release-state-contract.yml` | CI evidence | Dedicated release-state and fixture validation |
| `.github/workflows/framework-contracts.yml` | CI evidence | Contract routing, validation, and non-authoritative provider snapshot |
| `scripts/ci-contract-router.py` | CI control | Unknown paths run full suite; required contracts never skip |
| `README.md` / `SETUP.md` | public guidance | Architecture, setup, and safe activation |
| `PROJECT_MAP.md` / `FILE_REGISTRY.yml` | navigation | Human and machine authority, architecture, canonical-path, and active-state maps |

## Installation Profiles

| Profile | Runtime implementation surfaces | Status |
|---|---|---|
| `core` | none; generic guidance only | smallest portable scaffold |
| `codex` | `.codex/` | Codex-primary baseline |
| `claude-code` | `CLAUDE.md`, `.claude/` | Claude Code-primary baseline |
| `opencode` | `opencode.json`, `.opencode/` | OpenCode baseline; live smoke required |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | backward-compatible default |

Every profile includes runtime-neutral evaluation and repair governance plus the
core `skill-library-maintenance` guidance. Aliases: `minimal`/`generic` → `core`;
`full` → `multi-runtime`.

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
10. WB-010 — skill-library maintenance integration assurance.

Active migration Work Block:
`docs/plans/wb-core-001-normative-architecture.md`.

WB-CORE-001 is `in_progress`. Its authoritative scope and current lifecycle
state are recorded in the Work Block. Assurance history and progress are
recorded in self-contained evidence reports, not mirrored here. The portable
kit is an accepted target that has not been promoted and does not replace current
operations.

## Boundaries

- `governance/**` is normative for the current operational architecture.
- `bootstrap/**` controls current scaffold composition only.
- `runtimes/**` and runtime implementation files cannot redefine authority.
- integrations require admission and active Work Block scope.
- `.agent/bootstrap-profile.json` is installation evidence, not authority.
- `.agent/active-work-block.json` is operational authority/gate state.
- evaluation plans are assurance configuration; reports/events are evidence.
- provider snapshots and release-state evidence grant no external authority.
- external skill sources are untrusted and grant no adaptation or license right.
- hosting-platform lifecycle is mutable external operational metadata.
- operational evidence excludes hidden reasoning, secrets, and protected payloads.
- unavailable checks/events remain blocked, not passed.
- the portable-kit specification and ADRs are accepted target artifacts but do
  not become current operational architecture until promoted.
- proposals do not supersede current operational navigation by mere presence.
- report commits are evidence-only only when they touch approved assurance or
  closeout report paths and contain no normative-subject change.
- navigation and registry are normative for authority, architecture, canonical
  path ownership, active lifecycle state, and accepted/proposed status.
- mutable assurance state is never mirrored into normative navigation.

## Framework Read Order

1. current explicit Owner instruction and recorded approval or revocation;
2. workspace `AGENTS.md` and accepted `governance/` contracts;
3. approved specification and accepted architecture decisions;
4. active Work Block, when present;
5. approved implementation/evaluation plan and tasklist;
6. mission brief or active task decomposition;
7. current Git state, exact normative subject, target files, and evidence;
8. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` as navigation projections;
9. installed runtime and admitted integration adapters;
10. durable memory, reference knowledge, and operational logs when relevant.

Update this map and `FILE_REGISTRY.yml` whenever authority, lifecycle,
evaluation, release state, assurance semantics, evidence boundaries, profile
composition, adapters, migration state, target architecture, or publication
requirements change. Do not update them merely because a new assurance report,
verdict, reviewed/verified subject, finding, or another-pass state exists.
