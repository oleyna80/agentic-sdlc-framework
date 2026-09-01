---
schema_version: 1
artifact_type: specification
artifact_id: wb-core-004-portable-kit-installer-packaging
work_block_id: WB-CORE-004
status: approved
created_at: 2026-09-01
revision: define-r1-2026-09-01
owner_approval: OWNER_CORE_004_DEFINE_APPROVAL_GATE in GitHub Issue #50; Define approval only, with Execute requiring a separate gate.
---

# WB-CORE-004 — Portable Kit Installer and Packaging

## Purpose and authority

This Managed Work Block defines a host-neutral, standard-library-only installer
and package boundary for the noncanonical Portable Kit candidate. It is based on
the exact Owner-approved baseline `main@be988807c38543eb90a728fcb4349bc97dd5695a`.
This specification is authoritative for Define and for the prospective Execute
write-set below; it does not authorize implementation, publication, promotion,
merge, release, or deployment.

## Owner constraints

- M1: the installer is owned by `candidate/portable-agentic-sdlc-kit/tools/install.py`.
  Root `bootstrap/**` remains compatibility/regression input and is not repurposed.
- M2: the package boundary is `candidate/portable-agentic-sdlc-kit/template/`,
  `tools/`, `tests/`, `CANDIDATE.md`, and the machine-readable
  `package-manifest.json`. It is identified by repository revision, package
  identity, and manifest schema; no public archive or SemVer release is created.
- M3: plan is non-mutating; apply validates before publication, stages bytes,
  publishes only approved creates, and performs deterministic reverse-order
  best-effort rollback of only artifacts created by the run. Pre-existing target
  artifacts are never overwritten, merged, moved, or deleted. Incomplete
  rollback is a nonzero result with exact residual paths and recovery guidance.
  Filesystem-wide transactional atomicity is not claimed.
- M4: root `FILE_REGISTRY.yml` and `PROJECT_MAP.md` are not mutated. The
  candidate remains noncanonical, uninstalled, and unpromoted; promotion and
  archival belong to WB-CORE-007. Candidate-internal registry/map changes need
  a new explicit write-set gate.

## Requirements

- REQ-001: The package manifest identifies the candidate package identity, schema, repository revision, payload root, and approved create paths deterministically.
- REQ-002: `plan --target <repository>` resolves a host-neutral target and performs no target-file mutation or deletion.
- REQ-003: Installer path resolution rejects traversal, absolute escapes, symlink escapes, and destinations outside the managed target payload.
- REQ-004: Existing target artifacts and unsupported target states are classified as collisions and never overwritten, merged, moved, or deleted.
- REQ-005: `apply --target <repository>` revalidates the plan and approved create set immediately before publication, failing closed on drift or ambiguity.
- REQ-006: Apply stages bytes before publication and publishes only approved creates; an unexpected I/O failure rolls back only this run's created artifacts in reverse order and reports residual paths on incomplete rollback.
- REQ-007: The package is portable and host-neutral, uses Python 3.12 standard library only, and stops with a clear dependency blocker if that constraint cannot be met.
- REQ-008: The candidate boundary and generated local state do not claim canonical authority; root bootstrap compatibility is preserved without changing root registry or map.
- REQ-009: Deterministic fixtures exercise plan/apply success and adversarial collision, path, rollback, and cross-platform path cases against production behavior.
- REQ-010: The Execute write-set and assurance evidence are explicit, traceable, and bounded to the Owner-approved candidate paths.

## Acceptance criteria

- AC-001 [req=REQ-001]: A manifest fixture contains stable package identity/schema/revision fields and an explicit deterministic approved-create list rooted at the candidate payload.
- AC-002 [req=REQ-002]: Plan on an empty disposable target returns a deterministic plan and leaves every pre-existing target byte and directory unchanged.
- AC-003 [req=REQ-003]: Traversal, absolute, symlink-escape, and outside-payload destinations fail closed with deterministic diagnostics.
- AC-004 [req=REQ-004]: Existing files, directories, links, and ambiguous target states produce a nonzero collision result and retain their original bytes and metadata.
- AC-005 [req=REQ-005]: Apply rejects a changed target or changed approved set between plan and publication and performs no partial publication.
- AC-006 [req=REQ-006]: Publication is staged; injected failure removes only artifacts created by the run in reverse order, and incomplete rollback reports exact residual paths and recovery instructions without success.
- AC-007 [req=REQ-007]: Tests run on Python 3.12 with stdlib imports only and use host-neutral path fixtures, including Windows-style path inputs without requiring a live second OS.
- AC-008 [req=REQ-008]: Execute tests prove no root `FILE_REGISTRY.yml`, root `PROJECT_MAP.md`, bootstrap path, or canonical promotion state is changed.
- AC-009 [req=REQ-009]: The deterministic fixture suite invokes production installer behavior for empty target, first apply, repeat/collision, invalid path, staged-failure rollback, and cross-platform cases.
- AC-010 [req=REQ-010]: The committed Define artifacts trace every requirement and criterion to a bounded task and record evidence for requirements review, consistency, Critic, governance, SDD, publication, and release-state checks.

## Prospective Execute write-set

The sole proposed implementation write-set is:

- `candidate/portable-agentic-sdlc-kit/tools/install.py`
- `candidate/portable-agentic-sdlc-kit/tools/README.md`
- `candidate/portable-agentic-sdlc-kit/tests/test_install.py`
- `candidate/portable-agentic-sdlc-kit/tests/README.md`
- `candidate/portable-agentic-sdlc-kit/CANDIDATE.md`
- `candidate/portable-agentic-sdlc-kit/package-manifest.json`

No root bootstrap, root registry/map, governance, workflow, or other source path
may be added without a new Owner gate. Define completion stops at
`OWNER_CORE_004_EXECUTE_GATE`.

## Verification and evaluation plan

Execute verification will run the deterministic installer fixture suite,
`py_compile`, `git diff --check`, and the relevant bootstrap, SDD, governance,
publication, release-state, and Define traceability validators. The fixture
suite is the primary behavior evidence; no model-judged evaluation is needed
unless implementation introduces observable behavior not covered by tests.
