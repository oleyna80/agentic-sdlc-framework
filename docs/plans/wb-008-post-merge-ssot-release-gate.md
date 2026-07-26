---
schema_version: 1
artifact_type: work_block
artifact_id: wb-008-post-merge-ssot-release-gate
status: completed
owner_role: orchestrator
work_block_id: wb-008
created_at: 2026-07-26
last_verified: 2026-07-26
---

# WB-008 — Post-Merge SSOT Reconciliation and Release Gate

## Objective

Eliminate lifecycle drift between completed Work Blocks, `PROJECT_MAP.md`,
`FILE_REGISTRY.yml`, closeout evidence, and repository release state, then add an
executable release-state gate that fails closed when these sources disagree.

## Delivered Result

- normalized completed Work Blocks WB-001 through WB-007;
- reconciled WB-007 Work Block and closeout evidence;
- defined repository lifecycle versus mutable GitHub-state ownership;
- added `governance/release-state.md`;
- added a machine-readable release-state projection to `PROJECT_MAP.md`;
- added `FILE_REGISTRY.yml:release_state`;
- added `scripts/validate-release-state.py`;
- added positive and adversarial release-state fixtures;
- added `.github/workflows/release-state-contract.yml`;
- integrated release-state validation into governance checks;
- documented the contract in README and project navigation.

## Enforced Invariants

1. Completed Work Blocks exist, use `status: completed`, and contain no pending
   final lifecycle markers.
2. Completed Work Block IDs are unique.
3. An active Work Block is optional, active, and disjoint from completed paths and
   IDs.
4. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` agree exactly and in order.
5. Visible map navigation agrees with its machine block.
6. Latest completed equals the final ordered completed entry.
7. Closeout identity exactly matches the latest Work Block.
8. Review, verification, evaluation when present, drift, and closeout are internally
   successful.
9. Release contract assets exist at canonical paths.
10. Release-state evidence is assurance-only and cannot authorize external actions.
11. Mutable GitHub status is external operational metadata, not normative closeout.

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
- Framework Contracts run 459: success
- Release State Contract run 10: success

Release State Contract run 8 remains recorded as a failed fixture-order attempt,
followed by a scoped correction and successful rerun.

## Acceptance Result

- [x] WB-007 is completed in all repository lifecycle consumers.
- [x] Historical migration Work Blocks use canonical completed metadata.
- [x] No repository closeout predicts mutable GitHub state.
- [x] GitHub state is explicitly non-normative.
- [x] Release-state validator passes on the repository.
- [x] Adversarial fixtures cover all declared drift classes.
- [x] Dedicated release-state CI runs on push and pull request events.
- [x] Existing Framework Contracts remain green.
- [x] Final review and drift audit are complete.
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
