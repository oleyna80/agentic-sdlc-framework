---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-SKILL-002B
specification: docs/specs/wb-skill-002b-provider-guard-boundaries.md
specification_revision: execute-r1-2026-08-23
status: in_progress
---

# WB-SKILL-002B Tasklist — Provider Guard Imperative and Fence Boundary Correction

## Requirement Delivery

- [ ] TASK-001 [type=requirement] [req=REQ-001] [ac=AC-001,AC-002] [paths=scripts/test-sdd-contract.sh] Make the existing target-only predicate reject only the specified optional-purpose/polite `ask` or `request` provider-assurance forms, including ordinary wrapping, without widening its file scope or introducing general NLP.
- [ ] TASK-002 [type=requirement] [req=REQ-002] [ac=AC-003,AC-004] [paths=scripts/test-sdd-contract.sh] Replace fence-toggle behavior with at-most-three-space regular-opener character/run-length tracking and compatible closer validation while retaining exclusion through invalid or unclosed fences.
- [ ] TASK-003 [type=requirement] [req=REQ-003] [ac=AC-005,AC-006] [paths=scripts/test-sdd-contract.sh] Add adversarial fixtures that invoke the production predicate for specified imperative, wrapping, allowed negative/advisory, valid-closer, invalid-closer, and statement-boundary cases.
- [ ] TASK-004 [type=requirement] [req=REQ-004] [ac=AC-007] [paths=scripts/test-sdd-contract.sh] Preserve the provider-neutral source skill and the closed WB-SKILL-002A lifecycle/P1 correction; source scope is preserved by Coder write-set control and later Reviewer/Verifier diff evidence, not by this script.

## Define, Assurance, and Closeout

- [x] TASK-005 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-skill-002b-provider-guard-boundaries.md,docs/specs/wb-skill-002b-provider-guard-boundaries.md,docs/tasklist/wb-skill-002b-provider-guard-boundaries.md] Create bounded Managed Define artifacts and record the two confirmed P2 findings without modifying source or GitHub state.
- [x] TASK-006 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-skill-002b-provider-guard-boundaries.md,docs/reports/requirements/wb-skill-002b-provider-guard-boundaries-consistency.md,docs/reports/reviews/wb-skill-002b-provider-guard-boundaries-critic.md] Obtain requirements-quality review, consistency analysis, and Critic evidence before any Write Gate decision. Evidence: requirements READY, consistency READY, and Critic READY for exact Define subject `848be54d8d501e824e58ee8112f04b9111f72b7b`.
- [x] TASK-007 [type=requirement] [req=REQ-005] [ac=AC-008] [paths=docs/plans/wb-skill-002b-provider-guard-boundaries.md,docs/specs/wb-skill-002b-provider-guard-boundaries.md,docs/tasklist/wb-skill-002b-provider-guard-boundaries.md] Record the Owner's prospective 2026-08-23 approval of specification revision `execute-r1-2026-08-23` and exactly the one-path source write-set `scripts/test-sdd-contract.sh` before source Execute. This approval establishes WB-SKILL-002B Execute authority only; it is not retrospective and grants no commit, push, pull-request, merge, or GitHub-thread authority.
- [ ] TASK-008 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-002b-provider-guard-boundaries.md,docs/reports/verification/wb-skill-002b-provider-guard-boundaries.md,docs/reports/drift/wb-skill-002b-provider-guard-boundaries.md] Freeze the source subject and obtain independent Reviewer, fresh-clone Verifier, and Drift evidence. Reviewer and Verifier must run `git diff --name-status <frozen-base>..<frozen-head>` and `git diff --check` to prove AC-007.
- [ ] TASK-009 [type=requirement] [req=REQ-006] [ac=AC-009] [paths=docs/reports/closeout/wb-skill-002b-provider-guard-boundaries.md] Complete terminal closeout only after required assurance; preserve the unresolved GitHub review threads until authorized separately.

## Dependencies and Stops

The approved specification, Define quality, Critic evidence, and the Owner's
prospective approval of exactly `scripts/test-sdd-contract.sh` are recorded;
the Write Gate is READY for bounded source Execute. No source task has started.
No task authorizes source changes outside
`scripts/test-sdd-contract.sh`, a change to the provider-neutral skill,
governance/release-state/registry/map changes, external GitHub mutation,
commit, push, PR creation, merge, rebase, or thread resolution.

## Pre-Execution Validation

```bash
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-skill-002b-provider-guard-boundaries.md \
  --tasks docs/tasklist/wb-skill-002b-provider-guard-boundaries.md
```
