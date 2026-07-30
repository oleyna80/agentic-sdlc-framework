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
- first PR review at `c040015d17004fa90d36bfb26cc0600793a27063`;
- second PR review at `1fd216cfdc54d7868f4cb388506b08a733a5a418`;
- third review of normative subject
  `6e4b63a8d53ac7bbaf8d2910730a6601f2a16605` and evidence-only head
  `7ccec4d24982d0f9f28ac4ac8af4c1206031504b`;
- current repository contracts and history.

## Process and Authority Classification

- **Process level:** Standard.
- **Side effects:** feature-branch documentation commits and pull request only.
- **Write authority:** scoped Documentation Coder for the approved paths.
- **Merge authority:** none; merge requires separate explicit Owner approval.
- **Deployment/data/secrets:** none.
- **Lifecycle:** Define and initial documentation Execute are complete.
  REV-001 through REV-007 are accepted prior corrections. REV-008 correction is
  active.
- **Completion:** `in_progress`; Reviewer, Verifier, accepted-status
  finalization, closeout, and Owner-controlled integration gates remain open.

## Approved Write-Set

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
docs/plans/wb-core-001-normative-architecture.md
docs/reports/reviews/wb-core-001-pr-review-3.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

The Critic report and first two PR review reports are read-only historical
evidence in this pass. No other path may change.

## Commit Structure

This corrective pass uses two commits:

1. a normative correction commit containing the specification, both ADRs, this
   Work Block, `PROJECT_MAP.md`, and `FILE_REGISTRY.yml`;
2. an evidence-only commit creating
   `docs/reports/reviews/wb-core-001-pr-review-3.md`.

The second commit changes only that report path.

## Operational Release-State Registration

WB-CORE-001 remains the active migration Work Block under the existing
runtime-neutral control-plane release-state contract. `PROJECT_MAP.md` and
`FILE_REGISTRY.yml` continue to identify:

- `runtime_neutral_control_plane` as current operational architecture;
- this Work Block as active and `in_progress`;
- the portable kit as `proposed` target architecture;
- canonical evidence directory classes.

Normative navigation does not register individual review, verification,
evaluation, or closeout reports and does not mirror mutable verdicts, subjects,
findings, limitations, coverage, or another-pass state. Evidence is discovered
from canonical directories and report frontmatter.

## Out of Scope

- candidate content;
- installer or packaging code;
- role and skill implementation files;
- templates, tests, fixtures, or migration scripts;
- runtime/provider configuration;
- repository settings, secrets, deployment, live state, or data;
- default-branch writes or merge;
- modification of the Critic report or first two PR review reports;
- creation of a Verifier report.

## Required Decisions

1. Product is a complete project kit, not a skills library or control plane.
2. Runtime neutrality is non-ownership of runtime/provider concerns.
3. Six roles receive separate contracts; shared authority stays in `AGENTS.md`.
4. Exactly nine procedural skills form the core.
5. `memory_bank/` is canonical; `.agentic-local/` is ignored scratch.
6. Quick, Standard, and High-Risk are risk-based and precise.
7. One active write Work Block is allowed per working tree.
8. Feature-branch commits, push, and PR are allowed; merge remains
   Owner-controlled.
9. Candidate and installer contracts are specified without implementation.
10. Optional extensions remain outside the core.
11. Six migration Work Blocks are bounded.
12. Critic, Reviewer, and Verifier use distinct verdict vocabularies.
13. Assurance binds to an exact normative subject.
14. Evidence-only reports may follow their subject without invalidating verdict.
15. Navigation/registry are normative only for authority, architecture,
    canonical paths, active lifecycle state, and accepted/proposed status.
16. Mutable assurance state is prohibited from normative navigation.
17. Per-report registration is unnecessary; canonical directories and
    frontmatter are the evidence discovery mechanism.

## Execution Plan

1. Resolve current PR head and stop on unexpected divergence.
2. Preserve REV-001 through REV-007.
3. Remove mutable assurance mirrors from `PROJECT_MAP.md`.
4. Remove `current_review_evidence` and mutable per-report fields from
   `FILE_REGISTRY.yml`.
5. Retain static evidence directory classifications.
6. Correct specification, ADRs, and this Work Block.
7. Commit the corrected normative subject.
8. Create the third review in a separate evidence-only commit.
9. Run release-state and Framework Contracts workflows.
10. Leave PR open and unmerged for another Reviewer pass.

## Acceptance Criteria

- [x] Product boundary, runtime exclusions, roles, skills, memory, process levels,
  concurrency, Git boundaries, candidate, installer, extensions, and migration
  sequence remain defined.
- [x] Active Work Block precedence and non-expansion rules remain explicit.
- [x] `status: in_progress` is preserved.
- [x] Current operational and proposed target architectures remain distinct.
- [x] Role-specific verdict vocabularies remain unchanged.
- [x] Exact normative-subject and evidence-only semantics remain explicit.
- [x] Proposed-to-accepted finalization sequence remains unchanged.
- [x] Mutable review/verification verdicts and subjects are removed from
  normative navigation.
- [x] `current_review_evidence` is removed from the registry.
- [x] Per-report mutable registry fields are removed.
- [x] Static evidence directory registration remains available.
- [x] Evidence discovery uses canonical directories and structured frontmatter.
- [x] Changes are restricted to the approved seven-path write-set.
- [ ] A later Reviewer returns `READY` for the corrected normative subject.
- [ ] A later Verifier returns `READY`.
- [ ] Owner authorizes accepted-status finalization and separately approves merge.

## Self-Checks

Check:

- specification headings 1 through 24;
- verdict vocabulary consistency;
- normative-subject/evidence-only consistency;
- absence of self-referential final-head requirements;
- no mutable review/verification verdict or subject in `PROJECT_MAP.md`;
- no `current_review_evidence` or mutable per-report assurance fields in
  `FILE_REGISTRY.yml`;
- static review, verification, evaluation, and closeout directory classes;
- active Work Block agreement across frontmatter, map, and registry;
- operational architecture `runtime_neutral_control_plane`;
- target status `proposed`;
- no runtime/provider authority;
- no placeholder markers;
- final evidence-only commit changes only the third-review report.

## Current State

- **Define:** complete for the proposed target architecture.
- **Critic:** historical `APPROVE_WITH_CHANGES`; unchanged.
- **REV-001—REV-007:** preserved as accepted prior corrections.
- **REV-008:** Author Resolution is recorded in the third review after the
  normative correction commit.
- **Release state:** this Work Block remains active under the current
  runtime-neutral control-plane contract.
- **Reviewer:** another pass remains required against the corrected normative
  subject.
- **Verifier:** pending; no Verifier report is created by this pass.
- **Closeout:** pending; Work Block is not complete.
- **Merge:** requires separate explicit Owner approval.
