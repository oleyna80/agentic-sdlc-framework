---
schema_version: 1
artifact_type: work_block
artifact_id: wb-release-002-candidate-promotion-lifecycle
work_block_id: WB-RELEASE-002
status: in_progress
owner_role: Owner
created_at: 2026-08-25
last_updated: 2026-08-25
governance_profile: Managed
branch: agent/wb-release-002-candidate-promotion
base_revision: 73cd1cab36af327683991c768ea887911547df06
write_gate: BLOCKED
critic_gate: PENDING
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
evaluation_verdict: NOT_REQUIRED
closeout_mode: pending
owner_approval: Owner authorized correction of the WB-RELEASE-002 Define findings on 2026-08-25. This authorization is limited to the same three Define artifacts and their feature-branch persistence; it does not authorize source changes, canonical projection changes, pull request creation/update, merge, or thread resolution.
---

# WB-RELEASE-002 — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Stage and objective

- **Current Stage:** Define
- **Stage State:** in_progress
- **Role:** Orchestrator → Architect
- **Objective:** define a truthful, fail-closed transition from an evidence-complete `pre_closeout_candidate` to durable promoted history and then to the next candidate without discarding effective completion history or weakening ordinary release-state validation.

## Context and confirmed trigger

The accepted WB-RELEASE-001 contract supports one local `pre_closeout_candidate` and derives effective completion only after four exact evidence artifacts bind the candidate. It does not specify how that effective candidate is durably promoted before another candidate is declared. The WB-CORE-003G pilot exposed the resulting sequencing gap: a successor cannot truthfully become the next candidate while the prior evidence-complete candidate remains the sole active candidate declaration and the existing predecessor rule still points only at raw completed history.

This Define run specifies that missing transition only. It does not repair WB-CORE-003G, rewrite WB-RELEASE-001, relabel historical evidence, or implement a validator.

## Expected final result

An approved future specification and implementation plan define one serial candidate lifecycle with explicit promotion prerequisites, an append-only effective-completion history, exact effective-predecessor binding, and a fail-closed two-revision promotion/next-candidate transition. Historical raw records remain truthful; no evidence or Owner decision is fabricated.

## Done criteria for Define

- [ ] Current release-state candidate and all 29 raw completed records are reconciled from the baseline registry.
- [ ] Historical impact is classified without inferring missing profile/specification metadata.
- [ ] A prospective serial transition model and deterministic predecessor rule are selected.
- [ ] Future implementation owners and smallest proposed write-set are recorded.
- [ ] Requirements, acceptance criteria, and tasklist are structurally traceable.
- [ ] Requirements review, consistency analysis, and Critic remain pending until their separate read-only stages.

## Normative baseline

- **Release-state contract:** `governance/release-state.md`
- **Lifecycle contract:** `governance/lifecycle.md`
- **Artifact authority contract:** `governance/artifacts.md`
- **Authority contract:** `governance/authority.md`
- **Define-quality contract:** `governance/define-quality.md`
- **SDD protocol:** `.agent/workflows/sdd-protocol.md`
- **Machine state:** `FILE_REGISTRY.yml`
- **Human projection:** `PROJECT_MAP.md`
- **Existing candidate Work Block:** `docs/plans/wb-release-001-closeout-sequencing-reconciliation.md`
- **Existing candidate specification:** `docs/specs/wb-release-001-closeout-sequencing-reconciliation.md`
- **Existing candidate tasklist:** `docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md`

## Baseline and repository preflight

- **Base revision:** `73cd1cab36af327683991c768ea887911547df06`
- **Original Define subject:** `73cd1cab36af327683991c768ea887911547df06` → `1733a266bfa0da4b6137b62bdf448297cb2b408a`.
- **Branch:** `agent/wb-release-002-candidate-promotion`
- **Pre-existing untracked file:** `Repository Graph Evaluation Brief.md`; out of scope and untouched by this GitHub-only correction.
- **Define-only writable files:** the three WB-RELEASE-002 artifacts.

## Scope

### In scope

- read-only analysis of candidate promotion, effective completion, and next-candidate sequencing;
- exact inventory reconciliation of the 29 baseline raw completed Work Blocks plus the one active candidate declaration;
- requirements and acceptance criteria for a prospective serial transition;
- selection of the smallest draft state model needed to make predecessor semantics implementation-ready;
- a proposed future implementation write-set that remains unauthorized for Execute.

### Out of scope

