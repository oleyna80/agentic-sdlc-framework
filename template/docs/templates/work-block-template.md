# Work Block Template

> Fill this before non-trivial repository mutation. The Work Block binds the
> runtime-neutral governance contract to one concrete objective.

## Metadata

- **Work Block ID:** [wb-xxx]
- **Date:** [YYYY-MM-DD]
- **Owner:** [name/reference]
- **Orchestrator:** [logical role binding]
- **Governance Profile:** [Advisory | Controlled | Managed | Assured | Distributed]
- **Execution Mode:** [conductor | orchestrator | staged approval | read-only review | advisory]
- **Verification Tier:** [lite | standard | full]
- **Evaluation Required:** [yes | no; risk/non-determinism reason]

## Lifecycle State

- **Current Stage:** [Define | Execute | Assure | Close]
- **Stage State:** [blocked | ready | in_progress | completed]
- **Requirements Quality Gate:** [PENDING | READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED | SKIPPED]
- **Define Consistency Gate:** [PENDING | READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED | SKIPPED]
- **Write Gate:** [READY | BLOCKED]
- **Critic Gate:** [PENDING | READY | BLOCKED | SKIPPED | DEGRADED]
- **Review Gate:** [PENDING | READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED | SKIPPED]
- **Verification Verdict:** [PENDING | READY | BLOCKED | UNVERIFIED]
- **Evaluation Verdict:** [PENDING | READY | BLOCKED | UNVERIFIED | NOT_REQUIRED]
- **Drift Gate:** [PENDING | READY | BLOCKED | UNVERIFIED | SKIPPED]
- **Closeout Mode:** [pending | success-closeout | reporting-only]
- **Owner Approval Evidence:** [message/reference | not required]

Requirements-quality and Define-consistency states are pre-execution evidence.
They never grant source-write authority; the Write Gate remains separate.

## Objective

[What user or technical outcome must this Work Block produce?]

## Expected Final Result

[Describe the exact recognizable end state, including user-visible behavior,
repository/runtime state, evidence, documentation, and what must remain clean.]

## Done Criteria

- [ ] [Measurable outcome]
- [ ] [Required Define-quality, deterministic, output, and trajectory evidence exists]
- [ ] [Repository/runtime state is clean or documented]

## Normative Baseline

- **Approved Specification:** [path]
- **Specification Status:** [draft | proposed | approved | superseded]
- **Specification Revision:** [commit/hash/version]
- **Accepted Architecture Decisions:** [paths/IDs]
- **External Contracts:** [API/schema/legal/provider/user contract or not applicable]
- **Requirements Clarification:** [not required | completed reference | blocking decisions]
- **Requirements Quality Review:** [not required | report path and verdict]
- **Derived Implementation Plan:** [path]
- **Active Tasklist:** [path]
- **Traceability Validation:** [not required | command/result]
- **Define Consistency Analysis:** [not required | report/reference and verdict]
- **Approved Evaluation Plan:** [not required | docs/evals/<id>/plan.json]

Rule: approved specification and accepted architecture decisions outrank plans,
tasklists, requirements-quality/consistency reports, evaluation reports, and
operational logs.

## Repository Preflight

- **Git baseline:** [branch/commit/status]
- **Pre-existing dirty files:** [none | list with ownership]
- **Untracked artifacts:** [none | list]
- **Current diff:** [none | summary/reference]
- **Proceed rule:** [why unrelated changes will not be touched]

## Dependency Check

### Must Resolve Before Start

- [Permission, requirement, access, design, environment, or decision]

### May Resolve During Work

- [Non-blocking uncertainty and stop condition]

## Scope

### In Scope

- [Item]

### Out of Scope

- [Item]

## Write-Set

```text
[Approved files/directories]
```

- **One Coder per write-set:** [yes]
- **Parallel writers:** [no | separate worktrees and non-overlapping write-sets]
- **Scope guard:** [git diff/status/path validation]

Lifecycle reports, Define-quality/evaluation evidence, logs, and gate artifacts
are counted separately from implementation files when applying Quick-Fix and
trigger thresholds.

## Risk and Authority

