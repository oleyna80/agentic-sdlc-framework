---
schema_version: 1
artifact_type: critic_report
artifact_id: wb-define-001-corrective-critic-round-2
work_block_id: WB-DEFINE-001
reviewed_stage: corrective_define_pre_execution
reviewed_subject_base: 9d4d50764ca5fee8b03fa5883a95ad89617f1cbf
reviewed_subject_head: b48ca1e805ac9201e77b20d2a28eb7678f133691
subject_integrity: EXACT
verdict: APPROVE
created_at: 2026-08-16
---

# Corrective Critic Round 2 — WB-DEFINE-001

## Subject

Read-only pre-execution Critic re-review of the supplemented corrective Define plan for PR #36.

- base: `9d4d50764ca5fee8b03fa5883a95ad89617f1cbf`
- frozen head: `b48ca1e805ac9201e77b20d2a28eb7678f133691`
- PR state at review: open, Draft, unmerged
- subject integrity: `EXACT`
- Round-1 → Round-2 delta: only the Work Block plan and Round-1 Critic evidence
- Release State Contract #746: success
- Framework Contracts #1164: success

The CI results are deterministic baseline evidence only and do not replace this Critic.

## Verdict

**APPROVE.**

All Round-1 supplements C-01 through C-08 are resolved in the supplemented Define plan. No MATERIAL or blocking Round-2 findings were identified.

The approved target remains one aggregate `define_quality` evidence prerequisite inside the existing schema-v3 Work Block state. It does not create a second lifecycle, authority model, constitution, Write Gate, or authority-bearing role.

## Approved semantics

### Applicability

- Managed / Assured / Distributed: `define_quality` is mandatory by governance profile; mutable `required=false` cannot disable it and is treated as an unresolved/configuration contradiction that fails source execution closed.
- Controlled: applicability remains proportional to risk/work mode.
- Quick Fix / NDR: normally not required unless explicitly escalated by their existing contracts.

### Aggregate readiness

For applicable work, source execution requires all of:

```text
define_quality.status == READY
trim(define_quality.requirements_review) != ""
trim(define_quality.traceability) != ""
trim(define_quality.consistency_analysis) != ""
```

Hot-path guards need only validate the aggregate and non-blank evidence bindings; they should not recursively parse or re-run evidence reports.

### Schema and migration

Keep `schema_version: 3`.

The extension is additive and evidence-only. Migration is fail-closed:

- new generated v3 defaults contain `define_quality`;
- malformed aggregate → blocked;
- Managed / Assured / Distributed with missing aggregate → blocked / migration required;
- missing aggregate never implies READY.

### Canonical state

- `template/.agent/active-work-block.default.json` is the canonical tracked portable default.
- `template/.agent/active-work-block.json` is a scaffold compatibility copy that remains byte/semantically aligned at generation time but is not a second SSOT.
- generated `.agent/active-work-block.json` is local operational state restored from the validated default.

### Runtime boundary

Runtime-neutral semantics require applicable Define-quality readiness before formal source execution.

- Codex and Claude, which have source interception, must deny fail-closed.
- OpenCode/generic runtimes without equivalent interception must truthfully report the capability limitation and must not claim machine-enforced prevention.
- No new universal runtime hook framework is authorized.

### Traceability coverage

All task types receive structural/reference validation. Only `type=requirement` tasks contribute to requirement/acceptance implementation coverage and validate implementation REQ↔AC relationships. Enabling, assurance, and documentation tasks may carry meaningful references but cannot satisfy implementation coverage.

### Required fixture matrix

The corrective implementation must cover:

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

A physical missing-file CLI fixture is optional and non-blocking.

## Approved corrective source write-set

Exactly these sixteen paths are approved:

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

`scripts/test-bootstrap-profiles.py` is optional only if implementation reveals a real coverage gap. It is not part of the authorized default write-set.

No source path outside the sixteen above may be edited without returning to Define.

## Preservation constraints

The corrective Execute must preserve:

- PR #37 compact `AGENTS.md` architecture;
- PR #38 thin Claude `@AGENTS.md` import;
- PR #39 Git-authority semantics;
- one authority model;
- one lifecycle;
- one existing Write Gate;
- separate Critic, Reviewer, Verifier, Drift, Evaluation, and Hard Stop contracts;
- no Spec Kit runtime, `.specify/`, second constitution, or parallel gate system.

The Work Block template change is additive only and must preserve the complete current-main Navigation/Documentation, Commit/Publication Scope, Execution Log, Closeout, SSOT Sync, and Retrospective sections.

## P-01 historical boundary

The original Managed Execute occurred with `critic_gate=pending` and remains a material process deviation. Round 2 governs only future corrective Execute and does not retroactively repair the original execution.

## Gate decision

**SOURCE WRITE GATE MAY REOPEN: YES.**

Preconditions:

1. Record this APPROVE verdict through coordination/evidence state.
2. Reopen the existing Source Write Gate only for the exact sixteen-path write-set.
3. Use one bounded corrective Coder stream.
4. Return to Define before editing any seventeenth non-optional source path.
5. After implementation, close/freeze source mutation, run fresh CI, and obtain independent Reviewer → Verifier → Specification Drift assurance on one exact corrected head.

This Critic does not establish final PR readiness or merge authority.
