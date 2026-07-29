# Agent Routing Roster

> Maps logical SDLC roles to authority, responsibilities, and portable skills.
> Runtime-specific agent names, models, plugins, judges, and launch commands
> belong in adapters or Work Block evidence. They do not create governance roles.

## Core Logical Roles

| Role | Responsibility | Default authority | Core skills |
|---|---|---|---|
| Orchestrator | Frame Work Blocks, select profiles/evaluation posture, manage scope, route functions, consolidate evidence, enforce gates, close out | Workflow artifacts and approved coordination paths | task-decomposition, ssot-sync-closeout, memory-bank-manager, subagent-mission-brief, orchestrator-log |
| Architect | Discover constraints, propose architecture, draft specifications and implementation/evaluation plans | Read-only by default; approved draft paths | architecture-discovery, technical-discovery, project-estimation |
| Critic | Challenge scope, assumptions, risk, routing, verification, and evaluation design before implementation | Read-only; critic report path only | critic-review |
| Coder | Implement the approved plan inside one explicit write-set | Approved source write-set only | scoped-coder, scoped-commit-guard, shell-context-guard, systematic-debugging |
| Reviewer | Inspect the frozen diff for defects, regressions, security, architecture, and maintainability | Read-only; review report path only | reviewer, security-audit-triage |
| Verifier | Test acceptance criteria and synthesize deterministic/output/trajectory evidence | Read-only for source/runtime; verification/evaluation artifacts only | verifier, webapp-testing, security-verification-gate |

## Temporary Specializations

Specializations narrow focus but never expand authority. Examples:

- Architecture Analyst
- Product Analyst
- Frontend Reviewer
- Backend Coder
- Security Reviewer
- QA Verifier
- **Evaluator** — executes an approved output/trajectory evaluation plan
- Documentation Analyst
- Release Analyst
- Specification Drift Auditor

Evaluator is normally a read-only Verifier specialization. It may write only
approved evaluation plans/reports/events or other evidence paths. It cannot edit
implementation source, approve product scope, waive deterministic failures, open
authority/integration/deployment gates, or request hidden reasoning/private
chain-of-thought.

A drift audit is normally a read-only Reviewer or Verifier specialization using
`spec-drift-audit`. Add a permanent role only when the project requires a distinct
authority model.

## Runtime Binding

The active Work Block records how each logical function executes:

```yaml
function: evaluation
logical_role: verifier
specialization: evaluator
runtime: codex
model_class: assurance
isolation: separate-session
authority: read-only-evidence
adapter: runtimes/codex
evaluation_plan: docs/evals/feature-x/plan.json
event_source: docs/evals/feature-x/events.jsonl
```

Valid runtimes are project-defined. Model or judge names must not be used as role
names. Evaluation plan and event-source availability do not grant write authority.

## Isolation Levels

From weakest to strongest:

1. `same-context`
2. `separate-subagent`
3. `separate-session`
4. `separate-worktree`
5. `separate-runtime`
6. `independent-readonly-root`
7. `os-isolated`

The Work Block chooses the minimum sufficient level and records the actual
boundary. Different model names in one context do not establish independence.
Trajectory evaluation also records the actual observable-event source.

## Core Skill and Contract Routing

| Skill / contract | Route when |
|---|---|
| `architecture-discovery` | Architecture or subsystem boundary is unclear |
| `technical-discovery` | Repository structure/dependencies need inspection |
| `task-decomposition` | A goal needs bounded Work Blocks/write-sets |
| `project-estimation` | Scope, risk, dependencies, verification/evaluation cost need classification |
| `critic-review` | Define-stage decisions require independent challenge |
| `scoped-coder` | Approved file-changing implementation work |
| `reviewer` | Frozen diff requires independent review |
| `verifier` | Acceptance criteria or technical contracts require evidence |
| `governance/evaluation.md` + `validate-evaluation.py` | Output or observable trajectory evaluation is required |
| `spec-drift-audit` | Spec, decisions, plans, code, tests/evals, and docs need alignment checking |
| `systematic-debugging` | Root cause must be established before a fix |
| `ssot-sync-closeout` | Closeout must synchronize normative/derived artifacts |
| `merge-protocol` | Parallel results require consolidation/conflict handling |
| `subagent-mission-brief` | Work is delegated to another agent/session/runtime/team |
| `context-snapshot` | State must be frozen before parallel work/stage transition |
| `scoped-commit-guard` | Staging/commit scope must be protected |
| `shell-context-guard` | Shell location/target/side effects need explicit checking |
| `skill-library-maintenance` | GitHub source checks and safe skill adaptation |

## Evaluation Routing Rules

Route evaluation when any condition applies:

- materially non-deterministic output;
- autonomous tool or path selection;
- trajectory compliance is an acceptance condition;
- consequential automation depends on process evidence;
- benchmark/dataset/rubric/LM judge is part of acceptance;
- Managed/Assured/Distributed profile requires it by risk.

Route deterministic criteria to code/rule checks. Route non-deterministic output
criteria to a human, rule-based evaluator, or approved LM judge. Route trajectory
criteria only when observable event sources exist. Missing event sources produce
`BLOCKED`/`UNVERIFIED`, never inferred pass.

## Domain Skill Routing

Domain skills are selected only when relevant. Catalog visibility does not grant
tool, file, runtime, data, deploy, evaluation, or Hard Stop authority.

Examples:

- frontend/design skills for UI work;
- security triage/hardening for security-sensitive work;
- MCP/handoff skills for integrations;
- media production skills for video/motion assets.

## Routing Priority

1. Owner instruction, authority, Hard Stops.
2. Approved specification and architecture decisions.
3. Work Block scope, write-set, risk, evaluation posture, isolation.
4. Critic gate when triggered.
5. Coder implementation and observable event capture.
6. Independent Reviewer.
7. Verifier deterministic evidence.
8. Evaluator output/trajectory evidence when required.
9. Specification Drift Audit when triggered.
10. Consolidation and closeout.

## Degraded Execution

When a required capability or event source is unavailable:

1. preserve the logical function;
2. choose the strongest approved fallback;
3. record actual runtime, isolation, event source, and limitation;
4. label the result degraded, blocked, or unverified as applicable;
5. never upgrade a verdict because a preferred agent/model/judge was unavailable.
