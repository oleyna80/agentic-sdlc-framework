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
executable fail-closed release-state gate.

## Delivered Result

- normalized completed Work Blocks WB-001 through WB-008;
- reconciled map, registry, README, Work Block, and closeout state;
- separated repository lifecycle from mutable hosting-platform metadata;
- added `governance/release-state.md`;
- added `scripts/validate-release-state.py` and adversarial fixtures;
- added `.github/workflows/release-state-contract.yml`;
- integrated release-state checks into Framework Contracts;
- resolved four Codex Review rounds with dedicated regressions.

## Final Invariants

1. Completed Work Blocks use canonical frontmatter and one terminal state section.
2. Non-evaluation terminal markers are compared as complete exact values.
3. Evaluation accepts exact `READY` or `SKIPPED — <non-empty rationale>` only.
4. Active and completed paths/IDs are disjoint.
5. Map and registry agree exactly and in order.
6. Visible migration navigation agrees with machine state.
7. Latest completed and closeout identity bind exactly.
8. Closeout marker keys are unique.
9. Residual risks and follow-up sections are mandatory and non-empty.
10. Mutable external-state assertions are rejected throughout the complete closeout
    document.
11. Parsed YAML frontmatter rejects direct and nested PR/pull-request/merge state
    keys with mutable values after key normalization.
12. Bold Markdown identifier/state forms and Markdown table rows are rejected.
13. Release-state evidence is assurance-only and cannot authorize external actions.

## Scope Boundary

WB-008 did not deliver live runtime smoke, production telemetry, automatic
hosting-platform self-commits, release tags, in-place upgrades, model routing, or
changes to runtime/integration authority.

## Evidence

- Governance: `governance/release-state.md`
- Validator: `scripts/validate-release-state.py`
- Fixtures: `scripts/test-release-state-contracts.py`
- Dedicated CI: `.github/workflows/release-state-contract.yml`
- Final review: `docs/reports/reviews/pr-8-final-review.md`
- Drift audit: `docs/reports/drift/wb-008-post-merge-ssot-release-gate.md`
- Closeout: `docs/reports/closeout/wb-008-post-merge-ssot-release-gate.md`
- Reviewed implementation revision: `42b31c75f463a6a1ec77dd07b545d1be21175078`
- Release State Contract run 68: success
- Framework Contracts run 517: success

## Acceptance Result

- [x] Historical migration Work Blocks use canonical completed state.
- [x] Repository and hosting-platform lifecycle are separated.
- [x] Work Block, map, registry, and closeout are consistent.
- [x] Exact terminal-value semantics are enforced.
- [x] Evaluation rationale is restricted to documented skips.
- [x] Prose and whole-document mutable-state bypasses are closed.
- [x] Structured direct and nested frontmatter keys are rejected.
- [x] Bold Markdown and table state forms have regressions.
- [x] Required closeout sections are enforced.
- [x] Dedicated and full-framework CI pass.
- [x] Review, verification, drift, and closeout are synchronized.
- [x] No active implementation Work Block remains.

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
