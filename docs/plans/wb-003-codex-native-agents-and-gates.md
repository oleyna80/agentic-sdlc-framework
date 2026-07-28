---
schema_version: 1
artifact_type: work_block
artifact_id: wb-003-codex-native-agents-and-gates
status: completed
owner_role: orchestrator
work_block_id: wb-003
created_at: 2026-07-25
last_verified: 2026-07-26
---

# WB-003 — Codex-Native Agents and Executable Gates

## Objective

Turn the Codex adapter from policy-only documentation into an executable,
project-scoped runtime implementation while preserving the runtime-neutral
Governance Core.

## Delivered Result

- Added Codex project-scoped logical agents for Architect, Critic, Coder,
  Reviewer, and Verifier.
- Kept logical authority independent from model names and provider identity.
- Restricted implementation/source writes to the Coder role and approved write set.
- Added Work Block, stage-zero write, scope, and Hard Stop policy hooks.
- Added consequential-operation approval checks.
- Added Codex adapter and Hard Stop positive/adversarial fixtures.
- Registered Codex as one runtime adapter rather than the Governance Core.

## Scope Boundary

WB-003 did not activate external integrations, install credentials, replace the
portable Governance Core, or prove live provider/OS isolation. Integration
normalization and cross-runtime conformance were delivered later.

## Acceptance Result

- [x] Codex role definitions implement the shared logical-role contract.
- [x] Coder is the only implementation-write authority.
- [x] Reviewer and Verifier remain read-only assurance roles.
- [x] Work Block state controls source-write admission.
- [x] Hard Stops fail closed without explicit approvals.
- [x] Runtime-specific configuration cannot expand governance authority.
- [x] Executable adapter fixtures cover allowed and denied operations.

## Evidence

- Codex runtime adapter: `runtimes/codex/`
- Generated Codex surface: `template/.codex/`
- Adapter fixtures: `scripts/test-codex-adapter.py`
- Hard Stop fixtures: `scripts/test-codex-hard-stops.py`
- Final review: `docs/reports/reviews/pr-3-final-review.md`

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
