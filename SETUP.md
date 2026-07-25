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
```

The default profile is `multi-runtime`, preserving the previous maximum
scaffold. Aliases: `minimal`/`generic` → `core`; `full` → `multi-runtime`.

## What Bootstrap Does

The installer:

- validates `bootstrap/profiles.json` before target mutation;
- rejects unknown profiles, unsafe paths, missing components/skills, and non-empty
  targets;
- copies the common portable template and Governance Core;
- keeps runtime/integration documentation available in every project;
- prunes unselected runtime implementation surfaces;
- installs the selected skill sets and runtime mirrors;
- writes `.agent/bootstrap-profile.json`;
- replaces placeholders using literal character-safe replacement;
- makes installed hooks/scripts executable;
- runs the generated-project profile-aware health check.

It does **not** install or authenticate Codex, Claude Code, OpenCode, plugins,
MCP servers, providers, browsers, watchers, or services. Installation
composition does not grant Work Block authority or integration admission.

Rerun the generated health check after moving or restoring a project:

```bash
bash scripts/bootstrap.sh
```

## Installation Profiles

Source: `bootstrap/profiles.json`.

Guide: `docs/bootstrap-profiles.md`.

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
```

The profile state records selected components, runtimes, skills, required paths,
and known unselected paths. It is generated installation evidence, not an
approval file.

## Architecture Layers

The generated project separates:

1. **Governance Core** — `AGENTS.md` and `governance/` define authority,
   lifecycle, artifacts, capabilities, Hard Stops, and closeout.
2. **Portable workflow** — `.agent/`, specifications, plans, tasks, reports,
   selected skills, and memory coordinate the work.
3. **Runtime adapters** — documentation under `runtimes/`; project-local runtime
   surfaces only when selected by installation profile.
4. **Integration adapters** — optional plugins, MCP, external runtime CLIs,
   hosted tools, and audited file transport under `integrations/`.

Installation/runtime/model/integration choice never changes logical role
authority.

## First Session

Read progressively:

```text
AGENTS.md
.agent/bootstrap-profile.json
active Work Block, when present
approved specification and architecture decisions
PROJECT_MAP.md / FILE_REGISTRY.yml when navigation is needed
selected runtime adapter
selected integration adapter only when required
```

Do not treat a deliberately unselected runtime surface as missing/corrupt state.
Do not load every skill, runtime, integration, and memory file by default.

## Select Work Block Profiles

Installation profile is already recorded. For each Work Block use
`docs/profiles.md` and select independently:

```yaml
governance_profile: Managed
runtime_profile: codex
integration_profile: none
model_class: balanced_engineering
isolation: separate_subagent
```

Start with the smallest sufficient governance profile and
`integration_profile: none`. A runtime may be documented but not installed; a
surface may be installed but unavailable because CLI/auth/config is missing.
Record actual capability evidence.

## Runtime Setup

### Codex

Project-local Codex files exist in `codex` and `multi-runtime` installations.
Read:

```text
runtimes/codex/README.md
.codex/config.toml.template
.codex/hooks.json
.codex/agents/
```

Activation:

1. install/authenticate Codex outside the repository;
2. review project hooks and agent files;
3. copy `.codex/config.toml.template` to `.codex/config.toml` only when desired;
4. populate `.agent/active-work-block.json`;
5. run safe adapter fixtures/read-only smoke;
6. trust project hooks deliberately.

Concrete model/provider/auth settings remain user-local.

### Claude Code

Project-local Claude files exist in `claude-code` and `multi-runtime`
installations. Read:

```text
CLAUDE.md
runtimes/claude-code/README.md
.claude/settings.json
.claude/agents/
.claude/hooks/
```

The baseline contains logical-role agents only: Architect, Critic, Coder,
Reviewer, Verifier. Provider-named authority agents and pre-authorized MCP tools
are absent. Claude hooks use the shared machine Work Block for source writes,
Hard Stops, Review, Verification, Drift, and closeout.

### OpenCode

Project-local OpenCode files exist in `opencode` and `multi-runtime`
installations. Read:

```text
runtimes/opencode/README.md
opencode.json
.opencode/agents/
```

The baseline:

- denies common secret paths and external directories;
- requires approval for edits, Bash, web, task delegation, and MCP;
- explicitly denies commit, push, reset-hard, clean, and `rm` for every role;
- limits implementation writes to the logical Coder;
- starts with empty `mcp` and `plugin` collections;
- does not pin provider/model.

