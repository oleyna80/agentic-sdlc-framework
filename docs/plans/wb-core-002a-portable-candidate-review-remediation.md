---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-002a-portable-candidate-review-remediation
work_block_id: WB-CORE-002A
status: in_progress
owner_role: orchestrator
created_at: 2026-07-31
process_level: Standard
---

# WB-CORE-002A — Portable Candidate Review Remediation

## Objective and Source Contracts

Remediate the three P2 findings against the portable candidate without changing
the accepted portable-kit specification, ADRs, current operational architecture,
or candidate promotion state.

Source contracts are `docs/specs/portable-agentic-sdlc-project-kit.md` sections
5 and 9, `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`,
and `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`.

## Process-Level Classification

**Level:** Standard.

The bounded documentation remediation has no High-Risk trigger: no production
operation, secrets or permissions change, destructive action, live data mutation,
external transaction, or trust-boundary change. It is not Quick because it
changes coordinated authority/lifecycle contracts and requires independent
Reviewer and Verifier assurance. Side effects are limited to the draft candidate
and repository lifecycle projections; rollback is a targeted reversal of this
Work Block's changes.

## Scope and Exact Write-Set

In scope only:

```text
candidate/portable-agentic-sdlc-kit/template/AGENTS.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/work-block.md
docs/plans/wb-core-002a-portable-candidate-review-remediation.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

Out of scope: all other paths, including `docs/reports/**`, root
`PROJECT_BRIEF.md`, WB-CORE-003, the accepted specification and ADRs, installer
or runtime work, dependencies, configuration, database/schema/migration work,
deployment, and any mutable VCS or hosting-platform state.

## Roles, Side Effects, Risks, and Hard Stops

- One Coder owns the exact write-set in an isolated worktree; Reviewer and
  Verifier are read-only and independently assure the resulting exact normative
  subject in later stages.
- The sole intended side effect is clearer candidate lifecycle/template guidance
  and an active lifecycle projection. The candidate remains draft, noncanonical,
  uninstalled, unpromoted, and without current authority.
- Stop for scope expansion, a needed specification/ADR change, any installer or
  runtime work, dependency/configuration/database/deploy change, a secret,
  destructive operation, unclear authority, or failed required assurance.
- DB mode: none. No dependency, configuration, deployment, installer, runtime,
  external side effect, commit, push, pull request, or hosting action is
  authorized.

## P2 Acceptance Criteria

1. `template/AGENTS.md` states the authoritative lifecycle order exactly as
   Intake/classify → Define: discovery, architecture, specification, plan/tasks,
   Critic → Execute → Assure → Close, with the applicable between-stage assurance
   sequence and truthful-closeout boundary.
2. The Work Block template explicitly captures process-level classification and
   rationale, Source Contracts, scope/out-of-scope, exact write-set, roles, side
   effects, risks/Hard Stops, approvals, rollback, acceptance/assurance, and
   write-gate state.
3. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` consistently project
   WB-CORE-002A as the sole active Work Block, while keeping the current
   operational architecture unchanged and recording independent Reviewer and
   Verifier assurance as pending rather than complete.

## Execution, Assurance, and Rollback

Execute only the five paths listed above. Run structural and release/governance
validators applicable to this documentation-only change. Independent Reviewer
and Verifier assurance remains pending; this Work Block creates no evidence
report and makes no readiness, verification, closeout, or mutable VCS/hosting
claim.

Rollback is a targeted reversion of only this Work Block's approved paths after
Owner authorization. The write gate is **OPEN** for this sole Coder in this
isolated worktree; no overlapping writer is permitted.
