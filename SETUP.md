# Agentic SDLC Framework Setup

Setup guide for humans and agents creating a project from the runtime-neutral
framework.

## Quick Start

```bash
./bootstrap.sh /path/to/new-project "My Project" my-project
cd /path/to/new-project
git init
git add -A
git commit -m "Initial scaffold from Agentic SDLC Framework"
```

The installer:

- copies the generated-project template;
- installs Governance Core, runtime adapters, and integration documentation;
- installs the default portable skill baseline;
- replaces placeholders using literal character-safe replacement;
- makes project hooks/scripts executable;
- runs the generated-project health check.

It does **not** install or authenticate Codex, Claude Code, OpenCode, plugins,
MCP servers, providers, browsers, watchers, or services.

Rerun the health check after moving or restoring the project:

```bash
bash scripts/bootstrap.sh
```

## Architecture Layers

The generated project separates:

1. **Governance Core** — `AGENTS.md` and `governance/` define authority,
   lifecycle, artifacts, capabilities, Hard Stops, and closeout.
2. **Portable workflow** — `.agent/`, specifications, plans, tasks, reports,
   skills, and memory coordinate the work.
3. **Runtime adapters** — Codex, Claude Code, OpenCode, or generic execution
   mechanics under `runtimes/` and runtime-specific project files.
4. **Integration adapters** — optional plugins, MCP, external runtime CLIs,
   hosted tools, and audited file transport under `integrations/`.

Runtime/model/integration choice never changes logical role authority.

## First Session

Read progressively:

```text
AGENTS.md
active Work Block, when present
approved specification and architecture decisions
PROJECT_MAP.md / FILE_REGISTRY.yml when navigation is needed
selected runtime adapter
selected integration adapter only when required
```

Do not load every skill, runtime, integration, and memory file by default.

## Select Profiles

Use `docs/profiles.md` and record independent selections:

```yaml
governance_profile: Managed
runtime_profile: codex
integration_profile: none
model_class: balanced_engineering
isolation: separate-subagent
```

Start with the smallest sufficient governance profile and `integration_profile:
none`. Add an external bridge/tool/transport only when it provides necessary
value and has an admission record.

## Runtime Setup

### Codex

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
4. create/populate `.agent/active-work-block.json`;
5. run safe adapter fixtures or a read-only smoke;
6. trust project hooks deliberately.

Concrete model/provider/auth settings remain user-local.

### Claude Code

Read:

```text
CLAUDE.md
runtimes/claude-code/README.md
.claude/settings.json
.claude/agents/
.claude/hooks/
```

The generated default includes only logical-role agents:

- `solution-architect`;
- `critic`;
- `scoped-coder`;
- `reviewer`;
- `verifier`.

Provider-named `gpt-critic`, `gpt-verifier`, and `codex-reviewer` agents are not
installed. Claude hooks read the same machine Work Block as Codex for source
writes, Hard Stops, Review, Verification, Drift, and closeout.

No MCP server or plugin is enabled automatically.

### OpenCode

Read:

```text
runtimes/opencode/README.md
opencode.json
.opencode/agents/
```

The baseline:

- denies common secret paths and external directories;
- requires approval for edits, Bash, web, task delegation, and MCP;
- denies commit, push, destructive Git, and `rm`;
- includes five logical-role subagents;
- starts with empty `mcp` and `plugin` collections;
- does not pin a provider/model.

Run a target-environment smoke before Managed or higher-governance work. Confirm
that read-only agents cannot edit and that commit/push/secret/external-directory
access remains denied.

### Generic / Sequential Runtime

Read `runtimes/generic/README.md`. Perform required logical functions as separate
documented passes/sessions and record reduced independence honestly.

## Integration Admission

Generated projects start with no active external integrations:

```json
{
  "mcpServers": {}
}
```

OpenCode also starts with:

```json
{
  "mcp": {},
  "plugin": []
}
```

Before enabling any plugin, MCP server, external runtime CLI, hosted connector,
or file runner:

1. copy/fill `docs/templates/integration-admission-template.md`;
2. identify exact logical functions and tools;
3. record authority, paths, network, external-directory, data, and secret
   boundaries;
