---
schema_version: 1
artifact_type: pr_review
artifact_id: wb-core-001-pr-rereview
work_block_id: WB-CORE-001
status: corrections_requested
verdict: CHANGES_REQUIRED
reviewed_pr: 12
reviewed_head: 1fd216cfdc54d7868f4cb388506b08a733a5a418
normative_resolution_subject: 6e4b63a8d53ac7bbaf8d2910730a6601f2a16605
created_at: 2026-07-30
---

# PR Re-review — WB-CORE-001 Assurance Semantics

## Subject

Second independent review of PR #12 at head
`1fd216cfdc54d7868f4cb388506b08a733a5a418`, focused on assurance verdict
vocabularies, verified-subject identity, evidence-only commits, and the
proposed-to-accepted transition.

## Scope Reviewed

The review inspected:

- `docs/specs/portable-agentic-sdlc-project-kit.md`;
- both portable-kit ADRs;
- `docs/plans/wb-core-001-normative-architecture.md`;
- the first PR review and its Author Resolution;
- `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
- PR #12 state and CI evidence at the reviewed head.

The review did not assess candidate, installer, role, skill, template, test, or
migration implementation because those remain out of scope and do not exist in
this Work Block.

## Evidence

- reviewed PR: #12;
- reviewed head: `1fd216cfdc54d7868f4cb388506b08a733a5a418`;
- Framework Contracts run 730: `success`;
- Release State Contract run 309: `success`;
- first persisted PR review at head
  `c040015d17004fa90d36bfb26cc0600793a27063`;
- current specification, ADRs, Work Block, map, and registry at the reviewed head.

Runs 730 and 309 support structural and release-state consistency. They are not
sufficient final assurance for the semantic findings below.

## Accepted Prior Resolutions

The second review accepts the Author Resolution of REV-001 through REV-005:

- **REV-001:** the active Work Block is above plans, tasklists, and mission briefs,
  and lower artifacts cannot expand it;
- **REV-002:** WB-CORE-001 is truthfully `in_progress` with Reviewer, Verifier,
  closeout, and Owner-controlled integration gates still open;
- **REV-003:** the active Work Block is registered while
  `runtime_neutral_control_plane` remains the current operational architecture;
- **REV-004:** the first independent PR review is persisted without changing its
  `CHANGES_REQUIRED` verdict;
- **REV-005:** proposed artifacts require explicit accepted-status finalization,
  assurance, and separate Owner approval rather than implicit acceptance by PR or
  merge presence.

These findings are not reopened by this review.

## Findings

### REV-006 — Assurance roles use overlapping or incorrect verdict vocabularies

- **Severity:** High
- **Finding:** The specification used Critic-style approval verdicts for Reviewer
  output and did not fully define role-specific failure states. This made design
  criticism, review readiness, and acceptance verification ambiguous.
- **Required correction:** Define and consistently apply:
  - Critic: `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, `BLOCKED`;
  - Reviewer: `READY`, `CHANGES_REQUIRED`, `BLOCKED`, `UNVERIFIED`;
  - Verifier: `READY`, `NOT_READY`, `BLOCKED`, `UNVERIFIED`.
  Define each Reviewer and Verifier verdict operationally and preserve historical
  verdicts already recorded.

### REV-007 — Assurance subject and report commits are self-referential

- **Severity:** High
- **Finding:** The prior transition implied that final verification had to bind to
  a final head that would itself change when the report was committed. It did not
  distinguish normative-subject changes from evidence-only report commits.
- **Required correction:** Define the exact normative subject and evidence-only
  commit semantics. Reports must identify the exact subject SHA; subject changes
  invalidate applicable readiness; report-only evidence commits may follow the
  subject without invalidating their verdict; CI must pass on the resulting PR
  head. Correct the acceptance sequence so that the status-only normative commit
  is assured before a later evidence-only report commit and separate Owner merge
  approval.

## Verdict

**CHANGES_REQUIRED**

This verdict applies to reviewed head
`1fd216cfdc54d7868f4cb388506b08a733a5a418`. It is not changed by the Author
Resolution below. Another independent Reviewer pass must assess the corrected
normative subject.

## Required Corrections

1. **REV-006:** normalize Critic, Reviewer, and Verifier verdict vocabularies and
   all affected lifecycle, report, closeout, migration, and acceptance language.
2. **REV-007:** define exact normative-subject identity, evidence-only commit
   rules, invalidation behavior, and the non-self-referential acceptance sequence.
3. Register this report as current review evidence without changing the current
   operational architecture or active Work Block status.
4. Commit normative corrections separately before committing this report as
   evidence-only.

## Residual Risks

- The corrected normative subject still requires another independent Reviewer
  pass.
- Verifier assurance remains pending.
- The specification and both ADRs remain `proposed`.
- Accepted-status finalization has not been authorized or performed.
- CI can demonstrate structural consistency but cannot replace role-specific
  semantic review or Owner authority.
- Candidate and migration implementation remain future Work Blocks.

## Author Resolution

The Documentation Coder resolved REV-006 and REV-007 in normative subject
`6e4b63a8d53ac7bbaf8d2910730a6601f2a16605` before creating this report.

- **REV-006:** the specification, both ADRs, Work Block, map, and registry now use
  the required role-specific verdict vocabularies. Reviewer and Verifier verdicts
  have explicit operational definitions. Historical Critic and first-review
  verdicts were not modified.
- **REV-007:** those same normative surfaces now define the exact normative
  subject, eight evidence-only rules, readiness invalidation, report-correction
  boundaries, and the required acceptance sequence. They explicitly state that
  an assurance report may be committed after the subject it evaluates and need
  not be contained in that subject commit.
- `PROJECT_MAP.md` and `FILE_REGISTRY.yml` register this review with verdict
  `CHANGES_REQUIRED` and reviewed head
  `1fd216cfdc54d7868f4cb388506b08a733a5a418`, while preserving
  `architecture: runtime_neutral_control_plane`, the active Work Block path, and
  lifecycle status `in_progress`.
- The normative correction commit contains the navigation/registry updates. This
  report commit changes only this approved review-report path and is therefore
  evidence-only relative to normative subject `6e4b63a...`.

This Author Resolution does not change the original `CHANGES_REQUIRED` verdict,
does not claim Reviewer `READY` or Verifier `READY`, and does not authorize
accepted-status finalization or merge. Another Reviewer pass is explicitly
required.