- changing `governance/release-state.md`, validators, fixtures, `FILE_REGISTRY.yml`, `PROJECT_MAP.md`, or `.agent/workflows/sdd-protocol.md` in this Define correction;
- changing WB-RELEASE-001, WB-CORE-003G, or any historical Work Block/evidence artifact;
- source implementation, pull request creation/update, merge, rebase, thread resolution, or historical evidence relabeling;
- Gemini recommendations, converge loops, extensions, presets, workflows, bundles, or unrelated governance redesign.

## Historical impact inventory

The baseline `FILE_REGISTRY.yml:migration_state.completed_work_blocks` contains exactly **29 raw paths**. The first 19 have no structured `governance_profile` in their Work Block frontmatter. Legacy prose such as `Governance profile` or `process_level: Managed` is not promoted into modern profile metadata and no separate-specification binding is inferred from prose references.

### Legacy raw completed group — exactly 19 paths

```text
docs/plans/wb-001-runtime-neutral-control-plane.md
docs/plans/wb-002-runtime-neutral-template-convergence.md
docs/plans/wb-003-codex-native-agents-and-gates.md
docs/plans/wb-004-integration-adapter-normalization.md
docs/plans/wb-005-profile-aware-bootstrap-conformance.md
docs/plans/wb-006-bootstrap-restore-hardening.md
docs/plans/wb-007-agent-evaluation-trajectory-assurance.md
docs/plans/wb-008-post-merge-ssot-release-gate.md
docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md
docs/plans/wb-010-skill-library-maintenance-integration.md
docs/plans/wb-core-001-normative-architecture.md
docs/plans/wb-core-002-portable-candidate-content.md
docs/plans/wb-core-002a-portable-candidate-review-remediation.md
docs/plans/wb-core-003-codex-local-control-plane-pilot.md
docs/plans/wb-core-003a-work-block-composition-and-flow-feedback.md
docs/plans/wb-core-003b-self-hosting-control-plane-reconciliation.md
docs/plans/wb-core-003c-completed-state-assurance-binding.md
docs/plans/wb-core-003d-parallel-write-set-orchestration.md
docs/plans/wb-core-003e-closure-evidence-correction.md
```

For all 19: **Profile = UNVERIFIED; separate-specification applicability/binding = UNVERIFIED; serial-promotion impact = not retroactively evaluated.** They remain unchanged raw historical records.

### Raw completed records with explicit modern profile metadata — exactly 10 paths

| Raw Work Block | Explicit profile | Separate-specification fact used here | Serial-promotion disposition |
|---|---|---|---|
| WB-OPENCODE-002 | Managed | no explicit separate-spec binding is established by the prior impact inventory | no retroactive promotion rule |
| WB-DESIGN-001 | Controlled | formal-profile separate-spec rule not used for this classification | no retroactive promotion rule |
| WB-DESIGN-002 | Controlled | formal-profile separate-spec rule not used for this classification | no retroactive promotion rule |
| WB-REPO-GRAPH-001 | Managed | `UNVERIFIED` binding; a spec path appearing in a write-set is not a normative binding | no retroactive promotion rule |
| WB-CORE-003F | Managed | no explicit separate-spec binding is established by the prior impact inventory | no retroactive promotion rule |
| WB-DEFINE-001 | Managed | no explicit separate-spec binding is established by the prior impact inventory | no retroactive promotion rule |
| WB-GIT-001 | Controlled | formal-profile separate-spec rule not used for this classification | no retroactive promotion rule |
| WB-SKILL-002 | Managed | explicit specification; current status approved prospectively, historical deviation retained | historical truth preserved |
| WB-SKILL-002A | Managed | explicit approved specification | historical completed record unchanged |
| WB-SKILL-002B | Managed | explicit approved specification | remains the raw latest completed predecessor at this baseline |

The exact reconciliation is therefore **19 legacy/unverified-profile raw records + 10 explicit-profile raw records = 29 raw completed records**. `WB-SKILL-001` exists historically but is **not** a path in the baseline `migration_state.completed_work_blocks` and is not counted or used to justify this transition.

### Active candidate and excluded pilot

| Record | Baseline state | Disposition |
|---|---|---|
| WB-RELEASE-001 | Managed `pre_closeout_candidate`; evidence-derived effective completion when its four exact reports and persistence proof validate; not raw completed | the single direct lifecycle subject requiring durable promotion before a successor candidate |
| WB-CORE-003G pilot projection | not part of the baseline registry candidate/completed state | do not mutate, register, repair, or relabel from WB-RELEASE-002 |

