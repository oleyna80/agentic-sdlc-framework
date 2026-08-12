---
schema_version: 1
artifact_type: critic_review
artifact_id: wb-core-004-critic
work_block_id: WB-CORE-004
reviewed_subject: GitHub-native authority model implementation
subject_revision: 8b1300fcf1cae4b63141335818514084ce91030b
verdict: APPROVE
isolation: same_session_connector_review
recorded_by_role: orchestrator
---

# Critic Review — WB-CORE-004

## Scope

This record summarizes the Critic function applied during implementation of the
GitHub-native authority model. It is not represented as an independent subagent
or separate-runtime review. The pass used repository/PR state and contract-test
evidence available through the GitHub connector.

The Critic challenged the migration on the following questions:

- whether removing per-Work-Block SSH signatures accidentally removed engineering scope control;
- whether the new external capability boundary still blocks consequential Git and infrastructure operations;
- whether the lifecycle could claim successful closeout before assurance was resolved;
- whether Codex, Claude Code, and OpenCode retained equivalent Coder/write-set semantics;
- whether generated-project documentation accurately describes the new trust model.

## Findings and corrections

### C-01 — Premature success-closeout was possible

**Original severity: HIGH — RESOLVED.**

The schema-v3 Codex lifecycle helper could set `success-closeout` while required
Review/Verification state remained `PENDING`. This contradicted the lifecycle
contract even though the separate Claude Stop assurance hook would later reject
such state in its own runtime.

Correction: `lifecycle.py close` now validates all assurance functions before
recording closeout. Required Review and Verification must be `READY/READY`;
required Evaluation must be `READY/READY`; required Drift must be
`READY/ALIGNED`. Reporting-only closeout also refuses unresolved `PENDING`
assurance. Regression fixtures cover premature success and reporting-only close.

### C-02 — Broad and tag push forms escaped the obvious push guard

**Original severity: HIGH — RESOLVED.**

The first schema-v3 push guard covered direct default-branch refspecs, force push,
and branch deletion, but did not explicitly classify `--all`, `--mirror`,
`--prune`, `--tags`, `--follow-tags`, or explicit tag refspec publication.

Correction: the shared provider-neutral Hard Stop guard now rejects broad/
destructive remote push forms and external tag publication. Fixtures cover
branch deletion, broad/mirror/prune pushes, and the supported tag publication
forms. Normal feature-branch push remains available by design.

### C-03 — Claude Code Bash mutations bypassed Work Block write-set enforcement

**Original severity: HIGH — RESOLVED.**

Claude Code's Work Block scope hook initially intercepted only
`Edit|MultiEdit|Write`. A Coder with Bash could therefore mutate a source path
with shell redirection or file commands without passing the write-set guard; the
shared Hard Stop hook only classified consequential commands and was not a
general source-scope validator.

Correction: Claude Code now routes `Bash|Edit|MultiEdit|Write` through
`work_block_gate.py`. The hook scopes explicit Bash mutation targets, rejects
complex unscopable mutation, validates staged paths before local commits, and
retains the shared Hard Stop guard as the separate consequential-command layer.
Cross-runtime conformance tests assert this wiring.

### C-04 — Claude adapter documentation lagged the schema-v3 authority model

**Original severity: MEDIUM — RESOLVED.**

The Claude runtime README still described the older approval-oriented language
and did not document Bash write-set routing or the external GitHub/OS/credential
boundary.

Correction: the runtime adapter now explicitly documents
`authority_mode: github_capability`, retired SSH signing, the two Bash guard
layers, normal feature-branch Git operations, and external Hard Stops.

## Residual limitations

Project-local hooks remain cooperative and can be altered by the same local
principal. That is intentional in this model: they are engineering guardrails,
not the primary security boundary. Exact production/default-branch authority
must continue to be enforced by GitHub rulesets, least-privilege credentials,
Actions permissions, OS isolation, and separately held production secrets.

An implicit feature-branch `git push` can also be influenced by unusual local Git
configuration. The guard blocks the explicit dangerous forms covered by the
contract; the external GitHub ruleset remains the authoritative protection for
`main`. Treat this as a documented defense-in-depth limitation, not as locally
cryptographic security.

## Verdict

**APPROVE.** After the corrections above, this Critic pass found no remaining
BLOCKER or HIGH issue in the reviewed implementation subject. Final acceptance
still depends on Reviewer/Verifier evidence and the required GitHub checks for
the final PR head.
