---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-RELEASE-002
specification: docs/specs/wb-release-002-candidate-promotion-lifecycle.md
specification_revision: define-r1-2026-08-25
status: in_progress
---

# WB-RELEASE-002 Tasklist — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Define and investigation

- [ ] TASK-001 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-002-candidate-promotion-lifecycle.md,docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Create the bounded Managed Define artifacts and record that source implementation is not authorized.
- [ ] TASK-002 [type=enabling] [req=-] [ac=-] [paths=FILE_REGISTRY.yml,PROJECT_MAP.md,docs/plans/**,docs/specs/**,docs/tasklist/**] Inventory raw completed Work Blocks, the single active candidate, explicit governance profiles, separate specifications, and their statuses without modifying canonical state.
- [ ] TASK-003 [type=enabling] [req=-] [ac=-] [paths=docs/plans/wb-release-001-closeout-sequencing-reconciliation.md,docs/specs/wb-release-001-closeout-sequencing-reconciliation.md,docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md,governance/release-state.md,scripts/validate-release-state.py] Trace the current candidate/effective-completion contract and identify the missing promotion-to-next-candidate transition.
- [ ] TASK-004 [type=requirement] [req=REQ-001,REQ-002] [ac=AC-001,AC-002] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Define historical truth boundaries and a promotion transition that preserves WB-RELEASE-001 effective completion before successor declaration.
- [ ] TASK-005 [type=requirement] [req=REQ-003,REQ-004,REQ-005] [ac=AC-003,AC-004,AC-005] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Define exactly-one-candidate, predecessor, evidence, manifest, and fail-closed validation semantics.
- [ ] TASK-006 [type=requirement] [req=REQ-006,REQ-007] [ac=AC-006,AC-007] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Bound the design prospectively and preserve immutable prior evidence without retroactive historical rewrites or WB-CORE-003G mutation.
- [ ] TASK-007 [type=requirement] [req=REQ-008] [ac=AC-008] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Map every possible future source path to its owning contract and smallest sufficient change while leaving the write-set unauthorized.
- [ ] TASK-008 [type=requirement] [req=REQ-009] [ac=AC-009] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/plans/wb-release-002-candidate-promotion-lifecycle.md] Define deterministic positive and adversarial fixture scenarios for promotion and next-candidate sequencing.

## Define quality and later assurance

- [ ] TASK-009 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-002-candidate-promotion-lifecycle.md] Obtain an independent requirements-quality review after the Define artifacts are frozen.
- [ ] TASK-010 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-release-002-candidate-promotion-lifecycle-consistency.md] Obtain read-only consistency analysis across specification, plan, tasklist, governance, and proposed write-set.
- [ ] TASK-011 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-002-candidate-promotion-lifecycle-critic.md] Obtain Critic review before any future Write Gate decision.
- [ ] TASK-012 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-release-002-candidate-promotion-lifecycle.md,docs/reports/verification/wb-release-002-candidate-promotion-lifecycle.md,docs/reports/drift/wb-release-002-candidate-promotion-lifecycle.md] Reserve independent Reviewer, fresh-clone Verifier, and Drift evidence for a later frozen implementation subject; these are not produced in Define.
- [ ] TASK-013 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-release-002-candidate-promotion-lifecycle.md,docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Record Owner decisions, unresolved alternatives, and the final proposed future write-set without changing source or canonical release state.

## Traceability and execution boundary

- [ ] TASK-014 [type=assurance] [req=-] [ac=-] [paths=docs/specs/wb-release-002-candidate-promotion-lifecycle.md,docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md] Run structural Define traceability and retain the result as Define evidence; a structural PASS does not make the aggregate Define-quality state READY.
- [ ] TASK-015 [type=enabling] [req=-] [ac=-] [paths=governance/release-state.md,scripts/validate-release-state.py,scripts/test-release-state-contracts.py,FILE_REGISTRY.yml,PROJECT_MAP.md,.agent/workflows/sdd-protocol.md] Prepare a future implementation proposal only after requirements review, consistency analysis, and Critic; no listed source path is authorized by this task.

## Stops

No task authorizes source implementation, existing Work Block edits, registry/map changes, governance changes, commit, push, pull request, merge, rebase, or GitHub-thread resolution. A material choice between promotion-ledger representations returns to Owner/Define before Execute.

## Pre-execution validation

```bash
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-release-002-candidate-promotion-lifecycle.md \
  --tasks docs/tasklist/wb-release-002-candidate-promotion-lifecycle.md
```

