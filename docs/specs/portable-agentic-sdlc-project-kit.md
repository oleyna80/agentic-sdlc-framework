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

This specification defines a portable, repository-local Agentic SDLC Project Kit. The kit provides a complete artifact-based development lifecycle usable through native subagents, sequential single-agent role passes, or manual copy-and-paste handoffs.

It preserves the practical lifecycle demonstrated by `agentic-sdlc-framework@0c632db0b0444e556251c384f6254141c9df59bc`, retains useful authority and evidence rules from `agentic-sdlc-framework@0fce7389d27690482e910e942a1f3138c2fef123`, and adopts selected procedural ideas from `obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`, including design before implementation, implementation planning, systematic debugging, and verification before completion.

Those revisions are evidence, not runtime authorities. This specification becomes normative only after review and an Owner-approved merge. Until promotion, the current repository remains operationally canonical and the portable candidate remains noncanonical.

## 2. Product Boundary

The product is a complete project kit, not merely a skills library and not a runtime control plane. It contains:

- root `AGENTS.md` as the entry operating contract;
- SDD lifecycle and process levels;
- separate logical role contracts;
- procedural skills;
- Work Blocks;
- specifications and architecture decisions;
- implementation plans and tasklists;
- mission briefs, handoffs, and conditional context snapshots;
- canonical committed project memory;
- Orchestrator and review logs;
- Critic, Reviewer, and Verifier artifacts;
- closeout and memory synchronization;
- collision-safe installation.

The target installed structure is conceptually:

```text
AGENTS.md
agentic/
├── roles/
│   ├── README.md
│   ├── orchestrator.md
│   ├── architect.md
│   ├── critic.md
│   ├── coder.md
│   ├── reviewer.md
│   └── verifier.md
├── skills/
│   ├── technical-discovery/
│   ├── architecture-discovery/
│   ├── specification/
│   ├── implementation-planning/
│   ├── task-decomposition/
│   ├── systematic-debugging/
│   ├── memory-bank-manager/
│   ├── ssot-sync-closeout/
│   └── verification-before-completion/
└── templates/
    ├── work-block.md
    ├── specification.md
    ├── architecture-decision.md
    ├── implementation-plan.md
    ├── tasklist.md
    ├── mission-brief.md
    ├── context-snapshot.md
    ├── critic-report.md
    ├── review-report.md
    ├── verification-report.md
    └── closeout-report.md
docs/
├── specs/
├── architecture/decisions/
├── plans/
├── tasklists/
├── missions/
└── reports/
    ├── reviews/
    ├── verification/
    └── closeout/
memory_bank/
├── context.md
├── progress.md
├── decisions.md
├── orchestrator-log.md
├── review-log.md
└── snapshots/
.agentic-local/                 # ignored runtime-local state
```

The kit must not own, require, install, generate, validate, or synchronize:

- `.codex/`, `.claude/`, `.opencode/`, or equivalent provider directories;
- provider-specific agents, model routing, or model selection;
- hooks or runtime permission configuration;
- MCP or plugins;
- capability negotiation or runtime capability registries;
- provider snapshots or runtime profiles;
- duplicated provider-specific role or skill mirrors;
- framework-owned queues, daemons, services, or transports.

A project or user may create runtime-specific configuration independently. It is outside the portable framework contract, must not redefine authority or lifecycle semantics, and is not installed or verified by the kit.

## 3. Design Principles

1. **Artifacts are the interoperability boundary.** Required state is inspectable in repository files; hidden chat history and provider memory are never authoritative.
2. **Authority is structural.** Tool access, model capability, runtime identity, hooks, or plugins never expand authority.
3. **Use the smallest sufficient process level.** Process cost follows risk and uncertainty, not file count.
4. **Evidence precedes claims.** Completion, review readiness, PR readiness, merge recommendations, and closeout require fresh current-state evidence.
5. **One writer owns one write-set.** Parallel work uses isolation and non-overlapping ownership.
6. **Project memory is concise and durable.** It records accepted state, not raw transcripts.
7. **Runtime neutrality means non-ownership.** The kit does not reproduce runtime orchestration features.
8. **Missing assurance fails closed.** Required missing evidence remains degraded, `BLOCKED`, or `UNVERIFIED`.
9. **Installation is collision-safe.** Existing project files are never silently overwritten.
10. **Candidate evidence precedes promotion.** Candidate presence alone never makes it canonical.

