# GitHub Spec Kit Benchmark — 2026-08-14

## Status

Research artifact only. This document does not change framework authority,
lifecycle, runtime configuration, bootstrap behavior, or release state.

## Objective

Compare current GitHub Spec Kit capabilities with the Agentic SDLC Framework,
identify concrete gaps, and select only the mechanisms that improve the local
framework without introducing a second source of truth or replacing the existing
authority model.

The benchmark follows `governance/decision-provenance.md`. External frameworks
are research inputs, not project authority.

## Upstream snapshot

- Project: `github/spec-kit`
- Reviewed revision: `bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`
- Snapshot date: 2026-08-14
- Primary reviewed paths:
  - `docs/reference/agentic-sdd.md`
  - `docs/reference/overview.md`
  - `docs/quickstart.md`
  - `templates/commands/checklist.md`
  - `templates/tasks-template.md`
  - `docs/guides/evolving-specs.md`

The immutable revision is the evidence baseline for this benchmark. Future
Spec Kit changes do not silently change the conclusions below.

## Executive finding

Spec Kit and the Agentic SDLC Framework overlap in the specification-first part
of development but optimize for different control problems.

Spec Kit is currently stronger as an **SDD interaction and decomposition
frontend**: it provides a polished progression from natural-language intent to a
specification, targeted clarification, requirements-quality review, planning,
dependency-aware tasks, cross-artifact analysis, implementation, and convergence.

The Agentic SDLC Framework is stronger as a **runtime-neutral delivery control
plane**: authority, Work Blocks, write sets, role separation, Hard Stops,
risk-based assurance, deterministic/output/trajectory evaluation, specification
drift, release-state reconciliation, and fail-closed closeout remain local
framework responsibilities.

The recommended direction is therefore selective adaptation, not installation of
Spec Kit as a second governance system.

## Capability comparison

| Capability | Spec Kit mechanism | Current local position | Decision | Provenance if changed |
|---|---|---|---|---|
| Project principles | `constitution` drives later phases | Governance Core and project operating contracts already have higher authority and broader scope | KEEP LOCAL; do not introduce a second constitution | n/a |
| Intent before implementation detail | `specify` focuses on what/why; technical choices belong in `plan` | Already a normative local rule | KEEP LOCAL | n/a |
| Targeted ambiguity resolution | `clarify` asks up to five focused questions and writes answers back to `spec.md` | Architect/Critic can discover ambiguity, but there is no equally explicit reusable clarification protocol | ADAPT | `adapted` from Spec Kit |
| Requirements-quality review | `checklist` treats the requirements themselves as the test subject and separates reviewer approval from implementation completion | Critic covers some of this, but requirements quality is mixed with architecture/risk critique | ADAPT | `adapted` from Spec Kit |
| Plan generation | `plan` turns approved intent into technical design artifacts | Local implementation plan is richer in authority, write-set, topology, risk, rollback, verification and evaluation | KEEP LOCAL; borrow UX only when useful | n/a |
| Task decomposition | `tasks` uses Setup, Foundational, per-user-story phases, dependency order and parallel markers | Local task decomposition supports write sets and parallel Coder topology but is less prescriptive about traceable task shape | ADAPT | `adapted` from Spec Kit |
| Pre-execution consistency | `analyze` is read-only across spec/plan/tasks and sends fixes back to the owning artifact | Critic and drift logic cover related concerns but pre-execution traceability is not as explicit | ADAPT | `adapted` from Spec Kit |
| Implementation gate | `implement` reads checklist state and asks before proceeding when quality items remain open | Local write gate is stronger and tied to Work Block authority; Owner/Critic/Hard Stop state cannot be replaced by checklist state | REJECT DIRECT; preserve local gate | n/a |
| Implementation execution | `implement` executes dependency-ordered tasks and respects parallel markers | Coder execution is already bounded by approved write set and topology | KEEP LOCAL; task metadata may improve routing | n/a |
| Post-implementation completeness | `converge` compares code against spec/plan/tasks and appends missing tasks | Local Verifier + drift audit cover a broader graph including architecture, tests/evals and documentation | ADAPT LOOP ONLY; do not replace drift/verification | `adapted` from Spec Kit |
| Feature state independent of Git | `.specify/feature.json` identifies active feature without requiring a branch | Local active Work Block already separates lifecycle authority from mutable GitHub state | KEEP LOCAL | n/a |
| Runtime integrations | one active coding-agent integration can be switched | Local runtime profiles intentionally support runtime-neutral and multi-runtime topologies | REJECT DIRECT | n/a |
| Extensions/presets | composable command/template/script customization | Local skills, runtime adapters, integrations and bootstrap profiles solve adjacent problems with stronger authority separation | DEFER FOR SECOND BENCHMARK | unresolved |
| Workflows | command/prompt/shell/human-checkpoint automation with conditions, loops, fan-out/fan-in and resume | Potentially useful implementation reference for orchestration UX, but local lifecycle authority must remain separate | DEFER FOR SECOND BENCHMARK | unresolved |
| Bundles | versioned composition of extensions/presets/workflows with conflict/provenance handling | Potentially relevant to installation profiles and curated capability packs | DEFER FOR SECOND BENCHMARK | unresolved |

