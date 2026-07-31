---
schema_version: 1
artifact_type: pr_review
artifact_id: wb-core-001-pr-review-4
work_block_id: WB-CORE-001
status: corrections_requested
verdict: CHANGES_REQUIRED
reviewed_pr: 12
reviewed_normative_subject: 88d60b142f12e96f1c8fe09839fcc43f6ba95c3d
inspected_evidence_only_head: 2b9171e20fc681ebdd3a5619a307438dfeac6e3c
author_resolution_subject: 674e992548c0474b79bbf261ee7fbceae8eaff4a
created_at: 2026-07-30
---

# PR Review 4 — WB-CORE-001 Operational Registry Restoration

## Subject

Fourth independent review of PR #12. The review assessed normative subject
`88d60b142f12e96f1c8fe09839fcc43f6ba95c3d` and inspected evidence-only head
`2b9171e20fc681ebdd3a5619a307438dfeac6e3c`.

The review focused on whether REV-008 correctly removed mutable assurance mirrors
without silently deleting unrelated static contracts that remain part of the
current runtime-neutral control-plane inventory.

## Scope Reviewed

The review inspected:

- `FILE_REGISTRY.yml` at pre-REV-008 baseline `7ccec4d...`;
- `FILE_REGISTRY.yml` at normative subject `88d60b1...`;
- `PROJECT_MAP.md` at the same baseline and subject;
- `docs/plans/wb-core-001-normative-architecture.md`;
- the third persisted PR review;
- the evidence-only relationship between `88d60b1...` and `2b9171e...`.

The specification and both portable-kit ADRs were checked for contradiction but
required no modification. Candidate, installer, role, skill, template, test,
migration implementation, runtime/provider mutation, deployment, and Verifier
implementation remained outside scope.

## Evidence

- reviewed PR: #12;
- reviewed normative subject:
  `88d60b142f12e96f1c8fe09839fcc43f6ba95c3d`;
- inspected evidence-only head:
  `2b9171e20fc681ebdd3a5619a307438dfeac6e3c`;
- pre-REV-008 navigation baseline:
  `7ccec4d24982d0f9f28ac4ac8af4c1206031504b`;
- Framework Contracts run 738: `success`;
- Release State Contract run 317: `success`;
- third persisted PR review and its Author Resolution.

The green workflows support structural and release-state consistency. They do
not establish that unrelated current-operational registry contracts were
semantically preserved.

## Accepted Prior Resolution

The fourth review accepts REV-008 and does not reopen REV-001 through REV-008.
In particular, it accepts:

- prohibition of mutable assurance mirrors in normative navigation;
- removal of current/latest report pointers, verdicts, reviewed or verified SHAs,
  findings, coverage, limitations, and another-pass state;
- static evidence classes for review, verification, evaluation, and closeout;
- canonical-directory and structured-frontmatter evidence discovery;
- exact normative-subject and evidence-only commit semantics;
- role-specific verdict vocabularies;
- active Work Block precedence and `status: in_progress`;
- separation of the current runtime-neutral control plane from the proposed
  portable-kit target;
- the Owner-controlled proposed-to-accepted finalization sequence.

## Finding

### REV-009 — Unrelated static operational registry contracts were removed

- **Severity:** High
- **Finding:** Commit `88d60b1...` correctly removed mutable assurance state but
  also removed static registry rules, path classifications, relationship metadata,
  and detailed operational map descriptions unrelated to REV-008. WB-CORE-001 has
  not promoted the portable target or archived the current runtime-neutral control
  plane, so those existing operational contracts remain applicable.
- **Required correction:** Restore unrelated static content from baseline
  `7ccec4d...` while preserving every intentional REV-008 change. Do not perform a
  mechanical revert, restore mutable assurance mirrors, or redesign the registry.

## Verdict

**CHANGES_REQUIRED**

This verdict applies to reviewed normative subject `88d60b1...` and inspected
head `2b9171e...`. The Author Resolution below does not change the historical
verdict. Another independent Reviewer pass must assess the corrected normative
subject.

## Required Corrections

1. Restore `installation_profiles.rules`.
2. Restore the static `scripts/ci-contract-router.py` entry.
3. Restore static template path entries for shared hooks, bootstrap health check,
   installation-profile validation, and evaluation plan/report/event templates.
