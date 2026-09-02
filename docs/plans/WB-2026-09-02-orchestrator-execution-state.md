# Work Block: Orchestrator Execution State / Stateful Work Block Runtime

> Introduces a bounded, runtime-neutral execution-state plane for long-running Work Blocks so the Orchestrator can reason from canonical current state rather than accumulated conversation history, while preserving provenance in separate evidence and durable reusable knowledge in Engineering Memory.

## Meta
- **Work Block ID:** `WB-2026-09-02-orchestrator-execution-state`
- **Date:** 2026-09-02
- **Owner:** Repository Owner
- **Base branch:** `main`
- **Base revision:** `be988807c38543eb90a728fcb4349bc97dd5695a`
- **Feature branch:** `wb/2026-09-02-orchestrator-execution-state`
- **Governance profile:** Managed
- **Side-effect class:** framework governance / runtime contract / validation
- **Verification tier:** standard + deterministic contract tests + focused evaluation

## Independence Boundary
This Work Block is independent of:

- `agent/wb-learning-001-orchestrator-learning-loop`;
- `WB-RELEASE-002` candidate/promotion lifecycle work;
- any branch, commit, write-set, assurance subject, release state, or promotion lifecycle belonging to those Work Blocks.

No commit from those branches is an implicit dependency or permitted merge source. Any later convergence requires a separately reviewed integration decision.

## Lifecycle State
- **Current Stage:** Define
- **Execution State:** in_progress
- **Write Gate:** BLOCKED pending consistency analysis + Critic
- **Owner Approval Evidence:** Owner explicitly approved a separate branch and new Work Block in chat on 2026-09-02.
- **Requirements-Quality Review:** READY — `docs/reports/requirements/WB-2026-09-02-orchestrator-execution-state-requirements-review.md`
- **Traceability:** READY — `docs/reports/requirements/WB-2026-09-02-orchestrator-execution-state-traceability.md`
- **Consistency Analysis:** pending
- **Critic Gate:** pending
- **Verification Verdict:** pending
- **Evaluation:** required

## Source Research
Primary research input:

- arXiv:2608.26263, describing a state-centric agent runtime in which persistent structured execution state replaces accumulated interaction history as the default context carrier for long-horizon execution.

The paper is design evidence, not framework authority. Any adopted mechanism must conform to this repository's governance, lifecycle, evidence, memory, authority, and runtime-neutrality contracts.

## Problem Statement
The framework already records substantial structured Work Block state, including scope/write authority, Critic and assurance state, integrations, and external Hard Stops. Long-running Orchestrator sessions can nevertheless still depend on accumulated conversation/tool history to reconstruct current truth.

This creates four risks:

1. context growth with Work Block duration;
2. stale facts influencing decisions after authoritative observations change;
3. CI/tool noise contaminating later reasoning;
4. restart/cross-runtime recovery depending on narrative history rather than validated current state.

## Define Repository Findings

### F-01 — Existing canonical state is the correct anchor
`.agent/active-work-block.json` is already documented and enforced as executable Work Block state. Creating another live execution-state file would introduce an unnecessary second SSOT.

**Disposition:** extend the existing state contract.

### F-02 — Existing state is gate-centric, not sufficient as long-horizon execution state
Schema v3 records authority/gate and assurance data but does not canonically record lifecycle execution stage/state, current/frozen subject generation, active tasks/blockers/pending decisions/next action, latest observation, bounded current evidence pointers, or state mutation versioning.

**Disposition:** schema v4 adds only missing operational state.

### F-03 — Active state is intentionally local/ignored
Generated projects restore missing `.agent/active-work-block.json` from tracked blocked `.agent/active-work-block.default.json`. A fresh/cloud checkout therefore cannot recover an active Work Block from Git alone.

**Disposition:** retain local live state and add non-authoritative validated handoff snapshot export/import for cross-runtime transport. Do not make the high-churn active state a tracked second coordination stream.

### F-04 — Current `define_quality` state already has an internal drift
`template/.agent/active-work-block.default.json` includes `define_quality`, but `template/.codex/scripts/lifecycle.py::default_state()` does not create it. Managed source guards require it, so a Managed `prepare/open` path can produce a state that later guards reject.

**Disposition:** REQ-010/AC-010 make this a mandatory migration repair.

### F-05 — Schema version is coupled across multiple readers
Hard-coded schema-v3 assumptions exist in Codex source guard/doctor, Claude source/assurance guards, state defaults, control-plane/integration tests, runtime docs, and Define/lifecycle wording.

**Disposition:** schema version increases to 4 and all authority-relevant readers migrate atomically in this Work Block; old v3 active state fails closed rather than being silently treated as complete v4 state.

