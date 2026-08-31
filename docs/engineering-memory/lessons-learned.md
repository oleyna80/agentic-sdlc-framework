---
schema_version: 1
artifact_type: engineering_memory
artifact_id: lessons-learned
status: promoted
owner_role: orchestrator
last_verified: 2026-08-31
authority: lower_than_root_agents_and_accepted_governance
review_trigger: new_evidence_supersedes_a_recorded_lesson_or_a_recurring_pattern_is_confirmed
---

# Lessons Learned

This log records reusable engineering lessons from implemented, rejected,
retired, or materially revised framework approaches. It preserves the decision
lesson rather than raw conversation history.

Each entry should identify the attempted approach, why it looked reasonable,
what evidence changed the decision, the replacement, and the reusable principle.
Historical entries do not override current Owner instruction, governance,
specifications, ADRs, or active Work Blocks.

## LL-001 — Per-Work-Block SSH signing for normal development

**Status:** retired from the normal development path  
**Evidence:** `docs/plans/wb-core-003f-github-native-authority-model.md` and
`docs/reports/closeout/wb-core-003f-github-native-authority-model.md`  
**Verified:** 2026-08-14

### Attempted approach

The framework used SSH-signed authorization records, detached `.sig` files,
`allowed_signers`, authorization-bootstrap commits, expiry/replay checks, and
cross-runtime enforcement to provide stronger authorization around agent-driven
Git mutations.

### Why it initially looked attractive

The approach appeared to create a strong explicit Owner authorization boundary
for potentially dangerous agent actions and to make authorization independently
verifiable.

### What changed the decision

Implementation and recovery work showed that the mechanism imposed substantial
complexity on ordinary reversible development operations:

- authorization itself required Git state changes, creating bootstrap friction;
- replay, expiry, specification-digest, signature, and recovery states multiplied
  failure modes;
- equivalent behavior had to remain aligned across runtimes;
- project-local hooks were still writable by the same OS principal and therefore
  could not become a true independent security boundary;
- the operational cost was disproportionate to the threat addressed for normal
  scoped branch work.

### Replacement

Normal scoped development now relies on Work Block/write-set discipline,
feature-branch flow, CI and review, protected GitHub repository rules, and
least-privilege credentials. Production, VPS, database, secret, destructive,
and other consequential capabilities remain outside the normal agent channel.

### Reusable lesson

Do not solve a capability-boundary problem with elaborate project-local ceremony
when a simpler external boundary can enforce the meaningful risk more reliably.
Security strength must be evaluated together with operational complexity,
maintainability, and the actual threat model.

This lesson does **not** mean cryptographic authorization is generally wrong. It
means cryptographic machinery should be introduced when it protects a real,
independent, sufficiently valuable boundary rather than as a default layer over
low-risk reversible development work.

## LL-002 — Closeout must not depend on one ephemeral `/tmp` copy

**Status:** promoted  
**Evidence:** AzurSysTech canonical-checkout reconciliation and closeout recovery,
2026-08-30; preservation evidence showed that lifecycle completion could depend
on artifacts held only in a temporary execution workspace.  
**Verified:** 2026-08-31

### Attempted approach

A reconciliation Work Block used `/tmp` as its execution workspace and allowed
closeout-relevant Work Block/evidence material to exist there while the lifecycle
continued.

### Why it initially looked attractive

A disposable isolated workspace is useful for recovery, verification, rehome,
and other operations that must not mutate a canonical checkout. Keeping the
working artifacts next to that isolated execution also reduces incidental writes
to the project repository.

### What changed the decision

The closeout path exposed a durability problem: an ephemeral workspace can be
removed by reboot, cleanup, session loss, or an unrelated maintenance action.
If the only copy of a required Work Block or assurance/closeout artifact lives
there, Close becomes dependent on infrastructure that is explicitly not durable.
The workflow can therefore lose the evidence required to prove its own completed
state even though the underlying execution was correct.

### Replacement

Use `/tmp` only as an execution/cache surface. Before lifecycle Close relies on an
artifact, the artifact must either:

- exist in a durable canonical project/repository location; or
- have a verified durable copy or stable reference outside the ephemeral
  workspace.

Closeout preflight should fail closed when a required input exists only in an
ephemeral path and should provide a recovery/persistence step before Close.
Cleanup of the temporary workspace must occur only after durable reconciliation.

### Reusable lesson

Ephemeral isolation and durable lifecycle evidence are different concerns. An
isolated temporary workspace may be the safest place to execute recovery work,
but it must never become the sole source of truth for artifacts required by
Assure, Close, or later recovery.

## LL-003 — New historical invariants need a structural enforcement boundary

**Status:** promoted  
**Evidence:** `WB-RELEASE-002` promotion-ledger work, 2026-08-31. Activation of
full ancestry validation exposed historical commit
`8ec1621dd839137f5888ac99fe7ad5a59a60bff0`, whose committed
`FILE_REGISTRY.yml` contains unresolved conflict markers from before the new
promotion-history contract existed.  
**Verified:** 2026-08-31

### Attempted approach

The new release-state validator applied modern promotion-ledger and historical
integrity checks across the entire reachable ancestry when validating the first
canonical promotion.

### Why it initially looked attractive

A uniform ancestry scan is simple to reason about and maximally fail-closed. It
appears to guarantee that every historical state satisfies the same invariants
that protect current and future promotion transitions.

### What changed the decision

The first real promotion attempt reached legacy repository history that predates
the invariant and contains committed malformed canonical state. That history is
a real repository fact, not current working-tree corruption, but it cannot be
repaired without rewriting published history. Treating every pre-contract
ancestor as if it had been governed by a later invariant can therefore make the
new mechanism impossible to adopt at all.

At the same time, simply ignoring malformed ancestry would create a bypass: a
post-adoption transition could temporarily corrupt canonical history and later
repair it, defeating append-only and historical-integrity guarantees.

### Replacement

Historical enforcement must have a **structural**, ancestry-derived boundary:

- legacy history before the first valid adoption/promotion boundary may be
  tolerated only when it is irrelevant to the current protected proof;
- the adoption boundary itself and all protected descendants must remain fully
  fail-closed;
- malformed states in candidate/evidence/promotion proof lineage must never be
  tolerated;
- no SHA-, date-, or Work-Block-specific exception may define the boundary;
- if the boundary cannot be proved from repository structure, validation must
  fail closed rather than guess.

Regression fixtures should cover both legacy malformed ancestry that precedes
adoption and temporary/malformed history after adoption that must remain blocked.

### Reusable lesson

Do not retroactively require a newly introduced invariant to have been true
before the invariant existed. Define an explicit structural `legacy -> enforced`
boundary, then make every transition after that boundary strictly fail-closed.
This preserves adoptability without weakening the guarantees of the new regime.