## 4. Source of Truth

Conflicts are resolved in this order:

1. current explicit Owner instruction and recorded approvals or revocations;
2. root `AGENTS.md` for shared authority, Hard Stops, and lifecycle invariants;
3. approved specification and accepted ADRs;
4. approved implementation plans and tasklists;
5. active Work Block and bounded mission briefs;
6. frozen implementation diff or final artifact, interpreted against higher authorities;
7. Critic, Reviewer, Verifier, and closeout reports;
8. `memory_bank/`;
9. `.agentic-local/`, generated notes, runtime caches, and external references.

A lower-ranked artifact may provide evidence but must not silently revise a higher-ranked artifact. Material objective, specification, architecture, acceptance, risk, or write-set changes return to Define and require an approved revision.

## 5. Lifecycle

```text
Intake and classify
  → Define
      discovery
      architecture when material
      specification or explicit change contract
      implementation plan and tasks when required
      Critic when required
  → Execute
      bounded implementation
      self-checks
      checkpoint commits when useful
      frozen diff or final artifact
  → Assure
      Reviewer when required
      fresh verification
      independent assurance when required
  → Close
      SSOT synchronization
      memory synchronization
      truthful closeout
  → Integrate
      PR readiness recommendation
      separate Owner-approved merge or deployment action
```

Quick work may compress functions, but no level may omit scope, authority, acceptance criteria, fresh verification, or truthful closeout. A checkpoint commit is an execution aid, not a completion claim, and does not require full final assurance when it remains inside the approved feature-branch Work Block.

## 6. Process Levels

Classification uses:

- ambiguity;
- behavioral impact;
- architecture impact;
- system boundaries;
- authority;
- side effects;
- reversibility;
- security, privacy, credential, and data risk;
- verification cost and observability;
- nondeterminism.

File count, line count, duration, and number of directories are supporting indicators only.

### 6.1 Classification rule

A Work Block is **High-Risk** when any mandatory trigger applies:

- production deployment, live restart, or release publication;
- secret, credential, authentication, authorization, or trust-boundary change;
- live database, business-data, payment, order, stock, CRM, or consequential external mutation;
- destructive or difficult-to-reverse operation;
- security-sensitive input, file/path, webhook, import/export, or privileged-action boundary;
- legal, regulatory, safety, privacy, or material financial consequence;
- nondeterministic behavior whose failure could cause material harm;
- explicit Owner, policy, or domain requirement for independent assurance.

If no High-Risk trigger applies, a Work Block is **Standard** when ambiguity, behavior, architecture, cross-boundary integration, side effects, rollback, specification work, or verification is material.

A Work Block is **Quick** only when all are true: objective is unambiguous; behavior and architecture impact are low; write-set and side effects are tightly bounded; the change is reversible; no High-Risk trigger applies; acceptance is provable with a narrow fresh check; and a compact Work Block can explain the work without hidden context.

Uncertainty selects Standard. Missing evidence or independence never justifies lowering the level.

### 6.2 Quick

Quick requires:

- compact Work Block;
- explicit scope, out-of-scope boundary, and write-set;
- acceptance criteria;
- fresh verification against the final state;
- truthful closeout and memory update when project context changed.

Critic and a separate Reviewer are normally optional. A separate verification report is not required when evidence is recorded directly in the Work Block or closeout. New ambiguity, architecture impact, side effects, security/data risk, or expensive verification escalates the Work Block.

### 6.3 Standard

Standard requires:

- approved specification or explicit change contract;
- ADR when materially architectural;
- implementation plan;
- tasklist when sequencing, ownership, or verification benefits from decomposition;
- Critic, Coder, Reviewer, and Verifier functions;
- frozen diff or final artifact before independent review;
- closeout and memory synchronization.

One session may perform sequential role passes when independence is not required, but it must disclose that the passes are not independent.

### 6.4 High-Risk

High-Risk adds:

- risk or threat assessment;
- rollback, recovery, and containment;
- positive and negative verification cases;
- explicit Owner approvals for applicable Hard Stops;
- independent assurance where required;
- optional domain-specific evaluation for nondeterministic, safety-sensitive, or regulated outcomes.

Unavailable required independence, runtime evidence, or domain expertise leaves the result degraded, `BLOCKED`, or `UNVERIFIED`; it cannot be represented as fully assured.

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

