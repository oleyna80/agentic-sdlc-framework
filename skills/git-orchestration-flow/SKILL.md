---
name: git-orchestration-flow
description: Safe procedures for Git branch management, stacked PR synchronization, frozen-subject assurance, worktree isolation, two-pass Work Block closure projections, GitHub ruleset handling, PR thread resolution, and SSOT conflict resolution. Use when managing complex Git flows, worktrees, stacked PRs, PR merge blockers, frozen heads, or SSOT reconciliations.
---

# Git Orchestration Flow

Procedural guide for managing Git branches, worktrees, PR lifecycles, stacked
changes, frozen assurance subjects, and SSOT file reconciliations within an
agentic SDLC framework.

## 1. Worktree Isolation & Cleanup

### Rule
When delegating work to isolated subagents or parallel streams, use dedicated worktrees or clones. Never attempt to delete a branch currently checked out in an active worktree.

### Procedures

#### Detaching HEAD before Branch Deletion
If a branch cannot be deleted because it is checked out in a worktree:
```bash
git checkout --detach origin/main
git branch -d <branch-name>
```

#### Pruning Worktrees
To forcibly remove a completed or obsolete worktree:
```bash
git worktree remove /path/to/worktree --force
git worktree prune
```

---

## 2. Two-Pass Closure Projection Pipeline

### Rule
Finalizing a Work Block changes normative surfaces (`status: completed`, `active_work_block: null`), which alters SHA-256 aggregates. To preserve independent assurance integrity, use a two-pass sequence.

### Procedures

1. **Preliminary Candidate Assurance:**
   Compute the aggregate on the active candidate state and run independent preliminary assurance (Reviewer, Verifier, Drift Analyst).

2. **Ephemeral Projection:**
   Create an ephemeral non-repository projection to verify terminal state:
   ```bash
   cp -r . /tmp/wb-final-projection/
   # Edit /tmp/wb-final-projection/ files to project completed/no-active state
   ```

3. **Preflight Assurance:**
   Run preflight assurance against the ephemeral projection directory.

4. **Working Tree Application:**
   Apply the byte-equivalent projection changes to the working tree, re-verify deterministic checks, and commit.

---

## 3. GitHub PR Thread Resolution & Ruleset Handling

### Rule
GitHub repository rulesets (`required_review_thread_resolution: true`) block PR merges even when all CI checks pass if unresolved review comments exist (including outdated comments).

### Procedures

#### Inspecting PR Blockers
Check PR merge state and review threads:
```bash
gh pr view <pr-number> --json mergeStateStatus,mergeable,reviewDecision
```

#### Finding Unresolved Threads via GraphQL
```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 20) {
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 1) { nodes { body } }
        }
      }
    }
  }
}'
```

#### Resolving Outdated Threads
Resolve threads that have been addressed or invalidated by newer commits:
```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) {
    thread { id isResolved }
  }
}'
```

---

## 4. SSOT File Conflict Resolution (Rebase Pattern)

### Rule
When a rebase is intentionally selected for a simple feature branch, conflicts in
`FILE_REGISTRY.yml` and `PROJECT_MAP.md` must be reconciled without losing
historical completed Work Blocks or overwriting active state.

Do **not** default to this rebase pattern for already-reviewed stacked PRs where
preserving ancestry, frozen-subject evidence, and review history matters. Use the
stacked synchronization procedure in Section 5 instead.

### Procedures

#### Reconciling `FILE_REGISTRY.yml`
- Retain all historical completed Work Blocks in `completed_work_blocks`.
- Set `active_work_block` to the current active plan (or `null` if closing).
- Retain all new file entry definitions (`entries:`).

#### Reconciling `PROJECT_MAP.md`
- Preserve the completed Work Block list in both HTML comment blocks and human-readable text.
- Maintain accurate architectural decision references.

#### Rebase Continuation
After editing conflict markers:
```bash
git add FILE_REGISTRY.yml PROJECT_MAP.md
GIT_EDITOR=true git rebase --continue
```

---

## 5. Stacked PR Synchronization & Frozen Assurance

### Rule
When a child PR was built on another feature branch and its parent moves or lands,
synchronize the stack **bottom-up** and preserve the child's still-valid semantic
delta on top of the new accepted parent.

Default to a non-destructive two-parent merge plus a non-force branch update when
review/history preservation matters. After every layer, verify the exact
`new_parent → new_child` diff before continuing upward.

Do not restore an old whole-file child version over newly accepted parent
architecture merely to avoid conflict resolution. Accepted parent semantics win;
reapply only the child behavior that remains in scope.

Frozen assurance is SHA-bound. If the PR head moves, report `SUBJECT MOVED` and
renew applicable assurance. Do not treat old CI/review as evidence for a new head
without explicitly labeling it historical.

Detailed algorithm, Git-object-database variant, CI evidence boundaries, file-mode
rules, and observed GitHub API failure modes:

`reference/stacked-pr-synchronization.md`

### Minimum post-sync checklist

- record old child and exact new parent heads;
- preserve two-parent ancestry;
- advance branch ref with force disabled;
- inspect `new_parent → new_child` changed files and semantics;
- verify accepted parent/root surfaces did not leak back into the child;
- distinguish PR merge-ref CI from detached-head execution evidence;
- avoid normative self-reference to the file's own current head SHA;
- use PR metadata operations for PR body/title/base changes instead of no-op file writes;
- renew required frozen-subject assurance after head movement;
- never merge/default-branch mutate without the applicable Owner/repository authority.
