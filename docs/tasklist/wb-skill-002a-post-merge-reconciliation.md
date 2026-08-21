---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-SKILL-002A
specification: docs/specs/wb-skill-002a-post-merge-reconciliation.md
specification_revision: define-r1-2026-08-21
status: draft
---

# WB-SKILL-002A Tasklist — Post-Merge Specification and Regression-Guard Reconciliation

## Requirement Delivery

- [ ] TASK-001 [type=requirement] [req=REQ-001,REQ-002] [ac=AC-001,AC-002,AC-003] [paths=docs/specs/wb-skill-002-provider-neutral-verifier.md,docs/plans/wb-skill-002a-post-merge-reconciliation.md] Record the selected evidence-supported P1 remediation without fabricating or backdating historical Owner approval.
- [ ] TASK-002 [type=requirement] [req=REQ-003,REQ-004] [ac=AC-004,AC-005,AC-006] [paths=scripts/test-sdd-contract.sh] Make the existing target-only mandatory-provider predicate paragraph-aware and add adversarial cases that run through that predicate.
- [ ] TASK-003 [type=requirement] [req=REQ-005] [ac=AC-007,AC-008] [paths=governance/release-state.md,scripts/validate-release-state.py,scripts/test-release-state-contracts.py] Add the smallest approved latest-completed formal-specification authority invariant and its contract fixtures.
- [ ] TASK-004 [type=requirement] [req=REQ-006,REQ-007] [ac=AC-009] [paths=docs/plans/wb-skill-002a-post-merge-reconciliation.md,docs/tasklist/wb-skill-002a-post-merge-reconciliation.md] Maintain the bounded implementation manifest and demonstrate that the accepted provider-neutral skill remains outside it.

## Enabling, Documentation, and Assurance

- [ ] TASK-005 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-skill-002a-post-merge-reconciliation.md,docs/specs/wb-skill-002a-post-merge-reconciliation.md,docs/tasklist/wb-skill-002a-post-merge-reconciliation.md] Maintain truthful Define artifacts, the historical evidence classification, impact inventory, and the proposed-only implementation boundary.
- [ ] TASK-006 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-skill-002a-post-merge-reconciliation.md,docs/reports/requirements/wb-skill-002a-post-merge-reconciliation-consistency.md,docs/reports/reviews/wb-skill-002a-post-merge-reconciliation-critic.md] Obtain independent requirements-quality review, consistency analysis, and Critic review before any source Write Gate decision.
- [ ] TASK-007 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-002a-post-merge-reconciliation.md,docs/reports/verification/wb-skill-002a-post-merge-reconciliation.md,docs/reports/drift/wb-skill-002a-post-merge-reconciliation.md] Freeze the approved implementation subject and obtain independent Reviewer, Verifier, and Drift evidence before terminal closeout.
- [ ] TASK-008 [type=documentation] [req=-] [ac=-] [paths=docs/reports/closeout/wb-skill-002a-post-merge-reconciliation.md,FILE_REGISTRY.yml,PROJECT_MAP.md] Perform terminal projection and closeout only after final assurance; preserve historical reports and state mutable hosting facts as non-normative.

## Dependencies and Stops

The four requirement tasks require Define readiness and a Critic-approved
future Write Gate. The guard and release-state tasks may be implemented by one
Coder only after that gate opens; their shared assurance boundary prevents
parallel writers. Final independent assurance depends on a frozen post-Execute
subject, and terminal projection depends on assurance of its own normative
state.

No task authorizes source execution in this Define run, a change to
`skills/codex-verification/SKILL.md`, GitHub review-thread resolution, push,
PR creation, merge, rebase, deployment, or any out-of-scope artifact.

## Pre-Execution Validation

```bash
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-skill-002a-post-merge-reconciliation.md \
  --tasks docs/tasklist/wb-skill-002a-post-merge-reconciliation.md
```

## Retrospective and Closeout

Closeout must preserve the distinction between the historical evidence record,
the Owner's later decision if any, and current authority. It must also record
whether the paragraph-aware guard fixtures proved both prohibited wrapped prose
and paragraph separation without widening the target-only search.
