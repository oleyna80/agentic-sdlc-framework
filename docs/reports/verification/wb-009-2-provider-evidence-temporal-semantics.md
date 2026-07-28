# Verifier Report

**Tier:** focused Managed repair verification  
**Work Block:** WB-009.2 provider evidence temporal semantics  
**Verdict:** CHANGES_REQUIRED

## Subject

The initial frozen implementation manifest had SHA-256
`bcbe59b2494527de40f17974991308a64527256d80f0039e288a26b8ef96ec0d`, based on
PR #9 head `f6650acfa357411485d0f205532ca69f235d700e`. Provider verification and the
single authorized correction round ended at head
`b5ce0072d0b007bba182febc8ed0096ef55041d9`.

## Scope verification

[PASS] All implementation and evidence paths are inside the exact WB-009.2
write-set.  
[PASS] No WB-009.1 evidence, release-state implementation, product surface,
dependency, repository ruleset, PR metadata, or WB-009.3 branch file is changed.  
[PASS] PR #9 merge is not authorized by this Work Block.

## Local checks

[PASS] Original workflow reconstruction matched Git blob
`c2f21afcb3626b1d68ca56f6f9bbb1234447838d`, proving the workflow diff was
applied to the exact PR-head file.  
[PASS] Original router reconstruction matched Git blob
`1b1ae3d462deff521d4deefb846fb9191feceaf9`.  
[PASS] Original router-test reconstruction matched Git blob
`57a172ca4bdd2fadfd1d9df9bb9787162846147d`.

Commands and outcomes:

```text
python scripts/test-ci-contract-router.py
OK: CI route and provider snapshot temporal-semantics fixtures

python -m py_compile scripts/ci-contract-router.py scripts/test-ci-contract-router.py
PASS

PyYAML parse and structural assertions
PASS: jobs are route, contracts, provider-snapshot; snapshot is non-blocking

snapshot CLI with complete terminal contracts identity/result
PASS: evidence_status=PARTIAL, authority=none, point_in_time

snapshot CLI with missing identity/result
PASS: evidence_status=UNVERIFIED

textual authority assertions
PASS: final-aggregator absent; parent plan names sole live ruleset authority
```

## Semantic verification

[PASS] The snapshot records repository, workflow name/ref, run ID, run attempt,
event, job key/name, `needs.contracts.result`, PR head SHA, and workflow SHA.  
[PASS] `PARTIAL` means the current terminal job result is bound but coverage is
only the current workflow job.  
[PASS] Missing identity or result is `UNVERIFIED`; no false `READY` path exists.  
[PASS] `authority: none`, current-job-only coverage, no merge verdict, and
future-rerun limitations are explicit.  
[PASS] `contracts` remains the required validation job. `provider-snapshot` is
non-required and has job-level `continue-on-error: true`.  
[PASS] The aggregate verdict job and Checks API polling are removed; token
permission `checks: read` is no longer requested.  
[PASS] Parent WB-009 no longer assigns gate or final-verdict semantics to the
snapshot or historical `final-aggregator`.

## Provider verification

Run `30392046357` on exact head
`b5ce0072d0b007bba182febc8ed0096ef55041d9` produced:

- [PASS] required `release-state`: success in run `30392044344`;
- [PASS] `provider-snapshot`: success and artifact
  `provider-contracts-snapshot-30392046357-1` uploaded;
- [PASS] artifact identity: PR head `b5ce0072d0b007bba182febc8ed0096ef55041d9`,
  workflow SHA `8d89a716f6a8121a06bd3387e12e8ea9f4ad2152`, run ID
  `30392046357`, attempt `1`, job key/name `contracts`;
- [PASS] artifact semantics: `evidence_status: PARTIAL`, `authority: none`,
  `temporal_semantics: point_in_time`, current-job-only coverage, result
  `failure`, and explicit no-merge-verdict/future-rerun limitations;
- [FAIL] required `contracts`: publication validation found a private-project
  marker in `scripts/test-ci-contract-router.py` because the fixture used the
  previously non-synthetic repository identifier.

## Correction accounting

Correction round 1 was consumed after provider `release-state` rejected the
parent active Work Block's frontmatter `status: changes_required`. The correction
restored the machine lifecycle state to `status: in_progress` and preserved the
separate parent verdict `CHANGES_REQUIRED` in prose. Required `release-state`
then passed.

The publication failure requires changing the test fixture to a synthetic
repository identifier such as `example/framework`. That is a second
implementation correction. WB-009.2 permits at most one correction round, so no
further mutation is authorized in this Work Block.

## Final verdict

**CHANGES_REQUIRED.** The two original MEDIUM findings are implemented and the
new snapshot behaves honestly, including on a failed current job. Nevertheless,
the required `contracts` gate is red and a second correction would exceed the
Owner-approved lifecycle ceiling. Parent WB-009 remains `CHANGES_REQUIRED`.
PR #9 remains open and unmerged; merge is prohibited without separate Owner
direction.
