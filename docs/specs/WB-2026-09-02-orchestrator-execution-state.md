---
schema_version: 1
artifact_type: specification
artifact_id: wb-2026-09-02-orchestrator-execution-state
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: define_candidate_round_2
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
6. Model/runtime workers propose bounded changes; a provider-neutral deterministic reducer owns validation, derived invalidation, serialization, atomic write, and conflict rejection.

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
  current_evidence_refs[]   # maximum 16 current pointers
  handoff_snapshot_ref
```

`base_commit` remains the planning baseline to avoid duplicating an already canonical field. Full task history remains in the traceable tasklist; full evidence history remains in reports/log artifacts. `context.current_evidence_refs` is limited to **16** current pointers; older evidence is not deleted from its owning report/log artifact merely because it leaves active state. `progress.blockers` and `progress.pending_decisions` contain only current unresolved items, not history.

## State Mutation Transaction

Every state-changing command MUST serialize the complete transaction:

```text
acquire local state lock with bounded timeout
  -> re-read canonical state while holding lock
  -> validate schema/current state
  -> compare expected_state_version when applicable
  -> validate command/patch and authority rules
  -> compute reducer-derived changes
  -> write temporary file + fsync where supported
  -> atomic replace canonical state
  -> release lock
```

The portable implementation uses a standard-library local file-lock adapter: POSIX advisory locking where available and the corresponding Windows standard-library file-region locking path. Unsupported locking platforms fail closed. Lock acquisition timeout is a conflict/blocking result, not permission to write without serialization. A process crash must release the OS lock; the inert lock file may remain and is ignored by Git.

`state_version` is checked **after acquiring the lock and re-reading state**. Each accepted state-changing transaction increments it exactly once.

## Patch Classes

Generic patches may mutate only runtime context/progress paths explicitly allowlisted by the reducer. The following are **authority/identity/assurance protected** from generic patches:

- `schema_version` and `state_version` (reducer owned);
- `authority_mode`;
- `work_block_id`;
- `governance_profile`;
- `specification`;
- `base_commit`;
- `define_quality`;
- `write_gate`;
- `critic`;
- `assurance`;
- `closeout_mode`;
- `integrations`;
- `write_set`;
- `coordination_write_set`;
- `external_hard_stops`;
- lifecycle stage/readiness transitions that affect authority;
- `subject.current_revision`, `subject.frozen_revision`, and subject generation.

Protected fields change only through dedicated lifecycle/observation/assurance commands that enforce their existing contracts. Generic patch fluency cannot synthesize READY state.

## Subject Observation and Derived Invalidation

A generic patch does not set Git subject revisions. A dedicated observation/reconciliation transition records observation source/evidence and owns subject changes. For a local checkout it resolves the local Git revision itself. When an admitted external observation is supplied, the evidence source and observed revision are recorded explicitly.

If an authoritative current/frozen subject changes, the reducer advances subject generation and invalidates assurance bound to the old generation/subject according to the lifecycle contract. The caller does not manually patch each dependent assurance field.

## Canonical Digest

Portable state/snapshot digests use SHA-256 over canonical JSON bytes:

```text
json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
  -> UTF-8 bytes
  -> no trailing newline in the hashed bytes
  -> SHA-256 lowercase hexadecimal digest
