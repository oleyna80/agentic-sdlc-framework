---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-001-normative-architecture
work_block_id: WB-CORE-001
status: in_progress
owner_role: orchestrator
created_at: 2026-07-29
base_revision: 0fce7389d27690482e910e942a1f3138c2fef123
branch: agent/portable-kit-normative-architecture
process_level: Standard
---

# WB-CORE-001 — Normative Architecture for the Portable Agentic SDLC Project Kit

## Objective

Define the normative architecture for the Portable Agentic SDLC Project Kit
before candidate, installer, role, skill, template, test, or migration
implementation begins.

The Work Block preserves the practical SDLC and removes framework ownership of
specific runtimes, providers, models, hooks, plugins, MCP integrations,
capability negotiation, and provider-specific agent configuration.

## Evidence Baseline

- current repository base:
  `agentic-sdlc-framework@0fce7389d27690482e910e942a1f3138c2fef123`;
- practical framework baseline:
  `agentic-sdlc-framework@0c632db0b0444e556251c384f6254141c9df59bc`;
- external methodology reference:
  `obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`;
- recovery audit and imported Critic review;
- accepted Reviewer correction history REV-001 through REV-009;
- preliminary Verifier normative subject:
  `674e992548c0474b79bbf261ee7fbceae8eaff4a`;
- preliminary verification report:
  `docs/reports/verification/wb-core-001-preliminary-verification.md`;
- historical preliminary Verifier verdict: `NOT_READY`;
- failed criteria: `VER-006`, `VER-007`, `VER-008`, `VER-014`, and derived
  `VER-020`;
- current repository contracts and history.

The historical verification report remains unchanged. It records the failed
subject and verdict; this corrective pass does not revise historical evidence.

## Accepted Prior Decisions

REV-001 through REV-009 are not reopened. Preserve:

- complete project-kit product boundary;
- runtime/provider non-ownership;
- active Work Block precedence;
- separate portable roles;
- exactly nine core skills;
- canonical committed `memory_bank/`;
- Quick / Standard / High-Risk model;
- one write Work Block per working tree;
- exact normative-subject semantics;
- evidence-only report commits;
- prohibition of mutable assurance mirrors;
- current operational architecture `runtime_neutral_control_plane`;
- portable target status `proposed`;
- WB-CORE-001 status `in_progress`;
- Owner-controlled status finalization and merge.

## Process and Authority Classification

- **Process level:** Standard.
- **Side effects:** one feature-branch normative documentation commit and pull
  request update only.
- **Write authority:** scoped Architect / Documentation Coder for the exact
  three-file corrective write-set.
- **Merge authority:** none; PR #12 merge requires separate explicit Owner
  approval.
- **Deployment/data/secrets:** none.
- **Correction purpose:** resolve only the four normative gaps established by
  the preliminary Verifier.
- **Completion:** `in_progress`; new Reviewer, new preliminary Verifier,
  accepted-status finalization, closeout, and Owner-controlled integration gates
  remain open.

## Approved Write-Set

