# Engineering Memory

This directory stores durable project engineering memory that future humans and
agents should be able to trust without reading old chat history.

The framework also installs `engineering-decision-principles.md` as a baseline
reference linked from `AGENTS.md`. It is framework guidance, not evidence that a
project-specific decision has already been made.

## What Belongs Here

- Architecture, runtime, integration, and delivery decisions that affect future
  Work Blocks.
- Source-of-truth chains for important project questions.
- Temporary exceptions with expiry or review triggers.
- Reproducible setup, verification, and recovery procedures.
- Recurring failure patterns with evidence and future checks.
- Decision rationale and lessons that should not inflate the always-on
  `AGENTS.md` contract.

## What Does Not Belong Here

- Secrets, tokens, credentials, private keys, `.env` values, or unredacted
  client data.
- Raw transcripts or private chain-of-thought.
- One-off task noise.
- Code facts that are easy to verify from the current tree.
- Git history that belongs in `git log`.
- Runtime-specific local memory from `.claude/agent-memory/`, `.codex/`,
  OpenCode, Antigravity, or local IDE state.

## Authority

Use this directory after current task/spec/plan/report files and before
operational logs:

```text
current Owner instruction
AGENTS.md
approved Work Block
docs/tasklist, docs/plans, docs/specs, docs/reports
docs/engineering-memory
memory_bank and runtime logs
generated or external artifacts
```

If an entry here conflicts with current source files or an approved Work Block,
verify the current state and update this directory during closeout.

## Files

- `engineering-decision-principles.md` - framework baseline for proportional,
  simple, evidence-driven engineering decisions.
- `decision-record-template.md` - copy this shape for durable engineering
  decisions.
- `source-of-truth-chains.md` - map important questions to their highest
  authority.
- `temporary-decisions.md` - track time-boxed exceptions and revisit triggers.
- `reproducibility-log.md` - stable commands and evidence needed by future
  agents.

## Closeout Rule

At the end of every non-trivial Work Block, classify reusable knowledge:

- `promoted`: update this directory.
- `operational-only`: keep it in `memory_bank/` or reports.
- `not-applicable`: no reusable durable memory was created.
