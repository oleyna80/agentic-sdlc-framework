# WB-CORE-004 — GitHub-Native Authority Model

Status: READY_FOR_MERGE
Date: 2026-08-12
Owner: Project Owner
Baseline: `12bb1a11dce4957f2258869314016b1b544f2017`

## Objective

Replace per-Work-Block SSH-signed authorization as the normal development security boundary with a simpler capability model: GitHub repository rules, least-privilege credentials, protected default-branch flow, CI, and external Owner-controlled production credentials.

The Agentic SDLC process remains: Work Block → scoped implementation → Critic → Reviewer → Verifier → closeout. The change is about **where security authority lives**, not about removing engineering discipline.

## Decision

SSH signatures and authorization-bootstrap commits are retired from the default development path.

Reason:

1. The signed local state machine created a circular bootstrap problem: authorization had to be committed before it could authorize its own commit.
2. Recovery work exposed excessive implementation complexity: H0/H1/H2 binding, replay handling, specification digests, detached-signature bootstrap, and runtime parity became a larger risk surface than the ordinary Git operations being protected.
3. Project-local hooks are cooperative controls and are writable by the same principal as the agent; they are therefore the wrong place to implement the primary security boundary.
4. GitHub already provides an external boundary for the public framework repository. `main` is covered by an active ruleset requiring pull requests and the `contracts` and `release-state` status checks, with deletion and non-fast-forward updates prohibited.
5. Consequential operations are more reliably constrained by capability separation: the agent receives only the credentials it needs; production/VPS/database/secrets authority is kept outside the agent runtime.

## Authority model

### Normal agent capabilities

Allowed without Owner cryptographic signing:

- read and edit approved Work Block paths;
- run tests, builds, linters, and local disposable tooling;
- `git add` and local commits;
- create and push normal feature branches;
- create/update pull requests;
- inspect CI and review evidence.

### External authority boundaries

The framework repository relies on GitHub for default-branch protection:

- `main` changes only through pull requests;
- required status checks must pass;
- branch deletion is denied;
- non-fast-forward updates are denied;
- no ruleset bypass actor is configured.

Consumer projects must enforce consequential authority outside project-local hooks. Recommended model:

- dedicated fine-grained GitHub credential for the agent;
- `Contents`/PR permissions only as required;
- `Actions: read` for agents that must not dispatch production workflows;
- production secrets kept in GitHub/OS secret stores, not on the agent workstation;
- production deploy manually initiated by Owner or another externally controlled gate;
- VPS/DB credentials inaccessible to the normal agent process.

## Cooperative local guardrails

Generated project hooks remain useful for:

- enforcing the active Work Block write-set;
- rejecting obvious destructive Git/filesystem commands;
- rejecting direct default-branch pushes before GitHub rejects them;
- rejecting live infrastructure/data/credential/client-communication commands in the normal agent channel;
- failing closed when a mutating command cannot be scoped safely.

They are explicitly **not** a cryptographic or OS security boundary.

## Implementation scope

- governance authority/lifecycle documentation;
- framework self-hosting instructions;
- generated active Work Block schema;
- Codex lifecycle helper;
- shared/Codex local guardrails;
- Codex doctor/write-gate documentation;
- authorization documentation changed to legacy/deprecated status;
- contract tests updated to prove the simplified model;
- no production or external infrastructure change.

## Non-goals

- no production deployment;
- no secret or credential creation;
- no GitHub ruleset weakening;
- no removal of Critic/Reviewer/Verifier;
- no removal of write-set discipline;
- no automatic merge to `main`;
- no destructive cleanup of historical signed-authorization artifacts.

## Acceptance criteria

1. Generated projects no longer require `ssh-keygen`, an Owner private key, an `allowed_signers` file, or a detached `.sig` to start normal source work.
2. `git commit` and normal feature-branch push are not Hard Stops.
3. Direct push to `main`/`master`, force push, destructive operations, live infrastructure/data mutations, credential operations, and client-facing communications remain blocked by the normal local guardrail.
4. Work Block write-set enforcement remains active for source mutations and staged commits.
5. `apply_patch` validates both source and `Move to:` destination paths.
6. Complex/unknown mutating Bash fails closed when target paths cannot be safely determined.
7. Documentation states that GitHub/OS/credential separation is the real security boundary.
8. Existing GitHub ruleset remains active and unchanged.
9. Framework `contracts` and `release-state` required checks pass on the PR.
10. Critic, Reviewer, and Verifier find no BLOCKER/HIGH issue before merge.

## Assurance summary

Implementation subject through `8b1300fcf1cae4b63141335818514084ce91030b` completed the schema-v3 authority migration and the corrective hardening discovered during assurance.

Recorded evidence:

- `docs/reports/reviews/wb-core-004-critic.md` — APPROVE after resolving premature closeout, broad/tag push, Claude Bash write-set, and documentation-parity findings;
- `docs/reports/reviews/wb-core-004-review.md` — READY, no remaining BLOCKER/HIGH finding;
- `docs/reports/verification/wb-core-004-verification.md` — READY;
- Framework Contracts run `31624961564` — success on evidence head `c7400ca569b58f94ba68a64fb8ba341e975092e8`;
- Release State Contract run `31624961808` — success on the same evidence head;
- GitHub ruleset `19916164` remains active and unchanged.

The Critic/Reviewer/Verifier records are explicitly same-session connector-backed assurance and are not represented as independent human or separate-runtime review. The exact final PR head must still satisfy the repository-required `contracts` and `release-state` checks before merge.

## Migration

Existing signed authorization records may remain as historical evidence. They are not required by schema v3 and must not be treated as current authority.

Consumer projects may adopt this model incrementally: first install the schema/hooks/docs change, then move production credentials and workflow-dispatch authority outside the agent credential.

## Merge authority

This Work Block authorizes implementation and feature-branch/PR activity. It does not authorize bypassing the existing GitHub ruleset or merging a failing PR. Merge is permitted only through the protected PR path after the exact final head satisfies the required checks and the PR is no longer Draft.
