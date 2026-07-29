# Agentic SDLC Framework Setup

Setup guide for humans and agents creating projects from the runtime-neutral
framework.

## Quick Start

List installation profiles:

```bash
./bootstrap.sh --list-profiles
```

Create the backward-compatible complete scaffold:

```bash
./bootstrap.sh /path/to/new-project "My Project" my-project
```

Create a lean runtime-neutral scaffold:

```bash
./bootstrap.sh --profile core /path/to/new-project "My Project" my-project
```

Create a single-runtime scaffold:

```bash
./bootstrap.sh --profile codex /path/to/new-project "My Project" my-project
```

Then:

```bash
cd /path/to/new-project
git init
git add -A
git commit -m "Initial scaffold from Agentic SDLC Framework"
bash scripts/bootstrap.sh
```

The default profile is `multi-runtime`. Aliases:
`minimal`/`generic` → `core`; `full` → `multi-runtime`.

## What Bootstrap Does

The installer:

- validates `bootstrap/profiles.json` before target mutation;
- rejects unknown profiles, unsafe/missing paths, non-empty and symlink targets;
- builds in a sibling staging directory and publishes atomically;
- copies common Governance Core and portable workflow files;
- prunes unselected runtime implementation surfaces;
- installs selected skill sets and runtime mirrors;
- includes evaluation governance, templates, and validator in every profile;
- writes `.agent/bootstrap-profile.json`;
- runs the generated profile-aware health check.

It does **not** install or authenticate runtimes, providers, plugins, MCP servers,
LM judges, credentials, browsers, watchers, or services. Installation composition
does not grant Work Block authority, integration admission, or evaluation approval.

Rerun the generated health check after clone/restore:

```bash
bash scripts/bootstrap.sh
```

The health check validates the portable blocked default before restoring ignored
operational state. The default must remain write-blocked, approval-free,
integration-free, empty-write-set, `closeout_mode=pending`, and contain optional
unbound `PENDING` evaluation state.

## Installation Profiles

Source: `bootstrap/profiles.json`. Guide: `docs/bootstrap-profiles.md`.

The `core` skill set includes `skill-library-maintenance` for controlled
GitHub skill discovery and Owner-approved adaptation.

| Profile | Project-local implementation surfaces |
|---|---|
| `core` | none; generic runtime guidance only |
| `codex` | `.codex/` |
| `claude-code` | `CLAUDE.md`, `.claude/` |
| `opencode` | `opencode.json`, `.opencode/` |
| `multi-runtime` | all bundled runtime surfaces plus empty `.mcp.json` |

Every generated project contains:

```text
.agent/bootstrap-profile.json
scripts/validate-installation-profile.py
scripts/validate-evaluation.py
governance/evaluation.md
docs/evals/README.md
docs/reports/evaluations/README.md
docs/templates/evaluation-plan-template.json
docs/templates/evaluation-report-template.json
docs/templates/trajectory-event-template.json
```

These files provide evaluation capability, not a requirement or passing verdict.
The active Work Block decides whether evaluation is required.

## Architecture Layers

1. **Governance Core** — `AGENTS.md` and `governance/` define authority,
   lifecycle, artifacts, evaluation, capabilities, Hard Stops, and closeout.
2. **Portable workflow** — `.agent/`, specs, implementation/evaluation plans,
   tasks, reports, selected skills, memory, and observable evidence.
3. **Runtime adapters** — documentation under `runtimes/`; local surfaces only
   when selected by installation profile.
4. **Integration adapters** — optional plugins, MCP, external CLIs, hosted tools,
   and audited file transport under `integrations/`.

Installation/runtime/model/integration/evaluator selection never changes logical
role authority.

## First Session

Read progressively:

```text
AGENTS.md
.agent/bootstrap-profile.json
active Work Block
approved specification and architecture decisions
approved evaluation plan when required
PROJECT_MAP.md / FILE_REGISTRY.yml when navigation is needed
selected runtime adapter
selected integration adapter only when admitted
```

Do not load every skill, runtime, integration, event log, and memory file by default.

## Select Work Block Profiles

For each Work Block select independently:

```yaml
governance_profile: Managed
runtime_profile: codex
integration_profile: none
model_class: balanced_engineering
isolation: separate_session
evaluation_posture: required
approved_evaluation_plan: docs/evals/feature-x/plan.json
```

Start with the smallest sufficient governance profile and no external integration.
Determine evaluation from risk, non-determinism, autonomous tool selection,
consequences, and acceptance criteria—not from vendor/model name.

## Evaluation Setup

### Decide whether evaluation is required

Evaluation is normally required when:

- output is materially non-deterministic;
- the agent chooses tools or execution paths autonomously;
- trajectory/process compliance is an acceptance condition;
- consequential automation depends on correct gate/tool behavior;
- a benchmark, dataset, rubric, or LM judge is part of acceptance;
- the selected governance profile requires stronger evidence.

When deterministic checks and standard review/verification fully prove the result,
evaluation may be optional or not required, but the Work Block must record why.

### Create an approved plan

Copy:

```text
docs/templates/evaluation-plan-template.json
```

Recommended location:

```text
docs/evals/<evaluation-id>/plan.json
```

Define:

- exact Work Block and frozen subject revision;
- deterministic checks and evidence;
- output criteria, thresholds, weights, evaluator types;
- required/prohibited observable trajectory events and event sources;
- rubric and benchmark/dataset revisions;
- LM-judge policy and calibration when applicable;
- required isolation and aggregate verdict rule.

Validate before use:

```bash
python scripts/validate-evaluation.py plan \
  docs/evals/<evaluation-id>/plan.json \
  --require-approved
```

