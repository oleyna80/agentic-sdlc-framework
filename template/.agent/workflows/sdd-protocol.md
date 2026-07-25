# SDLC Protocol — Runtime-Neutral Stage Contract

> Canonical generated-project lifecycle. It defines management functions,
> evidence, gates, and state transitions independently of the agent runtime.

## Core Principle

The lifecycle requires functions and artifacts, not a fixed number of agents.
One capable runtime may execute several functions for low-risk work. Higher-risk
work requires stronger independence as recorded in the active Work Block.

The four macro-stages are:

```text
Stage 0 — Define
Stage 1 — Execute
Stage 2 — Assure
Stage 3 — Close
```

## State Model

Stage execution state:

```text
blocked -> ready -> in_progress -> completed
   ^                              |
   +------------- retry ----------+
```

Track gates and outcomes separately:

- **Write gate:** `READY | BLOCKED`
- **Critic gate:** `READY | BLOCKED | SKIPPED | DEGRADED`
- **Review gate:** `READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED | SKIPPED`
- **Verification verdict:** `READY | BLOCKED | UNVERIFIED`
- **Drift gate:** `READY | BLOCKED | UNVERIFIED | SKIPPED`
- **Closeout mode:** `success-closeout | reporting-only`

Only all required gates in a passing state permit `success-closeout`.
`BLOCKED`, `UNVERIFIED`, or unresolved `CHANGES_REQUIRED` permits diagnostics,
corrective planning, evidence capture, and reporting-only closeout. It does not
permit merge-ready, deploy-ready, release-ready, or completed-task claims.

## Governance Profiles

The Work Block selects the smallest sufficient governance profile:

- **Advisory:** read-only analysis; no repository mutation.
- **Controlled:** one bounded executor, explicit scope/write-set, basic review and checks.
- **Managed:** approved specification and plan, Critic, Reviewer, Verifier, durable evidence.
- **Assured:** stronger independence, threat/risk analysis where relevant, drift audit, runtime evidence.
- **Distributed:** multiple runtimes/worktrees/teams with explicit handoff and consolidation.

Runtime choice is separate from governance profile.

---

# Stage 0 — Define

## Owner

Orchestrator. Architect and Critic functions may be delegated.

## Purpose

Convert a request into an approved, bounded, auditable Work Block before source
changes begin.

## Required Inputs

- current Owner instruction;
- repository state and relevant current source;
- applicable governance and runtime adapter documents;
- relevant accepted specifications and architecture decisions;
- current operational context when resuming work.

## Activities

1. **Frame the objective**
   - expected final result;
   - measurable done criteria;
   - in-scope and out-of-scope boundaries.

2. **Resolve source of truth**
   - identify or create the active specification;
   - record specification status and revision;
   - identify accepted architecture decisions;
   - treat plans and tasklists as derived artifacts.

3. **Classify risk and authority**
   - side-effect class;
   - DB/data action mode;
   - Hard Stops;
   - rollback/recovery expectations;
   - required governance profile.

4. **Negotiate runtime capability**
   - active runtime and adapter;
   - subagent/session/worktree support;
   - hooks and sandbox availability;
   - model class and budget posture;
   - actual isolation available;
   - fallback path for missing capability.

5. **Define execution topology**
   - logical functions required;
   - runtime binding for each function;
   - one Coder per write-set;
   - parallel work only for independent scopes;
   - consolidation owner.

6. **Route skills**
   - checked;
   - matched;
   - used;
   - skipped with reason.

7. **Create the implementation plan**
   - ordered tasks;
   - explicit write-set;
   - dependencies;
   - verification plan;
   - review and drift triggers.

8. **Run Critic function when triggered**
   - challenge scope, assumptions, authority, risk, topology, and verification design;
   - record `APPROVE`, `SUPPLEMENT`, or `RECONSIDER`;
   - rerun Define for material gaps.

## Critic Triggers

Critic is required when any condition applies:

- 3 or more planned implementation files;
- production-code side effects or higher;
- new architecture boundary, runtime topology, or external integration;
- authentication, authorization, payment, DB/schema, deploy, infrastructure,
  webhook, provider, security, or client-facing behavior;
- 2 or more matched skills are skipped;
- Assured or Distributed profile;
- Owner or Orchestrator identifies material ambiguity.

A skip must be explicit and evidence-based. Same-context fallback is labelled
`DEGRADED`; it is not described as independent.

## Exit Conditions

- active specification identified and approved or marked with explicit approval requirement;
- architecture baseline identified;
- Work Block complete;
- write-set approved;
- runtime capability and isolation recorded;
- verification/review/drift plan recorded;
- Critic gate resolved when triggered;
- write gate `READY`.

No source changes are allowed while the write gate is `BLOCKED`.

---

# Stage 1 — Execute

## Owner

Coder. Exactly one write-capable Coder per write-set.

## Entry Conditions

- write gate `READY`;
- approved specification and implementation plan;
- explicit write-set;
- side-effect and Hard Stop classification;
- required runtime capability available or an approved degraded fallback recorded.

## Activities

1. Read the active specification, plan, acceptance criteria, and relevant source.
2. Implement only inside the approved write-set.
3. Preserve existing project patterns unless the specification approves a change.
4. Do not silently change requirements or architecture.
5. When a legitimate requirement change is discovered:
   - stop the affected implementation path;
   - record the proposed specification change;
   - return to Define for approval;
   - update plan/tasklist only after the specification decision.
6. Run scoped self-checks.
7. Freeze the implementation diff for assurance.
8. Report one outcome:
   - `DONE`;
   - `DONE_WITH_CONCERNS`;
   - `NEEDS_CONTEXT`;
   - `BLOCKED`.