Shared authority and Hard Stops remain canonical in `AGENTS.md`. Each role file contains only: purpose; authority; prohibited actions; required inputs; procedure; output; stop conditions; handoff.

### 7.1 Orchestrator

Purpose: frame and classify Work Blocks, bind roles, preserve scope, control gates, record approvals and limitations, consolidate results, and close work.

Authority: workflow and approved coordination artifacts; approved feature-branch operations.

Prohibited: unassigned implementation, self-approving Hard Stops, claiming unavailable independence, silent scope expansion, or default-branch integration without Owner approval.

Output: Work Block, routing and handoff records, Orchestrator log, gate state, and closeout.

### 7.2 Architect

Purpose: discover constraints and produce architecture, specification, and plan proposals.

Authority: read-only discovery plus approved documentation draft paths.

Prohibited: product implementation, unapproved architecture changes, or treating research as accepted specification.

Output: evidence-backed discoveries, ADR/specification proposals, and implementation-plan inputs.

### 7.3 Critic

Purpose: challenge Define-stage assumptions, boundary, scope, risk, architecture, process level, and verification design.

Authority: read-only except the approved Critic report path.

Prohibited: implementing corrections, expanding the write-set, or granting Owner approvals.

Output: findings, evidence limitations, verdict, required changes, and residual concerns.

### 7.4 Coder

Purpose: implement one approved write-set according to accepted artifacts.

Authority: exactly one approved write-set in one working tree.

Prohibited: out-of-scope writes, changing requirements to match code, unapproved Hard Stops, or sharing the write-set with another active Coder.

Output: bounded diff, self-check evidence, deviations, and review handoff.

### 7.5 Reviewer

Purpose: inspect the frozen diff or final artifact for correctness, regressions, architecture alignment, maintainability, security, and specification compliance.

Authority: read-only except the review report path.

Prohibited: editing the reviewed implementation or claiming runtime proof from static review.

Output: findings, verdict, inspected scope, evidence gaps, and correction handoff.

### 7.6 Verifier

Purpose: test acceptance criteria and observable contracts against the current final state.

Authority: read-only for source and runtime except approved evidence and nonconsequential fixtures in scope.

Prohibited: modifying implementation to make tests pass, using stale evidence, unapproved live mutation, or reporting blocked checks as pass.

Output: criterion-to-evidence mapping, procedures, results, blocked checks, verdict, and residual risk.

## 8. Role Execution Modes

### 8.1 Native subagents

The Orchestrator supplies role contract, Work Block, inputs, write-set or read-only boundary, expected output, and stop conditions. Delegation is an execution mechanism; repository artifacts remain authoritative.

### 8.2 Sequential single-agent passes

Each pass declares the active role, loads required inputs, obeys that role's authority, produces its artifact, and stops before assuming the next role. Sequential reuse is not independent assurance.

### 8.3 Manual copy-and-paste handoff

A human may transfer a complete mission brief and artifacts to another session or tool. The recipient returns the required output and blockers. Hidden prior chat context is not required.

## 9. Work Blocks and Concurrency

A Work Block records: identifier; objective and expected result; process level; source specification and ADRs; scope and out-of-scope boundary; write-set; role bindings and execution mode; side effects, risks, Hard Stops, and approvals; acceptance and assurance plan; rollback when required; current gates and closeout status.

Concurrency rules:

1. One active write-capable Work Block per working tree.
2. Multiple read-only discovery Work Blocks may coexist.
3. Multiple write Work Blocks require isolated worktrees or clones.
4. Each isolated tree still has one active write Work Block.
5. Parallel writers require non-overlapping write-sets or an explicit integration plan naming order, conflicts, combined review, and combined verification.
6. One Coder owns each write-set.
7. A shared file makes write-sets overlap even when different sections are targeted.
8. Integrating parallel results is a bounded write Work Block unless already authorized by the integration plan.

## 10. Specifications and Architecture Decisions

A specification defines required behavior, constraints, error states, acceptance criteria, and non-goals. An ADR records a material structural choice, rationale, rejected alternatives, consequences, and review triggers.

An ADR is required for material changes to product boundary, source-of-truth ownership, role authority, data/security/deployment boundaries, public interfaces, durable component relationships, installation, migration, or compatibility.

Implementation must not begin while equal material architectural alternatives remain unresolved. A proposal becomes accepted only through the project Owner-controlled process.

## 11. Plans and Task Decomposition

An implementation plan maps accepted requirements to paths and ordered work, with dependencies, verification, risks, rollback, and out-of-scope boundaries.

