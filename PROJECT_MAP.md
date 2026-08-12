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
  - docs/plans/wb-core-001-normative-architecture.md
  - docs/plans/wb-core-002-portable-candidate-content.md
  - docs/plans/wb-core-002a-portable-candidate-review-remediation.md
  - docs/plans/wb-core-003-codex-local-control-plane-pilot.md
  - docs/plans/wb-core-003a-work-block-composition-and-flow-feedback.md
  - docs/plans/wb-core-003b-self-hosting-control-plane-reconciliation.md
  - docs/plans/wb-core-003c-completed-state-assurance-binding.md
  - docs/plans/wb-core-003d-parallel-write-set-orchestration.md
  - docs/plans/wb-core-003e-closure-evidence-correction.md
  - docs/plans/wb-opencode-002-project-local-integration.md
  - docs/plans/wb-design-001-openai-frontend-delta.md
  - docs/plans/wb-design-002-portable-design-md-artifact-contract.md
  - docs/plans/wb-core-003f-github-native-authority-model.md
active_work_block: null
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

This worktree also carries an optional project-local OpenCode surface at the
repository root. `.opencode/` contains logical-role agents and separately
enumerated optional bridge skills. Both are runtime-adapter-only surfaces:
they grant no authority, do not change the runtime-neutral authority model, and
do not make OpenCode the framework Orchestrator. Runtime discovery of the
optional bridge skills remains `UNVERIFIED` pending separately approved live
smoke evidence.

## Accepted Target Architecture — Not Yet Promoted

WB-CORE-001 completed definition, accepted-status finalization, final assurance,
drift alignment, and repository closeout for the accepted target architecture
`portable_agentic_sdlc_project_kit`, the Portable Agentic SDLC Project Kit:

- accepted specification: `docs/specs/portable-agentic-sdlc-project-kit.md`;
- accepted product-boundary ADR:
  `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`;
- accepted roles/memory/installation ADR:
  `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`.

The accepted target is authoritative for later separately gated WB-CORE planning,
but it remains unimplemented, uninstalled, and unpromoted. The current
operational architecture identifier remains `runtime_neutral_control_plane`.

WB-CORE-002 completed its noncanonical candidate content, WB-CORE-002A completed
Standard P2 remediation, and WB-CORE-003 completed the local Codex control-plane
pilot; the candidate remains uninstalled, unpromoted, and non-authoritative.
WB-CORE-003A completed its bounded governance rule for Work Block composition
and evidence-based material process findings. It did not promote the candidate
or install any runtime adapter. WB-CORE-003B completed the bounded
self-hosting control-plane reconciliation, including final independent
assurance and repository closeout evidence. It did not promote the candidate,
install a runtime adapter, or authorize any version-control action.
WB-CORE-003C completed the evidence-only corrective follow-up: it binds
independent assurance to WB-CORE-003B's immutable completed-state snapshot and
does not reopen WB-CORE-003B or alter product Work Block sequencing.
WB-CORE-003D completed the separately bounded governance protocol for parallel
exclusive Coder write-sets, isolated worktrees, and the frozen integrated
assurance subject. It did not activate a runtime, generated template, hook, or
live multi-worktree pilot.
WB-CORE-003E completed the bounded corrective closure-evidence correction for
WB-CORE-003D. It applied a two-pass assurance sequence, obtained independent
preliminary and final preflight READY/READY/ALIGNED, and closed with no active
Work Block remaining. It did not reopen the parallel-write-set protocol or alter
product Work Block sequencing.
WB-CORE-003F completed the inserted GitHub-native authority-model migration. It
retired per-Work-Block SSH signing from the normal development path, preserved
Work Block/write-set/assurance discipline, and moved consequential security
authority to external GitHub/OS/workflow/credential capability boundaries. It
did not promote the Portable Kit or consume the pre-existing product roadmap ID.
WB-CORE-004 through WB-CORE-007 remain future product Work Blocks requiring their
own scope, authority, write-set, assurance, and approvals. WB-CORE-007 retains
promotion and legacy archival ownership. Separate explicit Owner approval remains
required for each future merge.

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
| `opencode.json` | runtime adapter | Project-local OpenCode instructions and permission baseline; no authority |
| `.opencode/agents/` | runtime adapter | Project-local logical-role subagents; live smoke required |
| `.opencode/skills/` | runtime adapter | Optional bridge skills: `critic-review`, `reviewer`, `scoped-coder`, `ssot-sync-closeout`, `subagent-mission-brief`, `task-decomposition`, and `verifier`; discovery unverified and no authority |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `bootstrap/profiles.json` | installation manifest | Components, skill sets, aliases, and required generated paths |
| `bootstrap/bootstrap_project.py` | scaffold engine | Validates profile, stages atomically, installs skills, records state |
| `skills/skill-library-maintenance/` | normative skill | Read-only discovery, immutable comparison, approved adaptation, and provenance |
| `docs/design/design-md-artifact-contract.md` | approved design-domain contract | Optional provider-neutral DESIGN.md authority, lifecycle, reconciliation, and interoperability contract |
| `docs/templates/design-md-template.md` | reference template | Reusable DESIGN.md starter; never auto-installed by presence alone |
| `docs/plans/wb-design-002-portable-design-md-artifact-contract.md` | completed Work Block | Portable DESIGN.md contract and Impeccable/frontend-design consumer reconciliation |
| `docs/plans/wb-010-skill-library-maintenance-integration.md` | completed Work Block | Admission and assurance for skill-library maintenance |
| `docs/reports/closeout/wb-010-skill-library-maintenance-integration.md` | completed closeout | Repository success-closeout for WB-010 |
| `docs/plans/wb-core-001-normative-architecture.md` | completed Work Block | Accepted normative architecture and repository closeout for the portable kit |
| `docs/plans/wb-core-003f-github-native-authority-model.md` | completed Work Block | GitHub-native capability boundary and retired normal-path SSH authorization |
| `docs/reports/closeout/wb-core-003f-github-native-authority-model.md` | completed closeout | Repository closeout for the authority-model migration |
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
| OpenCode | `runtimes/opencode/`, root `opencode.json`, root `.opencode/` | project-local optional surface; explicit permission baseline; live smoke required |
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
11. WB-CORE-001 — accepted normative architecture for the Portable Agentic SDLC Project Kit.

