---
schema_version: 1
artifact_type: verification_report
artifact_id: wb-opencode-002-project-local-integration-verification
work_block_id: WB-OPENCODE-002
verified_stage: assure
verified_subject: replacement candidate 63f88e3174668a8707445e54807c9cfcb2fbb81c and close projection
verdict: READY
created_at: 2026-08-11
isolation: isolated_publication_copy
recorded_by_role: orchestrator
---

# Verification Report — WB-OPENCODE-002

## Verdict

**READY.** Replacement verification assessed the bounded close projection in an
isolated publication copy. The previously unavailable shared-tree publication
context is resolved as an isolation condition, not a current verification
blocker.

## Required gate evidence

- [PASS] `python3 scripts/validate-release-state.py`
- [PASS] `python3 scripts/test-release-state-contracts.py`
- [PASS] `python3 scripts/test-integration-contracts.py`
- [PASS] `bash scripts/test-sdd-contract.sh`
- [PASS] `bash scripts/validate-governance.sh`
- [PASS] `git diff --check`

The Work Block terminal markers, map/registry projection, review evidence,
verification evidence, and approved closeout are mutually consistent. No live
runtime invocation, external provider, authentication, or mutable VCS state is
claimed.

## Residual limitation

Live OpenCode discovery and permission-merging behavior remains `UNVERIFIED`;
separate Owner approval is required before a live smoke.