Modify exactly:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
docs/plans/wb-core-001-normative-architecture.md
```

No change is authorized to:

```text
FILE_REGISTRY.yml
PROJECT_MAP.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/reports/verification/wb-core-001-preliminary-verification.md
```

No Reviewer, Verifier, evaluation, or closeout report is created or modified by
this pass. No other path may change.

## Commit Structure

Create one normative commit:

```text
docs(core): resolve preliminary verification gaps
```

The commit changes exactly the three approved normative paths. It is the new
normative subject for subsequent independent assurance.

## Operational Architecture and Navigation Boundary

The current repository remains the operational
`runtime_neutral_control_plane`. The portable
`portable_agentic_sdlc_project_kit` remains `proposed`, and this Work Block
remains active and `in_progress`.

This correction does not update `FILE_REGISTRY.yml` or `PROJECT_MAP.md` because
it changes no current operational path ownership, architecture identity,
canonical evidence directory, active Work Block identity, or accepted/proposed
status.

Normative navigation does not register individual review, verification,
evaluation, or closeout reports and does not mirror mutable verdicts, subjects,
findings, limitations, coverage, or another-pass state. Evidence is discovered
from canonical directories and structured report frontmatter.

## Correction Scope

### VER-006 — explicit mechanism disposition

Specification section 12 must:

- retain exactly the nine accepted core procedural skills;
- explicitly classify every listed current or historical mechanism as core
  skill, role contract, template/lifecycle mechanism, optional extension, or
  outside portable core;
- remove provider names from portable authority;
- state that current operational implementations may remain during migration but
  are not copied into or owned by the portable target.

### VER-007 — memory ownership and update triggers

Specification section 14 must define for every canonical memory path:

- owner;
- update trigger;
- required content;
- prohibited content;
- retention.

It must state that committed `memory_bank/` reconstructs accepted project state,
`.agentic-local/` is ignored/disposable/noncanonical, reports remain detailed
assurance sources, memory links rather than duplicates, and proposed/unverified
content is labelled.

The roles/memory/installation ADR must agree with this contract without
duplicating the complete specification table.

### VER-008 — operational process-level selection

Specification section 6 must:

- classify on ambiguity, impacts, boundaries, authority, side effects,
  reversibility, risk, consequence, verification cost, nondeterminism, writers,
  and handoffs;
- state that file count is not a primary classifier;
- require every Quick eligibility condition;
- make Standard the explicit default when neither Quick nor High-Risk applies;
- define escalation and reclassification;
- make High-Risk mandatory whenever a trigger exists;
- fail closed when required assurance, authority, rollback, or evidence is
  unavailable.

### VER-014 — path-traversal protection

Specification section 19 and the roles/memory/installation ADR must require:

- canonical target-root identity;
- normalized non-empty relative candidate paths;
- rejection of absolute, drive-prefixed, UNC/network-root, `..`, NUL/invalid, and
  root-escaping paths;
- parent symlink/junction containment;
- apply-time revalidation before mutation;
- whole-apply abort on traversal, root escape, unsafe link, or unresolved
  collision.

## Out of Scope

- candidate, installer, role, skill, or template implementation;
- status finalization or acceptance;
- modification of product-boundary ADR;
- navigation or registry changes;
- runtime/provider configuration;
- broad architecture redesign;
- repair of unrelated findings;
- repository settings, secrets, deployment, live state, or data;
- default-branch writes or merge;
- modification of historical assurance reports;
- creation of a new assurance report.

## Execution Plan

1. Resolve current PR #12 head and stop on unexpected divergence.
2. Confirm no applicable normative file changed after `674e992...`.
3. Preserve REV-001 through REV-009 and all accepted product boundaries.
4. Modify only the specification, roles/memory/installation ADR, and this Work
   Block.
5. Add explicit mechanism disposition.
6. Add per-memory-file ownership and update triggers.
7. Add operational risk-based process-level selection.
8. Add fail-closed traversal and destination-containment rules.
9. Run exact write-set and normative-content checks.
10. Create one normative commit and advance the existing PR branch.
11. Run Framework Contracts and Release State Contract.
12. Leave PR #12 open and unmerged for new independent Reviewer and Verifier
    passes.

## Acceptance Criteria

- [x] REV-001 through REV-009 remain accepted and are not reopened.
- [x] `status: in_progress` is preserved.
- [x] Current operational and proposed target architectures remain distinct.
- [x] Exactly nine core procedural skills remain.
- [x] Explicit disposition exists for every listed current/historical mechanism.
- [x] Every canonical memory path has an owner and event-driven update trigger.
- [x] Memory required/prohibited content and retention are explicit.
- [x] Reversibility is a process-classification dimension.
- [x] File count is explicitly non-authoritative.
- [x] Quick eligibility contains all mandatory conditions.
- [x] Standard is the explicit default when neither Quick nor High-Risk applies.
- [x] High-Risk cannot be downgraded when a mandatory trigger exists.
- [x] Reclassification rules are explicit.
- [x] Absolute, drive/UNC-root, `..`, invalid, and root-escaping paths are rejected.
- [x] Parent symlink/junction escape fails closed.
- [x] `apply` revalidates before any mutation.
- [x] Atomicity prevents partial mutation when any planned action is blocked.
- [x] No normative navigation update is required or made.
- [x] Specification and both ADRs remain `proposed`.
- [x] Operational architecture remains unchanged.
- [ ] A new Reviewer assesses the corrected normative subject and returns the
  applicable verdict.
- [ ] A new preliminary Verifier assesses the same corrected normative subject and
  returns `READY`.
- [ ] Owner authorizes accepted-status finalization.
- [ ] Final applicable assurance, closeout, and separate merge approval complete.

The checked correction criteria above mean the required normative text is present
in this same commit. They do not rewrite or resolve the historical Verifier
report. `VER-006`, `VER-007`, `VER-008`, `VER-014`, and derived `VER-020` remain
historical failures until a new Verifier assesses the corrected subject.

## Self-Checks

Check:

- exact three-file commit write-set;
- exactly nine core skills;
- explicit one-disposition-per-mechanism table;
- memory owner and update trigger for every `memory_bank/` path;
- strict Quick eligibility and Standard default/escalation;
- reversibility and non-authoritative file-count language;
- mandatory High-Risk triggers and no downgrade path;
- absolute/drive/UNC/`..` rejection;
- parent symlink/junction containment;
- apply-time revalidation and whole-apply abort;
- no change to map, registry, product-boundary ADR, or any report;
- specification and roles/memory/installation ADR remain `proposed`;
- Work Block remains `in_progress`;
- operational architecture remains `runtime_neutral_control_plane`;
- Framework Contracts and Release State Contract on the resulting head;
- PR #12 remains open and unmerged.

## Current State

- **Define:** proposed target architecture remains defined.
- **Critic:** historical accepted correction history REV-001 through REV-009;
  unchanged.
- **Reviewer:** prior `READY` is historical and stale for the changed normative
  surfaces; a new Reviewer pass is required.
- **Preliminary Verifier:** historical subject
  `674e992548c0474b79bbf261ee7fbceae8eaff4a` returned `NOT_READY` in
  `docs/reports/verification/wb-core-001-preliminary-verification.md`.
- **Correction:** specification/ADR correction is in progress in this normative
  commit.
- **New assurance:** new Reviewer and new preliminary Verifier passes are
  required against the corrected normative subject.
- **Accepted-status finalization:** blocked and Owner-controlled.
- **Closeout:** blocked; Work Block is not complete.
- **Merge:** PR #12 remains subject to separate explicit Owner approval.