### F-06 — Codex Cloud is technically suitable but remains an admitted worker
Codex Cloud can work from GitHub-hosted repositories/branches and is suitable for a bounded implementation or test task. The active state is not inherently present in a fresh cloud checkout, so a task requiring it must receive a validated handoff snapshot or equivalent admitted payload. Cloud execution does not create authority or assurance independence.

**Current tool limitation:** this Chat session has GitHub repository actions but no direct Codex Cloud dispatch action. The Work Block can define and record the admission/mission contract here; actual cloud dispatch must occur from a Codex surface that exposes cloud tasks. This limitation is capability evidence, not a design blocker.

## Objective
Define and implement a runtime-neutral **Execution State Plane** in which:

1. the next Orchestrator action is assembled primarily from immutable procedure, canonical current Work Block state, and the latest relevant observation;
2. workers propose bounded state changes and a deterministic provider-neutral reducer validates/applies them atomically;
3. provenance/history remains evidence retrievable on demand rather than default full-history context;
4. Engineering Memory remains the separate durable cross-Work-Block learning plane;
5. authoritative subject replacement deterministically invalidates assurance tied to stale subjects;
6. overlapping worker updates cannot silently overwrite accepted state;
7. cross-session/runtime recovery uses a validated non-authoritative snapshot, not transcript reconstruction.

## Normative Specification

`docs/specs/WB-2026-09-02-orchestrator-execution-state.md`

The accepted Define candidate selects:

- schema version 4;
- monotonic `state_version` + expected-version compare-and-swap;
- one live canonical state path;
- protected / runtime-mutable / reducer-derived field classes;
- deterministic atomic reducer;
- max 16 current evidence pointers;
- portable context metric = UTF-8 serialized bytes;
- non-authoritative handoff snapshots bound to exact source state/repository revision without self-referential commit SHA;
- explicit Codex Cloud admission/reconciliation semantics.

## Traceable Task Decomposition

`docs/tasklist/WB-2026-09-02-orchestrator-execution-state.tasklist.md`

Current structural result: `12 REQ / 12 AC / 10 TASK / 0 errors` under the exact current `validate-define-traceability.py` parsing/coverage semantics. Native checkout execution is still required during final verification because the current Chat container cannot resolve GitHub DNS.

## Architecture Separation

### Execution State Plane
Answers: **what is currently true and what transition is legal next?**

- compact and structured;
- one live canonical state per execution root;
- mutable only by validated transitions;
- no raw transcripts or private reasoning.

### Evidence Plane
Answers: **what observable evidence supports state and what happened?**

- stable report/log/artifact references;
- selectively retrieved;
- full history does not remain in default prompt context;
- handoff snapshot is evidence/input, not live authority.

### Engineering Memory Plane
Answers: **what durable reusable engineering lesson should change future Work Blocks?**

Existing Learning Review remains authoritative. Execution state must not become a second Engineering Memory system.

## Final Define Write-Set

Coordination artifacts below may be written while source remains blocked. Source implementation may begin only after Define/Critic resolves.

```text
# Define / coordination / evidence
docs/plans/WB-2026-09-02-orchestrator-execution-state.md
docs/specs/WB-2026-09-02-orchestrator-execution-state.md
docs/tasklist/WB-2026-09-02-orchestrator-execution-state.tasklist.md
docs/reports/requirements/WB-2026-09-02-orchestrator-execution-state-requirements-review.md
docs/reports/requirements/WB-2026-09-02-orchestrator-execution-state-traceability.md
docs/reports/requirements/WB-2026-09-02-orchestrator-execution-state-consistency-analysis.md
docs/reports/reviews/WB-2026-09-02-orchestrator-execution-state-critic.md
docs/reports/integrations/codex-cloud.md
docs/reports/reviews/WB-2026-09-02-orchestrator-execution-state.md
docs/reports/verification/WB-2026-09-02-orchestrator-execution-state.md
docs/reports/verification/WB-2026-09-02-orchestrator-execution-state-evaluation.md
docs/reports/drift/WB-2026-09-02-orchestrator-execution-state.md
docs/reports/closeout/WB-2026-09-02-orchestrator-execution-state.md
docs/engineering-memory/lessons-learned.md

# Normative/runtime contract
governance/execution-state.md
governance/lifecycle.md
governance/define-quality.md
governance/evaluation.md
framework/memory/project-engineering-memory.md
.agent/workflows/sdd-protocol.md
template/.agent/workflows/sdd-protocol.md
template/docs/session-bootstrap.md
docs/mcp-tool-policy.md
runtimes/codex/README.md
runtimes/opencode/README.md

# Canonical state + generic reducer
template/.agent/active-work-block.default.json
template/.agent/active-work-block.json
template/scripts/work-block-state.py
template/scripts/validate-installation-profile.py

# Runtime readers/wrappers
template/.codex/scripts/lifecycle.py
template/.codex/scripts/doctor.py
template/.codex/hooks/pre_tool_use_policy.py
template/.codex/write-gate.md
template/.claude/hooks/work_block_gate.py
template/.claude/hooks/assurance_gate.py

# Deterministic tests/evaluation
scripts/test-work-block-state.py
scripts/evaluate-work-block-state.py
scripts/test-codex-control-plane.py
scripts/test-codex-adapter.py
scripts/test-profile-restore.py
scripts/test-runtime-conformance.py
scripts/test-integration-contracts.py
scripts/test-codex-hard-stops.py
scripts/test-integration-admission-evidence.py
scripts/test-sdd-contract.sh

# Navigation / publication parity
PROJECT_MAP.md
FILE_REGISTRY.yml
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
```

