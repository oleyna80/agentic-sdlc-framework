---
schema_version: 1
artifact_type: critic_report
work_block_id: WB-2026-09-02-orchestrator-execution-state
status: supplement_required
verdict: SUPPLEMENT
critic_role: critic
isolation: same_context_read_only
created_at: 2026-09-02
subject_revision: ac4ef11ba00a355adae3de15961c7ab4ec7e2308
---

# Critic — Orchestrator Execution State

## Verdict

**SUPPLEMENT** — architecture direction is sound, but source write gate MUST remain BLOCKED until C-01 through C-05 are incorporated into the specification/task decomposition and consistency is rechecked.

This is a same-context read-only Critic and is not represented as independent assurance.

## Accepted Direction

The following choices are accepted:

- extend the existing `.agent/active-work-block.json` rather than create a second live state SSOT;
- advance to schema v4 so required execution semantics fail closed under old readers;
- keep evidence and Engineering Memory separate from live execution state;
- use a provider-neutral deterministic reducer;
- use non-authoritative handoff snapshots for cross-runtime transport;
- treat Codex Cloud as an admitted bounded worker, not authority or automatic independent assurance;
- evaluate long-horizon correctness/context behavior locally rather than importing paper benchmark claims.

## Required Supplements

### C-01 — CAS is not safe without serialized read/validate/write
**Severity:** MATERIAL / blocking

Checking `expected_state_version` and then using atomic file replacement does not prevent lost updates when two processes both read version N before either replacement occurs. Both can validate N and the later replace can overwrite the earlier accepted transition.

**Required correction:** define an inter-process serialization mechanism around the complete read -> validate expected version -> reduce -> write transaction. The implementation should use a deterministic project-local lock with bounded timeout, re-read canonical state while holding the lock, and only then compare `expected_state_version`. Conflict/lock timeout must fail closed. Add an actual concurrent fixture, not only sequential stale-patch tests.

### C-02 — Handoff digest canonicalization is unspecified
**Severity:** MATERIAL / blocking

`state digest` is not portable unless byte canonicalization is deterministic across runtimes.

**Required correction:** specify a provider-neutral digest algorithm. Recommended minimum: SHA-256 over canonical UTF-8 JSON with lexicographically sorted object keys, compact separators, `ensure_ascii=false`, no insignificant whitespace, and a precisely stated treatment of the final newline. Snapshot schema/version must be part of the hashed payload or separately bound unambiguously.

### C-03 — Authority-protected field set is incomplete
**Severity:** MATERIAL / blocking

REQ-009 prohibits authority expansion, but the current minimum protected list does not explicitly protect `work_block_id`, `specification`, `base_commit`, `define_quality`, `write_gate`, `critic`, `assurance`, and `closeout_mode`. A generic patch grammar must not be able to synthesize READY assurance or change specification identity merely because those paths were omitted from the example list.

**Required correction:** enumerate the complete top-level authority/assurance identity surfaces as protected from generic patches. Dedicated lifecycle/assurance commands may mutate them only under their existing contracts.

### C-04 — Handoff import can accidentally transfer write authority
**Severity:** MATERIAL / blocking

A snapshot of an active Coder state can contain `write_gate: READY`, admitted integrations, or other local process state. Importing it over a fresh blocked execution root would turn transport into authority propagation.

**Required correction:** handoff import must be authority-attenuating/fail-closed. It may restore operational execution context and evidence, but MUST set/retain source-write state BLOCKED and MUST NOT activate integration admission, Owner approval, assurance readiness, or external capability. The target runtime separately re-establishes its permitted write/admission state under the active Work Block and mission contract.

### C-05 — Schema-v3 active-state migration behavior is undefined
**Severity:** MATERIAL / blocking

After readers move to v4, an existing local schema-v3 active Work Block becomes invalid. Without a migration rule operators may manually edit it or lose operational context.

**Required correction:** define a deterministic v3 -> v4 migration path for structurally valid current state. Migration must preserve evidence/scope facts where compatible, initialize new fields conservatively, and force `write_gate` BLOCKED until v4 Define/critic prerequisites are revalidated. Malformed/unknown v3 input fails closed and remains untouched.

## Non-Blocking Recommendations

1. Keep `progress.blockers` and `progress.pending_decisions` as *current unresolved* items rather than history; consider bounded item counts/lengths to protect compactness.
2. Do not let a generic patch directly set `subject.current_revision`; prefer a dedicated observation/reconciliation transition that records observation source/evidence and owns dependent invalidation.
3. Historical schema-v3 reports/plans should remain unchanged where they describe historical truth; migration applies to current contracts/readers only.

## Gate Decision

`SOURCE WRITE GATE MAY OPEN: NO`

Return to Define, revise specification/tasklist/plan as needed, refresh traceability/consistency evidence, then perform a second Critic pass.
