---
schema_version: 1
artifact_type: work_block
artifact_id: wb-learning-002-engineering-memory-lesson-promotion
work_block_id: WB-LEARNING-002
status: draft
owner_role: orchestrator
created_at: 2026-09-08
base_revision: 168d61d470e434ac0f5e5c56e244c2516e7d3148
branch: docs/wb-learning-002-define-022
governance_profile: Managed
verification_tier: Standard
source_branch: agent/engineering-memory-lessons-2026-08-31
source_revision: 8fb9e2e5df6a74098862240dccd9d72782be37c7
specification: docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md
---

# WB-LEARNING-002 — Selective Promotion of Durable Engineering Memory Lessons

## Define decision

Materialize a bounded future promotion WB for exactly two rewritten,
evidence-backed engineering-memory candidates. The source branch is retained as
provenance input. The implementation baseline is current `main`; no source
branch implementation is a baseline for future work.

## Work plan

1. During future Execute, re-read current `main` engineering memory and confirm
   that proposed `LL-003` and `LL-004` remain collision-free and non-redundant.
2. Rewrite the ephemeral-workspace lesson into a generic durable-evidence rule,
   retaining incident evidence only as provenance.
3. Rewrite/prepare the structural-enforcement lesson as a generic adoption and
   enforcement-boundary principle, with no SHA/date/WB-specific workaround.
4. Perform independent semantic mapping and evidence review before any
   promotion decision.
5. If promotion is approved, use the existing canonical lifecycle and release-
   state flow; do not introduce new lifecycle or release-state semantics.
6. After promotion or explicit rejection, perform a separate source-branch
   deletion-readiness assessment against the four conditions in the
   specification.

## Boundaries

The future Execute write-set, if approved, must be limited to the canonical
engineering-memory target and the lifecycle/evidence paths required by the
existing contract. This Define does not authorize that write-set. It does not
authorize changes to validators, runtime, lifecycle/release-state semantics,
existing lessons, source branch, PRs, merges, or destructive cleanup.

## Dependencies and predecessor

- Predecessor evidence: the read-only content review of
  `agent/engineering-memory-lessons-2026-08-31@8fb9e2e5df6a74098862240dccd9d72782be37c7`.
- Baseline dependency: current `main@168d61d470e434ac0f5e5c56e244c2516e7d3148`.
- The existing engineering-memory contract and WB-LEARNING-001 learning-loop
  behavior remain governing context; neither is changed here.
- Future Execute may require canonical lifecycle registration, but this draft
  does not register an active Work Block.

## Risks and controls

| Risk | Control |
| --- | --- |
| Incident-specific wording is promoted as a universal lesson | Require generic wording and keep incident details in provenance/evidence only. |
| Proposed ID collides with a newer lesson | Recheck IDs on Execute baseline; existing `LL-001`/`LL-002` are immutable for this scope. |
| Documentation is mistaken for enforcement | State that structural enforcement is a future principle; do not mutate validators or lifecycle semantics here. |
| Source branch is deleted prematurely | Deletion is a later assessment gated by semantic coverage and dependency checks. |
| Define silently expands into framework policy | Any policy or contract change returns to a new Define/Owner decision. |

## Define readiness

The expected terminal result of this materialization is `DEFINE_READY`, subject
to structural traceability, SSOT/lifecycle consistency, and independent review.
It is not Execute authorization, lesson promotion, closeout, or deletion
authority.
