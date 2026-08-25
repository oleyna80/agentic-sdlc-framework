---
schema_version: 1
artifact_type: specification
artifact_id: wb-release-002-candidate-promotion-lifecycle
work_block_id: WB-RELEASE-002
status: draft
created_at: 2026-08-25
revision: define-r2-2026-08-25
owner_approval: Owner authorized correction of the WB-RELEASE-002 Define findings on 2026-08-25. This revision remains draft and grants no source-write, canonical-projection, pull request, merge, or thread-resolution authority.
---

# WB-RELEASE-002 — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Purpose and authority boundary

This draft specification defines the missing lifecycle transition exposed after WB-RELEASE-001 introduced a single evidence-bound `pre_closeout_candidate`: an evidence-complete candidate needs a durable, truthful promotion state before a successor candidate can be declared.

This revision is not approved for Execute. It is not authority to modify release-state policy, validators, registry, map, protocol, historical Work Blocks, or evidence. The future source/canonical write-set remains blocked until independent Define-quality evidence, Critic, and a later Owner approval resolve the normal Managed Write Gate.

The design preserves four distinct concepts:

1. raw historical `completed_work_blocks`;
2. evidence-derived effective completion;
3. the zero-or-one active `pre_closeout_candidate`;
4. append-only promoted-candidate history.

Candidate-derived completion must never be silently rewritten into raw history.

## Requirements

- REQ-001: The lifecycle inventory and future state model must distinguish repository-proven raw completed state, evidence-derived effective completion, active candidate state, and promoted-candidate history. The baseline inventory must reconcile all 29 raw completed paths exactly. Missing or contradictory historical profile/specification metadata must be reported as `UNVERIFIED` rather than inferred from legacy prose, `process_level`, write-sets, or path references.
- REQ-002: Before a successor candidate is declared, the prior evidence-complete candidate must pass a separate deterministic promotion transition. That transition must append an immutable evidence-bound promotion record to canonical machine history, clear the prior active candidate declaration, preserve its exact Work Block/evidence/normative-manifest/effective-completion meaning, and leave raw `completed_work_blocks` unchanged.
- REQ-003: The state model must allow at most one active `pre_closeout_candidate`. Every new candidate must bind one deterministic predecessor equal to the `effective_latest_completed_work_block` from the immediately preceding validated repository state. Promotion must therefore validate before a separate successor-declaration revision; coding may not redefine predecessor as raw-latest when promoted effective history exists.
- REQ-004: Promotion must require the existing four evidence classes with their required verdicts, exact candidate-subject binding, valid evidence-persistence ancestry/proof, and unchanged normative manifest at the promotion subject. Missing, stale, wrong-subject, or mutated evidence/manifest state must not authorize promotion.
- REQ-005: Ordinary release-state validation must remain fail-closed for duplicate active candidates, candidate/active coexistence, malformed registry/map projection, missing evidence, stale manifests, invalid effective predecessors, duplicate promotion records, mutation/deletion/reordering of prior promoted history, candidate/promoted duplication, raw/promoted overlap, or an ambiguous/combined promotion-plus-successor transition that bypasses validation of the promotion state.
- REQ-006: Promoted history must be append-only and retain immutable candidate/evidence revision bindings and evidence references. Promotion must not change historical Work Block lifecycle status/timing, relabel historical evidence, or append a candidate-derived completion to raw `completed_work_blocks`. Effective completion is derived from raw history plus ordered promoted history, plus the current evidence-complete candidate only where the existing candidate contract permits that derivation.
- REQ-007: The invariant is prospective and transition-scoped. It must not force any of the 29 baseline raw completed records into a retroactive promotion migration, infer missing historical profile/specification authority, register or mutate WB-CORE-003G, or bring WB-CORE-003G/unrelated historical corrections into this Work Block.
- REQ-008: The proposed future implementation write-set is exactly `governance/release-state.md`, `scripts/validate-release-state.py`, `scripts/test-release-state-contracts.py`, `FILE_REGISTRY.yml`, `PROJECT_MAP.md`, and `.agent/workflows/sdd-protocol.md`. Each path must remain owner-mapped to the smallest sufficient change. This draft authorizes none of those six paths for Execute.
- REQ-009: The future contract suite must deterministically exercise successful promotion followed by a valid next-candidate declaration and adversarial cases for incomplete/wrong evidence, stale manifests, duplicate or mutated promoted history, deletion/reordering, candidate/promoted duplication, raw/promoted overlap, invalid effective predecessor, candidate/active coexistence, map disagreement, and attempted promotion/successor collapse without an intervening validated promotion state.

## Acceptance criteria