## Exit Conditions

- planned changes implemented or blockers documented;
- no unapproved scope expansion;
- frozen diff or changed-file list available;
- self-check evidence recorded;
- implementation result handed to Stage 2.

A failed Execute stage blocks assurance from passing. Stage 2 may still inspect
partial work for diagnostics, but cannot produce a successful verdict.

---

# Stage 2 — Assure

Stage 2 contains three distinct functions:

```text
2A Independent Review
2B Technical Verification
2C Specification Drift Audit
```

They may be executed by separate agents or by separate passes of one runtime,
but actual independence and limitations must be recorded.

## 2A — Independent Review

### Purpose

Inspect the frozen diff for engineering quality and risk.

### Reviewer Checks

- defects and regressions;
- incorrect assumptions and edge cases;
- architecture and dependency violations;
- security and privacy risks;
- maintainability and unnecessary complexity;
- missing tests or observability;
- scope expansion;
- unsafe generated boilerplate or prompt-shaped abstractions.

### Verdicts

- `READY`
- `CHANGES_REQUIRED`
- `BLOCKED`
- `UNVERIFIED`

`CHANGES_REQUIRED` returns the Work Block to Execute for correction, followed by
review of the updated frozen diff.

## 2B — Technical Verification

### Purpose

Demonstrate that acceptance criteria and observable contracts hold.

### Lite Tier

- changed files match scope;
- targeted types/lint/build checks;
- relevant tests pass;
- no obvious regression.

### Standard Tier

Lite plus relevant:

- route and navigation contracts;
- API/schema contracts;
- positive and negative cases;
- runtime/dev-server smoke;
- error handling and logging;
- maintainability baseline;
- secret and injection baseline.

### Full Tier

Standard plus relevant:

- threat-model validation;
- security checklist;
- dependency/security scan classification;
- actual served response/header checks;
- auth/origin/CSRF/webhook guards;
- migration and rollback checks;
- independent runtime evidence;
- production-like but non-destructive smoke where approved.

### Verdicts

- `READY`
- `BLOCKED`
- `UNVERIFIED`

Unavailable evidence is `UNVERIFIED`, not `READY`.

## 2C — Specification Drift Audit

### Purpose

Compare:

```text
Specification <-> Architecture decisions <-> Plan <-> Code <-> Tests <-> Documentation
```

Use `spec-drift-audit` and the standard drift report template.

### Required Triggers

- public behavior, route, API, schema, persistence, or runtime contract changed;
- auth, payment, DB, provider, webhook, security, or architecture changed;
- specification changed during implementation;
- behavior was added outside the approved plan;
- 3 or more implementation files changed;
- Assured or Distributed profile.

### Verdicts

- `ALIGNED` -> drift gate `READY`;
- `ALIGNMENT_REQUIRED` -> drift gate `BLOCKED` until corrected and rerun;
- `BLOCKED` -> drift gate `BLOCKED`;
- `UNVERIFIED` -> drift gate `UNVERIFIED`.

A Quick Fix may skip drift audit only when it has no behavior, contract, schema,
security, runtime, architecture, or governance impact.

## Isolation Requirements

Minimum expected isolation:

| Work type | Review / verification expectation |
|---|---|
| Controlled, low-risk | separate pass; same-context allowed but recorded |
| Managed, non-sensitive | separate-subagent or separate-session preferred |
| Assured or sensitive | independent-readonly-root or separate-runtime preferred |
| credentials, live data, deploy mutation | os-isolated where practical and no production credentials for read-only assurance |
| parallel writers | separate-worktree per write-set plus consolidation |

## Stage 2 Exit Conditions

- review gate resolved;
- verification verdict recorded;
- drift gate resolved when triggered;
- findings include evidence and inspection gaps;
- corrections rerun through the applicable assurance functions;
- parallel results consolidated when relevant.

---

# Stage 3 — Close

## Owner

Orchestrator.

## Activities

1. Determine closeout mode.
2. Synchronize derived artifacts with the approved specification and delivered state.
3. Update task status.
4. Promote durable, reusable engineering knowledge.
5. Record operational results and residual risks.
6. Produce closeout report and Owner summary.

## Source-of-Truth Synchronization Order

1. current Owner instruction or approved change request;
2. approved specification;
3. accepted architecture decisions and external contracts;
4. approved implementation plan;
5. tasklist;
6. review, verification, drift, and closeout reports;
7. engineering memory;
8. operational memory and logs.

Plans and tasklists never silently override an approved specification.

## Successful Closeout Conditions

- implementation completed inside scope;
- review gate `READY` or valid documented skip;
- verification verdict `READY`;
- drift gate `READY` or valid documented skip;
- required Hard Stop actions either not performed or explicitly approved;
- residual risks documented;
- normative and derived artifacts synchronized.

Otherwise use `reporting-only` and keep the task blocked or incomplete.

---

# Quick-Fix Path

A Quick Fix is allowed only when all are true:

- at most 2 implementation files;
- no behavior, route, API, schema, persistence, security, architecture, runtime,
  dependency, governance, or public contract impact;
- no Hard Stop;
- rollback is trivial;
- targeted checks are available.

Flow:

```text
Scope statement -> Implement -> targeted self-review/checks -> sync -> close
```

The Orchestrator must record why the full lifecycle was not required.

---

# Failure and Degraded Modes

- A failed stage blocks downstream success claims.
- Work may continue for diagnostics, corrective planning, evidence capture, or reporting.
- Missing subagent/model/plugin capability does not remove the logical function.
- Use the strongest available fallback and record actual runtime and isolation.
- A degraded review cannot upgrade a blocked verification result.
- No agent may grant itself authority because a tool is technically available.
