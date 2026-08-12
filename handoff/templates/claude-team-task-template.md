---
schema_version: 2
artifact_type: runtime_task
task_id: YYYYMMDDTHHMMSSZ-claude-runner-001
work_block_id: wb-xxx
from_runtime: orchestrator-runtime
to_runtime: claude-code
logical_function: coder
status: queued
created_at: YYYY-MM-DDTHH:MM:SSZ
source_revision: commit-or-snapshot
project_root: /path/to/project
timeout_seconds: 1800
retry_policy: none
authority: approved-write-set
side_effect_class: production-code
transport_implementation: claude-code-runner
allowed_scope:
  - src/**
  - tests/**
  - docs/reports/**
  - memory_bank/external-team-log.md
forbidden_scope:
  - .env
  - .env.*
  - secrets/**
  - credentials/**
  - "*.pem"
  - "*.key"
external_capabilities: []
external_hard_stops:
  - protected_default_branch_mutation
  - destructive
  - live_infra
  - live_data
  - credentials
  - client_communications
  - irreversible_publish
result_destination: handoff/done/
log_destination: handoff/logs/
---

# Claude Code Runner Task — Compatibility Template

> Compatibility specialization for the current Claude Code runner. New generic
> orchestration should start with `runtime-task-template.md`.

## Objective

[One concrete outcome for Claude Code.]

## Acceptance Criteria

- [ ] [Observable result]
- [ ] [Required evidence]

## Runtime and Function Binding

- **Target runtime:** Claude Code
- **Transport:** file handoff / `claude-code-runner`
- **Logical function:** [Architect | Critic | Coder | Reviewer | Verifier | Drift Auditor]
- **Authority:** [read-only | approved write-set | reports only]
- **Isolation:** separate runtime, same user/machine unless otherwise established
- **Acceptance owner:** [Orchestrator/Owner reference]

Claude Code is an external runtime implementation, not a new authority layer.
Its internal agents, hooks, and memory remain bounded by this task and the active
Work Block.

## Normative Inputs

- **AGENTS:** `AGENTS.md`
- **Specification:** [path/revision]
- **Architecture decisions:** [paths]
- **Implementation plan:** [path]
- **Source revision/frozen diff:** [reference]

## Context

[Only required project context. Do not include private reasoning or secrets.]

## Scope Notes

Explain the frontmatter patterns. Add Claude process/evidence paths only when the
runtime is expected to update them, for example:

```yaml
allowed_scope:
  - memory_bank/orchestrator-log.md
  - memory_bank/review-log.md
  - .agent/critic-gate.md
  - .agent/verification-gate.md
  - .claude/agent-memory/**
```

These are project files and will be scope-audited. Do not add them by default.

## Capability Boundary

A Coder may create local commits and a normal feature-branch push when the Work
Block and runtime credential permit them. SSH-signed Work Block authorization is
not required for these normal reversible Git operations.

`external_capabilities` records capabilities already supplied by an external
boundary; editing this task cannot create production, secret, live-data,
destructive, irreversible-publish, or protected/default-branch authority.
Consequential operations listed in `external_hard_stops` require the separately
controlled GitHub/OS/credential channel.

## Required Checks

```text
[Exact commands or runtime checks]
```

Unavailable checks are blocked/not run, never pass.

## External Team Log

When `memory_bank/external-team-log.md` is allowed, append a concise delivery
entry containing:

- task/Work Block IDs;
- accepted objective and scope;
- logical functions/subagents used;
- source/result revision;
- actions and changed paths;
- checks and outcomes;
- findings/verdicts;
- scope-audit result;
- result/log paths;
- blockers, residual risks, and next action.

Do not log private chain-of-thought, secrets, environment values, or full command
transcripts.

## Response Contract

Return:

1. `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED | FAILED`;
2. source revision inspected and resulting revision;
3. concise action summary;
4. changed paths;
5. checks and outcomes;
6. required review/verification/drift verdict;
7. inspected/uninspected areas;
8. scope-audit result;
9. residual risks;
10. session/result/log identifiers;
11. recommended next action.

## Recovery

- stale source revision: return `NEEDS_CONTEXT`;
- timeout/cancellation: leave a non-success result and recover through runner
  state;
- retry: use a fresh task ID or explicit retry record;
- partial writes: quarantine or roll back according to the Work Block.
