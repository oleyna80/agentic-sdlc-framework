---
schema_version: 1
artifact_type: work_block
artifact_id: wb-define-001-requirements-quality-traceability
work_block_id: WB-DEFINE-001
status: in_progress
owner_role: orchestrator
created_at: 2026-08-14
last_updated: 2026-08-16
process_level: Standard
governance_profile: Managed
branch: agent/define-quality-pipeline
owner_approval: Owner approved the corrective course on 2026-08-16 after independent assurance
critic_gate: pending
write_gate: BLOCKED
writer: one bounded Coder-equivalent corrective stream after Critic readiness
base_revision: 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
historical_initial_base_revision: 8adf9adcb29dafb3dba9e7ee23bd33f9a392958d
implementation_state: corrective_define_pending_critic
process_deviation: docs/reports/process/wb-define-001-process-deviation.md
---

# WB-DEFINE-001 — Requirements Quality and Traceability Pipeline

## Objective

Strengthen Stage 0 / Define so implementation does not depend on an Architect
noticing every ambiguity or manually maintaining requirement/task coverage.

The framework-native capability contains four functions:

1. bounded requirements clarification before technical planning;
2. reviewer-owned requirements-quality review;
3. stable requirement → acceptance criterion → task traceability;
4. read-only pre-execution consistency analysis.

`converge`-style post-implementation correction remains explicitly deferred
because it overlaps existing Verifier and Specification Drift responsibilities
and needs its own corrective-loop design.

## Provenance

- **Classification:** adapted
- **Primary source:** `github/spec-kit@bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`
- **Research evidence:** `framework/research/spec-kit-benchmark-2026-08-14.md` and `framework/research/spec-kit-clarify-checklist-dry-run-2026-08-14.md`
- **Local delta:** preserve the framework authority/write-gate model; resolve
  repository-discoverable facts without asking Owner; batch independent material
  questions while asking dependent questions sequentially; keep requirements
  review distinct from implementation verification; use explicit IDs and a
  deterministic structural validator.
- **Novelty claim:** none

## Historical Implementation State

The first implementation was completed and frozen on the earlier stacked base,
but independent assurance returned `ASSURANCE NOT READY`. The Managed execution
had also begun while `critic_gate` was still `pending`. That historical sequence
is preserved truthfully in
`docs/reports/process/wb-define-001-process-deviation.md`; no later review may be
relabeled as the missing original pre-execution Critic.

The stack was then synchronized non-destructively, bottom-up, with accepted
current `main`:

```text
main 1474c7c5cf2f2e0e74f17aa493c39ac60fa1d94d
  -> PR #34 head 1b344563ec9aff9eb4e2287a121ee069a08d2978
  -> PR #35 head 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
  -> PR #36 synchronization commit 12d3b53e8eee9017b698f295a2f8236e02ce0a04
```

Each branch was advanced by a true merge commit and fast-forward ref update with
no rebase, force-push, or history rewrite. The synchronized PR #36 child delta no
longer includes root `AGENTS.md`, `template/AGENTS.md`, or
`template/docs/templates/work-block-template.md`; accepted current-main versions
therefore remain authoritative.

## Accepted Current-Main Constraints

Corrective work must preserve the already-merged design from PRs #37, #38, and
#39:

- root and portable `AGENTS.md` stay compact always-on contracts;
- detailed Define procedure belongs in workflows and reusable procedures in
  skills rather than duplicated in `AGENTS.md`;
- generated `CLAUDE.md` remains a thin `@AGENTS.md` import;
- normal reversible development inside an approved Work Block/write-set retains
  the current Git-authority semantics;
- engineering controls must be the simplest sufficient mechanism for the actual
  risk and must not create a parallel authority system without necessity.

## Required Behavior

### Clarification routing

