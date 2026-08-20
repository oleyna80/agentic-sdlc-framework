---
schema_version: 1
artifact_type: work_block
artifact_id: wb-git-001-stacked-pr-synchronization
work_block_id: WB-GIT-001
status: completed
owner_role: orchestrator
created_at: 2026-08-16
last_updated: 2026-08-20
process_level: Standard
governance_profile: Controlled
branch: agent/wb-git-001-corrective
owner_approval: Owner requested preserving GitHub operating experience for future sessions on 2026-08-16; Owner approved corrective normalization and terminal closeout of this bounded Work Block on 2026-08-20
critic_gate: SKIPPED
write_gate: BLOCKED
writer: one bounded Coder-equivalent documentation stream
base_revision: 1474c7c5cf2f2e0e74f17aa493c39ac60fa1d94d
---

# WB-GIT-001 — Stacked PR Synchronization Procedure

## Objective

Preserve repeatable Git/GitHub operating lessons from recent framework work so a
future session can synchronize stacked pull requests, preserve frozen assurance
subjects, and avoid accidental history or evidence invalidation without relying
on conversational memory.

Extend the existing `git-orchestration-flow` skill rather than creating a second
overlapping Git skill.

## Why Controlled

This is bounded, reversible documentation/procedure work. It changes no runtime,
hook, permission, authority model, release-state semantics, dependency, live
service, credential, protected branch, or production state. The existing skill
already owns complex Git/PR orchestration.

A separate Critic is skipped proportionally because the change is procedural
documentation with a three-file write-set and no machine enforcement. Normal
review/CI remains applicable before merge.

## Evidence Basis

The procedure is derived from observed repository operations, including:

- non-destructive synchronization of PR #38 after its former stacked parent
  landed on `main`;
- bottom-up synchronization of current stacked PRs #34 → #35 → #36 on
  2026-08-16 using true two-parent merge commits and fast-forward ref updates;
- verification that each synchronized child retained only its intended delta;
- an observed GitHub Contents API no-op update that still created a new commit;
- an observed self-invalidating evidence pattern when an exact validated SHA was
  written into a normative file, thereby creating a new head;
- distinction between PR merge-ref CI evidence and standalone detached-head
  evidence;
- repeated frozen-head independent assurance where a moved subject requires a
  new review rather than reusing the old verdict.

These are operating lessons, not new Git semantics or GitHub authority rules.

## Provenance

- **Classification:** `original_experience_derived`
- **Sources:** no external design asserted as the basis for this mechanism
- **Internal evidence:** the observed PR #38 synchronization; stack #34 → #35
  → #36 on 2026-08-16; GitHub Contents API no-op commit behavior; and repeated
  frozen-subject assurance invalidation described in Evidence Basis
- **Local delta:** records these internal operating lessons as a reusable,
  framework-governed Git orchestration procedure with explicit authority and
  assurance boundaries
- **Rationale:** the mechanism originated from this repository's observed
  operations rather than an identified external design materially shaping it
- **Novelty claim:** none

## In Scope

```text
skills/git-orchestration-flow/SKILL.md
skills/git-orchestration-flow/reference/stacked-pr-synchronization.md
docs/plans/wb-git-001-stacked-pr-synchronization.md
```

## Out of Scope

- changing `AGENTS.md`, governance, hooks, branch protection, rulesets, CI, or
  credentials;
- creating automation that mutates branches automatically;
- changing merge authority;
- changing any open PR in the provenance/Spec Kit stack;
- documenting project-specific secrets, raw prompts, hidden reasoning, or
  transient activity logs.

## Required Procedure Content

`SKILL.md` must define the executable procedure, including:

1. bottom-up stacked synchronization;
2. how to derive the intended child delta from old parent → old child;
3. how to build the synchronized child from the **new parent tree** rather than
   replaying an old whole-tree snapshot;
4. true two-parent merge commits and `force=false` fast-forward branch updates;
5. explicit conflict policy where newly accepted parent semantics win unless the
   child still needs an additive change;
6. post-sync `new parent → new child` delta verification;
7. frozen-subject assurance and `SUBJECT MOVED` handling;
8. GitHub Contents API no-op commit risk;
9. why normative files should not embed their own current validated head SHA;
10. PR merge-ref CI versus detached-head evidence;
11. preservation of file modes when constructing Git trees;
12. PR metadata updates versus repository-content mutations;
13. no merge/default-branch action without the applicable Owner/repository
    authority.

## Acceptance Criteria

1. Existing `git-orchestration-flow` remains the single skill owner for this
   procedure.
2. Main skill contains the core workflow, execution order, decision framework,
   and hard stops for stacked/frozen-subject work while remaining within the
   skill-directory size guidance.
3. Reference contains only supporting terminology, examples, evidence-record
   formats, and background; it contains no workflow instructions.
4. Main skill contains a deterministic bottom-up algorithm and post-sync
   verification requirements.
5. Procedure defaults to non-destructive synchronization and does not recommend
   rebase/force-push when preserving review/history is material.
6. Procedure distinguishes accepted-parent conflict resolution from blind
   old-file overlay.
7. Frozen-head and CI evidence caveats are explicit.
8. No authority, runtime, hook, or CI behavior is changed.

## Verification

- inspect the three-file diff;
- confirm the existing skill catalog still has one `git-orchestration-flow`
  entry and no duplicate skill was introduced;
- run applicable publication/framework contracts through PR CI;
- independent read-only review and independent reproducible verification are
  required for the final corrective frozen subject before closeout.

## Corrective Cycle

- R1: core execution workflow, decision rules, and hard stops are normalized
  into `SKILL.md`; the reference is limited to supporting material under
  `skills/SKILL-CONVENTION.md`.
- R2: this authoritative Work Block records its required provenance
  classification.
- C1: a future terminal closeout projection must set the local source
  `write_gate` to `BLOCKED`; `CLOSED` is descriptive only and not a valid gate
  value.

## Final State

- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Evaluation Verdict:** SKIPPED — deterministic documentation/procedure
  acceptance requires no non-deterministic evaluation
- **Task Status:** completed
- **Closeout Mode:** success-closeout
- **Write Gate:** BLOCKED
- **External VCS State:** non-normative; hosting-platform lifecycle remains
  Owner/repository-controlled.

## Closeout Evidence

- Review: `docs/reports/reviews/wb-git-001-stacked-pr-synchronization.md`
- Verification:
  `docs/reports/verification/wb-git-001-stacked-pr-synchronization.md`
- Drift: `docs/reports/drift/wb-git-001-stacked-pr-synchronization.md`
- Terminal record:
  `docs/reports/closeout/wb-git-001-stacked-pr-synchronization.md`
