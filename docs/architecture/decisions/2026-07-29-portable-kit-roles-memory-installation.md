---
schema_version: 1
artifact_type: architecture_decision
artifact_id: 2026-07-29-portable-kit-roles-memory-installation
status: proposed
created_at: 2026-07-29
source_framework_revision: 0fce7389d27690482e910e942a1f3138c2fef123
---

# ADR — Portable Roles, Memory, Candidate, and Installation

## Context

The portable product requires concrete decisions for role packaging, committed
versus local state, concurrent writes, candidate isolation, and installation into
both new and existing repositories. Leaving these as equal alternatives would
allow candidate implementations to recreate provider-specific agents, move
canonical memory into runtime-local directories, or overwrite project files.

## Decision

### Separate role contracts

The kit contains separate files:

```text
agentic/roles/
├── README.md
├── orchestrator.md
├── architect.md
├── critic.md
├── coder.md
├── reviewer.md
└── verifier.md
```

Root `AGENTS.md` remains canonical for shared authority, Hard Stops,
source-of-truth order, and lifecycle invariants. Role files contain only purpose,
authority, prohibited actions, required inputs, procedure, output, stop
conditions, and handoff. They do not contain model, runtime, tool, provider, or
plugin configuration.

A single consolidated `roles.md` is rejected because it weakens progressive
disclosure, makes role-specific handoff harder, and encourages runtimes to load
unrelated authority descriptions.

### Canonical committed memory

Canonical project memory is committed at:

```text
memory_bank/
├── context.md
├── progress.md
├── decisions.md
├── orchestrator-log.md
├── review-log.md
└── snapshots/
```

`memory_bank/` stores concise project state, progress, accepted decisions,
coordination events, assurance outcomes, and conditional context snapshots. It
must remain sufficient to reconstruct current accepted project state without
provider memory or chat history.

Runtime-local scratch, caches, raw transcripts, temporary traces, downloads, and
tool output use ignored `.agentic-local/`. They are noncanonical, disposable,
and prohibited from carrying the only copy of an accepted decision or required
evidence.

Moving canonical memory under a generic `project/` directory or a provider/runtime
directory is rejected. `memory_bank/` is the stable cross-runtime contract and
preserves compatibility with the proven practical framework.

### One write Work Block per working tree

Each working tree permits one active write-capable Work Block. Multiple read-only
discovery Work Blocks may coexist. Parallel write Work Blocks require isolated
worktrees or clones, and each isolated tree still has one writer Work Block.
Parallel write-sets must be non-overlapping or governed by an explicit integration
plan. Exactly one Coder owns a write-set.

This rule is enforced by process artifacts, not by required hooks or runtime
capability negotiation.

### Candidate isolation and promotion

Candidate implementation is isolated at:

```text
candidate/portable-agentic-sdlc-kit/
├── CANDIDATE.md
├── template/
├── tools/
└── tests/
```

The candidate is noncanonical until synthetic dry-run and HardwareLab pilot
evidence pass and the Owner explicitly approves promotion. The promoted canonical
location is `portable-agentic-sdlc-kit/`. Superseded framework material is
archived under `archive/legacy-control-plane/` with provenance rather than
silently deleted.

### Generic collision-safe installer

The candidate installer exposes:

```text
install.py plan --target <repository>
install.py apply --target <repository>
```

`plan` is mandatory and nonmutating. It resolves the target root, checks path and
symlink safety, inventories candidate paths, and reports `create`,
`skip-identical`, `collision`, or `blocked` for every action.

`apply` revalidates the plan, stages changes, creates only planned files, refuses
unresolved collisions, never silently overwrites or deletes, and reports
`created`, `skipped`, `colliding`, and `blocked` results. `.gitignore` changes are
bounded and collision-aware.

The installer creates no runtime agents, hooks, plugins, MCP configuration,
provider directories, model routing, capability profiles, or duplicated skill
mirrors.

### Acceptance-state transition

This ADR remains `proposed` while PR #12 awaits required assurance and Owner
approval. A proposed ADR is not accepted merely because a pull request exists, a
review is recorded, or a CI run is green. After review and verification are
`READY`, the Owner may approve integration. Before merge, its frontmatter must
be changed to the project's accepted status; the status-only finalization commit
must be included in the final verification subject. Merge of this file while it
is still marked `proposed` does not silently make the decision accepted.

## Rationale

Separate roles allow the same portable contracts to be routed to native
subagents, sequential passes, or manual handoffs. Canonical committed memory
preserves durable state. A distinct ignored local path prevents operational noise
and sensitive traces from contaminating project knowledge. One writer per tree
avoids implicit conflict resolution. Candidate isolation prevents draft content
from becoming authoritative through mere presence. A plan/apply installer is the
minimum safe interface for existing repositories.

## Rejected Alternatives

### One `roles.md`

Rejected because it over-consolidates role contracts and impairs bounded loading
and handoff.

### Provider-specific role mirrors

Rejected because mirrors drift and make provider layout part of the product.

### Runtime-local memory as the primary memory

Rejected because it is not portable, inspectable, or reliably committed.

### Store raw transcripts in `memory_bank/`

Rejected because transcripts are noisy, may contain sensitive information, and
are not a stable project source of truth.

### Multiple write Work Blocks in one tree

Rejected because file ownership and final assurance become ambiguous even when
agents intend to edit different areas.

### Copy-over installer

Rejected because silent overwrite is unsafe for existing projects and provides
no reviewable plan.

### Make the candidate canonical immediately

Rejected because normative architecture, packaging, synthetic safety tests, and a
real-project pilot must precede promotion.

## Consequences

- Projects receive explicit role and memory boundaries without requiring runtime
  features.
- Installer complexity is higher than a simple copy command but collisions and
  path safety become observable.
- Parallel implementation requires worktree/clone isolation managed outside the
  core kit or through an optional extension.
- Candidate and legacy paths coexist temporarily during migration, with exactly
  one operational baseline identified at each stage.
- Local runtime configuration remains possible but is deliberately unmanaged.

## Review Triggers

Review this decision when:

- a role requires authority not representable through `AGENTS.md` plus the role
  schema;
- pilot evidence shows canonical memory cannot remain concise and complete;
- installer safety requires a new mutation class;
- a proposed concurrency model allows shared-tree parallel writers;
- promotion or archival would create more than one canonical source of truth.
