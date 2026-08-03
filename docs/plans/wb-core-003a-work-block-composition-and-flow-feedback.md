---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003a-work-block-composition-and-flow-feedback
work_block_id: WB-CORE-003A
status: completed
owner_role: orchestrator
created_at: 2026-08-03
base_revision: 1710c44bf38ddfb2330e86838e8f976b5e9a71d6
branch: agent/wb-core-003a-work-block-flow-feedback
process_level: Standard
---

# WB-CORE-003A — Work-Block Composition and Flow Feedback

## Objective and Source Contracts

Turn proven WB-CORE-003 process lessons into a later portable rule for Work
Block composition and evidence-based material process findings. This opening
authorizes definition only.

- **Owner approval:** explicit approval to open and define WB-CORE-003A on
  2026-08-03. This authority does not authorize commit, push, merge, release,
  installation, promotion, or any external action.
- **Accepted specification:**
  `docs/specs/portable-agentic-sdlc-project-kit.md`.
- **Accepted architecture decisions:**
  `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`
  and
  `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`.
- **Opening baseline and isolation:**
  `1710c44bf38ddfb2330e86838e8f976b5e9a71d6` in the clean isolated worktree
  on branch `agent/wb-core-003a-work-block-flow-feedback`; no other repository
  writer is authorized for this opening.

## Process-Level Classification

**Level:** Standard.

This is a coordinated governance change to an accepted target specification and
portable candidate templates and skills. It requires one bounded Coder write-set,
Critic challenge, independent review and verification, drift assessment, and
truthful SSOT closeout. No High-Risk trigger applies: there is no irreversible
side effect, production deployment or restart, secret/credential/permission
change, destructive operation, live data or business-state mutation, security
or trust-boundary change, consequential external transaction, material
legal/privacy/financial consequence, or difficult-to-bound nondeterminism.

Quick is ineligible because the change coordinates accepted-target governance
semantics across a specification, templates, and skills and requires independent
Critic, Reviewer, and Verifier assurance. Its outcome is bounded and reversible
through a targeted rollback, so Standard is sufficient.

## Scope and Later Implementation Write-Set

In scope is a portable rule that:

- defines a Work Block by one verifiable outcome plus a coherent risk,
  write-set, and assurance boundary;
- permits multiple interdependent tasks in that single Work Block;
- requires a split only for an independent deliverable, distinct Owner
  authority or Hard Stop, conflicting ownership or write-set, a separate
  rollback boundary, or an independently verifiable assurance chain; and
- records only evidence-based material flow signals about scope, authority,
  reliability, assurance, or evidence quality.

The later implementation has separated authority boundaries. The sole Coder may
change only this frozen normative subject:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/work-block.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/closeout-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/task-decomposition/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/ssot-sync-closeout/SKILL.md
```

After that subject is frozen, Critic, Reviewer, and Verifier may each write only
their own bounded report contents in a separately documented evidence-authority
stage. They may never alter the normative subject they assess. The expected
report paths are:

```text
docs/reports/reviews/wb-core-003a-critic.md
docs/reports/reviews/wb-core-003a-independent-review.md
docs/reports/reviews/wb-core-003a-drift-assessment.md
docs/reports/verification/wb-core-003a-verification.md
```

The Orchestrator owns later SSOT and closeout projection only, using these paths
after the required assurance is complete:

```text
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/plans/wb-core-003a-work-block-composition-and-flow-feedback.md
docs/tasklist/wb-core-003a.md
docs/reports/closeout/wb-core-003a-work-block-composition-and-flow-feedback.md
```

## Material Process Finding Contract

A material process finding is testable only when it records all of the
following: an observed condition; one allowed category; its concrete effect on
scope, authority, reliability, assurance, or evidence quality; an
evidence/check/decision reference; and its disposition. Allowed categories are
scope, authority, reliability, assurance, and evidence quality.

Routine status, timestamps, agent or model activity, raw prompts or runtime
transcripts, hidden reasoning, secrets, and a continuous activity log are not
findings and must not be recorded. `none observed` is the only valid form when
there is no material signal. This contract does not add Quick-Work-Block
bureaucracy.

Out of scope: root `AGENTS.md`, all legacy `template/` paths, installer and
runtime paths, candidate installation or promotion, completed Work Block
artifacts, dependencies, configuration, database/schema/migration work,
deployment, external side effects, commit, push, merge, release, and mutable
hosting-platform state.

## Roles, Risks, and Hard Stops

- The opening write gate is **OPEN** only for one Coder in the isolated
  worktree and only for this opening's four approved paths. Later implementation
  and evidence stages require their separately bounded authority described
  above; overlapping normative writers are prohibited.
- Critic, Reviewer, and Verifier remain independent from the normative subject
  and have report-only authority in the later evidence stage.
- The candidate remains noncanonical, uninstalled, unpromoted, and
  non-authoritative throughout this Work Block.
- Stop for any needed scope expansion, unclear authority, installer/runtime or
  legacy-template change, dependency/configuration/database/deploy change,
  secret, destructive operation, or failed required assurance.

## Acceptance and Assurance

1. A multi-task Work Block can state why its tasks belong to one verifiable
   outcome and coherent risk/write-set/assurance boundary.
2. All five split triggers are explicit and no task-count or agent-count rule is
   introduced.
3. Material process findings are evidence-based and limited to scope, authority,
   reliability, assurance, or evidence quality.
4. The portable candidate remains runtime-neutral and receives neither installer
   nor runtime ownership.
5. The later exact normative subject passes applicable structural, contract,
   diff, independent review, verification, drift, and closeout checks.

Rollback, if later authorized, is a targeted reversal of only the then-approved
WB-CORE-003A paths to the recorded pre-change revision; it does not revert
unrelated work or any completed Work Block. This opening makes no readiness,
verification, closeout, or mutable VCS claim.

## Final State

- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

These required machine-readable values define the proposed terminal state for
release-state validation. They are not a claim that final Reviewer, Verifier,
and drift evidence for this uncommitted terminal lifecycle projection has
already been recorded or committed.

Completed initial Critic, independent Review, Verification, and drift-assessment
evidence is bound to working-tree subject base
`1710c44bf38ddfb2330e86838e8f976b5e9a71d6` and the five normative paths:

1. `docs/specs/portable-agentic-sdlc-project-kit.md`
2. `candidate/portable-agentic-sdlc-kit/template/agentic/templates/work-block.md`
3. `candidate/portable-agentic-sdlc-kit/template/agentic/templates/closeout-report.md`
4. `candidate/portable-agentic-sdlc-kit/template/agentic/skills/task-decomposition/SKILL.md`
5. `candidate/portable-agentic-sdlc-kit/template/agentic/skills/ssot-sync-closeout/SKILL.md`

The five-path normative diff SHA-256 is
`1e05ba31861e606c26b4f1741e670317fff601e5db01b871933985a8d53d67bb`.
The uncommitted terminal lifecycle projection is the candidate subject for
final applicable Reviewer, Verifier, and drift assurance before any commit.
It makes no claim about staging, commit, push, merge, release, installation,
promotion, or other external mutable VCS state.
