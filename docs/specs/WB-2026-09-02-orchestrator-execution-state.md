---
schema_version: 1
artifact_type: specification
artifact_id: wb-2026-09-02-orchestrator-execution-state
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: define_candidate
owner_role: repository_owner
created_at: 2026-09-02
base_revision: be988807c38543eb90a728fcb4349bc97dd5695a
---

# Specification — Orchestrator Execution State / Stateful Work Block Runtime

## Objective

Make long-running Work Blocks recoverable and operable from compact, validated current state rather than accumulated conversation/tool history, without weakening lifecycle authority, assurance provenance, or Engineering Memory boundaries.

## Accepted Architecture Direction

1. `.agent/active-work-block.json` remains the single live canonical Work Block state for one execution root. No second live state SSOT is introduced.
2. The state contract advances to **schema version 4** because required execution-state semantics become normative. Existing schema-v3 readers must fail closed rather than silently ignore required v4 fields.
3. The tracked `.agent/active-work-block.default.json` remains a safe blocked bootstrap source, not a persisted active Work Block.
4. Cross-runtime/cross-machine transfer uses an immutable **handoff snapshot** bound to exact repository/state versions. A snapshot is evidence/input to deterministic import; it is not a second live authority.
5. Evidence and Engineering Memory remain separate planes. Active state contains only bounded evidence pointers needed for current execution.
6. Model/runtime workers propose bounded changes; a provider-neutral deterministic reducer owns validation, derived invalidation, atomic write, and conflict rejection.

## State Model

Schema v4 preserves existing authority/gate fields and adds only operational state that is not already represented canonically:

```text
schema_version: 4
state_version: monotonic integer
existing authority/gate fields: authority_mode, work_block_id, governance_profile,
  specification, base_commit, define_quality, write_gate, critic, assurance,
  closeout_mode, integrations, write_set, coordination_write_set, external_hard_stops
lifecycle:
  stage
  execution_state
subject:
  current_revision
  frozen_revision
  generation
progress:
  active_tasks[]
  blockers[]
  pending_decisions[]
  next_action
context:
  latest_observation_ref
  current_evidence_refs[]
  handoff_snapshot_ref
```

`base_commit` remains the planning baseline to avoid duplicating an already canonical field. Full task history remains in the traceable tasklist; full evidence history remains in reports/log artifacts.

## Patch Classes

Generic state patches MUST distinguish:

- **authority-protected fields** — cannot be expanded by a generic model patch; require existing lifecycle/Owner/integration procedures;
- **runtime-mutable fields** — may be updated through an allowlisted patch when `expected_state_version` matches;
- **derived fields** — computed by the reducer and never accepted directly from a model patch.

At minimum, `write_set`, `coordination_write_set`, `external_hard_stops`, `integrations`, `governance_profile`, `authority_mode`, and source-write readiness are authority-protected.

## Requirements

- REQ-001: The framework MUST retain exactly one live canonical Work Block state per execution root at `.agent/active-work-block.json`; no parallel live Execution State SSOT may be introduced.
- REQ-002: Schema v4 MUST include a monotonic `state_version`, and every generic mutable-state transition MUST require an exact `expected_state_version` compare-and-swap precondition.
- REQ-003: A provider-neutral deterministic reducer MUST validate patch shape, allowed paths, values, state version, lifecycle invariants, and authority boundaries before atomically replacing canonical state; rejection MUST preserve the previous valid state byte-for-semantics.
- REQ-004: Authoritative observations that change the current or frozen assurance subject MUST deterministically invalidate or stale assurance bound to the prior subject and advance subject generation without relying on an LLM to remember each dependent field.
- REQ-005: Active state MUST store only bounded current evidence pointers; durable provenance MUST remain in existing report/log/evidence artifacts and MUST be retrievable without replaying full chat/tool history.
- REQ-006: Default Orchestrator context assembly MUST be defined as immutable procedure + canonical current state + latest relevant observation + selectively retrieved evidence, and MUST NOT require full conversation replay for routine next-step decisions.
- REQ-007: The framework MUST support deterministic export/import of a non-authoritative handoff snapshot sufficient to initialize an execution root on another session/runtime when the snapshot is bound to exact Work Block ID, state version/digest, branch/repository revision, and passes current-state/repository reconciliation.
- REQ-008: Concurrent/overlapping state mutation MUST fail deterministically through state-version compare-and-swap and shared-state serialization; a worker MUST NOT silently overwrite another worker's accepted transition.
- REQ-009: Generic state patches MUST NOT create or expand write authority, integration admission, Hard Stop capability, governance profile, Owner approval, or assurance readiness; those transitions remain governed by their existing procedures.
- REQ-010: Schema migration MUST update tracked defaults, runtime lifecycle helper(s), Codex and Claude source guards, bootstrap/default validation, documentation, and regression fixtures consistently; the existing `define_quality` default/lifecycle drift MUST be resolved rather than carried into v4.
- REQ-011: Codex Cloud MAY be used only as an admitted bounded worker supplied with an exact branch/revision and, when active state is required, a validated handoff snapshot; returned commits/results MUST be reconciled against GitHub before becoming current state, and cloud execution alone MUST NOT be labelled independent assurance.
- REQ-012: The implementation MUST include framework-specific evaluation fixtures covering at least 50 sequential transitions, external subject replacement, irrelevant tool/CI noise, restart/handoff recovery, conflicting patches, and observable context-size comparison against a history-heavy baseline without claiming unmeasured token savings.

