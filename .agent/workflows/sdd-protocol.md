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
Owner approvals. For parallel Coder work, this record also contains a common
immutable base revision; a stream ownership matrix of Coder, exclusive paths,
and isolation identifier; proof that the worker-path intersection is empty;
dependencies; named frozen handoffs; recovery points; Integration Coder and
glue-path ownership; and the approved integration plan. A shared path is
serialized under one owner, never concurrently edited.

For Managed work, a read-only Critic challenges this record before execution.
`READY` means its challenge found no unresolved blocker; `BLOCKED` returns to
Define. `SKIPPED` is only for bounded low-risk Controlled work. `DEGRADED`
records missing independence/capability and required approval. A Critic result
does not itself open a write gate. A Stage 0 record that authorises parallel
Coder streams requires governance profile Managed or Assured; the Critic gate
is mandatory and may not be SKIPPED.

## Stage 1 — Execute

One Coder edits only its approved exclusive write-set after the Critic gate is
resolved. Parallel Coders require the Stage 0 record above and distinct
isolated worktrees or clones; their worker-path intersection must remain empty.
Inspect Git state first, preserve unrelated work, run scoped checks, and stop
for a scope, authority, risk, or acceptance change. Freeze each worker handoff
at its named revision and report `DONE`, `DONE_WITH_CONCERNS`,
`NEEDS_CONTEXT`, or `BLOCKED`. Written files and worker checks are not a final
completion or readiness claim.

When integration is approved, the Integration Coder is a separately bounded
Coder assignment with a distinct integration worktree and owned glue paths. It
may only cleanly adopt the named frozen worker revisions. A merge conflict,
revision substitution, or edit to a worker-owned path returns the Work Block to
Define. Once integration is complete, freeze one integrated revision and path
manifest before Stage 2. Any normative edit after this freeze invalidates
readiness and requires a new freeze and applicable assurance.

## Stage 2 — Assure

Reviewer and Verifier assess the frozen subject read-only. For parallel work,
that subject is the one frozen integrated revision and path manifest, not an
individual worker output; worker checks are input evidence only. Review checks
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
