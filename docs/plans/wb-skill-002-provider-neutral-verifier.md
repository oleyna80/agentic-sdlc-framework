---
schema_version: 1
artifact_type: work_block
artifact_id: wb-skill-002-provider-neutral-verifier
work_block_id: WB-SKILL-002
status: in_progress
owner_role: Owner
created_at: 2026-08-21
last_updated: 2026-08-21
governance_profile: Managed
branch: agent/wb-skill-002-provider-neutral-verifier
base_revision: 0029baff70e11ca911a3c4c165c21b5a228e7358
write_gate: READY
critic_gate: READY
review_gate: READY
verification_verdict: READY
drift_gate: ALIGNED
---

# WB-SKILL-002 — Provider-Neutral Verifier Legacy Skill Correction

## Objective

Correct the one currently installed and catalogued `codex-verification` legacy
procedure so it is a bounded optional runtime-adapter procedure, not a
provider-specific Reviewer/Verifier authority or a parallel lifecycle gate.

## Evidence Basis

Dogfooding on current `main` at
`0029baff70e11ca911a3c4c165c21b5a228e7358` found that the active Codex profile
still includes `codex-verification`, while its skill text requires provider
review for selected tiers/domains/outcomes and uses `Control Tower`, Stage 0.5,
`gpt-critic`, and `gpt-verifier`. The accepted Portable Kit specification,
section 12, instead gives `codex-verification` the disposition: provider-neutral
Verifier contract plus `verification-before-completion`; no provider name may
survive as portable authority and second-model use is optional execution
metadata.

This is a current operational contradiction, not an instruction to converge all
historical legacy surfaces or implement an extension/preset/workflow/bundle.

## Lifecycle State

- **Current Stage:** Assure
- **Stage State:** in_progress
- **Write Gate:** READY — Owner approved the exact two-path Execute write-set
  on 2026-08-21 after Define-quality readiness and fresh Critic `APPROVE`.
- **Critic Gate:** READY — fresh independent Critic re-review `APPROVE` for
  `define-r2-2026-08-21`; it grants no source authority.
- **Review Gate:** READY — fresh independent Reviewer re-review is `READY` for
  exact frozen source subject
  `af0c1615f7186b42939cd35435b630a91a6c14fc` →
  `b3148bc559d2d32f4a5d56bfc1fbe0250b948bc1`; historical
  `CHANGES_REQUIRED` reports remain retained.
- **Verification Verdict:** READY — fresh independent Technical Verification
  in a detached local temporary clone passed for exact frozen source subject
  `af0c1615f7186b42939cd35435b630a91a6c14fc` →
  `b3148bc559d2d32f4a5d56bfc1fbe0250b948bc1`.
- **Evaluation Verdict:** NOT_REQUIRED — deterministic procedure and contract
  consistency only; reconsider if Execute expands the behavior.
- **Drift Gate:** ALIGNED — independent Specification Drift Audit found the
  exact frozen source subject aligned; its verdict is limited to
  `af0c1615f7186b42939cd35435b630a91a6c14fc` →
  `b3148bc559d2d32f4a5d56bfc1fbe0250b948bc1`.
- **Closeout Mode:** pending

## Approved Define Scope

### Eventual Coder source write-set — exactly two paths

```text
skills/codex-verification/SKILL.md
scripts/test-sdd-contract.sh
```

This exact source manifest applies only to the frozen Execute subject, from its
recorded pre-Execute base through its post-Execute commit. Later approved
Define, Assure, and Close evidence synchronization is outside that source
manifest and must preserve both assured source blobs.

### Current Define write-set

