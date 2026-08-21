---
schema_version: 1
artifact_type: specification
artifact_id: wb-skill-002-provider-neutral-verifier
work_block_id: WB-SKILL-002
status: approved
created_at: 2026-08-21
revised_at: 2026-08-21
revision: reconciliation-r1-2026-08-21
owner_approval: Owner prospectively approved this current specification on 2026-08-21. This approval takes effect only on that date; it does not establish pre-Execute approval, cure, or rewrite the historical WB-SKILL-002 process deviation. This specification grants no source-write, GitHub, or merge authority.
---

# WB-SKILL-002 — Provider-Neutral Verifier Legacy Skill Correction

## Purpose and Authority

## Lifecycle Reconciliation Record

WB-SKILL-002 Execute and closeout were historically recorded while this
specification had `status: draft`. Repository evidence does not establish an
Owner approval of revision `define-r2-2026-08-21` before that Execute; the
historical external approval fact remains `UNVERIFIED`. The Owner's current
approval on 2026-08-21 is prospective only. It makes this current revision
authoritative from that date and does not retroactively represent the historical
process as compliant.

This specification corrects one dogfooding-discovered legacy skill:
`skills/codex-verification/SKILL.md`. The current skill is installed in the
Codex profile and catalogued for review/verification, yet assigns a
provider-specific second model mandatory lifecycle triggers, legacy `Control
Tower`/`Stage 0.5` topology, and a Claude-versus-Codex authority model. That
contradicts the accepted runtime-neutral role model and the Portable Kit's
normative disposition for `codex-verification`.

The specification is the behavioral authority for this Work Block. It neither
opens a source Write Gate nor grants runtime, GitHub, provider, credential,
commit, push, pull-request, merge, or deployment authority.

## Requirements

- REQ-001: `codex-verification` must be a runtime-specific, optional advisory
  procedure rather than a Verifier role, lifecycle gate, or competing authority
  mechanism. Role authority remains with accepted governance and the routed
  Reviewer/Verifier contracts.
- REQ-002: The corrected procedure must not require a provider/model-specific
  review for a verification tier, domain, failure verdict, or lifecycle stage.
  A Work Block may request optional additional read-only evidence only when its
  approved assurance plan and available runtime capability justify it.
- REQ-003: The corrected procedure must not use `Control Tower`, `Stage 0.5`,
  `gpt-critic`, `gpt-verifier`, or Claude-versus-Codex authority/topology
  semantics. It must use the accepted Define → Execute → Assure → Close
  vocabulary where it describes lifecycle placement.
- REQ-004: The procedure must state that provider output is scoped evidence,
  cannot claim independence merely from a model/provider label, does not issue
  a project verdict, and reports unavailable execution honestly without
  weakening required Reviewer or Verifier assurance.
- REQ-005: The correction must retain only truthful, current runtime-adapter
  references. It must not instruct installation, authentication, MCP setup, or
  a transport command as a universal repository prerequisite.
- REQ-006: The correction must add deterministic regression protection in
  `scripts/test-sdd-contract.sh`, scoped only to
  `skills/codex-verification/SKILL.md`. It must require the corrected skill to
  defer authority to governing contracts and the active Work Block, state that
  additional provider execution is optional scoped evidence, and report an
  unavailable optional execution as an inspection gap. It must reject the
  legacy `Control Tower`, `Stage 0.5`, `gpt-critic`, and `gpt-verifier` terms
  and mandatory provider-review/prerequisite semantics in that target file
  only. It must not impose a repository-wide ban on historical provider
  wording.
- REQ-007: This Work Block is bounded to the one legacy skill and its focused
  contract test. It must not change role skills already converged by
  WB-SKILL-001, installation profiles/presets, workflow/bundle/extension
  design, candidates, runtime adapters other than this skill, or the Portable
  Kit promotion sequence.

## Acceptance Criteria

- AC-001 [req=REQ-001]: `skills/codex-verification/SKILL.md` explicitly defers
  authority, lifecycle, scope, and assurance selection to governing contracts
  and the active Work Block, and never represents itself as a Verifier role.
- AC-002 [req=REQ-002]: The procedure contains no mandatory provider-review
  trigger tied to Full tier, a domain, an adverse verdict, or a lifecycle stage.
- AC-003 [req=REQ-003]: The procedure contains no operational `Control Tower`,
  `Stage 0.5`, `gpt-critic`, or `gpt-verifier` semantics and uses only the
  accepted lifecycle vocabulary where needed.
- AC-004 [req=REQ-004]: The output boundary distinguishes scoped advisory
  evidence from project readiness and records unavailable optional execution as
  an inspection gap without altering required assurance verdicts.
- AC-005 [req=REQ-005]: No global installation/authentication/configuration or
  provider transport command is presented as a prerequisite; actual capability
  is discovered at execution time under the Work Block's authority.
- AC-006 [req=REQ-006]: `scripts/test-sdd-contract.sh` deterministically
  checks only `skills/codex-verification/SKILL.md` for all required and
  forbidden REQ-006 invariants; historical evidence and unrelated legacy
  surfaces remain outside its search scope.
- AC-007 [req=REQ-007]: The frozen Execute source subject, measured from the
  exact pre-Execute base through the exact post-Execute commit, changes exactly
  `skills/codex-verification/SKILL.md` and `scripts/test-sdd-contract.sh`.
  Later approved Define, Assure, or Close evidence synchronization is outside
  that source-subject manifest and must not alter either assured source blob.
  No phase alters catalogs, profiles/presets, workflows, bundles, candidate
  content, or the already-converged role skills.

## Verification Boundary

Before any Execute transition, an independent requirements-quality review,
traceability validation, consistency analysis, and Critic review are required.
The eventual frozen implementation subject requires independent Reviewer,
Verifier, and Specification Drift evidence. Evaluation is not required unless
the approved source design introduces non-deterministic behavior.

## Non-Goals

- Creating, promoting, installing, or configuring an external-review extension.
- Changing `skills/catalog.yml`, `bootstrap/profiles.json`, a preset, a bundle,
  a workflow, or any direct runtime adapter outside the named skill.
- General modernization of other legacy `Control Tower` historical surfaces.
- Changing the portable-kit specification, role contracts, source authority, or
  GitHub state.
