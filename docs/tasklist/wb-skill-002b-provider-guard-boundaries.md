---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-SKILL-002B
specification: docs/specs/wb-skill-002b-provider-guard-boundaries.md
specification_revision: define-r1-2026-08-23
status: in_progress
---

# WB-SKILL-002B Tasklist — Provider Guard Imperative and Fence Boundary Correction

## Requirement Delivery

- [ ] TASK-001 [type=requirement] [req=REQ-001] [ac=AC-001,AC-002] [paths=scripts/test-sdd-contract.sh] Make the existing target-only predicate reject the bounded direct imperative provider-assurance patterns, including polite and ordinary wrapped forms, without widening its file scope or introducing general NLP.
- [ ] TASK-002 [type=requirement] [req=REQ-002] [ac=AC-003,AC-004] [paths=scripts/test-sdd-contract.sh] Replace fence-toggle behavior with opener-character/run-length tracking and compatible closer validation while retaining exclusion through invalid or unclosed fences.
- [ ] TASK-003 [type=requirement] [req=REQ-003] [ac=AC-005,AC-006] [paths=scripts/test-sdd-contract.sh] Add adversarial fixtures that invoke the production predicate for imperative, wrapping, advisory, valid-closer, invalid-closer, and statement-boundary cases.
- [ ] TASK-004 [type=requirement] [req=REQ-004] [ac=AC-007] [paths=scripts/test-sdd-contract.sh] Preserve the provider-neutral source skill and the closed WB-SKILL-002A lifecycle/P1 correction by enforcing the one-path source manifest.

## Define, Assurance, and Closeout

- [x] TASK-005 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-skill-002b-provider-guard-boundaries.md,docs/specs/wb-skill-002b-provider-guard-boundaries.md,docs/tasklist/wb-skill-002b-provider-guard-boundaries.md] Create bounded Managed Define artifacts and record the two confirmed P2 findings without modifying source or GitHub state.
- [ ] TASK-006 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-skill-002b-provider-guard-boundaries.md,docs/reports/requirements/wb-skill-002b-provider-guard-boundaries-consistency.md,docs/reports/reviews/wb-skill-002b-provider-guard-boundaries-critic.md] Obtain requirements-quality review, consistency analysis, and Critic evidence before any Write Gate decision.
- [ ] TASK-007 [type=requirement] [req=REQ-005] [ac=AC-008] [paths=docs/plans/wb-skill-002b-provider-guard-boundaries.md,docs/specs/wb-skill-002b-provider-guard-boundaries.md,docs/tasklist/wb-skill-002b-provider-guard-boundaries.md] Record a prospective Owner approval of an approved specification revision and the exact one-path source write-set before source Execute; this requirement controls the truthful transition from blocked Define authority to source authority.
- [ ] TASK-008 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-002b-provider-guard-boundaries.md,docs/reports/verification/wb-skill-002b-provider-guard-boundaries.md,docs/reports/drift/wb-skill-002b-provider-guard-boundaries.md] Freeze the source subject and obtain independent Reviewer, fresh-clone Verifier, and Drift evidence.
- [ ] TASK-009 [type=requirement] [req=REQ-006] [ac=AC-009] [paths=docs/reports/closeout/wb-skill-002b-provider-guard-boundaries.md] Complete terminal closeout only after required assurance; preserve the unresolved GitHub review threads until authorized separately.

## Dependencies and Stops

Source Execute is blocked until the draft specification is approved, Define
quality and Critic evidence are READY, and the Owner approves the exact
one-path write-set. No task authorizes source changes outside
`scripts/test-sdd-contract.sh`, a change to the provider-neutral skill,
governance/release-state/registry/map changes, external GitHub mutation,
commit, push, PR creation, merge, rebase, or thread resolution.

## Pre-Execution Validation

```bash
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-skill-002b-provider-guard-boundaries.md \
  --tasks docs/tasklist/wb-skill-002b-provider-guard-boundaries.md
```
