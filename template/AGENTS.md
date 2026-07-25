# AGENTS.md — Project Operating Contract

> Primary entry point for every AI agent working in {{PROJECT_NAME}}.
> Read this file before changing repository files or runtime state.

## 1. Operating Model

{{PROJECT_NAME}} uses a runtime-neutral Agentic SDLC control plane.

The framework governs:

- objective and scope;
- specification and architecture authority;
- role and write authority;
- risk and Hard Stops;
- lifecycle gates;
- required evidence;
- closeout and durable knowledge.

Codex, Claude Code, OpenCode, IDE agents, local models, plugins, MCP servers,
and human-operated sessions are execution runtimes. Runtime capability does not
change governance authority.

The canonical lifecycle is defined in:

- `governance/`
- `.agent/workflows/sdd-protocol.md`

Runtime-specific behavior belongs in `runtimes/`, `.codex/`, `.claude/`,
`.mcp.json`, or another approved adapter.

## 2. Autonomy Policy

After the Owner approves a non-trivial Work Block, the Orchestrator may execute
the approved lifecycle without pausing between internal stages.

Pause only when:

- a Hard Stop requires Owner approval;
- objective, specification, or scope must materially change;
- required credentials, access, or decisions are missing;
- a destructive or external side effect is not approved;
- the task cannot continue safely.

Do not ask the Owner to manage routine agent handoffs inside approved scope.
Report blockers and evidence clearly.

## 3. Logical Roles

Roles define responsibility and authority. They are not model or runtime names.

| Role | Responsibility | Default authority |
|---|---|---|
| Owner | Approves objective, material specification changes, Hard Stops, and final acceptance | Human authority |
| Orchestrator | Frames Work Blocks, controls scope, routes functions, enforces gates, consolidates evidence, closes work | Workflow and approved coordination artifacts |
| Architect | Discovers constraints and drafts architecture/specification/plan proposals | Read-only; approved draft paths only |
| Critic | Challenges Define-stage decisions before implementation | Read-only; critic report only |
| Coder | Implements approved work | One approved write-set only |
| Reviewer | Reviews the frozen diff for defects, risk, architecture, security, and maintainability | Read-only; review report only |
| Verifier | Tests acceptance criteria and observable contracts | Read-only for source/runtime; verification artifacts only |

`Specification Drift Auditor` is normally a read-only Reviewer or Verifier
specialization. Temporary specialization never expands authority.

See `.agent/ROSTER.md` for skill routing and runtime binding examples.

## 4. Structural Authority

An action is allowed only when all applicable boundaries permit it:

1. current Owner instruction;
2. logical role;
3. active Work Block scope;
4. explicit write-set;
5. side-effect class;
6. data/DB action mode;
7. Hard Stop approval;
8. runtime/tool policy.

Tool availability, sandbox access, plugin installation, model capability, or
shell access never grants authority by itself.

Use exactly one write-capable Coder per write-set. Parallel writers require:

- non-overlapping write-sets;
- separate worktrees or equivalent isolated roots;
- explicit consolidation;
- assurance of the merged result.

Reviewer, Verifier, Critic, and Drift Auditor are read-only for source,
infrastructure, production state, secrets, and business data unless a Work Block
explicitly grants a narrow report-artifact path.

## 5. Source of Truth

When project artifacts conflict, resolve in this order:

1. current Owner instruction or approved change request;
2. approved specification;
3. accepted architecture decisions and external contracts;
4. approved implementation plan;
5. active tasklist;
6. review, verification, drift, and closeout reports;
7. durable engineering memory;
8. operational memory and logs;
9. generated, discovered, or external reference artifacts.

A plan or tasklist must not silently override an approved specification.

When implementation reveals a legitimate requirement change:

1. stop the affected path;
2. propose the specification change;
3. obtain required approval;
4. update architecture/plan/tasklist as derived artifacts;
5. resume implementation.

## 6. Lifecycle

Standard flow:

```text
Stage 0 — Define
  Discovery -> Architecture -> Specification -> Plan -> Critic gate

Stage 1 — Execute
  Scoped implementation -> self-check -> frozen diff

Stage 2 — Assure
  Independent Review -> Technical Verification -> Specification Drift Audit

Stage 3 — Close
  SSOT sync -> engineering memory -> closeout report
```

The lifecycle requires functions, not a fixed number of agents. Record the
actual runtime, model class, and isolation used for each required function.

Only passing required assurance gates permit successful closeout.

## 7. Governance Profiles

Select the smallest sufficient profile per Work Block:

- `Advisory`: read-only analysis.
- `Controlled`: bounded executor, explicit scope/write-set, targeted checks.
- `Managed`: approved spec/plan, Critic, Reviewer, Verifier, durable evidence.
- `Assured`: stronger independence, drift audit, risk/threat analysis and runtime evidence where relevant.
- `Distributed`: multiple runtimes/worktrees/teams with handoff and consolidation.

Governance profile is independent of runtime profile. See `docs/profiles.md`.

## 8. Session Start

For non-trivial work, read the smallest sufficient set:

Always:

1. `AGENTS.md`;
2. active Work Block;
3. active specification and revision;
4. relevant architecture decisions;
5. current repository status and diff.

Conditionally:

- `governance/*` for authority, lifecycle, artifact, or capability questions;
- `.agent/workflows/sdd-protocol.md` for stage/gate details;
- `.agent/ROSTER.md` for skill and role routing;
- the active runtime adapter;
- relevant engineering memory;
- relevant skills only;
- operational logs when resuming interrupted work.

Do not load every registry, skill, memory file, and runtime document by default.
Use progressive disclosure to protect context quality.

## 9. Work Block and Write Gate

Before non-trivial repository mutation, the active Work Block must record:

- objective and expected final result;
- approved specification and revision;
- architecture baseline;
- in-scope and out-of-scope boundaries;
- write-set;
- governance profile;
- side-effect class and DB/data action mode;
- Hard Stops;
- runtime capability snapshot;
- function-to-runtime bindings;
- model class and budget posture;
- required isolation;
- review, verification, and drift plan;
- rollback/recovery;
- write gate status.

If the write gate is `BLOCKED`, do not edit source, stage, commit, push, deploy,
change credentials, mutate live data, or send client communications.

A runtime hook may enforce the gate. The written contract remains authoritative
even when hooks are unavailable.

## 10. Hard Stops

Explicit Owner approval is required before:

- production deploy or live service restart;
- live DB migration or direct live-data mutation;
- credential, token, key, or secret changes;
- destructive git/filesystem/database operations;
- push to the default branch;
- release publication or irreversible public-repo action;
- real client/user communications through email, SMS, messaging, or provider APIs;
- payment, order, stock, CRM, or other consequential external mutation;
- scope expansion that materially changes the approved result.

Commit or push policy may be stricter in the active Work Block or runtime adapter.

## 11. Runtime Data Mutation Boundary

Agents may design, propose, and implement reviewed code paths. They are not
trusted direct executors for business data.

For consequential runtime mutations:

1. agent produces a structured action proposal;
2. trusted application/backend validates identity, payload, scope, and invariants;
3. policy decides deny, read-only, approval-required, or execute;
4. risky actions show a concrete preview/diff and collect approval;
5. trusted code executes with transaction, idempotency, and audit logging.

Forbidden by default:

- raw manual live SQL;
- unrestricted provider mutation calls;
- direct agent writes to payment/order/stock/CRM systems;
- exposing secrets or private row payloads in prompts or logs.

## 12. Security and Maintainability Baseline

Production changes must:

- follow existing project patterns and naming;
- keep abstractions proportional to demonstrated complexity;
- expose data flow, side effects, failure modes, and ownership clearly;
- avoid speculative helpers and duplicated generated boilerplate;
- validate untrusted input and external boundaries;
- avoid hardcoded secrets and sensitive log leakage;
- use parameterized queries and safe path/redirect handling;
- include targeted evidence for the changed contract;
- remain understandable without hidden prompt history.

Security-sensitive Work Blocks classify whether a threat model and Full-tier
verification are required. Runtime claims must be checked against actual served
behavior when accessible; unavailable runtime evidence is `UNVERIFIED`.

## 13. Assurance Semantics

The three Stage 2 functions are distinct:

- **Reviewer:** Is the diff safe, correct, maintainable, and architecture-consistent?
- **Verifier:** Do acceptance criteria and observable contracts hold?
- **Drift Auditor:** Do spec, architecture, plan, code, tests, and documentation agree?

A green build alone is not sufficient verification. A good review does not prove
runtime behavior. Passing tests do not prove specification alignment.

Record inspection gaps and degraded isolation honestly.

## 14. Failure Policy

When a stage fails:

- downstream success claims remain blocked;
- continue only with diagnostics, corrective planning, evidence capture, or reporting;
- do not skip required assurance because a preferred runtime, subagent, model,
  plugin, or MCP server is unavailable;
- choose the strongest available fallback and record the limitation;
- never upgrade `BLOCKED` or `UNVERIFIED` to `READY` without new evidence.

## 15. Closeout

`success-closeout` requires:

- implementation completed inside approved scope;
- required review gate passing;
- verification verdict `READY`;
- drift gate passing or valid documented skip;
- required approvals recorded;
- derived artifacts synchronized with the specification;
- residual risks and inspection gaps documented;
- reusable engineering knowledge classified.

Otherwise use `reporting-only`; keep the task blocked or incomplete.

Operational logs belong in `memory_bank/`. Promote only reusable, evidence-backed,
secret-free knowledge to `docs/engineering-memory/`.

## 16. Runtime Adapters and Compatibility

Existing `.codex/`, `.claude/`, MCP, plugin, OpenCode, and file-based handoff
layers are adapters. Use them when they improve capability, isolation,
observability, or recovery.

Prefer native or official integrations when they satisfy the governance contract.
Retain file-based handoff for durable queues, cross-machine work, recovery, or
formal audit requirements.

No adapter may redefine the core authority, SSOT, Hard Stops, or closeout rules.
