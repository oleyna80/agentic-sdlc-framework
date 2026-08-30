---
schema_version: 1
artifact_type: specification
artifact_id: wb-release-002-candidate-promotion-lifecycle
work_block_id: WB-RELEASE-002
status: approved
created_at: 2026-08-25
revision: owner-approved-define-r4-2026-08-30
owner_approval: Owner approved this corrected Define as authoritative and authorized only Phase A mechanism enablement in governance/release-state.md, scripts/validate-release-state.py, scripts/test-release-state-contracts.py, and .agent/workflows/sdd-protocol.md on 2026-08-30. FILE_REGISTRY.yml, PROJECT_MAP.md, actual promotion, push, PR mutation, merge, deployment, cleanup, and all other paths remain blocked pending separate Owner authority.
---

# WB-RELEASE-002 — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Purpose and authority boundary

This draft specification defines the missing lifecycle transition exposed after WB-RELEASE-001 introduced a single evidence-bound `pre_closeout_candidate`: an evidence-complete candidate needs a durable, truthful promotion state before a successor candidate can be declared.

This approved Define authorizes only Phase A mechanism enablement in its exact four-path write-set. It is not authority to modify registry/map canonical state, historical Work Blocks, evidence, actual promotion, successor declaration, push, PR mutation, merge, deployment, cleanup, or any other path.

The design preserves four distinct concepts:

1. raw historical `completed_work_blocks`;
2. evidence-derived effective completion;
3. the zero-or-one active `pre_closeout_candidate`;
4. append-only `promoted_candidates` history.

Candidate-derived completion must never be silently rewritten into raw history.

## Requirements

- REQ-001: The lifecycle inventory and future state model must distinguish repository-proven raw completed state, evidence-derived effective completion, active candidate state, and promoted-candidate history. The baseline inventory must reconcile all 29 raw completed paths exactly. Missing or contradictory historical profile/specification metadata must be reported as `UNVERIFIED` rather than inferred from legacy prose, `process_level`, write-sets, or path references.
- REQ-002: Before a successor candidate is declared, the prior evidence-complete candidate must pass a separate deterministic promotion transition from its sole direct parent, which already validates ordinary `READY` with that candidate derived as effective. The promotion revision must append exactly one immutable record to `FILE_REGISTRY.yml:migration_state.promoted_candidates`, clear `pre_closeout_candidate`, change exactly `FILE_REGISTRY.yml` and `PROJECT_MAP.md`, and leave raw `completed_work_blocks`, the candidate Work Block, evidence artifacts, and every other path unchanged.
- REQ-003: The state model must allow at most one active `pre_closeout_candidate`. Retain the single canonical successor field name `predecessor_completed_work_block`, but define its prospective meaning as the `effective_latest_completed_work_block` from the immediately preceding validated repository state; no second/legacy-alternative predecessor field is permitted. Promotion must validate before a separate successor-declaration revision; coding may not use raw-latest when promoted effective history exists.
- REQ-004: The promotion parent must already satisfy the existing four evidence classes with required verdicts, exact candidate-subject binding, valid evidence-persistence ancestry/proof, and current-HEAD equality for the candidate normative manifest. The commit that first introduces each promotion record must have exactly one direct parent, be uniquely discoverable from the retained append-only history, and be compared with that parent. The comparison must prove the exact two-path registry/map transition, exact copied candidate/evidence/manifest bindings, append-only growth by one record, candidate-slot clearing, and no other delta. Missing, stale, wrong-subject, mutated, merge-based, or ambiguous pre-promotion state must reject promotion.
- REQ-005: Ordinary release-state validation must remain fail-closed for duplicate active candidates, candidate/active coexistence, malformed registry/map projection, missing evidence, stale pre-promotion manifests, invalid effective predecessors, duplicate promotion records, mutation/deletion/reordering of prior promoted history, candidate/promoted duplication, raw/promoted overlap, forbidden promotion-transition paths, absent/null/empty ledger after the first promotion, or an ambiguous/combined promotion-plus-successor transition that bypasses validation of the promotion state.
- REQ-006: `promoted_candidates` is the sole canonical promotion-history store and must be append-only; `PROJECT_MAP.md` is its derived projection only. It retains immutable candidate/evidence revision bindings, evidence references, and the original assured normative manifest. Promotion must not change historical Work Block lifecycle status/timing, relabel historical evidence, or append a candidate-derived completion to raw `completed_work_blocks`. Before the first promotion, an absent ledger is valid; thereafter the ledger must be non-empty, ordered, and retained. Raw `completed_work_blocks` is prospectively frozen once promoted history begins, so every subsequent managed completion uses the candidate → promotion path and effective completion is deterministically raw-history prefix plus ordered promoted history, plus the temporary evidence-complete candidate where permitted.
- REQ-007: The invariant is prospective and transition-scoped. It must not force any of the 29 baseline raw completed records into a retroactive promotion migration, infer missing historical profile/specification authority, register or mutate WB-CORE-003G, or bring WB-CORE-003G/unrelated historical corrections into this Work Block.
- REQ-008: The future implementation write-set is exactly four paths: `governance/release-state.md`, `scripts/validate-release-state.py`, `scripts/test-release-state-contracts.py`, and `.agent/workflows/sdd-protocol.md`. The separate operational promotion transition is exactly `FILE_REGISTRY.yml` plus `PROJECT_MAP.md`, occurs only after implementation is validated and a later Owner gate authorizes that transition, and is not part of the implementation write-set. Each path remains owner-mapped to the smallest sufficient change; this draft authorizes none of them.
- REQ-009: The future contract suite must deterministically exercise successful validated-parent promotion followed by a valid next-candidate declaration and adversarial cases for incomplete/wrong evidence, stale pre-promotion manifests, forbidden extra transition paths, duplicate or mutated promoted history, deletion/reordering, candidate/promoted duplication, raw/promoted overlap, invalid effective predecessor, candidate/active coexistence, map disagreement, and attempted promotion/successor collapse without an intervening validated promotion state.

