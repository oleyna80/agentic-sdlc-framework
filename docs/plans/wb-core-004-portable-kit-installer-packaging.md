---
schema_version: 1
artifact_type: plan
artifact_id: wb-core-004-portable-kit-installer-packaging
work_block_id: WB-CORE-004
status: approved
owner_approval: OWNER_CORE_004_DEFINE_APPROVAL_GATE in Issue #50; implementation remains blocked pending OWNER_CORE_004_EXECUTE_GATE.
---

# WB-CORE-004 — Define and Execute Plan

## Baseline and lifecycle

Define is anchored to `main@be988807c38543eb90a728fcb4349bc97dd5695a` in an
isolated branch/worktree. The candidate is noncanonical, uninstalled, and
unpromoted. This plan records Owner decisions M1–M4 and separates mechanism
enablement from any future publication, promotion, archive, or release action.

## Define sequence

1. Materialize the stable requirements, acceptance criteria, constraints, and
   exact prospective Execute write-set in the specification.
2. Bind each requirement and criterion to a task, then record the requirements
   review, consistency analysis, Critic result, and governance evidence.
3. Run Define traceability and relevant bootstrap, SDD, governance, publication,
   release-state, and diff checks.
4. Commit only the approved Define artifacts and post a `CHECKPOINT` to Issue
   #50 with `AUTHORITY_REQUIRED: OWNER_CORE_004_EXECUTE_GATE`.

## Execute sequencing after a new gate

One Coder may change only the six candidate paths listed in the specification.
Implementation order is manifest/boundary, pure path and plan logic, staged
publication and compensating rollback, then deterministic fixtures and README
evidence. Plan must remain non-mutating. Apply must revalidate before any
publication and must not touch pre-existing target artifacts. Root bootstrap,
registry, map, governance, and workflow remain out of scope.

After implementation, freeze the exact subject, run deterministic validation,
fresh Reviewer, fresh Verifier, and Drift in that order. A failed assurance
step stops the lifecycle and requires a new Owner correction gate. No push, PR,
merge, promotion, release, deployment, cleanup, or successor declaration is
implied by this plan.

## Risks and controls

- Collision or symlink ambiguity: fail closed before mutation.
- Mid-publication I/O failure: reverse-order rollback of only created artifacts;
  report residuals when incomplete.
- Host differences: use pathlib and deterministic cross-platform fixtures.
- Authority drift: keep root bootstrap/registry/map untouched and require a new
  gate for any candidate-internal boundary expansion.