```text
docs/specs/wb-skill-002-provider-neutral-verifier.md
docs/plans/wb-skill-002-provider-neutral-verifier.md
docs/tasklist/wb-skill-002-provider-neutral-verifier.md
FILE_REGISTRY.yml
PROJECT_MAP.md
docs/reports/requirements/wb-skill-002-provider-neutral-verifier.md
docs/reports/requirements/wb-skill-002-provider-neutral-verifier-rereview.md
docs/reports/requirements/wb-skill-002-provider-neutral-verifier-consistency.md
docs/reports/requirements/wb-skill-002-provider-neutral-verifier-consistency-rereview.md
docs/reports/reviews/wb-skill-002-provider-neutral-verifier-critic.md
docs/reports/reviews/wb-skill-002-provider-neutral-verifier-critic-rereview.md
docs/reports/reviews/wb-skill-002-provider-neutral-verifier.md
docs/reports/reviews/wb-skill-002-provider-neutral-verifier-rereview.md
docs/reports/reviews/wb-skill-002-provider-neutral-verifier-rereview-2.md
```

## Requirements and Task Binding

- **Specification:** `docs/specs/wb-skill-002-provider-neutral-verifier.md`
- **Tasklist:** `docs/tasklist/wb-skill-002-provider-neutral-verifier.md`
- **Traceability status:** `READY` for `define-r2-2026-08-21`
  (`requirements=7 acceptance=7 tasks=8`).
- **Requirements-quality review:** historical initial review is
  `CHANGES_REQUIRED`; fresh independent re-review is `READY` for
  `define-r2-2026-08-21`.
- **Consistency analysis:** historical initial analysis is `CHANGES_REQUIRED`;
  fresh independent re-analysis is `READY` for `define-r2-2026-08-21` after
  its owning projection fix.

## Define Quality Prerequisite

```json
"define_quality": {
  "required": true,
  "status": "READY",
  "requirements_review": "docs/reports/requirements/wb-skill-002-provider-neutral-verifier-rereview.md (READY, define-r2-2026-08-21)",
  "traceability": "python3 scripts/validate-define-traceability.py: READY (requirements=7 acceptance=7 tasks=8)",
  "consistency_analysis": "docs/reports/requirements/wb-skill-002-provider-neutral-verifier-consistency-rereview.md (READY, define-r2-2026-08-21)"
}
```

This Managed Work Block cannot open its source Write Gate until the aggregate
is `READY` and each evidence binding is non-blank. The historical
`CHANGES_REQUIRED` report is retained as evidence; only a fresh independent
`READY` re-review may fill `requirements_review`.

## Provenance

- **Classification:** `original_experience_derived`
- **Internal evidence:** direct dogfooding of the current installed legacy skill
  against accepted role/lifecycle contracts and Portable Kit mechanism
  disposition.
- **Local delta:** remove obsolete provider-authority/lifecycle semantics while
  preserving a bounded optional runtime-adapter procedure.
- **Rationale:** no external mechanism is being adopted; the corrective boundary
  arises from the framework's own operating contradiction.
- **Novelty claim:** none.

## Hard Stops

- No source modification before formal Define readiness and a Critic-approved
  Write Gate.
- No change to `skills/catalog.yml`, `bootstrap/profiles.json`, installation
  profiles/presets, extensions, workflows, bundles, candidate content, or
  Portable Kit promotion without a separate Owner-approved Work Block.
- No provider installation, authentication, MCP configuration, runtime command,
  credential action, commit, push, pull request, merge, deployment, or
  destructive operation under this Work Block's Define authorization.
- Preserve unrelated working-tree state in every checkout.

## Required Assurance Sequence

1. independent requirements-quality review;
2. traceability validation and independent consistency analysis;
3. separate read-only Critic review before a source Write Gate decision;
4. one bounded Coder if the gate becomes READY;
5. independent Reviewer and Verifier on the frozen source subject;
6. Specification Drift re-audit;
7. evidence-only closeout only after final normative state is assured.

## Explicitly Out of Scope

- WB-SKILL-001's completed role-skill paths and all other legacy skills;
- `skills/catalog.yml` and `bootstrap/profiles.json`;
- extensions, presets, workflows, bundles, candidate content, installation,
  promotion, and the future WB-CORE sequence;
- specifications/architecture decisions unrelated to the bounded correction;
- GitHub state and protected/default-branch actions.
