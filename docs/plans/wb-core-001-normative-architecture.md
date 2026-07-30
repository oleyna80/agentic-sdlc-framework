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
- fourth review of normative subject
  `88d60b142f12e96f1c8fe09839fcc43f6ba95c3d` and evidence-only head
  `2b9171e20fc681ebdd3a5619a307438dfeac6e3c`;
- pre-REV-008 operational navigation baseline
  `7ccec4d24982d0f9f28ac4ac8af4c1206031504b`;
- current repository contracts and history.

## Process and Authority Classification

- **Process level:** Standard.
- **Side effects:** feature-branch documentation commits and pull request only.
- **Write authority:** scoped Documentation Coder for the approved paths.
- **Merge authority:** none; merge requires separate explicit Owner approval.
- **Deployment/data/secrets:** none.
- **Lifecycle:** Define and initial documentation Execute are complete.
  REV-001 through REV-008 are accepted prior corrections. REV-009 correction is
  active.
- **Correction purpose:** restore unrelated static current-operational inventory
  removed during REV-008 without reintroducing mutable assurance mirrors or
  changing the portable target architecture.
- **Completion:** `in_progress`; Reviewer, Verifier, accepted-status
  finalization, closeout, and Owner-controlled integration gates remain open.

## Approved Write-Set

```text
FILE_REGISTRY.yml
PROJECT_MAP.md
docs/plans/wb-core-001-normative-architecture.md
docs/reports/reviews/wb-core-001-pr-review-4.md
```

No specification or ADR change is authorized in this pass. The Critic report
and first three PR review reports are read-only historical evidence. No other
path may change.

## Commit Structure

This corrective pass uses two commits:

1. a normative correction commit containing `FILE_REGISTRY.yml`,
   `PROJECT_MAP.md`, and this Work Block;
2. an evidence-only commit creating
   `docs/reports/reviews/wb-core-001-pr-review-4.md`.

The second commit changes only that report path.

## Operational Release-State Registration

WB-CORE-001 remains the active migration Work Block under the existing
runtime-neutral control-plane release-state contract. `PROJECT_MAP.md` and
`FILE_REGISTRY.yml` continue to identify:

- `runtime_neutral_control_plane` as current operational architecture;
- this Work Block as active and `in_progress`;
- `portable_agentic_sdlc_project_kit` as the `proposed` target architecture;
- canonical static evidence directory classes.

This pass restores static operational inventory and relationships that remain
valid for the current control plane. It does not promote the portable target,
archive the current architecture, alter accepted/proposed authority state, or
register any current review verdict or report pointer.

Normative navigation does not register individual review, verification,
evaluation, or closeout reports and does not mirror mutable verdicts, subjects,
findings, limitations, coverage, or another-pass state. Evidence is discovered
from canonical directories and structured report frontmatter.

## Out of Scope

- specification or ADR changes;
- candidate content;
- installer or packaging code;
- role and skill implementation files;
- templates, tests, fixtures, or migration scripts;
- runtime/provider configuration changes;
- broad registry simplification or redesign;
- repository settings, secrets, deployment, live state, or data;
- default-branch writes or merge;
- modification of earlier assurance reports;
- creation of a Verifier report.

## Required Decisions

1. Product remains a complete project kit, not a skills library or control plane.
2. Runtime neutrality remains non-ownership of runtime/provider concerns.
3. Six roles receive separate contracts; shared authority stays in `AGENTS.md`.
4. Exactly nine procedural skills form the portable core.
5. `memory_bank/` is canonical; `.agentic-local/` is ignored scratch.
6. Quick, Standard, and High-Risk remain risk-based and precise.
7. One active write Work Block is allowed per working tree.
8. Feature-branch commits, push, and PR are allowed; merge remains
   Owner-controlled.
9. Candidate and installer contracts remain specified without implementation.
10. Optional extensions remain outside the portable core.
11. Six migration Work Blocks remain bounded.
12. Critic, Reviewer, and Verifier retain distinct verdict vocabularies.
13. Assurance binds to an exact normative subject.
14. Evidence-only reports may follow their subject without invalidating verdict.
15. Navigation/registry are normative only for authority, architecture,
    canonical paths, active lifecycle state, and accepted/proposed status.
16. Mutable assurance state remains prohibited from normative navigation.
17. Per-report registration remains unnecessary; canonical directories and
    structured frontmatter are the evidence discovery mechanism.
18. Current operational static contracts remain registered until an authorized
    migration or archive Work Block replaces them.