**Historical impact classification: BOUNDED COLLATERAL IMPACT.** The exact raw inventory is reconciled without retroactive profile/spec inference. None of the 29 raw completed records is migrated by this design. The direct transition impact is the one WB-RELEASE-001 effective candidate; the new invariant applies prospectively to promoted-candidate history and later candidates only.

## Selected prospective transition model

The draft design selects a **canonical append-only promotion ledger in `FILE_REGISTRY.yml:migration_state`**, mirrored by the release-state projection in `PROJECT_MAP.md`. Direct promotion into `completed_work_blocks` is rejected because it would convert evidence-derived completion into a raw historical fact that the original Work Block never recorded.

The future field name may be implementation-refined, but its semantics are fixed by this specification: an ordered promoted-candidate ledger is separate from raw `completed_work_blocks` and is canonical machine state.

### Promotion and successor sequence

1. **Current candidate validation:** there is zero or one `pre_closeout_candidate`; if present, current WB-RELEASE-001 evidence/persistence and current-HEAD normative-manifest checks must pass before promotion.
2. **Promotion revision:** append exactly one immutable promotion record for that candidate to the ordered promotion ledger and clear `pre_closeout_candidate`; do not change `completed_work_blocks` or historical Work Block status/timing. `PROJECT_MAP.md` must mirror the resulting migration state.
3. **Post-promotion ordinary validation:** ordinary mode must validate the ledger record, its exact candidate/evidence revisions, evidence paths, normative manifest, uniqueness, ordering, and predecessor continuity. The promoted Work Block becomes the effective latest completed entry through the ledger, not through raw-history mutation.
4. **Separate successor declaration revision:** only after the promotion revision validates in ordinary mode may a next `pre_closeout_candidate` be declared.
5. **Deterministic predecessor rule:** every new candidate's predecessor must equal the `effective_latest_completed_work_block` from the immediately preceding validated state. At the current baseline that is WB-SKILL-002B before WB-RELEASE-001 becomes effective; after WB-RELEASE-001 promotion it is WB-RELEASE-001 for the next candidate.
6. **Serialization:** a promotion record and a successor candidate may not be introduced as an ambiguous combined transition that bypasses validation of the promotion state; promotion precedes successor declaration in repository history.
7. **Uniqueness:** the same Work Block ID/path may not appear more than once across promoted history or simultaneously as promoted and active candidate; raw/promoted overlap is rejected unless a future separately approved migration contract explicitly defines it.
8. **Append-only history:** deletion, mutation, or reordering of a prior promotion record fails closed.
9. **Existing safety preserved:** incomplete evidence, stale manifests, candidate/active coexistence, malformed map/registry projection, invalid predecessor, duplicate candidate, or ambiguous promotion ancestry remains `BLOCKED`, never `READY`.

This is a draft architecture/specification choice, not Execute authority. Replacing the ledger with direct raw-history mutation or a separate canonical artifact is a material specification change and must return to Define/Owner approval rather than being selected during coding.

## Proposed future implementation write-set — exactly six paths, not authorized

| Path | Owner / defect | Smallest sufficient future change | Why required |
|---|---|---|---|
| `governance/release-state.md` | Architect; missing serial promotion semantics | define ordered promotion-ledger contract, effective history, promotion revision, and effective-predecessor rule | policy must exist before code enforcement |
| `scripts/validate-release-state.py` | deterministic release-state owner | validate append-only promoted history, exact evidence/manifest binding, uniqueness, ordering, and successor predecessor continuity | existing validator owns raw/effective release-state derivation |
| `scripts/test-release-state-contracts.py` | release-state fixture owner | add positive and adversarial promotion/next-candidate fixtures | regression proof belongs beside the validator |
| `FILE_REGISTRY.yml` | canonical machine migration state | add the ordered promoted-candidate history and use it for the actual future transition | selected design requires durable machine-readable history |
| `PROJECT_MAP.md` | human projection of migration state | mirror promoted history and candidate state consistently with the registry | current release-state contract requires registry/map agreement |
| `.agent/workflows/sdd-protocol.md` | self-hosting lifecycle procedure | add the operational promotion → ordinary validation → separate next-candidate sequence | the existing protocol currently stops after evidence persistence/ordinary validation |

No source or canonical path above is authorized for Execute by this Define correction. A later Owner decision must approve the specification revision and exact implementation write-set after Define-quality evidence and Critic are resolved.

## Define quality state

- **Required:** yes — Managed formal specification.
- **Requirements Review:** PENDING — rerun against corrected Define revision.
- **Traceability:** PENDING — rerun against corrected Define revision.
- **Consistency Analysis:** PENDING — rerun after requirements review/traceability.
- **Aggregate:** PENDING.

