---
name: ssot-sync-closeout
description: "Post-stage sync of docs, engineering memory, memory_bank, and tasklist without rewriting history. Includes non-trivial Work Block learning review. Triggers: обнови memory bank, закрыть stage, sync tasklist/context/progress, closeout."
compatibility: opencode
---

# SSOT Sync Closeout

> Adapted from framework `skills/ssot-sync-closeout/SKILL.md` for OpenCode.
> Original remains authoritative; this copy provides OpenCode-compatible tool references.

## Objective

Maintain consistency between:
- `docs/engineering-memory/*`
- `memory_bank/context.md`
- `memory_bank/progress.md`
- `docs/tasklist/*`

For every non-trivial Work Block, Close includes an Orchestrator Learning Review.
No separate Owner reminder to record a lesson is required when the relevant
Engineering Memory path is already inside the approved Work Block authority.

## Workflow

1. Verify actual stage completion against evidence.
2. Check acceptance: subagent `DONE` ≠ result acceptance; need scope/AC/checks verdict.
3. Classify closeout: `success-closeout` only when all required gates are READY; `reporting-only` for BLOCKED/UNVERIFIED.
4. For reporting-only: leave task `blocked`, record corrective action, no completed/release-ready claims.
5. Update `progress.md` with new entry (done + notes + checks).
6. Update `context.md` (current focus + next execution queue + date).
7. For a non-trivial Work Block, review material findings from **Define, Execute, Assure, and Close** for reusable engineering knowledge.
8. Apply the durable utility filter: evidence-backed knowledge must be capable of changing future planning, execution strategy, review, verification, recovery, or invariant enforcement. Exclude one-off noise, speculation, raw transcripts, private chain-of-thought, secrets/private data, routine status history, and facts cheaper to re-verify live.
9. Classify candidates as exactly `promoted`, `operational-only`, or `not-applicable`; `none identified` is valid and must not be replaced with artificial lessons.
10. Before `promoted`, deduplicate against existing `docs/engineering-memory/`; update/extend an existing reusable principle rather than create a parallel duplicate.
11. A promoted lesson records evidence, scope, reusable principle, replacement/mitigation/recovery, authority boundary, review trigger, and last verified. Promotion may mutate only an Engineering Memory path already approved by the active Work Block. Classification is not permission; an unapproved path returns to Define.
12. Keep project-specific lessons project-local. A framework generalization requires a separate evidence-backed framework Work Block.
13. Keep `operational-only` knowledge in `memory_bank/` or reports.
14. Update `decisions.md` if an architecture/runtime decision was made.
15. Update delivery notes in tasklist.
16. Run `rg` on contradictory stale formulations.
17. Verify Git ignore: `git check-ignore -v <paths>`.
18. Verify new status markers: `rg -n` because `git diff` may be empty for ignored files.

## Constraints

- Never rewrite historical entries; supersede/retire explicitly.
- If checks were not run — state this explicitly.
- Do not promote durable Engineering Memory without reusable evidence and a clear future-use trigger.
- Engineering Memory classification cannot override Owner/spec/governance/Work Block authority or expand the write-set.
- Do not automatically promote a project lesson into framework policy/templates.
- `BLOCKED` or `UNVERIFIED` permits diagnostics and reporting-only closeout, not merge/deploy/release readiness.

## Output

- Learning Review coverage: Define / Execute / Assure / Close
- Material lesson candidates and disposition, or `none identified`
- Engineering Memory classification: `promoted`, `operational-only`, or `not-applicable`
- Updated/deduplicated Engineering Memory entries, or `none`
- Residual risks and any authority-limited promotion follow-up
