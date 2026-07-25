# Agent Routing Roster

> Maps logical SDLC roles to authority, responsibilities, and portable skills.
> Runtime-specific agent names, models, plugins, and launch commands belong in
> runtime adapters. They do not create new governance roles.

## Core Logical Roles

| Role | Responsibility | Default authority | Core skills |
|---|---|---|---|
| Orchestrator | Frame Work Blocks, select governance profile, manage scope, route functions, consolidate evidence, enforce gates, close out | Workflow artifacts and approved coordination paths | task-decomposition, ssot-sync-closeout, memory-bank-manager, subagent-mission-brief, orchestrator-log |
| Architect | Discover constraints, propose architecture, draft specifications and plans | Read-only by default; draft artifact paths when approved | architecture-discovery, technical-discovery, project-estimation |
| Critic | Challenge scope, assumptions, risk classification, routing, and verification design before implementation | Read-only; critic report path only | critic-review |
| Coder | Implement the approved plan inside one explicit write-set | Approved source write-set only | scoped-coder, scoped-commit-guard, shell-context-guard, systematic-debugging |
| Reviewer | Inspect the frozen diff for defects, regressions, security risks, architecture violations, and maintainability problems | Read-only; review report path only | reviewer, security-audit-triage |
| Verifier | Test acceptance criteria and observable contracts with reproducible evidence | Read-only for source/runtime; verification artifacts only | verifier, webapp-testing, security-verification-gate |

## Temporary Specializations

Specializations narrow focus but never expand authority. Examples:

- Architecture Analyst
- Product Analyst
- Frontend Reviewer
- Backend Coder
- Security Reviewer
- QA Verifier
- Documentation Analyst
- Release Analyst
- Specification Drift Auditor

A drift audit is normally assigned to a read-only Reviewer or Verifier
specialization using `spec-drift-audit`. Add a permanent role only when the
project requires a distinct authority model.

## Runtime Binding

The active Work Block records how each logical function is executed:

```yaml
function: verification
logical_role: verifier
runtime: codex
model_class: balanced_engineering
isolation: separate-subagent
authority: read-only
adapter: runtimes/codex
```

Valid runtime values are project-defined, for example `codex`, `claude-code`,
`opencode`, `generic`, or another approved adapter. Model names must not be used
as role names.

## Isolation Levels

From weakest to strongest:

1. `same-context`
2. `separate-subagent`
3. `separate-session`
4. `separate-worktree`
5. `separate-runtime`
6. `independent-readonly-root`
7. `os-isolated`

The Work Block chooses the minimum sufficient level. A runtime capability never
justifies claiming a stronger isolation level than was actually used.

## Core Skill Routing

| Skill | Route when |
|---|---|
| `architecture-discovery` | Non-trivial architecture or subsystem boundary is unclear |
| `technical-discovery` | Repository structure, dependencies, or implementation constraints need inspection |
| `task-decomposition` | A goal must be converted into bounded Work Blocks or write-sets |
| `project-estimation` | Scope, complexity, dependencies, or verification cost must be classified |
| `critic-review` | Define-stage decisions require independent challenge |
| `scoped-coder` | Any approved file-changing implementation work |
| `reviewer` | A frozen diff requires independent defect and maintainability review |
| `verifier` | Acceptance criteria or technical contracts require evidence |
| `spec-drift-audit` | Spec, architecture, code, tests, and docs require alignment checking |
| `systematic-debugging` | Root cause must be established before a fix |
| `ssot-sync-closeout` | Closeout must synchronize normative and derived artifacts |
| `merge-protocol` | Parallel results must be consolidated and conflicts resolved |
| `subagent-mission-brief` | Work is delegated to a subagent, session, runtime, or external team |
| `context-snapshot` | State must be frozen before parallel work or a stage transition |
| `scoped-commit-guard` | Staging or commit scope must be protected in a dirty worktree |
| `shell-context-guard` | Shell location, target, or side effects require explicit checking |

## Domain Skill Routing

Domain-specific skills are selected only when relevant to the active Work Block.
The skill catalog is metadata for discovery; listing a skill does not grant tool,
file, runtime, data, deploy, or Hard Stop authority.

Examples:

- frontend/design skills for UI work;
- security triage and hardening skills for security-sensitive work;
- MCP and handoff skills for runtime integrations;
- media production skills for generated video or motion assets.

## Routing Priority

1. Owner instruction, authority, and Hard Stops.
2. Active specification and accepted architecture decisions.
3. Work Block scope, write-set, risk, and required isolation.
4. Critic gate before implementation when triggered.
5. Coder implementation.
6. Independent Reviewer.
7. Verifier evidence.
8. Specification Drift Audit when triggered.
9. Consolidation and closeout.

## Degraded Execution

When a required native capability is unavailable:

1. preserve the logical function;
2. choose the strongest available fallback from the runtime adapter;
3. record actual runtime, isolation, and limitation;
4. label the result degraded;
5. never upgrade a blocked or unverified verdict because a preferred agent or
   model was unavailable.
