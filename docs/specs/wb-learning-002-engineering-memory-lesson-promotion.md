---
schema_version: 1
artifact_type: specification
artifact_id: wb-learning-002-engineering-memory-lesson-promotion
status: draft
owner_role: owner
work_block_id: WB-LEARNING-002
revision: define-1
created_at: 2026-09-08
last_verified: 2026-09-08
governance_profile: Managed
---

# WB-LEARNING-002 — Selective Promotion of Durable Engineering Memory Lessons

## Objective

Prepare two generic, evidence-backed engineering-memory lessons for a later
Owner-authorized promotion into the current framework's canonical engineering
memory. This Define artifact does not promote either lesson and does not change
the existing lessons, runtime, validators, lifecycle semantics, or release-state
semantics.

## Source and baseline

- Source branch: `agent/engineering-memory-lessons-2026-08-31`.
- Source tip: `8fb9e2e5df6a74098862240dccd9d72782be37c7`.
- Implementation baseline: current `main` at Define materialization,
  `168d61d470e434ac0f5e5c56e244c2516e7d3148`.
- The source branch is provenance/evidence input only. Its wording is not a
  canonical target and its implementation/status metadata must not be copied.

## Proposed lesson identities

- Proposed `LL-003`: an ephemeral execution workspace cannot be the sole source
  of closeout evidence; durable evidence must be persisted in the repository's
  canonical evidence surfaces before the workspace disappears.
- Proposed `LL-004`: a newly recognized historical invariant requires a
  structural adoption/enforcement boundary in the owning contract or validator;
  documenting the rule alone is insufficient when future drift is possible.

`LL-003` and `LL-004` are proposals only. Execute must re-check the current
baseline for collisions and semantic overlap. Existing `LL-001` and `LL-002`
must not be changed or reused.

## Requirements

- REQ-001: Define exactly two selective-promotion lesson candidates, limited to the ephemeral-evidence principle and the structural-enforcement-boundary principle.
- REQ-002: Derive both target lessons from the source branch as evidence and provenance, while using current `main` as the only implementation and semantic baseline.
- REQ-003: Express the ephemeral-evidence candidate as a generic reusable principle, separate from the specific incident, branch, temporary path, date, SHA, or Work Block.
- REQ-004: Express the structural-enforcement candidate as a generic rule for adopting historical invariants at an enforceable contract boundary, without incident-specific identifiers or framework semantic changes.
- REQ-005: Preserve collision-free identity by treating `LL-003` and `LL-004` as proposed IDs and rechecking them against the Execute baseline; never overwrite or repurpose `LL-001` or `LL-002`.
- REQ-006: Preserve truthful provenance and semantic mapping from each source lesson to its future canonical candidate without copying stale status or metadata.
- REQ-007: Keep the promotion knowledge/governance-only: no runtime, validator, lifecycle, release-state, existing-lesson, or framework-policy mutation is authorized by this Define.
- REQ-008: Define deletion readiness for the source branch as a future assessment, not a guaranteed outcome, after promotion or explicit rejection has been established.

## Acceptance Criteria

- AC-001 [req=REQ-001]: The plan and tasklist identify exactly two bounded candidates and name no additional lesson payload.
- AC-002 [req=REQ-002]: The artifacts record the exact source branch/tip, current-main baseline, and the source-as-provenance-only boundary.
- AC-003 [req=REQ-003]: The proposed LL-003 content states the durable-evidence principle without requiring the original incident, `/tmp` path, SHA, date, or WB identifier to understand or reuse it.
- AC-004 [req=REQ-004]: The proposed LL-004 content states structural adoption/enforcement of historical invariants as a reusable governance principle and explicitly excludes implementation changes in this WB.
- AC-005 [req=REQ-005]: The artifacts label LL-003 and LL-004 as proposed, require an Execute-time collision check, and explicitly protect LL-001 and LL-002 from modification or reuse.
- AC-006 [req=REQ-006]: Each candidate has a source-to-target semantic mapping, evidence/provenance requirements, and a rule against importing stale source metadata.
- AC-007 [req=REQ-007]: Scope and out-of-scope sections exclude `docs/engineering-memory/lessons-learned.md`, runtime, validators, lifecycle/release-state semantics, and lesson promotion during Define.
- AC-008 [req=REQ-008]: Deletion-readiness is conditioned on semantic coverage, no valuable unpromoted content, no live worktree dependency, and no current PR/lifecycle dependency; otherwise the branch remains retained or is separately Owner-classified.

## Scope

In scope:

1. Define framing for the two proposed lessons.
2. Generic/reusable wording criteria and semantic source-to-target mapping.
3. Collision, provenance, evidence, and future deletion-readiness rules.
4. Existing canonical lifecycle/release-state flow only insofar as the future
   Work Block must use it.

Out of scope:

- Editing `docs/engineering-memory/lessons-learned.md` or any existing lesson.
- Promoting, rejecting, or deleting either lesson.
- Changing runtime behavior, validators, lifecycle semantics, or release-state
  semantics.
- Creating framework policy from either lesson in this WB.
- Deleting `agent/engineering-memory-lessons-2026-08-31`.
- Execute, assurance closeout, canonical promotion, PR, merge, or branch deletion.

## Authority and lifecycle boundary

This is a Define-only artifact with `status: draft`; it is not an active
implementation Work Block and does not open a write gate. If the framework
requires lifecycle registration for the future Execute, that registration must
use the existing canonical lifecycle/release-state flow and a separately
approved Execute gate. This Define does not alter that flow.

## Evidence and provenance strategy

Execute must retain the exact source branch and tip above, record the current
baseline used for collision/deduplication review, and cite the source lesson
sections plus repository evidence that demonstrates future utility. The
canonical lesson must contain the reusable principle, replacement/mitigation,
authority boundary, review trigger, and last-verified metadata; it must not
claim that source-branch wording was adopted literally. Any unavailable or
unconfirmed evidence is recorded as such rather than inferred.

## Deletion-readiness assessment

After a future promotion or explicit rejection, assess the source branch
separately. A `SAFE TO DELETE REMOTE — CONTENT PROMOTED / SUPERSEDED` verdict is
allowed only when both semantic mappings have full coverage, no valuable
unpromoted content remains, no live worktree depends on the branch, and no
current PR or lifecycle/provenance dependency requires the remote ref. Until
all applicable conditions are evidenced and Owner-controlled cleanup is
authorized, retain the branch.

## Future Owner gate

Define materialization is ready for a separate `OWNER_LEARNING_002_EXECUTE_GATE`
only after independent Define review confirms that the three artifacts agree,
the collision/provenance rules are testable, and no scope expansion is needed.
That gate, not this document, decides whether and how promotion proceeds.
