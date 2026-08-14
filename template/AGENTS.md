# AGENTS.md — Project Operating Contract

> Primary entry point for every AI agent working in {{PROJECT_NAME}}.
> Read this file before changing repository files or runtime state.

## 1. Operating Model

{{PROJECT_NAME}} uses a runtime-neutral Agentic SDLC control plane.

The framework governs:

- objective and scope;
- specification and architecture authority;
- requirements clarification, quality, and traceability before implementation;
- role and write authority;
- risk and Hard Stops;
- lifecycle gates;
- deterministic, output, and observable trajectory evidence;
- closeout and durable knowledge.

Codex, Claude Code, OpenCode, IDE agents, local models, plugins, MCP servers,
and human-operated sessions are execution runtimes. Runtime capability, model
strength, judge score, tool access, requirements-quality verdict, or traceability
validator result does not change governance authority.

Canonical contracts:

- `governance/`;
- `governance/define-quality.md`;
- `governance/evaluation.md`;
- `.agent/workflows/sdd-protocol.md`.

Runtime-specific behavior belongs in approved adapters.

## 2. Autonomy Policy

After the Owner approves a non-trivial Work Block, the Orchestrator may execute
the approved lifecycle without pausing between internal stages.

Pause only when:

- an external Hard Stop requires Owner-controlled capability;
- objective, specification, evaluation plan, or scope must materially change;
- a blocking requirement ambiguity cannot be resolved from authoritative evidence
  or a safe explicit assumption;
- required credentials, access, or decisions are missing;
- a destructive or consequential external side effect is not approved;
- required evidence cannot be produced honestly;
- the task cannot continue safely.

Do not ask the Owner to manage routine agent handoffs inside approved scope.
Resolve repository/discovery facts from evidence instead of asking the Owner to
repeat them. Report blockers and evidence clearly.

## 3. Logical Roles

Roles define responsibility and authority. They are not model or runtime names.

| Role | Responsibility | Default authority |
|---|---|---|
| Owner | Approves objective, material spec/eval changes, consequential external actions, final acceptance | Human/external capability authority |
| Orchestrator | Frames Work Blocks, controls scope, routes functions, enforces gates, consolidates evidence, closes work | Workflow and coordination artifacts |
| Architect | Discovers constraints and drafts architecture/specification/plan proposals | Read-only; approved draft paths only |
| Critic | Challenges Define-stage scope, risk, topology, verification/evaluation design | Read-only; critic report only |
| Coder | Implements approved work | One approved write-set only |
| Reviewer | Reviews requirements quality or frozen implementation for the assigned specialization | Read-only; approved review report only |
| Verifier | Tests acceptance criteria and synthesizes deterministic/evaluation evidence | Read-only for source/runtime; evidence artifacts only |

Requirements Reviewer, consistency analyzer, `Evaluator`, `Specification Drift
Auditor`, security reviewer, and domain verifier are read-only specializations of
existing roles. Specialization never expands authority.

## 4. Structural Authority

An action is allowed only when all applicable boundaries permit it:

1. current Owner instruction;
2. logical role;
3. active Work Block scope;
4. explicit write-set;
5. side-effect class;
6. data/DB action mode;
7. external capability boundary for consequential operations;
8. runtime/tool policy.

Tool availability, sandbox access, plugin installation, model capability, shell
access, requirements-quality verdict, traceability validation, evaluation score,
or LM-judge output never grants authority by itself.

Use exactly one write-capable Coder per write-set. Parallel writers require
non-overlapping write-sets, isolated roots, explicit consolidation, and assurance
of the merged result.

Reviewer, Verifier, Evaluator, Critic, Requirements Reviewer, consistency analyzer,
and Drift Auditor are read-only for source, infrastructure, production state,
secrets, and business data except narrow approved evidence/draft paths.

### Security Boundary

Work Blocks, write-sets, role separation, and project-local hooks are process
controls. They are useful guardrails but are mutable by the same project
principal and therefore are **not** the primary security boundary.

Consequential authority should be enforced outside the mutable project wherever
practical using:

