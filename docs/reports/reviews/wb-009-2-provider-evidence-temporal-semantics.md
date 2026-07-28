# Independent Review — WB-009.2 provider evidence temporal semantics

## Scope and subject

Read-only review was performed after freezing the implementation manifest at
SHA-256 `bcbe59b2494527de40f17974991308a64527256d80f0039e288a26b8ef96ec0d`.
The reviewed subject contains only:

```text
.github/workflows/framework-contracts.yml
scripts/ci-contract-router.py
scripts/test-ci-contract-router.py
docs/plans/WB-009-2-provider-evidence-temporal-semantics.md
docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md
```

No file was edited during this review pass.

## Review questions

1. Does the repair remain inside the Owner-approved WB-009.2 write-set?
2. Does it preserve `contracts` and `release-state` as the only live ruleset
   checks and avoid any replacement merge verdict?
3. Does the snapshot identify the current `contracts` job and result without
   conflating the PR head with the pull-request synthetic merge SHA?
4. Does incomplete evidence become `UNVERIFIED` rather than a false pass?
5. Does the workflow remain non-blocking outside the required `contracts` job?
6. Does the parent plan accurately describe temporal and authority semantics?

## Findings

### HIGH / P1

None.

### MEDIUM / P2

None.

### LOW / P3

None requiring correction.

## Observations

- The workflow preserves the required `contracts` job unchanged and removes only
  the non-required aggregate verdict path.
- `provider-snapshot` records `needs.contracts.result`, workflow name/ref, run ID
  and attempt, job key/name, repository, PR head SHA, and workflow SHA. Within a
  workflow run, the tuple of run ID, attempt, and job key identifies the current
  job deterministically.
- The artifact is deliberately `PARTIAL` even for a successful terminal result,
  because it covers only the current workflow job and is not complete merge
  authority. Missing identity or result becomes `UNVERIFIED`.
- `authority: none`, point-in-time semantics, current-job-only coverage, and the
  lack of any merge verdict are mechanically present in the generated JSON.
- Job-level `continue-on-error: true` and a non-required check context prevent
  snapshot capture from becoming a live merge gate.
- Removing `checks: read` is consistent with eliminating Checks API polling and
  reduces workflow token permissions.
- The parent plan now names ruleset `19916164` plus required checks `contracts`
  and `release-state` as the sole live merge authority. Historical
  `final-aggregator` state is explicitly non-required and non-authoritative.

## Verdict

**APPROVED** for Verification. The implementation closes the two authorized
MEDIUM findings without widening scope, changing required checks, rewriting
WB-009.1 evidence, mixing WB-009.3, or authorizing merge of PR #9.
