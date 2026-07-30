---
schema_version: 1
artifact_type: normative_specification
artifact_id: portable-agentic-sdlc-project-kit
status: accepted
owner_role: owner
created_at: 2026-07-29
source_framework_revision: 0fce7389d27690482e910e942a1f3138c2fef123
historical_framework_revision: 0c632db0b0444e556251c384f6254141c9df59bc
superpowers_reference_revision: 44c9b2d6e889982ac18c27d05a19fefe335194e1
---

# Portable Agentic SDLC Project Kit

## 1. Purpose

Define a portable, repository-local Agentic SDLC Project Kit. The cited framework
revisions are evidence, not runtime authority. Explicit Owner authorization was
recorded on 2026-07-30. This specification is now `accepted` as the normative
target contract; it is not yet the current operational architecture. Final
assurance, closeout, promotion, and merge remain pending.

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

### 6.1 Classification algorithm

Classification occurs during Intake/Define. Every Work Block must be assessed
against all of these dimensions:

```text
ambiguity
behavioral impact
architecture impact
system boundaries
authority and approvals
side effects
reversibility and rollback complexity
security and data risk
legal/privacy/financial consequence
verification cost
nondeterminism
number of writers and handoffs
```

File count is not a primary classifier.

A one-file change can be Standard or High-Risk. A many-file mechanical change can
remain Quick only when every Quick eligibility condition is satisfied.

Selection order is fail-closed:

1. evaluate every mandatory High-Risk trigger;
2. when no High-Risk trigger applies, evaluate every Quick eligibility condition;
3. select Quick only when all Quick conditions pass;
4. select Standard when the Work Block is not eligible for Quick and does not
   trigger High-Risk;
5. record the dimensions, result, rationale, required artifacts, assurance, and
   approvals in the Work Block before execution.

### 6.2 Quick eligibility

Quick may be selected only when **all** of the following are true:

1. objective and acceptance are unambiguous;
2. an accepted contract already governs the behavior;
3. no material architecture, authority, public-interface, data-model, or
   system-boundary decision is required;
4. no High-Risk trigger or Owner Hard Stop applies;
5. side effects are local, bounded, and understood;
6. the change is readily reversible with a simple rollback;
7. verification is deterministic, inexpensive, and available;
8. no required independent Critic, Reviewer, or domain assurance is needed;
9. one Coder and one bounded write-set are sufficient;
10. no migration, multi-system coordination, or consequential external action is
    involved.

Quick still requires:

```text
compact Work Block
scope and write-set
acceptance criteria
fresh verification
truthful closeout
```

A separate Critic or Reviewer report is normally optional, but may be required by
the Work Block.

### 6.3 Standard selection

Standard is the default when work is not eligible for Quick and does not trigger
High-Risk.

Escalate Quick to Standard when any of the following applies:

```text
material ambiguity
behavioral or contract change
material ADR decision
cross-component or system-boundary work
nontrivial rollback or migration
multiple coordinated artifacts or handoffs
separate Reviewer or Verifier assurance is required
verification is not cheap and deterministic
scope cannot be bounded confidently before implementation
```

Standard requires a specification or accepted change contract, material ADRs,
plan/tasks as needed, Critic, one bounded Coder, Reviewer, Verifier, truthful
closeout, and project-memory synchronization.

### 6.4 High-Risk selection

High-Risk applies whenever any mandatory trigger exists, regardless of file count
or apparent implementation size. Mandatory triggers include:

```text
irreversible or difficult-to-reverse side effects
production deployment or restart
secrets, credentials or permissions
destructive operations
live data or business-state mutation
security or trust-boundary change
consequential external communication or transaction
material legal, privacy or financial consequence
harmful or difficult-to-bound nondeterminism
```

High-Risk adds:

```text
risk or threat assessment
rollback and recovery plan
positive and negative cases
required independent assurance
explicit Owner approvals
domain-specific verification or evaluation when applicable
```

If required assurance, authority, rollback, or evidence is unavailable, the Work
Block is `BLOCKED` or `UNVERIFIED`; it cannot be downgraded to Standard or Quick.

### 6.5 Reclassification

- classification occurs during Intake/Define;
- new evidence may only preserve or raise the level unless a documented
  reassessment proves the original risk assumption false;
- discovering ambiguity, broader side effects, or reduced reversibility requires
  immediate escalation;
- reclassification requires Work Block revision before further execution;
- a lower-level artifact or agent cannot downgrade the Work Block.

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