Run a target-environment smoke before Managed or higher-governance work.

### Generic / Sequential Runtime

Generic guidance is always present under `runtimes/generic/`. Use it for a global
CLI, IDE agent, local model, or manual session without project-local runtime
configuration. Perform required logical functions as separate documented passes
and record reduced independence honestly.

## Integration Admission

No installation profile activates an external integration. `multi-runtime`
installs an empty `.mcp.json` only as an inert configuration surface.

Before enabling a plugin, MCP server, external runtime CLI, hosted connector, or
file runner:

1. fill `docs/templates/integration-admission-template.md`;
2. identify exact logical functions and tools;
3. record authority, paths, network, external-directory, data, and secret
   boundaries;
4. classify side effects and Hard Stops;
5. record authentication source without values;
6. define timeout, cancellation, retry, recovery, logging, and disable procedure;
7. run allowed and denied smoke fixtures;
8. add integration ID and admission-evidence path to the active Work Block.

Direct `codex`, `claude`, or `opencode` child-process invocation is an
integration and requires the same admission. Admission does not grant child
write authority.

## Work Block Setup

Before non-trivial mutation, create a Work Block from:

```text
docs/templates/work-block-template.md
```

Record:

- objective, expected result, done criteria;
- approved specification/revision and architecture baseline;
- scope, out-of-scope, write-set, and Git baseline;
- side-effect/data modes and Hard Stops;
- actual runtime capability and isolation;
- logical function bindings;
- integration profile/admission records or `none`;
- implementation and assurance plan;
- evidence/report paths;
- write gate and closeout state.

`.agent/active-work-block.json` is the executable authority/gate state. Do not
confuse it with `.agent/bootstrap-profile.json`, which only records installation.

## Smoke Checks

### Generated-project installation health

```bash
bash scripts/bootstrap.sh
```

Expected:

```text
Installation profile: OK (...)
Agentic SDLC layer: OK
```

### Framework contracts

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-bootstrap-profiles.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

### Runtime smoke

For each selected runtime prove in a disposable project:

- instructions/logical agents load;
- source writes remain blocked without valid Work Block state;
- in-scope write can proceed when approved;
- out-of-scope write is denied;
- read-only roles cannot change implementation source;
- consequential Git/filesystem actions remain denied or Owner-gated;
- secret/external-directory access is denied where supported;
- Review/Verification output includes evidence and actual isolation;
- runtime version and limitations are recorded.

Static conformance tests compare semantics; they do not prove live runtime or OS
isolation.

### Integration smoke

For each admitted integration prove exact allowed/denied tools, no committed
credentials, harmless denied-write failure, timeout/cancel/recovery, and result
identity/revision/scope/evidence.

Do not run paid/live smoke automatically during bootstrap or CI.

## Changing an Existing Project's Installation Composition

Bootstrap refuses non-empty targets. It is not an in-place upgrader.

To change composition:

1. review `bootstrap/profiles.json` and the target profile;
2. create a migration Work Block with explicit file additions/removals;
3. compare a disposable generated project against the existing project;
4. copy/remove only approved runtime surfaces and skills;
5. regenerate `.agent/bootstrap-profile.json` consistently;
6. run `scripts/validate-installation-profile.py`;
7. smoke the newly installed runtime;
8. review and verify the migration diff.

Do not rerun framework bootstrap against a populated project.

## Manual Installation

Manual copying is supported, but profile-aware bootstrap is preferred. If
copying manually, use the profile catalog as the composition contract, copy the
common portable files plus selected component paths/skills, create consistent
bootstrap profile state, replace placeholders literally, and run the generated
validator.

## Publication and Local State

Before committing/publishing runtime or integration state, inspect `.agent/`,
`.codex/`, `.claude/agent-memory/`, `.opencode/`, `memory_bank/`, handoff state,
provider/plugin config, MCP endpoints/arguments/environment names, local paths,
downloaded packages, generated output, transcripts, personal/live data, and
permissions that write/send/deploy/mutate.

Never commit secret values.

## Further Reading

- `README.md`
- `PROJECT_MAP.md`
- `docs/bootstrap-profiles.md`
- `docs/profiles.md`
- `docs/mcp-tool-policy.md`
- `governance/README.md`
- `runtimes/README.md`
- `integrations/README.md`
- `handoff/README.md`
