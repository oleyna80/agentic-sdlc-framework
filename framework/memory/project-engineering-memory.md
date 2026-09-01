# Project Engineering Memory

> Durable, agent-neutral engineering knowledge that future agents and humans
> can trust after the original chat context is gone.

---

## Purpose

Project Engineering Memory captures decisions, invariants, evidence pointers,
source-of-truth chains, recovery knowledge, and recurring verification lessons
that are not obvious from source code alone.

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
- `lessons-learned.md` - reusable evidence-backed lessons from completed or materially revised Work Blocks
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

`memory_bank/` or a report may discover a lesson. `docs/engineering-memory/` is
where that lesson becomes a reviewed, portable project memory.

## Authority

When sources conflict, use this order:

1. Explicit Owner instruction for the current task.
2. Active `AGENTS.md` and accepted governance.
3. Approved specification and accepted architecture decisions.
4. Approved Work Block plan and write-set.
5. Current tasklist, plans, and assurance/closeout reports.
6. `docs/engineering-memory/`.
7. `memory_bank/` and runtime logs.
8. Generated, discovered, or external artifacts.

Engineering memory explains and preserves durable knowledge. It does not
override current Owner intent, governance, an approved plan/specification, Hard
Stops, or the active Work Block write-set.

Learning classification is a disposition, not a permission grant. A candidate
may be `promoted` only when the target Engineering Memory path is already inside
the approved Work Block authority. If a new durable path or material framework
change is needed, return to Define rather than treating the lesson as authority.

## Promotion Rule

Promote information into `docs/engineering-memory/` only when it is
**evidence-backed** and at least one is true:

- It changes how future Work Blocks should be planned, executed, reviewed, or verified.
- It prevents a repeat failure or records a durable recovery sequence.
- It records a durable architecture, integration, runtime, delivery, or lifecycle invariant.
- It identifies a source-of-truth chain that prevents future drift.
- It captures a recurring failure pattern with evidence and a future check.
- It records a temporary exception with an expiry or review trigger.
- It documents a reproducible command, setup path, or verification sequence
  that future agents need.
- It explains why a previously reasonable approach was rejected or retired in a
  way that should alter future engineering decisions.

Before creating a new lesson, search existing Engineering Memory for the same
reusable principle. Prefer updating, extending, confirming, or explicitly
superseding an existing entry over creating a duplicate.

Do not promote:

- raw transcripts or private chain-of-thought;
- secrets, tokens, credentials, private URLs, or unredacted client data;
- one-off task noise or routine status chronology;
- code facts that are easy/cheaper to verify from the current tree;
- git history that belongs in `git log`;
- speculative observations or advice without evidence.

## Lesson Candidate Types

Useful candidates commonly include:

- recurring failure pattern;
- recovery lesson;
- durable invariant;
- source-of-truth lesson;
- process/lifecycle defect;
- verification or evidence gap;
- reusable operational pattern;
- rejected/retired approach with an evidence-backed reason.

These are candidate categories, not a requirement to create a lesson. `none
identified` is a valid non-trivial closeout result when the evidence contains no
material reusable knowledge.

## Record Shape

Each durable lesson or decision should answer the relevant fields below:

```text
Decision, invariant, or lesson:
Status:
Scope:
Why this matters:
Evidence:
Reusable principle:
Replacement / mitigation / recovery:
Source-of-truth chain:
Authority boundary:
Temporary until / review trigger:
Last verified:
```

Keep entries short. Prefer links to durable source files, reports, commits, or
Work Blocks over copying long evidence.

## Project-to-Framework Boundary

A project-specific lesson remains project-local by default. Repetition or
successful generalization may justify a **candidate** framework improvement, but
it does not automatically modify framework policy, skills, governance, or
templates. Promotion from a project lesson into the framework requires a
separate evidence-backed framework Work Block with its own scope, write-set,
review, verification, and Owner authority.

## Session Use

At session start, agents should read:

1. `AGENTS.md`
2. `PROJECT_MAP.md`
3. `FILE_REGISTRY.yml`
4. Current task or Work Block
5. Relevant `docs/engineering-memory/` entries
6. Relevant operational `memory_bank/` logs only after the durable sources

If an engineering memory entry is stale or conflicts with current files,
record the conflict and update, supersede, or retire the entry during closeout.

## Closeout Gate

Every **non-trivial** Work Block closeout, including reporting-only closeout,
MUST perform an Orchestrator Learning Review of material findings encountered in
**Define, Execute, Assure, and Close**. This is normal Close responsibility and
does not require a separate Owner reminder after the Work Block/write authority
has already been approved.

Classify reusable knowledge as exactly:

- `promoted`: durable evidence-backed entry updated in `docs/engineering-memory/`
- `operational-only`: kept in `memory_bank/` or reports only
- `not-applicable`: no durable reusable knowledge was created

The closeout records the reviewed stages, material lesson candidates and their
disposition (or `none identified`), deduplication result when promotion occurs,
and any authority-limited follow-up. This keeps the memory layer useful instead
of turning it into a second chat archive.