Skills are procedures, not authority. Exactly these nine skills form the portable
core:

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

### Normative mechanism disposition

Every relevant current or historical mechanism has exactly one portable
disposition:

| Existing or historical mechanism | Portable disposition | Target location or replacement | Rationale / boundary |
|---|---|---|---|
| `technical-discovery` | remain core procedural skill | `agentic/skills/technical-discovery/` | Portable discovery procedure; no authority expansion. |
| `architecture-discovery` | remain core procedural skill | `agentic/skills/architecture-discovery/` | Portable architecture-boundary analysis. |
| `specification` | remain core procedural skill | `agentic/skills/specification/` | Defines behavior and acceptance before implementation. |
| `implementation-planning` | remain core procedural skill | `agentic/skills/implementation-planning/` | Converts accepted requirements into bounded execution. |
| `task-decomposition` | remain core procedural skill | `agentic/skills/task-decomposition/` | Produces bounded, verifiable tasks and handoffs. |
| `systematic-debugging` | remain core procedural skill | `agentic/skills/systematic-debugging/` | Root-cause-first investigation remains portable. |
| `memory-bank-manager` | remain core procedural skill | `agentic/skills/memory-bank-manager/` | Maintains canonical committed project memory. |
| `ssot-sync-closeout` | remain core procedural skill | `agentic/skills/ssot-sync-closeout/` | Synchronizes accepted state and truthful closeout. |
| `verification-before-completion` | remain core procedural skill | `agentic/skills/verification-before-completion/` | Requires fresh evidence before readiness claims. |
| `scoped-coder` | become role contract | `agentic/roles/coder.md` | Implementation authority belongs to the Coder role and approved write-set. |
| `critic-review` | become role contract | `agentic/roles/critic.md` | Criticism is a logical role obligation, not a runtime skill gate. |
| `reviewer` | become role contract | `agentic/roles/reviewer.md` | Frozen-subject review belongs to the Reviewer role. |
| `verifier` | become role contract | `agentic/roles/verifier.md` | Criterion-mapped evidence belongs to the Verifier role. |
| `codex-verification` | become provider-neutral Verifier contract | `agentic/roles/verifier.md` plus `verification-before-completion` | No provider name survives as portable authority; second-model use is optional execution metadata. |
| `subagent-mission-brief` | become template and lifecycle mechanism | mission-brief template plus section 13 handoff mechanism | Works for native subagents, sequential sessions, and manual handoff. |
| `context-snapshot` | become conditional template rule | snapshot template under `agentic/templates/` and `memory_bank/snapshots/` | Created only when context loss or transfer risk justifies it. |
| `orchestrator-log` | become role obligation and canonical memory artifact | Orchestrator contract plus `memory_bank/orchestrator-log.md` | Records coordination facts without becoming a separate authority skill. |
| `review-log` | become assurance index | `memory_bank/review-log.md` | Indexes report identity and history; reports remain detailed evidence. |
| branch finishing | become optional extension | optional branch-finishing extension | VCS integration procedure may consume core artifacts but cannot redefine authority. |
| merge protocol automation | become optional extension | optional distributed-work extension | Automation is not required for portable sequential or manual operation. |
| worktree automation | become optional extension | optional workspace-isolation extension | Worktrees are one possible isolation mechanism, not a core dependency. |
| browser/UI testing | become optional extension | optional browser/UI assurance extension | Domain-specific verification remains triggered by the Work Block. |
| advanced threat/security tooling | become optional extension | optional security-assurance extension | May add checks but cannot redefine roles, lifecycle, or approvals. |
| external second-model review | become optional extension | optional external-review extension | Model/provider diversity never grants authority or independence by name alone. |
| specialized skill provenance tooling | become optional extension | optional skill-maintenance extension | Maintainer workflow, not project-kit core. |
| nondeterministic output evaluation | become optional extension | optional evaluation extension | Required only when the Work Block's risk and nondeterminism demand it. |
| TDD-specific workflow | become optional extension | optional test-first extension | Test strategy is selected by the Work Block; universal TDD is not core. |
| project estimation | become optional extension | optional estimation extension | Estimation does not define delivery authority. |
| spec-drift automation | become optional extension | optional drift-check extension | May consume specs/reports but cannot become a parallel source of truth. |
| provider/runtime adapters | remain outside portable core | current implementation may remain operational during migration | Neither copied into nor owned by the portable target. |
| installation profiles | remain outside portable core | current implementation may remain operational during migration | Portable install owns files, not runtime-profile composition. |
| model routing | remain outside portable core | runtime-local configuration | Models cannot define portable authority. |
| capability negotiation | remain outside portable core | runtime-local or operator decision | Portable workflow records actual execution mode without owning runtime capability catalogs. |
| provider-specific agents | remain outside portable core | runtime-local configuration | Portable roles are logical Markdown contracts. |
| hooks and runtime permission configuration | remain outside portable core | repository/runtime-local safeguards | Technical enforcement may exist externally but is not target-owned. |
| MCP and plugins | remain outside portable core | runtime-local integrations | Integrations cannot become core authority or lifecycle. |
| queues, daemons, and services | remain outside portable core | external operational tooling | The kit must operate through artifacts and manual handoff without services. |
| provider snapshots | remain outside portable core | external evidence when independently useful | Provider state is noncanonical and does not grant readiness. |
| runtime transport and handoff runners | remain outside portable core | manual/portable handoff artifacts replace them | Transport implementation is not part of the project kit. |
| duplicated runtime skill mirrors | remain outside portable core | one canonical `agentic/skills/` copy | Duplication creates drift and provider ownership. |
| runtime-specific bootstrap and conformance control | remain outside portable core | external runtime maintenance | The portable installer validates only its own managed paths and contract. |