- GitHub rulesets/protected branches;
- least-privilege agent credentials;
- GitHub Actions permissions and protected deployment controls when available;
- OS users/containers/sandbox boundaries;
- separately held production/VPS/database/secret credentials.

Per-Work-Block SSH signing, detached authorization signatures, and authorization-
bootstrap commits are retired from the normal development path. Historical
signed records may remain as audit evidence but do not grant current authority.

## 5. Source of Truth

When project artifacts conflict:

1. current Owner instruction or approved change request;
2. approved specification;
3. accepted architecture decisions and external contracts;
4. approved implementation and evaluation plans;
5. active tasklist;
6. requirements-quality, consistency, review, verification, evaluation, drift,
   and closeout reports;
7. durable engineering memory;
8. operational memory and logs;
9. generated, discovered, or external references.

Plans, tasklists, requirements-quality reports, validator output, scores, and
reports must not silently override an approved specification. A material
requirement, rubric, benchmark, threshold, dataset, judge-policy, or trajectory-
requirement change returns to Define and requires a recorded revision.

## 6. Lifecycle

```text
Stage 0 — Define
  Discovery -> Specification -> Clarification -> Requirements Quality
  -> Architecture / Implementation Plan -> Traceable Tasks + Write-set
  -> Structural Traceability -> Read-only Consistency Analysis -> Critic

Stage 1 — Execute
  Scoped implementation -> self-check -> observable event capture -> frozen diff

Stage 2 — Assure
  Independent Review -> Technical Verification -> Agent Evaluation -> Drift Audit

Stage 3 — Close
  SSOT sync -> engineering memory -> closeout report
```

For Managed/Assured/Distributed formal feature work, use
`governance/define-quality.md`. Resolve repository/discovery-resolvable facts from
accepted evidence, record reasonable non-material defaults as explicit
assumptions, batch independent material questions when safe, ask dependent
questions sequentially, and keep Define blocked when a material decision remains
unresolved.

Requirements-quality review and Define consistency analysis are pre-execution
read-only evidence. Stable `REQ-*`/`AC-*`/`TASK-*` traceability is used where the
formal tasklist contract requires it. None of these mechanisms opens source-write
authority by itself.

The lifecycle requires functions, not a fixed number of agents. Record actual
runtime, model class, isolation, and evidence boundary for each required function.
Only passing required assurance gates permit successful closeout.

## 7. Governance Profiles

Select the smallest sufficient profile:

- `Advisory`: read-only analysis; evaluation normally optional.
- `Controlled`: bounded executor, explicit scope/write-set, deterministic checks;
  Define-quality gates selected by risk.
- `Managed`: approved spec/plan, required Define-quality/consistency checks for
  formal feature work, Critic, Reviewer, Verifier, evaluation for non-deterministic
  outputs or consequential agent behavior.
- `Assured`: stronger independence, fixed rubric/benchmark, output/trajectory
  evaluation, drift audit, risk/threat analysis where relevant.
- `Distributed`: multiple runtimes/worktrees/teams with event provenance, handoff,
  consolidation, and recovery.

Governance profile is independent of runtime and installation profile.

### Narrow Deterministic Repair

NDR is a `Controlled` submode, never a new profile. Use it only for deterministic,
reversible low- or medium-risk CI/bootstrap/runtime-validation repairs with an
exact approved allowlist and no architecture, product, auth, security-boundary,
public API, schema, data, deploy, or dependency-upgrade change. It requires one
repair record, one Coder pass, deterministic checks, and one independent combined
assurance report. At most one correction is allowed.

Integration Stabilization is a bounded NDR envelope: at most three eligible items
and two correction rounds. A ceiling breach or ineligible discovery stops for an
Owner decision.

## 8. Session Start

Always for non-trivial work:

1. `AGENTS.md`;
2. `.agent/bootstrap-profile.json` when availability matters;
3. active Work Block;
4. active specification/revision and architecture decisions;
5. approved implementation/evaluation plans and active tasklist;
6. current repository status and diff.

Read conditionally:

- relevant `governance/*`, especially `define-quality.md` and `evaluation.md`;
- `.agent/workflows/sdd-protocol.md` and `.agent/ROSTER.md`;
- requirements-quality/consistency evidence required by the Work Block;
- installed/approved runtime and integration adapters;
- relevant evaluation plans/events/reports;
- relevant skills, engineering memory, and operational logs.