4. Restore unrelated static `related:` metadata removed from existing entries.
5. Restore detailed current-operational descriptions in `PROJECT_MAP.md` where
   their removal was unnecessary for REV-008.
6. Retain the REV-008 prohibition on mutable assurance mirrors and per-report
   registration.
7. Document every intentionally non-restored deletion and its equivalent wildcard
   or canonical-class coverage.
8. Commit normative corrections before this evidence report.

## Residual Risks

- The corrected normative subject requires another independent Reviewer pass.
- Verifier assurance remains pending.
- The specification and both ADRs remain `proposed`.
- Accepted-status finalization is not authorized or performed.
- WB-CORE-001 remains `in_progress`; closeout is pending.
- Static wildcard coverage must remain semantically adequate as operational
  inventory evolves.
- CI validates structure but does not itself establish Reviewer or Verifier
  readiness.

## Author Resolution

The Documentation Coder resolved REV-009 in normative subject
`674e992548c0474b79bbf261ee7fbceae8eaff4a` before committing this report.

### Static content restored

The correction restored:

- `installation_profiles.rules`:
  - `validate_before_target_mutation`;
  - `required_paths_validate_expected_filesystem_kind`;
  - `blocked_default_work_block_validates_before_restore`;
  - `evaluation_contract_available_in_every_profile`;
  - `selected_runtime_surfaces_only`;
  - `no_automatic_integration_activation`;
  - `no_credentials_or_provider_binding`;
  - `work_block_authority_remains_separate`;
  - `external_skill_adaptation_requires_owner_approved_write_set`;
- `scripts/ci-contract-router.py` with its fail-closed routing and snapshot role;
- `template/.agent/hooks/**`;
- `template/scripts/bootstrap.sh`;
- `template/scripts/validate-installation-profile.py`;
- `template/docs/templates/evaluation-plan-template.json`;
- `template/docs/templates/evaluation-report-template.json`;
- `template/docs/templates/trajectory-event-template.json`;
- the `related:` links on `skills/skill-library-maintenance/**` to the external
  skill discovery workflow, skill-routing gate, and installation profiles;
- detailed current-operational map descriptions for evaluation, release state,
  deterministic repair, skill-library maintenance, installation profiles,
  runtime/integration adapters, and key operational paths.

`template/scripts/repair-lifecycle.py` was reviewed and required no restoration
because it remained registered after REV-008.

### Intentionally non-restored baseline entries

The following individual entries remain omitted with explicit equivalent
coverage:

- completed Work Block entries under `docs/plans/` are covered by the static
  `docs/plans/**` class, while `migration_state.completed_work_blocks` retains the
  authoritative completed list;
- individual Critic and Reviewer report entries are covered by
  `docs/reports/reviews/**`, while structured report frontmatter carries exact
  subject, verdict, findings, coverage, limitations, and history.

No other unrelated static baseline deletion remains. No per-report current/latest
pointer or mutable assurance field was restored.

### Preserved invariants

The correction preserves:

- `architecture: runtime_neutral_control_plane`;
- active Work Block
  `docs/plans/wb-core-001-normative-architecture.md`;
- Work Block `status: in_progress`;
- target `portable_agentic_sdlc_project_kit` with `status: proposed`;
- all REV-001 through REV-008 decisions;
- static evidence classes and frontmatter-based discovery;
- the absence of `current_review_evidence`, mutable verdicts, reviewed or verified
  SHAs, findings, coverage, limitations, and another-pass state in normative
  navigation;
- pending Reviewer, Verifier, accepted-status finalization, closeout, and separate
  Owner merge gates.

This report is not individually registered in `PROJECT_MAP.md` or
`FILE_REGISTRY.yml`. Its canonical directory and structured frontmatter provide
discovery. This commit changes only
`docs/reports/reviews/wb-core-001-pr-review-4.md` and is evidence-only relative to
normative subject `674e992...`.

The Author Resolution does not change the original `CHANGES_REQUIRED` verdict,
does not claim Reviewer `READY` or Verifier `READY`, and does not authorize
accepted-status finalization or merge. Another Reviewer pass is explicitly
required.
