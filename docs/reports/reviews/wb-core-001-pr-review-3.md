---
schema_version: 1
artifact_type: pr_review
artifact_id: wb-core-001-pr-review-3
work_block_id: WB-CORE-001
status: corrections_requested
verdict: CHANGES_REQUIRED
reviewed_pr: 12
reviewed_normative_subject: 6e4b63a8d53ac7bbaf8d2910730a6601f2a16605
inspected_evidence_only_head: 7ccec4d24982d0f9f28ac4ac8af4c1206031504b
author_resolution_subject: 88d60b142f12e96f1c8fe09839fcc43f6ba95c3d
created_at: 2026-07-30
---

# PR Review 3 — WB-CORE-001 Mutable Assurance Navigation

## Subject

Third independent review of PR #12. The review assessed normative subject
`6e4b63a8d53ac7bbaf8d2910730a6601f2a16605` and inspected evidence-only head
`7ccec4d24982d0f9f28ac4ac8af4c1206031504b`.

The review focused on whether mutable assurance state was incorrectly mirrored
into normative navigation and whether that mirror invalidated the assurance
subject it attempted to register.

## Scope Reviewed

The review inspected:

- `docs/specs/portable-agentic-sdlc-project-kit.md`;
- both portable-kit ADRs;
- `docs/plans/wb-core-001-normative-architecture.md`;
- `PROJECT_MAP.md`;
- `FILE_REGISTRY.yml`;
- the first two persisted PR review reports;
- the commit relationship between normative subject `6e4b63a...` and
  evidence-only head `7ccec4d...`.

Candidate, installer, role, skill, template, test, migration, runtime/provider,
deployment, and Verifier implementation remained outside the reviewed scope.

## Evidence

- reviewed PR: #12;
- reviewed normative subject:
  `6e4b63a8d53ac7bbaf8d2910730a6601f2a16605`;
- inspected evidence-only head:
  `7ccec4d24982d0f9f28ac4ac8af4c1206031504b`;
- Framework Contracts run 732: `success` on the normative subject;
- Framework Contracts run 734: `success` on the evidence-only head;
- Release State Contract run 311: `success` on the normative subject;
- Release State Contract run 312: `success` on the evidence-only head;
- persisted first and second PR review artifacts.

These runs support structural and release-state consistency. They do not replace
semantic review of authority and assurance lifecycle contracts.

## Accepted Prior Resolutions

The third review accepts and does not reopen REV-006 or REV-007:

- **REV-006:** Critic, Reviewer, and Verifier use distinct role-specific verdict
  vocabularies with explicit operational definitions.
- **REV-007:** Reviewer and Verifier reports bind to an exact normative subject;
  applicable subject changes invalidate readiness; evidence-only report commits
  may follow the subject; the report need not be contained in the commit it
  evaluates; CI runs on the resulting PR head; accepted-status finalization
  remains Owner-controlled and non-self-referential.

REV-001 through REV-005 also remain accepted prior corrections and are not
reopened.

## Finding

### REV-008 — Normative navigation mirrors mutable assurance state

- **Severity:** High
- **Finding:** `PROJECT_MAP.md` and `FILE_REGISTRY.yml` are normative-subject
  surfaces, but they mirrored a current review path, verdict, reviewed head,
  accepted/open findings, and another-pass requirement. Every later assurance
  report would therefore require another normative navigation change, producing
  a new subject and invalidating the verdict being registered.
- **Required correction:** Remove mutable assurance mirrors and per-report verdict
  or subject registration from normative navigation. Retain only static evidence
  directory classes and normative authority, architecture, canonical-path,
  active-lifecycle, and accepted/proposed state. Define report discovery through
  canonical directories and structured frontmatter. Adding a report-only commit
  must not require a map or registry update.

## Verdict

**CHANGES_REQUIRED**

This verdict applies to reviewed normative subject `6e4b63a...` and inspected
head `7ccec4d...`. The Author Resolution below does not change this historical
verdict. Another independent Reviewer pass must assess the corrected normative
subject.

## Required Corrections

1. Remove `current_review_evidence` or equivalent mutable assurance mirrors from
   `FILE_REGISTRY.yml`.
2. Remove per-report `verdict`, reviewed/verified SHA, findings, coverage,
   limitations, and another-pass fields from normative navigation.
3. Remove current/latest assurance report enumeration and mutable progress from
   `PROJECT_MAP.md`.
4. Keep static evidence classes for reviews, verification, evaluations, and
   closeout.
5. Clarify in the specification, both ADRs, and Work Block that reports are
   discovered by canonical directories and structured frontmatter and require no
   per-report navigation registration.
6. Commit normative corrections separately before this report.

## Residual Risks

- The corrected normative subject still requires another independent Reviewer
  pass.
- Verifier assurance remains pending.
- The specification and both ADRs remain `proposed`.
- Accepted-status finalization is not authorized or performed.
- CI validates structure but does not itself establish Reviewer or Verifier
  readiness.
- Candidate and implementation work remain future Work Blocks.

## Author Resolution

The Documentation Coder resolved REV-008 in normative subject
`88d60b142f12e96f1c8fe09839fcc43f6ba95c3d` before committing this report.

The correction:

- removed the top-level `current_review_evidence` registry object;
- removed per-report mutable verdict, reviewed-head, findings, and another-pass
  mirrors from the registry;
- removed current/historical review report enumeration, verdicts, SHAs, findings,
  and assurance-progress mirrors from the project map;
- retained static canonical evidence classes:
  `docs/reports/reviews/**`, `docs/reports/verification/**`,
  `docs/reports/evaluations/**`, and `docs/reports/closeout/**`;
- defined normative navigation as authority, architecture, canonical path
  ownership, active lifecycle state, and accepted/proposed status only;
- defined report discovery through canonical directories and structured
  frontmatter;
- stated that adding an evidence-only report requires no normative navigation
  update and that indexing grants no authority;
- preserved REV-001 through REV-007, `status: in_progress`,
  `architecture: runtime_neutral_control_plane`, proposed target status,
  role-specific verdict vocabularies, exact-subject semantics, and the
  proposed-to-accepted sequence.

This report commit changes only
`docs/reports/reviews/wb-core-001-pr-review-3.md` and is evidence-only relative to
normative subject `88d60b1...`.

The Author Resolution does not change the original `CHANGES_REQUIRED` verdict,
does not claim Reviewer `READY` or Verifier `READY`, and does not authorize
accepted-status finalization or merge. Another Reviewer pass is explicitly
required.
