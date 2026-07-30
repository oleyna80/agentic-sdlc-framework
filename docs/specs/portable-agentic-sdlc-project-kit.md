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

This specification defines a portable, repository-local Agentic SDLC Project
Kit. It preserves the practical lifecycle demonstrated by
`agentic-sdlc-framework@0c632db0b0444e556251c384f6254141c9df59bc`, retains useful
authority and evidence rules from
`agentic-sdlc-framework@0fce7389d27690482e910e942a1f3138c2fef123`, and adopts
selected procedural ideas from
`obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`.

Those revisions are evidence, not runtime authorities. This specification is
`proposed` until the acceptance-state transition in section 10 is completed.

## 2. Product Boundary

The product is a complete project kit, not a skills library and not a runtime
control plane. It contains:

- root `AGENTS.md` entry contract;
- SDD lifecycle and process levels;
- role contracts and procedural skills;
- Work Blocks, specifications, ADRs, plans, tasklists, mission briefs, handoffs,
  and conditional context snapshots;
- canonical committed project memory and Orchestrator/review logs;
- Critic, Reviewer, Verifier, and closeout artifacts;
- memory synchronization and collision-safe installation.

Target portable paths include `agentic/roles/`, `agentic/skills/`,
`agentic/templates/`, `docs/`, `memory_bank/`, and ignored `.agentic-local/`.

The kit must not own, require, install, generate, validate, or synchronize
`.codex/`, `.claude/`, `.opencode/`, provider-specific agents, model routing,
hooks, runtime permissions, MCP, plugins, capability negotiation, provider
snapshots, runtime profiles, duplicated skill mirrors, queues, daemons, services,
or provider transports. Project-local runtime configuration may exist
independently but cannot redefine kit authority.

## 3. Design Principles

1. Artifacts are the interoperability boundary.
2. Authority derives from accepted contracts, not tools, models, or runtimes.
3. Process cost follows risk and ambiguity, not file count.
4. Fresh evidence precedes completion and readiness claims.
5. One Coder owns one write-set.
6. Project memory is concise, durable, and secret-free.
7. Runtime neutrality means non-ownership of runtime concerns.
8. Missing required assurance fails closed as degraded, `BLOCKED`, or
   `UNVERIFIED`.
9. Installation is collision-safe and never silently overwrites.
10. Candidate evidence and Owner approval precede promotion.
11. Assurance binds to an exact normative subject, not implicitly to a mutable PR
    head.
12. Evidence-only commits may record assurance without changing the normative
    subject.

## 4. Source of Truth

Conflicts are resolved in this order:

1. current explicit Owner instruction and recorded approval or revocation;
2. root `AGENTS.md`;
3. approved specification and accepted ADRs;
4. active Work Block;
5. approved implementation plan and tasklist;
6. mission brief;
7. frozen implementation diff or final artifact;
8. Critic, Reviewer, Verifier, and closeout reports;
9. `memory_bank/`;
10. `.agentic-local/`, generated notes, caches, and external references.

The active Work Block binds the objective, scope, write-set, process level, role
authority, Hard Stops, approvals, acceptance, and assurance obligations. A plan
or tasklist may sequence and decompose but cannot expand the Work Block. A
mission brief may narrow a Work Block or plan for one handoff but cannot expand
either artifact.

A lower-ranked artifact cannot silently revise a higher-ranked artifact. Any
material change to objective, specification, architecture, scope, write-set,
process level, role authority, Hard Stops, acceptance, risk, or required
assurance returns the lifecycle to Define and requires an explicit Work Block
revision.

## 5. Lifecycle

```text
Intake and classify
  → Define: discovery, architecture, specification, plan/tasks, Critic
  → Execute: bounded implementation, self-checks, checkpoint commits, frozen diff
  → Assure: Reviewer, Verifier, fresh evidence, required independence
  → Finalize status when Owner-authorized
  → Re-assure the final normative subject as required
  → Record assurance in evidence-only reports
  → Run CI on the resulting PR head
  → Close: SSOT sync, memory sync, truthful closeout
  → Integrate: separate Owner-approved merge or other consequential action
```

Quick work may compress functions but cannot omit scope, authority, acceptance,
fresh verification, or truthful closeout. Intermediate feature-branch commits do
not require final assurance and do not constitute completion. A report commit may
follow the exact normative subject it evaluates; the report does not need to be
contained in the commit it evaluates.

