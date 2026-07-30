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
- historical preliminary Verifier normative subject:
  `674e992548c0474b79bbf261ee7fbceae8eaff4a`;
- historical preliminary verification report:
  `docs/reports/verification/wb-core-001-preliminary-verification.md`;
- historical preliminary Verifier verdict: `NOT_READY`;
- historical failed criteria: `VER-006`, `VER-007`, `VER-008`, `VER-014`, and
  derived `VER-020`;
- renewed Reviewer subject:
  `9c169fd97bdbe90bb2fc1133fff29878d1373396`;
- renewed Reviewer report:
  `docs/reports/reviews/wb-core-001-pr-review-after-preliminary-verification.md`;
- renewed Reviewer verdict: `READY`;
- renewed preliminary Verifier subject:
  `9c169fd97bdbe90bb2fc1133fff29878d1373396`;
- renewed preliminary Verifier report:
  `docs/reports/verification/wb-core-001-preliminary-verification-2.md`;
- renewed preliminary Verifier verdict: `READY`;
- status-finalization starting evidence-only head:
  `668808bed0d38b483f46f034050939f25735b1cd`;
- current repository contracts and history.

The historical `NOT_READY` report remains unchanged and authoritative only for
its exact historical subject. The renewed Reviewer and preliminary Verifier
reports independently return `READY` for `9c169fd...`; neither report is modified
by this status-finalization pass.

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
- portable target status `accepted` but not promoted;
- WB-CORE-001 status `in_progress`;
- Owner-controlled promotion, closeout, and merge.

## Process and Authority Classification

- **Process level:** Standard.
- **Side effects:** one feature-branch status-only normative documentation commit;
  no PR-description update, merge, deployment, or operational mutation.
- **Write authority:** scoped Documentation Coder for the exact six-file
  status-finalization write-set.
- **Merge authority:** explicitly denied; PR #12 merge requires a separate future
  Owner authorization.
- **Deployment/data/secrets:** none.
- **Authorized purpose:** accepted-status finalization only; no architecture,
  behavior, process, role, skill, memory, installer, migration, or implementation
  change.
- **Completion:** `in_progress`; final Reviewer, final Verifier, final evidence-only
  reports, resulting-head CI, closeout, memory/SSOT synchronization where
  applicable, promotion, archival, and merge remain open.

## Approved Write-Set

Modify exactly:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/plans/wb-core-001-normative-architecture.md
```

No Reviewer, Verifier, Critic, evaluation, closeout, memory, runtime, candidate,
implementation, template, installer, test, migration, repository-setting, or
deployment path may change. The PR description and review threads are not
modified.

## Commit Structure

Create exactly one normative commit:

```text
docs(core): accept portable kit normative architecture
```

The commit changes exactly the six approved normative paths and becomes the new
normative subject for final applicable assurance. No evidence report is created
or modified in this commit.

## Operational Architecture and Navigation Boundary

The current repository remains the operational
`runtime_neutral_control_plane`. The Portable Agentic SDLC Project Kit is now the
`accepted` normative target contract but is not promoted, installed, implemented,
or the current operational architecture. This Work Block remains active and
`in_progress`.

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` synchronize only accepted target status,
canonical target classification, and the unchanged current operational
architecture. They do not register individual assurance reports or mirror mutable
verdicts, subjects, findings, limitations, coverage, or another-pass state.
Evidence continues to be discovered from canonical directories and structured
report frontmatter.

## Preliminary Assurance Record

```text
Reviewer subject: 9c169fd97bdbe90bb2fc1133fff29878d1373396
Reviewer verdict: READY
Reviewer report: docs/reports/reviews/wb-core-001-pr-review-after-preliminary-verification.md

Preliminary Verifier subject: 9c169fd97bdbe90bb2fc1133fff29878d1373396
Preliminary Verifier verdict: READY
Verifier report: docs/reports/verification/wb-core-001-preliminary-verification-2.md
Verifier matrix: 20 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_APPLICABLE
```

These verdicts authorize no merge and become preliminary evidence for the
Owner-authorized status transition. Final applicable assurance must assess the
new status-finalized normative subject.

## Owner Authorization Record

```text
Owner authorization date: 2026-07-30
Authorized action: accepted-status finalization only
Merge authorization: explicitly denied
```

Exact Owner statement:

> Да, как Owner разрешаю status-finalization commit в указанном scope.
> Merge не разрешаю.

## Historical Preliminary-Verification Remediation — Completed

