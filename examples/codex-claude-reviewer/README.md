# Example: Codex + Claude Code Read-only Reviewer

Profile: Level 3 Claude Code Team Runtime.

Use this when Codex remains the Control Tower but asks Claude Code to perform
an independent read-only review inside the same project.

## Task

Review a fictional checkout form refactor for missed UX, accessibility, and
scope risks. Claude Code must not edit files.

## Approved Scope

Read-only:

```text
src/app/checkout/**
src/components/forms/**
docs/plans/2026-01-20-checkout-form-refactor.md
memory_bank/review-log.md
```

Allowed report write, if the project permits reviewer reports:

```text
docs/reports/2026-01-20-checkout-form-review.md
```

## Expected Agent Flow

```text
Codex Orchestrator:
  - defines review objective, scope, and forbidden actions
  - confirms Claude Code is read-only

Claude Code Reviewer:
  - reads AGENTS.md and relevant Work Block
  - runs read-only inspection commands
  - may run tests if they do not mutate production or secrets
  - writes a concise review report if allowed

Codex Orchestrator:
  - accepts, rejects, or defers findings
  - records decision in memory_bank/review-log.md
```

## Expected Final Report

Claude Code report should include:

- verdict: READY, SUPPLEMENT, or BLOCKED;
- findings ordered by severity;
- evidence with file paths and commands;
- tests/checks run;
- scope or process concerns;
- explicit statement that no source files were modified.

## Expected Logs

```text
memory_bank/review-log.md
docs/reports/2026-01-20-checkout-form-review.md
.claude/agent-memory/reviewer/MEMORY.md
```

## What Must Not Happen

- Claude Code must not patch source files.
- Claude Code must not run external AI CLI calls through shell pipes unless
  that boundary is explicitly approved.
- Review must not inspect `.env`, tokens, cookies, or private provider config.
- Review findings are not automatic implementation approval.