- **Side-Effect Class:** [read-only | local-docs | production-code | local-test | public-repo | live-infra | live-data | client-facing | destructive]
- **DB/Data Action Mode:** [none | local_temp | live_readonly | live_migration_apply | runtime_app | emergency_remediation]
- **Sensitive Domains:** [none | auth | payments | DB/schema | webhooks | provider | deploy | security | client communications | other]
- **Output Non-Determinism:** [none | bounded | material; why]
- **Autonomous Tool/Trajectory Risk:** [none | bounded | material; why]
- **Threat Model Required:** [yes | no; reason]
- **Rollback / Recovery:** [procedure]

## Hard Stops in Scope

- [ ] Production deploy or live service restart
- [ ] Live DB migration or live-data mutation
- [ ] Credential/token/secret change
- [ ] Destructive git/filesystem/database operation
- [ ] Commit or push
- [ ] Push to default branch
- [ ] Public release/publication
- [ ] Client/user communication
- [ ] Payment/order/stock/CRM/external consequential mutation
- [ ] Material specification, evaluation-plan, or scope expansion

For each checked item, record approval state and evidence. Define-quality or
evaluation evidence cannot open or waive a Hard Stop.

## Runtime Capability Snapshot

- **Primary Runtime:** [codex | claude-code | opencode | generic | other]
- **Runtime Adapter:** [path/reference]
- **Runtime Version:** [observed version | unknown]
- **Native Subagents:** [available | unavailable | unknown]
- **Separate Sessions:** [available | unavailable | unknown]
- **Worktrees / Isolated Roots:** [available | unavailable | unknown]
- **Hooks / Tool Guards:** [available | unavailable | unknown]
- **Sandbox / Permission Controls:** [description]
- **Observable Event Sources:** [tool log/gate log/CI/artifacts/none]
- **MCP / Plugin / External Tools:** [available inventory or none]
- **Known Limitations:** [list]
- **Capability Evidence:** [version/config/smoke/reference]

## Integration Profile and Admission

- **Integration Profile:** [none | official plugin | MCP | file handoff | hosted connector | direct runtime CLI | manual handoff]
- **Approved Integration IDs:** [none | stable IDs matching machine Work Block]
- **Admission Records:** [none | paths based on integration-admission-template.md]
- **Logical Functions Served:** [none | Critic/Reviewer/Verifier/Evaluator/etc.]
- **From / To Boundary:** [runtime/service endpoints]
- **Exact Tools / Actions:** [none | list]
- **Authority:** [read-only | approved write-set | reports only | other]
- **Data Sent Externally:** [none | exact content boundary]
- **Secret / Authentication Source:** [none | local runtime/keychain/env name, no values]
- **Network / External Directory Boundary:** [deny/ask/approved endpoints or paths]
- **Timeout / Cancellation / Retry:** [behavior]
- **Disable / Recovery Procedure:** [steps]
- **Integration Smoke Evidence:** [not required for none | path/result]

Rules:

- generated projects default to `none`;
- availability does not imply permission;
- every automated non-`none` integration requires an admission record;
- external runtime CLI IDs and admission paths must also be present in
  `.agent/active-work-block.json`;
- integration access does not expand the bound logical role or write-set.

## Function Bindings

| Function | Logical Role | Runtime | Model Class | Actual Model | Isolation | Authority | Adapter / Integration / Launch Evidence |
|---|---|---|---|---|---|---|---|
| Orchestration | Orchestrator | [runtime] | [class] | [optional] | [level] | workflow | [reference] |
| Architecture / Specification | Architect | [runtime] | [class] | [optional] | [level] | read-only/drafts | [reference] |
| Requirements Clarification | Architect | [runtime] | [class] | [optional] | [level] | read-only/drafts | [reference] |
| Requirements Quality Review | Reviewer specialization | [runtime] | [class] | [optional] | [level] | read-only/evidence | [reference] |
| Define Consistency Analysis | Read-only analysis specialization | [runtime] | [class] | [optional] | [level] | read-only/evidence | [reference] |
| Critic | Critic | [runtime] | [class] | [optional] | [level] | read-only | [reference] |
| Implementation | Coder | [runtime] | [class] | [optional] | [level] | write-set | [reference] |
| Review | Reviewer | [runtime] | [class] | [optional] | [level] | read-only | [reference] |
| Verification | Verifier | [runtime] | [class] | [optional] | [level] | read-only | [reference] |
| Evaluation | Verifier/Evaluator specialization | [runtime] | [class] | [optional] | [level] | read-only/evidence | [reference] |
| Drift Audit | Reviewer/Verifier specialization | [runtime] | [class] | [optional] | [level] | read-only | [reference] |