```text
repository/discovery-resolvable fact -> resolve from evidence
reasonable non-material default      -> record explicit assumption
material independent ambiguity       -> ask in a bounded batch
material dependent ambiguity         -> ask sequentially
unresolved blocking ambiguity        -> keep Define BLOCKED
```

### Requirements-quality review

Managed, Assured, and Distributed formal work receives a requirements-quality
verdict before the applicable Critic/write transition. The review checks the
written requirements, not implementation correctness.

### Traceability

Formal non-trivial specifications use stable `REQ-*` and `AC-*` identifiers.
Requirement implementation tasks use stable `TASK-*` identifiers and explicitly
reference the requirements, acceptance criteria, and paths/write-set they deliver.

Enabling, assurance, and documentation tasks may have `req=-` and `ac=-`; they
must not be invented as product requirements and must not satisfy implementation
coverage merely by carrying a requirement reference.

### Pre-execution consistency

The consistency analyzer is read-only. It reports gaps across specification,
architecture/plan, tasks, and write-set and routes remediation to the artifact
that owns the problem. It never silently rewrites approved requirements.

## Independent Assurance Findings and Disposition

| Finding | Status before corrective Execute | Corrective disposition |
| --- | --- | --- |
| P-01 — Managed implementation ran before mandatory Critic | recorded | process deviation and Owner disposition recorded; corrective Critic required before source reopening |
| R-01 — non-requirement task can satisfy implementation coverage | open blocker | count implementation coverage only from `type=requirement` |
| R-02 — required Define readiness is not machine-observable at source gate | open blocker | add one aggregate `define_quality` prerequisite to existing schema/gates; no parallel authority system |
| R-03 — portable Work Block template was truncated | resolved by synchronization | current-main full template wins; do not reintroduce old child version |
| V-01 — adversarial fixture suite is incomplete | open blocker | add explicit cases for every promised structural fail-closed condition including R-01 bypass |
| D-01 — legacy generic Reviewer wording drift | excluded | separate follow-up only if still relevant |

## Corrective Design

### R-01 / V-01 — structural traceability

The validator must construct requirement and acceptance implementation coverage
from `type=requirement` tasks only. Non-requirement task types remain legal with
`req=-` / `ac=-` and cannot satisfy product implementation coverage.

The fixture suite must deterministically exercise at least:

- valid `REQ → AC → requirement TASK` → `READY`;
- orphan requirement;
- orphan acceptance criterion;
- unknown requirement reference;
- unknown acceptance reference;
- duplicate `REQ`, `AC`, and `TASK` IDs as applicable;
- malformed requirement task traceability;
- missing task paths/write-set;
- non-requirement task carrying `REQ/AC` references as the only apparent
  implementation coverage → `BLOCKED`;
- parity between framework and generated-project validator implementations.

### R-02 — aggregate executable Define readiness

Use the existing schema-v3 Work Block state and existing source guards. Add one
aggregate evidence prerequisite rather than three new authority-bearing gates.
Conceptually:

```json
"define_quality": {
  "required": true,
  "status": "PENDING",
  "requirements_review": "",
  "traceability": "",
  "consistency_analysis": ""
}
```

For profiles/work where this prerequisite is required, a source write must fail
closed unless `define_quality.status == "READY"` and the required evidence
references are present. This check precedes the existing Critic/write-set
acceptance path. `define_quality` is evidence state only: it grants no source,
integration, credential, deployment, publication, or Hard Stop authority.

Controlled/Quick/NDR behavior must remain proportional to their existing
contracts; the corrective implementation must not accidentally make the formal
Define-quality ceremony universal when governance does not require it.

The default generated Work Block remains fail-closed. The tracked default and any
tracked template compatibility copy must remain semantically aligned so bootstrap
cannot restore a weaker state than runtime hooks validate.

### R-03 — inherited resolution

