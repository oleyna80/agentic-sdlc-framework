---
schema_version: 1
artifact_type: specification
artifact_id: wb-release-001-closeout-sequencing-reconciliation
work_block_id: WB-RELEASE-001
status: draft
created_at: 2026-08-24
revision: define-r1-2026-08-24
owner_approval: Owner approved Define investigation only on 2026-08-24. No source, validator, governance, template, commit, push, pull-request, merge, or external authority is granted by this draft.
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

This draft is Define-only and creates no source authority. It must not retrofit
or relabel historical evidence. It defines a prospective contract for an
explicit, local-only pre-closeout candidate and its later evidence-only
persistence, if that design survives Define quality and Critic review.

## Requirements

- REQ-001: The release-state contract must distinguish a normal repository head
  from an explicit local-only pre-closeout candidate. The ordinary validator must
  continue to fail closed for incomplete closeout evidence on a normal head.
- REQ-002: A pre-closeout candidate must bind one exact terminal Work Block
  projection and preserve registry/map agreement, terminal-marker syntax, and
  all applicable pre-existing closeout evidence without representing the
  candidate as release-ready, pushable, merge-ready, or externally complete.
- REQ-003: The candidate validation path must validate the intended terminal
  projection sufficiently for independent Reviewer, Verifier, and Drift
  assurance, while requiring final evidence persistence to contain no hidden
  normative changes beyond the candidate subject.
- REQ-004: The protocol and machine-readable acceptance sequence must state the
  same prospective order: preliminary assurance; authorized local candidate;
  candidate validation and final applicable assurance; evidence-only report
  persistence; ordinary release-state validation and CI on the resulting PR
  head; then separate Owner merge approval.
- REQ-005: Executable positive and adversarial fixtures must prove both modes:
  a valid ordinary completed state, a valid explicit pre-closeout candidate, and
  rejection of candidate mode when its declaration, predecessor binding,
  registry/map projection, terminal markers, or evidence-only boundary is
  malformed or absent.
- REQ-006: The correction must remain a bounded release-state/procedure change.
  It must not alter completed historical Work Blocks, reopen WB-SKILL-002A/B,
  modify WB-CORE-003G source behavior, grant GitHub authority, weaken default
  release-state checks, or create a general exception for incomplete closeout.
- REQ-007: The Work Block must record a reusable closeout procedure that lets
  WB-CORE-003G resume only after this contract is accepted and implemented; the
  pilot's existing uncommitted status-only files remain out of scope for this
  Work Block.

## Acceptance Criteria

- AC-001 [req=REQ-001]: Default `python3 scripts/validate-release-state.py`
  continues to reject a repository head whose latest completed Work Block lacks
  its required successful closeout evidence.
- AC-002 [req=REQ-001]: Candidate validation is selected only by an explicit,
  machine-readable candidate declaration and a deliberate command-line mode; it
  cannot be activated implicitly by a missing closeout report.
- AC-003 [req=REQ-002]: Candidate validation binds exactly one final Work Block
  path, requires it to be the final migration projection and requires
  `FILE_REGISTRY.yml` and `PROJECT_MAP.md` to agree on that projection.
- AC-004 [req=REQ-002]: Candidate documentation and validation prohibit push,
  PR creation, CI/release-ready claims, merge, and external-state assertions
  until evidence-only persistence restores ordinary release-state validity.
- AC-005 [req=REQ-003]: Independent terminal assurance can name the exact
  candidate commit and its normative manifest; later evidence persistence is
  checked to contain only approved report/closeout paths and no candidate
  normative-path change.
- AC-006 [req=REQ-004]: `governance/release-state.md`, the self-hosting SDD
  protocol, and `FILE_REGISTRY.yml` prescribe one non-contradictory prospective
  sequence and preserve separate Owner merge authority.
- AC-007 [req=REQ-005]: Fixture coverage includes normal success, valid
  candidate success, undeclared candidate rejection, default-mode rejection,
  incorrect candidate/latest binding, map disagreement, malformed terminal
  markers, and forbidden normative changes in evidence persistence.
- AC-008 [req=REQ-006]: The frozen implementation manifest contains only the
  Owner-approved contract/procedure/validator/fixture paths; no completed
  historical Work Block or unrelated source path is changed.
- AC-009 [req=REQ-007]: The closeout records the exact prospective procedure,
  residual limitations, and the explicit condition for resuming WB-CORE-003G;
  it does not claim that WB-CORE-003G has been closed.

## Design Decision to Validate in Define

The leading option is a strict two-mode validator:

1. **Ordinary mode** remains the sole mode for a branch that may be pushed,
   reviewed, merged, or treated as release-ready. It requires a successful
   closeout report for the latest completed Work Block exactly as today.
2. **Pre-closeout candidate mode** is invoked deliberately for one local,
   unpublished candidate commit. It validates the candidate declaration,
   terminal Work Block projection, registry/map agreement, and predecessor
   closeout while permitting the candidate's new closeout evidence to be absent.
   It does not return a release-ready verdict and is not CI admission evidence.
3. After independent terminal assurance, an evidence-only commit persists the
   reports and successful closeout evidence without changing the assured
   normative manifest. Ordinary mode then becomes the only passing mode.

The exact candidate declaration shape, predecessor checks, and evidence-only
manifest proof remain design details for the implementation phase. They require
requirements-quality review, consistency analysis, Critic review, an Owner
approved specification revision, and an explicit future source write-set.

## Non-Goals

- Changing the completed historical record of WB-CORE-003G, WB-SKILL-002A, or
  WB-SKILL-002B.
- Treating a local candidate as a release-ready repository head.
- Weakening ordinary release-state validation, CI, or external GitHub controls.
- Source/product/runtime/provider changes, model routing, dependencies, or
  template-wide redesign unless later Define evidence establishes necessity.
