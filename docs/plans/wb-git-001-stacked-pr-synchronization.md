---
schema_version: 1
artifact_type: work_block
artifact_id: wb-git-001-stacked-pr-synchronization
work_block_id: WB-GIT-001
status: in_progress
owner_role: orchestrator
created_at: 2026-08-16
last_updated: 2026-08-16
process_level: Standard
governance_profile: Controlled
branch: agent/git-orchestration-stacked-sync
owner_approval: Owner requested preserving GitHub operating experience for future sessions on 2026-08-16
critic_gate: SKIPPED
write_gate: READY
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

The reference must explain:

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
2. Main skill remains compact and routes stacked/frozen-subject work to one
   detailed reference.
3. Reference contains a deterministic bottom-up algorithm and post-sync
   verification checklist.
4. Procedure defaults to non-destructive synchronization and does not recommend
   rebase/force-push when preserving review/history is material.
5. Procedure distinguishes accepted-parent conflict resolution from blind
   old-file overlay.
6. Frozen-head and CI evidence caveats are explicit.
7. No authority, runtime, hook, or CI behavior is changed.

## Verification

- inspect the three-file diff;
- confirm the existing skill catalog still has one `git-orchestration-flow`
  entry and no duplicate skill was introduced;
- run applicable publication/framework contracts through PR CI;
- independent read-only review is sufficient for this documentation-only
  Controlled change before merge.

## Current State

- Stage: Execute — documentation/procedure
- Write Gate: READY for the three paths above
- Critic: SKIPPED proportionally; no architecture/authority change
- Merge: not authorized
