---
schema_version: 1
artifact_type: work_block
artifact_id: wb-release-002-candidate-promotion-lifecycle
work_block_id: WB-RELEASE-002
status: completed
owner_role: Owner
created_at: 2026-08-25
last_updated: 2026-09-01
governance_profile: Managed
branch: agent/wb-release-002-candidate-promotion
base_revision: 73cd1cab36af327683991c768ea887911547df06
write_gate: BLOCKED
critic_gate: READY
review_gate: READY
verification_verdict: READY
drift_gate: ALIGNED
evaluation_verdict: SKIPPED
closeout_mode: success-closeout
owner_approval: Owner approved the corrected Define and Phase A mechanism enablement on 2026-08-30, then separately authorized the dedicated Phase B canonical promotion transition. The completed repository record does not grant push, PR mutation, merge, deployment, cleanup, or other external authority.
---

# WB-RELEASE-002 — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Stage and objective

- **Current Stage:** Close
- **Stage State:** completed
- **Role:** Orchestrator → Coder → Reviewer / Verifier / Drift Auditor
- **Objective:** complete and assure the approved fail-closed serial candidate
  lifecycle, including the separately Owner-authorized Phase B promotion from
  an evidence-complete `pre_closeout_candidate` to durable promoted history,
  without weakening ordinary release-state validation.

## Context and confirmed trigger

The accepted WB-RELEASE-001 contract supports one local `pre_closeout_candidate` and derives effective completion only after four exact evidence artifacts bind the candidate. It does not specify how that effective candidate is durably promoted before another candidate is declared. The WB-CORE-003G pilot exposed the resulting sequencing gap: a successor cannot truthfully become the next candidate while the prior evidence-complete candidate remains the sole active candidate declaration and the existing predecessor rule still points only at raw completed history.

This Work Block specified and implemented that missing prospective transition,
then completed the separately authorized canonical promotion. It does not repair
WB-CORE-003G, rewrite WB-RELEASE-001, or relabel historical evidence.

## Expected final result

One serial candidate lifecycle is implemented and assured with explicit
promotion prerequisites, append-only effective-completion history, exact
effective-predecessor binding, and a fail-closed two-revision
promotion/next-candidate transition. The final assured Phase B projection is
`df2304dee157f5b22374b6d32c6274e053730c53`: WB-RELEASE-001 is the sole
`promoted_effective` ledger record, its candidate slot is cleared, all 29 raw
completed records remain unchanged, and no successor candidate is declared.
No evidence or Owner decision is fabricated.

## Done criteria for Define

- [x] Current release-state candidate and all 29 raw completed records are reconciled from the baseline registry.
- [x] Historical impact is classified without inferring missing profile/specification metadata.
- [x] A prospective serial transition model and deterministic predecessor rule are selected.
- [x] Future implementation owners and smallest proposed write-set are recorded.
- [x] Requirements, acceptance criteria, and tasklist are structurally traceable.
- [x] Fresh read-only Requirements Review, Consistency Analysis, and Critic review are complete; their verdicts are recorded below because this correction cannot create separate report artifacts.

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

The draft design selects the exact canonical machine field **`FILE_REGISTRY.yml:migration_state.promoted_candidates`**; `PROJECT_MAP.md` is its derived projection, not a second SSOT. Direct promotion into `completed_work_blocks` is rejected because it would convert evidence-derived completion into a raw historical fact; clearing the candidate without durable history loses effective-predecessor continuity; a separate canonical artifact would create an unnecessary second SSOT.

`promoted_candidates` is an ordered append-only list. Its absence is valid only before the first promotion; thereafter it must be non-empty, ordered, retained, and projected exactly. Each record has exactly these semantic fields (final serialization syntax is YAML):

```text
work_block
work_block_id
predecessor_effective_work_block
candidate_revision
evidence_revision
required_evidence
normative_manifest
state: promoted_effective
```

`required_evidence` retains the existing four evidence classes/paths. `candidate_revision` and `evidence_revision` bind the already-proved candidate/evidence pair. `normative_manifest` remains the candidate's assured ordered manifest; it is not rewritten to pretend that the later promotion projections were part of the candidate subject.

### Promotion and successor sequence

