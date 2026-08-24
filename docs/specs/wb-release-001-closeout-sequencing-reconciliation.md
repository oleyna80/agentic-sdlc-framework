---
schema_version: 1
artifact_type: specification
artifact_id: wb-release-001-closeout-sequencing-reconciliation
work_block_id: WB-RELEASE-001
status: approved
created_at: 2026-08-24
revision: define-r5-2026-08-24
owner_approval: Owner authorized a corrective PR-history rewrite/force-push and directed prevention of recurrence after the exact-head Framework Contracts failure on 2026-08-24. Refreshed r5 Define assurance supports only the exact bounded Execute write-set; no candidate, push, PR, or merge authority is implied.
---

# WB-RELEASE-001 — Release-State Closeout Sequencing Reconciliation

## Purpose and Authority

This Managed Work Block reconciles a sequencing defect discovered while closing
WB-CORE-003G. The repository currently requires the final completed Work Block,
registry projection, and successful closeout report to coexist for ordinary
release-state validation. The accepted evidence sequence instead requires final
applicable assurance of the terminal normative projection before the
evidence-only report commit. A status-only candidate therefore fails the ordinary
validator before final assurance can be recorded.

This approved specification defines only the bounded prospective Execute
write-set stated in its revision record. It must not retrofit or relabel
historical evidence. It defines a prospective contract for an explicit,
local-only pre-closeout candidate and its later evidence-only persistence.

The first attempted evidence-only persistence exposed a CI integration gap: the
release-state validator correctly requires Git ancestry to bind a candidate to
its evidence commit, while its dedicated GitHub workflow used GitHub's default
shallow checkout. Revision r4 corrected that direct consumer, but exact-head
CI then exposed a second direct consumer: the `contracts` job in
`.github/workflows/framework-contracts.yml` invokes the same ancestry-dependent
validation through governance validation with its own shallow checkout. This
revision must make required history available to both identified direct
consumers and make that bounded dependency executable, rather than weakening
the validator or appending an unassured source change after terminal evidence.

## Requirements

- REQ-001: The release-state contract must distinguish a normal repository head
  from an explicit local-only pre-closeout candidate. The ordinary validator must
  continue to fail closed for incomplete closeout evidence on a normal head.
- REQ-002: A pre-closeout candidate must have one persistent, machine-readable
  declaration in `FILE_REGISTRY.yml`. It must bind exactly one Work Block,
  one predecessor completed Work Block, the candidate's `assurance_pending`
  state, its required terminal evidence classes, and the normative manifest to
  be assured. The declaration is created before terminal assurance and remains
  unchanged after it; an evidence-only persistence commit must not remove or
  rewrite it.
- REQ-003: Candidate-only Work Block and registry/map markers must mean
  `closeout_candidate`/`assurance_pending`, not `completed`,
  `success-closeout`, or a READY final gate. `closeout_candidate` is a new
  explicit lifecycle state, with `Current Stage: Close`, `Stage State:
  assurance_pending`, and `Closeout Mode: candidate`; the registry/map carry
  the same candidate state. Candidate validation must emit a distinct
  non-release-ready result and must preserve registry/map agreement,
  terminal-marker syntax, and all applicable pre-existing closeout evidence.
- REQ-004: The candidate validation path must validate the intended terminal
  projection sufficiently for independent Reviewer, Verifier, and Drift
  assurance. A reproducible comparison command must bind the exact candidate
  revision, the final evidence revision, and the allowed report/closeout
  manifest; it must reject any normative-path delta between them.
- REQ-005: The authoritative release-state contract must define
  `closeout_candidate` completion as an explicit two-part canonical state: the
  immutable candidate declaration and its bound required terminal evidence.
  The candidate stays outside `completed_work_blocks`; raw
  `latest_completed_work_block` stays the declared immediate predecessor; and
  `active_work_block` remains null. `PROJECT_MAP.md` carries the same one
  `closeout_candidate` record. The reports do not overwrite any raw state;
  they satisfy the declared finalization condition and cause the validator to
  derive exactly that candidate as the effective completed/latest entry only
  when every required report binds the candidate revision. Without that
  condition, `closeout_candidate` remains non-final and ordinary mode fails.