A tasklist is required when work contains multiple independently verifiable steps, multiple handoffs, or sequencing where omission is plausible. Each task names inputs, write-set, expected result, verification, and stop conditions. The kit imposes no universal time or file-count target.

## 12. Skills and Routing

Skills are procedures, not authority-bearing agents. A skill cannot expand role, scope, write-set, side effects, or Owner approval. The core contains exactly nine skills.

### 12.1 `technical-discovery`

- **Trigger:** repository behavior, implementation, dependencies, or current state must be understood.
- **Inputs:** objective, repository artifacts, history, constraints.
- **Procedure:** inventory relevant paths; trace contracts, data flow, side effects, and verification surfaces; identify gaps and duplicates; distinguish fact, inference, and unknown.
- **Output:** bounded evidence-backed discovery findings.
- **Stop/escalation:** missing access, secrets, unsafe live inspection, material architecture/risk discovery, or scope expansion.
- **Role/lifecycle:** Architect or Orchestrator in Define; bounded use by Reviewer/Verifier.

### 12.2 `architecture-discovery`

- **Trigger:** component, authority, data, installation, interoperability, or migration boundaries are material.
- **Inputs:** technical discovery, current ADRs, objective, constraints.
- **Procedure:** identify forces and invariants; map ownership; evaluate concrete alternatives; select one decision; record consequences and review triggers.
- **Output:** architecture findings and ADR proposal when material.
- **Stop/escalation:** missing Owner policy, domain expertise, or approved scope.
- **Role/lifecycle:** Architect in Define; Critic challenges the decision.

### 12.3 `specification`

- **Trigger:** Standard/High-Risk work, new behavior, or imprecise change contract.
- **Inputs:** objective, discovery, ADRs, constraints, risks, Owner decisions.
- **Procedure:** define behavior, boundaries, invariants, error states, acceptance criteria, non-goals, and blockers; remove equal alternatives.
- **Output:** approvable specification or explicit change contract.
- **Stop/escalation:** missing product decision or scope overrun.
- **Role/lifecycle:** Architect produces; Critic challenges; Owner accepts material scope.

### 12.4 `implementation-planning`

- **Trigger:** accepted specification requires ordered implementation.
- **Inputs:** specification, ADRs, discovery, assurance requirements.
- **Procedure:** map requirements to paths and steps; define dependencies, checks, rollback, and handoffs.
- **Output:** implementation plan.
- **Stop/escalation:** unresolved specification or architecture.
- **Role/lifecycle:** Architect or Orchestrator in Define; Critic reviews for Standard/High-Risk.

### 12.5 `task-decomposition`

- **Trigger:** plan has multiple steps, writers, handoffs, or verification points.
- **Inputs:** plan, write-set, role bindings, dependencies.
- **Procedure:** create ordered independently checkable tasks; assign one owner; specify input, result, verification, and stop conditions.
- **Output:** tasklist or mission-ready tasks.
- **Stop/escalation:** overlapping tasks without integration plan or discovered scope drift.
- **Role/lifecycle:** Architect/Orchestrator in Define; drives Coder missions.

### 12.6 `systematic-debugging`

- **Trigger:** defect, failed check, unexpected behavior, or inconsistent state.
- **Inputs:** reproducible symptom, logs, current code, environment facts, acceptance.
- **Procedure:** reproduce; gather evidence; isolate layer; test hypotheses; identify root cause; implement smallest approved fix; verify regression coverage.
- **Output:** root-cause statement, bounded fix, verification evidence.
- **Stop/escalation:** nonreproducibility, unsafe access, unapproved side effect, or out-of-scope root cause.
- **Role/lifecycle:** Coder in Execute; read-only portions for Reviewer/Verifier.

### 12.7 `memory-bank-manager`

- **Trigger:** Work Block open, decision, gate transition, handoff, blocker, closeout, or context compaction.
- **Inputs:** current authoritative and verified state.
- **Procedure:** update the responsible memory file; keep entries concise, dated, linked, and secret-free; mark stale current state; preserve decision history.
- **Output:** synchronized `memory_bank/`.
- **Stop/escalation:** unverified, sensitive, or higher-authority conflict.
- **Role/lifecycle:** Orchestrator owns synchronization; other roles propose updates.

### 12.8 `ssot-sync-closeout`

