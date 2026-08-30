---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-RELEASE-002
specification: docs/specs/wb-release-002-candidate-promotion-lifecycle.md
specification_revision: owner-approved-define-r4-2026-08-30
status: in_progress
---

# WB-RELEASE-002 Tasklist — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Define and investigation

- [x] TASK-001 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-002-candidate-promotion-lifecycle.md,docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Maintain the bounded Managed Define artifacts and record that the current correction authorizes only these three Define paths, not future source/canonical implementation.
- [x] TASK-002 [type=enabling] [req=-] [ac=-] [paths=FILE_REGISTRY.yml,PROJECT_MAP.md,docs/plans/**,docs/specs/**,docs/tasklist/**] Reconcile all 29 baseline raw completed Work Blocks, the single WB-RELEASE-001 candidate, explicit modern governance profiles, and separate-specification facts without modifying canonical state or inferring legacy metadata.
- [x] TASK-003 [type=enabling] [req=-] [ac=-] [paths=docs/plans/wb-release-001-closeout-sequencing-reconciliation.md,docs/specs/wb-release-001-closeout-sequencing-reconciliation.md,docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md,governance/release-state.md,scripts/validate-release-state.py] Trace the current raw/effective candidate contract and establish that candidate-derived effective completion needs durable promotion before the candidate slot can be reused.
- [ ] TASK-004 [type=requirement] [req=REQ-001,REQ-002] [ac=AC-001,AC-002] [paths=governance/release-state.md,scripts/validate-release-state.py] Phase A one-Coder implementation: encode the prospective historical boundary and one-parent exact two-path promotion contract.
- [ ] TASK-005 [type=requirement] [req=REQ-003,REQ-004,REQ-005] [ac=AC-003,AC-004,AC-005] [paths=governance/release-state.md,scripts/validate-release-state.py] Phase A one-Coder implementation: enforce the canonical effective-predecessor field, promotion-parent discovery, ledger schema, and fail-closed validation.
- [ ] TASK-006 [type=requirement] [req=REQ-006,REQ-007] [ac=AC-006,AC-007] [paths=governance/release-state.md,scripts/validate-release-state.py] Phase A one-Coder implementation: preserve immutable promoted evidence, freeze raw history after first promotion, and exclude legacy migration/WB-CORE-003G.
- [ ] TASK-007 [type=requirement] [req=REQ-008] [ac=AC-008] [paths=governance/release-state.md,scripts/validate-release-state.py,scripts/test-release-state-contracts.py,.agent/workflows/sdd-protocol.md] Phase A one-Coder implementation: deliver the exact four-path implementation write-set; the two-path registry/map promotion transition remains separately Owner-gated.
- [ ] TASK-008 [type=requirement] [req=REQ-009] [ac=AC-009] [paths=scripts/test-release-state-contracts.py] Phase A one-Coder implementation: add deterministic positive and adversarial promotion-parent, ledger, predecessor, and separate-successor fixtures.

## Define quality and later assurance

- [x] TASK-009 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-002-candidate-promotion-lifecycle.md] Obtain fresh independent Requirements Review `READY` of corrected revision `define-r3-2026-08-30`; the read-only verdict is recorded in the permitted plan rather than a new report artifact.
- [x] TASK-010 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-002-candidate-promotion-lifecycle-consistency.md] Obtain fresh read-only Consistency Analysis `READY`; the verdict is recorded in the permitted plan rather than a new report artifact.
- [x] TASK-011 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-002-candidate-promotion-lifecycle-critic.md] Obtain fresh Critic `APPROVE`; the verdict is recorded in the permitted plan rather than a new report artifact.
- [ ] TASK-012 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-002-candidate-promotion-lifecycle.md,docs/reports/verification/wb-release-002-candidate-promotion-lifecycle.md,docs/reports/drift/wb-release-002-candidate-promotion-lifecycle.md] Reserve independent Reviewer, fresh-clone Verifier, and Drift evidence for a later frozen implementation subject; these are not produced in Define.
- [x] TASK-013 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-002-candidate-promotion-lifecycle.md,docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Record exact canonical `migration_state.promoted_candidates`, four-path implementation/two-path transition boundary, later Owner approval state, and final future write-set without changing source or canonical release state.

## Traceability and execution boundary

- [x] TASK-014 [type=assurance] [req=-] [ac=-] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Run structural Define traceability for revision `define-r3-2026-08-30` and retain the result as Define evidence: `READY requirements=9 acceptance=9 tasks=15`; structural PASS alone does not make aggregate Define quality READY.
- [ ] TASK-015 [type=enabling] [req=-] [ac=-] [paths=FILE_REGISTRY.yml,PROJECT_MAP.md] Reserve the exact two-path operational promotion transition for a later dedicated Owner gate after the four-path implementation validates and its ordinary-valid promotion parent exists; no listed canonical path is authorized by this task.

## Stops

Only Phase A source implementation in the exact four-path write-set is authorized. No task authorizes existing Work Block/evidence edits, registry/map canonical changes, actual promotion, successor declaration, pull request creation/update, push, merge, rebase, deployment, cleanup, or GitHub-thread resolution. Directly promoting candidate-derived completion into raw `completed_work_blocks`, resuming raw-history appends after promotion begins, selecting another canonical promotion store, changing predecessor serialization, changing any path outside registry/map in the later promotion transition, or collapsing promotion and successor declaration into one unvalidated transition is a material specification change and returns to Define/Owner approval.

## Pre-execution validation

```bash
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-release-002-candidate-promotion-lifecycle.md \
  --tasks docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md
```

Expected structural result:

```text
READY
requirements=9 acceptance=9 tasks=15
```
