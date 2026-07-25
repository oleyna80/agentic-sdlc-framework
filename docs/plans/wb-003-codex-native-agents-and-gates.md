# Work Block WB-003 — Codex-Native Agents and Executable Gates

## Status

- **Stage:** Define
- **State:** in_progress
- **Branch:** `agent/runtime-neutral-control-plane`
- **Governance profile:** Assured
- **Side-effect class:** public repository change
- **Verification tier:** full
- **Parent ADR:** `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`

## Objective

Turn the Codex adapter from policy-only documentation into an executable,
project-scoped runtime integration while preserving the runtime-neutral
Governance Core.

## Expected Final Result

A generated project includes:

- project-scoped Codex custom agents for Architect, Critic, Coder, Reviewer, and
  Verifier;
- current `[agents]` configuration instead of the legacy `multi_agent = true`;
- project-local Codex hooks discovered from `.codex/hooks.json`;
- a machine-readable active Work Block gate;
- fail-closed checks for source writes, write-set scope, gate expiry, critic
  state, and dangerous Bash actions;
- SubagentStart context that communicates role, Work Block, scope, and authority;
- contract tests and CI checks for the Codex adapter.

## Normative Inputs

- `governance/authority.md`
- `governance/lifecycle.md`
- `governance/runtime-capabilities.md`
- `template/AGENTS.md`
- `template/.agent/workflows/sdd-protocol.md`
- `runtimes/codex/README.md`

## Current Codex Runtime Facts

- Project-scoped custom agents are standalone TOML files under
  `.codex/agents/`.
- Multi-agent settings use `[agents]`; `agents.enabled` defaults to true.
- Custom agents require `name`, `description`, and `developer_instructions` and
  may override normal session keys such as model, reasoning effort, sandbox,
  MCP, and skills.
- Project hooks may be declared in `.codex/hooks.json` or inline config, but one
  representation per layer is preferred.
- `PreToolUse` can inspect and deny Bash, `apply_patch`, MCP, and other local
  function tools.
- Project-local hooks require project trust and explicit hook review.
- Hooks are guardrails, not a complete security boundary.
- Subagents inherit live permission/sandbox overrides from the parent turn, so
  agent-file sandbox defaults must not be treated as absolute isolation.

## In Scope

```text
docs/plans/wb-003-codex-native-agents-and-gates.md
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
bootstrap.sh
scripts/test-codex-adapter.py
scripts/test-sdd-contract.sh
.github/workflows/framework-contracts.yml
PROJECT_MAP.md
FILE_REGISTRY.yml
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
scripts/validate-publication.sh
```

## Out of Scope

- hardcoding provider credentials or user-level provider settings;
- pinning a single concrete model family in the public scaffold;
- claiming hooks provide OS-level security isolation;
- removing existing Claude Code hooks or agents;
- final plugin/MCP/file-handoff normalization;
- enforcing live DB, deploy, payment, or client mutations solely through project
  hooks;
- enabling unrestricted parallel writers.

## Gate Design

The machine-readable gate is `.agent/active-work-block.json`.

A source write is allowed only when:

- gate schema is valid;
- `write_gate.status` is `READY`;
- Work Block ID is present;
- gate has not expired;
- current `HEAD` matches the recorded base commit when a base commit is set;
- specification path and revision are recorded;
- required Critic state is resolved;
- every target path is inside the approved write-set.

Before the source gate opens, writes remain allowed only to explicit coordination
paths needed to prepare specifications, plans, gate state, and reports.

The hook also denies dangerous public/live/destructive Bash operations unless the
matching Hard Stop approval is recorded. Complex mutating Bash commands that
cannot be scoped safely are denied with guidance to use `apply_patch` or a
simpler explicit command.

## Custom Agent Design

- Main Codex thread performs Orchestrator function.
- Architect, Critic, Reviewer, and Verifier are read-only by default.
- Coder uses workspace-write but remains limited by the Work Block write-set and
  hooks.
- Agent files omit concrete model names; local/user config may supply models.
- Reasoning effort may be suggested per function without changing authority.
- Agent output contracts point to the portable Work Block and report templates.

## Acceptance Criteria

- [ ] Legacy top-level `multi_agent = true` is removed.
- [ ] `[agents]` uses current Codex keys.
- [ ] Five project-scoped custom agents parse as TOML and expose logical roles.
- [ ] Hooks JSON parses and registers PreToolUse plus SubagentStart.
- [ ] Hook scripts use Python standard library only.
- [ ] Source writes are denied while gate is blocked, stale, expired, invalid, or
      outside the write-set.
- [ ] Approved in-scope `apply_patch` is allowed by fixtures.
- [ ] Preflight coordination writes remain possible while source gate is blocked.
- [ ] Dangerous Bash fixtures are denied without matching Hard Stop approval.
- [ ] Read-only Bash fixtures remain allowed.
- [ ] Subagent context reports Work Block, role, write-set, and authority without
      exposing secrets or hidden reasoning.
- [ ] Existing runtime-neutral and publication tests remain green.
- [ ] Disposable generated-project bootstrap includes and validates all Codex
      adapter files.

## Verification Plan

- parse TOML with Python `tomllib`;
- parse hooks/gate JSON with Python standard library;
- fixture-test PreToolUse decisions for blocked/ready/expired/out-of-scope and
  dangerous-command cases;
- fixture-test SubagentStart context;
- run shell syntax and Python compile checks;
- run all existing governance, SDLC, publication, and bootstrap smoke checks;
- keep PR draft until the full CI snapshot passes.

## Follow-up

- WB-004 — normalize Claude Code plugin, MCP, OpenCode, and file handoff
  integrations against the adapter contract.
- WB-005 — profile-aware bootstrap and cross-runtime conformance tests.