Optional extensions may consume core artifacts but cannot redefine authority,
lifecycle, Work Blocks, process levels, memory, or assurance. Current repository
implementations may remain operational during migration, but they are neither
copied into nor owned by the portable target.

## 13. Mission Briefs and Handoffs

A mission brief contains Work Block/role, objective, inputs, authority, read scope,
write-set, Hard Stops, skills, acceptance, verification, stop conditions, and
return format. It cannot expand the Work Block or plan. Handoffs record completed
work, evidence, deviations, blockers, and next authorized role.

## 14. Project Memory and Logs

Canonical project memory is committed, concise, secret-free, and sufficient to
reconstruct the current accepted project state without provider memory or chat
history.

| Path | Owner | Update trigger | Required content | Prohibited content | Retention |
|---|---|---|---|---|---|
| `memory_bank/context.md` | Orchestrator | Work Block opened; objective, scope, or gate changes; blocker appears or clears; active handoff changes; next authorized action changes | current focus; active Work Block; blockers; current gate; next action; links to authoritative artifacts | transcripts; secrets; speculative decisions; duplicated specification bodies | Current-state document; replace stale state rather than append indefinitely. |
| `memory_bank/progress.md` | Orchestrator | milestone completed; task blocked; work reopened; assurance verdict recorded; Work Block closed | date; Work Block; event/status; evidence link; correction or supersession when applicable | unsupported success claims; copied full reports; hidden reasoning | Append-only milestone ledger; corrections must be explicit. |
| `memory_bank/decisions.md` | Architect proposes; Owner accepts material product decisions when required; Orchestrator records accepted, revised, or revoked state | durable decision accepted; decision revised; decision revoked or superseded | decision; status; rationale summary; authority/evidence; supersession links | unaccepted proposals represented as decisions; credentials; private chain-of-thought; duplicated ADR bodies | Retain historical status and supersession chain. |
| `memory_bank/orchestrator-log.md` | Orchestrator | lifecycle transition; role assignment or handoff; approval or revocation; blocker; scope correction; closeout decision | date; Work Block; action; authority basis; result; artifact links | raw prompts; chat transcripts; hidden reasoning; secrets | Concise append-only coordination ledger. |
| `memory_bank/review-log.md` | Orchestrator, using facts supplied by Critic, Reviewer, and Verifier reports | assurance report created; verdict changes; subject changes and makes a verdict stale; blocking finding resolved; assurance superseded | report path; exact normative subject; role; independence mode; verdict; blocking state; supersession when applicable | replacing the report; copying full findings; mutable assurance data in `PROJECT_MAP.md` or `FILE_REGISTRY.yml` | Append verdict history; never silently rewrite historical verdicts. |
| `memory_bank/snapshots/` | Orchestrator or explicitly delegated role | likely context loss; long pause; environment/runtime transfer; manual handoff; major phase boundary when active context cannot be reconstructed cheaply | objective; authority; current subject/head; accepted decisions; completed work; blockers; evidence; next authorized action | raw transcripts; scratch; secrets; private reasoning | Retain referenced snapshots; stale unreferenced snapshots may be archived under an explicit policy. |

Global memory rules:

1. `memory_bank/` is committed, concise, and secret-free.
2. It must be sufficient to reconstruct current accepted project state without
   provider memory or chat history.
3. `.agentic-local/` is ignored, disposable, and noncanonical.
4. `.agentic-local/` cannot contain the only copy of an accepted decision,
   required evidence, current scope, a blocking condition, or the next authorized
   action.
5. Reports remain the source for detailed assurance results.
6. Memory links to reports rather than duplicating them.
7. Unverified or proposed content must be labelled as such.

Reports remain the source for verdict, subject, scope, findings, coverage,
results, and limitations. `review-log.md` indexes report identity and history
without replacing reports or becoming normative navigation.

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

`install.py plan` is mandatory, fail-closed, and nonmutating. It produces an
approved plan identity and classifies each candidate-managed path as `create`,
`skip-identical`, `collision`, or `blocked`.

### 19.1 Target-root resolution

1. Resolve the target repository root to a canonical absolute path.
2. Reject a missing, ambiguous, or unsafe target root.
3. Record the canonical root in the plan.
4. `apply` must resolve it again and require it to match the approved plan.

### 19.2 Candidate path validation

Every candidate-managed path must:

- be a normalized relative path;
- be non-empty;
- not be absolute;
- not use a Windows drive prefix;
- not use a UNC/network-root prefix;
- not contain `..` path components;
- not contain NUL or invalid platform path characters;
- not normalize outside the target root.

The installer rejects rather than sanitizes an invalid manifest path.

### 19.3 Destination containment

For every planned destination:

1. join it to the canonical target root;
2. resolve existing parent components and symlinks;
3. verify the destination remains inside the canonical target root;
4. classify any escape, ambiguous resolution, or unsupported link type as
   `blocked`.

A symlink or junction in any destination parent that redirects outside the target
root fails closed.

### 19.4 Apply-time revalidation

Before any mutation, `apply` repeats:

- target-root identity;
- path normalization;
- traversal checks;
- parent symlink/junction checks;
- collision state;
- approved plan identity.

Any mismatch or traversal finding aborts the entire apply before target mutation.

### 19.5 Atomicity and mutation boundary

No file is created, overwritten, merged, moved, or deleted when any planned action
is blocked by traversal, root escape, unsafe link resolution, or unresolved
collision.

After revalidation, `apply` stages and creates only approved `create` paths,
preserves `skip-identical`, refuses unresolved collisions, and never silently
overwrites, merges, moves, or deletes. It creates no runtime agents, hooks,
plugins, MCP, provider directories, routing, profiles, or mirrors.

Installer implementations may impose stricter platform rules but cannot weaken
these requirements.

## 20. Optional Extensions

Optional, non-core capabilities are classified individually in section 12.
Extensions may consume core artifacts but cannot redefine core authority,
lifecycle, Work Blocks, process levels, memory, or assurance.

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
- [x] Six roles and exactly nine core skills are specified.
- [x] Every listed current/historical mechanism has an explicit disposition.
- [x] Work Block precedence and non-expansion rules are explicit.
- [x] Process-level classification is risk-based, operational, and not file-count based.
- [x] Quick eligibility, Standard default/escalation, High-Risk triggers, and reclassification are explicit.
- [x] Per-memory-file ownership, update triggers, content boundaries, and retention are defined.
- [x] One-write-Work-Block concurrency is bounded.
- [x] Installer traversal, root containment, link escape, revalidation, and atomicity are fail-closed.
- [x] Role-specific verdict vocabularies are defined.
- [x] Exact normative-subject and evidence-only semantics are defined.
- [x] Mutable assurance state is prohibited from normative navigation.
- [x] Reports need no per-report map/registry registration.
- [x] Canonical evidence-path/frontmatter discovery is defined.
- [x] Proposed-to-accepted sequence is non-self-referential.
- [x] No candidate/installer/runtime implementation is included.
- [x] A renewed Reviewer returned `READY` for preliminary-assurance subject
  `9c169fd97bdbe90bb2fc1133fff29878d1373396`.
- [x] A renewed preliminary Verifier returned `READY` for the same subject.
- [x] The Owner authorized accepted-status finalization on 2026-07-30.
- [ ] Final applicable Reviewer and Verifier assurance is recorded against the
  status-finalized normative subject.
- [ ] Closeout, promotion, and separate Owner merge approval are completed.

This specification is `accepted` as the normative target contract. It is not yet
the current operational architecture and does not authorize promotion or merge.