1. **Validated promotion parent:** the sole direct parent of a promotion must pass ordinary release-state validation with exactly one evidence-complete candidate derived as effective. At that parent, the existing evidence-persistence proof and current-HEAD candidate normative-manifest checks must already pass.
2. **Dedicated promotion transition:** its one-parent child appends exactly one record to `migration_state.promoted_candidates` and clears `pre_closeout_candidate`. The promotion revision may change exactly `FILE_REGISTRY.yml` and `PROJECT_MAP.md`; `completed_work_blocks`, the candidate Work Block, all four evidence artifacts, and every other path remain unchanged.
3. **Cross-revision promotion proof:** a deterministic discovery of the unique first commit that introduces each ledger record must verify its one direct parent, exact two-path delta, copied candidate/evidence/manifest bindings, append-only ledger growth by one record, candidate-slot clearing, registry/map agreement, and no other change. Merge-based or ambiguous discovery fails closed.
4. **Post-promotion ordinary validation:** ordinary mode validates the new ledger record, its candidate/evidence revisions, evidence paths, historical normative-manifest binding through the parent, uniqueness, ordering, and predecessor continuity. The promoted Work Block becomes the durable effective latest completed entry through the ledger, not raw-history mutation.
5. **Separate successor declaration revision:** only after the promotion revision itself validates in ordinary mode may a next `pre_closeout_candidate` be declared through the existing `predecessor_completed_work_block` field, whose prospective meaning is effective latest; a second/legacy-alternative predecessor field is rejected.
6. **Deterministic ordering:** raw `completed_work_blocks` is frozen once promoted history begins. New Work Blocks may still be declared, executed, and ordinarily validated, but their managed completion proceeds through candidate then separately validated promotion, so the ledger supplies the unambiguous effective-history continuation.
7. **Serialization:** a promotion record and a successor candidate may not be introduced as an ambiguous combined transition that bypasses validation of the promotion state; promotion precedes successor declaration in repository history.
8. **Uniqueness and append-only history:** the same Work Block ID/path may not appear more than once in promoted history or simultaneously as promoted and active candidate; raw/promoted overlap, deletion, mutation, or reordering of a prior promotion record fails closed.
9. **Existing safety preserved:** incomplete evidence, stale pre-promotion manifests, candidate/active coexistence, malformed map/registry projection, invalid predecessor, duplicate candidate, or ambiguous promotion ancestry remains `BLOCKED`, never `READY`.

This is a draft architecture/specification choice, not Execute authority. Replacing `promoted_candidates` with direct raw-history mutation or a separate canonical artifact is a material specification change and must return to Define/Owner approval rather than being selected during coding.

## Proposed future implementation write-set — exactly four paths, not authorized

| Path | Owner / defect | Smallest sufficient future change | Why required |
|---|---|---|---|
| `governance/release-state.md` | Architect; missing serial promotion semantics | define `promoted_candidates`, promotion-parent proof, exact transition delta, effective history, and effective-predecessor rule | policy must exist before code enforcement |
| `scripts/validate-release-state.py` | deterministic release-state owner | validate append-only promoted history, pre-promotion evidence/manifest integrity, exact promotion transition, uniqueness, ordering, and successor predecessor continuity | existing validator owns raw/effective release-state derivation |
| `scripts/test-release-state-contracts.py` | release-state fixture owner | add positive and adversarial promotion/next-candidate fixtures | regression proof belongs beside the validator |
| `.agent/workflows/sdd-protocol.md` | self-hosting lifecycle procedure | add validated-parent → promotion proof → ordinary validation → separate next-candidate sequence | the existing protocol currently stops after evidence persistence/ordinary validation |

The four paths above implement the contract. Separately, the future operational promotion transition is exactly `FILE_REGISTRY.yml` plus `PROJECT_MAP.md`, after implementation validates and only under its own Owner gate; it is not part of the implementation write-set and cannot be bundled with successor declaration. No source or canonical path is authorized by this Define correction.

## Define quality state

- **Required:** yes — Managed formal specification.
- **Requirements Review:** READY — fresh independent read-only re-review of the corrected three-file subject.
- **Traceability:** READY — `python3 scripts/validate-define-traceability.py` reported `requirements=9 acceptance=9 tasks=15`.
- **Consistency Analysis:** READY — fresh independent read-only analysis of the corrected three-file subject and governing contracts.
- **Aggregate:** READY — evidence is Define-only and does not grant Execute authority.

## Final closeout state

- **Current Stage:** Close
- **Stage State:** completed
- **Write Gate:** BLOCKED — source and canonical mutation authority is closed.
- **Critic Gate:** READY — Define Critic `APPROVE` remains recorded advisory evidence.
- **Review Gate:** READY — independent final projection review of
  `df2304dee157f5b22374b6d32c6274e053730c53`.
- **Verification Verdict:** READY — fresh remote-only verification of the same
  final projection subject.
- **Drift Gate:** ALIGNED — final projection and its authoritative release-state
  sources agree.
- **Evaluation Verdict:** SKIPPED — this deterministic governance and
  release-state contract change has no non-deterministic product behavior that
  requires a separate evaluation.
- **Closeout Mode:** success-closeout.
- **External VCS State:** non-normative; this repository closeout makes no
  push, PR, merge, CI, or deployment claim.

## Acceptance criteria

