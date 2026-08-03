---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003b-self-hosting-control-plane-reconciliation
work_block_id: WB-CORE-003B
status: completed
owner_role: orchestrator
created_at: 2026-08-03
base_revision: cb952348dc0fb40b4a63b419612fa93a3932e84c
branch: agent/wb-core-003b-self-hosting-reconciliation
process_level: Managed
---

# WB-CORE-003B — Self-Hosting Control-Plane Reconciliation

## Objective and authority

Reconcile the framework's locally drafted self-hosting control-plane work with
the accepted `main` baseline, then deliver one traceable, runtime-neutral
operational layer for framework maintenance. The result must provide root
authority, SDD procedure, durable and operational memory, role routing, a
delegation template, and capability-aware but provider-neutral routing guidance
without changing the Portable Kit's accepted product boundary.

The Owner approved this reconciliation through Define, Execute, Assure, and
Close on 2026-08-03. That approval does not authorize hooks, runtime adapters,
installer work, dependencies, configuration, candidate promotion, staging,
commit, push, merge, or any external side effect.

Authority order is: current Owner instruction; root `AGENTS.md` and accepted
governance; accepted specification and ADRs; this Work Block; then evidence and
operational memory. Local, untracked WB-CORE-004 and WB-CORE-005 artifacts are
reference inputs only. They are not accepted history and must not be copied as
such.

## Composition boundary

This Work Block has one verifiable outcome: an internally consistent,
authoritative, self-hosting control-plane layer that an agent can retrieve and
apply from the accepted repository baseline. Its documentation, role routing,
memory, navigation, and evidence share one risk boundary (authority drift), one
integrated write-set, one rollback boundary, and one assurance chain. Splitting
them would leave either an unreferenced operational procedure or a false SSOT
claim.

The work is not split because no component is independently releasable, needs a
distinct Owner approval or Hard Stop, has conflicting Coder ownership, requires
separate rollback, or can be meaningfully assured apart from the integrated
authority chain. The future installer, synthetic dry-run, HardwareLab pilot,
promotion, hooks, and runtime adapters remain separately bounded Work Blocks.

## Material process finding

- **Observed condition:** local drafts claimed the self-hosting layer was
  installed and verified while the accepted `main` baseline had neither those
  files nor matching `PROJECT_MAP.md` / `FILE_REGISTRY.yml` lifecycle state.
- **Category:** authority and evidence quality.
- **Concrete impact:** an agent could follow unaccepted local policy or treat
  unsupported `READY` claims as canonical assurance.
- **Evidence:** read-only reconciliation review of the dirty legacy worktree
  against `origin/main` at `cb952348dc0fb40b4a63b419612fa93a3932e84c`.
- **Disposition:** rebuild a single clean, evidence-backed subject as
  WB-CORE-003B; retain the drafts only as selectively reviewed input.

## Scope and write boundaries

### Define-stage authority

Only this Work Block and its tasklist may be created or edited during Define.
No Coder write gate is open until the Critic returns `READY` and the exact
delivery set below remains valid.

### Initial Execute delivery set — one Coder

```text
AGENTS.md
.agent/workflows/sdd-protocol.md
.agent/ROSTER.md
.agent/skills/README.md
docs/templates/subagent-mission-brief-template.md
docs/engineering-memory/README.md
docs/engineering-memory/source-of-truth-chains.md
docs/engineering-memory/reproducibility-log.md
docs/engineering-memory/temporary-decisions.md
docs/engineering-memory/decision-record-template.md
memory_bank/README.md
memory_bank/context.md
memory_bank/progress.md
memory_bank/decisions.md
memory_bank/orchestrator-log.md
memory_bank/review-log.md
docs/plans/wb-core-003b-self-hosting-control-plane-reconciliation.md
docs/tasklist/wb-core-003b-self-hosting-control-plane-reconciliation.md
```

The Coder must selectively adapt only compatible draft content, preserve the
accepted WB-CORE-003A rules, and include a runtime-neutral capability-selection
rule. Before delegation, the Orchestrator must establish live evidence that an
option is available; `unknown` is not available. It may select the least-cost
option only from choices that already satisfy the Work Block's role authority,
write permission, required independence and isolation, assurance level, and
Hard Stops. Cost must never justify weaker assurance. The rule must not name,
lock, configure, or promise any provider, model, tool, or runtime.

