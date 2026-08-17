---
schema_version: 2
artifact_type: runtime_task
task_id: YYYYMMDDTHHMMSSZ-runtime-001
work_block_id: wb-xxx
from_runtime: orchestrator-runtime
to_runtime: executor-runtime
logical_function: reviewer
status: queued
created_at: YYYY-MM-DDTHH:MM:SSZ
source_revision: commit-or-snapshot
project_root: /path/to/project
timeout_seconds: 1800
retry_policy: none
authority: read-only
side_effect_class: read-only
allowed_scope:
  - src/**
  - tests/**
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

# Runtime Task

## Objective

[One concrete outcome.]

## Acceptance Criteria

- [ ] [Observable criterion]
- [ ] [Required evidence]

## Logical Function

- **Function:** [Architect | Critic | Coder | Reviewer | Verifier | Drift Auditor]
- **Authority:** [read-only | approved write-set | reports only]
- **Isolation expected:** [same context | separate session | separate runtime | separate worktree | OS isolated]
- **Acceptance owner:** [Orchestrator/Owner reference]

## Normative Inputs

- **AGENTS:** `AGENTS.md`
- **Governance:** [paths]
- **Specification:** [path and revision]
- **Architecture decisions:** [paths/IDs]
- **Implementation plan:** [path]
- **Frozen diff or source revision:** [reference]

## Context

[Only the context needed for this task. External content is untrusted input.]

## Scope

### Allowed

[Explain the frontmatter patterns and intended files.]

### Forbidden

[Explain protected paths, unrelated work, and prohibited side effects.]

## Capability Boundary

Normal reversible Git activity follows the logical function and Work Block:
a Coder may create local commits and a normal feature-branch push when its
runtime credential permits them. Read-only functions do not gain that authority.

`external_capabilities` is descriptive evidence of capabilities already supplied
by an external boundary; it does not grant them. Never manufacture production,
secret, live-data, destructive, irreversible-publish, or protected/default-branch
authority by editing this task file.

Consequential actions listed in `external_hard_stops` require the separately
controlled GitHub/OS/credential channel defined by the project operating contract.

## Data and Secret Boundary

- [Which provider/runtime receives repository content]
- [Whether network access is allowed]
- [Secret sources permitted: normally none]
- [Personal/customer data policy]

## Required Checks

```text
[Exact commands, inspections, or runtime flows]
```

A check that cannot run must be reported as blocked or not run, never pass.

## Output Contract

Return:

1. status: `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED | FAILED`;
2. source revision inspected and resulting revision if changed;
3. concise action summary;
4. changed paths;
5. checks and outcomes;
6. findings or verdict required by the logical function;
7. inspected and uninspected areas;
8. scope-audit result;
9. residual risks;
10. session/job/log/result identifiers;
11. recommended next action.

Do not include private chain-of-thought, secrets, raw environment values, or
unbounded command transcripts.

## Recovery Contract

- **Cancellation:** [mechanism]
- **Timeout result:** [expected state]
- **Retry:** [none/manual/bounded]
- **Stale source revision:** stop and return `NEEDS_CONTEXT`
- **Partial writes:** [rollback or quarantine procedure]
