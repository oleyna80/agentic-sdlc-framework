---
schema_version: 1
artifact_type: work_block
artifact_id: wb-define-001-requirements-quality-traceability
work_block_id: WB-DEFINE-001
status: completed
owner_role: orchestrator
created_at: 2026-08-14
last_updated: 2026-08-16
process_level: Standard
governance_profile: Managed
branch: agent/define-quality-pipeline
owner_approval: Owner approved the corrective course on 2026-08-16 after independent assurance
critic_gate: READY
corrective_critic_round_1: SUPPLEMENT
corrective_critic_round_2: APPROVE
corrective_critic_round_3: APPROVE
write_gate: BLOCKED
writer: one bounded Coder-equivalent corrective stream; R-02A source Execute complete and frozen
base_revision: 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
historical_initial_base_revision: 8adf9adcb29dafb3dba9e7ee23bd33f9a392958d
implementation_state: completed_assurance_ready
final_assurance: ASSURANCE_READY
final_assurance_subject: 2075cafdecdb75ac5f747c466abb3c1a5f71c611
final_assurance_report: docs/reports/reviews/wb-define-001-final-reassurance.md
closeout_mode: success-closeout
process_deviation: docs/reports/process/wb-define-001-process-deviation.md
corrective_critic_round_1_report: docs/reports/reviews/wb-define-001-corrective-critic-round-1.md
corrective_critic_round_2_report: docs/reports/reviews/wb-define-001-corrective-critic-round-2.md
corrective_critic_round_3_report: docs/reports/reviews/wb-define-001-corrective-critic-round-3.md
corrective_implementation_report: docs/reports/implementation/wb-define-001-corrective-execute.md
corrective_r02a_implementation_report: docs/reports/implementation/wb-define-001-corrective-r02a.md
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
versions therefore remain authoritative. The old truncated Work Block template
was removed from the synchronized child delta before the corrective Define round.

## Accepted Current-Main Constraints

Corrective work preserves the already-merged design from PRs #37, #38, and #39:

- root and portable `AGENTS.md` stay compact always-on contracts;
- detailed Define procedure belongs in workflows and reusable procedures in
  skills rather than duplicated in `AGENTS.md`;
- generated `CLAUDE.md` remains a thin `@AGENTS.md` import;
- normal reversible development inside an approved Work Block/write-set retains
  the current Git-authority semantics;
- engineering controls use the simplest sufficient mechanism for the actual risk
  and do not create a parallel authority system without necessity.

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
Any REQ/AC references they do carry remain subject to unknown-reference
validation.

### Pre-execution consistency

The consistency analyzer is read-only. It reports gaps across specification,
architecture/plan, tasks, and write-set and routes remediation to the artifact
that owns the problem. It never silently rewrites approved requirements.

## Independent Assurance Findings and Corrective Disposition

| Finding | Current status | Corrective disposition |
| --- | --- | --- |
| P-01 — Managed implementation ran before mandatory Critic | historical deviation recorded | Owner disposition preserved; later corrective Critics govern only future corrective Execute and do not rewrite history |
| R-01 — non-requirement task can satisfy implementation coverage | resolved | coverage now comes only from `type=requirement`; all carried refs still receive structural validation |
| R-02 — required Define readiness is not machine-observable at source gate | resolved | aggregate schema-v3 prerequisite, evidence binding, restore validation, and capability-aware interception remain; Round 3 closes the malformed/missing governance-profile applicability bypass |
| R-02A — malformed/missing governance profile can fail open | resolved | raw profile is type-checked, trimmed, validated against canonical enum, Advisory source writes denied, then applicability derived |
| R-03 — portable Work Block template was truncated | resolved | synchronized full current-main template preserved; only additive Define-quality mapping added |
| V-01 — adversarial fixture suite is incomplete | resolved | complete required deterministic matrix added, including R-01 bypass |
| D-01 — legacy generic Reviewer wording drift | excluded | separate follow-up only if still relevant |

Corrective Critic round 1 reviewed exact head
`9492bad041cb56ed968477e587e38b9e57c8a239` and returned `SUPPLEMENT`.

Corrective Critic round 2 reviewed the supplemented exact head
`b48ca1e805ac9201e77b20d2a28eb7678f133691`, resolved C-01 through C-08, returned
`APPROVE`, and explicitly authorized reopening the existing Source Write Gate for
exactly the sixteen corrective source paths below. Round 2 did not establish final
PR readiness.

Final independent assurance of head
`3bde7e76365ee307bfdc463e623bf26f96f40524` found one remaining MATERIAL issue,
R-02A: both source guards could treat missing, malformed, or unknown
`governance_profile` as non-formal and therefore make Define-quality
non-applicable.

Corrective Critic round 3 reviewed that exact head, accepted the narrow repair,
and returned `SOURCE WRITE GATE MAY REOPEN: YES` for exactly four source paths.

Reports:

```text
docs/reports/reviews/wb-define-001-corrective-critic-round-1.md
docs/reports/reviews/wb-define-001-corrective-critic-round-2.md
docs/reports/reviews/wb-define-001-corrective-critic-round-3.md
```