- REQ-006: The protocol and machine-readable acceptance sequence must state the
  same prospective order: preliminary assurance; authorized local candidate;
  candidate validation and final applicable assurance; evidence-only report
  persistence; ordinary release-state validation and CI on the resulting PR
  head; then separate Owner merge approval.
- REQ-007: Executable positive and adversarial fixtures must prove both modes:
  a valid ordinary completed state, a valid explicit pre-closeout candidate, and
  rejection of candidate mode when its declaration, predecessor binding,
  registry/map projection, terminal markers, or evidence-only boundary is
  malformed or absent.
- REQ-008: The correction must remain a bounded release-state/procedure change.
  It must not alter completed historical Work Blocks, reopen WB-SKILL-002A/B,
  modify WB-CORE-003G source behavior, grant GitHub authority, weaken default
  release-state checks, or create a general exception for incomplete closeout.
- REQ-009: The Work Block must record a reusable closeout procedure that lets
  WB-CORE-003G resume only after this contract is accepted and implemented; the
  pilot's existing uncommitted status-only files remain out of scope for this
  Work Block.
- REQ-010: The dedicated release-state GitHub Actions workflow must check out
  sufficient Git history for the validator's required candidate-to-evidence
  ancestry proof. The framework must have a deterministic contract check that
  fails if this workflow regresses to a shallow checkout. This prevention is
  limited to that named workflow and must not change candidate-manifest
  validation or add a repository-wide workflow policy.
- REQ-011: Every identified CI job that directly invokes the ancestry-dependent
  release-state validation, including through `bash scripts/validate-governance.sh`,
  must check out sufficient Git history. The identified direct consumers are
  `.github/workflows/release-state-contract.yml` job `release-state` and
  `.github/workflows/framework-contracts.yml` job `contracts`. The executable
  contract must reject a shallow, absent, or misplaced full-history setting for
  either named consumer. This is an explicit bounded inventory, not a
  repository-wide workflow scan or a change to candidate-manifest semantics.

## Acceptance Criteria

- AC-001 [req=REQ-001]: Default `python3 scripts/validate-release-state.py`
  continues to reject a repository head whose latest completed Work Block lacks
  its required successful closeout evidence.
- AC-002 [req=REQ-001]: Candidate validation is selected only by an explicit,
  machine-readable candidate declaration and a deliberate command-line mode; it
  cannot be activated implicitly by a missing closeout report.
- AC-003 [req=REQ-002]: Candidate validation accepts only one persistent
  `FILE_REGISTRY.yml` declaration containing the Work Block ID, predecessor ID,
  `assurance_pending` state, required evidence classes, and normative manifest;
  it rejects a missing, duplicate, or malformed record.
- AC-004 [req=REQ-003]: Candidate-only Work Block and registry/map projections
  use explicit `closeout_candidate`/`assurance_pending` markers and contain no `completed`,
  `success-closeout`, or READY final-gate claim. Candidate mode exits
  successfully only with the distinct `CANDIDATE_READY` classification; it is
  not ordinary `READY`, release-ready, or authority for push, PR, merge, CI,
  or external-state claims.
- AC-005 [req=REQ-004]: A reproducible validator command accepts exact
  candidate and final-evidence revisions plus the candidate manifest, verifies
  terminal reports bind the candidate revision, and rejects every changed path
  outside the approved evidence/closeout manifest, including a mutated
  persistent candidate record.
- AC-006 [req=REQ-005]: Ordinary mode derives `completed` for exactly one
  `closeout_candidate` only from its persistent declaration and every bound
  terminal report. It requires the raw completed/latest entry to remain the
  declared immediate predecessor, `active_work_block` to remain null, and the
  `PROJECT_MAP.md` candidate record to agree; it rejects absent, wrong-subject,
  incomplete, or duplicate evidence, and it never treats raw evidence as a
  direct overwrite of the Work Block state.
- AC-007 [req=REQ-006]: `governance/release-state.md`, the self-hosting SDD
  protocol, and `FILE_REGISTRY.yml` prescribe one non-contradictory prospective
  sequence and preserve separate Owner merge authority.
