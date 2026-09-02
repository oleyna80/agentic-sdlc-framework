# Work Block: Orchestrator Execution State / Stateful Work Block Runtime

> Introduces a bounded, runtime-neutral execution-state plane for long-running
> Work Blocks so the Orchestrator can reason from canonical current state rather
> than accumulated conversation history, while preserving provenance in separate
> evidence and durable reusable knowledge in Engineering Memory.

## Meta
- **Work Block ID:** `WB-2026-09-02-orchestrator-execution-state`
- **Date:** 2026-09-02
- **Owner:** Repository Owner
- **Base branch:** `main`
- **Base revision:** `be988807c38543eb90a728fcb4349bc97dd5695a`
- **Feature branch:** `wb/2026-09-02-orchestrator-execution-state`
- **Governance profile:** Managed
- **Side-effect class:** framework governance / runtime contract / validation
- **Verification tier:** standard + deterministic contract tests

## Independence Boundary
This Work Block is independent of:

- `agent/wb-learning-001-orchestrator-learning-loop`;
- `WB-RELEASE-002` candidate/promotion lifecycle work;
- any branch, commit, write-set, assurance subject, release state, or promotion
  lifecycle belonging to those Work Blocks.

No commit from those branches is an implicit dependency or permitted merge source.
Any later convergence requires a separately reviewed integration decision.

## Lifecycle State
- **Current Stage:** Define
- **Execution State:** in_progress
- **Write Gate:** BLOCKED pending Define completion and Critic
- **Owner Approval Evidence:** Owner explicitly approved a separate branch and new
  Work Block in chat on 2026-09-02.
- **Critic Gate:** pending
- **Verification Verdict:** pending
- **Evaluation:** required for long-horizon/context-efficiency behavior if a runtime
  implementation is included.

## Source Research
Primary research input:

- arXiv:2608.26263, describing a state-centric agent runtime in which persistent
  structured execution state replaces accumulated interaction history as the
  default context carrier for long-horizon execution.

The paper is design evidence, not framework authority. Any adopted mechanism must
conform to this repository's governance, lifecycle, evidence, memory, authority,
and runtime-neutrality contracts.

## Problem Statement
The framework already records substantial structured Work Block state, including
stage, execution state, assurance verdicts, write sets, approvals, integration
bindings, frozen subjects, and external capability state. However, long-running
Orchestrator sessions can still rely materially on accumulated conversational/tool
history to reconstruct current truth.

This creates four risks:

1. context/token growth with Work Block duration;
2. stale facts continuing to influence decisions after authoritative external
   observations change;
3. tool/log noise contaminating subsequent reasoning;
4. recovery and cross-runtime handoff depending on narrative history rather than
   one validated current-state contract.

## Objective
Define and, if accepted by the Critic, implement a runtime-neutral **Execution
State Plane** in which:

1. the next Orchestrator action is assembled primarily from immutable procedure,
   canonical current Work Block state, and the latest relevant observation;
2. model-produced state changes are proposed as bounded patches and applied only
   through deterministic schema/invariant validation;
3. provenance/history remains append-only evidence and is retrieved on demand
   rather than injected wholesale into every step;
4. reusable cross-Work-Block knowledge remains the responsibility of Engineering
   Memory and the existing Learning Review;
5. state replacement/recovery semantics invalidate stale assurance or subject
   claims deterministically when authoritative observations change;
6. multi-agent updates cannot silently create conflicting concurrent state
   ownership.

## Architectural Separation
The Work Block must preserve three distinct planes:

### Execution State Plane
Answers: **what is currently true and what transition is legal next?**

Expected characteristics:
- compact;
- structured;
- mutable only through validated transitions;
- sufficient for routine next-step orchestration;
- no raw transcripts or private reasoning.

### Evidence Plane
Answers: **what observable evidence supports the current state and what happened?**

Expected characteristics:
- append-only or immutable-by-subject evidence references;
- suitable for review, verification, debugging, audit, and recovery;
- selectively retrieved when needed;
- not injected wholesale by default.

### Engineering Memory Plane
Answers: **what durable reusable engineering lesson should influence future Work
Blocks?**

This remains governed by the existing non-trivial Work Block Learning Review.
Execution state MUST NOT become a second Engineering Memory system.

## In Scope
- Inventory the existing executable Work Block state and determine what already
  satisfies an Execution State Plane contract.
