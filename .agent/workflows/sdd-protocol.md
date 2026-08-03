# SDD Protocol — Framework Self-Hosting Procedure

This procedure operationalizes the runtime-neutral lifecycle for framework
maintenance. It is subordinate to `AGENTS.md` and accepted `governance/`;
it does not grant authority or install enforcement.

## State and authority

Use the lifecycle states in `governance/lifecycle.md`: Define → Execute →
Assure → Close, with execution state distinct from assurance verdicts. A failed,
unavailable, or unverified check is never a pass. Drafts, candidates, generated
context, and operational memory cannot override higher authority.

## Stage 0 — Define

The Orchestrator records objective, scope/exclusions, authority chain, risk,
side effects, Hard Stops, exact write-set, one-Coder ownership, topology,
capability limitations, acceptance checks, required assurance, and explicit
Owner approvals. For Managed work, a read-only Critic challenges this record
before execution. `READY` means its challenge found no unresolved blocker;
`BLOCKED` returns to Define. `SKIPPED` is only for bounded low-risk
Controlled work. `DEGRADED` records missing independence/capability and
required approval. A Critic result does not itself open a write gate.

## Stage 1 — Execute

One Coder edits only the approved write-set after the Critic gate is resolved.
Inspect Git state first, preserve unrelated work, run scoped checks, and stop
for a scope, authority, risk, or acceptance change. Freeze the exact changed
file set and report `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or
`BLOCKED`. Written files are not a completion claim.

## Stage 2 — Assure

Reviewer and Verifier assess the frozen subject read-only. Review checks
correctness, boundaries, maintainability, privacy/security, and documentation
drift. Verification demonstrates acceptance criteria with reproducible evidence;
missing evidence is `BLOCKED` or `UNVERIFIED`. Evaluation is selected only
by risk or non-determinism and uses observable artifacts/events, never private
reasoning. Report actual isolation; same-context assurance is never called
independent and is unavailable where the profile requires independence.

## Stage 3 — Close

Only completed required assurance permits successful closeout. Otherwise use
reporting-only closeout and preserve the blocker. Synchronize authoritative
records only when their governing contract requires it; classify knowledge as
durable, operational-only, or not-applicable; and report evidence, residual
risk, and next action.

## Capability routing and hard stops

Inspect live capability evidence before assignment: `unknown` is unavailable.
Choose the least-cost option only after it meets role authority, write
permission, required isolation/independence, assurance needs, and Hard Stops.
Record actual capability and fallback without provider-specific shared policy.
Stop for unapproved scope, failed required checks, secrets, destructive actions,
candidate promotion, configuration/hooks/CI/runtime work, live effects,
staging, commit, or push.
