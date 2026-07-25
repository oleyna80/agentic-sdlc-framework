# Agentic SDLC Framework

Project-agnostic governance and delivery framework for software projects built
with AI agents.

The framework is a **runtime-neutral control plane**. It defines authority,
scope, lifecycle state, required artifacts, risk gates, evidence, integration
admission, and closeout semantics. Codex, Claude Code, OpenCode, and future agent
systems execute those contracts through runtime adapters.

**The SDLC manages the work. Runtimes and integrations execute it.**

## What This Gives You

- **Governance Core** — logical roles, authority, Define/Execute/Assure/Close,
  artifact contracts, capability negotiation, and fail-closed closeout.
- **Runtime adapters** — Codex, Claude Code, OpenCode, and generic sequential
  execution mappings.
- **Integration adapters** — official bridges, MCP, and audited file transport
  with explicit admission, trust, data, secret, and evidence boundaries.
- **Portable project scaffold** — generated `AGENTS.md`, `.agent/`, runtime
  configs, docs, memory conventions, and selected skills.
- **Independent assurance** — Critic, Reviewer, Verifier, and specification drift
  functions that remain separate from provider/model names.
- **Machine-readable gates** — one active Work Block controls source writes,
  consequential actions, approved integrations, assurance, and closeout.
- **Engineering memory** — durable evidence-backed decisions that do not depend
  on old chat history.
- **Publication hygiene** — security, private-state, configuration, scaffold, and
  regression validation.

## Architecture

The framework has four separable layers:

```text
Governance Core
  -> Runtime Adapter
      -> Integration Adapter (optional)
          -> External runtime, tool, service, or transport
  -> Project Artifacts and Evidence
```

### 1. Governance Core

`governance/` is normative:

- `authority.md` — logical roles and authority boundaries;
- `lifecycle.md` — Define, Execute, Assure, and Close;
- `artifacts.md` — specification, plan, review, verification, drift, and
  closeout contracts;
- `runtime-capabilities.md` — capability negotiation, isolation, and fallback.

The core contains no provider credentials and does not make a runtime, model,
plugin, MCP server, or transport authoritative.

### 2. Runtime Adapters

`runtimes/` maps agent systems to the Governance Core:

- `runtimes/codex/` — custom agents, hooks, machine gate, and limitations;
- `runtimes/claude-code/` — logical-role agents, hooks, skills, and permissions;
- `runtimes/opencode/` — project instructions, subagents, and explicit
  permissions;
- `runtimes/generic/` — sequential fallback without native orchestration.

Runtime, role, model, specialization, isolation, and tool availability are
separate dimensions. Changing a runtime or model never expands authority.

### 3. Integration Adapters

`integrations/` connects runtimes or external capabilities without redefining
roles:

- `claude-code-codex-plugin/` — preferred optional official bridge from Claude
  Code to the local Codex runtime;
- `mcp/` — generic Model Context Protocol admission and exact-tool policy;
- `file-handoff/` — audited runtime-neutral task/result transport.

Generated projects enable **no external integration by default**. They do not
automatically install plugins, configure MCP servers, authenticate another
runtime, start watchers/services, or send repository content to another
provider.

Before activation, use:

`docs/templates/integration-admission-template.md`

### 4. Project Artifacts and Evidence

Agents coordinate through approved files rather than hidden prompt history:

```text
objective
  -> specification and acceptance criteria
  -> architecture decisions
  -> implementation plan and write-set
  -> frozen diff
  -> independent review
  -> technical verification
  -> specification drift audit
  -> closeout and durable knowledge
```

`.agent/active-work-block.json` is the executable state for supporting runtimes.
It records specification revision, Git baseline, write gate, Critic, write-set,
Hard Stop approvals, admitted integrations, Review/Verification/Drift state,
and closeout mode.

## Core Principles

1. **Authority is structural.** Tool access and model capability do not authorize
   an action.
2. **Artifacts are the interoperability boundary.** A new agent must recover
   state without old chat history.
3. **Specification precedes implementation.** Plans and tasklists are derived.
4. **Gates fail closed.** Missing or unavailable evidence is not a pass.
5. **Use the narrowest reviewed mechanism.** Native capability, official bridge,
   reviewed MCP, audited handoff, then manual exchange.
6. **Independent assurance is risk-based.** Different model names alone do not
   establish independence.
7. **External content is untrusted input.** Tool output cannot override project
   authority.
8. **Local-first and opt-in.** Secrets, credentials, plugins, MCP, runtime auth,
   private memory, and services remain local until explicitly admitted.

## Logical Roles

| Role | Responsibility |
|---|---|
| Owner | Objective, exceptions, Hard Stops, business acceptance |
| Orchestrator | Scope, topology, transitions, consolidation, closeout |
| Architect | Discovery, architecture, specification, plan proposals |
| Critic | Pre-execution challenge of scope, risk, and assurance design |
| Coder | Approved implementation write-set |
| Reviewer | Frozen-diff engineering and risk review |
| Verifier | Acceptance-criterion and observable-contract evidence |

