---
schema_version: 1
artifact_type: critic_review
artifact_id: wb-core-003b-critic
work_block_id: WB-CORE-003B
reviewed_stage: define
reviewed_subject: define-stage Work Block and tasklist
verdict: APPROVE
created_at: 2026-08-03
isolation: separate_subagent
recorded_by_role: orchestrator
---

# Critic Review — WB-CORE-003B Define Stage

## Reviewed scope

- `docs/plans/wb-core-003b-self-hosting-control-plane-reconciliation.md`
- `docs/tasklist/wb-core-003b-self-hosting-control-plane-reconciliation.md`
- accepted governance, Portable Kit specification, applicable ADRs, navigation,
  registry, and dirty legacy drafts as non-authoritative reference input.

## Findings

The proposed single Work Block has one coherent outcome and authority-drift
boundary. Its exact one-Coder delivery set, exclusions, and future-Work-Block
boundaries prevent accidental candidate promotion, runtime-adapter work, hooks,
configuration, installers, or VCS action.

The Work Block selects the `Managed` governance profile and requires separate
read-only Critic, Reviewer, and Verifier contexts. If demonstrated subagent
isolation is unavailable, a separately started top-level session is required;
otherwise execution remains blocked. Same-context assurance is not an allowed
fallback.

Capability selection is runtime-neutral and live-evidence-first. An unknown
capability is unavailable. Cost applies only among options that already meet
role authority, write permission, required independence/isolation, assurance,
and Hard Stops.

The plan separates the initial frozen normative subject, preliminary assurance,
declared terminal lifecycle projection, and final assurance. The
post-preliminary projection is explicitly a new normative subject and therefore
invalidates preliminary readiness by design. Operational-memory updates remain
lower-authority, derived records and may not assert a verdict absent from linked
evidence.

## Verdict and handoff

**Verdict: APPROVE.**

**Critic gate: READY.**

A single Coder may begin Execute only within the declared delivery set. Any
normative change after final assurance, failed required check, unavailable
independence, scope expansion, runtime/configuration/hook/installer work, or
VCS action returns the Work Block to Define or the Owner as applicable.
