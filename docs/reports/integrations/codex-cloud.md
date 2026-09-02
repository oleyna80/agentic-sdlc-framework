---
schema_version: 1
artifact_type: integration_admission_and_mission
integration_id: codex-cloud
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: admitted_for_bounded_coder_mission
owner_approval: Owner selected the hybrid execution option and approved Codex Cloud use in chat on 2026-09-02
created_at: 2026-09-02
---

# Codex Cloud Admission + Bounded Coder Mission

## Classification

Codex Cloud is admitted for this Work Block only as a **bounded Coder/native-test worker**.

It is not:

- framework authority;
- an Owner proxy;
- permission to mutate `main` or another Work Block branch;
- independent Reviewer/Verifier merely because execution is remote/cloud-hosted;
- permission to change the approved specification, requirements, architecture, or write-set.

Returned commits, diffs, command output, and test results are worker evidence and MUST be reconciled before the Orchestrator accepts them as current state.

## Mission Objective

Migrate the remaining authority-relevant runtime readers and regression fixtures from active Work Block schema v3 to the accepted schema-v4 Execution State contract, then run repository-native tests and report exact evidence.

The provider-neutral architecture is already selected and partially implemented. Do not redesign it unless a demonstrable blocker makes the approved contract impossible; report such a blocker instead of silently widening scope.

## Required Inputs

At dispatch, the Orchestrator MUST supply:

- repository provenance: `oleyna80/agentic-sdlc-framework`;
- source-branch provenance: `wb/2026-09-02-orchestrator-execution-state` or a dedicated Cloud child branch created from the same exact subject;
- **exact Git commit SHA** containing this mission record;
- specification: `docs/specs/WB-2026-09-02-orchestrator-execution-state.md`;
- tasklist: `docs/tasklist/WB-2026-09-02-orchestrator-execution-state.tasklist.md`;
- Critic approval: `docs/reports/reviews/WB-2026-09-02-orchestrator-execution-state-critic.md`;
- normative state contract: `governance/execution-state.md`;
- provider-neutral engine: `template/scripts/work-block-state.py`;
- core fixtures: `scripts/test-work-block-state.py`;
- synthetic evaluation: `scripts/evaluate-work-block-state.py`.

Do not dispatch from `main`, the Learning Loop subject, `WB-RELEASE-002`, or an unspecified moving branch head.

## Cloud Execution Identity Rule

The **exact dispatched commit SHA is the authoritative repository-subject identity** for this bounded Cloud mission.

Codex Cloud may expose that exact commit through a synthetic local branch name such as `work`, through a task-local branch, or through a detached checkout. The local branch label is therefore diagnostic metadata, not an authority predicate.

A Cloud checkout is acceptable when all of the following are true before implementation starts:

1. `git rev-parse HEAD` equals the exact dispatched SHA;
2. the worktree contains no pre-existing modified, staged, or untracked files attributable to another task;
3. the required mission/spec/core files at that SHA are present and readable;
4. no unrelated commit is introduced before work starts.

A different local branch name **alone** is not a reason to stop when the exact SHA and clean-subject conditions above hold.

The worker MUST NOT checkout, reset, rebase, merge, clean, or otherwise mutate an unrelated workspace merely to manufacture the requested branch label. If the exact HEAD SHA is wrong, STOP and report the mismatch.

A missing Git remote inside the sandbox is not by itself a mission failure. Report it as an environment limitation. Result reconciliation must then rely on the exact returned commit/diff/patch evidence until a resulting commit becomes visible through GitHub or is otherwise imported through a reviewed path.

## Coder Write-Set — Cloud Mission 1

The cloud worker may modify **only** these files:

```text
template/.codex/hooks/pre_tool_use_policy.py
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

Everything else is read-only for this mission, including:

```text
governance/execution-state.md
template/scripts/work-block-state.py
template/.codex/scripts/lifecycle.py
template/.agent/active-work-block.default.json
template/.agent/active-work-block.json
docs/specs/WB-2026-09-02-orchestrator-execution-state.md
docs/tasklist/WB-2026-09-02-orchestrator-execution-state.tasklist.md
docs/plans/WB-2026-09-02-orchestrator-execution-state.md
```

If a required fix needs another file, STOP and report the exact additional path and reason. Do not widen the write-set autonomously.

## Required Behavior

### 1. Schema-v4 readers

Authority-relevant source/assurance readers must reject schema v3 and malformed/incomplete v4 state. They must not treat a v3 active state as usable v4 state.

At minimum update hard-coded schema-version expectations from 3 to 4 and ensure the relevant source/closeout path still fails closed on:

- malformed/unknown governance profile;
- unresolved required Define-quality evidence for Managed/Assured/Distributed;
- BLOCKED write gate;
- missing Work Block/specification identity;
- unresolved required Critic;
- empty/out-of-scope source write-set;
- unresolved required assurance during success closeout.

Do not add a second state schema or provider-specific authority model.

### 2. Default/profile validation

`template/scripts/validate-installation-profile.py` must validate the schema-v4 blocked default consistently with the tracked default/scaffold and reject authority-bearing defaults.

The v4 default must remain:

- `schema_version: 4`;
- `state_version: 0`;
- `authority_mode: github_capability`;
- `governance_profile: Controlled`;
- `define_quality.required: false`, `status: PENDING`;
- `write_gate: BLOCKED`;
- approval/integration-free;
- empty source write-set;
- lifecycle `define/blocked`;
- empty operational subject/progress/context state.

### 3. Regression migration

Migrate fixtures that construct or assert current active Work Block state. Historical reports/plans describing schema v3 are not migration targets.

Tests should explicitly prove that current v3 state is rejected by v4 readers unless the dedicated migration command is used.

### 4. Core oracle

The following new files are read-only mission oracles and MUST pass unchanged:

```bash
python scripts/test-work-block-state.py
python scripts/evaluate-work-block-state.py
```

Do not weaken these tests to accommodate an adapter bug.

### 5. Existing contract suites

Run at least:

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
```

If repository-native discovery shows another directly coupled schema-state test, run it and report it. Do not modify an unrelated file merely to make an unrelated historical wording check pass; report such a failure for Orchestrator classification.

## Hard Stops

Do not:

- push or mutate `main`/protected default branch;
- merge, rebase, force-push, reset, clean an unrelated workspace, or rewrite history;
- adopt commits from Learning Loop or `WB-RELEASE-002`;
- modify files outside the Cloud Mission 1 write-set;
- change spec/requirements/tasklist/architecture;
- weaken fail-closed checks or core tests;
- install new dependencies unless already explicitly required by repository setup;
- access or expose credentials/secrets/live infrastructure/live data;
- create assurance READY verdicts.

A normal commit on the task-local/synthetic Cloud branch is permitted if the Codex Cloud surface supports it. A branch label such as `work` does not itself grant or reduce authority. If the environment returns a patch rather than a commit, report that honestly.

## Result Contract

Return all of the following:

1. exact input/base SHA actually checked out;
2. local branch label (including `work` or detached state) as diagnostic metadata;
3. exact resulting commit SHA, or state explicitly that no commit was created;
4. `git status --short --branch`;
5. `git diff --name-only <input-sha>...HEAD` (or equivalent exact changed-file list);
6. confirmation that every changed path is inside Cloud Mission 1 write-set;
7. commands run and exit status;
8. full list of passing/failing tests;
9. concise failure excerpts for any non-zero test;
10. any additional path/scope needed but not modified;
11. whether a Git remote was available and whether network/dependency setup differed from normal repository execution;
12. no merge/deployment/release/rebase/reset/force-push/protected-branch action performed.

## Reconciliation Rule

The Orchestrator accepts the cloud result only after checking:

```text
reported base SHA == dispatched SHA
starting tree was clean and bound to that SHA
changed paths subset-of Cloud Mission 1 write-set
no unrelated ancestry introduced
native evidence corresponds to the reported resulting subject
```

Branch-name equality is not required for a synthetic Cloud checkout.

If the resulting commit is pushed/visible on GitHub, its reported SHA MUST match GitHub. If no remote/push is available, the result remains worker evidence until the returned commit/diff/patch is imported through a reviewed path; narrative alone does not advance canonical state.

Any identity/evidence mismatch keeps the result `UNVERIFIED`.

## Data Boundary

This is a public repository. The worker may read the repository content required by this mission and send normal task/repository context to the Codex Cloud service. It must not seek local home-directory material, user browser state, secrets, unrelated repositories, private keys, production credentials, or external customer data.

## Rollback / Disable

If the mission fails or returns out-of-scope changes, discard/revert only the cloud worker's feature/task commit through normal reviewed Git history. Do not reset/rewrite the canonical branch. Codex Cloud admission ends with this bounded mission unless a subsequent Work Block/mission record explicitly renews it.