## Gates and authority

- **Write Gate:** BLOCKED.
- **Critic Gate:** PENDING.
- **Review Gate:** PENDING.
- **Verification Verdict:** PENDING.
- **Drift Gate:** PENDING.
- **Evaluation Verdict:** NOT_REQUIRED — deterministic governance/release-state lifecycle design introduces no non-deterministic product behavior.
- **Closeout Mode:** pending.

## Acceptance criteria

- [ ] AC-001 [req=REQ-001]: The inventory reconciles exactly 29 raw completed paths as 19 legacy records with structured profile/spec facts left `UNVERIFIED` plus 10 records with explicit modern profile metadata, separately identifies WB-RELEASE-001 as the sole active candidate, and does not count WB-SKILL-001 or WB-CORE-003G as baseline raw completed state.
- [ ] AC-002 [req=REQ-002]: The specification requires a separate validated promotion revision that appends an immutable WB-RELEASE-001 promotion record, preserves its exact evidence/manifest bindings and effective-completion meaning, clears the active candidate declaration, and leaves raw `completed_work_blocks` unchanged before any successor candidate revision.
- [ ] AC-003 [req=REQ-003]: The future state model permits at most one active candidate, and a successor candidate is accepted only when its predecessor equals the effective latest completed Work Block from the immediately preceding validated promotion state.
- [ ] AC-004 [req=REQ-004]: Promotion is rejected unless all four required evidence classes bind the exact candidate, the evidence-persistence proof is valid, and every normative-manifest path remains unchanged at the promotion subject.
- [ ] AC-005 [req=REQ-005]: Ordinary validation rejects incomplete, duplicated, malformed, reordered, deleted, stale, concurrently active, invalid-predecessor, raw/promoted-overlap, or ambiguous promotion state.
- [ ] AC-006 [req=REQ-006]: Promoting a candidate retains immutable evidence and exact candidate/evidence revision bindings without changing any raw historical Work Block lifecycle status/timing or appending the candidate to raw `completed_work_blocks`.
- [ ] AC-007 [req=REQ-007]: The new promotion invariant applies prospectively and does not migrate the 29 historical raw records, register/mutate WB-CORE-003G, or relabel historical evidence.
- [ ] AC-008 [req=REQ-008]: The proposed future implementation write-set is exactly the six owner-mapped paths above and remains unauthorized until a later Owner approval after Define-quality and Critic evidence.
- [ ] AC-009 [req=REQ-009]: The future fixture plan covers successful promotion followed by a valid next candidate plus incomplete evidence, stale manifest, duplicate promotion, promotion-record mutation/deletion/reordering, candidate/promoted duplication, raw/promoted overlap, invalid effective predecessor, candidate/active coexistence, map disagreement, and an attempted combined transition that bypasses a validated promotion state.

## Assumptions and Owner boundary

- The current Owner instruction authorizes correction/persistence of these three Define artifacts only; no Execute/source/canonical projection or PR/merge/thread authority is implied.
- The draft selects the registry promotion-ledger representation to remove implementation ambiguity. It is not authoritative for Execute until a later Owner approval makes the corrected specification authoritative.
- Historical records without structured `governance_profile` or explicit separate-specification binding remain `UNVERIFIED`; legacy prose is not converted into modern metadata.
- Any future proposal to mutate raw `completed_work_blocks` for candidate-derived completion, use a different canonical promotion store, or collapse promotion and successor declaration into one unvalidated state transition is a material specification change and returns to Define.

## Implementation plan

| Task | Owner Role | Write-Set | Dependencies | Expected Evidence | Status |
|---|---|---|---|---|---|
| Correct inventory, select transition model, refresh requirements and proposed write-set | Architect | three WB-RELEASE-002 Define artifacts | baseline registry/governing contracts | corrected specification, plan, tasklist | in_progress |
| Requirements-quality review | Requirements Reviewer | read-only report path | corrected Define artifacts | independent requirements verdict | planned |
| Structural traceability | Requirements Reviewer / deterministic validator | read-only command result | corrected spec/tasklist | `READY requirements=9 acceptance=9 tasks=15` | planned |
| Consistency analysis | Architect/Reviewer | read-only report path | requirements review + traceability | spec/plan/task/write-set consistency verdict | planned |
| Critic review | Critic | read-only report path | Define-quality evidence | Critic verdict | planned |
| Future Execute | Coder | only later Owner-approved exact six-path write-set | approved specification and resolved gates | implementation and tests | blocked |

