# Project Engineering Memory

> Durable, agent-neutral engineering knowledge that future agents and humans
> can trust after the original chat context is gone.

---

## Purpose

Project Engineering Memory captures decisions, invariants, evidence pointers,
source-of-truth chains, and recurring verification lessons that are not obvious
from source code alone.

It is designed for mixed agent stacks: Codex, Claude Code, OpenCode,
Antigravity, GPT, Claude, Gemini, DeepSeek, and future models. A new agent
should be able to read it quickly and understand why the project is shaped the
way it is.

## Storage

Generated projects store committed engineering memory in:

```text
docs/engineering-memory/
```

Recommended files:

- `README.md` - index, rules, and current durable memory map
- `decision-record-template.md` - template for promoted engineering decisions
- `source-of-truth-chains.md` - where to resolve important project questions
- `temporary-decisions.md` - time-boxed exceptions and review triggers
- `reproducibility-log.md` - stable setup/check commands and evidence pointers

## Boundary With Other Memory

| Layer | Purpose | Publish by default? | Authority |
|---|---|---|---|
| `docs/engineering-memory/` | Durable project engineering memory | Yes, after review | Below active task/spec/plan/report; above operational logs |
| `memory_bank/` | Current focus, progress, decisions, orchestrator/review/external-team logs | No, local-first by default | Operational context and evidence, not contract |
| `.claude/agent-memory/` | Claude Code per-agent memory | No | Runtime-specific local memory |
| `.codex/`, OpenCode, Antigravity local state | Runtime settings and local workflow state | No | Runtime-specific local state |

`memory_bank/` may discover a lesson. `docs/engineering-memory/` is where that
lesson becomes a reviewed, portable project memory.

## Authority

When sources conflict, use this order:

1. Explicit Owner instruction for the current task.
2. Active `AGENTS.md`.
3. Approved Work Block plan and write-set.
4. Current tasklist, plans, specs, and reports.
5. `docs/engineering-memory/`.
6. `memory_bank/` and runtime logs.
7. Generated, discovered, or external artifacts.

Engineering memory explains and preserves durable knowledge. It does not
override an approved current plan or specification.

## Promotion Rule

Promote information into `docs/engineering-memory/` only when at least one is
true:

- It changes how future Work Blocks should be planned, reviewed, or verified.
- It records a durable architecture, integration, runtime, or delivery
  decision.
- It identifies a source-of-truth chain that prevents future drift.
- It captures a recurring failure pattern with evidence and a future check.
- It records a temporary exception with an expiry or review trigger.
- It documents a reproducible command, setup path, or verification sequence
  that future agents need.

Do not promote:

- raw transcripts or private chain-of-thought;
- secrets, tokens, credentials, private URLs, or unredacted client data;
- one-off task noise;
- code facts that are easy to verify from the current tree;
- git history that belongs in `git log`;
- speculative advice without evidence.

## Record Shape

Each durable memory entry should answer:

```text
Decision or invariant:
Status:
Scope:
Why this matters:
Evidence:
Source-of-truth chain:
Temporary until / review trigger:
Last verified:
```

Keep entries short. Prefer links to source files, reports, commits, or Work
Blocks over copying long evidence.

## Session Use

At session start, agents should read:

1. `AGENTS.md`
2. `PROJECT_MAP.md`
3. `FILE_REGISTRY.yml`
4. Current task or Work Block
5. Relevant `docs/engineering-memory/` entries
6. Relevant operational `memory_bank/` logs only after the durable sources

If an engineering memory entry is stale or conflicts with current files,
record the conflict and update or retire the entry during closeout.

## Closeout Gate

Every non-trivial Work Block closeout should classify reusable knowledge:

- `promoted`: durable entry updated in `docs/engineering-memory/`
- `operational-only`: kept in `memory_bank/` or reports only
- `not-applicable`: no reusable knowledge created

This keeps the memory layer useful instead of turning it into a second chat
archive.
