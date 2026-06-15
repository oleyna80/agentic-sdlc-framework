# Agentic SDLC Overview

> The philosophy and structure of AI-agent-driven software development.

---

## What is Agentic SDLC?

An iterative-incremental, documentation-first, gate-based workflow with
controlled multi-agent orchestration. It borrows from Agile but adds structural
authority, verification gates, and intentional friction to make AI agents safe
and predictable collaborators.

**It is not:**
- Waterfall — plans and architecture may evolve after each verified gate
- "Vibe coding" — non-trivial work requires an approved Work Block, explicit final outcome, scope, AC, verification tier, hard stops, and maintainability review

## Core Principles

1. **Authority is structural, not prompt-based** — roles define what agents can do, not conversational pressure
2. **Gates before action** — Hard Stops, Stage 0 Preflight, Skill Routing Gate, and Verification Tiers prevent costly mistakes
3. **Intentional Friction** — agents slow down before generating code when the task is vague or risky
4. **Local-first workflow** — `.agent/` and `memory_bank/` stay local unless explicitly published
5. **Evidence over assertion** — every verdict, every check, every claim backed by file:line or command output

## Runtime Layering

Agentic SDLC is the core process, not a single tool's feature set.

| Layer | Purpose | Primary files |
|---|---|---|
| Core SDLC | Runtime-neutral operating model for planning, implementation, review, verification, memory, and closeout | `AGENTS.md`, `.agent/`, `skills/`, `docs/`, `memory_bank/` |
| Codex runtime | Codex-specific instructions, subagent policy, local config, and Stage 0 write gate for independent Codex operation | `.codex/` |
| Handoff | File-based dispatch between Codex control tower and Claude Code external team sessions | `handoff/` |
| Claude Code runtime | Claude Code orchestrator/subagent team layer with hooks, MCP, per-agent memory, critic/verifier gates | `CLAUDE.md`, `.claude/` |

Codex can run the core SDLC by itself. Claude Code is added when a Work Block
benefits from its native team architecture: subagents, hooks, MCP integration,
and independent critic/verifier workflows. The handoff layer connects the two
without making either runtime the only valid executor.

## Stage Flow

```
Standard:
  Plan & Discover (Control Tower)
    └─→ Implement (Scoped Coder, per-task)
          └─→ Verify (Verifier gate, tier-scoped)
                └─→ Sync & Report (SSOT Sync + Owner report)

Quick-fix (≤3 files, no route/schema/API/security):
  Implement (Lite checks) → Inline sync → Done
```

## Agent Roles

| Role | Responsibility | Write Access |
|---|---|---|
| Control Tower (Orchestrator) | Scope, workflow, delegation, consolidation, approvals, risks, next action | `.agent/*`, docs, memory_bank |
| Solution Architect | Pre-implementation research (read-only) | None |
| Scoped Coder | Approved-scope implementation only | Approved write-set |
| Reviewer | Read-only multi-dimension review | None |
| Verifier | AC verification gate (read-only) | `docs/reports/*` |

## Key Documents

| Document | Purpose |
|---|---|
| `AGENTS.md` | Operating contract — authoritative |
| `.agent/ROSTER.md` | Agent routing + skill assignments |
| `.agent/workflows/sdd-protocol.md` | Full stage definitions |
| `.codex/` | Codex runtime adapter, instructions, config, write gate |
| `CLAUDE.md` / `.claude/` | Claude Code runtime adapter, hooks, agents, memory |
| `handoff/` | Codex -> Claude Code delegation runner |
| `memory_bank/` | Durable project context |