- **Trigger:** required implementation/assurance finishes or work must close blocked/incomplete.
- **Inputs:** specification, ADRs, plan, tasks, final diff, review, verification, approvals, memory.
- **Procedure:** reconcile artifacts; record deviations and residual risks; update memory/logs; assign truthful status and follow-up gates.
- **Output:** closeout report or compact Quick closeout.
- **Stop/escalation:** successful closeout stops on missing required evidence or approval; use reporting-only closeout.
- **Role/lifecycle:** Orchestrator in Close.

### 12.9 `verification-before-completion`

- **Trigger:** before completion, final review request, PR readiness, merge recommendation, or successful closeout.
- **Inputs:** current final state, acceptance criteria, contracts, prior checks.
- **Procedure:** select current-state checks; run or observe them fresh; map criteria to evidence; record failures and blockers; reject stale evidence.
- **Output:** embedded verification evidence or separate Verifier report.
- **Stop/escalation:** failed or blocked required criterion prevents success; consequential live verification requires Owner approval.
- **Role/lifecycle:** Verifier in Assure; Coder self-check subset; Orchestrator claim gate.

### 12.10 Disposition of current and historical mechanisms

| Mechanism | Target disposition |
|---|---|
| `technical-discovery`, `architecture-discovery`, `task-decomposition`, `systematic-debugging`, `memory-bank-manager`, `ssot-sync-closeout` | Retain as normalized core procedural skills. |
| design/specification functions previously embedded in brainstorming or documents | Consolidate into core `specification`. |
| `writing-plans` or equivalent plan-writing behavior | Consolidate into core `implementation-planning`. |
| `verification-before-completion` | Core provider-neutral completion-claim gate. |
| `scoped-coder`, `critic-review`, `reviewer`, `verifier` | Become separate role contracts, not skills. |
| `codex-verification` | Retire provider naming; portable procedure moves into `verification-before-completion`. |
| `subagent-mission-brief` | Mission-brief template and lifecycle mechanism. |
| `context-snapshot` | Conditional lifecycle rule and template. |
| `orchestrator-log` | Orchestrator obligation using `memory_bank/orchestrator-log.md`. |
| `merge-protocol`, `scoped-commit-guard`, branch-finishing, `finishing-a-development-branch` | Optional Git extension. |
| `using-git-worktrees`, worktree automation | Optional concurrency extension; core keeps isolation rules only. |
| `spec-drift-audit` | Optional assurance extension. |
| `project-estimation` | Optional planning extension. |
| `webapp-testing` | Optional browser/UI extension. |
| `security-audit-triage`, `security-hardening-pass`, `security-verification-gate` | Optional security tooling; core retains High-Risk security trigger. |
| `shell-context-guard` | Optional local/runtime safety extension. |
| `agent-operations-review` | Optional retrospective without authority changes. |
| `handoff-live-smoke` | Optional transport verification. |
| `mcp-builder` | Outside core; project-local extension. |
| `output-skill` | Project-specific extension. |
| `graphify-code-map` | Optional knowledge/tooling extension. |
| `skill-creator`, `writing-skills`, `skill-library-maintenance` | Optional kit-maintainer tooling, not installed project lifecycle. |
| imported-skill provenance | Lightweight metadata: source, immutable revision, license/evidence state, local changes, validation; no control plane or automatic update authority. |
| design skills in the current catalog | Domain/project extensions excluded from core. |
| media-production and provider-routing skills in the current catalog | Domain/project extensions excluded from core; provider routing stays local. |
| `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents` | Execution modes or optional extensions, not required topology. |
| `requesting-code-review`, `receiving-code-review` | Absorbed into Reviewer handoff and correction flow. |
| `test-driven-development` | Optional project/Work Block engineering practice. |
| runtime bootstrap or provider plugin loader skills | Reference-only and excluded from the portable kit. |

No mechanism enters the core merely because a runtime can auto-trigger it. Admission requires a portable procedural purpose, bounded authority, lifecycle relationship, and approved provenance.

## 13. Mission Briefs and Handoffs

A mission brief contains: Work Block and role; objective and output; required inputs and authoritative paths; read scope and write-set; prohibited actions and Hard Stops; selected skills; acceptance and verification; stop conditions; output path and return format.

A handoff records completed work, evidence, deviations, blockers, unresolved questions, and next authorized role. It must not depend on hidden chat history.

