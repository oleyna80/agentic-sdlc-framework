---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-LEARNING-002
specification: docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md
specification_revision: define-1
status: draft
---

# WB-LEARNING-002 — Define Tasklist

## Define tasks

- [ ] TASK-001 [type=requirement] [req=REQ-001,REQ-002] [ac=AC-001,AC-002] [paths=docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md,docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/tasklist/wb-learning-002-engineering-memory-lesson-promotion.md] Materialize the bounded two-lesson Define from the exact source and current-main baseline.
- [ ] TASK-002 [type=requirement] [req=REQ-003] [ac=AC-003] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md] Define generic durable-evidence wording and keep the originating incident as provenance only.
- [ ] TASK-003 [type=requirement] [req=REQ-004] [ac=AC-004] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md] Define the generic structural adoption/enforcement-boundary principle without changing enforcement implementation.
- [ ] TASK-004 [type=requirement] [req=REQ-005] [ac=AC-005] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/tasklist/wb-learning-002-engineering-memory-lesson-promotion.md] Record proposed IDs, Execute-time collision checks, and protection of existing LL-001/LL-002.
- [ ] TASK-005 [type=requirement] [req=REQ-006] [ac=AC-006] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md] Define source-to-target semantic mapping and evidence/provenance requirements without stale metadata.
- [ ] TASK-006 [type=requirement] [req=REQ-007] [ac=AC-007] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md] Freeze the knowledge/governance-only scope and all implementation exclusions.
- [ ] TASK-007 [type=requirement] [req=REQ-008] [ac=AC-008] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md] Define conditional deletion-readiness assessment for the source branch.
- [ ] TASK-008 [type=assurance] [req=-] [ac=-] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md,docs/tasklist/wb-learning-002-engineering-memory-lesson-promotion.md] Run Define structure, cross-artifact consistency, and lifecycle/SSOT validation.
- [ ] TASK-009 [type=documentation] [req=-] [ac=-] [paths=docs/specs/wb-learning-002-engineering-memory-lesson-promotion.md,docs/plans/wb-learning-002-engineering-memory-lesson-promotion.md,docs/tasklist/wb-learning-002-engineering-memory-lesson-promotion.md] Record Define readiness and handoff to the separate Owner Execute gate without opening Execute.

## Stop conditions

- A collision or material redundancy is found on the Execute baseline.
- A proposed rewrite requires changing existing lessons or framework semantics.
- Evidence cannot establish generic reusable value.
- Owner scope or lifecycle authority is required beyond this Define.

## Define handoff

After the Define checks pass, stop at `OWNER_LEARNING_002_EXECUTE_GATE`. Do not
edit `docs/engineering-memory/lessons-learned.md`, promote lessons, close or
promote this Work Block, open a PR, merge, or delete the source branch.
