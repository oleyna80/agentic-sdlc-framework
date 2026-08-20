# Stacked PR Synchronization Supporting Reference

This reference supplies terminology, examples, and evidence-recording context
for the executable workflow in [`../SKILL.md`](../SKILL.md). It does not define
execution order, decision authority, or hard stops.

## Terminology

| Symbol | Meaning |
| --- | --- |
| `P0` | old parent head/base |
| `C0` | old child head |
| `P1` | new accepted or synchronized parent head |
| `C1` | synchronized child head |
| `intent_delta` | still-valid semantic delta represented by `P0 -> C0` |

The target tree relationship is:

```text
intent_delta = semantic delta of P0 -> C0
C1 tree      = P1 tree + still-valid intent_delta
C1 parents   = [C0, P1]
```

For a three-layer stack, the dependency shape is:

```text
main
  └─ A
      └─ B
          └─ C
```

## Conflict-classification examples

| Classification | Illustrative condition | Resulting semantic treatment |
| --- | --- | --- |
| child-only | Parent did not materially change the path | Child change remains applicable |
| parent-overlap, additive | Parent changed a path and the child retains a compatible need | The accepted parent version gains only the compatible child behavior |
| parent supersedes child | Accepted parent semantics replace an old child representation | The old representation is not restored |
| uncertain/material conflict | Resolving overlap changes requirement, architecture, authority, or scope | Historical examples record an Owner/Define decision |

Example of parent-first resolution:

```text
Old child: detailed lifecycle prose in AGENTS.md
New parent: accepted compact AGENTS.md plus workflow routing
Surviving child intent: lifecycle detail remains useful
```

The compatible end state retains the compact parent contract and places the
surviving detail in its workflow/skill owner. Restoring the old complete file
would discard accepted parent architecture.

## Git-object construction model

In an object-database environment, the synchronized result can be represented
without moving a branch ref:

```text
T1 = tree(base=P1.tree, overlays=resolved_child_delta)
C1 = commit(tree=T1, parents=[C0, P1])
```

The tree describes the intended parent baseline plus child delta; the two
parents preserve both the child’s history and the synchronization event.

## Evidence distinctions

| Evidence type | What it demonstrates | What it does not establish |
| --- | --- | --- |
| `P1 -> C1` local comparison | Resulting child delta and inherited-surface integrity | Provider CI status |
| PR merge-ref CI | Integration of the PR head with its base | Detached standalone-head execution |
| Detached-head CI | Execution of that exact checked-out SHA | PR merge-ref integration unless separately run |
| Historical review/verification | Facts about its recorded base/head pair | Assurance for a later base or head |
| PR metadata update | Provider-side title/body/base/reviewer state | Repository-content mutation or new commit |
| Contents API update | Repository-content operation | A guaranteed no-op, even if bytes appear unchanged |

A frozen assurance subject is always recorded as:

```text
frozen_base_sha -> frozen_head_sha
```

Both values identify the comparison. An unchanged head with a changed base is a
different subject.

## Evidence-record examples

### Synchronization record

```text
old_parent: <P0>
old_child: <C0>
new_parent: <P1>
new_child: <C1>
changed_paths_p1_to_c1: [<path>, ...]
ancestry: [<C0>, <P1>]
remote_update: non-force
```

### Assurance record

```text
subject: <base SHA> -> <head SHA>
ci_kind: merge-ref | detached-head
historical: true | false
verdict: READY | BLOCKED | UNVERIFIED | SUBJECT MOVED
```

### File-mode reference

| Mode | Meaning |
| --- | --- |
| `100644` | regular non-executable file |
| `100755` | executable file |
| `040000` | tree |

Blob identity covers bytes but not the executable mode. Direct tree construction
therefore needs mode data from the relevant parent/source tree.

## Failure-pattern examples

- A no-op Contents API update creates a new commit, making prior exact-head
  evidence historical.
- A PR retarget produces a visually clean comparison while inherited parent
  semantics remain absent from the child tree.
- An old whole-file conflict choice reintroduces parent behavior that had already
  been accepted or superseded.
- A matching child head is treated as unchanged despite a different base SHA.

These patterns are examples of evidence or semantic drift, not alternative
execution paths.
