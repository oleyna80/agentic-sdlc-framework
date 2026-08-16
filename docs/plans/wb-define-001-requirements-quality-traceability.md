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
corrective_critic_round_1: SUPPLEMENT
write_gate: BLOCKED
writer: one bounded Coder-equivalent corrective stream after Critic readiness
base_revision: 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
historical_initial_base_revision: 8adf9adcb29dafb3dba9e7ee23bd33f9a392958d
implementation_state: corrective_define_supplemented_pending_recritic
process_deviation: docs/reports/process/wb-define-001-process-deviation.md
corrective_critic_round_1_report: docs/reports/reviews/wb-define-001-corrective-critic-round-1.md
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
longer includes root `AGENTS.md` or `template/AGENTS.md`; accepted current-main
versions remain authoritative. The old truncated Work Block template was also
removed from the synchronized child delta before this corrective Define round.

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

Managed, Assured, and Distributed work uses the formal Define-quality path before
the applicable Critic/write transition. Controlled work applies it proportionally
by risk/work mode. Quick Fix/NDR normally do not require the formal aggregate
unless explicitly escalated by the governing contract or Owner decision.

The review checks the written requirements, not implementation correctness.

### Traceability

Formal non-trivial specifications use stable `REQ-*` and `AC-*` identifiers.
Requirement implementation tasks use stable `TASK-*` identifiers and explicitly
reference the requirements, acceptance criteria, and paths/write-set they deliver.

Enabling, assurance, and documentation tasks may have `req=-` and `ac=-`, or may
carry meaningful references, but they must never satisfy implementation coverage.
Any REQ/AC references they do carry are still subject to unknown-reference
validation.

### Pre-execution consistency

The consistency analyzer is read-only. It reports gaps across specification,
architecture/plan, tasks, and write-set and routes remediation to the artifact
that owns the problem. It never silently rewrites approved requirements.

## Independent Assurance Findings and Disposition

| Finding | Status before corrective Execute | Corrective disposition |
| --- | --- | --- |
| P-01 — Managed implementation ran before mandatory Critic | recorded | process deviation and Owner disposition recorded; corrective Critic required before source reopening |
| R-01 — non-requirement task can satisfy implementation coverage | open blocker | count implementation coverage only from `type=requirement`; still validate any references carried by all task types |
| R-02 — required Define readiness is not machine-observable at source gate | open blocker | add one aggregate `define_quality` evidence prerequisite to existing schema/gates with profile-derived applicability and fail-closed migration |
| R-03 — portable Work Block template was truncated | inherited regression resolved | use full current-main template as baseline; only additive Define-quality mapping is now allowed |
| V-01 — adversarial fixture suite is incomplete | open blocker | add explicit cases for every promised structural fail-closed condition including R-01 bypass |
| D-01 — legacy generic Reviewer wording drift | excluded | separate follow-up only if still relevant |

Corrective Critic round 1 reviewed exact head
`9492bad041cb56ed968477e587e38b9e57c8a239` and returned `SUPPLEMENT`. Its
accepted design constraints are recorded in
`docs/reports/reviews/wb-define-001-corrective-critic-round-1.md`.

## Corrective Design

### R-01 / V-01 — structural traceability

The validator must validate syntax, paths, duplicate IDs, and unknown references
for all task types that carry those fields. It must construct requirement and
acceptance **implementation coverage only from `type=requirement` tasks**.

The fixture suite must deterministically exercise at least:

- valid `REQ → AC → requirement TASK` → `READY`;
- orphan requirement;
- orphan acceptance criterion;
- unknown requirement reference;
- unknown acceptance reference;
- duplicate `REQ` ID;
- duplicate `AC` ID;
- duplicate `TASK` ID;
- malformed requirement task traceability;
- missing/empty task paths/write-set;
- non-requirement task carrying `REQ/AC` references as the only apparent
  implementation coverage → `BLOCKED`;
- parity between framework and generated-project validator implementations.

A CLI-level fixture for a physically missing spec/task file is desirable but is
not a blocking V-01 requirement because the validator already has a fail-closed
missing-input path.

### R-02 — one aggregate executable Define-quality prerequisite

Use the existing schema-v3 Work Block state and existing source guards. Do **not**
add separate requirements, traceability, or consistency authority gates.

Canonical aggregate shape:

```json
"define_quality": {
  "required": false,
  "status": "PENDING",
  "requirements_review": "",
  "traceability": "",
  "consistency_analysis": ""
}
```

The blank tracked default remains `governance_profile: Controlled`, therefore its
literal `required` value is `false`. This field is a proportional selector only
where the profile allows that decision; it is not trusted as an authority input
for higher-governance profiles.

#### Applicability derivation

Source guards and canonical validation must derive mandatory applicability
fail-closed from governance state:

