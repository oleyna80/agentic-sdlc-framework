---
schema_version: 1
artifact_type: work_block
artifact_id: wb-007-agent-evaluation-trajectory-assurance
status: in_progress
owner_role: orchestrator
work_block_id: wb-007
created_at: 2026-07-26
last_verified: 2026-07-26
---

# WB-007 - Agent Evaluation and Trajectory Assurance

## Objective

Add a runtime-neutral evaluation layer that distinguishes deterministic tests,
output evaluation, and observable trajectory evaluation, then binds required
evaluation evidence to Work Block assurance and successful closeout.

## Expected Final Result

- Governance defines evaluation terminology, authority, evidence, verdicts, and
  fail-closed behavior.
- Deterministic tests remain the primary evidence for deterministic contracts.
- Output evaluation measures the delivered artifact against an approved rubric.
- Trajectory evaluation measures observable actions: tool calls, gate events,
  required checks, retries, side effects, and evidence production.
- Trajectory evaluation never requires hidden reasoning, private chain-of-thought,
  or model-internal scratchpads.
- Evaluation plans and reports have portable machine-readable templates.
- The active Work Block can declare evaluation required or optional and record
  rubric, benchmark revision, report, isolation, status, and verdict.
- Required evaluation must resolve to `READY` before successful closeout.
- LM judges, when used, are identified and reproducible, but cannot be the sole
  evidence for deterministic correctness or open an authority gate by themselves.
- Regression fixtures reject malformed plans, unsupported verdicts, missing
  required evidence, incomplete trajectory events, and false pass claims.
- Navigation, registry, generated-project scaffold, CI, final review, and closeout
  evidence are synchronized.

## Scope

### In Scope

- `governance/evaluation.md` normative contract;
- lifecycle and portable artifact contract updates;
- generated evaluation plan/report templates;
- generated-project evaluation validator;
- active Work Block evaluation assurance state;
- Claude Code closeout-gate enforcement for required evaluation;
- runtime-neutral static/executable regression fixtures;
- installation manifest, publication validation, maps, registry, and CI;
- final review and WB-007 closeout evidence.

### Out of Scope

- collecting or exposing private chain-of-thought;
- production telemetry backends, tracing vendors, or hosted dashboards;
- live model/provider authentication;
- automatic model routing;
- MCP, A2A, plugin, or deployment activation;
- replacing deterministic tests with LM judges;
- merging without explicit Owner approval.

## Evaluation Model

```text
Approved intent and acceptance criteria
  -> deterministic tests for deterministic behavior
  -> output evaluation for artifact quality
  -> observable trajectory evaluation for process compliance
  -> verification synthesis
  -> closeout decision
```

Evaluation is assurance evidence. It does not grant implementation authority,
integration admission, tool access, credentials, deployment permission, or an
exception to Hard Stops.

## Implementation Tasks

1. Define the runtime-neutral evaluation contract and vocabulary.
2. Extend lifecycle and artifact-chain requirements.
3. Add evaluation plan and report templates to generated projects.
4. Add evaluation state to portable blocked-default Work Block data.
5. Implement a generated validator for plan/report/evidence invariants.
6. Enforce required evaluation in the Claude Code assurance closeout gate.
7. Add positive and adversarial evaluation fixtures.
8. Register new paths in installation profiles, maps, and registries.
9. Add evaluation validation to Framework Contracts and publication checks.
10. Open a draft PR, obtain green CI, perform final review/drift/verification,
    and mark Ready for review without merging.

## Assurance Plan

Review:

- evaluation remains separate from authority and verification;
- trajectory evidence contains observable events only;
- deterministic behavior cannot pass solely through an LM judge;
- required evaluation cannot be skipped;
- optional skipped evaluation records a reason;
- unavailable checks are `BLOCKED`, `UNVERIFIED`, or `not_run`, never `pass`;
- report paths remain repository-relative and under `docs/reports/`;
- benchmark and rubric revisions are recorded;
- judge identity, prompt/rubric revision, and isolation are explicit when used;
- success-closeout fails when required evaluation is unresolved.

Verification target:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-evaluation-contracts.py
python scripts/test-bootstrap-profiles.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

## Current State

- **Stage:** Define
- **Stage State:** in_progress
- **Write Gate:** limited to this branch and documented scope
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation Verdict:** PENDING
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
