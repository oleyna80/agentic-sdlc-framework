---
schema_version: 1
artifact_type: work_block
artifact_id: wb-009-2-provider-evidence-temporal-semantics
work_block_id: wb-009.2
parent_work_block_id: wb-009
status: completed
governance_profile: managed
owner_role: orchestrator
created_at: 2026-07-28
last_verified: 2026-07-28
write_gate: closed
risk: medium
---

# WB-009.2 — Provider evidence temporal semantics

## Objective

Close the two Owner-authorized MEDIUM findings in PR #9:

1. make the provider snapshot record the identity and result of the current
   `Framework Contracts` / `contracts` job, or state `PARTIAL` / `UNVERIFIED`
   honestly; and
2. remove parent-plan semantics that treated the snapshot or historical
   `final-aggregator` as a merge gate or final provider verdict.

## Governing architecture

```text
GitHub ruleset 19916164
+ required checks contracts/release-state
= sole live merge authority

provider snapshot
= time-bounded point-in-time evidence
= authority: none
```

The snapshot cannot block merge, replace or duplicate required checks, promise
that later reruns cannot occur, or publish a final provider verdict.

## Root cause

The original pull-request workflow queried check-runs for a synthetic merge SHA.
That query returned no current job evidence even though the workflow's
`contracts` job had completed. The repair therefore stopped polling the Checks
API and instead bound the snapshot directly to workflow-run identity,
`needs.contracts.result`, the PR head SHA, and the workflow SHA.

## Exact write-set

```text
.github/workflows/framework-contracts.yml
scripts/ci-contract-router.py
scripts/test-ci-contract-router.py
docs/plans/WB-009-2-provider-evidence-temporal-semantics.md
docs/reports/reviews/wb-009-2-provider-evidence-temporal-semantics.md
docs/reports/verification/wb-009-2-provider-evidence-temporal-semantics.md
docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md
```

Owner-authorized administrative closeout reconciliation may additionally update
repository SSOT, canonical closeout evidence, and PR metadata without changing
the implementation semantics.

## Implementation contract

- Preserve fail-closed path routing and required contract jobs.
- Generate the snapshot from current workflow-run identity and
  `needs.contracts.result`.
- Record PR head SHA and workflow SHA separately.
- Emit `PARTIAL` for a bound terminal current-job result and `UNVERIFIED` when
  identity or result is incomplete.
- Set `authority: none`, `temporal_semantics: point_in_time`, current-job-only
  coverage, and explicit limitations.
- Keep `provider-snapshot` non-required and non-blocking.
- Remove `final-aggregator`; no replacement aggregate verdict is permitted.
- Name ruleset-required checks as the only live merge authority.

## Acceptance result

- [x] Targeted/full routing behavior remains unchanged.
- [x] Snapshot fixtures bind current workflow/job identity and terminal result.
- [x] Missing identity or result becomes `UNVERIFIED`.
- [x] The artifact states `authority: none` and no merge-verdict semantics.
- [x] Workflow jobs are `route`, `contracts`, and non-blocking
      `provider-snapshot`; `final-aggregator` is absent.
- [x] Parent WB-009 names only required checks as live merge authority.
- [x] Required `contracts` and `release-state` checks remain unchanged.
- [x] Publication fixtures and evidence use synthetic identifiers.

## Correction accounting

The initial lifecycle correction restored a valid active parent status. The
Owner subsequently authorized narrowly scoped administrative corrections to
replace a repository-specific test fixture and the corresponding historical
report reference. Those corrections changed no architecture, required check,
product surface, dependency, or runtime behavior.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic contract validation and provider checks are sufficient
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

The implementation subject at revision
`49b9f137c8e6f994bf169e56301ee4934c7f4537` passed Framework Contracts run 675
and Release State Contract run 242. Provider snapshot artifact
`provider-contracts-snapshot-30393457599-1` recorded current `contracts` result
`success` as `PARTIAL`, with `authority: none` and exact point-in-time identity.
External integration or merge remains a separate Owner-controlled action.