```text
Managed / Assured / Distributed -> define_quality REQUIRED
Controlled                       -> use proportional risk/work-mode selection
Quick Fix / NDR                  -> normally NOT REQUIRED unless explicitly escalated
```

For Managed/Assured/Distributed, mutable `define_quality.required=false` is a
configuration contradiction and cannot disable the prerequisite. Missing or
malformed `define_quality` is unresolved and must not be inferred as success.

#### Readiness evidence

When applicable, source execution is not authorized unless all four conditions
hold:

```text
define_quality.status == READY
requirements_review   != ""
traceability           != ""
consistency_analysis   != ""
```

The hot-path source guard need not parse or semantically revalidate each referenced
report. Non-empty evidence binding is sufficient there; the dedicated validators,
Reviewer, Verifier, and Drift process remain responsible for deeper evidence
quality.

The aggregate is evidence state only. It grants no source, Git, integration,
credential, deployment, publication, external-action, or Hard Stop authority.
After it is READY, the existing Critic → Write Gate → write-set path remains fully
applicable.

#### Schema-v3 additive migration

No schema-v4 bump is planned. `define_quality` is an additive prerequisite inside
the existing schema-v3 source-control model and does not change authority mode,
lifecycle, roles, or Hard Stops.

Required migration behavior:

- new generated schema-v3 defaults contain `define_quality`;
- malformed `define_quality` → `BLOCKED`;
- Managed/Assured/Distributed with a missing aggregate → `BLOCKED` / migration
  required;
- missing aggregate is never treated as `READY`;
- local/restored active state may be refreshed from the canonical tracked default,
  but absence of the field never becomes a success path.

#### Canonical and restored state

`template/.agent/active-work-block.default.json` is the canonical portable tracked
default. The template repository also currently contains
`template/.agent/active-work-block.json`, and the scaffold copies the complete
template before bootstrap restoration. Within that existing architecture both
copies must receive the same additive aggregate and remain byte/semantically
aligned. The active copy remains operational compatibility state, not a second
SSOT.

`template/scripts/validate-installation-profile.py` must validate the canonical
default shape before restoration. `scripts/test-profile-restore.py` must prove
that malformed or weaker defaults fail before unsafe restoration and that valid
restore preserves the aggregate contract.

#### Runtime-neutral policy versus technical interception

The semantic rule is runtime-neutral:

> Formal source execution is not authorized until applicable Define-quality is
> READY with the required evidence binding.

Technical enforcement remains capability-aware:

- Codex/Claude adapters that already intercept source writes **must** deny them
  fail-closed until the applicable aggregate is ready;
- OpenCode/generic runtimes without equivalent interception must expose/report
  that limitation and must not claim machine-enforced prevention;
- this Work Block must not create a new universal OpenCode/generic hook framework
  merely to equalize implementation mechanisms.

### R-03 — full-template additive mapping only

Synchronization removed the old truncated Work Block child version. The
corrective implementation now **does require** one additive mapping in the full
current-main `template/docs/templates/work-block-template.md` so durable portable
state can record:

```text
Define Quality Prerequisite
- Required
- Status
- Requirements Review Evidence
- Traceability Evidence
- Consistency Analysis Evidence
```

This is one aggregate prerequisite, not three new gates. The Coder must preserve
the complete current-main template including Navigation/Documentation Impact,
Commit/Publication Scope, Execution Log, Closeout, SSOT Sync, Retrospective, and
all other existing sections. Any deletion/replacement with the historical
truncated variant is forbidden.

### Governance and procedure scope

`governance/define-quality.md` requires an additive machine-contract section for:
aggregate shape, applicability derivation, evidence requirements, schema-v3
migration, and runtime-capability boundary.

`template/.agent/workflows/sdd-protocol.md` requires an additive portable
procedure update reflecting the same semantic prerequisite without expanding
`AGENTS.md`.

No corrective changes are planned to:

```text
AGENTS.md
template/AGENTS.md
CLAUDE.md
governance/authority.md
governance/artifacts.md
FILE_REGISTRY.yml
PROJECT_MAP.md
template/FILE_REGISTRY.yml
template/PROJECT_MAP.md
bootstrap/profiles.json
```

Existing registries/maps already classify Define-quality as evidence-only with no
source-write authority.

## Corrective Source Write-Set — Supplemented Candidate

The next independent pre-execution Critic must review this exact candidate before
the source Write Gate may reopen:

```text
scripts/validate-define-traceability.py
template/scripts/validate-define-traceability.py
scripts/test-define-traceability.py

template/.agent/active-work-block.default.json
template/.agent/active-work-block.json

template/.codex/hooks/pre_tool_use_policy.py
template/.claude/hooks/work_block_gate.py

template/scripts/validate-installation-profile.py
scripts/test-profile-restore.py

scripts/test-codex-adapter.py
scripts/test-runtime-conformance.py
scripts/test-integration-contracts.py
scripts/test-sdd-contract.sh

governance/define-quality.md
template/.agent/workflows/sdd-protocol.md
template/docs/templates/work-block-template.md
```

