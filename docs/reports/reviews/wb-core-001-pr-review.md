---
schema_version: 1
artifact_type: pr_review
artifact_id: wb-core-001-pr-review
work_block_id: WB-CORE-001
status: corrections_requested
verdict: CHANGES_REQUIRED
reviewed_pr: 12
reviewed_head: c040015d17004fa90d36bfb26cc0600793a27063
created_at: 2026-07-29
---

# PR Review — WB-CORE-001 Normative Architecture

## Subject

Independent review of PR #12, `docs(core): define portable Agentic SDLC project
kit`, at head `c040015d17004fa90d36bfb26cc0600793a27063`.

## Scope Reviewed

The review covered the five documentation artifacts then present in PR #12:

- `docs/specs/portable-agentic-sdlc-project-kit.md`;
- `docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`;
- `docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`;
- `docs/plans/wb-core-001-normative-architecture.md`;
- `docs/reports/reviews/wb-core-001-critic-review.md`.

It also inspected the operational release-state projections in `PROJECT_MAP.md`
and `FILE_REGISTRY.yml` because their state determines whether WB-CORE-001 is
truthfully registered.

## Evidence

- PR #12 at reviewed head `c040015d17004fa90d36bfb26cc0600793a27063`;
- the five proposed WB-CORE-001 documents;
- `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, `governance/release-state.md`, and
  `scripts/validate-release-state.py`;
- Framework Contracts run 716: `success`;
- Release State Contract run 295: `success`.

Runs 716 and 295 support repository consistency at the reviewed head. They are
not sufficient final assurance because they did not detect the unregistered
active Work Block or decide the normative source-of-truth precedence.

## Findings

### REV-001 — Source-of-truth precedence is incorrect

The specification placed plans and tasklists above the active Work Block and
combined the Work Block with mission briefs. The active Work Block must instead
bind scope, write-set, process level, role authority, Hard Stops, and acceptance;
plans and mission briefs may narrow or sequence but cannot expand it.

### REV-002 — WB-CORE-001 is represented as a proposal rather than executed work

The Work Block was documentation already executed on a feature branch, with
review and verification still pending. It therefore requires active status
`in_progress` and a truthful lifecycle statement.

### REV-003 — Active Work Block is absent from release-state navigation

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` declared no active Work Block, allowing
the release-state validator to ignore WB-CORE-001. Both projections must register
its path while retaining `runtime_neutral_control_plane` as the current
operational architecture and identifying the portable kit only as the proposed
target.

### REV-004 — Independent PR review is not persisted

The `CHANGES_REQUIRED` review must be stored as repository evidence so the
correction and later re-review are reconstructable without mutable hosting state.

## Accepted Decisions

The review accepted the following architectural decisions and did not request
that they be reopened:

- the product boundary is a complete portable Agentic SDLC Project Kit rather
  than a skills library or runtime control plane;
- runtime/provider ownership is excluded from the portable core;
- six separate role contracts retain shared authority in root `AGENTS.md`;
- nine core procedural skills and their historical dispositions are defined;
- committed `memory_bank/` is canonical and `.agentic-local/` is disposable local
  state;
- Quick, Standard, and High-Risk are risk-based;
- one active write Work Block per working tree and one Coder per write-set are
  retained;
- the candidate remains noncanonical and installation is collision-safe,
  runtime-neutral, and specified without implementation;
- the six-Work-Block migration sequence and Owner-controlled merge boundary are
  retained;
- the runtime-neutral control plane remains the current operational architecture
  until later promotion.

## Verdict

**CHANGES_REQUIRED**

This verdict applies to reviewed head
`c040015d17004fa90d36bfb26cc0600793a27063`. It is not changed by the Author
Resolution below. A later Reviewer pass must assess the corrected head.

## Required Corrections

1. **REV-001:** correct the normative precedence and expansion rules.
2. **REV-002:** set the executed Work Block to `in_progress` and state the actual
   lifecycle gates.
3. **REV-003:** synchronize the active Work Block in both release-state
   projections without changing the operational architecture identifier.
4. **REV-004:** persist this review and its evidence.
5. **REV-005:** define the `proposed` to accepted status transition in the
   specification and both ADRs, without accepting them in the corrective pass.

## Residual Risks

- The corrected head still requires a later independent Reviewer pass.
- A separate Verifier report against the final status-finalization subject remains
  pending.
- The specification and both ADRs remain `proposed` and are not accepted.
- Candidate, installer, role, skill, template, test, and migration implementation
  do not yet exist.
- Owner approval remains required for merge and later promotion.

## Author Resolution

- **REV-001:** section 4 of the specification now places the active Work Block
  above plans, tasklists, and mission briefs and defines non-expansion and
  revision rules.
- **REV-002:** the Work Block status is `in_progress`; Define and documentation
  Execute are complete, the Reviewer correction loop is active, and Verifier,
  closeout, and Owner-controlled merge remain pending.
- **REV-003:** `PROJECT_MAP.md` and `FILE_REGISTRY.yml` register the active Work
  Block while preserving `runtime_neutral_control_plane` as the operational
  architecture and exposing the portable kit as a proposed target.
- **REV-004:** this report persists the original review, evidence, verdict, and
  required corrections.
- **REV-005:** the specification and both ADRs define an explicit status
  finalization rule; all three remain `proposed` in this corrective pass.

The Author Resolution records the changes made. It does not revise the original
`CHANGES_REQUIRED` verdict or claim that re-review or verification is complete.
