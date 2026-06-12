# Memory Bank Protocol

> Durable project context between sessions.

---

## Session Start Read Set

For non-trivial work, read before planning edits:

1. `AGENTS.md` — operating contract
2. `.agent/workflows/sdd-protocol.md` — stage flow, verification tiers
3. `.agent/ROSTER.md` — agent routing + skill assignments
4. `memory_bank/context.md` — current focus and next gate
5. `memory_bank/progress.md` — rolling status log
6. `memory_bank/decisions.md` — ADRs and durable decisions

## Memory Bank Files

| File | Purpose | Update Trigger |
|---|---|---|
| `context.md` | Current focus, active WBs, next gate | After Stage 3 closeout |
| `progress.md` | Rolling log: WHAT was done, status, verdict | After each verified closeout |
| `decisions.md` | Architecture decisions + rationale | When a significant decision is made |
| `orchestrator-log.md` | WHY decisions were made: tier, skips, topology, critic verdict, outcome | After Stage 0 (decisions) and Stage 3 (outcome) |
| `review-log.md` | WHAT subagents found: agent, verdict, key findings, evidence | After each subagent returns |

## Rules

- Update only after implementation has verification evidence
- Never write secrets, tokens, or credentials to memory bank
- Memory bank is a cache, not a contract — docs/ beats memory_bank in conflicts
- Keep entries concise — one line per decision, one line per progress entry