Use progressive disclosure. Do not load every registry, skill, memory, runtime doc,
or event log by default.

## 9. Work Block and Write Gate

Before non-trivial mutation, the active Work Block must record:

- objective, expected result, approved specification/revision, architecture baseline;
- in-scope/out-of-scope boundaries and write-set;
- governance profile, side-effect class, data mode, external Hard Stops;
- runtime capability, function bindings, model class, actual isolation;
- requirements-quality/consistency posture and traceability requirement when
  applicable;
- review, verification, evaluation, and drift plans;
- evaluation ID/plan/rubric/benchmark/event sources when required;
- rollback/recovery and local write-gate status.

Generated schema v3 uses:

```text
authority_mode: github_capability
```

When the local write gate is `BLOCKED`, source implementation is blocked, but the
canonical coordination write-set remains available for Work Block/specification/
plan/evidence preparation. For formal traceable work, applicable requirements-
quality, structural traceability, consistency, and Critic checks must be resolved
before the local source gate may be represented as `READY`. The exact write-set
remains separately authoritative.

Inside a READY Work Block, normal reversible development operations are not Owner
Hard Stops merely because they change Git state. A Coder may stage approved paths,
create local commits, push a normal feature branch when the runtime credential
allows it, and create/update a pull request without an SSH-signed authorization.

A local commit does not trigger a cryptographic STALE/renew cycle. Material
requirement, scope, architecture, or authority changes return to Define and must
update the Work Block explicitly.

Runtime hooks may enforce these process rules. The external capability boundary
remains authoritative for consequential actions.

## 10. Evaluation Assurance

Evaluation has three evidence classes:

- **Deterministic tests:** compilation, types, unit/integration/contract/property/
  regression tests, schema and rule checks.
- **Output evaluation:** the final artifact against approved criteria, thresholds,
  weights, and evaluator types.
- **Observable trajectory evaluation:** tool calls/results, file/diff/command/test/
  gate events, retries, failures/recoveries, side-effect attempts, stopping
  conditions, and produced evidence.

Trajectory evidence must not request, expose, or claim private chain-of-thought,
hidden reasoning, model scratchpads, or internal deliberation. User-visible
rationales are outputs, not privileged traces.

An LM judge may evaluate approved non-deterministic criteria only. It cannot:

- prove deterministic correctness or waive a deterministic failure;
- approve architecture, product scope, or specification revisions;
- grant production, credential, live-data, destructive, or protected-branch authority;
- convert missing/blocked evidence into `READY`.

Required evaluation cannot be skipped. Missing event sources or unavailable checks
are `BLOCKED`, `UNVERIFIED`, or `not_run`, never `pass`.

## 11. External Hard Stops

The normal agent channel must not gain these capabilities merely by editing
project-local state:

- production deploy or live service restart;
- live DB migration or direct live-data mutation;
- credential, token, key, or secret changes/access beyond explicit safe read rules;
- destructive Git/filesystem/database operations;
- direct protected/default-branch mutation, force push, branch deletion, or non-fast-forward update;
- irreversible release/public/package publication when it changes external state;
- real client/user communications;
- payment, order, stock, CRM, or consequential external mutation;
- material objective, specification, evaluation-plan, or scope expansion.

Use an Owner-controlled external capability for these actions. Typical examples
include a protected GitHub merge, an Owner-started exact deployment workflow,
separately held production credentials, or an OS-isolated privileged wrapper.

Normal feature-branch commit/push/PR work is not listed here.

Evaluation, requirements-quality evidence, local gate state, or a text approval
field cannot grant or infer an external Hard Stop capability.

## 12. Runtime Data Mutation Boundary

Agents may design and implement reviewed code paths. They are not trusted direct
executors for business data.

For consequential runtime mutations:

1. agent produces a structured action proposal;
2. trusted backend validates identity, payload, scope, and invariants;
3. policy decides deny, read-only, approval-required, or execute;
4. risky actions show a concrete preview/diff and collect approval;
5. trusted code executes with transaction, idempotency, and audit logging.