## Acceptance criteria

- AC-001 [req=REQ-001]: The approved design reconciles exactly 29 raw completed paths as 19 records whose structured profile/specification applicability remains `UNVERIFIED` plus 10 raw records with explicit modern `governance_profile`; it separately identifies WB-RELEASE-001 as the candidate and does not count WB-SKILL-001 or WB-CORE-003G as baseline raw completed state.
- AC-002 [req=REQ-002]: Given a parent revision where ordinary validation derives evidence-complete WB-RELEASE-001 as effective latest, a one-parent promotion revision appends exactly one `promoted_candidates` record, clears `pre_closeout_candidate`, changes exactly `FILE_REGISTRY.yml` and `PROJECT_MAP.md`, and leaves raw `completed_work_blocks`, the candidate Work Block, all four evidence artifacts, and every other path unchanged before any successor candidate revision.
- AC-003 [req=REQ-003]: After the promotion revision validates in ordinary mode, a separately created successor uses the canonical `predecessor_completed_work_block` field with WB-RELEASE-001 as its effective latest value; a second predecessor field or a successor pointing to the older raw latest WB-SKILL-002B is rejected.
- AC-004 [req=REQ-004]: Promotion is rejected unless its uniquely discoverable one-parent commit has a parent that already proves all required exact-bound evidence, valid evidence persistence, and unchanged candidate normative manifest, and unless the parent→promotion comparison proves one appended record, candidate-slot clearing, registry/map agreement, and exactly the two allowed transition paths with no other delta.
- AC-005 [req=REQ-005]: Ordinary validation rejects incomplete, duplicate, malformed, reordered, deleted, stale, concurrently active, invalid-predecessor, candidate/promoted-overlap, raw/promoted-overlap, absent/null/empty post-promotion ledger, forbidden-transition-path, map-disagreement, or unvalidated combined-transition state; candidate mode continues to emit only its distinct candidate classification and cannot emit ordinary `READY`.
- AC-006 [req=REQ-006]: The promoted record retains exact immutable candidate/evidence revisions, evidence references, predecessor, and original normative manifest while the original Work Block and raw `completed_work_blocks` retain their historical status, timing, and membership; after first promotion raw history is frozen and future managed completion order is the promoted ledger order.
- AC-007 [req=REQ-007]: No new validator rule performs a retroactive global migration or metadata inference; WB-CORE-003G and unrelated historical corrections remain explicitly excluded.
- AC-008 [req=REQ-008]: The implementation plan names the owning contract, smallest change, and rationale for the exact four-path implementation write-set and separately records the exact two-path promotion transition, neither of which is authorized until its later Owner gate.
- AC-009 [req=REQ-009]: Deterministic fixtures cover one successful validated-parent promotion and valid successor plus every adversarial class named in REQ-009, including a successor that incorrectly uses raw latest instead of promoted effective latest and a combined transition without an independently validated promotion state.

## Baseline historical impact and scope decision

The baseline registry contains exactly 29 raw completed Work Blocks and one `pre_closeout_candidate`:

- the first 19 raw entries, from WB-001 through WB-CORE-003E, have no structured modern `governance_profile`; their profile and separate-spec applicability remain `UNVERIFIED`, regardless of legacy prose or `process_level` values;
- the remaining 10 raw entries have explicit modern profiles: WB-OPENCODE-002, WB-DESIGN-001, WB-DESIGN-002, WB-REPO-GRAPH-001, WB-CORE-003F, WB-DEFINE-001, WB-GIT-001, WB-SKILL-002, WB-SKILL-002A, and WB-SKILL-002B;
- WB-SKILL-001 is not a baseline `completed_work_blocks` member and is not counted;
- WB-RELEASE-001 is the one candidate/effective-completion subject and is not raw completed;
- WB-CORE-003G is not part of the baseline completed/candidate registry state.

