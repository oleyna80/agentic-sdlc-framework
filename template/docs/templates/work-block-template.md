# Work Block Template

> Fill in before Stage 0 Preflight.

## Meta
- **Work Block ID:** [wb-xxx]
- **Date:** [YYYY-MM-DD]
- **Owner:** [name]
- **Execution Mode:** [end-to-end autonomous | staged approval | read-only review | advisory]
- **Side-Effect Class:** [read-only | local-docs | production-code | local-test | public-repo | live-infra | live-data | client-facing | destructive]
- **DB Action Mode:** [none | local_temp | live_readonly | live_migration_apply | runtime_app | emergency_remediation]
- **Verification Tier:** [lite | standard | full]

## Objective
[What user or technical outcome does this Work Block produce?]

## Expected Final Result
[What exact end state should be true when this Work Block is complete? Write it
as the target state the Owner can recognize. Include user-visible result,
published/deployed state if relevant, verification evidence, docs/logs updated,
and what must be left clean.]

## Done Criteria
- [ ] [Measurable completion condition 1]
- [ ] [Measurable completion condition 2]
- [ ] [Repo/runtime state is clean or documented]

## Dependency Check
### Must Resolve Before Start
- [Dependency, permission, credential, access, design, or decision required
  before implementation starts]

### Can Resolve During Work
- [Non-blocking uncertainty the Orchestrator may solve without pausing unless
  it hits a Hard Stop]

## Scope
### In Scope
- [Item 1]

### Out of Scope
- [Item 1]

## Write-Set
```
[Approved files/directories]
```

## Acceptance Criteria
- [ ] [AC 1]
- [ ] [AC 2]

## Risks and Mitigations
| Risk | Impact | Mitigation | Stop Condition |
|---|---|---|---|
| [Risk] | [Impact] | [Mitigation] | [When to stop and ask Owner] |

## Hard Stops in Scope
- [ ] Production deploy
- [ ] Live DB migration
- [ ] Credential rotation
- [ ] Destructive git ops
- [ ] Client communications

## Subagent Strategy
- **Classification:** [Subagent-Required | Single-Agent]
- **Triggers matched:** [list]
- **Use Claude Code team:** [yes | no | conditional; why]
- **Use Codex/GPT critic or verifier:** [yes | no | conditional; why]
- **Dispatch plan:** [agents, order, parallel groups]
- **Budget posture:** [normal | cheap CC/DeepSeek OK | constrained]
- **Skip reasons:** [only if any expected agent/critic/verifier is skipped]

## Skills
- **Checked:** [list]
- **Matched:** [list]
- **Used:** [list]
- **Skipped:** [list with reasons]

## Verification Plan
[How will the AC be verified? What evidence is expected?]

## Rollback / Recovery
[How to undo if this goes wrong?]

## Execution Log
| Time | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| [time] | [stage] | [what happened] | [command, file, review, or artifact] | [status] |

## Retrospective Notes
- **What worked:** [process/tooling/agent behavior worth preserving]
- **What did not work:** [friction, missed context, weak gate, slow step]
- **Framework updates to consider:** [template, hook, skill, doc, runner, memory]
- **Follow-up Work Blocks:** [links or IDs]
