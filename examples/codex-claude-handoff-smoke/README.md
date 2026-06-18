# Example: Codex -> Claude Code Handoff Smoke

Profile: Level 4 Codex -> Claude Code Handoff.

Use this before trusting automated delegation. The task is intentionally small
and safe: Claude Code writes one smoke artifact in `memory_bank/` and returns a
result file.

## Task

Create `memory_bank/handoff-smoke.txt` with the text:

```text
handoff smoke ok
```

Then report the command/check evidence through the handoff result.

## Approved Scope

```text
memory_bank/handoff-smoke.txt
memory_bank/external-team-log.md
handoff/done/**
handoff/failed/**
handoff/logs/**
handoff/status.json
```

Forbidden:

```text
.env
.env.*
**/.env
secrets/**
**/secrets/**
src/**
package.json
package-lock.json
prisma/**
```

## Expected Agent Flow

```text
Codex Control Tower:
  - writes a task file from handoff/templates/claude-team-task-template.md
  - puts it in handoff/queue/

handoff-runner:
  - moves task queue -> active
  - launches Claude Code with sanitized env and timeout
  - writes logs and status
  - runs scope audit

Claude Code external team:
  - edits only memory_bank/handoff-smoke.txt
  - updates external-team-log if requested
  - returns a result summary

Codex Control Tower:
  - reads result/log
  - records READY/BLOCKED and next action
```

## Expected Final Report

The result should state:

- status: complete;
- files changed;
- checks run;
- scope audit result;
- runner log path;
- residual risks.

## Expected Logs

```text
handoff/done/<task-id>-result.md
handoff/logs/session-<task-id>-<timestamp>-<pid>.log
handoff/status.json
memory_bank/external-team-log.md
```

## What Must Not Happen

- No source code edits.
- No package, database, auth, payment, or deploy changes.
- No secrets or provider env values in logs.
- No infinite retry loop; failed tasks must move to `handoff/failed/` or
  quarantine according to runner policy.
- No parallel swarm until single-task smoke is reliable.