## Corrective Design — Implemented Subject

### R-01 / V-01 — structural traceability

The validator validates syntax, paths, duplicate IDs, and unknown references for
all task types that carry those fields. It constructs requirement and acceptance
**implementation coverage only from `type=requirement` tasks**.

The deterministic fixture suite covers:

- valid `REQ → AC → requirement TASK` → `READY`;
- orphan requirement;
- orphan acceptance criterion;
- unknown requirement reference;
- unknown acceptance reference;
- duplicate `REQ`, `AC`, and `TASK` IDs;
- malformed requirement task traceability;
- missing/empty task paths/write-set;
- non-requirement task carrying `REQ/AC` references as the only apparent
  implementation coverage → `BLOCKED`;
- unknown refs on non-requirement tasks;
- honest non-requirement tasks with no fake IDs;
- byte-for-byte parity between framework and generated-project validators.

A CLI-level fixture for a physically missing spec/task file remains optional
because the validator already has a fail-closed `UNVERIFIED` missing-input path.

### R-02 — one aggregate executable Define-quality prerequisite

The existing schema-v3 Work Block state contains one aggregate evidence
prerequisite rather than separate requirements, traceability, or consistency
authority gates:

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

#### Governance profile validation and applicability derivation

Before Define-quality applicability is derived at the Codex/Claude source-write
boundary, the raw `governance_profile` must be an actual string, must remain
non-blank after trimming, and must belong to the canonical enum:

```text
Advisory | Controlled | Managed | Assured | Distributed
```

Missing, blank, whitespace-only, non-string, or unknown/typo values are unresolved
and deny source writes. `Advisory` is valid governance but read-only, so source
writes are denied explicitly.

After that validation:

```text
Managed / Assured / Distributed -> define_quality REQUIRED
Controlled                       -> proportional risk/work-mode selection
Advisory                         -> source writes denied
Quick Fix / NDR                  -> represented through the existing narrower governance path; not new profile values
```

For Managed/Assured/Distributed, mutable `define_quality.required=false` is a
configuration contradiction and cannot disable the prerequisite. Missing or
malformed applicable `define_quality` is unresolved and cannot be inferred as
success.

#### Readiness evidence

When applicable, source execution requires all four conditions:

```text
define_quality.status == READY
trim(requirements_review) != ""
trim(traceability) != ""
trim(consistency_analysis) != ""
```

The hot-path source guard checks evidence binding without recursively opening or
semantically revalidating the reports. Dedicated validators plus Reviewer,
Verifier, and Drift remain responsible for deeper evidence quality.

The aggregate is evidence state only. It grants no source, Git, integration,
credential, deployment, publication, external-action, or Hard Stop authority.
After it is READY, the existing Critic → Write Gate → write-set path remains fully
applicable.

#### Schema-v3 additive migration

No schema-v4 bump was introduced. `define_quality` is an additive prerequisite
inside the existing schema-v3 source-control model and does not change authority
mode, lifecycle, roles, or Hard Stops.

Migration is fail-closed:

- new generated schema-v3 defaults contain `define_quality`;
- malformed `define_quality` → blocked;
- Managed/Assured/Distributed with a missing aggregate → blocked / migration
  required;
- missing aggregate is never treated as `READY`;
- local/restored active state may be restored only after canonical default
  validation.

#### Canonical and restored state

`template/.agent/active-work-block.default.json` remains the canonical portable
tracked default. `template/.agent/active-work-block.json` remains an aligned
scaffold compatibility copy and not a second SSOT. The two template copies remain
byte-identical after the corrective implementation.

`template/scripts/validate-installation-profile.py` validates the canonical
Controlled/PENDING aggregate before restoration. `scripts/test-profile-restore.py`
proves valid parity/restore and fail-closed behavior for missing, malformed, READY,
prebound, or otherwise non-canonical defaults.

#### Runtime-neutral policy versus technical interception

The semantic rule is runtime-neutral:

> Formal source execution is not authorized until applicable Define-quality is
> READY with the required evidence binding.

Technical enforcement remains capability-aware:

- Codex/Claude adapters that already intercept source writes deny them fail-closed
  until the applicable aggregate is ready;
- OpenCode/generic runtimes without equivalent interception retain truthful
  capability limitations and do not claim machine-enforced prevention;
- no universal OpenCode/generic hook framework was added merely for symmetry.

### R-03 — full-template additive mapping

The corrective implementation added only one aggregate Define-quality section to
the complete current-main `template/docs/templates/work-block-template.md`:

```text
Define Quality Prerequisite
- Required
- Status
- Requirements Review Evidence
- Traceability Evidence
- Consistency Analysis Evidence
```

The complete Navigation/Documentation Impact, Commit/Publication Scope, Execution
Log, Closeout, SSOT Sync, Retrospective, and other current-main sections remain
present.

### Governance and procedure surfaces

`governance/define-quality.md` owns the aggregate shape, profile-derived
applicability, evidence requirements, schema-v3 migration, traceability coverage,
and runtime-capability boundary.

`template/.agent/workflows/sdd-protocol.md` routes applicable aggregate readiness
before Critic and the existing Write Gate while retaining runtime-neutral
capability semantics.