```

A handoff snapshot contains `snapshot_schema_version`, source Work Block ID, source state version, canonical source-state digest, source repository revision/branch identity, snapshot status, and the transported state/context payload. If a `snapshot_digest` is emitted, it is SHA-256 over the canonical snapshot object **with the `snapshot_digest` member omitted**, preventing self-reference.

## Handoff Transport, Import, and Authority Attenuation

A handoff snapshot is transport/evidence, not live state. The preferred cross-runtime transport is a direct task/session payload or another explicitly admitted artifact channel so the target checkout can remain at the exact bound source revision.

If a snapshot is later archived in Git, that archival commit is not the snapshot's bound execution subject. Import validates the declared source revision; intervening commits require explicit reconciliation. No containing-commit self-reference is required.

**Import cannot initialize or expand authority.** The target execution root must already have a canonical Work Block state initialized under its own lifecycle/mission contract. Snapshot protected fields are used only as match predicates. Import may merge compatible operational `progress`, `context`, and subject/evidence observations through the reducer, but it MUST NOT copy/activate source `write_gate`, integrations, Owner approval, assurance readiness, governance profile, write-set, Hard Stops, or external capability. A target blocked default with no matching Work Block identity rejects import until the normal Work Block initialization path establishes the target identity/scope.

## Schema-v3 Migration

A dedicated `migrate-v3` transition handles structurally valid local schema-v3 active state. It:

1. acquires the same state lock and validates known v3 structure;
2. preserves compatible Work Block identity, specification, planning baseline, scope/write-set, Critic/report pointers, evidence/report pointers, and external Hard Stop facts;
3. creates schema-v4 operational fields conservatively;
4. sets `state_version` to `0` for the new v4 state;
5. forces `write_gate` to `BLOCKED`;
6. clears active integration admission in the migrated local state until separately re-established;
7. marks previously READY assurance as not currently subject-bound (`UNVERIFIED` while preserving report/isolation evidence) until v4 subject reconciliation/assurance revalidation;
8. leaves malformed/unknown v3 input unchanged and returns BLOCKED.

Migration never silently reopens writes or declares prior assurance v4-bound.

## Context-Size Metric

The portable comparison metric is **UTF-8 serialized bytes of the assembled default Orchestrator context** for each evaluated step. If a runtime exposes exact tokenizer/token counts, they may be recorded additionally, but byte size is the required cross-runtime baseline. Evaluation reports per-step and cumulative bytes for state-centric and history-heavy baselines.

## Requirements

- REQ-001: The framework MUST retain exactly one live canonical Work Block state per execution root at `.agent/active-work-block.json`; no parallel live Execution State SSOT may be introduced.
- REQ-002: Schema v4 MUST include a monotonic `state_version`, and every generic mutable-state transition MUST execute under an inter-process serialized read/validate/write transaction and require an exact `expected_state_version` compare-and-swap precondition checked after the lock is acquired and state re-read.
- REQ-003: A provider-neutral deterministic reducer MUST validate command/patch shape, allowed paths, values, state version, lifecycle invariants, and authority boundaries before atomically replacing canonical state; rejection/lock timeout MUST preserve the previous valid state.
- REQ-004: Authoritative observations that change the current or frozen assurance subject MUST use a dedicated observation/reconciliation transition that deterministically invalidates/stales assurance bound to the prior subject and advances subject generation without relying on an LLM to patch dependent fields.
- REQ-005: Active state MUST store no more than 16 current evidence pointers; durable provenance MUST remain in existing report/log/evidence artifacts and MUST be retrievable without replaying full chat/tool history.
- REQ-006: Default Orchestrator context assembly MUST be defined as immutable procedure + canonical current state + latest relevant observation + selectively retrieved evidence, and MUST NOT require full conversation replay for routine next-step decisions.
- REQ-007: The framework MUST support deterministic canonical-digest export and authority-attenuating import of a non-authoritative handoff snapshot for another initialized session/runtime, bound to exact Work Block ID, state version/digest, branch/repository revision, and current-state/repository reconciliation without self-referential containing-commit SHA.
- REQ-008: Concurrent/overlapping state mutation MUST fail deterministically through local inter-process serialization plus state-version compare-and-swap; a worker MUST NOT silently overwrite another worker's accepted transition.
- REQ-009: Generic state patches and handoff imports MUST NOT create or expand write authority, integration admission, Hard Stop capability, governance profile, Owner approval, assurance readiness, lifecycle readiness, or Git subject identity; those transitions remain governed by dedicated existing/new reducer commands and their authority contracts.
- REQ-010: Schema migration MUST update tracked defaults, runtime lifecycle helper(s), Codex and Claude state readers/guards, bootstrap/default validation, documentation, and regression fixtures consistently; the existing `define_quality` default/lifecycle drift MUST be resolved, and a deterministic fail-closed v3->v4 active-state migration path MUST be provided.
- REQ-011: Codex Cloud MAY be used only as an admitted bounded worker supplied with an exact branch/revision and, when active state is required, a validated handoff snapshot; returned commits/results MUST be reconciled against GitHub before becoming current state, and cloud execution alone MUST NOT be labelled independent assurance.
- REQ-012: The implementation MUST include framework-specific evaluation fixtures covering at least 50 sequential transitions, actual concurrent same-version transitions, external subject replacement, irrelevant tool/CI noise, restart/handoff recovery, v3 migration, and observable context-size comparison using cumulative/per-step UTF-8 serialized bytes against a history-heavy baseline without claiming unmeasured token savings.

## Acceptance Criteria

- AC-001 [req=REQ-001]: Repository search and executable fixtures show one live canonical state path, while handoff snapshots are explicitly non-authoritative and import-only.
- AC-002 [req=REQ-002]: Two processes attempting transitions from the same expected version are serialized; exactly one succeeds, increments `state_version` once, and the other re-reads the new version and fails stale/conflict.
- AC-003 [req=REQ-003]: Malformed, unauthorized, invalid-value, invariant-breaking, and lock-timeout transitions return a blocking result and leave the last valid canonical state unchanged.
- AC-004 [req=REQ-004]: A fixture changes the authoritative subject after READY assurance through the dedicated observation path and demonstrates deterministic subject-generation advance plus invalidation/staleness of assurance tied to the old subject.
- AC-005 [req=REQ-005]: Active-state fixtures reject a seventeenth current evidence reference unless an existing pointer is retired from active state, while prior evidence remains addressable outside the active-state payload.
- AC-006 [req=REQ-006]: Runtime/session guidance specifies the compact context contract and a recovery fixture selects a legal next action without prior conversation transcript as required input.
- AC-007 [req=REQ-007]: Exported handoff uses the specified canonical SHA-256 digest, contains source Work Block/state/repository identity, and import rejects default/uninitialized targets, authority mismatches, stale/incompatible subjects, and any attempt to activate source authority while successfully merging compatible operational state into an already initialized target.
- AC-008 [req=REQ-008]: A true concurrent adversarial fixture proves that overlapping same-version transitions cannot both commit and that no accepted state is lost.
- AC-009 [req=REQ-009]: Fixtures attempt via generic patch and handoff import to alter protected identity/scope/write/integration/Hard-Stop/assurance/lifecycle/subject fields and all fail or are ignored as non-importable authority inputs.
- AC-010 [req=REQ-010]: v4 defaults and all authority-relevant state readers/writers agree; Managed `prepare/open` preserves valid `define_quality`; valid v3 migration produces blocked v4 state with preserved evidence/scope and unbound assurance, while malformed v3 remains unchanged; installation/control-plane fixtures pass.
- AC-011 [req=REQ-011]: Codex Cloud admission documentation records exact role, write-set, branch/revision, data boundary, snapshot/reconciliation procedure, and correctly classifies output evidence/isolation.
- AC-012 [req=REQ-012]: Deterministic evaluation runs the required scenarios, reports correctness/rejection/recovery/concurrency/migration results plus per-step and cumulative UTF-8 context bytes for state-centric and history-heavy baselines, and does not infer token savings when exact token measurement is unavailable.

## Failure and Recovery Semantics

- Invalid patch/command -> reject; canonical state unchanged.
- Lock timeout -> BLOCKED/conflict; never bypass serialization.
- Stale `expected_state_version` -> conflict; refresh current state before retry.
- Repository/subject mismatch on handoff -> reject; reconcile from authoritative observation.
- Handoff into uninitialized/default target -> reject; initialize target Work Block through normal lifecycle first.
- Valid v3 migration -> v4 blocked state requiring revalidation before writes; invalid v3 -> unchanged/BLOCKED.
- Material requirement/scope/authority change -> return to Define; generic state patch cannot encode the change.
- Missing required evidence -> remain `BLOCKED`/`UNVERIFIED`, never synthesize READY.
- Cross-runtime worker result with unknown exact revision -> do not accept as current state.

## Non-Goals

- No transcript persistence as canonical state.
- No private chain-of-thought storage.
- No replacement for Engineering Memory or Learning Review.
- No vector/semantic memory service.
- No provider-specific authority model.
- No automatic production/deploy/live-data capability.
