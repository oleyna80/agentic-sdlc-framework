---
schema_version: 1
artifact_type: closeout_report
artifact_id: wb-gov-001-commit-work-block-linkage-closeout
status: superseded
owner_role: orchestrator
work_block_id: WB-GOV-001
subject_revision: 1f508bf6eefc577951a2102685a41a94e4bdd949
created_at: 2026-09-06
last_verified: 2026-09-06
---

# WB-GOV-001 — Historical / Superseded Closeout Record

## Superseded Status

This closeout artifact represents a superseded, historical closeout projection.
In commit `8ef2caa03b9c7c68f708b9b35572a45a98463efc` (H4), an invalid raw-history
terminal projection was prematurely recorded (modifying raw `completed_work_blocks`
and raw `release_state` after canonical promotion history existed).

Hosted CI correctly rejected that projection because post-promotion raw release-state
history is immutable. Canonical completion of WB-GOV-001 is being conducted through
the prospective successor candidate flow (`candidate -> evidence persistence -> promotion`).
The fresh canonical terminal evidence is recorded in the `-r2.md` evidence paths:

- Review: `docs/reports/reviews/wb-gov-001-commit-work-block-linkage-r2.md`
- Verification: `docs/reports/verification/wb-gov-001-commit-work-block-linkage-r2.md`
- Drift: `docs/reports/drift/wb-gov-001-commit-work-block-linkage-r2.md`
- Closeout: `docs/reports/closeout/wb-gov-001-commit-work-block-linkage-r2.md`

This document is preserved for historical lineage and auditability across H1, H2, H3, and H4.

## Historical Result (Implementation H3)

The framework provides an opt-in, local-only commit-to-Work-Block linkage
contract and strictly read-only hook validation. Active schema-v3 Work Blocks
require exactly one canonical `Work-Block: <exact-current-work_block_id>` trailer
for hook-invoking commit flows; empty and retained terminal records remain
inactive. Generated projects receive the executable hook in every profile, while
hook installation is explicit and repository-local. Known commit-producing
limitations outside `commit-msg` invocation (such as `git cherry-pick` and
`git revert`) are documented and proven by fixtures as cooperative boundaries.

## PR #51 Correction Inputs

1. **Lifecycle reconciliation (P1):** Corrected lifecycle sequencing via prospective candidate flow.
2. **Read-only check (P2):** Corrected `template/scripts/bootstrap.sh --check-git-hooks`
   to exit immediately after validation without falling through to normal bootstrap,
   modifying Git configuration, or creating/rewriting operational files.
3. **Enforcement guarantee & known bypasses (P2):** Narrowed normative guarantee to
   hook-invoking commit flows, documented known bypasses and non-invoking paths,
   and added deterministic regression fixtures.

## Revision Lineage and Historical Subjects

- **Baseline:** `be988807c38543eb90a728fcb4349bc97dd5695a`
- **Initial frozen implementation subject (H1):** `a97e05643613946fc20c8c50a31647c1da9852d0`
- **Previous evidence head (H2):** `09adfbd990e76668ff8d95e1da4105230146bd9e`
- **Corrected frozen implementation subject (H3):** `1f508bf6eefc577951a2102685a41a94e4bdd949`
- **Invalid premature terminal projection head (H4):** `8ef2caa03b9c7c68f708b9b35572a45a98463efc`
- **Successor Candidate Revision (H5):** declared under prospective release-state flow.

Independent Review, Verification, and Drift originally assured immutable implementation
subject H3 (`1f508bf6eefc577951a2102685a41a94e4bdd949`). Fresh candidate assurance evaluates H5.

## Historical Evidence Summary

- normative contract: `governance/commit-work-block-linkage.md`;
- implementation: `template/.githooks/commit-msg`, `template/scripts/bootstrap.sh`;
- fixture: `scripts/test-commit-work-block-linkage.sh` — **55 assertions PASS**;
- profile matrix, CI router, SDD, governance, traceability, and release-state
  validations: PASS/READY.

## Residual Risks and Limitations

- The project-local `commit-msg` hook is a cooperative local governance guard,
  not an operating-system or server-side security boundary.
- Known commit-producing paths outside the guaranteed enforcement of `commit-msg`
  (including `git commit --no-verify`, `git cherry-pick`, `git revert`, uninstalled hooks,
  and GitHub API / web-created commits) remain documented cooperative limitations.
