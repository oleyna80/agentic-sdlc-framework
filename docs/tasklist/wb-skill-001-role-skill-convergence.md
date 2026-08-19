# WB-SKILL-001 Tasklist — Framework-Native Role Skill Convergence

## Status and Scope Binding

The approved implementation subject is frozen as
`3ec044953a854dd8906a4849df507357bd3b87f0` →
`6744f1071090c98b59de9160b05b2cf4fb20158e`. The exact twelve-path Coder
source write-set below is complete and independently reviewed and verified
`READY`. Coordination/evidence records are not additions to that source
write-set.

The Owner separately authorized the current closeout synchronization on
2026-08-19 for exactly these repository paths:

- `docs/plans/wb-skill-001-role-skill-convergence.md`
- `docs/tasklist/wb-skill-001-role-skill-convergence.md`
- `docs/reports/reviews/wb-skill-001-independent-review.md`
- `docs/reports/verification/wb-skill-001-verification.md`
- `docs/reports/drift/wb-skill-001-role-skill-convergence.md`

and PR #41 body metadata, including required checks, commit, and feature-branch
push. The authorization does not permit modification of the twelve source paths
or the approved specification and does not authorize merge.

This tasklist records completion state; it does not independently grant Git or
source-write authority.

## Requirement Tasks

- [x] TASK-001 [type=requirement] [req=REQ-001,REQ-002,REQ-003,REQ-009,REQ-010] [ac=AC-001,AC-002,AC-003,AC-004,AC-011,AC-012] [paths=skills/critic-review/SKILL.md] Converge the routed Critic procedure while preserving the accepted functional-verdict and gate-state distinction; record `original_experience_derived` provenance from current local governance, a local convergence delta, and no novelty claim.
- [x] TASK-002 [type=requirement] [req=REQ-001,REQ-002,REQ-004,REQ-007,REQ-009,REQ-010] [ac=AC-001,AC-002,AC-005,AC-006,AC-009,AC-011,AC-012] [paths=skills/scoped-coder/SKILL.md] Converge the routed Coder procedure to write-set, Git-authority, Hard Stop, and project-neutral requirements; record the same truthful local-convergence provenance.
- [x] TASK-003 [type=requirement] [req=REQ-001,REQ-002,REQ-005,REQ-007,REQ-009,REQ-010] [ac=AC-001,AC-002,AC-007,AC-009,AC-011,AC-012] [paths=skills/reviewer/SKILL.md] Converge the routed Reviewer procedure to the frozen-subject, verdict, evidence, and project-neutral requirements; record the same truthful local-convergence provenance.
- [x] TASK-004 [type=requirement] [req=REQ-001,REQ-002,REQ-006,REQ-007,REQ-009,REQ-010] [ac=AC-001,AC-002,AC-008,AC-009,AC-011,AC-012] [paths=skills/verifier/SKILL.md] Converge the routed Verifier procedure to reproducible verification, non-exclusive progression, and project-neutral requirements; record the same truthful local-convergence provenance.
- [x] TASK-005 [type=requirement] [req=REQ-003,REQ-008,REQ-009] [ac=AC-003,AC-004,AC-010,AC-011] [paths=template/.claude/agents/critic.md] Correct the direct Claude Critic adapter because the inventory established a live role/lifecycle/read-only contradiction.
- [x] TASK-006 [type=requirement] [req=REQ-004,REQ-008] [ac=AC-005,AC-006,AC-010] [paths=template/.claude/agents/scoped-coder.md] Correct only the direct Claude Coder adapter wording that remains semantically contradictory.
- [x] TASK-007 [type=requirement] [req=REQ-005,REQ-008,REQ-009] [ac=AC-007,AC-010,AC-011] [paths=template/.claude/agents/reviewer.md] Correct the direct Claude Reviewer adapter because its current verdict/authority language conflicts with the shared contract.
- [x] TASK-008 [type=requirement] [req=REQ-006,REQ-008,REQ-009] [ac=AC-008,AC-010,AC-011] [paths=template/.claude/agents/verifier.md] Correct the direct Claude Verifier adapter because its current authority/reference language conflicts with the shared contract.
- [x] TASK-009 [type=requirement] [req=REQ-001,REQ-002,REQ-003,REQ-005,REQ-006,REQ-008,REQ-009] [ac=AC-001,AC-002,AC-003,AC-004,AC-007,AC-008,AC-010,AC-011] [paths=template/.codex/AGENTS.md] Correct the direct Codex runtime contract because its current lifecycle and exclusive-Verifier wording would remain a live contradiction.
- [x] TASK-010 [type=requirement] [req=REQ-002,REQ-003,REQ-008,REQ-009] [ac=AC-002,AC-003,AC-004,AC-010,AC-011] [paths=template/.codex/critic.md] Correct the direct Codex Critic adapter because its parallel stage mapping conflicts with current Critic semantics.
- [x] TASK-011 [type=requirement] [req=REQ-001,REQ-002,REQ-004,REQ-008,REQ-009] [ac=AC-001,AC-002,AC-005,AC-006,AC-010,AC-011] [paths=template/.codex/instructions.md] Correct the direct Codex instruction because its Control Tower and parallel lifecycle text remains a live contradiction.
- [x] TASK-012 [type=requirement] [req=REQ-011] [ac=AC-013] [paths=scripts/test-sdd-contract.sh] Extend the existing contract-test owner with the smallest sufficient critical-role regression assertions; this bucket-B path is required for deterministic protection, not general policy enforcement.
- [x] TASK-013 [type=requirement] [req=REQ-012] [ac=AC-014] [paths=docs/plans/wb-skill-001-role-skill-convergence.md,docs/tasklist/wb-skill-001-role-skill-convergence.md] Preserve the approved critical-path boundary, bucket-C/D deferral, and separate aggregate/Spec Kit exclusions in the execution artifacts.