12. WB-CORE-002 — portable candidate content; candidate-only, noncanonical,
   uninstalled, and unpromoted.
13. WB-CORE-002A — Standard P2 remediation of candidate lifecycle and Work
   Block template controls; candidate remains noncanonical, uninstalled,
   unpromoted, and non-authoritative.
14. WB-CORE-003A — bounded Portable Kit governance rule and initial-assurance
    sequence; its terminal lifecycle projection requires final applicable
    assurance before any commit.
15. WB-CORE-003B — self-hosting control-plane reconciliation for framework
    maintenance; repository lifecycle closeout only, with no Portable Kit
    promotion, runtime adapter, hook, installer, or version-control action.
16. WB-CORE-003C — completed-state assurance binding for the immutable
    WB-CORE-003B snapshot; governance evidence only, with no version-control
    or external GitHub action.
17. WB-CORE-003D — completed governance protocol for parallel exclusive
    write-set orchestration and integrated-subject assurance; no runtime or VCS
    action was authorized.

18. WB-CORE-003E — completed bounded closure-evidence correction for
    WB-CORE-003D; governance evidence only, no runtime, protocol, or VCS action.

19. WB-OPENCODE-002 — completed project-local OpenCode runtime-adapter
    integration; live discovery and permission-merging behavior remain unverified.

20. WB-DESIGN-001 — completed Controlled refresh of `frontend-design` with a
    provider-neutral OpenAI methodological delta; no runtime or tool activation.

21. WB-DESIGN-002 — completed Controlled portable DESIGN.md artifact contract and
    internal frontend-design/Impeccable compatibility reconciliation; no Google
    tooling, MCP, runtime, bootstrap, or provider activation.

22. WB-CORE-003F — completed Managed GitHub-native authority-model migration;
    normal scoped development no longer requires SSH-signed Work Block records,
    while consequential authority remains external to mutable project state.

No active implementation Work Block.

Planned:

- WB-CORE-004 — installer and packaging;
- WB-CORE-005 — synthetic dry run;
- WB-CORE-006 — HardwareLab pilot;
- WB-CORE-007 — promotion and legacy archive.

WB-CORE-004 remains the next planned product Work Block. WB-CORE-003A through
WB-CORE-003F are inserted governance/control-plane follow-ups, not replacements
for that product sequence. Planned status grants no execution authority. Each
future Work Block requires separate Owner authority, exact scope, write-set,
assurance, and closeout.

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