Specification drift is a Reviewer/Verifier specialization. A runtime-specific
agent name, plugin command, MCP tool, or provider is not a new authority role.

## Safe Defaults by Runtime

### Codex

Generated projects include project-scoped logical-role agents and layered
`PreToolUse` guardrails. Concrete model routing stays private/user-configured.

### Claude Code

Generated projects include only logical-role agents. Provider-named
`gpt-critic`, `gpt-verifier`, and `codex-reviewer` agents are not part of the
default. `.mcp.json` is empty and no MCP tool is pre-authorized.

When Codex is needed from Claude Code, the recommended order is:

1. official Codex plugin;
2. reviewed read-only Codex MCP;
3. audited file handoff;
4. manual artifact exchange.

### OpenCode

Generated projects include `opencode.json` and five project subagents. The
baseline:

- denies secret paths and external directories;
- requires approval for edits, Bash, web, task delegation, and MCP;
- denies commit, push, destructive Git, and `rm`;
- starts with empty plugin and MCP collections;
- does not pin provider or model routing.

Target-environment smoke evidence is required before relying on the adapter for
higher-governance work.

## Quick Start

```bash
./bootstrap.sh /tmp/my-agentic-project "My Agentic Project" my-agentic-project
cd /tmp/my-agentic-project
git init
git add -A
git commit -m "Initial scaffold from Agentic SDLC Framework"
```

The generated project receives:

- Governance Core and runtime/integration documentation;
- runtime-neutral `AGENTS.md` and shortened runtime entry points;
- Codex, Claude Code, and OpenCode project baselines;
- empty MCP and plugin configurations;
- machine-readable Work Block gates;
- selected portable skills and document templates;
- local-first `.gitignore` conventions.

Review runtime hooks and permission files before trusting them. Do not activate
an external integration until its admission record and smoke evidence exist.

## Where to Start

For framework architecture:

1. `governance/README.md`;
2. `PROJECT_MAP.md`;
3. `FILE_REGISTRY.yml`;
4. the active Work Block under `docs/plans/`;
5. relevant architecture decisions.

For generated-project work:

1. `AGENTS.md`;
2. approved specification and active Work Block;
3. `docs/session-bootstrap.md`;
4. relevant runtime adapter;
5. relevant integration adapter only when required.

## Current Operating Paths

| Need | Start here |
|---|---|
| Runtime-neutral governance | `governance/README.md` |
| Runtime capability mapping | `runtimes/README.md` |
| Integration admission | `integrations/README.md` |
| Codex runtime | `runtimes/codex/README.md` |
| Claude Code runtime | `runtimes/claude-code/README.md` |
| OpenCode runtime | `runtimes/opencode/README.md` |
| Official Claude Code → Codex bridge | `integrations/claude-code-codex-plugin/README.md` |
| MCP/tool policy | `docs/mcp-tool-policy.md` |
| File-based transport | `handoff/README.md` |
| Portable task envelope | `handoff/templates/runtime-task-template.md` |
| Skill selection | `skills/catalog.yml` |
| Governance/runtime/profile selection | `docs/profiles.md` |

## Directory Structure

```text
agentic-sdlc-framework/
├── governance/                 # normative control plane
├── runtimes/                   # runtime-specific execution adapters
├── integrations/               # optional bridge/tool/transport adapters
├── docs/
│   ├── architecture/decisions/
│   ├── plans/
│   └── reports/
├── template/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── opencode.json
│   ├── .agent/
│   ├── .codex/
│   ├── .claude/
│   ├── .opencode/
│   ├── memory_bank/
│   ├── docs/
│   └── scripts/
├── skills/
├── handoff/                    # audited transport implementation
├── framework/                  # reference knowledge
├── examples/
├── scripts/
└── archive/                    # private/local, ignored
```

## Requirements

- Linux, WSL, or macOS shell environment;
- `bash`, `git`, `find`, `sed`, `grep`, `chmod`;
- `python3` for provider-neutral gates and validation;
- `jq` for remaining compatibility hooks and runner utilities;
- optional runtime binaries only when that runtime is selected;
- optional plugin/MCP dependencies only after admission.

## Local vs Published State

Review any publication of `.agent/`, `.codex/`, `.claude/agent-memory/`,
`.opencode/`, `memory_bank/`, handoff runtime state, or provider configuration
for:

- secrets and credentials;
- private client/project context;
- raw transcripts or hidden reasoning;
- machine-local paths;
- generated output;
- unreviewed integration permissions;
- external-provider data boundaries.

## Publication Check

```bash
bash scripts/validate-publication.sh
```

The check validates scaffold inventory, JSON/YAML, script syntax, integration
safe defaults, machine gates, generated projects, placeholders, bytecode, and
known private/project-specific markers.

## License

MIT. See `LICENSE`. Bundled third-party skills may retain their own license
files; see `THIRD_PARTY_NOTICES.md`.