Use `not required` for functions legitimately skipped by profile and triggers.
Model/provider/integration names do not define roles or authority.

## Degraded / Fallback Plan

- **Missing capability:** [none | capability]
- **Preferred execution:** [method]
- **Fallback:** [same-context | separate-session | alternate runtime | manual | other]
- **Degraded label:** [none | exact label]
- **Residual limitation:** [what independence/evidence is not established]
- **Follow-up required:** [yes/no]

## Skills

- **Checked:** [list]
- **Matched:** [list]
- **Used:** [list]
- **Skipped:** [list with reasons]

## Implementation Plan

For formal traceable work, use `docs/templates/traceable-tasklist-template.md`
and `scripts/validate-define-traceability.py` instead of duplicating the detailed
task graph here. Keep this table as the Work Block-level execution summary.

| Task | Owner Role | Write-Set | Dependencies | Expected Evidence | Status |
|---|---|---|---|---|---|
| [Task] | [role] | [paths] | [deps] | [evidence] | [planned] |

## Acceptance Criteria

- [ ] [AC-001]
- [ ] [AC-002]

## Assurance Plan

### Requirements Quality

- **Required:** [yes/no; profile/risk trigger]
- **Specification subject:** [path/revision]
- **Expected report:** [docs/reports/requirements/<work-block-id>.md]
- **Required verdict:** [READY | valid documented skip]

### Define Consistency

- **Required:** [yes/no; profile/risk trigger]
- **Inputs:** [spec/architecture/plan/tasklist/write-set/traceability result]
- **Expected result/report:** [reference]
- **Required verdict:** [READY | valid documented skip]

### Critic

- **Required:** [yes/no; trigger]
- **Inputs:** [spec/plan/risk/topology/requirements-quality/consistency/integration admissions/evaluation design]
- **Expected report:** [path]

### Independent Review

- **Required:** [yes/no; trigger]
- **Frozen diff:** [reference]
- **Review dimensions:** [correctness/security/architecture/maintainability/integration/evaluation boundaries]
- **Expected report:** [path]

### Technical Verification

- **Canonical checks:** [exact commands/flows]
- **Runtime/browser/API/integration smoke:** [required/optional/not applicable]
- **Positive and negative cases:** [list]
- **Evidence expected:** [logs/screenshots/report/artifacts]
- **Allowed fallback checks:** [narrower checks and residual risk]
- **Skipped checks:** [none | reason]

### Agent Evaluation

- **Required:** [yes/no; trigger]
- **Evaluation ID / Plan:** [not required | ID and path]
- **Subject/Frozen Revision:** [revision]
- **Deterministic Checks:** [criterion IDs and commands]
- **Output Criteria:** [criterion IDs, thresholds, evaluator types]
- **Trajectory Requirements:** [required/prohibited observable events]
- **Event Sources:** [paths/logs/artifacts]
- **Rubric Revision:** [revision]
- **Benchmark/Dataset Revision:** [revision | not-applicable]
- **LM Judge Policy:** [disabled | identity/prompt revision/calibration]
- **Isolation:** [actual or required boundary]
- **Expected Report:** [docs/reports/evaluations/<id>.json]
- **No Hidden Reasoning:** [confirmed; observable events only]

### Specification Drift Audit

- **Required:** [yes/no; trigger]
- **Inputs:** [spec/decisions/plans/diff/tests/evals/docs]
- **Expected report:** [path]
- **Valid skip reason:** [Quick Fix only, or not applicable]

## Navigation and Documentation Impact

- **Files added/moved/removed:** [none | list]
- **PROJECT_MAP update:** [yes/no; why]
- **FILE_REGISTRY update:** [yes/no; why]
