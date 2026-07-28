# Independent Review — WB-009.2 provider evidence temporal semantics

## Scope and subject

The independent read-only review covered the provider-snapshot implementation,
workflow routing, parent authority semantics, and the final administrative
publication corrections. The implementation subject was frozen before review;
the later corrections only replaced repository-specific prose/test data and did
not change executable semantics.

Reviewed paths:

```text
.github/workflows/framework-contracts.yml
scripts/ci-contract-router.py
scripts/test-ci-contract-router.py
docs/plans/WB-009-2-provider-evidence-temporal-semantics.md
docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md
```

## Review questions

1. Does the repair preserve `contracts` and `release-state` as the only live
   ruleset checks?
2. Does it avoid any replacement merge verdict?
3. Does the snapshot identify the current `contracts` job and result without
   conflating the PR head with the synthetic workflow SHA?
4. Does incomplete evidence become `UNVERIFIED` rather than a false pass?
5. Does snapshot capture remain non-required and non-blocking?
6. Do the parent plan and closeout describe temporal and authority semantics
   consistently?
7. Are publication-facing fixtures and evidence project-neutral?

## Findings

### HIGH / P1

None.

### MEDIUM / P2

None.

### LOW / P3

None requiring correction.

## Observations

- The required `contracts` job remains the validation authority supplied to the
  repository ruleset.
- `provider-snapshot` records `needs.contracts.result`, workflow name/ref, run ID
  and attempt, job key/name, repository, PR head SHA, and workflow SHA.
- A successful or failed terminal current-job result is deliberately `PARTIAL`,
  because the artifact covers only that job and is not complete merge authority.
- Missing identity or result becomes `UNVERIFIED`.
- `authority: none`, point-in-time semantics, current-job-only coverage, and the
  absence of a merge verdict are mechanically present in generated JSON.
- Job-level `continue-on-error: true` and a non-required check context prevent
  snapshot capture from becoming a live merge gate.
- Checks API polling, `checks: read`, and `final-aggregator` were removed.
- The parent plan names ruleset `19916164` plus required checks `contracts` and
  `release-state` as the sole live merge authority.
- Final administrative corrections anonymized the fixture and historical report
  reference without modifying implementation behavior.

## Provider evidence reviewed

Framework Contracts run 675 and Release State Contract run 242 completed
successfully for implementation revision
`49b9f137c8e6f994bf169e56301ee4934c7f4537`. The associated snapshot artifact
recorded current job result `success` as `PARTIAL`, with `authority: none`.

## Verdict

**APPROVED / READY.** The implementation closes the authorized MEDIUM findings,
preserves required-check authority, remains project-neutral, and introduces no
replacement merge gate. External integration or merge is not authorized by this
review.