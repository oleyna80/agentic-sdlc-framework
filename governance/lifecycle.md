# Runtime-Neutral Lifecycle

## Purpose

The lifecycle defines control functions and evidence transitions. It does not
require one permanent agent per function and does not prescribe a specific
runtime topology.

## Macro Stages

### Stage 0 — Define

Functions:

1. Intake and objective framing.
2. Discovery and repository orientation.
3. Architecture and dependency decisions.
4. Specification and acceptance criteria.
5. Implementation planning and write-set definition.
6. Critic review of scope, risks, topology, and verification design.

Required outcome:

- approved objective;
- authoritative specification or explicit quick-fix contract;
- implementation plan and write set;
- risk, side-effect, and hard-stop classification;
- verification plan;
- resolved Critic gate or documented permitted fallback.

No implementation write may begin while Stage 0 is blocked.

### Stage 1 — Execute

Functions:

1. Scoped implementation by one Coder per write set.
2. Targeted self-checks.
3. Scope and side-effect re-evaluation when new information appears.
4. Diff freeze for assurance.

Required outcome:

- implementation matches the approved write set;
- no unapproved side effect occurred;
- the diff is frozen or its exact revision is recorded;
- implementation concerns and unresolved assumptions are reported.

A material scope change returns the Work Block to Stage 0.

### Stage 2 — Assure

Functions:

1. Independent code review of the frozen diff.
2. Technical verification against acceptance criteria and contracts.
3. Specification drift audit when required.
4. Consolidation of findings and corrective-loop decision.

Review asks whether the change is safe and maintainable.

Verification asks whether the required behavior is demonstrated by evidence.

Drift audit asks whether specification, architecture decisions, plan, code,
tests, and documentation still describe the same system.

Required outcome:

- review verdict;
- verification verdict;
- drift classification when triggered;
- residual risks and inspection gaps;
- corrective action for blocking findings.

### Stage 3 — Close

Functions:

1. Classify closeout.
2. Synchronize specifications, decisions, task state, and documentation.
3. Promote reusable knowledge into engineering memory.
4. Record residual risks and follow-up Work Blocks.
5. Produce an Owner-facing report.

Only a verification verdict of `READY` permits successful closeout.

`BLOCKED` or `UNVERIFIED` permits diagnostics, corrective planning, and
reporting-only closeout. It does not permit merge-ready, deploy-ready,
release-ready, or completed claims.

## Lifecycle State

Track execution state separately from assurance verdict:

```yaml
stage: define | execute | assure | close
execution_state: blocked | ready | in_progress | completed
verification_verdict: pending | READY | BLOCKED | UNVERIFIED
closeout_mode: pending | success | reporting_only
```

A stage may be `completed` because its required activity finished while the
result remains `BLOCKED` or `UNVERIFIED`.

## Governance Profiles

### Advisory

- Read-only analysis.
- No implementation write.
- Same-context critique is acceptable when labeled.

### Controlled

- One bounded executor.
- Explicit scope and write set.
- Basic review and verification may run sequentially.

### Managed

- Approved specification and plan.
- Critic before execution.
- Reviewer and Verifier contracts after execution.
- Evidence-based closeout.

### Assured

- Independent review and verification.
- Drift audit.
- Threat model or domain-specific assurance when relevant.
- Runtime evidence and stronger isolation.

### Distributed

- Multiple runtimes, sessions, worktrees, or external teams.
- Formal handoff, consolidation, conflict handling, recovery, and audit trail.

Governance profile and runtime profile are independent selections.

## Quick-Fix Path

A quick-fix path may be used only when all of the following are true:

- the objective is unambiguous;
- implementation scope is small and bounded;
- there is no material logic, API, schema, auth, security, database, runtime,
  deployment, provider, or governance impact;
- verification is cheap and deterministic;
- no hard stop is in scope.

The quick-fix contract still requires scope, an explicit result, checks, and a
truthful closeout. It does not exempt side-effect or secret rules.

## Failure Rules

When a lifecycle function fails:

- downstream state-changing functions remain blocked;
- diagnostics and corrective planning may continue;
- reporting-only closeout may continue;
- a failed or unavailable review/verification step must not be represented as a
  pass;
- implementation may resume only after the controlling gate is reopened through
  the documented corrective loop.
