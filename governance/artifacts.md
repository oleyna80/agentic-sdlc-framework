# Portable Artifact Contract

## Purpose

Artifacts are the interoperability boundary between humans, agent runtimes,
models, sessions, and machines. A future agent must be able to recover the
approved state without relying on hidden prompt history.

## Normative Chain

```text
Owner objective or approved change request
  → specification and acceptance criteria
  → architecture decisions
  → implementation plan and write set
  → frozen implementation diff
  → review report
  → verification report
  → specification drift report when required
  → closeout report and engineering-memory promotion
```

Operational logs, generated code maps, external reports, and agent memory may
provide evidence. They do not override approved normative artifacts.

## Minimum Artifact Metadata

Normative and assurance artifacts should expose machine-readable metadata, for
example YAML front matter:

```yaml
schema_version: 1
artifact_type: specification
artifact_id: feature-listing-publication
status: approved
owner_role: orchestrator
work_block_id: wb-042
revision: 3
supersedes: null
created_at: 2026-07-25
last_verified: 2026-07-25
```

Required concepts:

- artifact type and stable ID;
- lifecycle status;
- responsible role;
- Work Block association;
- revision or immutable source revision;
- supersession relationship;
- verification date or method where relevant.

## Artifact Status

Use explicit status values appropriate to the artifact:

- `draft` — proposed content, not authoritative;
- `review` — awaiting the required decision;
- `approved` — current authority for its scope;
- `superseded` — replaced by a named artifact/revision;
- `retired` — no longer applicable;
- `blocked` — incomplete because a dependency or gate failed;
- `generated` — derived context, never authority by itself.

## Specification

A feature or system specification defines:

- intended user or technical outcome;
- required behavior and contracts;
- acceptance criteria;
- constraints and non-goals;
- security, data, and operational requirements;
- compatibility and migration expectations;
- open decisions that block implementation.

Plans and tasklists are derived from the approved specification. If a plan or
implementation conflicts with the specification, the workflow must either
correct the derivative artifact or formally revise the specification.

## Implementation Plan

The plan defines:

- implementation sequence;
- approved write set;
- dependencies;
- runtime and topology selection;
- isolation requirement;
- risk and side-effect classification;
- verification plan;
- rollback/recovery strategy.

A plan may not silently change product or architecture requirements.

## Review Report

The Reviewer reports:

- exact diff or revision reviewed;
- inspected files and omitted areas;
- defects and regressions;
- architecture and maintainability findings;
- security and side-effect findings;
- missing tests or evidence;
- verdict: `APPROVE | CHANGES_REQUIRED | BLOCKED`.

## Verification Report

The Verifier reports:

- exact objective, specification revision, and diff verified;
- commands, tests, runtime checks, and artifacts used;
- acceptance-criterion result matrix;
- inspection gaps and blocked checks;
- residual risks;
- isolation level and launch mechanism;
- verdict: `READY | BLOCKED | UNVERIFIED`.

A check that could not run is `blocked` or `not_run`, never `pass`.

## Drift Report

Drift audit compares:

```text
specification ↔ architecture decisions ↔ plan ↔ code ↔ tests ↔ documentation
```

Classifications:

- `aligned` — no material mismatch;
- `documented_change` — the approved requirement changed and all normative
  artifacts were synchronized;
- `implementation_drift` — code or tests diverge from approved requirements;
- `documentation_drift` — documentation no longer matches behavior;
- `unverified` — insufficient evidence to establish alignment.

## Closeout Report

Successful closeout requires:

- verification verdict `READY`;
- resolved blocking review findings;
- required drift status `aligned` or `documented_change`;
- updated task and decision state;
- recorded residual risks;
- promoted durable knowledge when applicable.

Otherwise use reporting-only closeout and keep the Work Block blocked.

## Source-of-Truth Order

Resolve conflicts in this order:

1. Current explicit Owner instruction for the active Work Block.
2. Active project operating contract and approved governance policy.
3. Approved specification and acceptance criteria.
4. Accepted architecture decisions and external/public contracts.
5. Approved implementation plan and write set.
6. Active task decomposition.
7. Review, verification, drift, and closeout evidence.
8. Durable engineering memory.
9. Operational memory, runtime logs, and generated context.

Lower layers must not silently override higher layers.