19. Static entries may be omitted only when an explicit canonical wildcard or
    class provides equivalent coverage.

## REV-009 Restoration Scope

Restore static content removed by `88d60b1...` that is unrelated to mutable
assurance state:

- `installation_profiles.rules`;
- `scripts/ci-contract-router.py`;
- `template/.agent/hooks/**`;
- `template/scripts/bootstrap.sh`;
- `template/scripts/validate-installation-profile.py`;
- `template/docs/templates/evaluation-plan-template.json`;
- `template/docs/templates/evaluation-report-template.json`;
- `template/docs/templates/trajectory-event-template.json`;
- the static `related:` metadata for
  `skills/skill-library-maintenance/**`;
- detailed current-operational descriptions in `PROJECT_MAP.md` that were
  shortened without necessity for REV-008.

The following baseline-specific entries remain intentionally unregistered:

- individual completed Work Block entries, because `docs/plans/**` provides the
  canonical static class and `migration_state.completed_work_blocks` preserves
  the authoritative completed list;
- individual Critic and Reviewer report entries, because
  `docs/reports/reviews/**` provides the canonical evidence class and report
  frontmatter carries subject, verdict, findings, coverage, and limitations.

## Execution Plan

1. Resolve current PR head and stop on unexpected divergence.
2. Preserve REV-001 through REV-008.
3. Compare current navigation against baseline `7ccec4d...`.
4. Restore unrelated static operational registry rules, entries, and metadata.
5. Restore unrelated detailed operational map descriptions.
6. Keep mutable assurance mirrors absent and static evidence classes intact.
7. Confirm every non-restored static deletion has explicit wildcard coverage.
8. Commit the corrected normative subject.
9. Create the fourth review in a separate evidence-only commit.
10. Run release-state and Framework Contracts workflows.
11. Leave PR open and unmerged for another Reviewer pass.

## Acceptance Criteria

- [x] REV-001 through REV-008 remain accepted and unchanged.
- [x] `status: in_progress` is preserved.
- [x] Current operational and proposed target architectures remain distinct.
- [x] Role-specific verdict vocabularies remain unchanged.
- [x] Exact normative-subject and evidence-only semantics remain explicit.
- [x] Proposed-to-accepted finalization sequence remains unchanged.
- [x] Mutable assurance mirrors remain absent.
- [x] Static evidence directory registration remains available.
- [x] Evidence discovery remains canonical-directory and frontmatter based.
- [x] Unrelated static operational registry rules and entries are restored.
- [x] Unrelated static `related:` metadata is restored.
- [x] Remaining omitted individual completed Work Block entries are covered by
  `docs/plans/**` and `migration_state.completed_work_blocks`.
- [x] Remaining omitted individual review entries are covered by
  `docs/reports/reviews/**` and structured frontmatter.
- [x] `PROJECT_MAP.md` retains detailed current-operational descriptions without
  mutable assurance enumeration.
- [x] Changes are restricted to the approved four-path write-set.
- [ ] A later Reviewer returns `READY` for the corrected normative subject.
- [ ] A later Verifier returns `READY`.
- [ ] Owner authorizes accepted-status finalization and separately approves merge.

## Self-Checks

Check:

- no mutable review or verification verdict, SHA, findings, coverage,
  limitations, current/latest report pointer, or another-pass state in normative
  navigation;
- static review, verification, evaluation, and closeout directory classes;
- all restored operational registry paths and `installation_profiles.rules`;
- explicit wildcard coverage for every intentionally non-restored static entry;
- active Work Block agreement across frontmatter, map, and registry;
- operational architecture `runtime_neutral_control_plane`;
- target status `proposed`;
- no target-architecture promotion;
- no runtime/provider artifact gains authority;
- no placeholder markers;
- final evidence-only commit changes only the fourth-review report.

## Current State

- **Define:** complete for the proposed target architecture.
- **Critic:** historical `APPROVE_WITH_CHANGES`; unchanged.
- **REV-001—REV-008:** preserved as accepted prior corrections.
- **REV-009:** correction active; Author Resolution will be recorded in the
  fourth review after the normative correction commit.
- **Release state:** this Work Block remains active under the current
  runtime-neutral control-plane contract.
- **Reviewer:** another pass remains required against the corrected normative
  subject.
- **Verifier:** pending; no Verifier report is created by this pass.
- **Accepted-status finalization:** pending and Owner-controlled.
- **Closeout:** pending; Work Block is not complete.
- **Merge:** requires separate explicit Owner approval.