- AC-008 [req=REQ-007]: Fixture coverage includes normal success, valid
  candidate success with `CANDIDATE_READY`, undeclared/default-mode rejection,
  duplicate or incorrect predecessor binding, map disagreement, prohibited
  success markers, missing evidence, and forbidden normative changes between
  candidate and evidence revisions.
- AC-009 [req=REQ-008]: The frozen implementation manifest contains only the
  Owner-approved contract/procedure/validator/fixture paths; no completed
  historical Work Block or unrelated source path is changed.
- AC-010 [req=REQ-009]: The closeout records the exact prospective procedure,
  residual limitations, and the explicit condition for resuming WB-CORE-003G;
  it does not claim that WB-CORE-003G has been closed.
- AC-011 [req=REQ-010]: `.github/workflows/release-state-contract.yml` sets
  `fetch-depth: 0` on its checkout step, and
  `scripts/test-release-state-contracts.py` deterministically rejects a
  shallow, absent, or misplaced full-history checkout configuration.
- AC-012 [req=REQ-011]: `.github/workflows/framework-contracts.yml` sets
  `fetch-depth: 0` on the `contracts` job checkout. The release-state fixture
  deterministically checks both named direct consumers and rejects shallow,
  absent, or misplaced full-history checkout configuration for either job.

## Design Decision to Validate in Define

The leading option is a strict two-mode validator:

1. **Ordinary mode** remains the sole mode for a branch that may be pushed,
   reviewed, merged, or treated as release-ready. It requires a successful
   closeout report for the latest completed Work Block exactly as today.
2. **Pre-closeout candidate mode** is invoked deliberately for one local,
   unpublished candidate revision. `FILE_REGISTRY.yml` contains one persistent
   `pre_closeout_candidate` record with: Work Block ID; predecessor completed
   Work Block ID; `closeout_candidate`/`assurance_pending` state; required
   `review`, `verification`, `drift`, and `closeout` evidence classes; and an
   ordered normative manifest. The Work Block and registry/map use the same
   `closeout_candidate`/`assurance_pending` identity; they do not claim
   `completed`, `success-closeout`, or final READY gates.
   Candidate mode validates that record, the terminal projection, map agreement,
   and predecessor closeout while permitting only the new candidate evidence to
   be absent. A successful run emits `CANDIDATE_READY`, never ordinary `READY`.
3. After independent terminal assurance, an evidence-only commit persists the
   required reports and successful closeout evidence without changing the
   candidate record or its assured normative manifest. A dedicated reproducible
   comparison receives the exact candidate and final-evidence revisions and
   rejects any changed path outside the declared report/closeout manifest. The
   authoritative release-state contract recognizes the immutable candidate
   declaration and its bound terminal evidence as a two-part canonical state.
   The raw registry latest-completed entry stays the candidate's immediate
   predecessor, `active_work_block` stays null, and the map retains the matching
   candidate record; the validator derives an effective completed final entry
   only then. The reports do not overwrite the candidate's raw lifecycle state.
   Ordinary mode is the only passing mode after that condition is satisfied.

Candidate mode grants no push, PR, merge, release, CI, or external-state
authority; a local validator cannot physically prevent such actions. Default
CI continues to run ordinary mode and therefore rejects an incomplete
candidate. The exact flag/interface names remain implementation details, but
the persistent declaration, markers, result classification, and cross-revision
proof above are required design constraints. They require a refreshed
requirements-quality review, consistency analysis, Critic review, an Owner
approved specification revision, and an explicit future source write-set.

The CI history correction is part of that same bounded procedure: it is made
before the new candidate is frozen and is independently assured with the rest
of the frozen source subject. It is never appended after evidence-only
persistence.

## Non-Goals

- Changing the completed historical record of WB-CORE-003G, WB-SKILL-002A, or
  WB-SKILL-002B.
- Treating a local candidate as a release-ready repository head.
- Weakening ordinary release-state validation, CI, or external GitHub controls.
- Source/product/runtime/provider changes, model routing, dependencies, or
  template-wide redesign unless later Define evidence establishes necessity.
