# Stacked PR Synchronization and Frozen-Subject Assurance

Use this reference when a pull request was built on another feature branch, the
parent/base has moved or merged, and preserving review history and exact assurance
subjects matters.

The objective is **not** to make history look linear. The objective is to produce
a new child head whose tree means:

```text
accepted new parent
+ only the still-intended child delta
```

while preserving the old child history non-destructively.

## 1. Core Invariants

1. **Synchronize bottom-up.** Update the lowest parent first, then use that exact
   synchronized head as the next child's parent.
2. **New parent is the semantic baseline.** Do not restore an old whole-file
   version over changes already accepted in the parent/main branch.
3. **Preserve child intent, not stale bytes.** Reapply only the child behavior or
   artifact delta that is still intended after the parent changed.
4. **Prefer a real merge commit.** When review/history preservation matters,
   default to a two-parent merge rather than rebase/force-push.
5. **Advance refs without force.** A successful synchronization should normally
   be a fast-forward update of the existing child branch.
6. **Verify the child delta after synchronization.** The authoritative check is
   `new_parent → new_child`, not the visual plausibility of the merge operation.
7. **Assurance is subject-bound.** If the reviewed head moves, the old verdict is
   historical evidence only; it is not assurance for the new head.

## 2. Terminology

For one stacked child:

```text
P0 = old parent head/base
C0 = old child head
P1 = new accepted/synchronized parent head
C1 = synchronized child head
```

The intended relationship is:

```text
intent_delta = semantic delta of P0 -> C0
C1 tree      = P1 tree + still-valid intent_delta
C1 parents   = [C0, P1]
```

Do **not** assume `P0 → C0` can always be replayed byte-for-byte. Parent changes
may intentionally supersede part of the child's old representation.

## 3. Preflight

Before mutation, record:

- repository and PR number;
- current PR base branch and base SHA;
- current child head SHA;
- exact new parent SHA;
- whether the PR is Draft;
- old parent → child changed filenames/diff;
- new parent changes that overlap those paths;
- current CI/review/frozen-head evidence and which SHA it actually covers.

Stop if the named child head has moved unexpectedly before synchronization.
Resolve that subject movement first rather than mixing two writers' histories.

## 4. Bottom-Up Stack Algorithm

For a stack such as:

```text
main
  └─ PR A
      └─ PR B
          └─ PR C
```

synchronize in this order:

```text
main -> A
new A -> B
new B -> C
```

Never synchronize C first and then rewrite its parent assumptions underneath it.

### Step 1 — Freeze the old child intent

Inspect `P0 → C0` and classify every changed path:

- **child-only:** parent has not materially changed the path;
- **parent-overlap, additive:** parent changed the path but the child still needs
  a small compatible addition;
- **parent supersedes child:** accepted parent semantics replace the old child
  representation;
- **uncertain/material conflict:** resolution changes requirements, architecture,
  authority, or scope and must return to Define/Owner decision.

Changed-file count alone is not enough; read overlapping semantic contracts.

### Step 2 — Start from the new parent tree

The synchronized result must be built from `P1`, not from the old child tree.
This prevents stale parent files from reappearing merely because they existed in
`C0`.

With a normal local checkout, the usual approach is:

```bash
git switch <child-branch>
git status --short
git merge --no-ff --no-commit <new-parent-ref>
```

Resolve only the actual overlaps, then commit the merge. Do not use blanket
`ours`/`theirs` strategy choices for normative files.

When the operating environment exposes Git's object database but no convenient
local checkout, the equivalent operation is:

1. create a resolved tree `T1` from `P1` + intended child delta (using the **new parent tree** as `base_tree` and overlaying only intended child blobs/resolutions);
2. create commit `C1` with parents `[C0, P1]` without moving the branch ref;
3. inspect/verify `T1` and `P1 -> C1` completely before any ref update;
4. only after verification passes, update the child branch ref with force disabled.

Conceptually:

```text
T1 = tree(base=P1.tree, overlays=resolved_child_delta)
C1 = commit(tree=T1, parents=[C0, P1])

verify(P1 -> C1)

only if verification passes:
update_ref(child_branch, C1, force=false)
```

The creation of the Git commit object itself is not the consequential remote
branch movement. The first parent keeps the child branch's history continuous.
The second parent records the synchronization with the new parent.

