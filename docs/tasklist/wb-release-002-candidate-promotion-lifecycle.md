---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-RELEASE-002
specification: docs/specs/wb-release-002-candidate-promotion-lifecycle.md
specification_revision: define-r2-2026-08-25
status: in_progress
---

# WB-RELEASE-002 Tasklist — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Define and investigation

- [ ] TASK-001 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-002-candidate-promotion-lifecycle.md,docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Maintain the bounded Managed Define artifacts and record that the current correction authorizes only these three Define paths, not future source/canonical implementation.
- [ ] TASK-002 [type=enabling] [req=-] [ac=-] [paths=FILE_REGISTRY.yml,PROJECT_MAP.md,docs/plans/**,docs/specs/**,docs/tasklist/**] Reconcile all 29 baseline raw completed Work Blocks, the single WB-RELEASE-001 candidate, explicit modern governance profiles, and separate-specification facts without modifying canonical state or inferring legacy metadata.
- [ ] TASK-003 [type=enabling] [req=-] [ac=-] [paths=docs/plans/wb-release-001-closeout-sequencing-reconciliation.md,docs/specs/wb-release-001-closeout-sequencing-reconciliation.md,docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md,governance/release-state.md,scripts/validate-release-state.py] Trace the current raw/effective candidate contract and establish that candidate-derived effective completion needs durable promotion before the candidate slot can be reused.
- [ ] TASK-004 [type=requirement] [req=REQ-001,REQ-002] [ac=AC-001,AC-002] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Define the exact 29-record historical truth boundary and a separate promotion revision that preserves WB-RELEASE-001 effective completion in append-only promoted history before successor declaration.
- [ ] TASK-005 [type=requirement] [req=REQ-003,REQ-004,REQ-005] [ac=AC-003,AC-004,AC-005] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Define exactly-one-candidate, effective-latest predecessor, evidence/persistence/manifest, append-only ledger, separate-revision, and fail-closed validation semantics.
- [ ] TASK-006 [type=requirement] [req=REQ-006,REQ-007] [ac=AC-006,AC-007] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Preserve immutable promoted evidence and raw historical truth prospectively without legacy migration, WB-CORE-003G mutation, or historical evidence relabeling.
- [ ] TASK-007 [type=requirement] [req=REQ-008] [ac=AC-008] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Map the exact six proposed future implementation paths to their owning contracts and smallest sufficient changes while leaving every future path unauthorized.
- [ ] TASK-008 [type=requirement] [req=REQ-009] [ac=AC-009] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Define deterministic positive and adversarial fixture scenarios for promotion-ledger integrity, effective predecessor continuity, and separate successor declaration.

## Define quality and later assurance

- [ ] TASK-009 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-002-candidate-promotion-lifecycle.md] Obtain a fresh independent requirements-quality review of corrected revision `define-r2-2026-08-25`.
- [ ] TASK-010 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-002-candidate-promotion-lifecycle-consistency.md] Obtain fresh read-only consistency analysis across corrected specification, plan, tasklist, governing contracts, and exact proposed future write-set.
- [ ] TASK-011 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-002-candidate-promotion-lifecycle-critic.md] Obtain fresh Critic review after corrected Define-quality evidence and before any future Write Gate decision.
- [ ] TASK-012 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-002-candidate-promotion-lifecycle.md,docs/reports/verification/wb-release-002-candidate-promotion-lifecycle.md,docs/reports/drift/wb-release-002-candidate-promotion-lifecycle.md] Reserve independent Reviewer, fresh-clone Verifier, and Drift evidence for a later frozen implementation subject; these are not produced in Define.
- [ ] TASK-013 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-002-candidate-promotion-lifecycle.md,docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Record the selected draft promotion-ledger design, later Owner approval state, and final future write-set without changing source or canonical release state.

## Traceability and execution boundary

- [ ] TASK-014 [type=assurance] [req=-] [ac=-] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Run structural Define traceability for revision `define-r2-2026-08-25` and retain the result as Define evidence; expected result is `READY requirements=9 acceptance=9 tasks=15`, but structural PASS alone does not make aggregate Define quality READY.
- [ ] TASK-015 [type=enabling] [req=-] [ac=-] [paths=governance/release-state.md,scripts/validate-release-state.py,scripts/test-release-state-contracts.py,FILE_REGISTRY.yml,PROJECT_MAP.md,.agent/workflows/sdd-protocol.md] Prepare the exact six-path future implementation proposal only after requirements review, traceability, consistency analysis, and Critic; no listed source/canonical path is authorized by this task.

## Stops

No task authorizes source implementation, existing Work Block/evidence edits, registry/map/protocol/governance changes, pull request creation/update, merge, rebase, or GitHub-thread resolution. Directly promoting candidate-derived completion into raw `completed_work_blocks`, selecting another canonical promotion store, or collapsing promotion and successor declaration into one unvalidated transition is a material specification change and returns to Define/Owner approval.

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

