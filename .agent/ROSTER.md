# Agent Routing Roster

This compact roster routes framework lifecycle work. It is subordinate to
[`AGENTS.md`](../AGENTS.md), accepted governance, the active Work Block,
and the approved write-set. It is an operational index, not a replacement for
the Portable Kit's accepted separate-role ADR or a runtime/model catalog.

| Role | Outcome | Boundary | Procedure route |
| --- | --- | --- | --- |
| Orchestrator | Scope, gates, evidence, next action | Does not implement during Coder step | `task-decomposition`, `spec-consistency-analysis` |
| Architect / Analyst | Read-only recommendation and specification refinement | Cannot approve/write outside scope | `architecture-discovery`, `requirements-clarification` |
| Reviewer (requirements specialization) | Requirements-quality verdict before implementation | Read-only; reviews written requirements, not code | `requirements-quality-review` |
| Consistency analyzer (read-only specialization) | Spec/plan/task/write-set alignment before Critic | Read-only; reports gaps to owning artifact | `spec-consistency-analysis` |
| Critic | Pre-execution challenge after required Define-quality checks | Read-only | `critic-review` |
| Coder | Approved implementation and evidence | One writer per exclusive isolated write-set; no shared-path parallel edits | `scoped-coder` |
| Reviewer | Frozen-subject implementation review | Read-only; no silent repair | `reviewer` |
| Verifier | Reproducible acceptance verdict | Read-only except expressly approved evidence docs | `verifier` |

Requirements Reviewer and consistency analyzer are specializations of existing
read-only roles/functions; they do not create new authority classes. Temporary
Product, Architecture, Frontend, Backend, Design, Security, QA, or Docs Analyst
labels only narrow a research lens; they never expand base-role authority.

For formal Managed/Assured/Distributed feature or governance work, route Define
through:

```text
requirements-clarification
  -> requirements-quality-review
  -> task-decomposition
  -> validate-define-traceability.py
  -> spec-consistency-analysis
  -> critic-review
```

The Architect may resolve repository/discovery facts directly from authoritative
evidence and record reasonable non-material assumptions. Material independent
questions may be batched; dependent questions are sequential. Blocking ambiguity
keeps Define blocked. Requirements-quality/consistency verdicts and validator
results are evidence only; they never grant Coder authority or open Hard Stops.

For non-trivial delegation, use the mission brief template and state role,
specialization, scope, exclusions, authorities, allowed procedure, file-change
permission, expected output, isolation, and Hard Stops. Inspect live capability
evidence before assigning a role: unknown is unavailable. Cost is considered
only among choices meeting required authority, write permission, isolation,
assurance, and Hard Stops. A skill supplies procedure, not authority.

Sequential reuse is not independent assurance. Where the profile does not
permit a documented degraded fallback, stop rather than claim independence.

Where an approved Work Block permits parallel Coder streams, each Coder has a
distinct worktree or clone, isolation identifier, and exclusive paths. The
Orchestrator records an empty worker-path intersection, dependencies, and
frozen handoffs in an integration plan before execution. An Integration Coder
is a separately bounded Coder assignment, not a role: it owns only declared
integration/glue paths in a distinct integration worktree and may cleanly adopt
only named frozen worker revisions. Conflict resolution or a worker-path edit
returns the work to Define. Final Reviewer, Verifier, and drift assurance assess
one frozen integrated revision and path manifest; worker checks are evidence
inputs only, and a post-freeze normative edit invalidates readiness.