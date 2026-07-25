# Codex Runtime Adapter

## Status

Implemented baseline for project-scoped Codex subagents and executable Work
Block guardrails.

This adapter maps Codex runtime capabilities to the runtime-neutral Governance
Core. It does not redefine role authority, SSOT, Hard Stops, or closeout rules.

## Logical Role Mapping

| Logical role | Codex implementation | Default sandbox |
|---|---|---|
| Orchestrator | Main Codex thread / control tower | Parent session policy |
| Architect | `.codex/agents/architect.toml` | read-only |
| Critic | `.codex/agents/critic.toml` | read-only |
| Coder | `.codex/agents/coder.toml` | workspace-write |
| Reviewer | `.codex/agents/reviewer.toml` | read-only |
| Verifier | `.codex/agents/verifier.toml` | read-only |

The built-in `explorer` remains useful for read-heavy repository discovery.
Temporary specializations may be expressed in the mission brief; they do not
create broader authority.

## Installed Project Files

```text
.codex/
├── config.toml.template
├── hooks.json
├── agents/
│   ├── architect.toml
│   ├── critic.toml
│   ├── coder.toml
│   ├── reviewer.toml
│   └── verifier.toml
└── hooks/
    ├── pre_tool_use_policy.py
    └── subagent_context.py

.agent/
└── active-work-block.json
```

`config.toml.template` is not activated automatically. Copy it to
`.codex/config.toml` after reviewing project-local settings.

## Current Codex Configuration Model

Multi-agent configuration belongs under `[agents]`:

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 6
interrupt_message = true
```

`agents.enabled` currently defaults to true. The explicit setting documents
project intent and allows the adapter contract test to detect regressions.

Standalone project-scoped custom agents live under `.codex/agents/*.toml`.
Each agent supplies `name`, `description`, and `developer_instructions` and may
also set normal session values such as reasoning effort and sandbox mode.

The public framework does not pin concrete models. Model routing belongs in
private/user configuration or a deliberately validated project baseline.

## Hooks

Project hooks are declared only in `.codex/hooks.json`:

- `PreToolUse` runs `pre_tool_use_policy.py` for Bash and edit/apply-patch paths.
- `SubagentStart` runs `subagent_context.py` to add bounded Work Block authority
  to the spawned agent context.

Codex loads project-local hooks only for trusted projects. New or modified
non-managed hooks must be reviewed and trusted in Codex before they run. Inspect
hook sources before accepting them.

Do not duplicate the same project hooks inline in `.codex/config.toml`; Codex
merges both sources and warns when both representations are present.

## Machine-Readable Work Block Gate

`.agent/active-work-block.json` is the executable gate input. It is generated in
`BLOCKED` state.

Source writes require:

- schema version 1;
- non-empty Work Block ID;
- approved specification path and revision;
- `write_gate.status: READY`;
- timezone-aware, non-expired `expires_at`;
- current Git `HEAD` matching `base_commit`;
- resolved required Critic state;
- non-empty approved `write_set`;
- every source target matching that write-set.

Before the source gate opens, the hook allows only explicit coordination paths
needed to prepare specifications, plans, reports, gate state, and operational
logs.

The gate becomes stale after `HEAD` changes. Renew it deliberately before
additional source writes.

## Bash Policy

The hook permits ordinary read-only commands and inspects supported mutation
classes.

It:

- denies source writes while the gate is blocked, invalid, expired, or stale;
- denies patches outside the approved write-set;
- denies dynamic, globbed, repository-wide, or compound mutations that cannot be
  scoped safely;
- validates staged paths before an approved commit;
- requires separate approvals for commit, push, default-branch push,
  destructive operations, live infrastructure, live data, credentials, and
  client communications;
- allows approved feature-branch push only after the relevant approval is
  recorded;
- recommends `apply_patch` or small explicit commands for inspectable writes.

Dependency-manager commands have broad implicit writes and require a separately
reviewed workflow rather than automatic scope inference.

## Subagent Context

`subagent_context.py` adds:

- logical agent type;
- current permission mode;
- role authority;
- Work Block ID and governance profile;
- specification and revision;
- source gate and expiry;
- Critic state;
- approved write-set and coordination paths.

This context is operational guidance. It does not itself grant approval.

## Sandbox and Isolation Limits

Custom agent files set safe defaults, but Codex reapplies the parent turn's live
sandbox and approval overrides when spawning a child. Therefore:

- read-only agent profiles are defense in depth, not absolute isolation;
- choose parent permissions before delegation;
- record actual permission mode and isolation in the Work Block;
- use a separate read-only root, separate runtime, container, or OS boundary when
  stronger independence is required;
- treat hooks as guardrails, not a complete enforcement or security boundary.

Use parallel subagents primarily for independent read-heavy tasks. Parallel
writers require separate worktrees, non-overlapping write-sets, consolidation,
and assurance of the merged result.

## Activation

1. Bootstrap the project.
2. Review `AGENTS.md`, `governance/`, and this adapter.
3. Copy `.codex/config.toml.template` to `.codex/config.toml`.
4. Create the human Work Block.
5. Populate `.agent/active-work-block.json` while keeping the source gate
   `BLOCKED`.
6. Run required Critic review and record the result.
7. Set `base_commit`, write-set, expiry, and required approvals.
8. Change `write_gate.status` to `READY` only after Define is complete.
9. Open Codex hook management, inspect the project hook definitions, and trust
   them deliberately.
10. Run a safe fixture or read-only smoke before real writes.

## Validation

Framework CI runs:

```bash
python scripts/test-codex-adapter.py
bash scripts/test-sdd-contract.sh
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

The disposable bootstrap smoke also verifies that all agent, hook, gate, and
adapter files reach generated projects.

## Degraded Mode

When custom agents or hooks are unavailable:

- preserve the logical function through a separate session or manual pass;
- record actual runtime and isolation;
- keep source writes blocked unless another approved guardrail enforces scope;
- label same-context review as degraded;
- do not upgrade BLOCKED or UNVERIFIED evidence because the preferred Codex
  capability was unavailable.

## Official References

- [Codex subagents and custom agents](https://developers.openai.com/codex/subagents)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Codex configuration reference](https://developers.openai.com/codex/config-reference)
