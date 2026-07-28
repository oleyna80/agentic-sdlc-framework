---
schema_version: 1
artifact_type: work_block
artifact_id: wb-005-profile-aware-bootstrap-conformance
status: completed
owner_role: orchestrator
work_block_id: wb-005
created_at: 2026-07-25
last_verified: 2026-07-26
---

# WB-005 — Profile-Aware Bootstrap and Cross-Runtime Conformance

## Objective

Make generated-project installation selectively composable without coupling
installation composition to governance authority, and prove semantic conformance
across supported runtime adapters.

## Delivered Result

- Added manifest-driven profiles: `core`, `codex`, `claude-code`, `opencode`, and
  `multi-runtime`.
- Added compatibility aliases `minimal`/`generic` → `core` and `full` →
  `multi-runtime`.
- Preserved `multi-runtime` as the backward-compatible default.
- Added transactional `bootstrap/bootstrap_project.py` and compatible `bootstrap.sh`.
- Added generated `.agent/bootstrap-profile.json` installation evidence.
- Enforced exact selected and unselected runtime surfaces.
- Added generated installation-profile validation and fail-closed target handling.
- Added clone/restore fixtures and canonical blocked defaults.
- Added semantic cross-runtime conformance for logical roles, write authority,
  shared Work Block/Hard Stop behavior, and inert integrations.
- Added profile matrix, runtime conformance, publication, and CI validation.

## Scope Boundary

WB-005 did not install runtime CLIs, credentials, plugins, MCP servers, providers,
or services; did not select concrete models; and did not claim live paid-runtime
or OS-sandbox proof.

## Acceptance Result

- [x] Installation profiles are data-driven and validated before target mutation.
- [x] Fresh scaffolds contain exactly the selected runtime implementation surfaces.
- [x] Governance and portable artifacts remain present in every profile.
- [x] Installation evidence is separate from Work Block authority.
- [x] Unknown profiles, unsafe paths, symlinks, and non-empty targets fail closed.
- [x] Cross-runtime fixtures preserve the same logical authority contract.
- [x] Integrations remain inert unless separately admitted.
- [x] Framework Contracts and publication checks cover every profile and alias.

## Evidence

- Profile manifest: `bootstrap/profiles.json`
- Bootstrap engine: `bootstrap/bootstrap_project.py`
- Profile fixtures: `scripts/test-bootstrap-profiles.py`
- Restore fixtures: `scripts/test-profile-restore.py`
- Runtime conformance: `scripts/test-runtime-conformance.py`
- Final review: `docs/reports/reviews/pr-5-final-review.md`

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