### Step 3 — Resolve overlaps using parent-first semantics

For every overlapping path:

1. read the accepted current parent version;
2. identify the exact child requirement that still survives;
3. add only that requirement to the parent version;
4. preserve newly accepted parent architecture, naming, authority, documentation
   placement, tests, and contracts;
5. do not copy the old child file wholesale merely because it is easier.

Example:

```text
old child AGENTS.md contains detailed lifecycle prose
new parent has accepted a compact AGENTS.md + workflow routing architecture
```

Correct resolution:

```text
keep new compact AGENTS.md
place surviving child lifecycle detail in the workflow/skill owner
```

Incorrect resolution:

```text
restore old detailed AGENTS.md and thereby undo the accepted parent design
```

### Step 4 — Verify the resulting child locally

No remote ref update may occur before local post-sync verification passes.
After constructing or committing `C1` locally, but before pushing or updating the
remote ref, compare:

```text
P1 -> C1
```

not merely:

```text
C0 -> C1
```

Check at minimum:

- changed filenames are exactly expected;
- intended child delta is preserved;
- stale inherited parent paths are absent;
- accepted parent files not owned by the child remain byte/semantically intact;
- no unrelated files were reintroduced;
- semantic conflict resolution matches accepted-parent-first policy;
- file modes are correct where applicable;
- `C1` has the intended ancestry (`[C0, P1]`).

For a research child that originally changed two files, a clean synchronization
should still normally show exactly those two files against its new parent.

If this verification fails:

**STOP.** Do not push. Do not move the remote branch. Do not trigger unnecessary
PR subject movement or CI.

### Step 5 — Advance the branch non-destructively

Only after local verification in Step 4 passes:

- confirm the remote child branch still points to the previously recorded `C0`;
- perform a normal non-force push or `update_ref(force=false)`:

```bash
git push <remote> <child-branch>
```

or, with a ref API, explicitly use `force=false`.

If a non-force update is rejected, **STOP** and inspect why the remote child moved.
Never silently fall back to force-push.

After remote update:

- re-read PR, base SHA, and head SHA metadata to confirm they reflect the expected
  synchronized subject;
- confirm the PR base SHA now points to the intended parent head (`P1`);
- confirm the PR remains Draft/Ready as intended;
- check mergeability, but do not describe remote mergeability as proof of semantic correctness.

## 5. Retargeting vs Synchronizing

Retargeting a PR changes which branch GitHub compares against. It does not by
itself reconcile the child tree with newly accepted parent changes.

Use these separately:

- **retarget** when only the PR comparison base should change and the child tree
  already correctly includes the new parent semantics;
- **synchronize** when the child history/tree needs the new parent incorporated;
- often synchronize first, verify `new_parent → child`, then retarget if the
  stack structure changed because a parent merged.

Do not interpret GitHub showing a clean diff after retarget as proof that all
semantic parent changes were incorporated correctly.

## 6. Frozen-Subject Assurance

Independent assurance is bound to an exact subject:

```text
frozen_base_sha -> frozen_head_sha
```

Before starting assurance:

1. read PR base SHA and head SHA from GitHub;
2. confirm both live values match the requested frozen subject (`frozen_base_sha`
   and `frozen_head_sha`);
3. capture the changed-file set and diff for that exact pair;
4. perform review read-only.

Immediately before issuing the final verdict, re-read both `current_base_sha` and
`current_head_sha` from GitHub and compare:

```text
current_base_sha == frozen_base_sha
current_head_sha == frozen_head_sha
```

If either comparison fails:

```text
SUBJECT MOVED
```

Do not issue `READY` or any other assurance verdict for the old subject, and do
not reuse the old verdict.

### Why base movement matters

A PR can be retargeted or its parent/base branch can move while the head SHA
remains identical. That changes `base SHA -> head SHA` and therefore can change:

- the actual diff;
- changed-file set;
- inherited semantics;
- integration context.

Thus identical head SHA alone does not prove an identical assurance subject. Any
base or head movement changes the frozen comparison subject. A base retarget,
base branch advance, semantic no-op commit, merge-only sync, or evidence-only
source commit still invalidates the frozen subject.

### Historical assurance after synchronization

