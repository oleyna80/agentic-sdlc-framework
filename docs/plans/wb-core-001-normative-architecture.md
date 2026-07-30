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
before any candidate, installer, role, skill, template, test, or migration
implementation begins.

The Work Block preserves the practical SDLC and removes framework ownership of
specific runtimes, providers, models, hooks, plugins, MCP integrations,
capability negotiation, and provider-specific agent configuration.

## Evidence Baseline

- Current repository base:
  `agentic-sdlc-framework@0fce7389d27690482e910e942a1f3138c2fef123`
- Practical framework baseline:
  `agentic-sdlc-framework@0c632db0b0444e556251c384f6254141c9df59bc`
- External methodology reference:
  `obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`
- `Agentic SDLC Framework Core Recovery Audit`
- `Critic Review — Portable Agentic SDLC Project Kit`
- independent PR review at
  `c040015d17004fa90d36bfb26cc0600793a27063`
- second PR review at
  `1fd216cfdc54d7868f4cb388506b08a733a5a418`
- current repository contracts and history

The current `main` SHA matched the previously reviewed baseline at Work Block
start. No intervening `main` change required scope adjustment.

## Process and Authority Classification

- **Process level:** Standard. The change is documentation-only but materially
  changes target product boundary, role packaging, memory ownership,
  installation, migration architecture, and assurance semantics.
- **Side effects:** feature-branch documentation commits and pull request only.
- **Write authority:** scoped Documentation Coder for the approved paths below.
- **Merge authority:** none. Merge requires separate explicit Owner approval.
- **Deployment/data/secrets:** none.
- **Current lifecycle state:** Define and documentation Execute are complete for
  the initial architecture. REV-001 through REV-005 are accepted by the second
  review. The REV-006/REV-007 correction loop is active.
- **Assurance state:** historical reviews retain `CHANGES_REQUIRED`. Another
  Reviewer pass and a later Verifier pass remain pending against exact normative
  subjects.
- **Completion:** this Work Block remains `in_progress`; it is not complete until
  required review, verification, accepted-status finalization, closeout, and
  Owner-controlled integration gates are satisfied.

## Approved Write-Set

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
docs/plans/wb-core-001-normative-architecture.md
docs/reports/reviews/wb-core-001-pr-rereview.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

The original Critic report and first PR review report are read-only historical
evidence in this pass. No other path may be changed.

## Commit Structure

This corrective pass uses two commits:

1. a normative correction commit containing the specification, both ADRs, this
   Work Block, and the navigation/registry registration required by REV-006 and
   REV-007;
2. an evidence-only commit creating
   `docs/reports/reviews/wb-core-001-pr-rereview.md` after the normative commit
   SHA exists.

Navigation and registry are part of the normative subject, even when they index
a report. They therefore belong in the first commit. The second commit changes
only an approved assurance-report path and is evidence-only.

## Operational Release-State Registration

WB-CORE-001 is the current active migration Work Block under the existing
runtime-neutral control-plane release-state contract. `PROJECT_MAP.md` and
`FILE_REGISTRY.yml` register
`docs/plans/wb-core-001-normative-architecture.md` as the active Work Block while
continuing to identify the runtime-neutral control plane as the current
operational architecture.

The navigation sources also register the second PR review as current review
evidence with verdict `CHANGES_REQUIRED` and reviewed head
`1fd216cfdc54d7868f4cb388506b08a733a5a418`. This registration does not promote
the target architecture, complete the Work Block, or grant merge authority.

## Out of Scope

- `candidate/portable-agentic-sdlc-kit/` content;
- installer or packaging code;
- role and skill implementation files;
- templates, tests, fixtures, or migration scripts;
- `.codex/`, `.claude/`, `.opencode/`, hooks, MCP, plugins, model routing, or
  runtime profiles;
- repository settings, secrets, credentials, deployment, live state, or data;
- default-branch writes or merge;
- modifying the original Critic report or first PR review report;
- creating the Verifier report in this Documentation Coder pass.

## Required Decisions

1. Product is a complete project kit, not a skills library or control plane.
2. Runtime neutrality is achieved by non-ownership of runtime/provider concerns.
3. Six roles receive separate portable contracts; shared authority stays in
   `AGENTS.md`.
4. Exactly nine procedural skills form the core.
5. `memory_bank/` remains canonical committed project memory; `.agentic-local/`
   is ignored scratch.
6. Quick, Standard, and High-Risk are risk-based and operationally precise.
7. One active write Work Block is allowed per working tree.
8. Feature-branch commits, push, and PR are allowed within the approved Work
   Block; merge/default-branch push remain Owner-controlled.