## 6. Process Levels

Classification uses ambiguity, behavioral impact, architecture impact, system
boundaries, authority, side effects, reversibility, security/data risk,
verification cost, and nondeterminism. File count is secondary.

### Quick

Quick requires a compact Work Block, explicit scope/write-set, acceptance,
fresh verification, and truthful closeout. Critic and separate Reviewer are
normally optional. Verification evidence may be recorded in the Work Block.

### Standard

Standard requires an approved specification or explicit change contract, a
material ADR when needed, implementation plan, tasks when useful, Critic, Coder,
Reviewer, Verifier, closeout, and memory synchronization.

### High-Risk

High-Risk adds risk/threat assessment, rollback/recovery, positive and negative
cases, independent assurance where required, explicit Owner approvals, and
optional domain evaluation. Required unavailable independence leaves the result
`BLOCKED` or `UNVERIFIED`, not fully assured.

Mandatory High-Risk triggers include production deployment/restart, secrets or
permissions, destructive operations, live data/business mutation,
consequential external communications or transactions, security/trust-boundary
change, material legal/privacy/financial consequence, and harmful
nondeterminism.

## 7. Logical Roles

The kit specifies:

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

Shared authority and Hard Stops remain canonical in `AGENTS.md`. Each role file
contains only purpose, authority, prohibited actions, required inputs,
procedure, output, stop conditions, and handoff.

- **Orchestrator:** frames Work Blocks, routes roles, controls gates, records
  approvals/limitations, synchronizes logs, and closes work.
- **Architect:** performs discovery and drafts specifications, ADRs, and plans.
- **Critic:** challenges Define-stage assumptions, scope, risk, architecture,
  process level, and verification design.
- **Coder:** implements exactly one approved write-set without changing
  requirements or crossing Hard Stops.
- **Reviewer:** inspects an exact normative subject and records findings and a
  role-specific verdict without editing that subject.
- **Verifier:** tests acceptance against an exact normative subject and records
  fresh evidence and a role-specific verdict without repairing implementation.

## 8. Role Execution Modes

Roles must work through native subagents, sequential single-agent passes, and
manual copy-and-paste handoff. The Orchestrator provides role contract, Work
Block, inputs, scope/write-set, prohibited actions, expected output, and stop
conditions. Sequential reuse is disclosed as non-independent assurance.

## 9. Work Blocks and Concurrency

A Work Block records identifier, objective, process level, source contracts,
scope/out-of-scope, write-set, roles, side effects, risks, Hard Stops,
approvals, acceptance, assurance plan, rollback when required, and current gate
state.

1. One active write-capable Work Block per working tree.
2. Multiple read-only discovery Work Blocks may coexist.
3. Multiple write Work Blocks require isolated worktrees or clones.
4. Each isolated tree still has one active write Work Block.
5. Parallel writers require non-overlapping write-sets or an explicit integration
   plan.
6. One Coder owns each write-set.
7. A shared file makes write-sets overlap.

## 10. Specifications and Architecture Decisions

A specification defines behavior, constraints, failure states, acceptance, and
non-goals. An ADR records a material structural choice, rationale, rejected
alternatives, consequences, and review triggers. Material product, authority,
data/security, interface, installation, migration, or compatibility changes
require an ADR. Equal material alternatives must be resolved before execution.

### Normative subject

The **normative subject** is the exact commit or artifact revision containing the
final state of every applicable authority-bearing or delivered surface:

- specification;
- ADRs;
- active Work Block;
- plans and tasks when authoritative for the work;
- navigation and registry projections;
- implementation or other delivered artifact;
- proposed-to-accepted status changes.

Reviewer and Verifier reports must identify the exact normative-subject SHA or
artifact revision. A report must never use an unspecified, moving, or
self-referential moving PR head as its verified identity.

### Evidence-only commit

An **evidence-only commit** changes only approved assurance or closeout report
paths and does not modify the normative subject. The following rules are
mandatory:

1. Reviewer and Verifier reports identify the exact normative-subject SHA.
2. Any applicable normative-subject change invalidates prior Reviewer or Verifier
   readiness for the changed surfaces.
3. An evidence-only commit does not invalidate the verdict it records.
4. The final PR head may contain evidence-only commits after the verified
   normative subject.
