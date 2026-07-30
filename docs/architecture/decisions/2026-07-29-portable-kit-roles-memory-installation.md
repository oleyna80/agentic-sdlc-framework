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
versus local state, concurrent writes, candidate isolation, installation into
new and existing repositories, and assurance evidence identity. Equal
alternatives would permit provider-specific role mirrors, runtime-local
canonical memory, unsafe overwrites, ambiguous assurance subjects, or mutable
assurance state in normative navigation.

## Decision

### Separate role contracts

The kit contains:

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

### Role-specific verdict vocabularies

- Critic: `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, `BLOCKED`.
- Reviewer: `READY`, `CHANGES_REQUIRED`, `BLOCKED`, `UNVERIFIED`.
- Verifier: `READY`, `NOT_READY`, `BLOCKED`, `UNVERIFIED`.

Reviewer `READY` means no unresolved blocking finding;
`CHANGES_REQUIRED` requires correction and re-review; `BLOCKED` means required
subject, authority, access, or evidence is unavailable; `UNVERIFIED` means
coverage is insufficient.

Verifier `READY` means fresh evidence demonstrates every required acceptance
criterion; `NOT_READY` means one or more criteria fail; `BLOCKED` means a
required procedure cannot run; `UNVERIFIED` means evidence is absent or
insufficient. Historical verdicts remain unchanged.

### Canonical committed memory

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
coordination events, assurance outcomes, exact normative-subject identities, and
conditional context snapshots. Runtime-local scratch, caches, raw transcripts,
temporary traces, downloads, and tool output use ignored `.agentic-local/`.
They are noncanonical and cannot carry the only copy of an accepted decision or
required evidence.

### One write Work Block per working tree

Each working tree permits one active write-capable Work Block. Multiple
read-only discovery Work Blocks may coexist. Parallel write Work Blocks require
isolated worktrees or clones, and each isolated tree still has one writer Work
Block. Parallel write-sets must be non-overlapping or governed by an explicit
integration plan. Exactly one Coder owns a write-set.

### Candidate isolation and promotion

```text
candidate/portable-agentic-sdlc-kit/
├── CANDIDATE.md
├── template/
├── tools/
└── tests/
```

The candidate is noncanonical until synthetic dry-run and HardwareLab pilot
evidence pass and the Owner explicitly approves promotion. The promoted
canonical location is `portable-agentic-sdlc-kit/`. Superseded material is
archived under `archive/legacy-control-plane/` with provenance rather than
silently deleted.

### Generic collision-safe installer

```text
install.py plan --target <repository>
install.py apply --target <repository>
```

`plan` is mandatory and nonmutating. It resolves the target root, checks path and
symlink safety, inventories candidate paths, and reports `create`,
`skip-identical`, `collision`, or `blocked`.

`apply` revalidates the plan, stages changes, creates only planned files, refuses
unresolved collisions, never silently overwrites or deletes, and reports
`created`, `skipped`, `colliding`, and `blocked`. The installer creates no
runtime agents, hooks, plugins, MCP configuration, provider directories, model
routing, capability profiles, or duplicated skill mirrors.

### Normative subject and evidence-only commits

The normative subject is the exact commit or artifact revision containing the
applicable specification, ADRs, Work Block, authoritative plans/tasks, normative
navigation/registry content, delivered artifact, and proposed-to-accepted status
changes. Reviewer and Verifier reports identify that exact subject.

An evidence-only commit changes only approved assurance or closeout report paths.
It may follow the normative subject, does not invalidate the verdict it records,
and must contain no hidden normative changes. CI and structural checks run on
the resulting PR head.

Navigation and registry are normative only for authority, architecture,
canonical path ownership, active lifecycle state, and accepted/proposed status.
They must not mirror mutable assurance verdicts, subjects, findings, coverage,
limitations, or another-pass state.

Reports require no per-report registration in normative files. They are
discovered through canonical evidence directories and structured frontmatter.
A static directory classification is normative but does not change for each
report. Verdict history is reconstructed from report artifacts.

Any applicable normative-subject change invalidates prior readiness. A report
correction remains evidence-only only when verdict, subject, scope, procedures,
results, coverage, and limitations are unchanged.

### Acceptance-state transition

This ADR remains `proposed` while required assurance and Owner approval are
pending.

```text
preliminary Reviewer and Verifier assurance
  → Owner authorizes accepted-status finalization
  → status-only normative commit
  → final Reviewer/Verifier assurance against that normative subject as required
  → evidence-only report commit
  → CI on the resulting PR head
  → separate Owner merge approval
```

Before merge, frontmatter must be changed to the project's accepted status. The
status-only commit is part of the normative subject. The report may follow as
evidence-only and does not need to be contained in the commit it evaluates.
Merge while still `proposed` does not silently accept the decision.

## Rationale

Separate roles enable bounded loading and handoff. Role-specific verdicts
separate design criticism, review readiness, and verification results.
Committed memory preserves durable state; `.agentic-local/` contains disposable
noise. One writer per tree prevents implicit conflict resolution. Candidate
isolation avoids accidental authority. A plan/apply installer is the minimum
safe existing-repository interface. Static evidence discovery prevents mutable
assurance state from recursively changing its normative subject.

## Rejected Alternatives

- One consolidated `roles.md`: weakens progressive disclosure and handoff.
- Shared verdict vocabulary: conflates distinct assurance decisions.
- Provider-specific role mirrors: drift and make provider layout part of product.
- Runtime-local canonical memory: not portable or reliably committed.
- Raw transcripts in `memory_bank/`: noisy and potentially sensitive.
- Multiple write Work Blocks in one tree: ambiguous ownership and assurance.
- Copy-over installer: unsafe silent overwrite.
- Immediate candidate promotion: bypasses architecture, tests, and pilot.
- Report inside its verified commit: circular.
- Per-report navigation entries: create mutable normative churn and invalidate
  assurance.

## Consequences

- Projects receive explicit role and memory boundaries without runtime features.
- Installer complexity is higher but collisions and path safety are observable.
- Parallel implementation requires external worktree/clone isolation.
- Candidate and legacy paths coexist temporarily with one operational baseline.
- Assurance reports may follow the verified subject without changing it.
- Evidence consumers enumerate canonical report directories and parse
  frontmatter rather than consulting mutable navigation pointers.

## Review Triggers

Review this decision when:

- a role needs authority not representable through `AGENTS.md` plus role schema;
- a role requires a verdict outside its vocabulary;
- canonical memory cannot remain concise and complete;
- installer safety requires a new mutation class;
- concurrency permits shared-tree parallel writers;
- assurance tooling cannot distinguish normative from evidence-only commits;
- normative navigation mirrors mutable assurance state;
- promotion or archival creates more than one canonical source of truth.