9. Candidate and installer contracts are specified without implementation.
10. Optional extensions remain outside the core.
11. Six migration Work Blocks are bounded with no equal unresolved alternatives.
12. Critic, Reviewer, and Verifier use distinct verdict vocabularies.
13. Assurance binds to an exact normative subject.
14. Evidence-only report commits may follow the subject they evaluate and do not
    invalidate the verdict they record.
15. Navigation/registry and accepted-status changes remain normative-subject
    surfaces.

## Execution Plan

1. Resolve the current PR head and stop on unexpected divergence.
2. Preserve the accepted resolution of REV-001 through REV-005.
3. Normalize role verdict vocabularies and report contracts for REV-006.
4. Define normative-subject and evidence-only commit semantics for REV-007.
5. Correct acceptance-state lifecycle language in the specification and both
   ADRs.
6. Update this Work Block without claiming completion.
7. Register the second review in `PROJECT_MAP.md` and `FILE_REGISTRY.yml` while
   preserving current operational architecture and active Work Block state.
8. Commit the normative subject.
9. Create the second review report in a separate evidence-only commit with an
   Author Resolution that identifies the normative correction commit.
10. Run release-state and full framework workflows on the resulting PR head.
11. Leave the PR open and unmerged for another Reviewer pass.

## Acceptance Criteria

- [x] Complete project-kit boundary is defined.
- [x] Runtime/provider ownership is excluded.
- [x] Six separate role contracts are specified and common authority remains in
  `AGENTS.md`.
- [x] Nine core skills are fully specified.
- [x] Relevant current and historical mechanisms have a disposition.
- [x] Project memory and local scratch boundaries are explicit.
- [x] Process levels and concurrency rules are precise.
- [x] Git and Owner authority rules are precise.
- [x] Candidate, installer, optional extensions, and six migration Work Blocks are
  bounded without implementation.
- [x] Exact evidence revisions are recorded.
- [x] Active Work Block precedence and non-expansion rules are explicit.
- [x] REV-001 through REV-005 are represented as accepted by the second review.
- [x] Critic verdicts are `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, and
  `BLOCKED`.
- [x] Reviewer verdicts are `READY`, `CHANGES_REQUIRED`, `BLOCKED`, and
  `UNVERIFIED` with explicit definitions.
- [x] Verifier verdicts are `READY`, `NOT_READY`, `BLOCKED`, and `UNVERIFIED` with
  explicit definitions.
- [x] Normative subject and evidence-only commit semantics are explicit.
- [x] The lifecycle contains no self-referential requirement that a report be in
  the commit it evaluates.
- [x] The second review is registered with reviewed head `1fd216c...` and verdict
  `CHANGES_REQUIRED`.
- [x] Changes are limited to the approved seven-path write-set.
- [ ] A later Reviewer returns `READY` for the applicable normative subject.
- [ ] A later Verifier returns `READY` for the applicable normative subject.
- [ ] Owner authorizes accepted-status finalization and later separately approves
  merge.

## Self-Checks

The documentation set must be checked for:

- exact required specification headings `1` through `24`;
- internal Markdown path references and path spelling;
- role-specific verdict vocabulary consistency;
- acceptance criteria and lifecycle consistency;
- exact normative-subject and evidence-only commit semantics;
- absence of self-referential final-head requirements;
- consistent use of `Quick`, `Standard`, and `High-Risk`;
- consistent candidate and promotion paths;
- absence of Codex, Claude Code, OpenCode, MCP, hooks, or plugins as authorities
  or core dependencies;
- absence of candidate implementation files and installer code;
- absence of placeholder markers, equal alternatives, or silent open decisions;
- diff/write-set restricted to the seven approved corrective paths;
- active Work Block registration consistent across frontmatter, map, and registry;
- second review registration consistent across report, map, and registry;
- proposed-to-accepted transition consistent in the specification and both ADRs.

## Current State

- **Define:** complete for the proposed target architecture.
- **Critic:** imported with historical verdict `APPROVE_WITH_CHANGES`; unchanged.
- **Documentation Execute:** complete for the initial document set; second
  corrective edits are active within the approved write-set.
- **First Reviewer:** head `c040015d17004fa90d36bfb26cc0600793a27063`
  returned historical verdict `CHANGES_REQUIRED`.
- **Second Reviewer:** head `1fd216cfdc54d7868f4cb388506b08a733a5a418`
  accepts REV-001 through REV-005 and returns `CHANGES_REQUIRED` for REV-006 and
  REV-007.
- **Release state:** this file remains the active Work Block under the current
  operational runtime-neutral control-plane contract.
- **Next Reviewer:** pending against the corrected normative subject.
- **Verifier:** pending against the applicable later normative subject; no
  Verifier report is created by this pass.
- **Closeout:** pending. The Work Block is not complete.
- **Merge:** remains controlled by a separate explicit Owner approval and is not
  authorized by this Work Block, a review report, or a green workflow.
