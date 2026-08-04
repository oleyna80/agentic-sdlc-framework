# Integration Plan Template

Use this template only when an approved Work Block permits parallel Coder
write-sets. It operationalizes `AGENTS.md`, accepted governance, the active
Work Block, and the SDD protocol; it grants no authority, VCS permission, or
runtime enforcement.

## Authority and subject

- **Work Block:**
- **Objective:**
- **Approved integration authority:**
- **Common immutable base revision:**
- **Integration worktree / branch:**
- **Integration isolation identifier:**
- **Integration Coder:**
- **Final assurance subject:** integrated revision and path manifest, to be
  recorded only after integration is frozen.

## Stream matrix

| Stream | Coder | Isolation identifier | Isolated worktree / branch | Exact exclusive paths | Dependencies | Required checks | Frozen handoff revision |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

Every stream starts from the recorded common base unless the active Work Block
expressly records another dependency. A path may have one Coder owner only.
The worker-path intersection must be empty. Shared or ambiguous paths are not
permitted worker write-sets; declared glue paths belong solely to the
Integration Coder and are serialized.

## Integration boundary

- **Integration-owned paths (including declared glue/navigation paths):**
- **Named worker revisions eligible for adoption:**
- **Allowed integration method:** only the Owner-approved method and exact
  revisions listed above.
- **Recovery point:** immutable common base and each frozen worker revision.

The Integration Coder is a Coder assignment, not a new authority role. It may
cleanly adopt the listed named frozen worker revisions. It must not edit a
worker-owned path, resolve a content conflict, substitute a revision, or add a
path without returning the Work Block to Define for an Owner decision.

## Freeze and assurance

- **Frozen integrated revision:**
- **Frozen integrated path manifest and digest:**
- **Worker evidence received:**
- **Integrated checks:**
- **Reviewer / Verifier / drift-assessment assignments:**

Worker checks establish implementation evidence only. Reviewer, Verifier, and
drift assessment evaluate the one frozen integrated subject. Any normative edit
after that freeze invalidates readiness and requires a new freeze and applicable
assurance.

## Hard stops

Stop and return to Define for an overlapping write-set, shared worktree,
missing common base or frozen handoff, undocumented dependency, integration
conflict, edit to a worker-owned path, failed required check, scope expansion,
or any unapproved VCS action. Workers never merge directly to the authoritative
branch; staging, commit, push, PR, and merge require their own Owner approval.
