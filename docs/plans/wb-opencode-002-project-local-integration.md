---
schema_version: 1
artifact_type: work_block
artifact_id: wb-opencode-002-project-local-integration
work_block_id: WB-OPENCODE-002
status: completed
owner_role: orchestrator
created_at: 2026-08-04
process_level: Managed
governance_profile: Managed
branch: agent/opencode-integration
owner_approval: current explicit Owner instruction to integrate OpenCode in the current project
critic_gate: APPROVE_WITH_CHANGES — corrections incorporated before Execute
write_gate: READY
writer: one Coder, Orchestrator disclosed
dependency: WB-OPENCODE-001 current dirty subject is protected; overlapping test edits are additive-only
---

# WB-OPENCODE-002 — Project-Local OpenCode Integration

Install the already-reviewed OpenCode runtime adapter as an optional,
project-local surface in this framework worktree. Keep the framework's
runtime-neutral Governance Core authoritative and preserve Codex as the
authority-bearing orchestrator. This Work Block does not make OpenCode the
default runtime and does not activate external capabilities.

## Scope

**In scope:**

1. Add root `opencode.json` with root-relative instructions and the validated
   permission baseline from `template/opencode.json`.
2. Add root `.opencode/agents/` with the five validated logical-role agents,
   preserving exact semantic parity with the template surface.
3. Register root OpenCode paths as `runtime_adapter` surfaces in
   `FILE_REGISTRY.yml` and project-local optional runtime surfaces in
   `PROJECT_MAP.md`.
4. Update `README.md` and `SETUP.md` with safe current-project OpenCode usage
   and the live-smoke limitation.
5. Extend the existing runtime/integration contract tests to require root
   surface presence and exact template parity.

## Protected Existing State

The current uncommitted WB-OPENCODE-001 subject remains preserved. Its existing
changes to template OpenCode files, adapter documentation, profile docs, and
test files may only receive additive root-parity assertions and the bounded
Critic-verdict vocabulary correction required by the canonical governance
contract; existing unrelated hunks must not be rewritten or removed.

## Exclusions

- provider, model, authentication, API keys, or user credential configuration;
- MCP servers, plugins, hooks, server mode, or custom tools;
- machine-level OpenCode installation or package changes;
- `bootstrap/profiles.json` or generated-project default/profile changes;
- candidate-kit promotion or changes under `candidate/`;
- OpenCode as an authority-bearing Orchestrator or approval authority;
- live OpenCode smoke, network calls, or provider authentication;
- staging, commit, push, or pull request creation.

## Risk and Topology

- **Risk:** Managed, bounded runtime configuration and navigation change.
- **Side effects:** repository-local files only; no external integration.
- **Data mode:** source/configuration read-write; secrets and live data prohibited.
- **Implementation:** one Coder in this dedicated worktree.
- **Assurance:** independent read-only Reviewer and Verifier sessions.
- **Evaluation:** deterministic contract and parity checks; live runtime smoke is
  deferred and remains `UNVERIFIED` until a separate approved execution.
- **Rollback:** remove only the new root `opencode.json`, root `.opencode/`
  agents, root registry/navigation entries, and additive documentation/tests;
  preserve WB-OPENCODE-001 files and unrelated dirty state.

## Acceptance Checks

```text
python3 scripts/test-runtime-conformance.py
python3 scripts/test-integration-contracts.py
bash scripts/test-sdd-contract.sh
bash scripts/validate-governance.sh
python3 scripts/validate-release-state.py
python3 scripts/validate_publication.py
git diff --check
```

Required assertions:

- root `opencode.json` and five root agents exist;
- root and template OpenCode surfaces have exact byte/semantic parity;
- no provider/model/auth, MCP, plugin, hook, or external-directory activation;
- secret and destructive-command boundaries remain denied;
- current project navigation and registry do not grant runtime authority;
- publication false-positives, if any, are classified rather than marked pass.

## Hard Stops

- scope, authority, risk, or write-set expansion returns to Define;
- any provider, model, credential, MCP, plugin, hook, server, or dependency
  change requires separate Owner approval;
- live runtime smoke requires a separate approved execution and capability record;
- staging, commit, push, and PR creation require separate Owner approval.

## Write-set

