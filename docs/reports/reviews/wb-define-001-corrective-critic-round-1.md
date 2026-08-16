---
schema_version: 1
artifact_type: critic_report
artifact_id: wb-define-001-corrective-critic-round-1
work_block_id: WB-DEFINE-001
reviewed_stage: corrective_define_pre_execution
reviewed_base: 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
reviewed_head: 9492bad041cb56ed968477e587e38b9e57c8a239
subject_integrity: EXACT
verdict: SUPPLEMENT
created_at: 2026-08-16
---

# Corrective Critic — WB-DEFINE-001 — Round 1

## Boundary

This is a read-only pre-execution Critic of the corrective Define plan for
WB-DEFINE-001. It is not a retrospective replacement for the missing Critic on
the original Managed execution, and it does not make that historical execution
conformant.

The reviewed PR #36 subject was exact at both the opening and final integrity
checks:

```text
base: 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
head: 9492bad041cb56ed968477e587e38b9e57c8a239
```

PR #36 remained Draft, open, and unmerged.

## Verdict

**SUPPLEMENT.**

The target architecture is accepted: one aggregate `define_quality` evidence
prerequisite inside the existing schema-v3 Work Block state is the simplest
sufficient design. No second lifecycle, authority role, constitution, or
parallel gate system is required.

The Source Write Gate may **not** reopen on the reviewed plan because the plan's
machine contract and candidate write-set were incomplete.

## Findings

| ID | Severity | Area | Finding | Required correction |
| --- | --- | --- | --- | --- |
| C-01 | MATERIAL | R-02 applicability | Mutable `define_quality.required` cannot independently decide whether Managed/Assured/Distributed work is subject to the prerequisite. | Derive mandatory applicability fail-closed from `governance_profile`; `required=false` cannot bypass Managed/Assured/Distributed. |
| C-02 | MATERIAL | R-02 restore | The candidate write-set omitted canonical default validation and restore regression coverage. | Add `template/scripts/validate-installation-profile.py` and `scripts/test-profile-restore.py`. |
| C-03 | MATERIAL | R-02 durable semantics | Exact aggregate JSON semantics, applicability, and migration were not defined in canonical governance. | Additive update to `governance/define-quality.md`. |
| C-04 | MATERIAL | R-02 portable state | The full portable Work Block template lacked a durable mapping for the aggregate prerequisite and evidence refs. | Add only an additive Define-quality section to the complete current-main `template/docs/templates/work-block-template.md`. |
| C-05 | MATERIAL | R-02 runtime neutrality | Universal machine interception cannot be claimed because OpenCode/generic do not provide the same source-write hook capability as Codex/Claude. | Keep one runtime-neutral semantic requirement; require fail-closed technical denial only where an adapter has interception, and truthful degraded/process semantics otherwise. |
| C-06 | MATERIAL | R-02 evidence | `status=READY` alone is insufficient because mutable state could carry no evidence binding. | When applicable, require READY plus non-empty `requirements_review`, `traceability`, and `consistency_analysis`. |
| C-07 | MATERIAL | R-01 | Implementation coverage currently can be contributed by non-requirement tasks. | Only `type=requirement` contributes to REQ/AC implementation coverage; all task types still validate any references they carry. |
| C-08 | MATERIAL | V-01 | Existing executable fixtures do not cover the full promised adversarial matrix. | Add explicit deterministic fixtures for every promised class, including non-requirement coverage bypass, unknown AC, duplicates, and missing paths. |
| C-09 | INFO | P-01 | Historical process-deviation disposition is correct. | Preserve history; do not record a retrospective original Critic READY. |

## Accepted R-02 Architecture

### Applicability

```text
Managed / Assured / Distributed -> Define-quality prerequisite mandatory
Controlled                       -> selected proportionally by risk/work mode
Quick Fix / NDR                  -> normally not required unless explicitly escalated
```

For Managed/Assured/Distributed, mutable `required=false` is a contradiction,
not a bypass. Missing or malformed aggregate state remains unresolved and source
execution is denied where technical interception exists.

### Aggregate shape

The blank Controlled default should use:

```json
"define_quality": {
  "required": false,
  "status": "PENDING",
  "requirements_review": "",
  "traceability": "",
  "consistency_analysis": ""
}
```

When the prerequisite is applicable, readiness requires:

```text
status == READY
AND requirements_review is non-empty
AND traceability is non-empty
AND consistency_analysis is non-empty
```

The hot-path source guard does not need to parse or semantically revalidate the
referenced reports; non-empty evidence binding is sufficient there.

### Schema and migration

Keep `schema_version: 3`. The aggregate is an additive evidence prerequisite,
not a new authority model.

Fail-closed migration semantics:

- new generated schema-v3 defaults contain `define_quality`;
- malformed `define_quality` -> BLOCKED;
- Managed/Assured/Distributed with missing aggregate -> BLOCKED / migration required;
- missing aggregate is never inferred as READY;
- restored/local active state remains operational and subordinate to the tracked
  default contract.

### Canonical state and runtime semantics

`template/.agent/active-work-block.default.json` is the canonical portable
tracked default. The template repository currently also carries
`template/.agent/active-work-block.json`; both must remain byte/semantically
aligned because the scaffold copies the template before bootstrap restoration.
The active copy must not become a second SSOT.

Formal source execution is not authorized until applicable Define-quality is
READY. Runtime adapters with source-write interception must deny writes
fail-closed. Runtimes without interception must report that limitation and must
not claim machine-enforced prevention. This Work Block must not introduce a new
OpenCode/generic universal hook system.

## R-01 and V-01 Decisions

Implementation coverage is contributed only by `type=requirement` tasks.
Enabling, assurance, and documentation tasks may carry REQ/AC references when
meaningful, but such references never satisfy implementation coverage. Unknown
REQ/AC references are still invalid for any task type that carries them.

Required deterministic fixture matrix:

- positive READY;
- orphan REQ;
- orphan AC;
- unknown REQ;
- unknown AC;
- duplicate REQ;
- duplicate AC;
- duplicate TASK;
- malformed requirement task;
- missing/empty task paths;
- non-requirement coverage bypass;
- framework/template validator parity.

A CLI-level fixture for a physically missing spec/task file is useful but not a
blocking requirement for V-01.

## Approved Supplement to Candidate Write-Set

The previously listed eleven paths remain required. Add these five required
paths before the next Critic:

```text
governance/define-quality.md
template/.agent/workflows/sdd-protocol.md
template/docs/templates/work-block-template.md
template/scripts/validate-installation-profile.py
scripts/test-profile-restore.py
```

`scripts/test-bootstrap-profiles.py` is optional if installation-profile
validation plus restore tests fully demonstrate the canonical default contract.

No changes are required to `AGENTS.md`, `template/AGENTS.md`, `CLAUDE.md`,
`governance/authority.md`, `governance/artifacts.md`, `FILE_REGISTRY.yml`,
`PROJECT_MAP.md`, `template/FILE_REGISTRY.yml`, `template/PROJECT_MAP.md`, or
`bootstrap/profiles.json` for this correction.

## Process Decision

P-01 remains historical truth:

```text
original Managed Execute + critic_gate pending -> material process deviation
```

This round and any later corrective Critic govern only future corrective Execute.

## Handoff

**SOURCE WRITE GATE MAY REOPEN: NO.**

Supplement the corrective Work Block with the accepted applicability rule,
schema-v3 fail-closed migration, evidence binding, runtime capability boundary,
additive full-template mapping, and five missing required paths. Freeze the new
head and run another narrow pre-execution Critic before any source correction.