5. CI and structural checks must pass on the resulting PR head.
6. An evidence-only commit must not contain hidden normative changes.
7. A report correction that changes only wording or metadata, without changing
   verdict, subject, scope, procedures, results, or limitations, remains
   evidence-only.
8. A change to verdict, normative subject, coverage, result, or limitation
   requires renewed assurance as applicable.

Navigation or registry changes are part of the normative subject even when they
only index evidence. They must therefore precede the evidence-only report commit
when a two-commit corrective sequence is used.

### Acceptance-state transition

`proposed` artifacts are not accepted merely because a pull request exists,
checks pass, or a review is recorded. The required transition is:

```text
preliminary Reviewer and Verifier assurance
  → Owner authorizes accepted-status finalization
  → status-only normative commit
  → final Reviewer/Verifier assurance against that normative subject as required
  → evidence-only report commit
  → CI on the resulting PR head
  → separate Owner merge approval
```

Before merge, every artifact being accepted must have frontmatter changed from
`proposed` to the project's accepted status. The status-only commit is part of
the normative subject and must receive the applicable final assurance. The
Reviewer or Verifier report may be committed afterward as evidence-only and does
not need to be contained in the commit it evaluates. Merge of files still marked
`proposed` does not silently make them accepted.

## 11. Plans and Task Decomposition

An implementation plan maps accepted requirements to ordered paths and work,
with dependencies, checks, risks, rollback, handoffs, and out-of-scope
boundaries. A tasklist is required when multiple independently verifiable steps,
handoffs, or omission-prone sequencing exist. Every task names inputs,
write-set, owner, expected result, verification, and stop conditions. Neither a
plan nor tasklist can expand the active Work Block.

## 12. Skills and Routing

Skills are procedures, not authority-bearing agents. A skill cannot expand role,
scope, write-set, side effects, or approval.

| Skill | Trigger and inputs | Procedure and output | Stop/escalation | Role/lifecycle |
|---|---|---|---|---|
| `technical-discovery` | Need current implementation/dependency facts; objective, repo, history | Inventory paths, trace contracts/data/side effects/checks; output evidence-backed findings | Missing access, unsafe live inspection, scope expansion | Architect/Orchestrator in Define; bounded Reviewer/Verifier use |
| `architecture-discovery` | Material component/authority/data/install/migration boundary; discovery and ADRs | Map forces/ownership, assess concrete alternatives, select one; output ADR proposal | Missing Owner policy/domain evidence | Architect in Define; Critic challenges |
| `specification` | New or imprecise behavior; objective, discovery, ADRs, risks | Define behavior, boundaries, errors, acceptance, non-goals; output specification | Missing product decision or scope overrun | Architect produces; Critic challenges |
| `implementation-planning` | Accepted specification; spec, ADRs, assurance | Map requirements to paths/steps/checks/rollback/handoffs; output plan | Unresolved spec/architecture | Architect/Orchestrator in Define |
| `task-decomposition` | Multiple steps/writers/handoffs; plan and write-set | Produce ordered checkable tasks with owner/result/check/stop | Overlap without integration plan | Architect/Orchestrator in Define |
| `systematic-debugging` | Defect or failed check; reproducible symptom/logs/code | Reproduce, isolate, test hypotheses, root-cause, smallest approved fix, regression check | Unsafe access, nonreproducibility, out-of-scope cause | Coder in Execute; read-only Reviewer/Verifier use |
| `memory-bank-manager` | Work Block/gate/decision/handoff/blocker/closeout change | Update responsible memory file concisely with links; output synchronized memory | Sensitive/unverified/conflicting state | Orchestrator owns; roles propose |
| `ssot-sync-closeout` | Work completes or closes blocked; all artifacts/evidence | Reconcile artifacts, deviations, memory, logs, status, follow-ups; output closeout | Missing required evidence/approval blocks success | Orchestrator in Close |
| `verification-before-completion` | Before completion/review/readiness/merge recommendation/closeout | Run fresh checks, map criteria to evidence, record failures/blockers; output embedded evidence or report | Failed/blocked required criterion | Verifier in Assure; Coder self-check subset |

Disposition of historical/current mechanisms:

- `scoped-coder`, `critic-review`, `reviewer`, and `verifier` become role
  contracts.
- `subagent-mission-brief` becomes a template and lifecycle mechanism.
- `context-snapshot` becomes a conditional rule and template.
- `orchestrator-log` becomes an Orchestrator obligation.
- branch finishing, merge protocol, worktree automation, spec-drift audit,
  project estimation, browser/UI testing, security tooling, shell guards,
  transport smoke, TDD, and external-model review are optional extensions.
