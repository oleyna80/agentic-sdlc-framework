---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-001-normative-architecture
work_block_id: WB-CORE-001
status: completed
owner_role: orchestrator
created_at: 2026-07-29
last_verified: 2026-07-31
base_revision: 0fce7389d27690482e910e942a1f3138c2fef123
branch: agent/portable-kit-normative-architecture
process_level: Standard
---

# WB-CORE-001 — Normative Architecture for the Portable Agentic SDLC Project Kit

## Objective

Define, assure, accept, and close the normative architecture for the Portable
Agentic SDLC Project Kit before candidate, installer, role, skill, template,
test, or migration implementation begins.

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
- renewed preliminary Reviewer and Verifier subject:
  `9c169fd97bdbe90bb2fc1133fff29878d1373396`;
- renewed preliminary Reviewer report:
  `docs/reports/reviews/wb-core-001-pr-review-after-preliminary-verification.md`;
- renewed preliminary Reviewer verdict: `READY`;
- renewed preliminary Verifier report:
  `docs/reports/verification/wb-core-001-preliminary-verification-2.md`;
- renewed preliminary Verifier verdict: `READY`;
- accepted normative subject:
  `ca14aa1aae3e0168678f0cee93da2a6b9dcc7e23`;
- final Reviewer evidence head:
  `4a0eb36f79584003ed5656b8ba1472227687360e`;
- final Verifier evidence head:
  `864dc547767774d0e2390c32f43f770170d083b3`;
- current repository contracts and history.

Historical assurance remains bound to its exact subject. The historical
`NOT_READY` verdict for `674e992...` is unchanged. Renewed preliminary assurance
for `9c169fd...` and final assurance for `ca14aa1...` are separate later
assessments and do not rewrite prior evidence.

## Accepted Prior Decisions

REV-001 through REV-009 are not reopened. Preserve:

- complete project-kit product boundary;
- runtime/provider non-ownership;
- active Work Block precedence;
- separate portable roles;
- exactly nine core skills;
- canonical committed `memory_bank/` target contract;
- Quick / Standard / High-Risk model;
- one write Work Block per working tree;
- exact normative-subject semantics;
- evidence-only report commits;
- prohibition of mutable assurance mirrors;
- current operational architecture `runtime_neutral_control_plane`;
- portable target status `accepted` but not promoted;
- Owner-controlled later Work Blocks, promotion, archival, and merge.

## Process and Authority Classification

- **Process level:** Standard.
- **Side effects:** one feature-branch closeout and SSOT-reconciliation commit;
  no PR-description update, merge, deployment, repository-setting, or operational
  mutation.
- **Write authority:** scoped Orchestrator / Documentation Coder for the exact
  five-file closeout write-set.
- **Merge authority:** explicitly denied; PR #12 merge requires a separate future
  Owner authorization.
- **Deployment/data/secrets:** none.
- **Authorized purpose:** WB-CORE-001 closeout and lifecycle SSOT reconciliation
  only; no architecture, behavior, process, role, skill, memory, installer,
  migration, candidate, or implementation change.
- **Completion:** completed for normative architecture only. Later implementation,
  pilot, promotion, archival, and merge remain separately gated.

## Approved Write-Set — Current Closeout Pass

Modify or create exactly:

```text
docs/plans/wb-core-001-normative-architecture.md
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/reports/drift/wb-core-001-normative-architecture.md
docs/reports/closeout/wb-core-001-normative-architecture.md
```

No specification, ADR, Reviewer, Verifier, Critic, evaluation, historical report,
memory, runtime, integration, candidate, implementation, template, installer,
test, migration, workflow, script, repository-setting, deployment, or PR-metadata
path may change.

## Historical Execution Write-Sets

The accepted-status finalization pass used exactly six normative files:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/plans/wb-core-001-normative-architecture.md
```

The preliminary-verification remediation used exactly three normative files:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
docs/plans/wb-core-001-normative-architecture.md
```

These write-sets are historical execution records and do not authorize current
changes.

## Commit Structure

Create exactly one closeout commit:

```text
docs(core): close WB-CORE-001 normative architecture
```