Historical impact is therefore **BOUNDED COLLATERAL IMPACT**: the new rule does not migrate any raw historical record. It supplies a prospective transition for WB-RELEASE-001 and later candidates only.

## Selected state representation

The exact proposed canonical machine field is `FILE_REGISTRY.yml:migration_state.promoted_candidates`; `PROJECT_MAP.md` is its derived projection and never an independent lifecycle authority. It is an ordered append-only list. Before the first promotion, the field is absent; once promoted history begins it must be present, non-empty, ordered, and immutable. Each record contains:

```yaml
work_block: <repository-relative Work Block path>
work_block_id: <Work Block ID>
predecessor_effective_work_block: <prior effective latest Work Block path>
candidate_revision: <40-hex candidate commit>
evidence_revision: <40-hex evidence-persistence commit>
required_evidence:
  review: <path>
  verification: <path>
  drift: <path>
  closeout: <path>
normative_manifest:
  - <ordered candidate manifest path>
state: promoted_effective
```

The promotion record binds the already-assured candidate and evidence pair. The candidate's original normative manifest remains historical binding data. It is validated at the promotion parent; the later promotion revision intentionally changes registry/map projection and therefore does not pretend those two post-transition blobs were part of the earlier assured candidate subject.

Promotion and successor declaration are separate repository revisions:

1. a sole direct parent validates the candidate as effective and proves its current normative manifest;
2. its one-parent promotion child changes exactly registry/map, appends one record, and clears the candidate;
3. a cross-revision promotion proof uniquely discovers and validates that exact parent/child transition;
4. the promotion revision passes ordinary validation with the ledger-derived effective latest;
5. only then may a later revision declare the successor through the existing `predecessor_completed_work_block` field, whose prospective meaning is effective latest.

Raw `completed_work_blocks` is frozen after the first promotion. New Work Blocks may still be declared, executed, and ordinarily validated, but their managed completion uses the serial candidate → separately validated promotion route, which makes the ordered ledger the unambiguous future effective-history continuation. Directly appending candidate-derived completion to raw history, using a different canonical promotion store, changing an extra path in the promotion transition, or combining promotion and successor declaration so that the intermediate promoted state is never validated is outside this specification.

## Future implementation and transition boundaries — proposed, exact, unauthorized

- `governance/release-state.md` — define `promoted_candidates`, promotion-parent requirements, exact cross-revision transition proof, effective-history derivation, append-only semantics, and effective-predecessor rule.
- `scripts/validate-release-state.py` — enforce pre-promotion evidence/manifest integrity, exact two-path promotion transition, ledger uniqueness/order/immutability, effective-history derivation, and successor predecessor continuity.
- `scripts/test-release-state-contracts.py` — prove positive and adversarial promotion/next-candidate behavior.
- `.agent/workflows/sdd-protocol.md` — prescribe validated parent → promotion proof → ordinary validation → separate successor declaration sequencing.

Those four paths are authorized only for Phase A mechanism enablement. Separately, an already-validated implementation may later use the exact two-path operational promotion transition: `FILE_REGISTRY.yml` (canonical state) and `PROJECT_MAP.md` (derived projection). That two-path revision needs its own Owner authorization and cannot be bundled with implementation or successor declaration. The two canonical transition paths remain blocked.

## Verification boundary

Corrected Define revision `owner-approved-define-r4-2026-08-30` has fresh independent Requirements Review `READY`, structural traceability, Consistency Analysis `READY`, and Critic `APPROVE`. The Owner has accepted those results and opened the restricted Phase A Write/Execute Gate; Phase B remains blocked. Structural traceability is:

```text
READY
requirements=9 acceptance=9 tasks=15
```

Independent Reviewer, fresh-clone Verifier, and Drift assurance apply later to the frozen implementation subject. Evaluation is not required because the target is deterministic governance/tooling lifecycle behavior with no non-deterministic product behavior.

## Non-goals

- Do not change WB-RELEASE-001 or any of its historical/source/final evidence from this Define revision.
- Do not repair, register, promote, or relabel WB-CORE-003G from this Work Block.
- Do not alter existing candidate validation merely to make an invalid intermediate state pass.
- Do not infer external Owner approval, historical governance profile, or historical specification authority.
- Do not retroactively add candidate-derived completion to raw `completed_work_blocks`.
- Do not address Gemini recommendations, converge loops, context pruning, extensions, presets, workflows, bundles, or unrelated legacy cleanup.