No corrective edit is planned to
`template/docs/templates/work-block-template.md`. The synchronized branch inherits
the complete accepted current-main template, including Navigation/Documentation,
Commit/Publication Scope, Execution Log, Closeout, SSOT Sync, and Retrospective.
If a later implementation requires additive Define-quality fields in that
template, that is a material scope decision and must return to Define rather than
silently reintroducing the old truncated variant.

## Corrective Source Write-Set Candidate

The independent Critic must challenge this candidate before the write gate may be
reopened:

```text
scripts/validate-define-traceability.py
template/scripts/validate-define-traceability.py
scripts/test-define-traceability.py
template/.agent/active-work-block.default.json
template/.agent/active-work-block.json
template/.codex/hooks/pre_tool_use_policy.py
template/.claude/hooks/work_block_gate.py
scripts/test-codex-adapter.py
scripts/test-runtime-conformance.py
scripts/test-integration-contracts.py
scripts/test-sdd-contract.sh
```

A path may be removed after Critic inspection if existing tests already provide
sufficient coverage. Adding source/runtime/governance paths outside this list is
a scope expansion and returns to Define.

Coordination/evidence paths remain governed separately and may record the Critic,
review, verification, drift, and closeout evidence without granting source-write
authority.

## Corrective Acceptance Criteria

1. `type=assurance`, `type=enabling`, or `type=documentation` cannot satisfy
   implementation coverage for a `REQ` or `AC`.
2. Every structural failure class promised by the Work Block has an explicit
   adversarial fixture, including the R-01 bypass.
3. Framework and generated traceability validators remain byte-identical or use
   one demonstrably canonical implementation without creating a second divergent
   source.
4. Formal Define-quality readiness is machine-observable through one aggregate
   prerequisite in the existing Work Block state and fails closed in applicable
   source guards.
5. The aggregate prerequisite remains evidence-only and does not create a new
   authority role, lifecycle, constitution, Hard Stop exception, or write
   permission.
6. Controlled/Quick/NDR proportional behavior is preserved.
7. The synchronized compact `AGENTS.md` contracts, thin Claude import, Git
   authority semantics, and full Work Block template remain intact.
8. No Spec Kit runtime, `.specify/`, hooks, constitution, lifecycle state, or
   extension system is installed.
9. Full applicable framework CI passes on the new frozen corrective head.
10. Independent Reviewer, Verifier, and Drift assurance pass on that same frozen
    subject before any success-closeout/readiness claim.

## Corrective Verification Plan

- run expanded deterministic traceability fixtures;
- run Codex/Claude source-gate negative tests with required Define-quality state
  absent/PENDING/BLOCKED and positive tests with valid READY evidence;
- verify default Work Block state remains BLOCKED and bootstrap restoration
  preserves the aggregate field;
- run installation-profile/runtime conformance and SDD contracts;
- run release-state and publication contracts;
- bootstrap a disposable generated project and inspect the restored state and
  selected runtime guards;
- inspect the final diff for preservation of PR #37/#38/#39 contracts;
- freeze one exact corrective head for independent Reviewer, Verifier, and Drift.

## Current Gate State

- **Stage:** Define — corrective planning
- **Historical original Critic:** missing; recorded as process deviation, not
  retroactively repaired
- **Corrective Critic:** `PENDING`
- **Source Write Gate:** `BLOCKED`
- **Corrective Execute:** not authorized yet
- **PR:** remains Draft
- **Merge:** not authorized

No source correction may begin until an independent Critic reviews this current
corrective plan and returns an acceptable pre-execution verdict. A Critic verdict
for the corrective plan does not rewrite the history of the original execution.

## Stop Conditions

Return to Define/Owner decision if correction requires:

- a new authority-bearing role or second lifecycle/constitution;
- separate authority-like gates where one aggregate prerequisite is sufficient;
- modification of external capability/Hard Stop semantics;
- changes to accepted compact `AGENTS.md` or thin Claude-import architecture;
- post-implementation auto-remediation;
- unrelated legacy cleanup such as D-01;
- copying upstream protected expression rather than adapting concepts.
