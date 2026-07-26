---
schema_version: 1
artifact_type: work_block
artifact_id: wb-001-runtime-neutral-control-plane
status: completed
owner_role: orchestrator
work_block_id: wb-001
created_at: 2026-07-25
last_verified: 2026-07-26
---

# WB-001 — Runtime-Neutral Control Plane

## Objective

Refactor the framework so that the Agentic SDLC core manages work independently
of any specific agent runtime, model provider, or integration mechanism.

## Delivered Result

- Accepted `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.
- Added the runtime-neutral Governance Core under `governance/`.
- Added Codex, Claude Code, OpenCode, and generic adapter boundaries under
  `runtimes/`.
- Separated logical role, runtime, model, specialization, isolation, and tool
  capability.
- Reclassified plugins, MCP, and file handoff as optional integrations/transports
  rather than authority-bearing governance.
- Updated repository overview, navigation, registry, and structural governance
  validation.

## Scope Boundary

WB-001 established the architecture. Portable template convergence, executable
runtime gates, integration normalization, installation profiles, evaluation, and
release-state reconciliation were intentionally delivered by later Work Blocks.

## Acceptance Result

- [x] Core architecture is explicitly runtime-neutral.
- [x] Logical roles are separate from runtime, model, and isolation.
- [x] Governance functions do not require one process per role.
- [x] Runtime adapters expose capabilities without redefining authority.
- [x] Integrations and legacy transports are outside the Governance Core.
- [x] Repository navigation points to the normative control-plane documents.

## Evidence

- Architecture decision: `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`
- Governance validation: `scripts/validate-governance.sh`
- Historical implementation branch: `agent/runtime-neutral-control-plane`

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
