# Session Bootstrap

Use this guide at the start of framework maintenance or before a non-trivial
Work Block in a generated project.

## Goal

Load enough current context to act safely without reading the entire repository,
loading every skill/runtime document, or relying on stale memory.

## Progressive Read Strategy

### Always Read

For framework maintenance:

1. active workspace `AGENTS.md`, when present;
2. current task or active Work Block;
3. relevant accepted ADR, specification, and evaluation plan when applicable;
4. current branch, commit, status, and relevant diff;
5. `bootstrap/profiles.json` only when scaffold composition is affected.

For generated-project work:

1. `AGENTS.md`;
2. `.agent/bootstrap-profile.json` when runtime/tool availability matters;
3. active Work Block or current task;
4. approved specification/revision and relevant architecture decisions;
5. approved evaluation plan when required;
6. current repository state.

Installation state is evidence of copied files and selected skills only. It does
not grant Work Block authority, evaluation approval, integration admission,
credentials, live permissions, or runtime capability.

### Read Conditionally

- `governance/*` for authority, lifecycle, artifact, evaluation, or capability rules.
- `.agent/workflows/sdd-protocol.md` for generated-project stage semantics.
- `.agent/ROSTER.md` for logical roles and skill routing.
- the active runtime adapter under `runtimes/`.
- runtime-specific `.codex/`, `.claude/`, `.opencode/`, MCP, plugin, or handoff
  files only when installed/approved and used.
- `docs/evals/` plans/events and `docs/reports/evaluations/` only when bound to the Work Block.
- relevant skills after trigger and installation-profile matching.
- relevant engineering memory and operational logs.
- `PROJECT_MAP.md` and `FILE_REGISTRY.yml` for structural impact.

Do not load all registries, memories, skills, runtime docs, or evaluation logs by
default. Do not treat a deliberately unselected runtime surface as corruption.

## Framework-Maintenance Preflight

Before changing the framework, answer briefly:

- What exact outcome is required?
- Which Work Block and ADR govern the change?
- Does it affect governance, evaluation, installation composition, templates,
  runtime adapters, integrations, skills, or reference knowledge?
- Which artifacts are normative, derived/configuration, evidence, generated, or local?
- Does `bootstrap/profiles.json` need a component, skill-set, alias, or required-path change?
- Which generated-project files must converge?
- What is the approved write-set and current Git state?
- Do bootstrap, validation, profile matrix, evaluation fixtures, conformance,
  navigation, publication, or documentation need updates?
- What review, verification, evaluation, drift, clone/restore, and transactional evidence is required?

## Generated-Project Preflight

Before implementation, answer:

- What requested/resolved installation profile is recorded?
- Which runtime implementation surfaces and skills are actually present?
- Do `scripts/validate-installation-profile.py` and the generated health check pass?
- What governance profile is active?
- What specification/revision and architecture decisions govern the work?
- What paths are in the write-set?
- What runtime is active, and does live capability evidence exist?
- What integration profile/admission is active, if any?
- What actual isolation is available?
- Which logical functions are required?
- Is evaluation required; what plan/rubric/benchmark revisions and event sources apply?
- What Hard Stops, side effects, and assurance evidence apply?

## Authority and Conflict Rules

For framework maintenance:

1. current Owner instruction;
2. accepted framework ADR and active Work Block;
3. `governance/` runtime-neutral rules;
4. `PROJECT_MAP.md` and `FILE_REGISTRY.yml` structural classification;
5. `bootstrap/profiles.json` installation composition;
6. generated template contracts;
7. runtime/integration adapters;
8. reference docs, examples, logs, generated artifacts.

For generated-project product intent:

1. current Owner instruction or approved change request;
2. approved specification;
3. accepted architecture decisions and external contracts;
4. approved implementation and evaluation plans;
5. active tasklist;
6. review, verification, evaluation, drift, and closeout evidence;
7. durable engineering memory;
8. runtime policy, operational logs, generated and external artifacts.

For agent behavior and permission:

1. current Owner instruction;
2. active `AGENTS.md`;
3. runtime-neutral Governance Core;
4. active Work Block scope/write-set/approvals;
5. canonical lifecycle protocol;
6. active runtime and admitted integration adapters;
7. operational logs and generated artifacts.

Installation profile and evaluation scores are not authority layers.

## Evaluation Preflight

When evaluation is required, record:

- evaluation ID, approved plan path/revision, and frozen subject revision;
- deterministic checks and evidence locations;
- output criteria, thresholds, weights, and evaluator types;
- required/prohibited observable trajectory events and event sources;
- rubric, benchmark/dataset, and judge-policy revisions;
- actual runtime/model class/isolation boundary;
- blocking criteria, gaps, and aggregate verdict rule.

Trajectory evidence is limited to observable tool, gate, check, retry, side-effect,
stopping, and artifact events. Never request or store private chain-of-thought,
hidden reasoning, model scratchpads, secrets, or unredacted protected payloads.

An unavailable check/event source is `BLOCKED`, `UNVERIFIED`, or `not_run`, never `pass`.

## Installation and Runtime Capability Check

From `.agent/bootstrap-profile.json`, record:

- requested/resolved installation profile;
- selected components and runtime guidance;
- selected skills and mirrors;
- known unselected runtime surfaces;
- validator result.

Then separately record for the runtime actually used:

- capability available, unavailable, or unknown;
- version/config/auth/smoke evidence;
- actual isolation and observable-event capability;
- fallback and residual limitation;
- whether degraded execution requires later independent evidence.

Static conformance does not prove a live runtime or OS isolation.

## Repository Preflight

```text
Branch:
Commit:
Status:
Unrelated dirty files:
Untracked artifacts:
Installation profile / affected profile manifest:
Installed runtime surfaces:
Active Work Block:
Governing ADR/specification:
Approved implementation/evaluation plans:
Approved write-set:
Affected layers:
Next gate:
```

Inspect relevant uncommitted diffs before planning edits. Never stage or overwrite
unrelated work silently.

## Portable, Operational, and Evidence State

- current source and approved artifacts outrank memory;
- `.agent/bootstrap-profile.json` and `.agent/active-work-block.default.json` are portable;
- `.agent/active-work-block.json`, project config, `memory_bank/`, and runtime memory are local operational state;
- blocked default must be approval-free, integration-free, empty-write-set,
  `closeout_mode=pending`, and contain optional PENDING unbound evaluation state;
- its `coordination_write_set` must exactly match canonical safe paths;
- health checks must not replace an existing active Work Block;
- evaluation plans/reports/events are portable evidence only when secret-free,
  attributable, and explicitly bound to the Work Block;
- durable engineering memory must be evidence-backed and secret-free.

## Structural Impact Check

When adding or redefining important paths, inspect:

- README, setup, maps, and registries;
- Governance Core and accepted ADRs;
- `bootstrap/profiles.json`, bootstrap engine, generated state, clone/transactional tests;
- template operating contracts, evaluation validator, and health checks;
- runtime/integration adapters and conformance tests;
- skill catalog and profile-selected skills;
- publication inventory/privacy rules;
- examples and engineering documentation.

Related files identify impact, not automatic permission.

## Minimal Session Start Record

```text
Stage:
Objective:
Expected result:
Work Block:
Governing ADR/specification:
Installation profile:
Installed runtime surfaces:
Governance profile:
Affected layers:
Runtime adapter and capability evidence:
Integration profile/admission:
Logical role/function:
Isolation:
Scope / out of scope:
Write-set:
Git status:
Hard Stops:
Evaluation required / plan / event sources:
Required assurance:
Relevant files read:
Next action:
```
