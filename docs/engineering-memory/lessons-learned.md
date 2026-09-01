---
schema_version: 1
artifact_type: engineering_memory
artifact_id: lessons-learned
status: promoted
owner_role: orchestrator
last_verified: 2026-08-14
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

## LL-002 — Candidate-derived completion needs a durable, separately validated history

**Status:** adopted prospectively
**Evidence:** `docs/reports/closeout/wb-release-002-candidate-promotion-lifecycle.md`; canonical promotion transition `a144dc2a4f93c15faeab32252dbe30f4dff96c4c` → `541a8e0382849012147a9e33ca9d9929f9dafd39`
**Verified:** 2026-09-01
**Trigger:** a completed evidence-bound candidate must release the single active-candidate slot without being rewritten as raw historical completion.

### Attempted approach

The preceding candidate procedure correctly derived effective completion from
bound evidence, but had no durable promoted-history state before a successor
could be declared.

### What changed the decision

Clearing the candidate alone loses deterministic predecessor continuity, while
adding it to `completed_work_blocks` misstates evidence-derived completion as
raw historical completion. A combined promotion and successor revision also
prevents the intermediate promotion state from being independently validated.

### Replacement

Use an append-only canonical `promoted_candidates` ledger in `FILE_REGISTRY.yml`
with `PROJECT_MAP.md` as its projection. Require a sole-parent, exact two-path
registry/map promotion from an already-valid evidence-complete parent; only
after ordinary validation of that promoted state may a later successor bind to
the effective latest Work Block.

### Reusable lesson

When a lifecycle derives completion from evidence rather than a raw history
entry, preserve that distinction in a durable append-only record and validate
the state transition separately from the next lifecycle declaration. This keeps
predecessor semantics deterministic without rewriting historical facts.

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
