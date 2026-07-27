---
schema_version: 1
artifact_type: work_block
artifact_id: wb-008-post-merge-ssot-release-gate
status: completed
owner_role: orchestrator
work_block_id: wb-008
created_at: 2026-07-26
last_verified: 2026-07-27
---

# WB-008 — Post-Merge SSOT Reconciliation and Release Gate

## Objective

Eliminate lifecycle drift between completed Work Blocks, `PROJECT_MAP.md`,
`FILE_REGISTRY.yml`, closeout evidence, and repository release state, then add an
executable release-state gate that fails closed when these sources disagree.

## Delivered Result

- normalized the completed migration ledger WB-001 through WB-008;
- reconciled Work Block, map, registry, and closeout state;
- separated repository lifecycle from mutable hosting-platform state;
- added `governance/release-state.md`;
- added machine and visible release-state projections;
- added `scripts/validate-release-state.py`;
- added positive and adversarial release-state fixtures;
- added `.github/workflows/release-state-contract.yml`;
- integrated release-state validation into governance checks;
- resolved two Codex Review correction cycles.

## Enforced Invariants

1. Completed Work Blocks exist, use `status: completed`, and contain exactly one
   `Final State` or legacy `Closeout State` section.
2. Terminal review, verification, evaluation when declared, drift, closeout, and
   task values are validated explicitly.
3. `BLOCKED`, `UNVERIFIED`, `MISALIGNED`, pending, missing, or contradictory
   lifecycle evidence fails closed.
4. Completed Work Block paths and IDs are unique and disjoint from active state.
5. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` agree exactly and in order.
6. Visible active/no-active navigation is scoped to the unique `Migration Work`
   section.
7. Latest completed and closeout identity match exactly.
8. Duplicate normalized closeout markers are rejected.
9. Evaluation declared by the latest Work Block is mandatory in closeout with the
   same terminal `READY` or `SKIPPED` token.
10. Closeout drift requires exact `ALIGNED`.
11. Mutable hosting-platform status assertions are excluded from normative closeout.
12. Residual risks and follow-up work are mandatory non-empty closeout sections.
13. Release contract assets exist at canonical paths.
14. Release-state evidence is assurance-only and cannot authorize external actions.

## Scope Boundary

WB-008 did not deliver live runtime smoke, production telemetry, automatic
hosting-platform self-commits, release tags, in-place upgrades, model routing, or
changes to runtime/evaluation authority.

## Evidence

- Governance: `governance/release-state.md`
- Validator: `scripts/validate-release-state.py`
- Fixtures: `scripts/test-release-state-contracts.py`
- Dedicated CI: `.github/workflows/release-state-contract.yml`
- Final review: `docs/reports/reviews/pr-8-final-review.md`
- Drift audit: `docs/reports/drift/wb-008-post-merge-ssot-release-gate.md`
- Closeout: `docs/reports/closeout/wb-008-post-merge-ssot-release-gate.md`
- Reviewed implementation revision: `8ccd56e23e62741eb546c6a3f64e2df746bcf119`
- Release State Contract run 38: success
- Framework Contracts run 487: success

Release State Contract run 8 remains recorded as a failed fixture-order attempt,
followed by a scoped correction. Both Codex Review rounds were handled through
new implementation and dedicated regression evidence.

## Acceptance Result

- [x] Completed Work Blocks use canonical completed metadata and terminal evidence.
- [x] Adverse lifecycle verdicts cannot pass through exact-string blacklist gaps.
- [x] Required evaluation cannot disappear during closeout.
- [x] Machine and visible navigation remain synchronized.
- [x] Hosting-platform state is explicitly non-normative.
- [x] Duplicate closeout markers fail closed.
- [x] Residual-risk and follow-up sections are executable requirements.
- [x] Dedicated release-state CI runs on push and pull request events.
- [x] Existing Framework Contracts remain green.
- [x] Final review, drift, and closeout evidence are synchronized.
- [x] Repository lifecycle closes with no active implementation Work Block.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic release-state contract is sufficient
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