All sixteen listed paths are **REQUIRED** in the supplemented candidate.

`scripts/test-bootstrap-profiles.py` is explicitly **OPTIONAL** and may be added
only if implementation discovers that installation-profile validation plus
restore tests do not adequately prove aggregate presence across generated
profiles. Adding it for convenience alone is unnecessary.

Any other source/runtime/governance path is a scope expansion and returns to
Define before editing.

Coordination/evidence paths remain governed separately and may record Critic,
review, verification, drift, and closeout evidence without granting source-write
authority.

## Corrective Acceptance Criteria

1. `type=assurance`, `type=enabling`, or `type=documentation` cannot satisfy
   implementation coverage for a `REQ` or `AC`.
2. Unknown REQ/AC references remain invalid for any task type that carries them.
3. Every structural failure class promised by the Work Block has an explicit
   adversarial fixture, including unknown AC, duplicate REQ/AC/TASK, missing
   paths, and the R-01 non-requirement bypass.
4. Framework and generated traceability validators remain byte-identical or use
   one demonstrably canonical implementation without creating a second divergent
   source.
5. Formal Define-quality readiness is machine-observable through one aggregate
   schema-v3 prerequisite.
6. Managed/Assured/Distributed applicability cannot be disabled with mutable
   `required=false`; missing/malformed aggregate state fails closed.
7. Applicable readiness requires READY plus all three non-empty evidence refs.
8. The canonical tracked default is validated before restore, and restoration
   preserves the aggregate without making the active compatibility copy a second
   SSOT.
9. Codex/Claude existing interception guards deny applicable source writes
   fail-closed; OpenCode/generic capability limitations remain truthful without a
   new universal hook architecture.
10. The aggregate prerequisite remains evidence-only and does not create a new
    authority role, lifecycle, constitution, Hard Stop exception, Git capability,
    or write permission.
11. Controlled/Quick/NDR proportional behavior is preserved.
12. The complete current-main Work Block template remains intact with only an
    additive aggregate Define-quality section.
13. The compact `AGENTS.md` contracts, thin Claude import, and PR #39 Git
    authority semantics remain intact.
14. No Spec Kit runtime, `.specify/`, hooks, constitution, lifecycle state, or
    extension system is installed.
15. Full applicable framework CI passes on the new frozen corrective head.
16. Independent Reviewer, Verifier, and Drift assurance pass on that same frozen
    subject before any success-closeout/readiness claim.

## Corrective Verification Plan

- run the complete deterministic traceability fixture matrix;
- run Codex/Claude source-gate negative tests for missing/malformed aggregate,
  Managed `required=false`, PENDING/BLOCKED state, READY-with-empty-evidence, and
  positive READY-with-evidence;
- validate the canonical default before restore and prove restore failure on an
  unsafe default;
- verify `template/.agent/active-work-block.default.json` and template active copy
  remain byte/semantically aligned;
- run profile restore, installation-profile/runtime conformance, integration, and
  SDD contracts;
- run release-state and publication contracts;
- bootstrap disposable generated projects across applicable profiles and inspect
  aggregate presence/restoration plus truthful runtime enforcement capability;
- inspect the Work Block template diff for additive-only preservation of the full
  current-main template;
- inspect the final diff for preservation of PR #37/#38/#39 contracts;
- freeze one exact corrective head for independent Reviewer, Verifier, and Drift.

## Current Gate State

- **Stage:** Define — supplemented corrective planning
- **Historical original Critic:** missing; recorded as process deviation, not
  retroactively repaired
- **Corrective Critic round 1:** `SUPPLEMENT` on exact head
  `9492bad041cb56ed968477e587e38b9e57c8a239`
- **Corrective Critic round 2:** `PENDING`
- **Source Write Gate:** `BLOCKED`
- **Corrective Execute:** not authorized
- **PR:** remains Draft
- **Merge:** not authorized

No source correction may begin until a new independent Critic reviews the
supplemented plan on a newly frozen exact head and returns an acceptable
pre-execution verdict. Any such verdict governs only future corrective Execute
and does not rewrite the history of the original execution.

## Stop Conditions

Return to Define/Owner decision if correction requires:

- a new authority-bearing role or second lifecycle/constitution;
- separate authority-like gates where one aggregate prerequisite is sufficient;
- treating mutable `required=false` as a bypass for Managed/Assured/Distributed;
- universal runtime-hook machinery solely to simulate interception where the
  runtime lacks it;
- modification of external capability/Hard Stop semantics;
- changes to accepted compact `AGENTS.md` or thin Claude-import architecture;
- replacement/truncation of the current-main Work Block template rather than the
  allowed additive section;
- post-implementation auto-remediation;
- unrelated legacy cleanup such as D-01;
- copying upstream protected expression rather than adapting concepts.