A context snapshot is created only when context may be lost through compaction, cross-session transfer, interruption, long-running work, or manual handoff. It is not mandatory when canonical artifacts cheaply reconstruct state.

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

| Path | Purpose | Update trigger | Ownership | Required content | Prohibited content | Retention |
|---|---|---|---|---|---|---|
| `context.md` | Current focus and next gate | open, scope/gate change, closeout | Orchestrator | active Work Blocks, blockers, next gate, links | history dump, transcript, secrets, speculation | Keep current; replace stale state with durable links |
| `progress.md` | Milestone ledger | material completion, blocker, reopen, closeout | Orchestrator | date, Work Block, status, verdict, evidence link | detailed reasoning, copied reports, unsupported success | Append milestones; corrections explicit |
| `decisions.md` | Durable accepted project decisions not fully represented by an ADR | accept, revise, revoke | Architect proposes; Orchestrator records | decision, status, rationale, alternatives, evidence, supersession | hidden reasoning, guesses, credentials, duplicate ADR body | Retain accepted and superseded entries |
| `orchestrator-log.md` | Coordination, authority, approvals, routing, blockers | delegation, transition, approval, blocker, recovery, closeout | Orchestrator | date, Work Block, action, authority basis, result, links | private chain-of-thought, raw prompts, secrets, verbose output | Append concise audit-relevant events |
| `review-log.md` | Index of assurance outcomes | report created or verdict changed | Orchestrator with assurance-role input | artifact, scope, execution mode, verdict, blockers, residual risk | duplicated full reports, unsupported pass | Retain verdict history with correction links |
| `snapshots/` | Compact reconstructable context | conditional snapshot trigger | Orchestrator or delegated role | objective, authority, state, decisions, evidence, next action, links | transcript, scratchpad, secrets, copied large files | Retain referenced snapshots; archive/remove redundant unreferenced snapshots by project policy |

Runtime-local scratch, caches, raw transcripts, temporary traces, tool outputs, and downloads use ignored `.agentic-local/`. The installer adds or verifies the ignore rule without overwriting unrelated `.gitignore` content. Runtime-local state must not be mixed into `memory_bank/` or hold the only accepted decision or evidence.

## 15. Review

Standard and High-Risk work require a Reviewer pass against a frozen diff or final artifact. Quick may use bounded self-review unless independence is required.

A review records: reviewed revision/artifact; inspected and excluded paths; specification/ADR references; severity-ranked findings; applicable security and maintainability observations; evidence limitations; verdict (`APPROVE`, `APPROVE_WITH_CHANGES`, `CHANGES_REQUIRED`, or `BLOCKED`); correction handoff.

Review does not prove runtime behavior. Reviewer does not edit the implementation. Corrections return to a Coder pass and changed surfaces are re-reviewed.

## 16. Verification

Verification maps current-state evidence to acceptance criteria. Standard and High-Risk require a Verifier artifact unless a documented non-independent fallback is explicitly allowed. Quick may embed evidence in the Work Block or closeout.

Fresh evidence is produced or directly observed against the current head, final artifact, or live state being claimed. Relevant changes make earlier evidence stale.

A verification report records: verified identity; each criterion; command/procedure/observation; expected and actual result; pass/fail/blocked/not-applicable; environment limitations; verdict (`READY`, `NOT_READY`, `BLOCKED`, or `UNVERIFIED`).

Fresh evidence is mandatory before claiming completion, requesting final review, claiming PR readiness, recommending merge, or successful closeout. Tests and reviewers cannot approve Hard Stops.

## 17. Closeout

Successful closeout requires:

- implementation inside approved scope;
- required review with no unresolved blocking finding;
- required verification `READY` against current state;
- required Owner approvals;
- synchronized specifications, ADRs, plans, tasks, and derived documentation;
- synchronized memory and logs;
- disclosed residual risks and blocked nonrequired checks;
- follow-up Work Blocks identified without expanding the current one.

Reporting-only closeout is used for blocked, incomplete, unverified, rejected, or superseded work. It records why success was not claimed.

## 18. Git and Owner Approval Boundaries

Explicit Owner approval is required before:

- merge into default/protected branch;
- direct push to default/protected branch;
- production deployment or live restart;
- secret, key, token, credential, or permission changes;
- destructive Git, filesystem, database, or infrastructure operations;
- live database or business-data mutation;
- consequential external communications or transactions;
- material objective, specification, architecture, or scope expansion.

