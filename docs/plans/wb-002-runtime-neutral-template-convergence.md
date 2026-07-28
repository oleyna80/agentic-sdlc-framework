---
schema_version: 1
artifact_type: work_block
artifact_id: wb-002-runtime-neutral-template-convergence
status: completed
owner_role: orchestrator
work_block_id: wb-002
created_at: 2026-07-25
last_verified: 2026-07-26
---

# WB-002 — Runtime-Neutral Template Convergence

## Objective

Align the generated-project contract with the runtime-neutral Governance Core so
that project scaffolds describe authority, lifecycle, artifacts, and evidence
without making a provider or runtime authoritative.

## Delivered Result

- Normalized generated `AGENTS.md` around logical roles.
- Converged the lifecycle on Define / Execute / Assure / Close.
- Separated Critic, Reviewer, Verifier, and Specification Drift functions.
- Placed approved specifications above plans and tasklists in the SSOT order.
- Added portable capability, model-class, runtime, and isolation fields to Work
  Block templates.
- Added the reusable specification-drift audit skill and report template.
- Copied Governance Core and runtime-adapter documentation into generated projects.
- Normalized generated map, registry, and session-bootstrap navigation.
- Added runtime-neutral structural contract checks and GitHub Actions execution.

## Scope Boundary

WB-002 did not add executable Codex hooks, final runtime-specific agents,
profile-aware selective bootstrap, or live cross-runtime smoke. Those items were
handled by later Work Blocks.

## Acceptance Result

- [x] No provider-named role is required by the generated-project core contract.
- [x] Logical authority roles are runtime-neutral.
- [x] Review, verification, and drift are distinct assurance functions.
- [x] Specification authority remains above derived plans and tasklists.
- [x] Generated Work Blocks record runtime and assurance dimensions separately.
- [x] Generated navigation and bootstrap are progressive and runtime-neutral.
- [x] Existing runtime and integration surfaces remain adapters.
- [x] Framework Contracts execute governance, structural, and publication checks.

## Evidence

- Generated contract: `template/AGENTS.md`
- SDLC protocol: `template/.agent/workflows/sdd-protocol.md`
- Structural validation: `scripts/test-sdd-contract.sh`
- Framework workflow: `.github/workflows/framework-contracts.yml`

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