Changing criteria, thresholds, datasets, judge policy, or required events after
observing results creates a new plan revision.

### Record observable trajectory evidence

Use `docs/templates/trajectory-event-template.json` as a shape guide. Store only
observable events such as tool calls/results, gate decisions, commands, tests,
retries, failures/recoveries, side-effect attempts, stopping conditions, and
produced artifacts.

Do not collect private chain-of-thought, hidden reasoning, model scratchpads,
secrets, credentials, or unredacted protected payloads.

### Produce and validate the report

Copy:

```text
docs/templates/evaluation-report-template.json
```

Recommended location:

```text
docs/reports/evaluations/<evaluation-id>.json
```

Validate it against the approved plan:

```bash
python scripts/validate-evaluation.py report \
  docs/reports/evaluations/<evaluation-id>.json \
  docs/evals/<evaluation-id>/plan.json
```

Per-check states are `pass`, `fail`, `blocked`, `not_run`, or `not_applicable`.
Aggregate verdicts are `READY`, `BLOCKED`, or `UNVERIFIED`.

A deterministic requirement cannot pass solely through an LM judge. A trajectory
criterion cannot pass with missing required events or observed prohibited events.

### Bind evaluation to closeout

The active Work Block records:

```json
"evaluation": {
  "required": true,
  "status": "READY",
  "verdict": "READY",
  "plan": "docs/evals/<id>/plan.json",
  "report": "docs/reports/evaluations/<id>.json",
  "rubric_revision": "1",
  "benchmark_revision": "dataset-v1",
  "isolation": "separate-session",
  "skip_reason": ""
}
```

Validate Work Block binding:

```bash
python scripts/validate-evaluation.py closeout .
```

Required evaluation cannot be skipped and must be `READY` for
`success-closeout`. Optional skipped evaluation requires a concrete reason.

## Runtime Setup

### Codex

Project-local Codex files exist in `codex` and `multi-runtime` installations.
Install/authenticate outside the repository, review hooks/config, populate the
active Work Block, and run safe adapter/read-only smoke. Concrete provider/model/
auth configuration remains local.

### Claude Code

Project-local Claude files exist in `claude-code` and `multi-runtime`. The
baseline contains logical-role agents only. Shared machine gates enforce source
writes, Hard Stops, review, verification, required evaluation, drift, and closeout.

### OpenCode

Project-local OpenCode files exist in `opencode` and `multi-runtime`. The baseline
uses explicit permissions, read-only assurance roles, denied consequential shell
commands, empty MCP/plugin collections, and no public model pin. Run target smoke
before Managed or higher-governance work.

### Generic / Sequential

Generic guidance is always present. Perform logical functions as separate
documented passes and record reduced independence or missing observable-event
capability honestly.

## Integration Admission

No profile activates an external integration. Before enabling a plugin, MCP
server, external runtime CLI, hosted connector, or file runner:

1. fill `docs/templates/integration-admission-template.md`;
2. identify exact functions/tools and authority;
3. record network, external-directory, data, and secret boundaries;
4. classify side effects and Hard Stops;
5. define timeout, cancellation, retry, recovery, logging, and disable procedure;
6. run allowed and denied smoke fixtures;
7. bind integration ID and evidence path to the active Work Block.

Admission does not grant child write authority. Evaluation does not grant admission.

## Work Block Setup

Create non-trivial Work Blocks from:

```text
docs/templates/work-block-template.md
```

Record objective, done criteria, spec/revision, architecture baseline, scope,
write-set, Git state, risks, Hard Stops, runtime capability/isolation, function
bindings, integration admissions, implementation/evaluation plans, evidence paths,
and closeout state.

`.agent/active-work-block.json` is executable authority/gate state.
`.agent/bootstrap-profile.json` records installation only.

## Smoke Checks

### Generated-project health

```bash
bash scripts/bootstrap.sh
```

### Framework contracts

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-evaluation-contracts.py
python scripts/test-bootstrap-profiles.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

### Runtime smoke

For each selected runtime prove:

- role instructions load;
- source writes are blocked without valid Work Block state;
- in-scope writes proceed only when approved;
- out-of-scope/consequential actions are denied or Owner-gated;
- read-only roles cannot change implementation source;
- required Review/Verification/Evaluation evidence can be produced;
- actual runtime version, event sources, isolation, and limitations are recorded.

Static conformance does not prove live runtime behavior or OS isolation.

### Integration smoke

For admitted integrations prove exact allowed/denied tools, no committed secrets,
harmless denied-write failure, timeout/cancel/recovery, and result identity/
revision/scope/evidence. Do not run paid/live smoke automatically in bootstrap/CI.

## Changing an Existing Project's Installation Composition

Bootstrap is not an in-place upgrader. Create a migration Work Block, compare a
disposable generated project, copy/remove only approved surfaces and skills,
regenerate profile state consistently, validate it, smoke the runtime, and assure
the migration diff.

## Publication and Local State

Before publishing inspect `.agent/`, runtime configs/memory, `memory_bank/`,
handoff state, provider/plugin config, MCP arguments/environment names, event
logs, local paths, downloaded packages, generated output, transcripts, personal/
live data, and mutation permissions.

Never commit secret values, hidden reasoning, or unredacted protected payloads.

## Further Reading

- `README.md`
- `PROJECT_MAP.md`
- `docs/bootstrap-profiles.md`
- `docs/profiles.md`
- `governance/README.md`
- `governance/evaluation.md`
- `runtimes/README.md`
- `integrations/README.md`
- `handoff/README.md`
