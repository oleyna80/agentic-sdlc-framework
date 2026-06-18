# Example: Codex-only Next.js Work Block

Profile: Level 1 Minimal Codex-only or Level 2 Standard Codex SDLC.

Use this when one local agent should make a small frontend change under an
approved write-set and leave review/verification evidence.

## Task

Improve the empty state copy on a fictional product catalog page.

## Approved Scope

```text
src/app/catalog/page.tsx
src/components/catalog/empty-state.tsx
docs/plans/2026-01-15-catalog-empty-state.md
memory_bank/orchestrator-log.md
memory_bank/review-log.md
```

## Expected Agent Flow

```text
Orchestrator:
  - reads AGENTS.md
  - creates or updates the Work Block
  - states expected final result and write-set

Coder:
  - edits only the approved source files
  - keeps the change small and reversible

Reviewer:
  - checks scope, UX copy, accessibility, and regressions

Verifier:
  - runs typecheck/lint or scoped fallback checks
  - records READY or BLOCKED
```

## Expected Final Report

The closeout should include:

- final result compared with the expected final result;
- files changed;
- checks run;
- review findings;
- residual risks;
- next action.

## Expected Logs

```text
memory_bank/orchestrator-log.md
memory_bank/review-log.md
docs/plans/2026-01-15-catalog-empty-state.md
```

## What Must Not Happen

- No payment, order, database, auth, or deploy changes.
- No edits outside the approved write-set.
- No generated build output committed.
- No external agent or Claude Code handoff required.
- No private project/client details in the example Work Block.
