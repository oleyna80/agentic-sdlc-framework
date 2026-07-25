# Work Block WB-003 — Codex-Native Agents and Executable Gates

## Status

- **Stage:** Close
- **State:** completed
- **Closeout:** success
- **Branch:** `agent/runtime-neutral-control-plane`
- **Governance profile:** Assured
- **Side-effect class:** public repository change
- **Verification tier:** full
- **Parent ADR:** `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`

## Objective

Turn the Codex adapter from policy-only documentation into an executable,
project-scoped runtime integration while preserving the runtime-neutral
Governance Core.

## Delivered Result

A generated project now includes:

- project-scoped Codex custom agents for Architect, Critic, Coder, Reviewer, and
  Verifier;
- current `[agents]` configuration instead of legacy `multi_agent = true`;
- project-local hooks declared in `.codex/hooks.json`;
- a machine-readable, fail-closed active Work Block gate;
- `PreToolUse` enforcement for source-write readiness, expiry, Critic state,
  write-set scope, inspectable patch targets, scoped staging, and selected Hard
  Stop operations;
- `SubagentStart` context carrying bounded role, Work Block, specification,
  write-set, gate, and authority information;
- deterministic Codex-adapter fixture tests and disposable scaffold validation;
- a human-readable compatibility view that no longer acts as the write-gate
  source of truth.

## Normative Inputs

- `governance/authority.md`
- `governance/lifecycle.md`
- `governance/runtime-capabilities.md`
- `template/AGENTS.md`
- `template/.agent/workflows/sdd-protocol.md`
- `runtimes/codex/README.md`

## Implemented Paths

```text
runtimes/codex/README.md
template/.codex/config.toml.template
template/.codex/hooks.json
template/.codex/agents/architect.toml
template/.codex/agents/critic.toml
template/.codex/agents/coder.toml
template/.codex/agents/reviewer.toml
template/.codex/agents/verifier.toml
template/.codex/hooks/pre_tool_use_policy.py
template/.codex/hooks/subagent_context.py
template/.agent/active-work-block.json
template/.codex/write-gate.md
template/scripts/bootstrap.sh
scripts/test-codex-adapter.py
.github/workflows/framework-contracts.yml
```

Related navigation, registry, publication, and portable-contract files were
updated where required.

## Gate Contract

`.agent/active-work-block.json` is the executable gate input. The generated
state is intentionally `BLOCKED`.

Source writes require:

- supported gate schema;
- non-empty Work Block ID;
- approved specification path and revision;
- `write_gate.status: READY`;
- valid, future, timezone-aware expiry;
- resolved required Critic state;
- non-empty approved write-set;
- every source target inside that write-set;
- current `HEAD` matching `base_commit` when a base commit is recorded.

Before READY, only the explicit coordination write-set is permitted so Define
and evidence artifacts can be prepared.

The hook also denies unsupported opaque mutations and selected public, live,
credential, communication, and destructive Bash operations unless their
matching Hard Stop approval is recorded.

## Custom Agent Contract

- The main Codex thread performs the Orchestrator function.
- Architect, Critic, Reviewer, and Verifier default to `read-only`.
- Coder defaults to `workspace-write`, but the Work Block gate and write-set
  remain authoritative.
- Public agent templates do not pin concrete models.
- Model routing remains user/private runtime configuration.
- Agent sandbox defaults are defense in depth; live parent overrides and actual
  isolation must still be recorded.

## Acceptance Criteria

- [x] Legacy top-level `multi_agent = true` is removed.
- [x] `[agents]` uses current Codex keys.
- [x] Five project-scoped custom agents parse as TOML and expose logical roles.
- [x] Hooks JSON parses and registers `PreToolUse` plus `SubagentStart`.
- [x] Hook scripts use the Python standard library only.
- [x] Source writes are denied while the gate is blocked, expired, invalid,
      unresolved, or outside the write-set.
- [x] Approved in-scope `apply_patch` is allowed by fixtures.
- [x] Coordination writes remain possible while the source gate is blocked.
- [x] Dangerous Bash fixtures are denied without matching Hard Stop approval.
- [x] Read-only Bash fixtures remain allowed.
- [x] Subagent context reports Work Block, role, write-set, gate, and authority
      without exposing secrets or hidden reasoning.
- [x] Existing runtime-neutral, governance, and publication tests remain green.
- [x] Disposable generated-project bootstrap includes and validates all Codex
      adapter files.

## Verification Evidence

Current Framework Contracts CI completed successfully and included:

```text
Check syntax                              PASS
Validate runtime-neutral SDLC contracts  PASS
Validate Codex adapter gates              PASS
Validate governance structure            PASS
Validate publication scaffold            PASS
Bootstrap disposable generated project   PASS
```

The Codex fixture suite covers:

- blocked and ready gates;
- expired gates;
- missing specification metadata;
- unresolved Critic state;
- in-scope and out-of-scope patches;
- coordination-only patches;
- explicit and broad staging;
- opaque mutation denial;
- Git push and destructive-operation approvals;
- bounded SubagentStart context.

## Residual Limits

- Project hooks are guardrails, not OS-level security isolation.
- Project-local hooks require project trust and human inspection.
- Parent session permission/sandbox overrides can affect spawned agents.
- Unknown or complex mutation commands may still require stricter runtime or OS
  policy outside this project hook.
- No live infrastructure, data, credential, payment, or client mutation is
  authorized solely by these hooks.
- Concrete model routing remains unvalidated project/user configuration.

## Closeout

WB-003 is complete. The PR remains draft for human review of the combined
WB-001 through WB-003 architectural release. Additional integration migration
should be delivered separately to keep review scope bounded.

## Follow-up

- WB-004 — normalize Claude Code plugin, MCP, OpenCode, and file handoff
  integrations against the adapter contract.
- WB-005 — profile-aware bootstrap and cross-runtime conformance tests.
