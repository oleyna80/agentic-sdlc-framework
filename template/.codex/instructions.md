# Codex Instructions — Project-Level

> System instructions for Codex CLI. Read alongside `AGENTS.md`.
> Primary operating contract is `AGENTS.md` (Claude Code).
> This file applies only when using Codex as a secondary tool.

---

## Sub-Agent Delegation Policy

You have `multi_agent = true`. Keep the main thread as Control Tower: plan,
delegate, collect results, handle Owner/Hard Stop decisions, and report. Use
sub-agents actively whenever delegation materially improves speed, quality,
context isolation, or expected work size. Do not run large/non-trivial pipelines
entirely in the main thread.

Owner approval of a Work Block is explicit authorization to launch scoped
sub-agents automatically when the Work Block is `Subagent-Required` under
`AGENTS.md -> Multi-Agent Default`. This authorization is limited to the
approved scope. It does not expand write authority, side-effect authority,
DB authority, or Hard Stop authority.

Before any non-trivial edit/write action, the first visible Work Block output
must include `Stage 0 Routing Preflight` with Skill Routing Gate, Subagent
Topology, side-effect class, DB action mode, Hard Stops, and
`Write gate: READY` or `Write gate: BLOCKED`.

### When to spawn sub-agents

| Situation | Action |
|---|---|
| Stage 1 (Implement) has 2+ independent tasks | Spawn one agent per task, wait for all |
| Running tests, lint, type checks, build | Spawn a verifier agent — keeps main context clean |
| Reading many files for discovery | Spawn a reader agent for each independent area |
| Expected work is large or multi-domain | Split by independent domain/task |
| SSOT sync (Stage 3) | Spawn a sync agent to update memory_bank |

### When NOT to spawn

- Quick-fix pipeline (≤3 files, trivial change) — run inline
- Single-file edit — no benefit from delegation
- Hard Stop operations — handle in main thread for explicit Owner interaction

### Delegation template

When spawning a sub-agent, always include:

1. **Task name**: descriptive (e.g., `implement-feature-x`)
2. **Scope**: exact files the agent may modify (write-set)
3. **Constraints**: "You are not alone in the environment."
4. **Verification tier**: Lite / Standard / Full
5. **Recursion guard**: "Do not spawn sub-agents yourself and do not launch nested external AI CLI tools."
6. **Self-report boundary**: "Report only from your assigned role."
7. **Authority boundary**: include Side-effect class and DB action mode from `AGENTS.md`.
8. **Close**: always `close_agent` when done

---

## SDD Stage Mapping

```
Stage 0 · Plan & Discover  →  Main thread (you)
Stage 1 · Implement         →  Spawn sub-agent(s) per task from write-set
Stage 2 · Verify            →  Spawn verifier agent OR run inline for Lite tier
Stage 3 · Sync & Report     →  Main thread (you)
```

### Verification tier routing

| Tier | Verifier approach |
|---|---|
| Lite | Run `git diff --check` inline, no sub-agent needed |
| Standard | Spawn one verifier agent: types + lint + build |
| Full | Spawn one verifier agent: full check suite |

---

## Context Hygiene

- **Offload noisy reads**: spawn an agent to scan large codebases
- **Keep main thread for planning**: main thread plans, delegates, collects, reports
- **Close agents**: always `close_agent` after collecting results

---

## File Authority

Same as `AGENTS.md § File Write Authority`. Sub-agents inherit your sandbox policy.
Constrain each sub-agent's write-set explicitly.

---

## Memory Bank

Read on session start (main thread):
1. `memory_bank/context.md`
2. `memory_bank/progress.md`
3. `memory_bank/decisions.md`

Update only in Stage 3 (Sync & Report), after verification evidence exists.

---

## Hard Stops

Sub-agents must NOT perform Hard Stop operations. These stay in the main thread:
- Production deploy
- Live DB migration
- Credential rotation
- Destructive git ops
- Real client communications
