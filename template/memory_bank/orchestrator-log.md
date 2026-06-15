# Orchestrator Log

> Control Tower decision log — why decisions were made.
> Updated by Control Tower after Stage 0 and Stage 3.
> Distinct from `progress.md`: progress tracks *what*; orchestrator-log tracks *why*.

---

| Date | Work Block | Decision | Rationale | Subagents Used | Critic Verdict | Outcome |
|---|---|---|---|---|---|---|
| — | wb-example | Standard tier | No auth/DB/payment touched | codex-critic, verifier | APPROVE | READY |

## What to log

| Event | When | Content |
|---|---|---|
| Tier selection | After Stage 0 | Chosen tier + rationale (why not higher/lower) |
| Skill skip | After Stage 0 | Each skipped skill + skip reason + why valid |
| Subagent topology | After Stage 0 | Which agents dispatched + why this topology |
| Codex critic mode | After Stage 0.5 | READY / FALLBACK / SKIPPED + reason |
| Critic verdict | After Stage 0.5 | APPROVE/SUPPLEMENT/RECONSIDER + action taken |
| Critic skip | Before Stage 1 | Valid skip condition or Owner approval |
| Hard Stop trigger | Any stage | Which Hard Stop + Owner decision |
| Scope change | Any stage | What changed + why + re-approval status |
| Stage outcome | After Stage 3 | Final verdict (READY/BLOCKED/ESCALATED) + residual risks + critic value + retrospective lesson if any |

## What NOT to log

- Implementation details — these are in git history
- Subagent report contents — these are in `review-log.md`
- Architecture decisions — these are in `decisions.md`
- Task status — this is in `progress.md` and `docs/tasklist/`