Old assurance can still explain prior findings or prove a defect existed, but it
must be labeled historical. New synchronization/correction requires fresh
applicable assurance where the governance profile requires it.

## 7. CI Evidence: PR Merge Ref vs Standalone Head

GitHub pull-request workflows often run against a synthetic merge ref that
combines the PR head with its base. This is valuable **integration evidence**, but
it is not identical to executing a detached standalone child head.

When reporting evidence, distinguish:

```text
PR merge-ref/integration CI
standalone detached-head CI
```

Do not claim detached-head execution unless that is what the workflow actually
checked out. For most PR integration decisions, merge-ref CI is expected and
useful; the distinction matters when an assurance claim specifically binds to a
standalone SHA.

## 8. Evidence Must Not Self-Invalidate

Avoid writing a statement such as:

```text
validated_revision: <current HEAD>
```

into a normative file on that same branch as the final validation step. Updating
the file creates a new commit, so `<current HEAD>` immediately becomes the
previous head.

Prefer:

- immutable baseline/input revisions inside normative plans when needed;
- exact current provider/head SHA in PR metadata, CI artifacts, or external
  evidence tied to that run;
- a closeout report only when its governing lifecycle intentionally includes the
  report itself in the final frozen subject and renewed assurance follows.

A file cannot stably certify its own current commit SHA without an external
anchoring mechanism.

## 9. GitHub Contents API No-Op Commit Hazard

Do not use a repository file update as a harmless way to refresh metadata or
"touch" evidence. Some GitHub content-update paths can create a new commit even
when the resulting blob/content is unchanged from the previous file version.

Consequences:

- PR head moves;
- prior frozen assurance becomes stale;
- CI reruns;
- exact-head statements in PR descriptions become outdated.

For PR title/body/base/state changes, use PR metadata operations. Do not rewrite a
repository file unless repository content actually needs to change.

Before any content update, compare the intended bytes/semantic change with the
current file and skip the write if there is no real repository delta.

## 10. Git Tree File Modes Matter

A blob SHA identifies file content, not its executable mode. When constructing a
Git tree directly, preserve each path's mode from the source/new parent tree:

```text
100644 regular file
100755 executable file
040000 tree
```

Accidentally writing a validator or shell script with the wrong mode creates a
real Git diff even if the blob bytes are correct.

Inspect tree metadata before creating a resolved tree when executable files are
in scope.

## 11. PR Metadata vs Repository Mutation

PR metadata operations such as changing:

- title;
- description/body;
- base branch;
- Draft/Ready state;
- reviewers/labels;

normally do **not** create a repository commit and therefore do not move the PR
head SHA.

Repository content operations, merges, commits, ref updates, and conflict
resolutions do move or replace Git subjects.

Use PR metadata for dynamic status/evidence summaries when appropriate, and keep
normative repository files for durable project state rather than volatile
provider observations.

## 12. Post-Sync Checklist

For every synchronized stack layer verify:

```text
[ ] old child head recorded
[ ] exact new parent head recorded
[ ] synchronization is non-destructive
[ ] merge commit has old child + new parent ancestry
[ ] new parent -> new child changed-file set inspected
[ ] accepted parent semantics preserved on overlapping files
[ ] no unrelated parent/root surfaces leaked into child delta
[ ] local verification passed before remote ref movement
[ ] remote child still matched recorded C0 before update
[ ] branch ref advanced with force disabled
[ ] PR base/head metadata matches intended stack
[ ] old frozen assurance labeled historical
[ ] fresh CI/assurance scheduled when required
[ ] no default-branch merge/release performed without applicable authority
```

For multi-layer stacks, only continue to the next child after the current layer
passes this checklist.

## 13. When to Stop

Return to Define/Owner decision instead of "resolving" automatically when:

- parent and child contain materially conflicting product/governance intent;
- preserving the child would undo a newly accepted authority or security model;
- synchronization needs a scope expansion beyond the child Work Block;
- the remote child head moved unexpectedly;
- a force-push/history rewrite appears necessary;
- the intended child delta cannot be distinguished from stale inherited changes;
- an external merge/protected-branch action lacks explicit authority.

The purpose of this procedure is to preserve **intent, history, and evidence
integrity**. It is not to make Git history aesthetically linear.
