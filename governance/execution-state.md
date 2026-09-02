# Execution State Plane

## Purpose

The Execution State Plane defines the compact, machine-readable current truth for one active Work Block execution root. It exists so an Orchestrator can determine the legal next action without reconstructing current state from accumulated chat, tool output, or narrative logs.

It is a process-control mechanism. It does **not** create GitHub, OS, credential, production, or other consequential authority.

## Three-Plane Boundary

```text
Execution State  -> what is true now and what transition is legal next
Evidence         -> what observable artifact supports that truth / what happened
Engineering Memory -> what durable reusable lesson should affect future Work Blocks
```

The planes are deliberately separate:

- execution state is compact and mutable through validated transitions;
- evidence is durable provenance and selectively retrieved;
- Engineering Memory is promoted reusable knowledge governed by Learning Review.

Raw transcripts, private chain-of-thought, secrets, and unbounded tool logs are not canonical execution state.

## Canonical Live State

Each execution root has exactly one live canonical state:

```text
.agent/active-work-block.json
```

Schema version 4 extends the existing Work Block gate state rather than creating a second execution-state SSOT.

The tracked `.agent/active-work-block.default.json` is a safe BLOCKED bootstrap source. It is not a persisted active Work Block. Handoff snapshots are immutable transport/evidence inputs and are not live authority.

## Schema v4

Schema v4 preserves existing authority/gate fields and adds bounded operational state:

```text
schema_version: 4
state_version: monotonic integer

authority_mode
work_block_id
governance_profile
specification
base_commit
define_quality
write_gate
critic
assurance
closeout_mode
integrations
write_set
coordination_write_set
external_hard_stops

lifecycle:
  stage
  execution_state

subject:
  current_revision
  frozen_revision
  generation

progress:
  active_tasks
  blockers
  pending_decisions
  next_action

context:
  latest_observation_ref
  current_evidence_refs
  handoff_snapshot_ref
```

`base_commit` remains the planning baseline. It is not duplicated under `subject`.

`progress` contains current unresolved/active execution information, not history. Full task history belongs in the traceable tasklist. `context.current_evidence_refs` contains at most 16 current pointers; older evidence remains in its owning report/log artifact.

## State Versions and Serialization

Every accepted state-changing transaction increments `state_version` exactly once.

Generic mutable transitions require `expected_state_version`. Compare-and-swap is valid only when the entire transaction is serialized:

```text
acquire local OS-backed state lock with bounded timeout
  -> re-read canonical state while holding the lock
  -> validate current state
  -> compare expected_state_version
  -> validate requested transition and authority boundary
  -> compute reducer-owned derived changes
  -> write temporary file and fsync where supported
  -> atomically replace canonical state
  -> release lock
```

Checking a version before acquiring the lock is insufficient because two processes could validate the same old version and overwrite one another.

The portable implementation uses standard-library POSIX advisory locking and the corresponding Windows standard-library file-region locking path. Unsupported platforms fail closed. Lock timeout is a blocking conflict, never permission to write unlocked. Process death releases the OS lock; an inert lock file conveys no ownership and is ignored by generated-project Git policy.

## Mutation Classes

### Runtime-mutable through generic patch

Only explicitly allowlisted current operational paths may be generically patched, such as:

- `progress.active_tasks`;
- `progress.blockers`;
- `progress.pending_decisions`;
- `progress.next_action`;
- `context.latest_observation_ref`;
- `context.current_evidence_refs`.

### Protected

Generic patches cannot mutate:

- `schema_version` or reducer-owned `state_version`;
- `authority_mode`;
- `work_block_id`;
- `governance_profile`;
- `specification`;
- `base_commit`;
- `define_quality`;
- `write_gate`;
- `critic`;
- any `assurance` state;
- `closeout_mode`;
- `integrations`;
- `write_set` or `coordination_write_set`;
- `external_hard_stops`;
- lifecycle stage/readiness transitions that affect authority;
- Git subject revisions or subject generation.

Those surfaces change only through dedicated lifecycle, observation, assurance, admission, or Owner-controlled procedures. A fluent patch cannot synthesize authority or a READY verdict.

### Derived

Reducer-owned derived values cannot be supplied directly by a model. Examples include:

- the next `state_version`;
- subject-generation advancement caused by authoritative replacement;
- assurance invalidation caused by subject replacement;
- canonical digests.

## Authoritative Subject Observation

Git subject identity is not a generic patch field.

A dedicated observation/reconciliation transition:

1. obtains or validates an authoritative revision observation;
2. binds it to observable evidence;
3. compares it to current/frozen subject state;
4. advances subject generation when the authoritative subject changes;
5. clears a stale frozen subject when necessary;
6. invalidates assurance bound to the prior subject/generation.