## Supporting Bucket-B Decisions

| Path | Decision | Reason |
|---|---|---|
| `template/.codex/AGENTS.md` | REQUIRED | A live direct Codex adapter assigned old lifecycle and exclusive Verifier authority. |
| `template/.codex/critic.md` | REQUIRED | A live direct Critic adapter retained the parallel stage flow. |
| `template/.codex/instructions.md` | REQUIRED | A live direct runtime instruction retained Control Tower and parallel lifecycle semantics. |
| `scripts/test-sdd-contract.sh` | REQUIRED | It is the existing smallest sufficient owner for deterministic critical-role regression coverage. |

## Define and Assurance Tasks

- [x] TASK-014 [type=documentation] [req=-] [ac=-] [paths=docs/plans/wb-skill-001-role-skill-convergence.md,docs/specs/wb-skill-001-role-skill-convergence.md,docs/tasklist/wb-skill-001-role-skill-convergence.md,docs/reports/requirements/wb-skill-001-consistency.md] Maintain the authoritative Define plan, specification, task traceability, and evidence bindings without granting source authority.
- [x] TASK-015 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-001-critic.md] Obtain a separate read-only Critic review of the exact proposed source write-set before Execute; functional verdict `SUPPLEMENT` was addressed by Define synchronization.
- [x] TASK-016 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-001-independent-review.md] Obtain independent read-only implementation review against frozen subject `3ec044953a854dd8906a4849df507357bd3b87f0` → `6744f1071090c98b59de9160b05b2cf4fb20158e`; final verdict `READY`.
- [x] TASK-017 [type=assurance] [req=-] [ac=-] [paths=docs/reports/verification/wb-skill-001-verification.md] Obtain independent read-only reproducible verification against the same frozen subject, including the focused regression and canonical checks; final verdict `READY`.

## Drift and Closeout State

The first independent Specification Drift Audit for the assured implementation
subject returned `ALIGNMENT_REQUIRED`: implementation/specification alignment is
complete, while lifecycle/task/evidence/PR metadata required synchronization.
The audit is persisted at
`docs/reports/drift/wb-skill-001-role-skill-convergence.md`.

A passing re-audit remains required before successful Close. The source
implementation and approved specification are not reopened by this bookkeeping
correction.

## Explicitly Deferred

Inventory bucket C, historical bucket D, canonical content aggregate SHA
hardening, and Spec Kit behavior remain outside this tasklist. They need a new
approved Work Block if later evidence establishes a critical-path requirement.
