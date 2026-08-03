---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003d-parallel-write-set-orchestration
work_block_id: WB-CORE-003D
status: completed
owner_role: orchestrator
created_at: 2026-08-03
base_revision: 30374351ca919165a2530d77f6a670438425d355
branch: agent/wb-core-003d-parallel-write-set-orchestration
process_level: Managed
---

# WB-CORE-003D — Parallel Write-Set Orchestration

## Objective and authority

Operationalize the already accepted rule that one Orchestrator may coordinate
multiple Coders in parallel only when every Coder owns an exclusive write-set
in an isolated worktree or clone and a separately scoped Integration Coder
freezes the resulting integrated subject before final assurance. This Work
Block clarifies the framework's self-hosted operational layer; it neither
promotes the Portable Kit nor changes accepted governance authority.

Authority order is the current explicit Owner instruction, root `AGENTS.md`
and accepted governance, accepted specifications and ADRs, this Work Block,
then evidence and memory. The accepted roles/memory/installation ADR already
describes isolated parallel write Work Blocks and integration planning. Current
root governance is stricter: all parallel worker write-sets must be
non-overlapping. An integration plan coordinates frozen handoffs; it never
authorizes concurrent shared-file edits. A shared path has one named owner and
is serialized. This Work Block refines subordinate operating guidance and does
not create a new base role: an Integration Coder is a bounded Coder assignment.

## Composition boundary

This Work Block has one outcome: a coherent, runtime-neutral protocol for
parallel exclusive write-sets and their integration. The root contract, SDD
procedure, roster, mission brief, and integration-plan template must agree on
the same authority, ownership, hard stops, and assurance subject. Splitting
them would leave agents with contradictory instructions about who may write,
integrate, or declare readiness.

The protocol itself is introduced under the currently authoritative one-Coder
execution rule. It must not self-apply parallel writing until it is assured and
closed. A live multi-worktree pilot, generated-template propagation, hooks,
CI enforcement, runtime adapters, and installer work remain separate follow-up
decisions.

## Scope and write boundaries

### Define-stage authority

During Define, the Orchestrator may create or update only this Work Block,
tasklist, navigation, and registry state needed to make it the active bounded
work. The Critic record is evidence of a separate read-only challenge. No
Coder writes are permitted until the Critic gate is resolved.

### Execute delivery set — one Coder under the current contract

```text
AGENTS.md
.agent/workflows/sdd-protocol.md
.agent/ROSTER.md
docs/templates/subagent-mission-brief-template.md
docs/templates/integration-plan-template.md
```

The Coder may only implement the protocol stated in this plan. In particular,
it must retain root authority, describe one Coder per exclusive isolated
write-set (not unrestricted concurrent editing), and treat the Integration
Coder as a separately scoped Coder assignment. It must require a common base
revision, an ownership/topology matrix, frozen worker handoffs, a single frozen
integrated subject, and fresh final assurance against that subject.

### Projection, evidence, and closeout authority — Orchestrator