- AC-001 [req=REQ-001]: The approved design reconciles exactly 29 raw completed paths as 19 records whose structured profile/specification applicability remains `UNVERIFIED` plus 10 raw records with explicit modern `governance_profile`; it separately identifies WB-RELEASE-001 as the candidate and does not count WB-SKILL-001 or WB-CORE-003G as baseline raw completed state.
- AC-002 [req=REQ-002]: Given an evidence-complete WB-RELEASE-001 candidate, a promotion revision appends exactly one immutable promoted-history record, preserves exact candidate/evidence/manifest bindings, clears `pre_closeout_candidate`, mirrors the resulting state in `PROJECT_MAP.md`, and leaves raw `completed_work_blocks` byte-for-meaning unchanged before any successor candidate revision.
- AC-003 [req=REQ-003]: After the promotion revision validates in ordinary mode, a separately created successor candidate is accepted only when its predecessor equals WB-RELEASE-001 as the effective latest completed Work Block; a successor pointing to the older raw latest WB-SKILL-002B is rejected.
- AC-004 [req=REQ-004]: A promotion attempt without all required exact-bound evidence, without valid evidence-persistence proof, or with any changed normative-manifest path is rejected deterministically.
- AC-005 [req=REQ-005]: Ordinary validation rejects incomplete, duplicate, malformed, reordered, deleted, stale, concurrently active, invalid-predecessor, candidate/promoted-overlap, raw/promoted-overlap, map-disagreement, or unvalidated combined-transition state; candidate mode continues to emit only its distinct candidate classification and cannot emit ordinary `READY`.
- AC-006 [req=REQ-006]: The promoted record retains exact immutable candidate/evidence revision and evidence-reference data while the original Work Block and raw `completed_work_blocks` retain their historical status, timing, and membership.
- AC-007 [req=REQ-007]: No new validator rule performs a retroactive global migration or metadata inference; WB-CORE-003G and unrelated historical corrections remain explicitly excluded.
- AC-008 [req=REQ-008]: The implementation plan names the owning contract, smallest change, and rationale for exactly the six proposed future paths, and records that none is authorized until a later Owner decision after Define-quality and Critic evidence.
- AC-009 [req=REQ-009]: Deterministic fixtures cover one successful promotion and valid successor plus every adversarial class named in REQ-009, including a successor that incorrectly uses raw latest instead of promoted effective latest and a combined transition without an independently validated promotion state.

## Baseline historical impact and scope decision

The baseline registry contains exactly 29 raw completed Work Blocks and one `pre_closeout_candidate`:

- the first 19 raw entries, from WB-001 through WB-CORE-003E, have no structured modern `governance_profile`; their profile and separate-spec applicability remain `UNVERIFIED`, regardless of legacy prose or `process_level` values;
- the remaining 10 raw entries have explicit modern profiles: WB-OPENCODE-002, WB-DESIGN-001, WB-DESIGN-002, WB-REPO-GRAPH-001, WB-CORE-003F, WB-DEFINE-001, WB-GIT-001, WB-SKILL-002, WB-SKILL-002A, and WB-SKILL-002B;
- WB-SKILL-001 is not a baseline `completed_work_blocks` member and is not counted;
- WB-RELEASE-001 is the one candidate/effective-completion subject and is not raw completed;
- WB-CORE-003G is not part of the baseline completed/candidate registry state.

Historical impact is therefore **BOUNDED COLLATERAL IMPACT**: the new rule does not migrate any raw historical record. It supplies a prospective transition for WB-RELEASE-001 and later candidates only.

## Selected state representation

The draft selects an ordered append-only promoted-candidate ledger under `FILE_REGISTRY.yml:migration_state`, mirrored in `PROJECT_MAP.md`. The implementation may choose the final field spelling, but not a different semantic model without returning to Define.

Each promoted record must bind at minimum:

- Work Block path and ID;
- deterministic predecessor effective Work Block;
- exact candidate revision;
- exact evidence-persistence revision;
- the four declared evidence paths and their exact candidate binding;
- the ordered normative manifest that was proved unchanged;
- an unambiguous promoted/effective-completion state token.

The ledger is canonical machine history separate from raw `completed_work_blocks`. Ordinary effective history is derived in order from raw completed history plus validated promotion records. A currently declared candidate may be additionally derived as effective only under the existing evidence-complete candidate contract; that temporary derivation must be converted to a durable ledger record before the candidate slot is reused.

Promotion and successor declaration are separate repository revisions. The promotion revision must validate first. The later candidate declaration must use the previously validated `effective_latest_completed_work_block` as predecessor.

Directly appending candidate-derived completion to raw `completed_work_blocks`, using a separate unapproved canonical store, or combining promotion and successor declaration so that the intermediate promoted state is never validated is outside this specification.

## Future implementation write-set — proposed, exact, unauthorized

- `governance/release-state.md` — define the ordered promotion ledger, effective-history derivation, promotion prerequisites, append-only semantics, and effective-predecessor rule.
- `scripts/validate-release-state.py` — enforce exact promotion evidence/manifest binding, ledger uniqueness/order/immutability, effective-history derivation, and successor predecessor continuity.
- `scripts/test-release-state-contracts.py` — prove positive and adversarial promotion/next-candidate behavior.
- `FILE_REGISTRY.yml` — host the canonical ordered promoted-candidate history used by the actual future transition.
- `PROJECT_MAP.md` — mirror the same migration state and candidate/promotion projection.
- `.agent/workflows/sdd-protocol.md` — prescribe promotion → ordinary validation → separate successor declaration operational sequencing.

No source implementation, governance edit, registry/map edit, protocol edit, or fixture change is authorized while this specification remains `draft`.

## Verification boundary

Corrected Define revision `define-r2-2026-08-25` requires fresh independent requirements-quality review, structural traceability, read-only consistency analysis, and Critic before any future Execute decision. Expected structural traceability remains:

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