- `codex-verification` is renamed into provider-neutral
  `verification-before-completion`.
- runtime bootstrap/plugin/MCP/provider-router mechanisms are outside core.
- imported-skill provenance is lightweight metadata: source, immutable revision,
  license/evidence state, local changes, and validation; it is not a control
  plane.

## 13. Mission Briefs and Handoffs

A mission brief contains Work Block/role, objective/output, inputs/authority,
read scope/write-set, prohibited actions/Hard Stops, selected skills,
acceptance/verification, stop conditions, and return format. It cannot expand the
Work Block or plan. A handoff records completed work, evidence, deviations,
blockers, and next authorized role. A context snapshot is conditional on likely
context loss and never replaces canonical artifacts.

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

| Path | Purpose and trigger | Owner and required content | Prohibited content and retention |
|---|---|---|---|
| `context.md` | Current focus/gates; open or scope/gate change | Orchestrator; active WBs, blockers, next gate, links | No transcript/secrets/speculation; keep current |
| `progress.md` | Milestone ledger; completion/blocker/reopen/closeout | Orchestrator; date, WB, status, verdict, evidence | No copied reports/unsupported success; append corrections |
| `decisions.md` | Durable accepted decisions not fully in ADR; accept/revise/revoke | Architect proposes, Orchestrator records; status, rationale, evidence, supersession | No hidden reasoning/credentials/duplicate ADR body; retain history |
| `orchestrator-log.md` | Coordination/authority/approvals/routing; every transition | Orchestrator; date, WB, action, authority basis, result, links | No chain-of-thought/raw prompts/secrets; append concise events |
| `review-log.md` | Assurance index; report/verdict change | Orchestrator with assurance roles; artifact, normative subject, scope, mode, verdict, blockers | No duplicated full reports; retain verdict history |
| `snapshots/` | Reconstructable context; conditional snapshot trigger | Orchestrator/delegate; objective, authority, state, decisions, evidence, next action | No transcript/scratch/secrets; retain referenced snapshots |

Runtime-local scratch, caches, raw transcripts, temporary traces, tool output,
and downloads use ignored `.agentic-local/` and must not contain the only copy of
accepted decisions or required evidence.

## 15. Review

Critic and Reviewer are distinct assurance roles and use distinct verdict
vocabularies.

### Critic verdicts

- `APPROVE`: the Define-stage proposal may proceed without required correction.
- `APPROVE_WITH_CHANGES`: the direction is acceptable after specified bounded
  changes are incorporated.
- `RECONSIDER`: material assumptions, scope, architecture, process level, or
  verification design must return to Define before execution.
- `BLOCKED`: required subject, authority, access, or evidence is unavailable.

### Reviewer verdicts

- `READY`: no unresolved blocking review finding.
- `CHANGES_REQUIRED`: identified corrections must be completed and re-reviewed.
- `BLOCKED`: review cannot continue because required subject, authority, access,
  or evidence is missing.
- `UNVERIFIED`: review coverage is insufficient to make a readiness judgment.

Standard and High-Risk require Reviewer inspection of an exact normative subject.
A review report records the normative-subject SHA, included and excluded paths,
source contracts, procedures, severity-ranked findings, coverage, limitations,
verdict, and correction handoff. Reviewer does not edit the reviewed subject.
Any applicable normative-subject change invalidates prior `READY` and requires
re-review of the changed surfaces. Historical Critic and Reviewer verdicts retain
the vocabulary under which they were issued and are not silently rewritten.

## 16. Verification

Verifier verdicts are:

- `READY`: fresh evidence demonstrates all required acceptance criteria.
- `NOT_READY`: evidence demonstrates one or more required criteria fail.
- `BLOCKED`: a required procedure cannot run because authority, environment,
  dependency, or access is unavailable.
- `UNVERIFIED`: required evidence is absent or insufficient.

Verification maps fresh evidence to acceptance for an exact normative subject.
Standard and High-Risk require a Verifier artifact unless a documented fallback
is explicitly allowed. A report records the normative-subject SHA, criterion,
procedure, expected and actual result, pass/fail/blocked/not-applicable status,
coverage, limitations, verdict, and residual risk.

