---
schema_version: 1
artifact_type: specification
artifact_id: wb-skill-002a-post-merge-reconciliation
work_block_id: WB-SKILL-002A
status: draft
created_at: 2026-08-21
revision: define-r1-2026-08-21
owner_approval: Owner approved Define-only investigation and artifact creation on 2026-08-21; this specification grants no source-write, GitHub, or merge authority.
---

# WB-SKILL-002A — Post-Merge Specification and Regression-Guard Reconciliation

## Purpose and Authority

This corrective specification addresses two confirmed post-merge defects in
WB-SKILL-002 while preserving its accepted provider-neutral source outcome.
It is a proposed Define artifact, not authority to modify source, historical
evidence, GitHub state, or the prior specification.

The historical record establishes that the prior separate specification was
created as `draft` and remained so through Execute and closeout. It does not
establish whether an external Owner approval of `define-r2-2026-08-21` occurred
before Execute. Repository-proven facts and possible external historical facts
remain distinct.

## Requirements

- REQ-001: The correction must preserve historical truth. It must not fabricate,
  backdate, or imply an Owner approval that repository evidence cannot establish,
  and must distinguish repository evidence from an external historical fact.
- REQ-002: WB-SKILL-002's separate specification lifecycle metadata must be
  reconciled with the accepted artifact-authority contract. The remediation must
  distinguish historical tracked state, any verified historical approval, a
  historical process deviation when applicable, and any new prospective Owner
  approval. No current approval may be represented as pre-Execute approval
  without independently supported timing.
- REQ-003: The mandatory-provider regression guard must detect prohibited
  semantics across ordinary Markdown line wrapping, while remaining scoped to
  `skills/codex-verification/SKILL.md` and never becoming a repository-wide
  vocabulary scanner.
- REQ-004: Regression coverage must exercise the actual guard predicate with
  single-line forbidden samples, reordered forbidden samples, multiline/wrapped
  forbidden samples, allowed advisory positive controls, and paragraph-separated
  non-matches.
- REQ-005: The framework should prevent successful closeout of a formal
  Managed, Assured, or Distributed Work Block that explicitly uses a separate
  normative specification when that specification remains non-authoritative.
  The exact validator scope must follow the recorded historical-impact analysis
  and must not create false retroactive historical states.
- REQ-006: The accepted provider-neutral behavior of
  `skills/codex-verification/SKILL.md` must remain unchanged unless a new,
  independent source defect is discovered. The expected correction is in
  metadata, lifecycle validation, and the focused test surface, not a redesign
  or reversion of that skill.
- REQ-007: The correction must remain bounded. Gemini recommendations, Spec Kit
  adaptation, converge loops, context pruning, verifier JSON manifests,
  extension/preset/workflow/bundle work, broad legacy-skill cleanup, and
  unrelated governance redesign are out of scope.

## Acceptance Criteria

- AC-001 [req=REQ-001]: The corrective record classifies the repository evidence
  for pre-Execute approval exactly as A, B, or C and explicitly records the
  independent status of any historical external Owner approval.
- AC-002 [req=REQ-001,REQ-002]: No Define or Execute artifact represents an
  unverified historical approval as fact, and any later current approval records
  its prospective timing and scope separately from history.
- AC-003 [req=REQ-002]: The selected P1 remediation branch records the prior
  tracked `draft` state, cites its supporting repository evidence, and retains a
  truthful historical-process-deviation or unresolved-fact record where needed.
- AC-004 [req=REQ-003]: The target-only guard rejects each prohibited semantic
  when its ordinary words are wrapped within one Markdown paragraph, including
  `Provider review is` / `mandatory.`, `Provider` / `review is mandatory.`,
  `Installation is required` / `before verification.`, and `Must install` /
  `Codex.`.
- AC-005 [req=REQ-003,REQ-004]: The guard continues to accept advisory controls
  such as `Provider execution is optional.` and `This skill does not grant
  provider authority.`, and it does not create a match from unrelated words in
  separate paragraphs.
- AC-006 [req=REQ-004]: Contract-suite fixtures prove the same parser/predicate
  that evaluates the target skill for single-line, reordered, multiline, allowed,
  and paragraph-separation cases.
- AC-007 [req=REQ-005]: The future validator design applies only at the
  latest-completed closeout boundary and only when that formal Work Block
  explicitly declares a repository-resolvable separate specification; it does
  not infer profiles or bindings for historical records that omit them.
- AC-008 [req=REQ-005]: The future release-state contract rejects a
  latest-completed eligible Work Block whose declared separate specification has
  `draft`, `review`, `superseded`, `retired`, or another non-authoritative status,
  while accepting `approved` (and existing accepted authority where the artifact
  contract permits it).
- AC-009 [req=REQ-006,REQ-007]: The frozen future implementation subject does
  not modify `skills/codex-verification/SKILL.md` and does not introduce any
  out-of-scope extension, preset, workflow, bundle, converge loop, or broad
  legacy-skill change.

## Verification Boundary

Before source Execute, this Managed Work Block requires a requirements-quality
review, deterministic traceability, consistency analysis, and Critic review.
Any approved implementation then requires independent Reviewer, Verifier, and
Specification Drift assurance on its exact frozen subject. Evaluation is not
required for this deterministic governance/tooling reconciliation.

## Non-Goals

- Reverting or redesigning the provider-neutral WB-SKILL-002 skill correction.
- Deciding an untracked historical Owner fact.
- Treating a current approval as evidence that it happened before Execute.
- Applying a global historical specification-status migration without an
  explicit, evidence-supported follow-up decision.
