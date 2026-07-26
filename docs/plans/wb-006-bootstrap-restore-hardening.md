---
schema_version: 1
artifact_type: work_block
artifact_id: wb-006-bootstrap-restore-hardening
status: in_progress
owner_role: orchestrator
work_block_id: wb-006
created_at: 2026-07-26
last_verified: 2026-07-26
---

# WB-006 - Bootstrap Restore Hardening

## Objective

Address the two unresolved P2 Codex review findings from merged PR #5 by
hardening generated-project installation validation and clone/restore behavior.

## Expected Final Result

- Required installation-profile paths validate their expected filesystem kind,
  rejecting directories where files are required.
- Generated `.agent/bootstrap-profile.json` records expected required-path kinds.
- Generated health checks validate `.agent/active-work-block.default.json` before
  restoring `.agent/active-work-block.json`.
- The portable default Work Block must be valid JSON, `BLOCKED`,
  approval-free, integration-free, and empty-write-set.
- Regression fixtures prove both P2 cases fail closed.
- Navigation, registry, documentation, review, verification, drift, and closeout
  evidence are updated.
- A draft PR is opened from `agent/bootstrap-restore-hardening`, Framework
  Contracts pass, and the PR is made Ready for review.

## Scope

### In Scope

- `bootstrap/bootstrap_project.py`
- `template/scripts/validate-installation-profile.py`
- `template/scripts/bootstrap.sh`
- generated profile and clone/restore regression fixtures
- documentation, maps, registry, Work Block, and final review evidence
- Framework Contracts CI

### Out of Scope

- changing installation profile composition;
- adding an in-place upgrader;
- enabling runtime CLIs, plugins, MCP servers, credentials, or live smoke tests;
- changing Governance Core authority or lifecycle semantics;
- merging the PR without explicit Owner approval.

## Implementation Tasks

1. Record expected required-path kinds in generated installation profile state.
2. Make the generated validator enforce required-path kind instead of
   `.exists()` alone.
3. Validate portable blocked default Work Block invariants before restore.
4. Add regression fixtures for directory-as-file and corrupt default restore.
5. Update documentation, registry, and navigation.
6. Run local contract checks.
7. Open a draft PR, wait for Framework Contracts, write final review/closeout,
   and mark the PR Ready for review.

## Assurance Plan

Review:

- required files cannot be satisfied by directories;
- missing old `required_path_kinds` state remains safely treated as file
  requirements;
- blocked default validation runs before local state restore;
- existing active Work Block state is not overwritten;
- failure messages are actionable and fail closed.

Verification:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-bootstrap-profiles.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

## Current State

- **Stage:** Execute
- **Stage State:** in_progress
- **Write Gate:** READY for this branch and documented scope
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