## Acceptance Criteria

- AC-001 [req=REQ-001]: Repository search and executable fixtures show one live canonical state path, while handoff snapshots are explicitly non-authoritative and import-only.
- AC-002 [req=REQ-002]: Two patches with the same expected version cannot both succeed; the first increments `state_version` and the second is rejected as stale.
- AC-003 [req=REQ-003]: Malformed, unauthorized, invalid-value, and invariant-breaking patches return a blocking result and leave the last valid canonical state unchanged.
- AC-004 [req=REQ-004]: A fixture changes the authoritative subject after READY assurance and demonstrates deterministic subject-generation advance plus invalidation/staleness of assurance tied to the old subject.
- AC-005 [req=REQ-005]: Active-state fixtures enforce bounded current evidence references, while prior evidence remains addressable from stable report/log references outside the active-state payload.
- AC-006 [req=REQ-006]: Runtime/session guidance specifies the compact context contract and a recovery fixture selects a legal next action without using prior conversation transcript as required input.
- AC-007 [req=REQ-007]: Exported handoff contains Work Block ID, state version/digest, repository/branch revision, and snapshot status; import rejects mismatched/stale subjects and can restore a valid new execution root from a compatible snapshot.
- AC-008 [req=REQ-008]: An adversarial fixture submits overlapping transitions from the same base state and proves deterministic rejection of the stale/conflicting transition.
- AC-009 [req=REQ-009]: Fixtures attempt to expand write-set, integration admission, Hard Stops, governance, and readiness through generic patches and all fail closed.
- AC-010 [req=REQ-010]: v4 defaults and all state readers/writers agree; `prepare`/`open` for Managed state preserve a valid `define_quality` object, existing control-plane fixtures are migrated, and installation/default validation passes.
- AC-011 [req=REQ-011]: Codex Cloud admission documentation records exact role, write-set, branch/revision, data boundary, snapshot/reconciliation procedure, and correctly classifies output evidence/isolation.
- AC-012 [req=REQ-012]: Deterministic evaluation runs the required scenarios, reports correctness/rejection/recovery results and observable context sizes, and does not infer savings when measurement is unavailable.

## Failure and Recovery Semantics

- Invalid patch -> reject; canonical state unchanged.
- Stale `expected_state_version` -> conflict; refresh current state before retry.
- Repository/subject mismatch on handoff import -> reject; reconcile from authoritative Git/GitHub observation.
- Material requirement/scope/authority change -> return to Define; generic state patch cannot encode the change.
- Missing required evidence -> remain `BLOCKED`/`UNVERIFIED`, never synthesize READY.
- Cross-runtime worker result with unknown exact revision -> do not import as current state.

## Non-Goals

- No transcript persistence as canonical state.
- No private chain-of-thought storage.
- No replacement for Engineering Memory or Learning Review.
- No vector/semantic memory service.
- No provider-specific authority model.
- No automatic production/deploy/live-data capability.