Within an approved Work Block, feature-branch creation, checkpoint/final commits, feature-branch push, PR creation/update, nonconsequential checks, and approved evidence artifacts are allowed unless explicitly restricted.

Opening a PR does not grant merge authority. PR readiness is an assurance statement, not merge approval. Full final verification is not required before each checkpoint commit; it is required before completion/readiness claims.

## 19. Installation

Conceptual interface:

```text
install.py plan --target <repository>
install.py apply --target <repository>
```

### 19.1 Plan

`plan` is mandatory and nonmutating. It supports new and existing repositories, resolves a real repository root, rejects path traversal and symlink escape, inventories candidate files and collisions, compares identities where appropriate, classifies every path as `create`, `skip-identical`, `collision`, or `blocked`, reports bounded `.gitignore` additions, and produces deterministic human- and machine-readable output.

### 19.2 Apply

`apply` consumes or reproduces an unchanged valid plan, refuses unresolved collisions, stages content safely, rechecks target state, creates only planned paths, never silently overwrites/merges/deletes, preserves unrelated content and modes, applies bounded collision-aware `.gitignore` changes, reports `created`, `skipped`, `colliding`, and `blocked`, records files created by the operation, and fails closed on partial or unsafe state.

The installer creates no runtime agents, hooks, plugins, MCP configuration, provider directories, model routing, capability profiles, or duplicated skill mirrors.

## 20. Optional Extensions

Optional and not core:

- nondeterministic output evaluation;
- security/threat-model tooling beyond the core High-Risk trigger;
- browser/UI testing;
- worktree automation;
- Git branch/PR/release finishing;
- external second-model review;
- specialized skill provenance/update tooling;
- MCP, plugins, hooks, runtime profiles, queues, daemons, and provider adapters.

An extension may consume core artifacts but cannot redefine authority, source of truth, process levels, Hard Stops, memory ownership, or closeout. If a Work Block makes an extension required, its failure remains visible.

## 21. Candidate and Promotion Model

Noncanonical candidate:

```text
candidate/portable-agentic-sdlc-kit/
├── CANDIDATE.md
├── template/
├── tools/
└── tests/
```

Candidate content is evidence-bearing but nonauthoritative. Promotion requires successful synthetic installation, HardwareLab pilot, resolved blocking findings, complete verification, and explicit Owner approval.

Promoted canonical distribution:

```text
portable-agentic-sdlc-kit/
├── KIT.md
├── template/
├── tools/
└── tests/
```

The verified candidate moves or is reproduced there without semantic drift. Superseded control-plane/runtime-owned material is archived at `archive/legacy-control-plane/` with provenance and migration notes, not silently deleted. Repository maps must identify exactly one canonical kit after promotion.

## 22. Migration Sequence

### WB-CORE-001 — Normative architecture

- **Objective:** define product boundary, roles, skills, memory, process levels, concurrency, installation, candidate, and migration contract.
- **Expected paths:** only this specification, two ADRs, Work Block plan, and imported Critic review.
- **Dependencies:** current contracts and immutable revisions listed in section 1.
- **Acceptance:** unambiguous architecture; no implementation; branch pushed; PR open and unmerged.
- **Risks:** conflict with current control-plane contracts or accidental candidate authority.
- **Out of scope:** candidate/installer/roles/skills/templates/tests/migrations and final independent verification report.

### WB-CORE-002 — Portable candidate content

- **Objective:** implement portable `AGENTS.md`, roles, nine skills, templates, memory skeleton, and docs skeleton.
- **Expected paths:** `candidate/portable-agentic-sdlc-kit/CANDIDATE.md`, `template/`, and bounded evidence paths.
- **Dependencies:** Owner-approved WB-CORE-001 merge.
- **Acceptance:** candidate matches spec; internal links/contracts pass; no runtime/provider config.
- **Risks:** copying control-plane ownership or duplicating authority.
- **Out of scope:** installer, packaging, pilot, promotion, archive.

### WB-CORE-003 — Installer and packaging

- **Objective:** implement/test plan/apply installer and package candidate without semantic drift.
- **Expected paths:** candidate `tools/`, `tests/`, packaging metadata, bounded evidence.
- **Dependencies:** accepted WB-CORE-002.
- **Acceptance:** collision/path/symlink/staging/no-overwrite tests; explicit results; runtime-neutral output.
- **Risks:** path escape, partial install, silent overwrite, nondeterministic plan.
- **Out of scope:** real-project adoption, promotion, archive.

