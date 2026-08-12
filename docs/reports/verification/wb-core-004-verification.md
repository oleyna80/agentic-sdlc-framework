---
schema_version: 1
artifact_type: verification
artifact_id: wb-core-004-verification
work_block_id: WB-CORE-004
verified_subject_revision: 8b1300fcf1cae4b63141335818514084ce91030b
evidence_head_revision: c7400ca569b58f94ba68a64fb8ba341e975092e8
verdict: READY
isolation: same_session_connector_verification
recorded_by_role: orchestrator
---

# Verification — WB-CORE-004

## Verification boundary

This Verifier pass checks the WB-CORE-004 implementation subject through
`8b1300fcf1cae4b63141335818514084ce91030b`. The evidence head
`c7400ca569b58f94ba68a64fb8ba341e975092e8` adds only Critic/Reviewer reports on
top of that implementation subject.

The pass uses GitHub-hosted CI and repository/ruleset state obtained through the
GitHub connector. It is labeled `same_session_connector_verification`; it is not
represented as an independent human, subagent, or separate-runtime verification.

## Required GitHub checks

Both required PR workflows completed successfully on evidence head
`c7400ca569b58f94ba68a64fb8ba341e975092e8`:

- **Framework Contracts** — run `31624961564`, success. The `contracts` job
  passed syntax/config parsing, runtime-neutral SDLC contracts, evaluation/NDR
  contracts, installation profiles and runtime conformance, integration
  adapters, Codex adapter gates, governance structure, release-state validation,
  publication validation, and disposable generated-project bootstrap.
- **Release State Contract** — run `31624961808`, success.

These runs include the regressions added during WB-CORE-004 for schema-v3
control-plane behavior, lifecycle closeout, hard-stop push handling, and Claude
Bash write-scope wiring.

## Acceptance-criteria verification

1. **No SSH signer required for normal source work — PASS.** Schema v3 uses
   `authority_mode=github_capability`; normal lifecycle/open logic no longer
   requires an Owner key, `ssh-keygen`, `allowed_signers`, or detached `.sig`.
2. **Normal local commit / feature push not cryptographic Hard Stops — PASS.**
   Coder paths permit local commit and normal feature-branch push subject to
   runtime/write-set controls.
3. **Consequential Git/external operations remain blocked locally — PASS.**
   Fixtures cover direct default-branch push, force/history-rewriting push,
   branch deletion, broad/mirror/prune push, tag publication, destructive
   filesystem/Git commands, live infrastructure/data, credentials, and client
   communication patterns.
4. **Work Block write-set remains active — PASS.** Codex and Claude source
   mutation paths enforce schema-v3 READY state and exact write-set; staged
   commits are path-validated.
5. **`apply_patch` move destination checked — PASS.** Codex regression fixtures
   cover source and destination scope.
6. **Unscopable mutating Bash fails closed — PASS.** Codex and Claude guards
   reject complex mutation whose targets cannot be safely established.
7. **Security-boundary documentation — PASS.** Governance/runtime documentation
   explicitly distinguishes cooperative local guardrails from GitHub/OS/
   credential capability boundaries.
8. **Framework GitHub ruleset preserved — PASS.** Ruleset `19916164`,
   `WB-009.3 main merge authority`, remains active for `refs/heads/main` with
   pull-request enforcement, required `contracts` and `release-state` checks,
   deletion and non-fast-forward protection, and no bypass actor.
9. **Required checks pass — PASS** for the evidence head named above.
10. **Critic/Reviewer blocking findings — PASS.** The recorded Critic findings
    were corrected; the final Reviewer verdict is READY with no remaining
    BLOCKER/HIGH issue.

## Residual verification limits

- CI proves the committed generated-project contracts and disposable fixtures;
  it does not prove every future local Claude/OpenCode/Codex version or user-level
  configuration.
- Project hooks remain cooperative by design. The security property for default
  branch and production authority depends on the external GitHub/OS/credential
  boundary.
- Evidence-only commits made after this report must still receive the required
  GitHub checks on the exact PR head before merge. This report does not waive
  that repository rule.

## Verdict

**READY.** WB-CORE-004 satisfies its implementation acceptance criteria for the
reviewed subject. Merge remains conditional on the required GitHub status checks
being green on the exact final PR head and on the PR no longer being Draft.