The commit changes exactly the five approved paths. The drift and closeout reports
are created in the same repository closeout commit because this pass atomically
reconciles lifecycle SSOT; no separate evidence-only commit is authorized.

## Operational Architecture and Navigation Boundary

The current repository remains the operational
`runtime_neutral_control_plane`. The Portable Agentic SDLC Project Kit remains the
`accepted` normative target contract but is not promoted, installed, implemented,
or the current operational architecture.

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` synchronize the completed Work Block,
null active Work Block, accepted target classification, latest completed Work
Block, and canonical closeout path. They do not register individual assurance,
drift, or closeout report instances or mirror mutable verdicts, subjects,
findings, limitations, coverage, workflow runs, or latest-report state.

## Preliminary Assurance Record

```text
Historical preliminary subject:
674e992548c0474b79bbf261ee7fbceae8eaff4a

Historical preliminary Verifier verdict:
NOT_READY

Renewed preliminary subject:
9c169fd97bdbe90bb2fc1133fff29878d1373396

Renewed preliminary Reviewer verdict:
READY

Renewed preliminary Verifier verdict:
READY

Renewed preliminary Verifier matrix:
20 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_APPLICABLE
```

## Accepted-Status Owner Authorization Record

```text
Owner authorization date: 2026-07-30
Authorized action: accepted-status finalization only
Merge authorization: explicitly denied
```

Exact Owner statement:

> Да, как Owner разрешаю status-finalization commit в указанном scope.
> Merge не разрешаю.

This authorization is preserved and applies only to the earlier accepted-status
transition.

## Final Assurance Record

```text
Accepted normative subject:
ca14aa1aae3e0168678f0cee93da2a6b9dcc7e23

Final Reviewer report:
docs/reports/reviews/wb-core-001-final-review.md

Final Reviewer verdict:
READY

Final Reviewer matrix:
13 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_APPLICABLE

Final Verifier report:
docs/reports/verification/wb-core-001-final-verification.md

Final Verifier verdict:
READY

Final Verifier matrix:
24 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_APPLICABLE

Final evidence-only head:
864dc547767774d0e2390c32f43f770170d083b3

Framework Contracts:
run 766 — success