### WB-CORE-004 — Synthetic dry run

- **Objective:** exercise empty, compatible, colliding, symlinked, and partial targets.
- **Expected paths:** controlled fixtures and reports only.
- **Dependencies:** verified WB-CORE-003.
- **Acceptance:** positive/negative cases; stable repeated plan; apply only planned files; fail-closed safety; recovery evidence.
- **Risks:** unrealistic fixtures or filesystem gaps.
- **Out of scope:** HardwareLab, production use, promotion, legacy removal.

### WB-CORE-005 — HardwareLab pilot

- **Objective:** use candidate for representative Quick, Standard, and High-Risk-classified scenarios without production mutation.
- **Expected paths:** approved HardwareLab feature branch/worktree, pilot reports, explicitly approved candidate corrections.
- **Dependencies:** successful WB-CORE-004 and Owner pilot write-set approval.
- **Acceptance:** collision-safe install; at least two execution modes where feasible; usable memory; fresh review/verification evidence.
- **Risks:** pilot contamination, unapproved production effects, overgeneralizing one project.
- **Out of scope:** production deploy, HardwareLab default-branch merge, automatic rollout, promotion.

### WB-CORE-006 — Promotion and legacy archive

- **Objective:** promote to `portable-agentic-sdlc-kit/`, archive superseded material, and establish one canonical entry path.
- **Expected paths:** canonical kit, `archive/legacy-control-plane/`, maps/registry/README migration notes, final assurance.
- **Dependencies:** successful WB-CORE-005, resolved blockers, complete verification, explicit Owner promotion/merge approval.
- **Acceptance:** unambiguous canonical/archive boundaries; provenance retained; no silent downstream migration; checks pass.
- **Risks:** broken links, dual SSOT, accidental deletion, adoption without consent.
- **Out of scope:** automatic downstream migration, runtime config generation, deletion of legacy evidence.

## 23. Compatibility and Non-Goals

Compatibility is artifact-based. Any agent or human able to read and write the specified artifacts may execute the lifecycle. Native subagents, sequential passes, and manual handoffs are supported modes, not dependencies.

The kit does not guarantee runtime enforcement. Local enforcement may be added outside the kit but is not canonical framework state.

Non-goals:

- orchestrating/installing AI runtimes;
- selecting models/providers;
- configuring permissions, sandboxes, hooks, plugins, or MCP;
- maintaining capability databases or provider snapshots;
- mirroring skills into provider directories;
- running queues, services, or daemons;
- replacing project-specific engineering standards;
- requiring TDD, worktrees, browser tests, external-model review, or evaluation infrastructure for every Work Block;
- automatic merge, deployment, live mutation, or external communication;
- treating candidate as canonical before promotion.

The retained core is the practical artifact chain, role authority, Work Block scope control, distinct review and verification, Hard Stops, truthful evidence, and closeout/memory synchronization. Runtime/provider ownership is not carried forward.

## 24. Acceptance Criteria

- [x] Complete project-kit boundary is defined.
- [x] Runtime/provider ownership is explicitly excluded.
- [x] Six separate portable role contracts are specified.
- [x] Common authority remains canonical in `AGENTS.md`.
- [x] Nine core procedural skills include trigger, inputs, procedure, output, stop/escalation, and lifecycle relationship.
- [x] Relevant current and historical mechanisms have an explicit disposition.
- [x] `memory_bank/` is canonical committed project memory.
- [x] Runtime-local scratch is separate at ignored `.agentic-local/`.
- [x] Quick, Standard, and High-Risk are operationally precise and risk-based.
- [x] Work Block concurrency rules are precise.
- [x] Git and Owner approval boundaries are precise.
- [x] Candidate path and noncanonical status are precise.
- [x] Installer behavior is specified without implementation.
- [x] Optional extensions are separated from core.
- [x] Six migration Work Blocks are bounded with objective, paths, dependencies, acceptance, risks, and out-of-scope boundaries.
- [x] No candidate or installer implementation is part of WB-CORE-001.
- [x] No runtime-specific configuration is required or added.
- [x] Exact framework, historical, and Superpowers revisions are recorded.
- [x] No equal unresolved architectural alternatives remain.
- [ ] Independent PR review and verification are complete.
- [ ] Owner has explicitly approved merge.

The final two criteria remain open until post-PR assurance and a separate Owner merge decision. They do not authorize implementation or promotion.
