---
schema_version: 1
artifact_type: work_block_define_amendment
artifact_id: wb-2026-09-02-orchestrator-execution-state-amendment-002
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: define_review
created_at: 2026-09-02
parent_plan: docs/plans/WB-2026-09-02-orchestrator-execution-state.md
requirement: REQ-010
acceptance_criterion: AC-010
task: TASK-005
implementation_checkpoint: 7d96b07ba70cc5ef693bfb50cdde164f67d33847
---

# Define Amendment 002 — Evaluation closeout schema-v4 reader

## Trigger

Bounded local Coder continuation on exact implementation baseline `b45e3c5b1c0de48dd92aa037cd5ef17fbb047606` completed the authorized 14-file schema-v4 reader/fixture migration and published checkpoint commit:

`7d96b07ba70cc5ef693bfb50cdde164f67d33847`

All required native tests passed except `python scripts/test-integration-contracts.py`. The failing integration fixture identified a current active Work Block schema consumer outside the effective TASK-005 source write-set:

`template/scripts/validate-evaluation.py`

Repository inspection confirms that this file declares `ACTIVE_WORK_BLOCK_SCHEMA_VERSION = 3` and that its closeout validator rejects any active Work Block state whose schema version differs from that constant.

The local Coder did not modify the out-of-scope path and stopped as required.

## Classification

This is a **non-material additive scope correction** under existing `REQ-010` / `AC-010`, not a new requirement, architecture change, or authority expansion.

`REQ-010` already requires consistent schema migration across current authority-relevant state readers/writers and regression consumers. `validate-evaluation.py` is a current closeout/evaluation consumer of `.agent/active-work-block.json`; leaving it on v3 causes otherwise valid v4 state to fail integration-contract validation.

No change is made to:

- schema-v4 state semantics;
- lifecycle authority;
- evaluation verdict semantics;
- reducer design;
- handoff/snapshot authority attenuation;
- assurance independence;
- Hard Stops;
- Owner authority.

## Effective TASK-005 scope

TASK-005 is amended to include both runtime-discovered readers:

```text
template/.codex/hooks/subagent_context.py
template/scripts/validate-evaluation.py
```

Amendment 001 already authorized `subagent_context.py`. Amendment 002 adds exactly:

```text
template/scripts/validate-evaluation.py
```

The canonical tasklist is updated so final traceability reflects the effective discovered migration surface rather than relying on narrative exception history.

## Required implementation behavior

`template/scripts/validate-evaluation.py` must:

- validate active Work Block closeout state against schema version 4;
- continue requiring `authority_mode=github_capability`;
- fail closed for schema v3, malformed/incomplete v4, or unsupported authority mode;
- preserve existing evaluation-plan/report/closeout semantics;
- not create a second state schema or weaken assurance/closeout requirements.

The change should be minimal unless native tests demonstrate another directly coupled v4 fixture adjustment inside the already effective TASK-005/test write-set.

## Required verification after implementation

Rerun the complete bounded migration matrix:

```bash
python scripts/test-work-block-state.py
python scripts/evaluate-work-block-state.py
python scripts/test-codex-control-plane.py
python scripts/test-codex-adapter.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-codex-hard-stops.py
python scripts/test-integration-admission-evidence.py
bash scripts/test-sdd-contract.sh
git diff --check
```

PyYAML was confirmed available in the local execution environment; runtime-conformance and integration-contract suites therefore require actual passing results rather than environment-blocked classification.

## Checkpoint evidence

GitHub reconciliation of `b45e3c5b1c0de48dd92aa037cd5ef17fbb047606..7d96b07ba70cc5ef693bfb50cdde164f67d33847` shows:

- status: ahead;
- ahead by exactly 1 commit;
- behind by 0;
- merge-base equals the dispatched base;
- exactly the 14 authorized Mission 1A files changed;
- no unrelated ancestry or source-path leakage.

The checkpoint remains implementation evidence, not assurance READY.

## Gate

Source mutation of `template/scripts/validate-evaluation.py` remains BLOCKED until this amendment receives a refreshed consistency analysis and Critic approval. Coordination artifacts may proceed under existing Work Block coordination authority.