No path outside this write-set may be changed without returning to Define.

## Codex Cloud Feasibility Gate
Codex Cloud may be used only as an admitted runtime/worker, never as authority. Before a state-changing dispatch:

1. confirm repository access in the user's Codex Cloud environment;
2. bind task to exact branch/revision;
3. assign one bounded logical role and explicit write-set subset;
4. prohibit protected/default branch mutation and unrelated branch adoption;
5. supply validated handoff snapshot only if active state is needed;
6. record data leaving the current runtime/machine and authentication boundary without secrets;
7. require exact resulting revision/diff/check evidence;
8. reconcile GitHub head/result before updating canonical current state;
9. never infer independent Reviewer/Verifier status from cloud execution alone.

If active state cannot be transported/reconciled safely, Codex Cloud remains read-only for this Work Block.

## Acceptance Criteria
Use AC-001 through AC-012 in the normative specification. No prose-only completion claim supersedes them.

## Evaluation Plan
At minimum:

1. >=50 sequential state transitions;
2. external current/frozen subject replacement after earlier assurance;
3. irrelevant CI/tool noise that must not persist in default compact context;
4. restart/handoff recovery without transcript input;
5. overlapping patches from the same expected state version;
6. state-centric versus history-heavy per-step/cumulative UTF-8 context bytes.

Exact tokenizer counts may be additional evidence if a runtime exposes them. Do not claim unmeasured token savings.

## Risks and Controls
| Risk | Control / Stop Condition |
| --- | --- |
| second state SSOT | one live `.agent/active-work-block.json`; snapshots explicitly import-only |
| compression loses needed fact | stable evidence pointers + selective retrieval; provenance not deleted |
| LLM corrupts state | deterministic allowlisted reducer + CAS + atomic replace |
| patch expands authority | authority fields protected; existing lifecycle/Owner procedures only |
| old reader silently ignores v4 | schema bump; v3 fails closed; migrate coupled readers/tests together |
| handoff commit SHA circularity | bind snapshot to source revision/state digest; containing archive commit is not subject |
| concurrent writers race | expected `state_version` + serialized canonical write |
| Codex Cloud treated as authority/independent assurance | explicit admission + actual isolation classification + GitHub reconciliation |
| paper result over-generalized | framework-specific evaluation with portable byte metric |

## Hard Stops / Exclusions
No production deploy, live DB/data mutation, credential/secret handling, destructive Git, protected/default-branch mutation, client communication, or irreversible publication is authorized by this Work Block.

## Recovery / Rollback
All implementation remains on the isolated feature branch. Revert only Work Block commits through normal reviewed Git history. Do not reset/rewrite unrelated branches, Learning Loop work, or `WB-RELEASE-002` state.

## Execution Log
| Date | Stage | Action / Decision | Evidence | Status |
| --- | --- | --- | --- | --- |
| 2026-09-02 | Define | Owner approved separate branch and Work Block | chat instruction | complete |
| 2026-09-02 | Define | Branch created from exact `main` revision `be988807c38543eb90a728fcb4349bc97dd5695a` | GitHub ref | complete |
| 2026-09-02 | Define | Initial architecture recorded | this plan | complete |
| 2026-09-02 | Define | Existing state/default/lifecycle/guards/bootstrap/runtime surfaces inventoried | repository evidence | complete |
| 2026-09-02 | Define | `define_quality` default/lifecycle drift identified | tracked default vs lifecycle helper | complete |
| 2026-09-02 | Define | Local active-state portability gap identified for cloud/fresh checkouts | bootstrap/restore contract | complete |
| 2026-09-02 | Define | Formal specification created and tightened after requirements self-review | specification + requirements review | complete |
| 2026-09-02 | Define | Traceable tasklist created; exact validator semantics yield 12/12/10/0 | traceability report | complete |
| 2026-09-02 | Define | Final implementation write-set expanded to all identified schema-v4 consumers | this plan/tasklist | complete |
| 2026-09-02 | Define | Consistency analysis | pending | pending |
| 2026-09-02 | Define | Critic | pending | pending |