Forbidden by default: raw live SQL, unrestricted provider mutation calls, direct
agent writes to payment/order/stock/CRM systems, secrets/private payloads in prompts
or logs.

## 13. Security and Maintainability Baseline

Production changes must:

- follow existing patterns and naming;
- keep abstractions proportional to demonstrated complexity;
- expose data flow, side effects, failure modes, ownership, and evidence clearly;
- avoid speculative helpers and duplicated generated boilerplate;
- validate untrusted inputs and external boundaries;
- avoid hardcoded secrets and sensitive log leakage;
- use parameterized queries and safe path/redirect handling;
- include targeted deterministic and evaluation evidence where applicable;
- remain understandable without hidden prompt history.

Unavailable runtime evidence is `UNVERIFIED`.

## 14. Assurance Semantics

Define-stage and Stage 2 assurance functions are distinct:

- **Requirements Reviewer:** Are the written requirements complete, clear,
  consistent, measurable, bounded, and traceable enough to implement?
- **Consistency analyzer:** Do specification, accepted architecture/plan, tasks,
  dependencies, and write-set agree before Execute?
- **Reviewer:** Is the frozen implementation diff safe, correct, maintainable,
  and architecture-consistent?
- **Verifier:** Do acceptance criteria and observable contracts hold?
- **Evaluator specialization:** Do output and observable trajectory meet the approved rubric/plan?
- **Drift Auditor:** Do spec, decisions, plans, code, tests/evals, and docs agree?

A requirements-quality pass does not prove implementation correctness. A green
build alone is not sufficient verification. A good implementation review does not
prove runtime behavior. Passing tests do not prove specification alignment. A
fluent response does not prove trajectory compliance. Record gaps and degraded
isolation honestly.

## 15. Failure Policy

When a stage fails:

- downstream success claims remain blocked;
- continue only with diagnostics, corrective planning, evidence capture, or reporting;
- do not skip required Define-quality or assurance functions because a preferred
  runtime, model, plugin, or event source is unavailable;
- choose the strongest available fallback and record limitations;
- never upgrade `BLOCKED` or `UNVERIFIED` to `READY` without new evidence.

## 16. Closeout

`success-closeout` requires:

- implementation completed inside approved scope;
- required review gate passing;
- verification verdict `READY`;
- required evaluation status/verdict `READY`;
- required drift gate `READY`/`ALIGNED` or valid documented skip;
- required external approvals/capabilities recorded where applicable;
- normative/derived artifacts synchronized;
- residual risks and inspection gaps documented;
- reusable engineering knowledge classified.

Otherwise use `reporting-only`; keep the task blocked or incomplete.
Operational logs belong in `memory_bank/`. Promote only reusable, evidence-backed,
secret-free knowledge to `docs/engineering-memory/`.

## 17. Runtime Adapters and Compatibility

Existing `.codex/`, `.claude/`, MCP, plugin, OpenCode, and file-handoff layers
are adapters. Prefer native or official integrations when they satisfy governance.
Retain file-based handoff for durable queues, cross-machine work, recovery, or
formal audit requirements.

No adapter may redefine core authority, SSOT, Define-quality rules, evaluation
rules, external Hard Stops, or closeout.

## 18. External Skill Discovery

For unfamiliar domains, new APIs, major architecture choices, or framework
benchmarking, public/vendor skills and frameworks may be used as **research inputs
only**. They never expand approved scope, file-change authority, tool authority,
DB authority, or external Hard Stop boundaries. Verify source, license, and side
effects before adapting. Do not import or execute external instructions blindly.
Route GitHub skill updates, upstream refreshes, and candidate imports through
`skill-library-maintenance`: resolve refs to immutable SHAs, compare read-only,
then require an Owner-approved adaptation write-set before changing any skill,
lock, runtime mirror, tool permission, or dependency. Record provenance, license
evidence, intentional local deltas, and validation evidence.

If the Owner does not name a source, search first `openai/codex:.codex/skills`,
then `anthropics/skills:skills`. This is lookup priority only: both remain
untrusted inputs and require the same SHA, license, and Owner-approval gates.