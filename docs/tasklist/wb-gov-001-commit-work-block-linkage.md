---
schema_version: 1
artifact_type: tasklist
work_block_id: WB-GOV-001
specification: docs/specs/wb-gov-001-commit-work-block-linkage.md
specification_revision: owner-approved-2026-09-06
status: in_progress
---

# WB-GOV-001 tasklist

- [ ] TASK-001 [type=requirement] [req=REQ-001,REQ-002,REQ-003,REQ-004,REQ-005,REQ-006] [ac=AC-001,AC-002,AC-003,AC-004,AC-005,AC-006,AC-014,AC-016] [paths=template/.githooks/commit-msg,scripts/test-commit-work-block-linkage.sh] Implement and test structured state/trailer enforcement.
- [ ] TASK-002 [type=requirement] [req=REQ-007,REQ-008] [ac=AC-007,AC-008,AC-013] [paths=template/.githooks/commit-msg,template/scripts/bootstrap.sh,bootstrap/profiles.json] Add portable hook and explicit local-only activation/check.
- [ ] TASK-003 [type=requirement] [req=REQ-009,REQ-010] [ac=AC-009,AC-010,AC-015,AC-017] [paths=scripts/test-commit-work-block-linkage.sh,.github/workflows/framework-contracts.yml] Add deterministic fixture and CI integration.
- [ ] TASK-004 [type=requirement] [req=REQ-011] [ac=AC-011] [paths=governance/commit-work-block-linkage.md,governance/lifecycle.md,docs/bootstrap-profiles.md,skills/scoped-commit-guard/SKILL.md] Publish one normative contract and referential guidance.
- [ ] TASK-005 [type=requirement] [req=REQ-012] [ac=AC-012,AC-018] [paths=docs/reports/reviews/wb-gov-001-commit-work-block-linkage.md,docs/reports/verification/wb-gov-001-commit-work-block-linkage.md] Verify scope, schema, and reserved-roadmap boundaries.
- [ ] TASK-006 [type=assurance] [req=-] [ac=AC-017] [paths=docs/reports/drift/wb-gov-001-commit-work-block-linkage.md,docs/reports/closeout/wb-gov-001-commit-work-block-linkage.md] Record drift, publication, release-state, and closeout evidence.
- [ ] TASK-007 [type=assurance] [req=-] [ac=-] [paths=docs/reports/requirements/wb-gov-001-commit-work-block-linkage.md] Record Define quality and structural traceability evidence.

## Stop conditions

Do not broaden the write-set, change schema v3, activate the current framework
checkout's hooksPath, open a PR, merge, push protected/default branches, or touch
WB-CORE-004 through WB-CORE-007.
