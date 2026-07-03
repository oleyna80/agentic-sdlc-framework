# Operational Memory Bank Protocol

> Local operational context, progress, and audit logs between sessions.

---

## Session Start Read Set

For non-trivial work, read before planning edits:

1. `AGENTS.md` — operating contract
2. `.agent/workflows/sdd-protocol.md` — stage flow, verification tiers
3. `.agent/ROSTER.md` — agent routing + skill assignments
4. Relevant `docs/engineering-memory/` entries — durable project memory
5. `memory_bank/context.md` — current focus and next gate
6. `memory_bank/progress.md` — rolling status log
7. `memory_bank/decisions.md` — operational decision summary

## Memory Bank Files

| File | Purpose | Update Trigger |
|---|---|---|
| `context.md` | Current focus, active WBs, next gate | After Stage 3 closeout |
| `progress.md` | Rolling log: WHAT was done, status, verdict | After each verified closeout |
| `decisions.md` | Operational decision summaries and pointers to durable records | When a significant decision is made |
| `orchestrator-log.md` | WHY decisions were made: tier, skips, topology, critic verdict, outcome, retrospective lessons | After Stage 0 (decisions) and Stage 3 (outcome/lessons) |
| `review-log.md` | WHAT subagents found: agent, verdict, key findings, evidence | After each subagent returns |
| `external-team-log.md` | HOW delegated external teams worked: accepted scope, actions, files, checks, risks | During and after external handoff sessions |

## Rules

- Update only after implementation has verification evidence
- Never write secrets, tokens, or credentials to memory bank
- Never write private chain-of-thought; log decision/action summaries only
- Memory bank is operational context, not a contract — `docs/` and
  `docs/engineering-memory/` beat `memory_bank/` in conflicts
- Promote reusable engineering knowledge to `docs/engineering-memory/` during
  closeout instead of leaving it only in operational logs
- Keep entries concise — one line per decision, one line per progress entry
- Retrospectives must stay evidence-based: record action summaries, critic
  value, process misses, and reusable framework updates; never record private
  chain-of-thought.