## Candidate adaptations

### 1. Requirements Clarification Protocol

**Decision:** ADAPT.

Spec Kit makes ambiguity resolution a first-class phase rather than relying on a
planner to notice missing information while already designing the solution. The
useful principle is not the slash command itself; it is the explicit contract:

1. inspect the approved/raw specification for high-impact ambiguity;
2. ask a small bounded set of targeted questions;
3. write the accepted answers back into the authoritative specification;
4. repeat only when material ambiguity remains;
5. block architecture/implementation decisions that depend on unresolved answers.

Local delta required:

- integrate with Owner/Architect authority rather than Spec Kit constitution;
- distinguish blocking questions from questions that may be resolved by an
  explicit assumption;
- record assumptions and unanswered questions in the Work Block;
- remain compatible with Quick Fix and risk-tiered profiles;
- do not force user interaction for facts that repository discovery can resolve.

**Provenance:** `adapted` from GitHub Spec Kit `clarify`.

### 2. Requirements Quality Gate

**Decision:** ADAPT.

The strongest Spec Kit idea in this benchmark is the explicit distinction
between **testing requirements quality** and testing implementation behavior.
Requirements review should ask whether requirements are complete, clear,
consistent, measurable and sufficiently covered before source work begins.

Local delta required:

- make it a requirements-quality artifact/function, not a source-write authority;
- keep Critic responsible for broader scope, architecture, risk, verification and
  evaluation challenge;
- allow domain-focused checklists such as API, security, UX, data and operations;
- require human/independent review where the selected governance profile demands
  it;
- never treat a checked requirements item as evidence that code works.

**Provenance:** `adapted` from GitHub Spec Kit `checklist`.

### 3. Requirement-to-Task Traceability

**Decision:** ADAPT.

Spec Kit's task model makes execution structure visible: blocking foundational
work, user-story phases, dependency order and explicit parallelizable tasks. The
local framework should borrow the traceability discipline without replacing
write sets.

Candidate local task metadata:

```yaml
id: T-012
requirement_ids: [REQ-004, REQ-007]
work_block: WB-XXX
write_set: [path/a, path/b]
depends_on: [T-009]
parallelizable: true
acceptance_ids: [AC-006]
verification: targeted-test-name
```

This would let the Orchestrator derive safe parallel topology from both
dependencies and write-set overlap instead of inferring it from prose.

**Provenance:** `adapted` from GitHub Spec Kit `tasks`.

### 4. Pre-Execution Artifact Analysis

**Decision:** ADAPT.

Add an explicit read-only consistency pass before the write gate for Managed or
higher work when separate specification/plan/task artifacts exist.

Minimum questions:

- does every blocking requirement have implementation coverage?
- does every planned behavior trace to an approved requirement or architecture
  decision?
- does every task trace to a requirement, plan item or required assurance action?
- do plan or tasks silently contradict the specification?
- are unresolved ambiguities being converted into implementation assumptions?
- do dependencies and proposed parallel tasks conflict with write-set ownership?

The pass should report findings and route remediation back to the authoritative
artifact. It must not silently rewrite the specification.

