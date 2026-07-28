---
schema_version: 1
artifact_type: work_block
artifact_id: wb-009-2-provider-evidence-temporal-semantics
work_block_id: wb-009.2
parent_work_block_id: wb-009
status: in_progress
governance_profile: managed
owner_role: orchestrator
created_at: 2026-07-28
write_gate: open
risk: medium
---

# WB-009.2 — Provider evidence temporal semantics

## Objective

Close only the two Owner-authorized MEDIUM findings in PR #9:

1. make the provider snapshot record the identity and result of the current
   `Framework Contracts` / `contracts` job, or state `PARTIAL` / `UNVERIFIED`
   honestly; and
2. remove all parent-plan semantics that treat the snapshot or
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

The snapshot must not block merge, replace or duplicate required checks, promise
that later reruns cannot occur, or publish a final provider verdict.

## Root cause

For `pull_request` workflows, `github.sha` is the synthetic merge revision. Run
`30377306228` therefore queried check-runs for merge SHA
`a5a905ec449372334b9adf567e65468cfac0bf33`; the uploaded artifact contained
`total_count: 0` and no check runs. The actual PR head was
`f6650acfa357411485d0f205532ca69f235d700e`, while the current workflow's
`contracts` job itself completed successfully.

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

No WB-009.1 evidence, release-state implementation, product surface, dependency,
repository ruleset, PR metadata, or WB-009.3 branch content may change.

## Implementation contract

- Preserve the existing fail-closed path router and all required contract jobs.
- Replace check-runs polling with a deterministic snapshot generated from the
  current workflow-run identity and `needs.contracts.result`.
- Record both the PR head SHA and workflow SHA so synthetic merge semantics are
  explicit rather than conflated.
- Emit `PARTIAL` when the current terminal job result and identity are bound;
  emit `UNVERIFIED` when identity or result is incomplete.
- Set `authority: none`, `temporal_semantics: point_in_time`, and explicit
  limitations in the artifact.
- Keep `provider-snapshot` non-required and non-blocking.
- Remove `final-aggregator`; no replacement aggregate verdict is permitted.
- Update the parent WB-009 plan to name ruleset-required checks as the only live
  merge authority.

## Lifecycle limits

One implementation pass, one independent read-only Review, one Verification,
and at most one correction round are permitted. A HIGH/P1 finding, write-set
escape, required-check regression, or second correction stops as
`CHANGES_REQUIRED` for Owner decision.

## Acceptance criteria

1. Router fixtures prove targeted/full routing remains unchanged.
2. Snapshot fixtures prove exact workflow/job identity and terminal result are
   captured as `PARTIAL`.
3. Missing identity or non-terminal/absent result is `UNVERIFIED`.
4. The artifact explicitly states `authority: none`, point-in-time semantics,
   current-job-only coverage, and no merge verdict.
5. Workflow YAML has jobs `route`, `contracts`, and non-blocking
   `provider-snapshot`; `final-aggregator` is absent.
6. Parent WB-009 no longer describes snapshot or aggregation as a merge gate.
7. Required `contracts` and `release-state` ruleset checks remain unchanged.
8. PR #9 is not merged.

## Verification commands

```text
python scripts/test-ci-contract-router.py
python -m py_compile scripts/ci-contract-router.py scripts/test-ci-contract-router.py
python -c "import yaml; yaml.safe_load(open('.github/workflows/framework-contracts.yml'))"
```

The repository-level contract suite and live required checks must then pass on
the resulting PR head. The uploaded provider snapshot is inspected as evidence,
not as an authority or gate.
