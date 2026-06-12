# Orchestrator Log

> Control Tower decision log — why decisions were made.
> Updated by Control Tower after Stage 0 and Stage 3.
> Distinct from `progress.md`: progress tracks *what*; orchestrator-log tracks *why*.

---

| Date | Work Block | Decision | Rationale | Subagents Used | Critic Verdict | Outcome |
|---|---|---|---|---|---|---|
| — | wb-example | Standard tier | No auth/DB/payment touched | verifier | APPROVE | READY |

## What to log

| Event | When | Content |
|---|---|---|
| Tier selection | After Stage 0 | Chosen tier + rationale (why not higher/lower) |
| Skill skip | After Stage 0 | Each skipped skill + skip reason + why valid |
| Subagent topology | After Stage 0 | Which agents dispatched + why this topology |
| Critic verdict | After Stage 0.5 | APPROVE/SUPPLEMENT/RECONSIDER + action taken |
| Hard Stop trigger | Any stage | Which Hard Stop + Owner decision |
| Scope change | Any stage | What changed + why + re-approval status |
| Stage outcome | After Stage 3 | Final verdict (READY/BLOCKED/ESCALATED) + residual risks |

## What NOT to log

- Implementation details — these are in git history
- Subagent report contents — these are in `review-log.md`
- Architecture decisions — these are in `decisions.md`
- Task status — this is in `progress.md` and `docs/tasklist/`