The following three-file remediation produced normative subject
`9c169fd97bdbe90bb2fc1133fff29878d1373396`. It is retained as historical
context and is not the current authorized write-set.

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

- candidate, role, skill, memory, template, installer, test, packaging, or
  migration implementation;
- WB-CORE-002 or any later implementation Work Block;
- promotion of the portable target to current operational architecture;
- archival of the runtime-neutral control plane;
- closeout or completion of WB-CORE-001;
- memory/SSOT synchronization beyond recording this Work Block gate state;
- runtime/provider configuration or operational mutation;
- repository settings, secrets, deployment, live state, or data;
- default-branch writes, merge, or auto-merge;
- creation or modification of assurance, evaluation, or closeout reports;
- PR-description or review-thread mutation.

## Execution Plan

1. Resolve PR #12 and require head
   `668808bed0d38b483f46f034050939f25735b1cd`.
2. Confirm commits after `9c169fd...` change only the renewed Reviewer and
   preliminary Verifier reports.
3. Confirm both reports return `READY` and the Verifier matrix is 20/0/0/0.
4. Confirm Framework Contracts and Release State Contract are green on the
   preliminary subject and both evidence-only heads.
5. Record the exact Owner authorization and merge denial.
6. Change only current target status, status-dependent prose, map/registry target
   classification, registry version, and this Work Block gate state.
7. Inspect the complete diff and prove that every changed line is status
   finalization or gate-state synchronization.
8. Create one six-file normative commit with the authorized message.
9. Run Framework Contracts and Release State Contract on the new subject.
10. Leave PR #12 open and unmerged for final Reviewer and Verifier assurance.

## Acceptance Criteria

- [x] Renewed Reviewer assessed
  `9c169fd97bdbe90bb2fc1133fff29878d1373396` and returned `READY`.
- [x] Renewed preliminary Verifier assessed the same subject and returned `READY`.
- [x] Preliminary Verifier matrix is 20 PASS, 0 FAIL, 0 BLOCKED, and
  0 NOT_APPLICABLE.
- [x] Owner authorized accepted-status finalization on 2026-07-30.
- [x] Owner explicitly denied merge authorization.
- [x] Specification status is `accepted`.
- [x] Product-boundary ADR status is `accepted`.
- [x] Roles/memory/installation ADR status is `accepted`.
- [x] `PROJECT_MAP.md` identifies an accepted but unpromoted target.
- [x] `FILE_REGISTRY.yml` classifies the target and three artifacts as `accepted`.
- [x] Current operational architecture remains `runtime_neutral_control_plane`.
- [x] WB-CORE-001 remains `in_progress`.
- [x] No substantive architecture, behavior, process, role, skill, memory,
  installer, migration, or implementation rule changes.
- [ ] Final Reviewer returns the applicable verdict against the new
  status-finalized normative subject.
- [ ] Final Verifier returns the applicable verdict against that subject.
- [ ] Final evidence-only reports are committed.
- [ ] Framework Contracts and Release State Contract pass on the resulting
  evidence-only PR head.
- [ ] Truthful closeout and memory/SSOT synchronization are completed where
  applicable.
- [ ] Promotion and legacy archival are performed by their authorized later Work
  Block.
- [ ] Separate Owner merge approval is obtained and merge is performed.

## Self-Checks

Check:

- starting head and post-`9c169fd...` report-only ancestry;
- exact six-file commit write-set and one normative commit;
- specification and both ADR frontmatter values are `accepted`;
- map states accepted target and unchanged current operational architecture;
- registry version increments once and target/specific entries are `accepted`;
- registry wildcard architecture-decision class is unchanged;
- Work Block frontmatter remains `in_progress`;
- exact Owner authorization and explicit merge denial are recorded;
- no evidence report, mutable assurance mirror, candidate, runtime, implementation,
  template, installer, test, migration, or repository-setting path changes;
- specification and ADR headings/frontmatter parse;
- YAML parses;
- complete diff contains only status-finalization and gate-state synchronization;
- Framework Contracts and Release State Contract on the resulting subject;
- PR #12 remains open and unmerged.

## Current State

```text
Normative target status: accepted
Current operational architecture: runtime_neutral_control_plane
WB-CORE-001: in_progress
Final Reviewer: required against new subject
Final Verifier: required against new subject
Closeout: blocked
Promotion: not performed
Merge: explicitly not authorized
```

Candidate implementation, WB-CORE-002, final evidence reports, resulting-head CI,
memory/SSOT closeout synchronization, legacy archival, and integration remain
outside this status-only commit.