Fresh evidence is mandatory before completion, final review request, PR readiness,
merge recommendation, and successful closeout. Applicable normative-subject
changes make prior readiness stale. Evidence-only report commits do not make the
verdict they record stale. Tests, reviewers, and verifiers cannot approve Hard
Stops or substitute for Owner authority.

## 17. Closeout

Successful closeout requires in-scope implementation, Reviewer `READY` when
required, Verifier `READY` against the applicable normative subject, required
Owner approvals, synchronized specifications/ADRs/plans/tasks/navigation,
synchronized memory and logs, disclosed residual risks, and bounded follow-up
Work Blocks. CI and structural checks must pass on the resulting PR head,
including any evidence-only commits.

Blocked, incomplete, `CHANGES_REQUIRED`, `NOT_READY`, `UNVERIFIED`, rejected, or
superseded work uses reporting-only closeout and cannot claim success.

## 18. Git and Owner Approval Boundaries

Explicit Owner approval is required for default/protected-branch merge or direct
push, production deployment/restart, secrets/credentials/permissions,
destructive operations, live data mutation, consequential external
communications/transactions, and material objective/specification/architecture/
scope expansion.

Within an approved Work Block, feature-branch creation, commits, push, PR
creation/update, nonconsequential checks, and approved evidence artifacts are
allowed. PR existence, a report commit, or readiness does not grant merge
authority.

## 19. Installation

Conceptual interface:

```text
install.py plan --target <repository>
install.py apply --target <repository>
```

`plan` is mandatory and nonmutating. It supports new/existing repositories,
resolves a safe root, rejects traversal/symlink escape, inventories collisions,
and classifies paths as `create`, `skip-identical`, `collision`, or `blocked`.

`apply` revalidates an unchanged plan, stages safely, creates only planned paths,
refuses unresolved collisions, never silently overwrites/merges/deletes,
preserves unrelated content, applies bounded `.gitignore` changes, and reports
`created`, `skipped`, `colliding`, and `blocked`. It creates no runtime agents,
hooks, plugins, MCP, provider directories, routing, profiles, or mirrors.

## 20. Optional Extensions

Optional, not core: nondeterministic evaluation, advanced threat/security
tooling, browser/UI testing, worktree automation, Git branch/PR finishing,
external second-model review, specialized provenance tooling, and all MCP,
plugins, hooks, runtime profiles, queues, daemons, and provider adapters.
Extensions may consume core artifacts but cannot redefine authority, source of
truth, process levels, Hard Stops, memory, assurance semantics, or closeout.

## 21. Candidate and Promotion Model

Noncanonical candidate:

```text
candidate/portable-agentic-sdlc-kit/
├── CANDIDATE.md
├── template/
├── tools/
└── tests/
```

Promotion requires successful synthetic installation, HardwareLab pilot,
resolved blockers, preliminary assurance, Owner-authorized accepted-status
finalization, final applicable Reviewer/Verifier assurance against that normative
subject, evidence-only assurance reports, green CI on the resulting PR head, and
separate explicit Owner approval. The canonical promoted path is
`portable-agentic-sdlc-kit/`. Superseded material is archived under
`archive/legacy-control-plane/` with provenance, not silently deleted. Exactly
one canonical kit is identified after promotion.

## 22. Migration Sequence

### WB-CORE-001 — Normative architecture

- **Objective:** define product, roles, skills, memory, process, concurrency,
  installation, candidate, assurance, and migration contracts.
- **Expected paths:** approved specification/ADRs/Work Block/reviews/navigation.
- **Dependencies:** current contracts and immutable revisions in section 1.
- **Acceptance:** unambiguous architecture, registered active WB, role-specific
  verdicts, exact normative-subject/evidence-only semantics, no implementation,
  PR unmerged, and assurance gates explicit.
- **Risks:** dual-current/target confusion, self-referential verification, or
  accidental candidate authority.
- **Out of scope:** candidate/installer/roles/skills/templates/tests/migrations
  and current-pass Verifier report.

### WB-CORE-002 — Portable candidate content

- **Objective:** implement portable entry contract, roles, nine skills,
  templates, memory, and docs skeleton.
- **Expected paths:** candidate `CANDIDATE.md`, `template/`, bounded evidence.
- **Dependencies:** accepted WB-CORE-001.
- **Acceptance:** candidate matches spec; links/contracts pass; no runtime config.
- **Risks:** copied control-plane ownership or duplicated authority.
- **Out of scope:** installer, packaging, pilot, promotion, archive.

