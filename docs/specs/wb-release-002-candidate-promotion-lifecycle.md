---
schema_version: 1
artifact_type: specification
artifact_id: wb-release-002-candidate-promotion-lifecycle
work_block_id: WB-RELEASE-002
status: draft
created_at: 2026-08-25
revision: define-r1-2026-08-25
owner_approval: Owner authorized Define-only investigation of this revision on 2026-08-25. No source-write, commit, push, PR, merge, or canonical-projection authority is granted.
---

# WB-RELEASE-002 — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Purpose and authority boundary

This draft specification investigates the missing lifecycle transition exposed by the WB-CORE-003G pilot after WB-RELEASE-001 introduced a single evidence-bound `pre_closeout_candidate`. It is not approved for Execute and is not authority to modify release-state policy, validators, registry, map, or historical Work Blocks.

The specification must preserve the distinction between raw completed history and effective completion derived from immutable candidate evidence. A later approved revision may define a promotion record or another canonical representation, but may not fabricate evidence or backdate Owner approval.

## Requirements

- REQ-001: The lifecycle record must distinguish repository-proven raw completed state, evidence-derived effective completion, active candidate state, and any future promoted-candidate history. Missing or contradictory historical metadata must be reported as unverified rather than inferred.
- REQ-002: Before a next candidate is declared, the prior evidence-complete candidate must be promoted through an explicit, deterministic transition that preserves its exact Work Block, evidence bindings, normative manifest, and effective-completion meaning.
- REQ-003: The state model must allow exactly one active `pre_closeout_candidate` and must bind every candidate to one deterministic predecessor under the selected raw/effective history model.
- REQ-004: Promotion must require the existing four evidence classes with the required verdicts, exact candidate binding, and unchanged normative manifest; incomplete or stale evidence must not authorize promotion.
- REQ-005: Ordinary release-state validation must remain fail-closed for duplicate candidates, candidate/active coexistence, malformed projections, missing evidence, stale manifests, invalid predecessors, and ambiguous promotion history.
- REQ-006: Promotion must retain immutable prior evidence and must not rewrite a raw historical Work Block from candidate-derived completion into a fact that was not recorded by the original lifecycle.
- REQ-007: The invariant is prospective and transition-scoped. It must not force legacy records with absent profile/specification metadata into false compliance and must not register or mutate the WB-CORE-003G pilot from this Work Block.
- REQ-008: The implementation design must assign each future source path to its owning contract and use the smallest sufficient change; this Define run authorizes no source path.
- REQ-009: The future contract suite must exercise successful sequential promotion and adversarial cases for incomplete, duplicate, stale, reordered, and next-candidate state.

## Acceptance criteria

- AC-001 [req=REQ-001]: The approved design includes a table of current completed/candidate records and explicitly labels missing profile/specification facts as `UNVERIFIED`.
- AC-002 [req=REQ-002]: Given an evidence-complete WB-RELEASE-001 candidate, the design defines a transition that preserves its effective completion before a next candidate can be declared.
- AC-003 [req=REQ-003]: The design defines exactly-one-candidate and predecessor rules for both the current candidate and its successor.
- AC-004 [req=REQ-004]: A promotion attempt without all required exact-bound evidence or with a changed normative manifest is rejected deterministically.
- AC-005 [req=REQ-005]: Existing fail-closed ordinary-mode behavior is retained for incomplete, duplicate, malformed, concurrent, or stale state; candidate mode cannot emit `READY`.
- AC-006 [req=REQ-006]: The promoted record retains the prior candidate's immutable evidence references and does not alter the original Work Block's historical status or timing claims.
- AC-007 [req=REQ-007]: No future validator rule is scoped as a retroactive global migration; the design explicitly excludes WB-CORE-003G and unrelated historical corrections.
- AC-008 [req=REQ-008]: The approved implementation plan names the owning contract, smallest change, and rationale for every proposed source path, with the write-set remaining unauthorized until a later Owner decision.
- AC-009 [req=REQ-009]: The future fixture plan covers a successful promotion, incomplete evidence, stale manifest, duplicate candidate, invalid predecessor, and valid next-candidate transition.

## Historical impact and scope decision

The repository-wide inventory finds bounded impact: WB-RELEASE-001 is the only active evidence-complete candidate requiring promotion semantics. WB-SKILL-002, WB-SKILL-002A, WB-SKILL-002B, and WB-SKILL-001 have explicit approved specifications and raw completed records; no new transition failure is inferred for them. Nineteen older completed records lack structured profile/specification metadata and remain unverified. WB-CORE-003G is not part of the current baseline.

The recommended scope is prospective serial transition (option d: a separate promotion contract), not a latest-only retroactive validator sweep and not a rewrite of all completed records. The approved design must compare a durable effective-completion ledger with direct promotion into `completed_work_blocks`, explaining why the selected representation preserves raw history and current validator safety.

## Future implementation candidates (not authorized)

- `governance/release-state.md` — normative serial-promotion and effective-history semantics are absent from the current contract.
- `scripts/validate-release-state.py` — deterministic enforcement of promotion prerequisites, one-candidate serialization, predecessor continuity, and history binding.
- `scripts/test-release-state-contracts.py` — regression fixtures for successful and adversarial transitions.
- `FILE_REGISTRY.yml` — only if the selected canonical history representation requires a new machine-state field; not a pre-authorized path.
- `PROJECT_MAP.md` — only if the machine-state shape changes and its human projection must be synchronized; not a pre-authorized path.
- `.agent/workflows/sdd-protocol.md` — only if the final design requires a lifecycle procedure beyond release-state policy; not a pre-authorized path.

No source implementation, governance edit, registry/map edit, or fixture change occurs while this specification is `draft`.

## Verification boundary

Define quality, consistency analysis, and Critic are required before any future Execute decision. Independent Reviewer, fresh-clone Verifier, and Drift assurance apply to the later frozen implementation subject. Evaluation is not required because the target is deterministic governance/tooling lifecycle behavior with no non-deterministic product behavior.

## Non-goals

- Do not change WB-RELEASE-001 or its historical evidence in this Define run.
- Do not repair WB-CORE-003G from this branch.
- Do not alter existing candidate validation to make an invalid intermediate state pass.
- Do not infer external Owner approval, historical profile, or historical specification authority.
- Do not address Gemini recommendations, converge loops, context pruning, extensions, presets, workflows, bundles, or unrelated legacy cleanup.

