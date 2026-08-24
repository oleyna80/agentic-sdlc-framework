---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-RELEASE-001
specification: docs/specs/wb-release-001-closeout-sequencing-reconciliation.md
specification_revision: define-r3-2026-08-24
status: in_progress
---

# WB-RELEASE-001 Tasklist — Release-State Closeout Sequencing Reconciliation

## Define and Decision Tasks

- [x] TASK-001 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-001-closeout-sequencing-reconciliation.md,docs/specs/wb-release-001-closeout-sequencing-reconciliation.md,docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md] Create bounded Managed Define artifacts from clean `bc05d3c554225d77aa23a4d63c5a8dd41c37ea34` without touching the WB-CORE-003G pilot worktree.
- [x] TASK-002 [type=enabling] [req=-] [ac=-] [paths=governance/release-state.md,.agent/workflows/sdd-protocol.md,FILE_REGISTRY.yml,scripts/validate-release-state.py,scripts/test-release-state-contracts.py] Investigate the current default-validator/accepted-sequence contradiction and historic WB-SKILL-002A/B terminal-projection ordering; record the smallest prospective design.
- [ ] TASK-003 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-001-closeout-sequencing-reconciliation.md] Obtain independent requirements-quality review of the draft specification before any source write decision.
- [ ] TASK-004 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-001-closeout-sequencing-reconciliation-consistency.md] Obtain independent consistency analysis for authority, lifecycle, candidate semantics, and REQ → AC → TASK traceability.
- [ ] TASK-005 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-001-closeout-sequencing-reconciliation-critic.md] Obtain a Critic assessment of candidate-state risks, default fail-closed behavior, test design, and write-set minimality.

## Potential Execute Tasks — Blocked Pending Approval

- [ ] TASK-006 [type=requirement] [req=REQ-001] [ac=AC-001,AC-002] [paths=scripts/validate-release-state.py] Add explicit candidate-mode parsing without changing ordinary-mode fail-closed requirements.
- [ ] TASK-007 [type=requirement] [req=REQ-002,REQ-003,REQ-005] [ac=AC-003,AC-004,AC-006] [paths=governance/release-state.md,scripts/validate-release-state.py,FILE_REGISTRY.yml] Add and validate one persistent `closeout_candidate` declaration, its `assurance_pending` projection, predecessor binding, two-part canonical completion rule, distinct `CANDIDATE_READY` result, and non-promotion boundary.
- [ ] TASK-008 [type=requirement] [req=REQ-004] [ac=AC-005] [paths=scripts/validate-release-state.py] Add deterministic exact candidate-to-evidence revision comparison and manifest verification with no hidden normative delta.
- [ ] TASK-009 [type=requirement] [req=REQ-006] [ac=AC-007] [paths=governance/release-state.md,.agent/workflows/sdd-protocol.md,FILE_REGISTRY.yml] Synchronize the normative contract, operational procedure, and machine-readable acceptance sequence.
- [ ] TASK-010 [type=requirement] [req=REQ-007] [ac=AC-008] [paths=scripts/test-release-state-contracts.py] Add positive and adversarial fixtures for ordinary and candidate modes, including candidate declaration lifecycle and exact cross-revision proof.
- [ ] TASK-011 [type=requirement] [req=REQ-008] [ac=AC-009] [paths=governance/release-state.md,.agent/workflows/sdd-protocol.md,FILE_REGISTRY.yml,scripts/validate-release-state.py,scripts/test-release-state-contracts.py] Preserve bounded scope and prove the frozen source manifest excludes historical Work Blocks and unrelated implementation.

## Assure and Close

- [ ] TASK-012 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-001-closeout-sequencing-reconciliation.md,docs/reports/verification/wb-release-001-closeout-sequencing-reconciliation.md,docs/reports/drift/wb-release-001-closeout-sequencing-reconciliation.md] Freeze the approved source subject and obtain independent Reviewer, fresh-clone Verifier, and Drift evidence.
- [ ] TASK-013 [type=requirement] [req=REQ-009] [ac=AC-010] [paths=docs/reports/closeout/wb-release-001-closeout-sequencing-reconciliation.md,docs/plans/wb-release-001-closeout-sequencing-reconciliation.md,docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md,FILE_REGISTRY.yml,PROJECT_MAP.md] Close only after the accepted contract is implemented and the final repository state has ordinary release-state validation; record WB-CORE-003G as a follow-up/resumption dependency rather than changing it here.

## Dependencies and Stop Conditions

The Define assurance tasks are required before any Write Gate decision. The
potential Execute tasks require an Owner-approved specification revision and
exact source write-set; they are not authorized by this draft. The terminal
assurance task requires a frozen implementation diff. The Close task requires
READY/ALIGNED final assurance.

Stop for Owner direction if candidate mode would weaken default validation,
weaken default validation, treat a candidate as externally promotable, require
changes to historical completed Work Blocks, require a new dependency, or
require an unplanned template-wide change.