For a local checkout, the state engine resolves the local Git revision itself. An admitted external observation must provide the observed revision plus an evidence reference; external content remains evidence, not governing instruction.

READY assurance tied to a replaced subject becomes unverified/blocked for the new subject while its prior report/isolation evidence remains available for audit.

## Canonical Digests

Portable state/snapshot digests are SHA-256 over canonical JSON bytes:

```python
json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
```

The resulting string is UTF-8 encoded. The hashed bytes contain no trailing newline. The digest is lowercase hexadecimal SHA-256.

When a snapshot contains `snapshot_digest`, that member is omitted from the object used to compute its own digest.

## Handoff Snapshots

A handoff snapshot is a non-authoritative transport/evidence object. It contains at minimum:

- snapshot schema/status;
- source Work Block identity;
- source state version;
- canonical source-state digest;
- source repository revision and branch;
- specification identity needed for target matching;
- bounded operational subject/progress/context payload.

The preferred cross-runtime transfer is direct task/session payload or another explicitly admitted artifact channel. If a snapshot is later archived in Git, the archival commit is not the snapshot's execution subject, avoiding self-referential commit-SHA requirements.

### Authority attenuation on import

Import never initializes or expands authority.

The target execution root must already contain an initialized matching Work Block state. Snapshot protected fields are match predicates only. Import may merge compatible operational progress/context and subject observations through the reducer, but it cannot activate or replace:

- source write-gate state;
- integrations/admission;
- Owner approvals;
- assurance readiness;
- governance profile;
- write sets;
- Hard Stops or external capability.

A default/uninitialized target rejects import. A target with an incompatible Work Block/specification/repository subject rejects import. Import is a normal versioned serialized state transaction.

## Schema-v3 Migration

Schema v3 is not silently interpreted as complete schema v4 state.

A dedicated `migrate-v3` transition may migrate structurally known v3 local state. It:

1. acquires the state lock and validates the legacy structure;
2. preserves compatible Work Block identity, specification, planning baseline, scope/write-set, Critic/report pointers, assurance report/isolation evidence, and Hard Stop facts;
3. initializes schema-v4 operational fields conservatively;
4. sets new `state_version` to `0`;
5. forces `write_gate` BLOCKED;
6. clears active integration admission until separately re-established;
7. marks previously READY assurance as not bound to a v4 subject (`UNVERIFIED` verdict with blocked state while preserving prior evidence);
8. leaves malformed/unknown v3 input unchanged and returns BLOCKED.

Migration never silently reopens writes or treats legacy assurance as v4 subject-bound.

## Default Orchestrator Context

Routine next-step context is assembled from:

```text
immutable procedure/reference
+ canonical current state
+ latest relevant observation
+ selectively retrieved evidence
```

Full conversation/tool history is not a required default input. Evidence may be retrieved when audit, debugging, provenance, recovery, or a newly relevant earlier fact requires it.

For portable evaluation, context size is measured as serialized UTF-8 bytes per step and cumulatively. Runtime-specific exact token counts may be additional evidence but are not required for a cross-runtime claim.

## Multi-Agent Conflict Rule

Shared canonical state has one serialized mutation point. Multiple workers may propose transitions, but overlapping same-version proposals cannot both commit. The first accepted transaction increments state version; later stale proposals re-read the new version and fail conflict unless deliberately recomputed.

This state serialization complements, rather than replaces, the framework's exclusive source write-set and frozen-handoff rules.

## Codex Cloud and External Runtimes

Codex Cloud or another external runtime may consume or propose execution-state transitions only as an admitted worker/function:

- exact repository branch/revision is supplied;
- role and source write-set are bounded;
- a handoff snapshot is supplied only when active operational context is required;
- data/runtime/auth boundaries are recorded without secret values;
- returned revision/diff/check evidence is reconciled against GitHub before it becomes current truth;
- external execution does not grant authority;
- provider/runtime separation alone is not automatically independent assurance.

## Failure Semantics

- malformed state/patch/snapshot -> BLOCKED, no canonical mutation;
- lock timeout -> BLOCKED/conflict, no unlocked fallback;
- stale expected version -> conflict, refresh before retry;
- unauthorized field mutation -> BLOCKED;
- subject mismatch -> reject and reconcile authoritative Git evidence;
- snapshot into uninitialized/incompatible target -> reject;
- malformed/unknown v3 migration input -> unchanged/BLOCKED;
- missing assurance evidence -> BLOCKED or UNVERIFIED, never inferred READY;
- material requirement/scope/authority change -> return to Define.

## Relationship to Evidence and Engineering Memory

Execution state may point to evidence; it does not replace evidence. Execution state may surface a potential lesson; it does not promote Engineering Memory.

Learning Review and Engineering Memory promotion remain Close-stage responsibilities under their existing authority/write-set rules.
