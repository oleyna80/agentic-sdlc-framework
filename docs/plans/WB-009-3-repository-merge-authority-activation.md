---
schema_version: 1
artifact_type: work_block
artifact_id: wb-009-3-repository-merge-authority-activation
work_block_id: wb-009.3
parent_work_block_id: wb-009
status: success
governance_profile: assured
owner_role: orchestrator
created_at: 2026-07-28
write_gate: closed
side_effect_class: external_repository_policy
---

# WB-009.3 — Repository merge authority activation

## Objective

Make GitHub repository policy, rather than provider snapshots or framework
artifacts, the live merge authority for `refs/heads/main`. Preserve a minimal,
redacted pre-state and post-state record plus provider-native enforcement
evidence.

At the time this Work Block executed, parent `WB-009`, `WB-009.1`, and
`WB-009.2` were outside its write-set and were not resumed. That historical
boundary is retained; subsequent WB-009 closeout is documented separately.

## Approved policy

Create one active repository branch ruleset targeting only `refs/heads/main`:

- pull requests are required before merge; required human approvals: zero;
- required status checks are exactly `contracts` and `release-state`, each strict
  (the branch must be up to date before merge);
- conversation resolution is required;
- force pushes and deletion of `main` are blocked;
- no standing bypass actor exists.

Do not add `provider-snapshot`, `final-aggregator`, merge queue, deployment
gates, signed commits, or any other check/rule. GitHub rulesets/required checks
are the sole live merge authority.

## Exact write-set

```text
docs/plans/WB-009-3-repository-merge-authority-activation.md
docs/reports/verification/wb-009-3-repository-merge-authority-activation.md
docs/reports/reviews/wb-009-3-repository-merge-authority-activation.md
```

The only non-file mutation was one GitHub repository ruleset created or updated
through the provider API for the repository under test. The original evidence
worktree and branch were separate from PR #9. Owner approval on 2026-07-29
authorized this later docs-only integration into `main` through a dedicated PR.

## Explicit exclusions

- all code, workflows, routers, templates, validators, and framework contracts;
- PR #9 implementation files and commits;
- release-state workflow implementation and all other repository policy;
- merge queue, deployments, signed commits, branch protection rules, test changes,
  direct changes to `main`, and bypass actors;
- reopening or altering the completed parent WB-009 lifecycle.

## Assured lifecycle, acceptance, and stop conditions

1. Record provider pre-state before mutation.
2. Independent policy review validates the exact API representation and test plan.
3. Create the policy once, then API-read it back and record its ID, active
   enforcement, target, required checks, bypass actors, and enabled rules.
4. Independently verify on PR #9 that an intentionally rerun required check
   makes merge unavailable while pending and available only after success. Do not
   merge from this Work Block. Confirm direct-push protection using provider
   rule-suite/ruleset evidence, not a test write to `main`.
5. Run independent Review, Verification, trajectory evaluation, and drift check
   against this fixed rubric: no extra policy; exact target/checks; no bypass;
   pending blocks; success unblocks; direct push is protected.

Mark this Work Block `BLOCKED` without further mutation if the API readback
differs from the approved policy, a bypass exists, the rule does not apply to
`main`, or GitHub permits merge during a pending/failed required rerun. A policy
change outside this exact approved model requires new Owner approval.

## Historical interim verification outcome

Ruleset `19916164` was created and independently read back as an exact match for
the approved policy. The authorized rerun bound `contracts` to the required
GitHub Actions integration and completed successfully. However, the required
acceptance proof that PR #9 becomes unblocked only after success could not yet be
made: one pre-existing unresolved review conversation correctly kept the PR
blocked under the required-conversation-resolution rule. PR metadata was
excluded, so the initial Assured verification recorded `BLOCKED`.

## Durable closeout update

After Owner-approved resolution of the only review conversation, an
independent, read-only live-provider re-verification at
`2026-07-28T18:41:04Z` returned `READY` for subject SHA
`f6650acfa357411485d0f205532ca69f235d700e` and ruleset `19916164`.
Both and only required checks, `contracts` and `release-state`, were
successful; unresolved review threads were `0`; and GitHub reported REST
`mergeable: true` and GraphQL `mergeable: MERGEABLE`.

The GraphQL `mergeStateStatus: UNSTABLE` observation was a residual,
non-authoritative state caused solely by historical
`final-aggregator=failed`. `final-aggregator` was non-required and was not a
ruleset gate, so it did not affect merge eligibility or the approved policy.

The earlier verifier verdict remains a historical `BLOCKED` interim result;
the later re-verification is `READY`. WB-009.3 is `SUCCESS`. This evidence is a
time-bounded provider read and does not claim that future reruns cannot change
provider state.

## Integration note

Commit `6781f9ee470bc35b2b88478e5f23ed9609fc836b` was preserved through a
new docs-only branch based on the post-PR-#9 `main`. Repository-specific URL
markers were normalized for publication hygiene. The subsequent canonical
WB-009 closeout records WB-009 and WB-009.2 as completed; WB-009.1 remains a
historical `CHANGES_REQUIRED` result. This integration does not reopen any Work
Block or alter live repository policy.