- [x] AC-001 [req=REQ-001]: The inventory reconciles exactly 29 raw completed paths as 19 legacy records with structured profile/spec facts left `UNVERIFIED` plus 10 records with explicit modern profile metadata, separately identifies WB-RELEASE-001 as the sole active candidate, and does not count WB-SKILL-001 or WB-CORE-003G as baseline raw completed state.
- [x] AC-002 [req=REQ-002]: The specification requires a separately validated promotion parent and a promotion revision that appends exactly one `promoted_candidates` record, clears the active candidate declaration, changes exactly `FILE_REGISTRY.yml` and `PROJECT_MAP.md`, and leaves raw `completed_work_blocks`, candidate/evidence artifacts, and every other path unchanged before any successor candidate revision.
- [x] AC-003 [req=REQ-003]: The future state model permits at most one active candidate, and a successor candidate uses the canonical `predecessor_completed_work_block` field with the effective latest completed Work Block from the immediately preceding validated promotion state; no alternate predecessor field is allowed.
- [x] AC-004 [req=REQ-004]: Promotion is rejected unless the parent state already proves all four exact candidate-bound evidence classes, valid evidence persistence, and unchanged candidate normative manifest, and unless the parent→promotion comparison proves the exact two-path registry/map transition with no other delta.
- [x] AC-005 [req=REQ-005]: Ordinary validation rejects incomplete, duplicated, malformed, reordered, deleted, stale, concurrently active, invalid-predecessor, raw/promoted-overlap, absent/null/empty post-promotion ledger, merge-based/ambiguous promotion ancestry, or ambiguous promotion state.
- [x] AC-006 [req=REQ-006]: Promoting a candidate retains immutable candidate/evidence/manifest bindings through the promotion record without changing any raw historical Work Block lifecycle status/timing or appending the candidate to raw `completed_work_blocks`; raw history is frozen after the first promotion.
- [x] AC-007 [req=REQ-007]: The new promotion invariant applies prospectively and does not migrate the 29 historical raw records, register/mutate WB-CORE-003G, or relabel historical evidence.
- [x] AC-008 [req=REQ-008]: The proposed future implementation write-set is exactly the four owner-mapped implementation paths; the exact two-path registry/map promotion transition is separately Owner-gated and neither set is authorized by this Define correction.
- [x] AC-009 [req=REQ-009]: The future fixture plan covers successful validated-parent promotion followed by a valid next candidate plus incomplete evidence, stale pre-promotion manifest, forbidden extra transition path, duplicate promotion, promotion-record mutation/deletion/reordering, candidate/promoted duplication, raw/promoted overlap, invalid effective predecessor, candidate/active coexistence, map disagreement, and an attempted combined transition that bypasses a validated promotion state.

## Assumptions and Owner boundary

- The Owner first authorized the corrected Define and exact four-path Phase A mechanism, then separately authorized the completed exact two-path canonical promotion. Neither approval grants push, PR/merge/thread, deployment, cleanup, or successor-declaration authority.
- The completed implementation uses `migration_state.promoted_candidates` as the only canonical promotion-history store, with `PROJECT_MAP.md` derived from it; `FILE_REGISTRY.yml` remains the lifecycle SSOT.
- Historical records without structured `governance_profile` or explicit separate-specification binding remain `UNVERIFIED`; legacy prose is not converted into modern metadata.
- Any future proposal to mutate raw `completed_work_blocks` for candidate-derived completion, resume raw-history appends after promotion begins, use a different canonical promotion store, change predecessor serialization, or collapse promotion and successor declaration into one unvalidated state transition is a material specification change and returns to Define.

## Implementation plan

| Task | Owner Role | Write-Set | Dependencies | Expected Evidence | Status |
|---|---|---|---|---|---|
| Correct inventory, select transition model, refresh requirements and proposed write-set | Architect | three WB-RELEASE-002 Define artifacts | baseline registry/governing contracts | corrected specification, plan, tasklist | completed |
| Requirements-quality review | Requirements Reviewer | read-only verdict recorded in this plan | corrected Define artifacts | `READY` | completed |
| Structural traceability | Requirements Reviewer / deterministic validator | read-only command result | corrected spec/tasklist | `READY requirements=9 acceptance=9 tasks=15` | completed |
| Consistency analysis | Architect/Reviewer | read-only verdict recorded in this plan | requirements review + traceability | `READY` | completed |
| Critic review | Critic | read-only verdict recorded in this plan | Define-quality evidence | `APPROVE` | completed |
| Phase A mechanism Execute | Coder | exact four-path implementation write-set | Owner-approved Define baseline | implementation and deterministic fixture suite | completed |
| Future promotion transition | Coder | separately Owner-authorized exact two-path registry/map transition | validated implementation and ordinary-valid promotion parent | exact transition proof and ordinary validation | completed |
| Final independent assurance and Close synchronization | Reviewer / Verifier / Drift Auditor / Coder | read-only assurance plus approved Close documentation paths | frozen final projection `df2304dee157f5b22374b6d32c6274e053730c53` | Review READY, Verification READY, Drift ALIGNED, success-closeout record | completed |
