---
schema_version: 1
artifact_type: requirements_quality_review
work_block_id: WB-SKILL-002
specification: docs/specs/wb-skill-002-provider-neutral-verifier.md
specification_revision: draft-2026-08-21
reviewer_role: reviewer / requirements-quality specialization
isolation: separate delegated Reviewer context in the same isolated clone; independent from the authoring context, but not OS-isolated
verdict: CHANGES_REQUIRED
---

# Requirements Quality Review — WB-SKILL-002 Provider-Neutral Verifier Legacy Skill Correction

## Subject

- Specification: `docs/specs/wb-skill-002-provider-neutral-verifier.md`
- Revision: `draft-2026-08-21`
- Work Block: `WB-SKILL-002`
- Reviewed baseline: `0029baff70e11ca911a3c4c165c21b5a228e7358`
- Review boundary: written requirements, Work Block, task decomposition, and
  governing Define/lifecycle authority only; source implementation behavior is
  out of scope.

## Result Matrix

| Dimension | Status | Evidence / references | Finding |
|---|---|---|---|
| Scope and exclusions | CHANGES_REQUIRED | REQ-007; AC-007; Work Block lines 59-67; TASK-003 | RQ-002 |
| Actors / permissions / ownership | CHANGES_REQUIRED | Work Block `governance_profile: Managed`; lifecycle state; `governance/define-quality.md` “Executable Define-Quality Prerequisite” | RQ-003 |
| Requirement completeness | CHANGES_REQUIRED | REQ-006; AC-006; TASK-002 | RQ-001 |
| Clarity / ambiguity | CHANGES_REQUIRED | REQ-006 / AC-006; AC-007 | RQ-001, RQ-002 |
| Internal consistency | CHANGES_REQUIRED | AC-006 / AC-007; Work Block source write-set and Define write-set; TASK-002 / TASK-003 | RQ-001, RQ-002, RQ-003 |
| Acceptance measurability | CHANGES_REQUIRED | AC-006, AC-007 | RQ-001, RQ-002 |
| Alternate / failure / recovery coverage | READY | REQ-002, REQ-004, REQ-005; Work Block Hard Stops and required assurance sequence | Optional additional evidence and unavailable execution are bounded without weakening required assurance. |
| Security / privacy / operational coverage | READY | REQ-004, REQ-005, REQ-007; Work Block Hard Stops | No new credential, installation, transport, deployment, or provider authority is introduced; those actions remain prohibited. |
| Assumptions / dependencies | CHANGES_REQUIRED | Managed profile; required Define-quality sequence; REQ-006 / TASK-002 conditional test wording | RQ-001, RQ-003 |
| Requirement / acceptance traceability | CHANGES_REQUIRED | REQ-001..REQ-007; AC-001..AC-007; TASK-001..TASK-003; validator result | IDs are structurally complete, but RQ-001 and RQ-002 leave the behavior and subject that TASK-002/TASK-003 must deliver under-specified. |

## Findings

### RQ-001 — Regression-protection invariant is not specified deterministically

- Severity: `material`
- Requirement/section: REQ-006 and AC-006, specification lines 47-49 and
  72-74; TASK-002, tasklist line 15.
- Quality dimension: requirement completeness; clarity / ambiguity; acceptance
  measurability.
- Finding: The specification requires the “smallest sufficient deterministic
  regression protection” and says that the existing test must check “new
  current-skill invariants,” but it never identifies those invariant assertions
  or the target-bound search boundary. It also makes the only named test path
  conditional (“if needed”) while REQ-006 uses mandatory language (“must add”).
- Why it matters: A Coder would have to invent whether the test protects the
  absence of mandatory provider triggers, the retired topology terms, universal
  provider prerequisites, the advisory-output boundary, or some subset. Review
  and verification could then accept materially different regressions while
  each claims to satisfy AC-006.
- Owning remediation: `specification`
- Smallest sufficient correction: state the fixed, target-file-only invariant
  classes that the focused test must demonstrate, and resolve whether updating
  `scripts/test-sdd-contract.sh` is mandatory or whether a named pre-existing
  check demonstrably supplies each class. Preserve the explicit exclusion of
  historical evidence and unrelated legacy surfaces.

### RQ-002 — “Implementation diff” has no unambiguous subject for the exact-path rule

- Severity: `material`
- Requirement/section: AC-007, specification lines 75-78; Work Block lines
  59-80; TASK-003, tasklist line 16.
- Quality dimension: scope and exclusions; clarity / ambiguity; internal
  consistency; acceptance measurability.
- Finding: AC-007 says that “the implementation diff changes exactly” the two
  source paths, while the Work Block separately authorizes Define and assurance
  documentation paths and TASK-003 itself owns plan/tasklist paths. The
  specification does not say whether the criterion applies to the frozen
  Execute source subject, a later evidence-sync subject, or the full Work Block
  branch/PR diff.
- Why it matters: Applied to the branch or PR literally, the criterion would
  reject required evidence and coordination updates. Applied too loosely, it
  would not prevent an unapproved source path from entering the frozen subject.
  The Coder, Reviewer, and Verifier need one shared comparison boundary.
- Owning remediation: `specification`
- Smallest sufficient correction: define AC-007 against the frozen Execute
  source subject/path manifest (one required skill path plus the named test path
  only when its specified invariant change requires it), and explicitly exclude
  approved Define/Assure/closeout evidence synchronization from that source
  manifest.

### RQ-003 — Managed Define-quality prerequisite lacks its required aggregate binding

- Severity: `material`
- Requirement/section: Work Block front matter and lifecycle state, plan lines
  1-17 and 43-55; `governance/define-quality.md`, “Executable Define-Quality
  Prerequisite,” especially the Managed applicability and readiness binding.
- Quality dimension: actors / permissions / ownership; internal consistency;
  assumptions / dependencies.
- Finding: The Work Block declares `governance_profile: Managed` and correctly
  lists the three Define functions, but it does not record the required
  `define_quality` aggregate with `required`, `status`, `requirements_review`,
  `traceability`, and `consistency_analysis` bindings. The governing contract
  says that a missing aggregate for Managed work is unresolved and fail-closed.
- Why it matters: The current `write_gate: BLOCKED` prevents an immediate source
  change, but there is no authoritative, inspectable binding to update before a
  future Critic/write-gate decision. That leaves the mandatory Define evidence
  easy to treat as prose rather than a source-transition prerequisite.
- Owning remediation: `plan`
- Smallest sufficient correction: add the canonical pending aggregate to the
  active Work Block, with `required: true` for its Managed profile and blank
  evidence bindings; later bind this review, traceability evidence, and the
  consistency report before any READY source-gate decision.

## Remaining Owner Decisions

- None. Each finding is resolvable from the accepted Define-quality and
  lifecycle contracts without changing the approved objective or broadening the
  Work Block.

## Inspection Gaps

- Source implementation and the current test implementation were intentionally
  not inspected: this is a requirements-quality review before Execute, not a
  code review or verification pass.
- Isolation is a separate delegated Reviewer context in the same isolated clone;
  it is independent from the authoring context but is not an OS-isolated or
  separate-runtime assurance claim.

## Verdict

`CHANGES_REQUIRED`

The specification/plan must resolve RQ-001 through RQ-003 before this
requirements-quality review can become `READY` and before Critic/Execute.
This is Define-stage evidence only. It does not grant source-write authority,
change the Critic state, open the Write Gate, approve a commit/push/PR/merge, or
modify an external capability.
