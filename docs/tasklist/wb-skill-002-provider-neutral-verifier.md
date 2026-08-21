---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-SKILL-002
specification: docs/specs/wb-skill-002-provider-neutral-verifier.md
specification_revision: define-r2-2026-08-21
status: in_progress
---

# WB-SKILL-002 Tasklist — Provider-Neutral Verifier Legacy Skill Correction

## Requirement Delivery

- [ ] TASK-001 [type=requirement] [req=REQ-001,REQ-002,REQ-003,REQ-004,REQ-005] [ac=AC-001,AC-002,AC-003,AC-004,AC-005] [paths=skills/codex-verification/SKILL.md] Replace only the legacy role/lifecycle/provider-prerequisite procedure with a bounded optional runtime-adapter procedure that defers to accepted governance and the active Work Block.
- [ ] TASK-002 [type=requirement] [req=REQ-006] [ac=AC-006] [paths=scripts/test-sdd-contract.sh] Add deterministic target-file-only protection for every required and forbidden current-skill invariant.
- [ ] TASK-003 [type=requirement] [req=REQ-007] [ac=AC-007] [paths=docs/plans/wb-skill-002-provider-neutral-verifier.md,docs/tasklist/wb-skill-002-provider-neutral-verifier.md] Preserve the exact two-path source boundary and recorded exclusions throughout Execute and Assure.

## Define and Assurance

- [ ] TASK-004 [type=documentation] [req=-] [ac=-] [paths=docs/specs/wb-skill-002-provider-neutral-verifier.md,docs/plans/wb-skill-002-provider-neutral-verifier.md,docs/tasklist/wb-skill-002-provider-neutral-verifier.md,FILE_REGISTRY.yml,PROJECT_MAP.md] Maintain the authoritative Define artifacts and active Work Block projection; do not grant source authority.
- [x] TASK-005 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-skill-002-provider-neutral-verifier.md,docs/reports/requirements/wb-skill-002-provider-neutral-verifier-rereview.md] Preserve the initial independent requirements-quality review and obtain a fresh independent re-review of the revised specification.
- [x] TASK-006 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-skill-002-provider-neutral-verifier-consistency.md,docs/reports/requirements/wb-skill-002-provider-neutral-verifier-consistency-rereview.md] Preserve the initial independent consistency analysis and obtain a fresh re-analysis after its owning projection correction.
- [x] TASK-007 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-002-provider-neutral-verifier-critic.md,docs/reports/reviews/wb-skill-002-provider-neutral-verifier-critic-rereview.md] Preserve the initial Critic review and obtain a fresh Critic review after Define-quality readiness is recorded, before any source Write Gate decision.
- [ ] TASK-008 [type=assurance] [req=-] [ac=-] [paths=docs/reports/reviews/wb-skill-002-provider-neutral-verifier.md,docs/reports/verification/wb-skill-002-provider-neutral-verifier.md,docs/reports/drift/wb-skill-002-provider-neutral-verifier.md] Obtain independent final Reviewer, Verifier, and Drift evidence for the exact frozen source subject.

## Dependencies and Stops

The two source requirement tasks depend on the three preceding Define-assurance
tasks; only one Coder may own their shared source write-set. Final assurance
depends on a frozen post-Execute subject. No task authorizes a profile/preset, extension,
workflow, bundle, provider setup, commit, push, pull request, merge, or
deployment action.

## Pre-Execution Validation

```bash
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-skill-002-provider-neutral-verifier.md \
  --tasks docs/tasklist/wb-skill-002-provider-neutral-verifier.md
```