```text
docs/plans/wb-core-003d-parallel-write-set-orchestration.md
docs/tasklist/wb-core-003d-parallel-write-set-orchestration.md
docs/reports/reviews/wb-core-003d-parallel-write-set-critic.md
docs/reports/reviews/wb-core-003d-parallel-write-set-review.md
docs/reports/reviews/wb-core-003d-parallel-write-set-drift.md
docs/reports/verification/wb-core-003d-parallel-write-set-verification.md
docs/reports/closeout/wb-core-003d-parallel-write-set-orchestration.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

Reviewer, Verifier, and drift-assessment contexts are read-only. The
Orchestrator records their actual findings in evidence reports and may only
make the declared lifecycle projection after required assurance is complete.
Evidence reports do not alter the frozen normative subject they assess.

### Out of scope

- changes to accepted ADRs, specifications, or `governance/**` contracts;
- generated `template/` surfaces, skills, framework specifications, tests,
  scripts, CI, hooks, runtime adapters, configuration, dependencies, or
  installation composition;
- a real parallel Coder pilot, branch integration, merge, cherry-pick, staging,
  commit, push, deployment, live mutation, or destructive action;
- candidate promotion or any claim that a runtime enforces the protocol.

Any discovered need for an excluded change is a hard stop and requires a new
Owner-approved scope rather than silent expansion.

## Topology, risk, and hard stops

- **Profile:** Managed; **side-effect class:** local governance
  documentation; **evaluation:** not required.
- **Current Work Block topology:** one clean worktree at the recorded base
  revision and one Coder during Execute; independent Critic, Reviewer, and
  Verifier are read-only contexts.
- **Future protocol topology:** each task Coder receives one exclusive
  write-set and isolated worktree/clone. The worker-path intersection must be
  empty. Any shared/glue path is exclusively owned by the Integration Coder and
  is serialized. The Integration Coder owns a distinct integration worktree;
  it may adopt named frozen worker revisions, but a conflict or any content edit
  to a worker-owned path returns the work to Define.
- **Primary risks:** overlapping ownership, a shared worktree, a missing or
  mutable handoff revision, treating worker checks as final READY evidence, or
  an Integration Coder silently resolving a design conflict.
- **Hard stops:** missing common base, a non-empty worker-path intersection,
  undocumented serialized ownership of a shared path, undocumented integration
  ownership, merge conflict, post-freeze normative edit, failed required check,
  scope expansion, configuration/hook/CI/runtime work, or any VCS action
  without separate Owner approval.
- **Stage 0 preflight:** database mode is `none`; side effects are `none`;
  the approved branch and clean worktree establish current isolation evidence.
  A separate read-only Critic context has been invoked. Before each subsequent
  assignment the Orchestrator must inspect live capability/isolation evidence
  for the selected Coder, Reviewer, and Verifier; unavailable independence
  blocks this Managed Work Block. Deterministic structural checks plus
  independent review and verification are the planned assurance; evaluation is
  not required because no non-deterministic output or live parallel execution
  is claimed.

## Acceptance and assurance

1. The root contract, SDD procedure, roster, mission brief, and new integration
   template consistently permit parallelism only per exclusive isolated
   write-set. Their worker-path intersections are empty; a shared path has one
   serialized owner. They never create a new authority role.
2. Define records the common base revision, worker/Coder/worktree/write-set
   matrix, dependencies, handoff revisions, integration ownership, recovery,
   and required checks before parallel execution.
3. Integration is a separately named Coder assignment; it may cleanly adopt
   frozen worker outputs but cannot resolve a conflict or edit a worker-owned
   path without a return to Define.
4. A single integrated revision and path manifest are frozen before final
   review, verification, and drift assessment. Worker-level checks are input
   evidence only; post-freeze normative edits invalidate readiness. Until a
   commit is approved, the manifest is reproducible from the exact pathname
   list supplied to assurance: run `sha256sum` for each path, sort the complete
   output lines with `LC_ALL=C sort`, then run `sha256sum` on that line stream.
   The evidence report records the list, individual digests, aggregate, and
   command form.
5. Documentation remains runtime-neutral; no hook, template installation,
   automation, or adapter is claimed as installed or enforced.
6. The frozen subject passes applicable structural, cross-reference, SDD,
   governance, whitespace, and changed-path checks, with independent Critic,
   Reviewer, Verifier, and drift evidence that reports actual isolation.

## Lifecycle plan

1. **Define:** create this bounded active Work Block on the clean recorded
   baseline; record scope, exclusions, topology, acceptance, and hard stops.
2. **Critic gate:** independently challenge authority, circularity, scope,
   generated-surface drift, and final-assurance semantics. A material finding
   returns the plan to Define. The revised non-overlap and Managed-profile
   record received a separate-context `READY` verdict on 2026-08-03; the
   report records intentional generated-surface drift as a required follow-up.
3. **Execute:** one Coder updates only the delivery set and reports a frozen
   candidate subject plus scoped checks.
4. **Assure:** independent Reviewer, Verifier, and documentation-drift review
   assess the exact frozen subject. Any normative repair refreezes the subject
   and repeats applicable assurance.
5. **Close and final assurance:** after preliminary assurance, record the
   evidence-only closeout and the declared plan/task/map/registry lifecycle
   projection. Freeze that changed normative subject and require independent
   final Reviewer, Verifier, and drift assessment before terminal readiness;
   no later normative edit is permitted without renewed assurance. Staging,
   commit, push, PR, and merge remain separate Owner approval boundaries.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic documentation and contract validation are sufficient
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

The terminal state is limited to the approved repository-local governance
subject and is validated by the separately recorded final applicable assurance
for the close projection. It does not claim staging, commit, push, merge,
promotion, installation, deployment, release readiness, or mutable external
VCS status. Any later normative change requires a new applicable Work Block
and assurance chain.