The initial frozen normative subject is exactly the twelve non-`memory_bank/`
paths above. It explicitly excludes `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, and
all `docs/reports/**` evidence. `memory_bank/**` is delivered and
schema-reviewed alongside it, but is operational lower-authority state and is
not a status-bearing input to the final normative-subject verdict.

### Later final-assurance projection authority — Orchestrator

Only after preliminary assurance is ready, a distinct final-assurance
projection
subject may include:

```text
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/plans/wb-core-003b-self-hosting-control-plane-reconciliation.md
docs/tasklist/wb-core-003b-self-hosting-control-plane-reconciliation.md
```

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` are approved later final-assurance
projection normative paths, not part of the initial Execute subject.
This preserves their approved write authority without implying that the initial
Coder froze, validated, or updated them.

### Assurance and closeout authority

```text
docs/reports/reviews/wb-core-003b-critic.md
docs/reports/reviews/wb-core-003b-preliminary-review.md
docs/reports/verification/wb-core-003b-preliminary-verification.md
docs/reports/reviews/wb-core-003b-drift-assessment.md
docs/reports/reviews/wb-core-003b-independent-review.md
docs/reports/verification/wb-core-003b-verification.md
docs/reports/closeout/wb-core-003b-self-hosting-control-plane-reconciliation.md
```

The Critic evidence is recorded in Define from its separate-subagent review.
Reviewer, Verifier, and the final documentation-drift assessment are read-only
and must not alter the frozen normative subject. The Orchestrator records their
independent findings faithfully in the evidence-only reports after receiving
their outputs; it must not alter a finding's verdict, scope, or cited evidence.
The Orchestrator writes the closeout report only after final assurance is
complete.

`memory_bank/` is operational, lower-authority state rather than normative
navigation. The Coder creates its schema and initial truthful state; the
Orchestrator may append factual report links and change current context at
Close. Those derived operational entries do not alter the reviewed normative
subject, but must preserve the reviewed schema and never claim a verdict not
present in its linked report.

### Out of scope

- installer and packaging work reserved for WB-CORE-004, synthetic dry-run
  reserved for WB-CORE-005, HardwareLab pilot, promotion, and legacy archive;
- hooks, machine-enforced gates, scripts, CI, runtime adapters, provider/model
  configuration, skills implementations, skill mirrors, dependencies, secrets,
  integrations, deployment, data mutation, and destructive actions;
- alteration, deletion, staging, commit, push, merge, or rewriting of the
  legacy dirty worktree and its unaccepted historical WB identifiers.

## Risk, topology, and hard stops

- **Profile:** Managed; **side-effect class:** local documentation;
  **evaluation:** not required.
- **Topology:** this clean worktree has one active write-capable Work Block and
  exactly one Coder during Execute. Critic, Reviewer, and Verifier are required
  as `separate_subagent` read-only contexts. If that capability has no live
  evidence, use a separately started top-level session; if that is unavailable,
  stop `BLOCKED`. Same-context assurance is not a permitted fallback for this
  Managed Work Block without a new Owner-approved profile change.
- **Primary risk:** accidentally promote local drafts, regress accepted
  WB-CORE-003A policy, or introduce provider-specific governance.
- **Hard stops:** any need to expand the write-set, introduce runtime/config/
  hook/CI/installer work, modify an unrelated artifact, encounter a failed
  required check, or stage/commit/push requires a return to the Owner.

## Acceptance and assurance

1. The delivered layer is reachable from `AGENTS.md`, subordinate to accepted
   governance, and does not establish a competing authority chain.
2. The SDD procedure, role roster, mission template, durable memory, and
   operational memory have explicit responsibilities, update rules, isolation,
   and truthful limitations.
3. Capability selection is runtime-neutral: availability is inspected live and
   the least-cost capable option is selected without a static provider catalog.
4. The Portable Kit remains noncanonical and retains its separate-role ADR
   boundary; the compact framework roster is explicitly an operational index.
5. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` describe the accepted current
   lifecycle state, WB-CORE-003A rules, WB-CORE-003B, and future product WBs
   without copying mutable assurance verdicts.
6. Preliminary and final frozen subjects pass documentation, SDD, governance,
   structural, cross-reference, whitespace, and changed-path checks;
   independent Critic, Review, Verification, and documentation-drift evidence
   records actual isolation and verdicts.

## Lifecycle plan

1. **Define:** inventory accepted baseline and local draft inputs; record this
   composition decision, finding, exact write-set, and evidence plan.
2. **Critic gate:** independently challenge scope, authority, Portable Kit
   boundary, capability rule, evidence model, and hard stops. A `RECONSIDER` or
   `BLOCKED` verdict returns the plan to Define.
3. **Execute:** one Coder selectively implements the initial normative subject
   and operational-memory schema. It represents WB-CORE-003B as active and
   assurance pending, never as successfully closed.
4. **Preliminary assure:** independent Reviewer and Verifier assess that frozen
   initial subject. If either is not `READY`, return to Define.
5. **Final-assurance projection:** after preliminary `READY`, the Orchestrator
   updates only the predeclared plan/tasklist and `PROJECT_MAP.md` /
   `FILE_REGISTRY.yml` final-assurance lifecycle projection. That new projection is a
   distinct final normative subject; it invalidates preliminary readiness by
   design.
6. **Final assure:** independent Reviewer and Verifier assess the exact final
   normative subject; a separate documentation-drift assessment checks the
   durable documents, navigation, registry, and operational records for
   contradictions. The Orchestrator faithfully records their read-only outputs
   in evidence-only reports. Any normative change then returns the Work Block
   to Define.
7. **Close:** write an evidence-only closeout, update derived operational memory
   from the final reports, report residual risks, and stop for separate Owner
   approval before any staging, commit, push, or merge.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic documentation and contract validation are sufficient
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

Final independent Reviewer and Verifier assurance and the separate
documentation-drift assessment were recorded on 2026-08-03 against the active
final-assurance projection. The repository closeout evidence is
`docs/reports/closeout/wb-core-003b-self-hosting-control-plane-reconciliation.md`.
This completed repository lifecycle state does not claim staging, commit, push,
merge, promotion, installation, deployment, release readiness, or mutable
external VCS status. Any later normative change requires a new applicable Work
Block and assurance chain.
