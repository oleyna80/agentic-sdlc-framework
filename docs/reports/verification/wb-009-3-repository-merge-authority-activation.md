# Verifier Report

**Tier:** full (Assured fixed rubric)  
**Work Block:** WB-009.3 repository merge-authority activation  
**Final verdict:** READY  
**Historical interim verdict:** BLOCKED

## Scope and method

Independent, read-only verification covered the live GitHub repository policy,
PR #9, and the authorized required-check rerun. No direct push to `main`, PR
merge, policy expansion, code change, workflow change, or bypass mutation was
performed by this verifier.

Initial provider reads were made on 2026-07-28 between `18:15:51Z` and
`18:18:07Z`. A later Owner-authorized read-only re-verification was made at
`2026-07-28T18:41:04Z`. Provider responses used API version `2022-11-28`; no
credential value is recorded.

## Changed file

- `docs/reports/verification/wb-009-3-repository-merge-authority-activation.md`
  — independent policy verification and durable closeout evidence.

## Policy checks

### Exact active ruleset — PASS

A provider read of `/repos/{repository}/rulesets/19916164` returned HTTP `200`
with this effective shape:

```json
{
  "id": 19916164,
  "name": "WB-009.3 main merge authority",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": []
    }
  },
  "bypass_actors": [],
  "current_user_can_bypass": "never"
}
```

The rule list was exactly:

```text
deletion
non_fast_forward
pull_request
required_status_checks
```

The pull-request rule required zero approving reviews and required review-thread
resolution. Required status checks were exactly:

```json
{
  "strict_required_status_checks_policy": true,
  "required_status_checks": [
    {"context": "contracts", "integration_id": 15368},
    {"context": "release-state", "integration_id": 15368}
  ]
}
```

No standing bypass actor was present.

### Effective `main` protection — PASS

A provider read of `/repos/{repository}/rules/branches/main` returned all four
effective rules from ruleset `19916164`, including pull-request enforcement,
deletion prevention, and non-fast-forward prevention. This is provider-native,
read-only evidence for protected `main`; no risky direct-write test was needed.

### No additional policy — PASS

The repository ruleset list returned exactly one active repository ruleset:
`19916164`. The legacy branch-protection endpoint returned HTTP `404`, so no
legacy branch-protection rule, merge queue, deployment gate, signed-commit rule,
or other hidden policy supplemented the approved ruleset.

### Strictness applicability — PASS

The tested PR head was ahead of, and not behind, its recorded `main` base. Strict
required-status-check enforcement therefore applied without an unrelated stale
base condition.

## Required-check trajectory

### Authorized rerun identity — PASS

Workflow run `30377306228`, attempt `2`, was bound to PR #9 and subject SHA
`f6650acfa357411485d0f205532ca69f235d700e`. The final `contracts` check was:

```json
{
  "id": 90366960968,
  "name": "contracts",
  "status": "completed",
  "conclusion": "success",
  "started_at": "2026-07-28T18:14:04Z",
  "completed_at": "2026-07-28T18:14:20Z",
  "app_id": 15368,
  "check_suite_id": 82332828002
}
```

This bound the successful required context to the same GitHub Actions
integration required by ruleset `19916164`.

### Historical interim endpoint — BLOCKED

The initial verification could not honestly prove the complete
pending-to-unblocked trajectory. By the first live provider read, the
`contracts` check had already completed successfully. In addition, GitHub still
reported one unresolved review conversation, and the ruleset correctly required
conversation resolution.

At that time:

- both required checks were successful;
- the PR head was not stale;
- one unresolved review thread remained;
- GraphQL reported merge state `BLOCKED`;
- REST reported the PR as mergeable but blocked by policy.

The verifier did not resolve the thread because WB-009.3 excluded PR mutation.
The initial fixed-rubric verdict was therefore correctly recorded as `BLOCKED`.

## Re-verification closeout

After Owner-approved resolution of the sole review conversation, a fresh
read-only provider verification at `2026-07-28T18:41:04Z` returned:

- [PASS] required `contracts`: success;
- [PASS] required `release-state`: success;
- [PASS] unresolved review threads: `0`;
- [PASS] REST merge eligibility: `mergeable: true`;
- [PASS] GraphQL merge eligibility: `mergeable: MERGEABLE`;
- [PASS] ruleset `19916164` unchanged and still the sole live merge authority.

GraphQL also observed `mergeStateStatus: UNSTABLE`, explained solely by the
historical non-required `final-aggregator=failed` status. `final-aggregator` was
not a ruleset requirement and had no merge authority.

The historical `BLOCKED` result remains factual for the earlier observation.
The later re-verification satisfies the closeout endpoint and supersedes it with
final verdict `READY`. WB-009.3 is `SUCCESS`.

## Drift and boundary verification

- [PASS] exact target: `refs/heads/main`;
- [PASS] exact required checks: `contracts`, `release-state`;
- [PASS] strict required-check policy;
- [PASS] zero required approvals;
- [PASS] required conversation resolution;
- [PASS] deletion and non-fast-forward prevention;
- [PASS] no bypass actors;
- [PASS] no snapshot, aggregate, queue, deployment, signature, or extra gate;
- [PASS] no code, workflow, validator, template, or runtime mutation;
- [PASS] no direct push to `main` used as a test.

## Residual limitations

- Provider evidence is time-bounded and does not guarantee future provider
  state or future rerun results.
- A dynamic direct-push rejection was intentionally not attempted; effective
  provider rules are the safer read-only evidence.
- The initial pending state was not captured before the fast `contracts` job
  completed. The later successful-unblock endpoint was verified after the
  unrelated conversation blocker was removed.

## Integration note

This report originated in commit
`6781f9ee470bc35b2b88478e5f23ed9609fc836b`. Owner approval on 2026-07-29
authorized its integration through a fresh docs-only branch based on current
`main`. Repository-specific URL markers were normalized to satisfy publication
hygiene. The canonical WB-009 closeout subsequently completed WB-009 and
WB-009.2; WB-009.1 remains historical `CHANGES_REQUIRED`. This evidence import
does not reopen any Work Block or modify live repository policy.
