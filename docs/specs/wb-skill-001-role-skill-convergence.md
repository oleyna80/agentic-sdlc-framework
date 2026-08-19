---
schema_version: 1
artifact_type: specification
artifact_id: wb-skill-001-role-skill-convergence
status: approved
created_at: 2026-08-18
updated_at: 2026-08-19
owner_approval: Owner confirmed continuation and the exact source write-set in this session on 2026-08-19; governing contracts remain higher authority.
---

# WB-SKILL-001 — Framework-Native Role Skill Convergence Specification

## Purpose and Authority

This specification defines the required behavior for the WB-SKILL-001
corrective implementation. The approved revision of this specification is the
behavioral authority for the Work Block. The Work Block records bounded
execution scope, planning, write-set, lifecycle state, evidence routing, and
authority already granted by higher-authority contracts; it cannot override or
silently redefine the approved specification. If execution planning conflicts
with the approved specification, return to Define and correct the derivative
Work Block or revise the owning specification according to the authority chain.
This document neither opens a source Write Gate nor grants a role, runtime, or
Git capability.

The subject is the current critical role-skill execution path identified in the
accepted inventory. Historical evidence is preserved and is not a correction
target under this specification.

## Requirements

- REQ-001: Reusable operational role skills must be subordinate to `AGENTS.md`,
  `governance/authority.md`, `governance/lifecycle.md`,
  `governance/artifacts.md`, the runtime-neutral SDD protocol, and the active
  Work Block/write-set; a skill supplies procedure and creates no competing
  authority model.
- REQ-002: Current operational role skills must use
  Define → Execute → Assure → Close for framework lifecycle semantics and must
  not introduce Stage 0.5, a Control Tower lifecycle, or another parallel state
  machine; historical evidence is excluded.
- REQ-003: The Critic must remain read-only except an expressly approved report
  artifact, challenge applicable Define evidence and delivery design, use
  `APPROVE | SUPPLEMENT | RECONSIDER`, distinguish that functional verdict from
  operational Critic gate state, return RECONSIDER work to Define, and create no
  independent source-write authority.
- REQ-004: The Coder must stay inside the approved write-set, preserve unrelated
  working-tree state, report unresolved obstacles, and respect Hard Stops while
  allowing authorized ordinary reversible edits, tests, staging, local commits,
  normal feature-branch pushes, and PR updates when the Work Block and runtime
  credential permit them.
- REQ-005: The implementation Reviewer must be read-only except expressly
  approved review evidence, review a frozen subject and relevant evidence,
  report inspection gaps, and use exactly
  `READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED`; its findings cannot all be
  described as merely advisory.
- REQ-006: The Verifier must be read-only except expressly approved verification
  evidence, verify acceptance criteria/contracts reproducibly, report
  blocked/not-run checks honestly, use `READY | BLOCKED | UNVERIFIED`, and not
  claim exclusive framework authority to stop progression.
- REQ-007: Critical reusable role skills must not present unrelated consumer
  topology, paths, languages, routes, form/API/email flows, or Next.js/VPS/
  Docker assumptions as universal framework requirements; clearly labelled,
  non-authoritative specializations remain permissible.
- REQ-008: A direct Claude or Codex adapter that routes or restates a corrected
  role procedure must not retain a live semantic contradiction with the corrected
  shared skill or accepted runtime-neutral governance; cosmetic-only adapter
  edits are excluded.
- REQ-009: Current operational role skills must not rely on nonexistent AGENTS
  section names, helper scripts, runtime paths, or skill IDs; mechanically
  checkable retained references must be validated where practical.
- REQ-010: Each reusable skill materially revised by this Work Block must carry
  accurate decision provenance under `governance/decision-provenance.md`; an
  unavailable source is recorded as unresolved, not invented, and historical
  provenance absence alone requires no backfill.
- REQ-011: The correction must use the smallest sufficient deterministic
  regression protection in an existing appropriate contract test when practical,
  limited to current critical operational role-skill invariants and excluding a
  repository-wide ban on historical wording.
- REQ-012: WB-SKILL-001 must remain bounded to the current critical role-skill
  execution path; inventory bucket C, canonical aggregate SHA hardening, and
  Spec Kit behavior remain outside the corrective implementation unless a new
  approved Work Block changes that boundary.

## Acceptance Criteria

- AC-001 [req=REQ-001]: Every corrected critical role procedure explicitly
  defers authority, scope, and write permission to the governing contracts and
  active Work Block/write-set, with no conflicting authority owner.
- AC-002 [req=REQ-002]: The corrected critical role procedures contain no
  authority-bearing `Control Tower` or `Stage 0.5` lifecycle semantics and use
  the current lifecycle vocabulary where lifecycle state is stated.
- AC-003 [req=REQ-003]: The corrected Critic procedure is read-only and exposes
  exactly the functional verdict vocabulary `APPROVE | SUPPLEMENT | RECONSIDER`.
- AC-004 [req=REQ-003]: The Critic procedure states that RECONSIDER returns work
  to Define/keeps source progression blocked and does not collapse functional
  verdict into operational Critic gate state.
- AC-005 [req=REQ-004]: The corrected Coder procedure binds changes to an
  approved write-set, preserves unrelated state, reports blockers, and retains
  current Hard Stop boundaries.
- AC-006 [req=REQ-004]: The corrected Coder procedure does not impose a blanket
  prohibition on normal in-scope local commits or feature-branch pushes when
  current governance and runtime permission allow them.
- AC-007 [req=REQ-005]: The corrected Reviewer procedure is read-only, binds to
  a frozen subject, reports inspection gaps, and advertises exactly
  `READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED`.
- AC-008 [req=REQ-006]: The corrected Verifier procedure is read-only, binds
  verdicts to reproducible evidence, advertises exactly
  `READY | BLOCKED | UNVERIFIED`, and makes no exclusive-blocker claim.
- AC-009 [req=REQ-007]: Generic critical role procedures contain none of the
  inventory's universalized `web/*`, `05_ai/*`, fr/ru, route, form/API/email,
  Next.js, VPS, or Docker requirements.
- AC-010 [req=REQ-008]: Each changed direct role adapter has a recorded
  critical-path contradiction and, after correction, agrees with the applicable
  shared role procedure and governing contract without unrelated cleanup.
- AC-011 [req=REQ-009]: Retained critical-path AGENTS references, helper paths,
  runtime paths, and skill IDs resolve to current existing targets, or are
  removed when no current target exists.
- AC-012 [req=REQ-010]: Every materially revised reusable shared role skill has
  a concise provenance statement with primary classification, source or
  unresolved status, local delta, and no unsupported novelty claim.
- AC-013 [req=REQ-011]: An existing contract test deterministically checks only
  the agreed critical-role lifecycle, authority, verdict, Git, and retained-path
  invariants, while historical reports remain outside its search scope.
- AC-014 [req=REQ-012]: The final implementation diff excludes inventory bucket
  C/D surfaces, canonical aggregate logic, and Spec Kit mechanisms unless a
  separately approved change explicitly authorizes them.

## Verification Boundary

The eventual verification binds the frozen implementation subject to these
criteria with the existing governance, SDD-contract, release-state, and focused
contract checks selected proportionally to the final approved write-set.
Evaluation is not required because the intended behavior is deterministic
procedure/documentation and contract-test consistency.
