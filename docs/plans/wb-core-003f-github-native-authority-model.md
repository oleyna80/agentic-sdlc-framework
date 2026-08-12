---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003f-github-native-authority-model
work_block_id: WB-CORE-003F
status: completed
owner_role: orchestrator
created_at: 2026-08-12
last_updated: 2026-08-12
process_level: Standard
governance_profile: Managed
branch: agent/wb-core-003f-authority-closeout
owner_approval: current Owner instruction to finish the authority-model change and reconcile repository lifecycle state
critic_gate: APPROVE
write_gate: BLOCKED
writer: bounded post-merge reconciliation by Orchestrator
base_revision: a25261f650193e2631bcc2d14809265bfeec0023
---

# WB-CORE-003F — GitHub-Native Authority Model

## Identity correction

The implementation entered repository history under the provisional identifier
`WB-CORE-004`. Post-merge SSOT discovery found that the accepted Portable Kit
roadmap already reserves `WB-CORE-004` for installer and packaging work, followed
by `WB-CORE-005` synthetic dry run, `WB-CORE-006` HardwareLab pilot, and
`WB-CORE-007` promotion/legacy archive.

The authority-model change is therefore canonically recorded as **WB-CORE-003F**,
the next unused inserted governance/control-plane follow-up after
WB-CORE-003A—WB-CORE-003E. This preserves the pre-existing product roadmap rather
than silently renumbering future product Work Blocks. Historical hosting-platform
metadata and Git commit messages may retain the provisional identifier; they are
non-normative history and do not override repository SSOT.

## Objective

Replace per-Work-Block SSH-signed authorization as the normal development
security boundary with a simpler capability model based on GitHub repository
rules, least-privilege credentials, protected default-branch flow, CI, OS
isolation, and externally controlled production credentials.

The Agentic SDLC process remains: Work Block → scoped implementation → Critic →
Reviewer → Verifier → closeout. The change relocates consequential security
authority; it does not remove engineering discipline.

## Decision

SSH signatures and authorization-bootstrap commits are retired from the default
development path.

Reasons:

1. The signed local state machine created a circular bootstrap problem: an
   authorization commit was needed before that same authorization could permit
   ordinary Git state changes.
2. Recovery exposed disproportionate H0/H1/H2, replay, expiry, specification-
   digest, detached-signature, and cross-runtime parity complexity around
   reversible development operations.
3. Project-local hooks are cooperative controls writable by the same local
   principal as the agent and are therefore the wrong place for the primary
   security boundary.
4. Protected repository state is better constrained by GitHub rulesets and
   least-privilege credentials outside the mutable project.
5. Production/VPS/database/secret authority is more reliably constrained by
   capability separation than by a project-local signed state machine.

## Authority model

### Normal agent capabilities

Inside an approved Work Block and write-set, normal development may include:

- reading and editing approved paths;
- tests, builds, linters, and disposable local tooling;
- staging approved paths and local commits;
- normal feature-branch pushes when the runtime credential permits them;
- pull-request creation/update and CI/review inspection.

These actions do not require an Owner private signing key, `ssh-keygen`, an
`allowed_signers` file, an authorization-bootstrap commit, or a detached `.sig`.

### External capability boundaries

Consequential operations remain outside the normal agent channel and require an
externally controlled capability where applicable:

- production deployment or live service restart;
- live database/schema/data mutation;
- credential, token, key, or secret operations;
- destructive Git/filesystem/database operations;
- direct protected/default-branch mutation;
- force/history-rewriting pushes, remote branch deletion, broad/mirror/prune
  pushes, and external tag publication;
- irreversible package/image/public release publication;
- real client/user communications or consequential business mutations.

Project-local hooks remain defense-in-depth guardrails only. The primary boundary
is GitHub/OS/workflow/credential capability separation.

## Implemented scope

The completed implementation delivered:

- active Work Block schema v3 with `authority_mode: github_capability`;
- non-cryptographic Codex lifecycle coordination state;
- fail-closed lifecycle closeout until required assurance is resolved;
- Codex source/write-set, staged-commit, `apply_patch` move-destination, and
  unscopable-Bash checks;
- shared provider-neutral Hard Stop handling for consequential Bash and Git push
  forms;
- Claude Code Bash plus Edit/MultiEdit/Write Work Block scope enforcement and
  staged-commit parity;
- OpenCode Coder local-commit/feature-push posture while read-only roles retain
  commit/push denial;
- generated-project profile, evaluation, integration, runtime-conformance, and
  publication fixtures reconciled to schema v3;
- `.agent/authorizations/` retained only for legacy audit/history compatibility;
- governance, runtime, session/bootstrap, handoff, and adapter documentation
  updated to distinguish process guardrails from security boundaries.

## Assurance corrections completed before closeout

Critic/Reviewer work found and corrected four material gaps:

1. lifecycle success-closeout could previously be recorded with unresolved
   assurance;
2. broad/tag publication Git push forms were not all classified by the local
   consequential-operation guard;
3. Claude Code Bash mutation initially bypassed the Work Block write-set guard;
4. Claude Code runtime documentation lagged the schema-v3 authority model.

Regression fixtures and cross-runtime conformance checks cover the corrected
behavior.

## Explicit exclusions

- no production deployment or live infrastructure mutation;
- no secret, token, credential, or key creation/rotation;
- no weakening of repository rulesets;
- no removal of Critic/Reviewer/Verifier or write-set discipline;
- no destructive cleanup of historical signed-authorization artifacts;
- no Portable Kit promotion;
- no renumbering or repurposing of the accepted WB-CORE-004—WB-CORE-007 product
  roadmap.

## Acceptance criteria

1. Generated projects no longer require SSH signing machinery for normal scoped
   source work.
2. Local commit and normal feature-branch push are not cryptographic Hard Stops.
3. Consequential Git, live infrastructure/data, credential, destructive, and
   client-facing operations remain blocked in the normal agent channel where the
   local guard can identify them.
4. Work Block write-set enforcement remains active for source mutation and
   staged commits.
5. Codex `apply_patch` validates both source and `Move to:` destination paths.
6. Complex/unknown mutating Bash fails closed when targets cannot be scoped.
7. Claude Code Bash mutations receive the same Work Block/write-set discipline.
8. Lifecycle success-closeout cannot bypass unresolved required assurance.
9. Documentation identifies GitHub/OS/credential separation as the real
   consequential security boundary.
10. Repository ruleset protection remains unchanged.
11. Required repository contracts pass for the final normative/evidence subject.
12. Critic, Reviewer, Verifier, and Drift assurance contain no unresolved
   blocking finding.

## Assurance evidence

Canonical same-session connector-backed reports for this Work Block are stored
under `docs/reports/reviews/` and `docs/reports/verification/`. They are not
represented as independent human or separate-runtime assurance. Deterministic
GitHub-hosted contract CI is the executable verification boundary for the
repository changes.

## Final State

- **Stage state:** completed
- **Review gate:** READY
- **Verification verdict:** READY
- **Drift gate:** ALIGNED
- **Closeout mode:** success-closeout
- **Task status:** completed
- **Evaluation verdict:** SKIPPED — deterministic governance/control-plane contract migration; no nondeterministic model-output benchmark is part of acceptance

Repository-owned lifecycle state is reconciled separately from mutable hosting-
platform metadata. Future Portable Kit work resumes with the previously reserved
WB-CORE-004 installer/packaging Work Block.
