---
schema_version: 1
artifact_type: work_block_define_amendment
artifact_id: wb-2026-09-02-orchestrator-execution-state-amendment-003
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: define_review
created_at: 2026-09-02
parent_plan: docs/plans/WB-2026-09-02-orchestrator-execution-state.md
requirement: REQ-010
acceptance_criterion: AC-010
task: TASK-005
---

# Define Amendment 003 — Installation profile requires execution-state reducer

## Trigger

Post-TASK-005 bootstrap inspection found that `bootstrap/bootstrap_project.py` copies the full `template/` tree, so `template/scripts/work-block-state.py` is physically present in newly scaffolded projects. However, `bootstrap/profiles.json` does not list `scripts/work-block-state.py` in `common_required_paths`.

Generated `.agent/bootstrap-profile.json` therefore does not declare the reducer as required, and `template/scripts/validate-installation-profile.py` validates only the paths declared in that manifest. A generated project can consequently lose `scripts/work-block-state.py`, still pass installation-profile validation, and fail only later when schema-v4 lifecycle code attempts to load the reducer.

## Classification

This is a non-material additive installation-contract correction under existing `REQ-010` / `AC-010`. Schema-v4 lifecycle correctness requires the provider-neutral reducer that current lifecycle/runtime wrappers depend on to be part of the generated installation profile's required-path contract.

No execution-state architecture, authority model, requirement, acceptance criterion, assurance model, handoff semantics, or bootstrap composition algorithm changes.

## Source Write-Set Delta

Add exactly:

```text
bootstrap/profiles.json
```

The already approved coupled fixture `scripts/test-profile-restore.py` may be updated if necessary to prove the required-path contract.

## Required behavior

`bootstrap/profiles.json` must add exactly:

```text
scripts/work-block-state.py
```

to `common_required_paths` in the scripts section, preserving deterministic order and all existing profiles/components.

Generated projects must therefore record the reducer in `.agent/bootstrap-profile.json.required_paths`; installation-profile validation must fail if that required reducer is absent.

Do not change `bootstrap/bootstrap_project.py`: full-template copy behavior already transports the file and does not require redesign.

## Validation

At minimum rerun:

```bash
python3 scripts/test-profile-restore.py
python3 scripts/test-runtime-conformance.py
python3 scripts/test-integration-contracts.py
python3 scripts/test-codex-adapter.py
bash scripts/test-sdd-contract.sh
git diff --check
```

If another source path is required, stop and return to Define rather than widening scope.

## Gate

Mutation of `bootstrap/profiles.json` remains BLOCKED until refreshed consistency analysis and Critic approval for Amendment 003.