- Define minimal canonical state fields required for next-step orchestration.
- Define a machine-readable state-patch contract.
- Define deterministic reducer/validator behavior and rejection semantics.
- Define authoritative observation/reconciliation rules, including external
  revision changes that make prior assurance stale.
- Define evidence-pointer and selective-retrieval semantics.
- Define context-assembly rules that avoid default full-history replay.
- Define recovery/restart semantics across sessions/runtimes.
- Define multi-agent state ownership/conflict rules consistent with exclusive
  write sets and frozen handoffs.
- Add deterministic tests/validators where executable contracts are introduced.
- Evaluate whether Codex Cloud can serve as an admitted worker/runtime for this
  Work Block without becoming framework authority.
- Update documentation/templates/navigation only where required by the accepted
  architecture.

## Out of Scope
- Replacing Engineering Memory or the current Learning Review.
- Changing `WB-RELEASE-002` release/promotion semantics.
- Importing the paper's implementation or schema verbatim.
- Persisting private chain-of-thought.
- Treating conversation transcripts as canonical state.
- Building a vector database or generalized semantic-memory service.
- Provider-specific governance rules for Codex, Claude, OpenCode, or other agents.
- Production deployment, credentials, secrets, destructive Git operations, or
  protected-branch mutation.

## Candidate State Model
The exact schema is subject to Define/Critic review, but the working model is:

```yaml
work_block:
  id:
  stage:
  execution_state:
subject:
  base_revision:
  current_revision:
  frozen_revision:
scope:
  write_set: []
  exclusions: []
authority:
  approvals: []
  hard_stops: []
  capabilities: {}
progress:
  active_task:
  completed_tasks: []
  blockers: []
  pending_decisions: []
assurance:
  critic:
  reviewer:
  verifier:
  evaluation:
  evidence_refs: []
invariants: []
next_action:
```

The implementation should extend or normalize existing canonical state rather
than creating a gratuitous parallel state file.

## Candidate Transition Contract
A model/runtime worker may propose only a bounded transition, for example:

```json
{
  "state_patch": {
    "subject.current_revision": "<observed-sha>",
    "assurance.reviewer": "stale",
    "assurance.verifier": "stale"
  },
  "evidence_refs": ["<stable-evidence-ref>"],
  "proposed_next_action": "re-freeze subject and rerun required assurance"
}
```

A deterministic reducer MUST reject malformed, unauthorized, invariant-breaking,
or out-of-write-authority transitions. Model fluency cannot waive validator
failure.

## Authority and Invariants
At minimum:

- runtime/provider adapters cannot redefine governance;
- state classification is not permission;
- state patches cannot expand the approved write set or external capability;
- changing the assurance subject invalidates assurance bound to the old subject;
- evidence references cannot silently rewrite historical evidence;
- a worker cannot mutate another worker's exclusively owned state surface;
- conflict resolution that requires architecture/scope/authority change returns
  to Define;
- hidden reasoning is never required evidence.

## Initial Write-Set
Define-stage research may refine this list before the write gate opens.

```text
docs/plans/WB-2026-09-02-orchestrator-execution-state.md
.agent/workflows/sdd-protocol.md
governance/lifecycle.md
governance/evaluation.md
docs/mcp-tool-policy.md
runtimes/codex/README.md
framework/memory/project-engineering-memory.md
template/.agent/active-work-block.default.json
template/.agent/active-work-block.json
template/.agent/workflows/sdd-protocol.md
template/docs/session-bootstrap.md
template/docs/templates/work-block-template.md
scripts/validate-work-block-state.py
scripts/test-validate-work-block-state.py
PROJECT_MAP.md
FILE_REGISTRY.yml
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
```

No file beyond this candidate write-set may be changed without returning to
Define and recording the scope change.

## Codex Cloud Feasibility Gate
Codex Cloud may be used only as an admitted runtime/worker, never as authority.
Before dispatch:

1. confirm the repository is accessible to the user's Codex Cloud environment;
2. record the exact base revision/branch supplied to the task;
3. assign one bounded role and explicit write set;
4. prohibit protected/default-branch mutation and unrelated branch adoption;
5. require the worker to report exact resulting revision/diff/evidence;
6. treat Codex Cloud output as worker evidence, not Reviewer/Verifier independence
   unless actual isolation and the selected governance profile support that claim;
7. reconcile returned state against GitHub before accepting it as current truth.

If these conditions cannot be demonstrated, Codex Cloud remains unavailable for
state-changing execution and may be used only for read-only analysis.