```text
opencode.json
.opencode/agents/architect.md
.opencode/agents/critic.md
.opencode/agents/coder.md
.opencode/agents/reviewer.md
.opencode/agents/verifier.md
template/.opencode/agents/critic.md
FILE_REGISTRY.yml
PROJECT_MAP.md
README.md
SETUP.md
scripts/test-runtime-conformance.py
scripts/test-integration-contracts.py
docs/plans/wb-opencode-002-project-local-integration.md
```

## Assurance

- Critic: `APPROVE_WITH_CHANGES`, corrections incorporated.
- Reviewer: required, independent and read-only.
- Verifier: required, independent and read-only.
- Closeout: success only after both assurance verdicts are `READY`; otherwise
  reporting-only with residual risks preserved.

## Stage 0 Addendum — 2026-08-11 Owner-approved replacement candidate

This addendum records the explicit Owner amendment in this session. It returns
the corrected candidate definition to Stage 0 only to resolve the Critic
conditions before the bounded amendment execution; it does not close this Work
Block or create a terminal readiness claim.

### Corrected candidate subject and scope

- Historical candidate `8ec1621dd839137f5888ac99fe7ad5a59a60bff0` contains
  unresolved markers and is not `READY`.
- The corrected replacement candidate is the full commit
  `63f88e3174668a8707445e54807c9cfcb2fbb81c`.
- The adapter bridge scope is limited to these seven pre-existing root mirrors:
  - `.opencode/skills/critic-review/SKILL.md`
  - `.opencode/skills/reviewer/SKILL.md`
  - `.opencode/skills/scoped-coder/SKILL.md`
  - `.opencode/skills/ssot-sync-closeout/SKILL.md`
  - `.opencode/skills/subagent-mission-brief/SKILL.md`
  - `.opencode/skills/task-decomposition/SKILL.md`
  - `.opencode/skills/verifier/SKILL.md`
- The historical root/template configuration parity is limited to
  `opencode.json` and `template/opencode.json` having `skills.paths:
  ["skills"]`. This static parity does **not** claim that `skills.paths`
  discovers any of the seven mirrors.

### Explicit exclusions and remaining limitation

- `.opencode/skills/skill-library-maintenance/**` is excluded.
- All changes introduced after the corrected candidate by `cd79823`,
  `6342296`, and `d90d016` are excluded.
- Live OpenCode discovery and permission-merging behavior remain `UNVERIFIED`.
  A live smoke requires separate Owner approval, a capability record, and a
  separately approved execution; this amendment neither invokes nor authorizes
  it.

### Gate re-resolution

- Critic gate: `APPROVE_WITH_CHANGES`; its replacement-subject, bounded-scope,
  explicit-exclusion, and static-coverage conditions are satisfied by this
  addendum.
- Amendment execution write gate: `READY` for one Coder and the exclusive
  amendment paths below.
- Reviewer and Verifier assurance remains pending and independent. No
  `READY`, completion, or closeout verdict is asserted by this addendum.

### Corrected-candidate and amendment write-set record

The original write-set above remains historical record. The corrected-candidate
path manifest additionally records the seven bridge paths and the configuration
paths listed here; they are evidence of the replacement candidate, not writable
paths for this amendment:

```text
opencode.json
template/opencode.json
.opencode/skills/critic-review/SKILL.md
.opencode/skills/reviewer/SKILL.md
.opencode/skills/scoped-coder/SKILL.md
.opencode/skills/ssot-sync-closeout/SKILL.md
.opencode/skills/subagent-mission-brief/SKILL.md
.opencode/skills/task-decomposition/SKILL.md
.opencode/skills/verifier/SKILL.md
FILE_REGISTRY.yml
```

The exclusive write-set for this amendment execution is exactly:

```text
docs/plans/wb-opencode-002-project-local-integration.md
PROJECT_MAP.md
scripts/test-integration-contracts.py
```

## Final State

- **Stage state:** completed
- **Review gate:** READY
- **Verification verdict:** READY
- **Drift gate:** ALIGNED
- **Closeout mode:** success-closeout
- **Task status:** completed

Live OpenCode discovery and permission-merging behavior remains `UNVERIFIED`;
it was not part of this deterministic closeout and still requires separate Owner
approval and a live capability record.