Release State Contract:
run 345 — success
```

The final reports bind to accepted normative subject `ca14aa1...`. Commits after
that subject through `864dc547...` contain only the final Reviewer and Verifier
reports and do not alter normative architecture.

## Owner Closeout Authorization Record

```text
Owner authorization date: 2026-07-31
Authorized action: WB-CORE-001 closeout and five-file SSOT reconciliation
WB-CORE-002 authorization: explicitly denied
Promotion authorization: explicitly denied
Archival authorization: explicitly denied
Merge authorization: explicitly denied
```

Exact Owner statement:

> Да, как Owner разрешаю WB-CORE-001 closeout и SSOT reconciliation в указанном пятифайловом scope. WB-CORE-002, promotion, archival и merge не разрешаю.

The accepted-status authorization and closeout authorization govern different
actions and neither grants authority for later implementation or integration.

## Historical Preliminary-Verification Remediation — Completed

The remediation that produced `9c169fd...` resolved:

- `VER-006`: explicit disposition for current and historical mechanisms while
  retaining exactly nine core skills and provider-neutral authority;
- `VER-007`: owner, update trigger, required/prohibited content, and retention for
  each canonical memory surface;
- `VER-008`: fail-closed Quick / Standard / High-Risk selection based on risk,
  ambiguity, side effects, reversibility, authority, and verification;
- `VER-014`: explicit canonical-root, path-traversal, link-containment,
  apply-time revalidation, and all-or-nothing installer requirements.

The historical remediation is complete and was independently re-reviewed and
re-verified before accepted-status finalization.

## Memory Classification

Engineering-memory classification:
not-applicable — the accepted specification and ADRs are already the canonical,
higher-authority durable record. Creating a duplicate engineering-memory entry
would weaken SSOT.

Operational-memory classification:
not-applicable — the current operational repository does not contain the target
committed memory_bank surface. Creating that surface is implementation owned by
WB-CORE-002 and is outside this closeout authorization.

No new memory file or target `memory_bank/` surface was created.

## Out of Scope and Future Gates

- WB-CORE-002 activation or portable candidate implementation;
- roles, skills, target memory seed, templates, installer, tests, packaging, or
  migration implementation;
- synthetic dry run;
- HardwareLab pilot;
- promotion of the portable target to current operational architecture;
- archival of the runtime-neutral control plane;
- deployment, live-state mutation, repository settings, or secrets;
- default-branch writes, merge, or auto-merge;
- PR-description or review-thread mutation.

Promotion and archival are WB-CORE-006 responsibilities. Merge remains separately
Owner-controlled. These are future gates, not failed WB-CORE-001 acceptance
criteria.

## Closeout Execution Plan

1. Resolve PR #12 and require head
   `864dc547767774d0e2390c32f43f770170d083b3`.
2. Confirm `ca14aa1...` is followed only by the final Reviewer and Verifier
   report commits.
3. Confirm final Reviewer `READY` with matrix 13/0/0/0.
4. Confirm final Verifier `READY` with matrix 24/0/0/0.
5. Confirm workflow runs 762/341, 764/343, and 766/345 are successful.
6. Record exact Owner closeout authorization and explicit denials.
7. Change Work Block lifecycle to `completed`.
8. Reconcile map and registry completed/active/release-state projections.
9. Create aligned drift and success-closeout evidence.
10. Validate the exact five-file diff and repository release-state contracts.
11. Create one closeout commit and leave all later gates unopened.

## Acceptance Criteria

- [x] Final Reviewer returned `READY` for
  `ca14aa1aae3e0168678f0cee93da2a6b9dcc7e23`.
- [x] Final Reviewer matrix is 13 PASS, 0 FAIL, 0 BLOCKED, and
  0 NOT_APPLICABLE.
- [x] Final Verifier returned `READY` for the same accepted normative subject.
- [x] Final Verifier matrix is 24 PASS, 0 FAIL, 0 BLOCKED, and
  0 NOT_APPLICABLE.
- [x] Both final evidence-only reports were committed.
- [x] Framework Contracts run 766 and Release State Contract run 345 passed on
  the final Verifier evidence head.
- [x] Drift audit returned `ALIGNED`.
- [x] Closeout report was created.
- [x] Work Block status became `completed`.
- [x] Map and registry completed-state projections were reconciled.
- [x] No active Work Block remains.
- [x] Reusable-memory classification was recorded without creating duplicate
  memory.
- [x] Current operational architecture remains
  `runtime_neutral_control_plane`.
- [x] Portable target remains accepted but unimplemented, uninstalled, and
  unpromoted.
- [x] WB-CORE-002 remains planned and unauthorized.
- [x] No promotion or archival occurred.
- [x] No merge occurred.
- [x] No substantive architecture, behavior, process, role, skill, memory,
  installer, migration, evidence-semantic, or implementation rule changed.

## Self-Checks

Check:

- exact starting head and report-only ancestry after `ca14aa1...`;
- exact five-file commit write-set and one closeout commit;
- YAML and frontmatter parsing;
- exactly one terminal Final State section and no legacy Current State section;
- exact terminal marker values;
- closeout lifecycle markers exactly once;
- nonempty residual-risk and follow-up sections;
- external VCS marker begins with `non-normative`;
- no concrete hosting-platform state in closeout evidence;
- map machine block and visible Migration Work agree;
- registry and map completed lists agree;
- active Work Block is null in map and registry;
- WB-CORE-001 is listed once as completed;
- WB-CORE-002 remains planned;
- current operational architecture remains unchanged;
- accepted target remains unpromoted;
- no individual assurance-report registration;
- no target memory implementation;
- no later Work Block activation;
- release-state and full contract validation.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic normative documentation, independent semantic assurance, and repository contract validation are sufficient
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

WB-CORE-001 successfully defined and accepted the portable-kit normative
architecture. The current operational architecture remains
`runtime_neutral_control_plane`, while the accepted target remains
`portable_agentic_sdlc_project_kit`.

The target is not implemented, installed, or promoted. No active implementation
Work Block remains. WB-CORE-002 remains planned and requires separate explicit
Owner authority. Promotion and archival remain WB-CORE-006 responsibilities.
Merge remains separately Owner-controlled and is not authorized.
