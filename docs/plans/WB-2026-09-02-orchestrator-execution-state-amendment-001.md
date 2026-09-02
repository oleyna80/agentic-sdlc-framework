---
schema_version: 1
artifact_type: work_block_define_amendment
artifact_id: wb-2026-09-02-orchestrator-execution-state-amendment-001
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: define_review
created_at: 2026-09-02
parent_plan: docs/plans/WB-2026-09-02-orchestrator-execution-state.md
requirement: REQ-010
acceptance_criterion: AC-010
task: TASK-005
---

# Define Amendment 001 — Additional schema-v4 runtime reader

## Trigger

Codex Cloud Mission 1 executed from exact base `b801071246eba364af0c552583f0f0cc124f7598` and stopped after discovering an authority-relevant runtime reader that was not present in the round-2 final source write-set:

`template/.codex/hooks/subagent_context.py`

The reader currently requires `schema_version == 3`; therefore it rejects otherwise valid schema-v4 active Work Block state.

The cloud worker did not modify the out-of-scope path. Its local cloud commit `43a2ba2efcb549e22b6d2b7cc14e20fed19fddd6` was not published to GitHub and is not a canonical repository subject.

## Classification

This is a **non-material additive scope correction**, not a new requirement or architecture change.

Existing `REQ-010` already requires schema migration across all authority-relevant state readers/guards, and `AC-010` requires v4 defaults and all authority-relevant readers/writers to agree. The discovered file is therefore already semantically required; only the enumerated TASK-005/source write-set was incomplete.

No change is made to REQ/AC semantics, the schema-v4 state model, reducer design, handoff model, authority boundaries, or assurance model.

## Source Write-Set Delta

Add exactly:

```text
template/.codex/hooks/subagent_context.py
```

This path is added to TASK-005 implementation scope and to the bounded Codex Cloud migration mission. No other source path is added by this amendment.

## Required implementation behavior

`template/.codex/hooks/subagent_context.py` must:

- accept only the current schema-v4 state contract for active state;
- continue requiring `authority_mode=github_capability`;
- fail closed for schema v3, malformed/incomplete v4, or unsupported authority mode;
- expose bounded coordination context only and never synthesize source authority;
- remain consistent with the Codex source gate and current adapter tests.

The coupled in-scope fixture `scripts/test-codex-control-plane.py` must also be corrected to use the schema-v4 lifecycle CLI contract, including required `--expected-version` for `open`.

## Validation evidence required

At minimum rerun:

```bash
python scripts/test-work-block-state.py
python scripts/evaluate-work-block-state.py
python scripts/test-codex-control-plane.py
python scripts/test-codex-adapter.py
python scripts/test-profile-restore.py
python scripts/test-codex-hard-stops.py
python scripts/test-integration-admission-evidence.py
bash scripts/test-sdd-contract.sh
```

Runtime-conformance and integration-contract suites remain required when their declared PyYAML dependency is available. Missing dependency is environment evidence, not a pass.

## Gate

Source implementation of the added path remains BLOCKED until this amendment receives a refreshed consistency result and Critic approval. Coordination artifacts under the existing `docs/plans/**` / `docs/reports/**` coordination authority may be written while the source gate is blocked.