### WB-CORE-003 — Installer and packaging

- **Objective:** implement/test plan/apply installer and packaging.
- **Expected paths:** candidate `tools/`, `tests/`, packaging, evidence.
- **Dependencies:** accepted WB-CORE-002.
- **Acceptance:** collision/path/symlink/staging/no-overwrite tests and explicit
  runtime-neutral results.
- **Risks:** path escape, partial install, overwrite, nondeterministic plan.
- **Out of scope:** real-project adoption, promotion, archive.

### WB-CORE-004 — Synthetic dry run

- **Objective:** test empty, compatible, colliding, symlinked, and partial targets.
- **Expected paths:** controlled fixtures and reports.
- **Dependencies:** verified WB-CORE-003.
- **Acceptance:** positive/negative cases, stable plan, fail-closed apply,
  recovery evidence.
- **Risks:** unrealistic fixtures or filesystem gaps.
- **Out of scope:** HardwareLab, production, promotion, legacy removal.

### WB-CORE-005 — HardwareLab pilot

- **Objective:** exercise Quick, Standard, and High-Risk-classified scenarios
  without production mutation.
- **Expected paths:** approved pilot branch/worktree, reports, approved fixes.
- **Dependencies:** successful WB-CORE-004 and Owner pilot write-set approval.
- **Acceptance:** safe install, at least two execution modes where feasible,
  usable memory, fresh review/verification evidence.
- **Risks:** pilot contamination or overgeneralization.
- **Out of scope:** production deploy, default-branch merge, rollout, promotion.

### WB-CORE-006 — Promotion and legacy archive

- **Objective:** promote canonical kit, archive superseded material, establish one
  entry path, and update architecture status/navigation atomically.
- **Expected paths:** canonical kit, archive, maps/registry/README, assurance.
- **Dependencies:** successful WB-CORE-005, resolved blockers, preliminary
  assurance, Owner-authorized accepted-status finalization, final assurance on
  the resulting normative subject, green CI, and separate Owner approval.
- **Acceptance:** one canonical boundary, provenance retained, exact assurance
  subject recorded, no silent downstream migration, checks pass.
- **Risks:** broken links, dual SSOT, deletion, adoption without consent.
- **Out of scope:** automatic downstream migration, runtime config generation,
  deletion of legacy evidence.

## 23. Compatibility and Non-Goals

Compatibility is artifact-based. Native subagents, sequential passes, and manual
handoffs are supported modes, not dependencies. Runtime enforcement is not
guaranteed by the core.

Non-goals: runtime/model/provider orchestration, permissions/sandboxes/hooks/
plugins/MCP, capability databases, provider mirrors, queues/services/daemons,
replacement of project engineering standards, universal TDD/worktree/browser/
external-model/evaluation requirements, automatic merge/deployment/live
mutation/external communication, or candidate authority before promotion.

## 24. Acceptance Criteria

- [x] Complete project-kit boundary and runtime/provider exclusions are defined.
- [x] Six roles and nine procedural skills are specified.
- [x] Shared authority remains in `AGENTS.md`.
- [x] Historical/current mechanisms have dispositions.
- [x] Canonical `memory_bank/` and ignored `.agentic-local/` are defined.
- [x] Process levels, concurrency, Git/Owner boundaries, candidate, installer,
  optional extensions, and six migration Work Blocks are precise.
- [x] Exact evidence revisions are recorded.
- [x] Active Work Block precedence and non-expansion rules are explicit.
- [x] Critic, Reviewer, and Verifier verdict vocabularies are role-specific.
- [x] Normative subject and evidence-only commit semantics are explicit.
- [x] The acceptance transition does not require an assurance report to be in the
  commit it evaluates.
- [x] No self-referential final-head assurance requirement remains.
- [x] Proposed-to-accepted status transition is explicit.
- [x] No candidate/installer/runtime-specific implementation is included.
- [x] No equal material architectural alternatives remain.
- [ ] A later Reviewer returns `READY` for the applicable normative subject.
- [ ] A later Verifier returns `READY` for the applicable normative subject.
- [ ] Owner authorizes accepted-status finalization and later separately approves
  integration after final assurance and green CI.

The final criteria remain open. This specification is not accepted and does not
authorize merge or promotion while its frontmatter remains `proposed`.
