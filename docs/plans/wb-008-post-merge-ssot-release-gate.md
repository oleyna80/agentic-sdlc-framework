---
schema_version: 1
artifact_type: work_block
artifact_id: wb-008-post-merge-ssot-release-gate
status: in_progress
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

## Problem Statement

After PR #7 was merged, the framework implementation and closeout evidence were
complete, but several repository SSOT consumers still represented WB-007 as active
or pending. The defect exists because internal Work Block lifecycle and mutable
GitHub pull-request lifecycle were mixed in the same documentation without an
executable consistency contract.

## Target Invariants

1. A completed Work Block has frontmatter `status: completed` and no pending
   lifecycle verdicts in its current-state section.
2. Every path in `FILE_REGISTRY.yml:migration_state.completed_work_blocks` exists
   and has completed Work Block frontmatter.
3. `migration_state.active_work_block`, when non-null, exists, is not listed as
   completed, and has an active status.
4. `PROJECT_MAP.md` completed/active migration statements agree with
   `FILE_REGISTRY.yml`.
5. A successful closeout report describes repository closeout state only. Mutable
   GitHub PR state is external operational metadata and cannot be a normative
   release invariant stored in a pre-merge commit.
6. A repository with no active Work Block must not claim an active migration in
   maps, registries, or Work Block state.
7. Release readiness fails closed when required Work Block, closeout, map, or
   registry evidence is missing or contradictory.

## Scope

### In Scope

- reconcile WB-007 Work Block, map, registry, and closeout wording;
- define the repository-vs-GitHub lifecycle boundary;
- add `scripts/validate-release-state.py`;
- add positive and adversarial fixtures;
- add a dedicated GitHub Actions release-state workflow;
- register and document the release-state contract;
- complete review, verification, drift, and closeout for WB-008;
- keep merge under explicit Owner approval.

### Out of Scope

- live Codex/Claude Code/OpenCode smoke tests;
- production telemetry or a hosted run ledger;
- automatic GitHub self-commits after merge;
- release tagging or publishing v1.0;
- in-place project upgrades;
- changing runtime authority or evaluation semantics.

## Implementation Plan

1. Reconcile WB-007 lifecycle evidence already present in `main`.
2. Define release-state ownership and prohibit mutable PR status as normative SSOT.
3. Implement the release-state validator.
4. Add adversarial fixtures for stale active paths, completed/active overlap,
   missing Work Blocks, incomplete frontmatter, map drift, and mutable PR claims.
5. Add a dedicated CI workflow running the validator and fixtures on push/PR.
6. Synchronize map, registry, README, and Work Block lifecycle.
7. Perform final review, verification, drift audit, and success closeout.
8. Mark the PR Ready for review without merging.

## Acceptance Criteria

- [ ] WB-007 is represented as completed in all repository lifecycle consumers.
- [ ] No repository SSOT states that merged PR #7 is still Draft or unmerged.
- [ ] Mutable GitHub PR state is explicitly non-normative.
- [ ] Release-state validator passes on the repository.
- [ ] Adversarial fixtures fail for every listed drift class.
- [ ] CI runs the release-state gate on push and pull request events.
- [ ] Existing Framework Contracts remain green.
- [ ] Final review, verification, drift, and closeout evidence are synchronized.
- [ ] PR remains unmerged until explicit Owner approval.

## Current State

- **Stage:** Define
- **Stage State:** in_progress
- **Write Gate:** limited to WB-008 branch and documented scope
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation:** optional; deterministic release-state contract is primary
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