No Round-3 corrective changes were required to governance/schema/default/restore
surfaces because their normative semantics were already correct. No corrective
changes were made to:

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

## Corrective Source Write-Sets — Approved and Executed

Round 2 approved exactly these sixteen source paths, and its corrective Execute
used all and only these paths:

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

Implementation evidence:
`docs/reports/implementation/wb-define-001-corrective-execute.md`.

Round 3 approved and executed exactly four source paths for R-02A:

```text
template/.codex/hooks/pre_tool_use_policy.py
template/.claude/hooks/work_block_gate.py
scripts/test-codex-adapter.py
scripts/test-integration-contracts.py
```

No fifth Round-3 source path was introduced.

Round-3 implementation evidence:
`docs/reports/implementation/wb-define-001-corrective-r02a.md`.

## Corrective Acceptance Criteria

1. `type=assurance`, `type=enabling`, or `type=documentation` cannot satisfy
   implementation coverage for a `REQ` or `AC`.
2. Unknown REQ/AC references remain invalid for any task type that carries them.
3. Every structural failure class promised by the Work Block has an explicit
   adversarial fixture, including unknown AC, duplicate REQ/AC/TASK, missing
   paths, and the R-01 non-requirement bypass.
4. Framework and generated traceability validators remain byte-identical.
5. Formal Define-quality readiness is machine-observable through one aggregate
   schema-v3 prerequisite.
6. The source-write guards fail closed on missing, blank, malformed/non-string,
   or unknown `governance_profile`; `Advisory` cannot source-write; Controlled
   remains proportional; Managed/Assured/Distributed cannot disable applicability
   with mutable `required=false`.
7. Applicable readiness requires READY plus all three trimmed non-empty evidence
   refs.
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
15. Full applicable framework CI passes on the frozen corrected subject.
16. Independent Reviewer, Verifier, and Drift assurance pass on that same frozen
    subject before any success-closeout/readiness claim.

Acceptance criteria 1–16 are satisfied by final independent assurance of exact
normative subject `2075cafdecdb75ac5f747c466abb3c1a5f71c611`: Reviewer `READY`,
Verifier `READY`, and Specification Drift `ALIGNED`.

## Corrective Verification Evidence

The Round-2 corrective source implementation head
`28d24f05619be045d152b2f54a87639d91c25329` passed:

- Release State Contract #782 — `success`;
- Framework Contracts #1200 — `success`.

The prior coordination-complete head
`3bde7e76365ee307bfdc463e623bf26f96f40524` passed:

- Release State Contract #786 — `success`;
- Framework Contracts #1204 — `success`.

The Round-3 R-02A source implementation head
`b2f4b08c24c4b571f21c8bce4caed859611ad67b` passed:

- Release State Contract #796 — `success`;
- Framework Contracts #1214 — `success`.

Framework Contracts #1214 passed runtime-neutral SDD contracts, evaluation/NDR
contracts, installation profiles and runtime conformance, integration adapters,
Codex adapter gates, governance validation, release-state validation, publication
validation, disposable generated-project bootstrap, and provider snapshot. The
new Codex and Claude governance-profile regression matrices therefore executed in
the authoritative suite.

The final assured normative subject
`2075cafdecdb75ac5f747c466abb3c1a5f71c611` passed Release State Contract #800
and Framework Contracts #1218. Final independent re-assurance of that same subject
returned Reviewer `READY`, Verifier `READY`, Specification Drift `ALIGNED`, and
overall `ASSURANCE READY`; evidence is recorded in
`docs/reports/reviews/wb-define-001-final-reassurance.md`.

## Final State

- **Stage State:** completed
- **Write Gate:** CLOSED — source implementation remains blocked after the final freeze
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic framework contracts and executable fixtures were sufficient; no non-deterministic output evaluation was required
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
- **Assured Normative Subject:** `2075cafdecdb75ac5f747c466abb3c1a5f71c611`
- **Final Assurance:** `docs/reports/reviews/wb-define-001-final-reassurance.md`
- **Historical Process Deviation:** P-01 remains recorded in `docs/reports/process/wb-define-001-process-deviation.md`; successful corrective closeout does not retroactively make the original Managed Execute governance-conformant
- **PR State Boundary:** repository closeout does not authorize merge; PR #36 remains subject to separate Owner merge authority

## Stop Conditions

Return to Define/Owner decision if further correction requires:

- a new authority-bearing role or second lifecycle/constitution;
- separate authority-like gates where one aggregate prerequisite is sufficient;
- treating mutable `required=false` as a bypass for Managed/Assured/Distributed;
- accepting missing/malformed/unknown governance profile as a source-write path;
- allowing Advisory source implementation;
- universal runtime-hook machinery solely to simulate interception where the
  runtime lacks it;
- modification of external capability/Hard Stop semantics;
- changes to accepted compact `AGENTS.md` or thin Claude-import architecture;
- replacement/truncation of the current-main Work Block template rather than the
  allowed additive section;
- post-implementation auto-remediation;
- unrelated legacy cleanup such as D-01;
- copying upstream protected expression rather than adapting concepts.