**Provenance:** `adapted` from GitHub Spec Kit `analyze`.

### 5. Convergence Feedback Loop

**Decision:** ADAPT LOOP ONLY.

Spec Kit's append-only convergence loop is useful because a completeness scan can
turn discovered omissions into explicit remaining work. The local framework
already has a stronger assurance model, so the adaptation should live beneath
Verifier/drift rather than replace them.

Candidate behavior:

```text
frozen implementation
  -> verification + drift comparison
  -> missing approved implementation?
       yes -> create corrective tasks / reopen Execute
       no  -> continue assurance and closeout
```

Local delta required:

- findings are classified using the existing drift taxonomy;
- new tasks cannot silently change the approved specification;
- `UNSPECIFIED_IMPLEMENTATION` routes to specification/Owner decision, not merely
  task creation;
- `MISSING_IMPLEMENTATION` may produce corrective tasks;
- failed tests/evaluations remain assurance failures rather than generic tasks;
- convergence never grants READY by itself.

**Provenance:** `adapted` from GitHub Spec Kit `converge`.

## What should not be imported

### A second constitution

The local Governance Core, project operating contract, approved specifications,
ADRs and Work Blocks already define source-of-truth order. A generated Spec Kit
constitution would either be subordinate derived material or create an ambiguous
second policy layer. There is no current benefit that justifies the duplication.

### A second lifecycle/state machine

`.specify/feature.json`, Spec Kit command sequencing and checklist state must not
become lifecycle authority. The active Work Block and local lifecycle remain the
control plane.

### Checklist-driven write authority

Requirements-quality completion is useful evidence but cannot grant source write,
external integration, credential, production, destructive or publication
authority.

### Same-agent convergence as final assurance

A fluent implementation agent deciding that its own implementation converged is
not a substitute for the selected review, verification, evaluation or drift
independence requirements.

## Proposed local Define flow

The benchmark suggests a refinement of Stage 0 rather than a new lifecycle:

```text
Owner objective / change request
        |
        v
Specification framing
        |
        v
Targeted clarification  [candidate adaptation]
        |
        v
Requirements quality review  [candidate adaptation]
        |
        v
Architecture + implementation/evaluation planning
        |
        v
Requirement-linked task decomposition  [candidate adaptation]
        |
        v
Read-only cross-artifact analysis  [candidate adaptation]
        |
        v
Critic + existing authority/risk gates
        |
        v
WRITE GATE READY
```

This preserves the existing Define -> Execute -> Assure -> Close lifecycle while
making the front of Define more deterministic and easier for both users and
agents to operate.

## Practical pilot recommendation

Do not install Spec Kit into the framework repository for the first experiment.
Instead, use a disposable sample project and compare two runs on the same feature
brief:

1. **Baseline:** current Agentic SDLC Define process.
2. **Reference:** stock Spec Kit at the pinned revision.
3. Compare:
   - number and quality of ambiguities surfaced before coding;
   - requirement completeness;
   - acceptance-criterion measurability;
   - requirement -> task coverage;
   - amount of unsupported agent assumption;
   - task dependency/parallelism quality;
   - post-implementation omissions;
   - user interaction burden;
   - token/context overhead.
4. Use the results to design framework-native adaptations.

The pilot should test the mechanisms rather than proving that one framework is
"better" overall.

## Initial priority

Recommended adoption order:

1. targeted clarification protocol;
2. requirements-quality gate;
3. requirement/task traceability;
4. read-only pre-execution artifact analysis;
5. convergence feedback integrated with Verifier/drift.

Extensions, presets, workflows and bundles deserve a separate architecture
benchmark after the SDD front-end mechanisms are evaluated.

## Benchmark provenance

- **Classification:** research only; no framework mechanism is adopted by this
  document itself.
- **Sources:** GitHub Spec Kit at
  `bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`.
- **Internal evidence:** current Governance Core, portable artifact contract,
  runtime-neutral SDD protocol and existing drift/evaluation model.
- **Local delta:** candidate adaptations preserve local authority, Work Blocks,
  write sets, risk gates and assurance rather than installing Spec Kit as a
  parallel control plane.
- **Novelty claim:** none.