## Acceptance Criteria
- [ ] Existing state surfaces are inventoried and duplicate-state risk is resolved.
- [ ] One canonical execution-state authority is named.
- [ ] State updates have schema and invariant validation.
- [ ] Invalid state patches fail closed and preserve previous valid state.
- [ ] Current-state context can be assembled without default full conversation
      replay.
- [ ] Evidence remains available for audit/debug/review through stable references.
- [ ] Authoritative external revision changes deterministically stale affected
      frozen-subject assurance.
- [ ] Restart/cross-runtime handoff can recover current execution state without
      reconstructing it from chat history.
- [ ] Multi-agent conflicting state writes are prevented or deterministically
      rejected.
- [ ] Execution State and Engineering Memory responsibilities remain separate.
- [ ] Existing lifecycle, write-set, Hard Stop, and external capability authority
      cannot be expanded by a state patch.
- [ ] Deterministic validation/tests pass.
- [ ] Long-horizon evaluation demonstrates no material correctness regression and
      measures context/token reduction versus a history-heavy baseline.
- [ ] Codex Cloud use, if exercised, is evidence-backed and correctly classified.

## Evaluation Plan
If implementation changes runtime context assembly, evaluate at least:

1. **Long-horizon synthetic Work Block:** repeated observations and transitions
   over >= 50 steps.
2. **External-state replacement:** remote HEAD or assurance subject changes after
   an earlier accepted observation.
3. **Noise injection:** large irrelevant CI/tool output that should not persist in
   subsequent default context.
4. **Recovery:** new session/runtime reconstructs legal next action from canonical
   state + evidence references.
5. **Conflict:** two workers propose overlapping or contradictory state patches.

Record correctness, validator outcomes, prompt/context size where observable, and
failure/recovery behavior. Do not claim token savings that are not measured.

## Risks
| Risk | Mitigation / Stop Condition |
|---|---|
| New state layer duplicates `.agent/active-work-block.json` | Extend/normalize existing canonical state where possible; stop if two authorities emerge. |
| Compression loses a fact needed later | Keep stable evidence pointers and selective retrieval; do not delete provenance merely because it leaves active state. |
| LLM corrupts canonical state | Deterministic patch schema + invariant validator; reject and retain prior valid state. |
| State patch silently expands authority | Validator binds changes to approved scope/capabilities; material change returns to Define. |
| Evidence/history becomes unbounded prompt context again | Evidence is retrievable, not default-injected. |
| Multi-agent races create non-deterministic truth | Exclusive ownership / serialized shared-state transitions / deterministic conflict rejection. |
| Codex Cloud output is mistaken for independent assurance | Record actual runtime isolation and role; never infer independence from provider name. |
| Paper benchmark is over-generalized | Run framework-specific evaluation; treat paper results as hypothesis evidence only. |

## Verification Plan
Candidate checks after implementation:

- state-schema/validator unit tests;
- malformed/unauthorized/stale-subject patch tests;
- existing framework contract suite;
- publication/template parity checks;
- `git diff --check`;
- search for contradictory state-authority wording;
- evaluation fixtures described above.

Exact commands will be finalized after repository inventory.

## Recovery / Rollback
All implementation remains on the isolated feature branch. Recovery must preserve
unrelated branches and Work Blocks. Revert only commits belonging to this Work
Block; do not reset, rewrite history, or mutate the Learning Loop / RELEASE-002
branches as part of rollback.

## Define-Stage Open Questions
- Which existing fields in `.agent/active-work-block.json` are already sufficient
  and which truly require extension?
- Should evidence references live directly in canonical state or in a small
  bounded index pointing to existing reports/artifacts?
- What is the minimal patch grammar that remains provider/runtime neutral?
- Which transitions can be mechanically inferred by the reducer (for example,
  assurance invalidation after subject change) rather than requested by an LLM?
- What context-size metric is reliably observable across supported runtimes?

These questions are repository/research-resolvable and should be answered during
Define without unnecessary Owner interruption unless they produce a material
scope or authority decision.

## Execution Log
| Date | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| 2026-09-02 | Define | Owner approved separate branch and new Work Block | chat instruction | complete |
| 2026-09-02 | Define | Branch created from exact `main` revision `be988807c38543eb90a728fcb4349bc97dd5695a` | GitHub ref | complete |
| 2026-09-02 | Define | Initial state-plane architecture and boundaries recorded | this plan | complete |
| 2026-09-02 | Define | Codex Cloud feasibility added as an explicit admission gate | OpenAI current product documentation + framework capability rules | in_progress |
