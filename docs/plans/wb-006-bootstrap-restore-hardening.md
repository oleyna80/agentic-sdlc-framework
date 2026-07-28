---
schema_version: 1
artifact_type: work_block
artifact_id: wb-006-bootstrap-restore-hardening
status: completed
owner_role: orchestrator
work_block_id: wb-006
created_at: 2026-07-26
last_verified: 2026-07-26
---

# WB-006 — Bootstrap Restore Hardening

## Objective

Resolve the P2 and P1 review findings left around generated-project path-kind and
blocked-default restore validation.

## Delivered Result

- Required installation-profile paths now validate expected filesystem kinds and
  reject directories where files are required.
- Generated profile evidence records required-path kinds.
- `.agent/active-work-block.default.json` is validated before restoring local
  active Work Block state.
- Portable default state must be valid JSON, `BLOCKED`, approval-free,
  integration-free, and empty-write-set.
- Authorization-bearing `coordination_write_set` must exactly match the canonical
  ordered safe coordination paths.
- Broad wildcards, arbitrary source paths, repository roots, absolute paths,
  traversal paths, missing/additional/reordered values, malformed values, and
  non-string entries fail closed.
- Canonical blocked defaults still restore successfully.
- Regression fixtures cover directory-as-file, corrupted defaults, and authority
  broadening attempts.

## Scope Boundary

WB-006 did not change profile composition, add an in-place upgrader, enable live
runtimes/integrations, or change Governance Core authority semantics.

## Acceptance Result

- [x] Required files cannot be satisfied by directories.
- [x] Blocked default validation runs before local-state restore.
- [x] Coordination authority exactly matches the canonical ordered safe set.
- [x] Unsafe wildcard/root/absolute/traversal/source paths deny restore.
- [x] Missing, additional, reordered, malformed, and non-string entries deny restore.
- [x] Existing active state is not overwritten.
- [x] Framework Contracts and final review completed successfully.

## Evidence

- Installation validator: `template/scripts/validate-installation-profile.py`
- Profile fixtures: `scripts/test-bootstrap-profiles.py`
- Clone/restore fixtures: `scripts/test-profile-restore.py`
- Final review: `docs/reports/reviews/pr-6-final-review.md`
- Framework Contracts runs 321–324, including final successful head
  `54e1b5a5bb1cc23b60251febd2ea3e06806747aa`

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
