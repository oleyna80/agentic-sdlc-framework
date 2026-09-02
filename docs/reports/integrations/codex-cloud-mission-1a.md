---
schema_version: 1
artifact_type: integration_mission_amendment
integration_id: codex-cloud
work_block_id: WB-2026-09-02-orchestrator-execution-state
mission: 1A
status: pending_critic
created_at: 2026-09-02
parent_mission: docs/reports/integrations/codex-cloud.md
scope_amendment: docs/plans/WB-2026-09-02-orchestrator-execution-state-amendment-001.md
---

# Codex Cloud Mission 1A — Schema-v4 reader completion

## Purpose

Mission 1A supersedes only the source-path envelope of Cloud Mission 1 after Mission 1 discovered one omitted active runtime reader. All architecture, hard stops, result-contract rules, and read-only core-oracle rules from `docs/reports/integrations/codex-cloud.md` remain in force.

## Exact Cloud write-set

The worker may modify only:

```text
template/.codex/hooks/pre_tool_use_policy.py
template/.codex/hooks/subagent_context.py
template/.codex/scripts/doctor.py
template/.codex/write-gate.md
template/.claude/hooks/work_block_gate.py
template/.claude/hooks/assurance_gate.py
template/scripts/validate-installation-profile.py
scripts/test-codex-control-plane.py
scripts/test-codex-adapter.py
scripts/test-profile-restore.py
scripts/test-runtime-conformance.py
scripts/test-integration-contracts.py
scripts/test-codex-hard-stops.py
scripts/test-integration-admission-evidence.py
```

Everything else remains read-only.

## Required corrections

1. Complete schema-v4 migration for the listed active Codex/Claude readers, including `subagent_context.py`.
2. Preserve fail-closed authority semantics: schema v3 is not accepted as current active state.
3. Correct `scripts/test-codex-control-plane.py` for the current lifecycle CLI, including the required `--expected-version` argument on `open` and any subsequent exact state-version transitions.
4. Keep `template/scripts/work-block-state.py`, `template/.codex/scripts/lifecycle.py`, the schema-v4 defaults, specification, original tasklist, and core tests read-only.
5. Do not widen scope if another path is discovered; stop and report it.

## Native test matrix

Run:

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

If `PyYAML` is absent, report the affected suites as environment-blocked rather than passing. Do not install dependencies unless normal repository setup explicitly calls for that dependency and installation is allowed by the runtime mission.

## Cloud runtime identity

The authoritative preflight identity is the exact dispatched Git commit SHA plus a clean initial worktree. A Codex Cloud synthetic branch label such as `work` is permitted and is diagnostic only.

## Result contract

Return exact base SHA, local branch label, resulting commit/patch identity, changed-file list, write-set subset confirmation, command exit statuses, failure excerpts, environment/dependency deviations, and confirmation that no protected/default-branch, merge, deploy, release, reset, rebase, force-push, or unrelated Work Block mutation occurred.

A cloud-local commit that is not visible in GitHub remains worker evidence only. The Orchestrator must reconcile an actual GitHub commit/patch before accepting it as current repository state.