4. classify side effects and Hard Stops;
5. record authentication source without values;
6. define timeout, cancellation, retry, recovery, logging, and disable procedure;
7. run allowed and denied smoke fixtures;
8. add the integration ID and admission-evidence path to the active Work Block.

### Claude Code → Codex

Preferred order:

1. official Codex plugin for Claude Code;
2. reviewed Codex MCP server/tool;
3. audited file handoff;
4. manual artifact exchange;
5. direct `codex` process only as an explicitly admitted exception.

See:

```text
integrations/claude-code-codex-plugin/README.md
integrations/mcp/README.md
integrations/file-handoff/README.md
```

The official plugin uses the local Codex runtime, authentication, configuration,
machine, and checkout. Record the actual boundary; do not claim OS isolation.

### MCP

`.mcp.json` is empty by default. Add only reviewed, credential-free
configuration; grant exact tools rather than the whole server. Keep tokens,
passwords, cookies, keys, connection strings, and personal paths outside
committed files.

External MCP content is untrusted input and cannot override project authority.

### File Handoff

Use the runtime-neutral envelope:

```text
handoff/templates/runtime-task-template.md
```

The existing `handoff-runner.sh` invokes Claude Code and is a compatibility
transport. It does not define the public protocol and is not started
automatically.

Enable a watcher or user service only after reviewing identity, environment,
project roots, scope audit, concurrency, logs/retention, shutdown, and uninstall.

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
- runtime capability snapshot;
- logical function bindings and actual isolation;
- integration profile/admission records, or `none`;
- implementation and assurance plan;
- evidence/report paths;
- write gate and closeout state.

`.agent/active-work-block.json` is the executable gate for supporting runtimes.
Generated state begins blocked, with empty integration approvals and pending
assurance.

## Smoke Checks

### Generated-project health

```bash
bash scripts/bootstrap.sh
```

Expected:

```text
Agentic SDLC layer: OK
```

Warnings about project dependencies or `DATABASE_URL` are normal when not
applicable.

### Framework contracts

From the framework repository:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-integration-contracts.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

### Runtime smoke

For each selected runtime prove, in a disposable project:

- instructions and logical agents load;
- source writes remain blocked without a valid Work Block;
- in-scope write can proceed when approved;
- out-of-scope write is denied;
- secret/external-directory access is denied where supported;
- Review/Verification output includes evidence and actual isolation;
- runtime version and limitations are recorded.

### Integration smoke

For each admitted integration prove:

- only intended tools/actions are visible;
- denied tools remain denied;
- no committed credentials are required;
- a harmless denied-write fixture fails;
- timeout/cancel/recovery is understood;
- result identifies integration, runtime, revision, scope, gaps, and evidence.

Do not run paid/live smoke automatically during bootstrap or CI.

## Manual Installation

Manual copying is supported, but `bootstrap.sh` is preferred because it preserves
character-safe placeholders and validates the complete delivery manifest.

When copying manually, include:

```text
template/.
governance/.
runtimes/.
integrations/.
selected skills
```

Then replace placeholders literally in text files:

| Placeholder | Meaning |
|---|---|
| `{{PROJECT_NAME}}` | display name |
| `{{PROJECT_SLUG}}` | stable project identifier |
| `{{PROJECT_ROOT}}` | absolute project root |
| `{{SOURCE_DIRS}}` | source path patterns |
| `{{TECH_STACK}}` | project technology summary |

Make hooks/scripts executable and run `bash scripts/bootstrap.sh`.

## Publication and Local State

Before committing/publishing runtime or integration state, inspect:

- `.agent/`, `.codex/`, `.claude/agent-memory/`, `.opencode/`;
- `memory_bank/` and handoff runtime/log directories;
- provider and plugin configuration;
- MCP endpoints/arguments/environment names;
- local absolute paths;
- downloaded packages and generated output;
- raw transcripts or hidden reasoning;
- customer/personal/live data;
- permissions that write, send, deploy, or mutate data.

Never commit secret values.

## Further Reading

- `README.md`
- `PROJECT_MAP.md`
- `docs/profiles.md`
- `docs/mcp-tool-policy.md`
- `governance/README.md`
- `runtimes/README.md`
- `integrations/README.md`
- `handoff/README.md`
