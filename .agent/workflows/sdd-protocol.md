# SDD Protocol — Framework Self-Hosting Procedure

This procedure operationalizes the runtime-neutral lifecycle for framework
maintenance. It is subordinate to `AGENTS.md` and accepted `governance/`;
it does not grant authority or install enforcement.

## State and authority

Use the lifecycle states in `governance/lifecycle.md`: Define → Execute →
Assure → Close, with execution state distinct from assurance verdicts. A failed,
unavailable, or unverified check is never a pass. Drafts, candidates, generated
context, requirements-quality reports, tasklists, operational memory, and
Engineering Memory classification cannot override higher authority.

## Stage 0 — Define

The Orchestrator records objective, scope/exclusions, authority chain, risk,
side effects, Hard Stops, exact write-set, one-Coder ownership, topology,
capability limitations, acceptance checks, required assurance, and explicit
Owner approvals. When durable learning is a credible closeout outcome, include
the exact Engineering Memory target path in the approved Work Block/write-set;
Close must not manufacture write authority after a lesson is discovered.

For formal Managed/Assured/Distributed work, Stage 0 also follows
`governance/define-quality.md`:

```text
specification draft
  -> requirements clarification
  -> requirements-quality review
  -> architecture / implementation plan
  -> traceable task decomposition + write-set
  -> deterministic traceability validation
  -> read-only spec/plan/task consistency analysis
  -> Critic
  -> write gate READY
```

Repository/discovery-resolvable facts are resolved from evidence instead of
asking the Owner. Reasonable non-material defaults are explicit assumptions.
Independent material questions may be asked in a small bounded batch; dependent
questions are asked sequentially. Unresolved blocking ambiguity keeps Define
blocked.

Formal requirement implementation tasks use stable `REQ-*`, `AC-*`, and
`TASK-*` references and explicit paths. Enabling, assurance, and documentation
tasks are classified honestly and do not require fake product requirement IDs.
Run `scripts/validate-define-traceability.py` when that stable-ID format is in
use. A `BLOCKED` structural result cannot be waived by a fluent analysis.

For parallel Coder work, the Stage 0 record also contains a common immutable base
revision; a stream ownership matrix of Coder, exclusive paths, and isolation
identifier; proof that the worker-path intersection is empty; dependencies;
named frozen handoffs; recovery points; Integration Coder and glue-path
ownership; and the approved integration plan. A shared path is serialized under
one owner, never concurrently edited.

For Managed work, a read-only Critic challenges this record after the applicable
requirements-quality and consistency checks. `READY` means its challenge found no
unresolved blocker; `BLOCKED` returns to Define. `SKIPPED` is only for bounded
low-risk Controlled work. `DEGRADED` records missing independence/capability and
required approval. A Critic result does not itself open a write gate. A Stage 0
record that authorises parallel Coder streams requires governance profile Managed
or Assured; the Critic gate is mandatory and may not be SKIPPED.

## Stage 1 — Execute

One Coder edits only its approved exclusive write-set after the Critic gate is
resolved. Parallel Coders require the Stage 0 record above and distinct isolated
worktrees or clones; their worker-path intersection must remain empty. Inspect Git
state first, preserve unrelated work, run scoped checks, and stop for a scope,
authority, risk, acceptance, or material requirement change. Freeze each worker
handoff at its named revision and report `DONE`, `DONE_WITH_CONCERNS`,
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
missing evidence is `BLOCKED` or `UNVERIFIED`. Evaluation is selected only by
risk or non-determinism and uses observable artifacts/events, never private
reasoning. Report actual isolation; same-context assurance is never called
independent and is unavailable where the profile requires independence.

Requirements-quality review is not Stage 2 implementation assurance: it checks
whether the specification was implementable before coding. Stage 2 still reviews
and verifies the delivered code against the approved specification.

## Stage 3 — Close

Only completed required assurance permits successful closeout. Otherwise use
reporting-only closeout and preserve the blocker. Synchronize authoritative
records only when their governing contract requires it.

For every **non-trivial** Work Block, including reporting-only closeout, the
Orchestrator MUST perform a Learning Review before Close is complete:

1. Review material findings encountered during **Define, Execute, Assure, and Close** rather than considering only the final assurance report.
2. Identify candidate reusable knowledge such as recurring failure/recovery
   patterns, durable invariants, source-of-truth lessons, lifecycle/process
   defects, verification gaps, reusable operational patterns, or rejected
   approaches with an important evidence-backed reason.
3. Apply the utility filter: durable knowledge must be evidence-backed and
   capable of changing future planning, execution strategy, review,
   verification, recovery, or invariant enforcement. Exclude one-off noise,
   speculation, raw transcripts, private chain-of-thought, secrets/private data,
   routine status chronology, and facts cheaper to re-verify live.
4. Classify material reusable candidates as exactly `promoted`,
   `operational-only`, or `not-applicable`. `none identified` is valid; do not
   create a lesson just to satisfy the closeout form.
5. Before `promoted`, deduplicate against existing Engineering Memory. Prefer
   updating/extending/superseding an existing reusable principle over creating a
   duplicate.
6. A promoted lesson records evidence, scope, reusable principle,
   replacement/mitigation/recovery, authority boundary, review trigger, and last
   verified.
7. Promotion may mutate only an Engineering Memory path already approved by the
   active Work Block. Classification/candidate discovery is not permission; if
   the required path or material policy change is outside the write-set, return
   to Define.
8. Keep project-specific lessons project-local. Repetition/generalization may be
   recorded as a follow-up candidate, but framework policy/template promotion
   requires a separate evidence-backed framework Work Block.

This Learning Review is ordinary Orchestrator Close responsibility and does not
require a separate Owner reminder such as "record the lesson" after the Work
Block and relevant write authority are approved. Record review coverage,
candidate dispositions/deduplication, evidence, residual risk, and next action in
the closeout report.

When `governance/release-state.md` authorizes an explicit `pre_closeout_candidate`,
use its sequence exactly: Owner-authorized local candidate declaration and
status-only commit; deliberate `CANDIDATE_READY` validation; independent final
assurance of that exact candidate; evidence-only persistence; exact
candidate-to-evidence comparison; ordinary release-state validation and CI; then
separate Owner merge approval. A candidate is never a completed, release-ready,
or externally promotable state, and ordinary validation does not pass until every
declared evidence artifact binds the candidate subject.

Canonical promotion is a distinct Owner-gated transition, never part of
mechanism implementation or evidence persistence. It is permitted only as the
validated sole-parent, exact-two-path registry/map transition described by
`governance/release-state.md`; any source, manifest, or multi-parent change is a
separate subject and must stop for Owner direction.

## Capability routing and hard stops

Inspect live capability evidence before assignment: `unknown` is unavailable.
Choose the least-cost option only after it meets role authority, write
permission, required isolation/independence, assurance needs, and Hard Stops.
Record actual capability and fallback without provider-specific shared policy.
Stop for unapproved scope, material authority or risk changes, failed required
checks, secrets, destructive or consequential external actions, or missing
required capability/evidence. Normal reversible development operations inside an
approved Work Block/write-set, including staging, local commits, and normal
feature-branch pushes, follow `AGENTS.md` and `governance/authority.md`.
