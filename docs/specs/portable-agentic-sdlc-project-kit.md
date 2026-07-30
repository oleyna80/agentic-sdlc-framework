---
schema_version: 1
artifact_type: normative_specification
artifact_id: portable-agentic-sdlc-project-kit
status: proposed
owner_role: owner
created_at: 2026-07-29
source_framework_revision: 0fce7389d27690482e910e942a1f3138c2fef123
historical_framework_revision: 0c632db0b0444e556251c384f6254141c9df59bc
superpowers_reference_revision: 44c9b2d6e889982ac18c27d05a19fefe335194e1
---

# Portable Agentic SDLC Project Kit

## 1. Purpose

Define a portable, repository-local Agentic SDLC Project Kit. The cited framework
revisions are evidence, not runtime authority. This specification remains
`proposed` until the section 10 acceptance transition is complete.

## 2. Product Boundary

The product is a complete project kit, not a skills library and not a runtime
control plane. It contains root `AGENTS.md`, lifecycle/process contracts, role
contracts, procedural skills, Work Blocks, specifications, ADRs, plans, tasks,
mission briefs, handoffs, memory, assurance reports, closeout, and a collision-safe
installer contract.

Portable paths include `agentic/roles/`, `agentic/skills/`,
`agentic/templates/`, `docs/`, `memory_bank/`, and ignored `.agentic-local/`.
The kit does not own provider agents, model routing, hooks, runtime permissions,
MCP, plugins, provider profiles, queues, daemons, transports, or runtime-specific
conformance state.

## 3. Design Principles

1. Artifacts are the interoperability boundary.
2. Accepted contracts, not runtimes or models, define authority.
3. Process cost follows risk and ambiguity.
4. Fresh evidence precedes readiness and completion claims.
5. One Coder owns one write-set.
6. Canonical memory is concise, durable, and secret-free.
7. Runtime neutrality means non-ownership of runtime concerns.
8. Missing required assurance fails closed as `BLOCKED` or `UNVERIFIED`.
9. Installation never silently overwrites.
10. Candidate evidence and Owner approval precede promotion.
11. Assurance binds to an exact normative subject.
12. Evidence-only commits may follow the subject they evaluate.
13. Mutable assurance state lives in reports, not normative navigation.

## 4. Source of Truth

Conflicts resolve in this order:

1. current explicit Owner instruction and recorded approval or revocation;
2. root `AGENTS.md`;
3. approved specification and accepted ADRs;
4. active Work Block;
5. approved implementation plan and tasklist;
6. mission brief;
7. frozen implementation diff or final artifact;
8. Critic, Reviewer, Verifier, evaluation, and closeout reports;
9. `memory_bank/`;
10. `.agentic-local/`, generated notes, caches, and external references.

The Work Block binds objective, scope, write-set, process level, role authority,
Hard Stops, approvals, acceptance, and assurance. Plans/tasks cannot expand it;
mission briefs cannot expand the Work Block or plan. Material change returns to
Define and requires Work Block revision.

## 5. Lifecycle

```text
Intake/classify
  → Define: discovery, architecture, specification, plan/tasks, Critic
  → Execute: bounded implementation and self-checks
  → Assure: Reviewer and Verifier against an exact normative subject
  → Owner-authorized status finalization when applicable
  → final applicable assurance
  → evidence-only report commit
  → CI on resulting PR head
  → Close: SSOT/memory sync and truthful closeout
  → separate Owner-controlled integration
```

A report may follow the exact subject it evaluates; it need not be contained in
that subject commit.

## 6. Process Levels

**Quick** requires a compact Work Block, scope/write-set, acceptance, fresh
verification, and closeout. Critic and separate Reviewer are normally optional.

**Standard** requires specification/change contract, material ADRs, plan/tasks as
needed, Critic, Coder, Reviewer, Verifier, closeout, and memory synchronization.

**High-Risk** adds threat/risk assessment, rollback, positive/negative cases,
required independence, explicit Owner approvals, and optional domain evaluation.
Triggers include production mutation, secrets/permissions, destructive actions,
live data, consequential communications/transactions, security boundaries, and
material legal/privacy/financial risk.

## 7. Logical Roles

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

Shared authority and Hard Stops remain canonical in `AGENTS.md`.
Orchestrator frames/routes/closes; Architect discovers and designs; Critic
challenges Define-stage assumptions; Coder changes one approved write-set;
Reviewer inspects an exact normative subject without editing it; Verifier maps
fresh evidence to acceptance without repairing the subject.

## 8. Role Execution Modes

Native subagents, sequential single-agent passes, and manual copy/paste handoffs
are supported. The Orchestrator supplies role, Work Block, inputs, scope,
write-set, prohibited actions, output, and stop conditions. Sequential reuse is
disclosed as non-independent assurance.

