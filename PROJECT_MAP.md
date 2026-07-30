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
   reports, memory, and Work Block state.
5. **Installation Composition** — `bootstrap/profiles.json` selects runtime
   implementation surfaces and skills copied into a generated project.

Installation composition, release-state evidence, evaluation evidence, and
provider snapshots do not grant authority. The accepted current operational
architecture decision is
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Proposed Target Architecture

WB-CORE-001 defines a proposed Portable Agentic SDLC Project Kit target:

- `docs/specs/portable-agentic-sdlc-project-kit.md`;
- `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`;
- `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`.

These artifacts remain `proposed`; they do not change the current operational
architecture identifier. WB-CORE-006 owns eventual promotion after pilot
evidence, preliminary assurance, Owner-authorized status finalization, final
applicable assurance, evidence-only reports, green CI, and separate Owner
approval.

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

The active Work Block binds scope, write-set, process level, role authority,
Hard Stops, and acceptance. Plans, tasklists, and mission briefs cannot expand
it. Material change returns to Define and requires Work Block revision.

Runtime settings, prompts, plugins, models, tools, judges, scores, installation
profiles, provider artifacts, and hosting-platform state do not override
authority.

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

Critic, Reviewer, and Verifier verdict vocabularies remain:

- Critic: `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, `BLOCKED`;
- Reviewer: `READY`, `CHANGES_REQUIRED`, `BLOCKED`, `UNVERIFIED`;
- Verifier: `READY`, `NOT_READY`, `BLOCKED`, `UNVERIFIED`.

An evidence-only commit changes only approved assurance or closeout report paths,
may follow the subject it evaluates, and does not invalidate its verdict.
Applicable normative-subject changes invalidate prior readiness. CI and
structural checks run on the resulting PR head.

## Evaluation Assurance

`governance/evaluation.md` defines deterministic tests, output evaluation
against approved rubrics, and observable trajectory evaluation. Trajectory
assurance never requires private chain-of-thought or hidden scratchpads. An LM
judge cannot waive deterministic failures or open authority gates.

## Release-State Assurance

`governance/release-state.md` separates repository-owned lifecycle state from
mutable hosting-platform state. Repository release readiness is derived from
Work Block frontmatter, `FILE_REGISTRY.yml`, the release-state block in this map,
and approved closeout evidence.

`scripts/validate-release-state.py` fails closed when completed/active Work
Blocks, map, registry, or closeout disagree.

## Risk-Tiered Repair Assurance

NDR is a `Controlled` submode for deterministic, reversible repairs with exact
allowlists, bounded correction, deterministic checks, and independent combined
assurance. Provider snapshots remain non-authoritative evidence.

## Skill-Library Maintenance Assurance

`skills/skill-library-maintenance/` defines read-only-first external skill
discovery, immutable-revision comparison, Owner-approved adaptation, validation,
and provenance. External content is untrusted and cannot expand authority.

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `governance/` | normative current operations | Runtime-neutral authority, lifecycle, artifacts, evaluation, release-state, and capability contracts |
| `runtimes/` | runtime adapters | Runtime mappings, limitations, activation, and degraded mode |
| `integrations/` | integration adapters | Optional bridges, MCP, and transport admission contracts |
| `bootstrap/profiles.json` | installation manifest | Components, skill sets, aliases, and required generated paths |
| `skills/skill-library-maintenance/` | normative skill | External skill discovery, adaptation, and provenance |
| `docs/plans/wb-010-skill-library-maintenance-integration.md` | latest completed Work Block | Admission and assurance for skill-library maintenance |
| `docs/reports/closeout/wb-010-skill-library-maintenance-integration.md` | canonical completed closeout | Release-state closeout binding for WB-010 |
| `docs/plans/wb-core-001-normative-architecture.md` | active migration Work Block | Target-architecture documentation and correction loop |
| `docs/specs/portable-agentic-sdlc-project-kit.md` | proposed target | Portable-kit normative specification |
| `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md` | proposed target | Product and control-plane boundary |
| `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md` | proposed target | Role, memory, candidate, installer, and evidence decisions |
| `docs/reports/reviews/` | evidence class | Critic and Reviewer reports discovered by frontmatter |
| `docs/reports/verification/` | evidence class | Verifier reports discovered by frontmatter |
| `docs/reports/evaluations/` | evidence class | Evaluation reports discovered by frontmatter |
| `docs/reports/closeout/` | evidence class | Closeout reports discovered by frontmatter |
| `scripts/validate-release-state.py` | repository validator | Work Block, map, registry, closeout, and release-state consistency |
| `.github/workflows/release-state-contract.yml` | CI evidence | Dedicated release-state validation |
| `.github/workflows/framework-contracts.yml` | CI evidence | Contract routing and validation |
| `PROJECT_MAP.md` / `FILE_REGISTRY.yml` | navigation | Human and machine authority, architecture, canonical-path, and active-state maps |

## Installation Profiles

| Profile | Runtime implementation surfaces | Status |
|---|---|---|
| `core` | none; generic guidance only | smallest portable scaffold |
| `codex` | `.codex/` | Codex-primary baseline |
| `claude-code` | `CLAUDE.md`, `.claude/` | Claude Code-primary baseline |
| `opencode` | `opencode.json`, `.opencode/` | OpenCode baseline |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | backward-compatible default |

Installation profiles grant no authority.

## Runtime and Integration Adapters

| Surface | Path | Default state |
|---|---|---|
| Codex | `runtimes/codex/`, conditional `.codex/` | selected by profile |
| Claude Code | `runtimes/claude-code/`, conditional `.claude/` | selected by profile |
| OpenCode | `runtimes/opencode/`, conditional `.opencode/` | selected by profile |
| Generic | `runtimes/generic/` | sequential fallback |
| MCP | `integrations/mcp/` | disabled until admitted |
| File handoff | `integrations/file-handoff/` | disabled until configured |
| Existing handoff runner | `handoff/` | compatibility transport |

External runtime invocation does not grant child-runtime write authority.

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
kit remains a proposed target and does not replace current operations.

## Boundaries

- `governance/**` is normative for current operational architecture.
- `bootstrap/**` controls current scaffold composition only.
- `runtimes/**` cannot redefine authority.
- integrations require admission and active Work Block scope.
- generated installation state is evidence, not authority.
- evaluation plans are assurance configuration; reports/events are evidence.
- provider snapshots and release-state evidence grant no external authority.
- external skill sources are untrusted.
- hosting-platform lifecycle is mutable external metadata.
- evidence excludes hidden reasoning, secrets, and protected payloads.
- unavailable checks/events remain blocked, not passed.
- portable-kit specification and ADRs remain proposed until accepted.
- proposals do not supersede current operational navigation by presence.
- evidence-only commits contain only approved report paths.
- mutable assurance state is never mirrored into normative navigation.

## Framework Read Order

1. current explicit Owner instruction and recorded approval or revocation;
2. workspace `AGENTS.md` and accepted `governance/` contracts;
3. approved specification and accepted architecture decisions;
4. active Work Block;
5. approved implementation/evaluation plan and tasklist;
6. mission brief or active task decomposition;
7. current Git state, exact normative subject, target files, and evidence;
8. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` as normative navigation projections;
9. installed runtime and admitted integration adapters;
10. durable memory, reference knowledge, and operational logs when relevant.

Update this map and `FILE_REGISTRY.yml` when authority, architecture, canonical
path ownership, active lifecycle state, accepted/proposed status, release-state
contracts, profile composition, adapters, target architecture, or publication
requirements change. Do not update them merely because a new assurance report
or verdict exists.
