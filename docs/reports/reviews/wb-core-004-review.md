---
schema_version: 1
artifact_type: review
artifact_id: wb-core-004-review
work_block_id: WB-CORE-004
reviewed_stage: assure
reviewed_subject: schema-v3 GitHub capability authority implementation
subject_revision: 8b1300fcf1cae4b63141335818514084ce91030b
verdict: READY
isolation: same_session_connector_review
recorded_by_role: orchestrator
---

# Final Review — WB-CORE-004

## Review boundary

This is a logical Reviewer pass over the implementation subject through
`8b1300fcf1cae4b63141335818514084ce91030b`; evidence-only report commits are not
part of that implementation subject. The review used PR/file state and CI
results obtained through the GitHub connector. It is deliberately labeled
`same_session_connector_review` and is not claimed as independent runtime or
human review.

## Result

**Verdict: READY. No remaining BLOCKER or HIGH finding was identified.**

The reviewed implementation consistently separates process guardrails from the
real capability boundary:

- active Work Block schema v3 uses `authority_mode=github_capability` and no
  longer binds normal source work to SSH-signed authorization records;
- Work Block scope, Critic state, write-set checks, staged-commit validation,
  Review/Verification/Evaluation/Drift closeout requirements, and integration
  admission remain in place;
- normal local commits and feature-branch pushes are no longer Owner
  cryptographic Hard Stops;
- direct protected/default-branch pushes, force/history-rewriting pushes,
  destructive/broad remote pushes, tag publication, live infrastructure/data,
  credential operations, destructive filesystem/Git operations, and configured
  client-facing communications remain rejected in the normal agent channel;
- Claude Code Bash mutations now pass both the shared Hard Stop guard and the
  Work Block/write-set scope guard, removing the prior cross-runtime parity gap;
- OpenCode Coder permissions permit local commit and prompt on push while
  read-only logical roles retain commit/push denial;
- Codex source mutations and staged commits remain scoped to the active Work
  Block, including `apply_patch` move destinations and fail-closed handling for
  unscopable Bash mutation;
- lifecycle success-closeout cannot be recorded with unresolved required
  assurance.

## Security-model assessment

The removal of SSH signing is coherent with the declared threat model. The
repository explicitly treats local hooks as cooperative defense in depth and
moves consequential authority to externally controlled GitHub/OS/credential
capabilities. This avoids presenting a same-principal mutable hook as a stronger
security boundary than it is.

For the framework repository, the design depends on the active GitHub ruleset
for the protected default branch and on not provisioning production credentials
or workflow-dispatch authority to an ordinary agent credential in consumer
projects. That dependency is intentional and documented.

## Residual risks / inspection limits

1. Local hooks cannot prevent a malicious same-OS-principal process from
   bypassing or editing them. This is an explicit property of the new model, not
   a hidden guarantee.
2. The explicit Git push guard is defense in depth rather than a complete parser
   for every possible Git configuration/refspec behavior. The external protected-
   branch ruleset remains authoritative.
3. This review did not perform a live target-environment Claude/OpenCode native
   smoke. CI validates the generated contracts and disposable fixtures; actual
   runtime version/configuration still requires environment-specific evidence
   when a consumer project relies on it for stronger assurance.
4. This Reviewer pass is same-session and therefore does not satisfy any future
   governance profile that explicitly requires independent human/runtime review.

None of these residual limitations contradicts the WB-CORE-004 objective or its
acceptance criteria for the framework change.

## Reviewer verdict

**READY.** The implementation is internally coherent and suitable to proceed to
final Verifier checks. Any source/control-plane change after the reviewed subject
revision requires the relevant assurance to be reconsidered.