## 9. Work Blocks and Concurrency

A Work Block records identity, objective, process level, source contracts,
scope/out-of-scope, write-set, roles, side effects, risks, Hard Stops, approvals,
acceptance, assurance, rollback, and gate state.

One write-capable Work Block is active per working tree. Parallel writers require
isolated worktrees/clones and non-overlapping write-sets or an explicit integration
plan. Exactly one Coder owns each write-set; a shared file makes sets overlap.

## 10. Specifications and Architecture Decisions

Specifications define behavior, constraints, failures, acceptance, and non-goals.
ADRs define material structural choices, rationale, rejected alternatives,
consequences, and review triggers.

### Normative subject

The normative subject is the exact commit or artifact revision containing every
applicable final authority-bearing or delivered surface:

- specification and ADRs;
- active Work Block;
- authoritative plans/tasks;
- normative navigation/registry content;
- implementation or other delivered artifact;
- proposed-to-accepted status changes.

Navigation/registry belong to the subject only for authority, architecture,
canonical path ownership, active lifecycle state, or accepted/proposed status.
Changes to those are normative. Mutable assurance progress is not.

### Evidence-only commits and discovery

An evidence-only commit changes only approved assurance or closeout report paths.
Rules:

1. Reviewer and Verifier reports identify the exact normative-subject SHA.
2. Applicable normative-subject changes invalidate prior readiness.
3. An evidence-only commit does not invalidate the verdict it records.
4. Evidence-only commits may follow the verified subject in the final PR head.
5. CI and structural checks pass on the resulting PR head.
6. Evidence-only commits contain no hidden normative change.
7. Wording/metadata-only report corrections remain evidence-only only when verdict,
   subject, scope, procedures, results, coverage, and limitations are unchanged.
8. Changes to verdict, subject, coverage, result, or limitation require renewed
   assurance as applicable.

Mutable verdicts, reviewed/verified SHAs, findings, coverage, limitations, and
another-pass state are prohibited from normative navigation. Reports require no
per-report map/registry entry. They are discovered by canonical paths and
structured frontmatter:

```text
docs/reports/reviews/
docs/reports/verification/
docs/reports/evaluations/
docs/reports/closeout/
```

A static directory-class entry is normative classification but does not change
for each report. Adding a report-only commit requires no navigation update.
Verdict history is reconstructed from report artifacts. Indexing grants no
authority.

### Acceptance-state transition

```text
preliminary Reviewer and Verifier assurance
  → Owner authorizes accepted-status finalization
  → status-only normative commit
  → final Reviewer/Verifier assurance against that subject as required
  → evidence-only report commit
  → CI on resulting PR head
  → separate Owner merge approval
```

`proposed` artifacts are not accepted by PR existence, review, CI, or merge.
Before merge, accepted artifacts receive the project's accepted frontmatter status.

## 11. Plans and Task Decomposition

Plans map accepted requirements to paths, dependencies, checks, risks, rollback,
and handoffs. Tasks name inputs, write-set, owner, result, verification, and stop
conditions. Neither may expand the active Work Block.

## 12. Skills and Routing

Skills are procedures, not authority. Core skills are:

| Skill | Purpose |
|---|---|
| `technical-discovery` | inventory current code, contracts, dependencies, and side effects |
| `architecture-discovery` | evaluate component, authority, data, install, and migration boundaries |
| `specification` | define behavior, constraints, failures, acceptance, and non-goals |
| `implementation-planning` | map accepted requirements to ordered work and checks |
| `task-decomposition` | create bounded, verifiable tasks and handoffs |
| `systematic-debugging` | reproduce, isolate, test hypotheses, fix within scope |
| `memory-bank-manager` | synchronize concise durable memory |
| `ssot-sync-closeout` | reconcile artifacts, state, evidence, and follow-ups |
| `verification-before-completion` | obtain fresh criterion-mapped evidence before readiness claims |

Skills cannot expand role, scope, write-set, side effects, Hard Stops, or approval.

## 13. Mission Briefs and Handoffs

A mission brief contains Work Block/role, objective, inputs, authority, read scope,
write-set, Hard Stops, skills, acceptance, verification, stop conditions, and
return format. It cannot expand the Work Block or plan. Handoffs record completed
work, evidence, deviations, blockers, and next authorized role.

## 14. Project Memory and Logs

Canonical committed memory is:

```text
memory_bank/
├── context.md
├── progress.md
├── decisions.md
├── orchestrator-log.md
├── review-log.md
└── snapshots/
```

Reports remain the source for verdict, subject, scope, findings, coverage,
results, and limitations. `review-log.md` may index report paths without replacing
reports or becoming normative navigation. Raw transcripts, scratch, caches, and
tool output belong in ignored `.agentic-local/`.

## 15. Review

Critic verdicts: `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, `BLOCKED`.

Reviewer verdicts:

- `READY`: no unresolved blocking review finding;
- `CHANGES_REQUIRED`: corrections must be completed and re-reviewed;
- `BLOCKED`: required subject, authority, access, or evidence is missing;
- `UNVERIFIED`: coverage is insufficient for a readiness judgment.

Review reports record exact subject, scope, procedures, findings, coverage,
limitations, verdict, and handoff. Historical verdicts are not rewritten.

## 16. Verification

Verifier verdicts:

- `READY`: fresh evidence demonstrates every required criterion;
- `NOT_READY`: evidence demonstrates one or more criteria fail;
- `BLOCKED`: a required procedure cannot run because authority, environment,
  dependency, or access is unavailable;
- `UNVERIFIED`: required evidence is absent or insufficient.

Verification reports record exact subject, criterion, procedure, expected/actual,
status, coverage, limitations, verdict, and residual risk.

## 17. Closeout

Successful closeout requires in-scope delivery, required Reviewer `READY`,
Verifier `READY`, required Owner approvals, synchronized normative artifacts and
memory, disclosed residual risks, bounded follow-ups, and green CI on the
resulting PR head. Incomplete, blocked, `CHANGES_REQUIRED`, `NOT_READY`, or
`UNVERIFIED` work cannot claim success.

## 18. Git and Owner Approval Boundaries

Owner approval is required for default/protected-branch merge or direct push,
production deployment/restart, secrets/permissions, destructive operations, live
data mutation, consequential communications/transactions, and material scope or
architecture expansion. Feature-branch commits, PR updates, checks, and approved
evidence artifacts are allowed within the Work Block. None grants merge authority.

## 19. Installation

```text
install.py plan --target <repository>
install.py apply --target <repository>
```

`plan` is mandatory and nonmutating; it checks root/path/symlink safety and
classifies `create`, `skip-identical`, `collision`, or `blocked`. `apply`
revalidates, stages, creates only planned files, refuses unresolved collisions,
and never silently overwrites, merges, or deletes. It creates no runtime agents,
hooks, plugins, MCP, provider directories, routing, profiles, or mirrors.

## 20. Optional Extensions

Optional, non-core capabilities include nondeterministic evaluation, advanced
security tooling, browser/UI testing, worktree automation, PR finishing,
external-model review, provenance tooling, MCP, plugins, hooks, runtime profiles,
queues, daemons, and provider adapters. Extensions cannot redefine core authority.

## 21. Candidate and Promotion Model

Candidate content lives under `candidate/portable-agentic-sdlc-kit/` and is
noncanonical. Promotion to `portable-agentic-sdlc-kit/` requires synthetic tests,
HardwareLab pilot, resolved blockers, accepted-status finalization, final
assurance, evidence-only reports, green CI, and explicit Owner approval.
Superseded material is archived with provenance.

## 22. Migration Sequence

- **WB-CORE-001:** normative architecture and assurance semantics; no implementation.
- **WB-CORE-002:** portable candidate roles, skills, templates, memory, and docs.
- **WB-CORE-003:** collision-safe installer and packaging.
- **WB-CORE-004:** synthetic dry-run fixtures and recovery evidence.
- **WB-CORE-005:** HardwareLab pilot without production mutation.
- **WB-CORE-006:** accepted-status promotion, one canonical entry path, and legacy archive.

Each later Work Block depends on the accepted or verified result required by its
predecessor and defines its own exact write-set, risks, checks, and out-of-scope.

## 23. Compatibility and Non-Goals

Compatibility is artifact-based across native subagents, sequential passes, and
manual handoffs. Non-goals include runtime/model/provider orchestration,
permissions/sandboxes/hooks/plugins/MCP ownership, provider mirrors, automatic
merge/deploy/live mutation/external communication, or candidate authority before
promotion.

## 24. Acceptance Criteria

- [x] Product boundary and runtime/provider exclusions are defined.
- [x] Six roles and nine skills are specified.
- [x] Work Block precedence and non-expansion rules are explicit.
- [x] Process, concurrency, memory, installer, candidate, and migration are bounded.
- [x] Role-specific verdict vocabularies are defined.
- [x] Exact normative-subject and evidence-only semantics are defined.
- [x] Mutable assurance state is prohibited from normative navigation.
- [x] Reports need no per-report map/registry registration.
- [x] Canonical evidence-path/frontmatter discovery is defined.
- [x] Proposed-to-accepted sequence is non-self-referential.
- [x] No candidate/installer/runtime implementation is included.
- [ ] A later Reviewer returns `READY` for the applicable normative subject.
- [ ] A later Verifier returns `READY` for the applicable normative subject.
- [ ] Owner authorizes status finalization and separately approves integration.

This specification remains `proposed` and does not authorize merge or promotion.
