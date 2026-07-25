# Agentic SDLC Framework

Project-agnostic governance and delivery framework for software projects built
with AI agents.

The framework is a **runtime-neutral control plane**. It defines authority,
scope, lifecycle state, required artifacts, risk gates, evidence, and closeout
semantics. Codex, Claude Code, OpenCode, Antigravity, and future agent systems
execute those contracts through runtime adapters.

The SDLC manages the work. Agent runtimes execute it.

## What This Gives You

- **Governance core**: stable roles, authority, lifecycle, artifact, risk,
  verification, drift, and closeout contracts under `governance/`.
- **Portable project scaffold**: generated `AGENTS.md`, `.agent/`,
  `memory_bank/`, `docs/`, and selected skills.
- **Runtime adapters**: Codex, Claude Code, OpenCode, and generic sequential
  execution guidance under `runtimes/`.
- **Reusable skill library**: discovery, implementation, review, verification,
  design, security, debugging, integrations, and closeout skills.
- **Engineering memory**: committed, evidence-backed decisions and
  reproducibility guidance that do not depend on chat history.
- **Operational memory**: local context, progress, decision, review, and external
  team logs.
- **Advanced handoff**: audited file-based Codex → Claude Code transport for
  recovery, cross-machine work, external teams, or environments without a direct
  integration.
- **Publication hygiene**: validation scripts, security policy, third-party
  notices, and private/local-state boundaries.

## Architecture

The framework is intentionally layered.

### 1. Governance Core

`governance/` is the target normative control plane:

- `authority.md` — logical roles and authority boundaries;
- `lifecycle.md` — Define, Execute, Assure, and Close stages;
- `artifacts.md` — specification, plan, review, verification, drift, and
  closeout contracts;
- `runtime-capabilities.md` — capability negotiation and fallback rules.

The core contains no provider credentials and must not make a runtime, model,
plugin, MCP server, or transport authoritative.

### 2. Runtime Adapters

`runtimes/` explains how agent systems implement the core contract:

- `runtimes/codex/`;
- `runtimes/claude-code/`;
- `runtimes/opencode/`;
- `runtimes/generic/`.

Runtime, model, role, and isolation are separate dimensions. Changing a runtime
or model never expands authority.

### 3. Project Artifacts

Agents coordinate through approved files rather than hidden prompt history:

```text
objective → specification → implementation plan → frozen diff
          → review → verification → drift audit → closeout
```

### 4. Existing Compatibility Layers

The repository still ships operational implementations created before the
runtime-neutral refactor:

- `template/.codex/` — Codex instructions, critic contract, and write gate;
- `template/.claude/` — Claude Code agents, hooks, skills, settings, and memory;
- `handoff/` — file-based Codex → Claude Code transport;
- `framework/workflow/codex-model-routing.md` — model-routing guidance.

These remain usable during migration. Later Work Blocks will normalize them as
runtime and integration adapters without removing working functionality first.

See the architecture decision:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.

## Core Principles

1. **Authority is structural.** Tools and model capability do not authorize an
   action.
2. **Artifacts are the interoperability boundary.** A new agent must recover
   project state without old chat history.
3. **Specification precedes implementation.** Plans and tasklists are derived
   from approved requirements.
4. **Gates fail closed.** Missing review or verification is not a pass.
5. **Use the smallest sufficient topology.** Native runtime mechanisms are
   preferred over custom transports.
6. **Independent assurance is risk-based.** Low-risk work may run sequentially;
   high-risk work requires stronger isolation and evidence.
7. **Local-first by default.** Secrets, private memory, runtime caches, and
   provider configuration remain local.

## Logical Roles

The governance core defines functions, not permanent processes:

| Role | Responsibility |
|---|---|
| Owner | Objective, exceptions, hard stops, business acceptance |
| Orchestrator | Scope, topology, transitions, consolidation, closeout |
| Architect | Discovery, architecture, specification, plan proposals |
| Critic | Pre-execution challenge of scope, risks, and verification design |
| Coder | Approved implementation write set |
| Reviewer | Frozen-diff quality, security, architecture, maintainability review |
| Verifier | Acceptance-criterion and contract evidence |

One runtime may execute several functions in low-risk work. Managed and assured
profiles require stronger separation.

## Quick Start

From this repository:

```bash
./bootstrap.sh /tmp/my-agentic-project "My Agentic Project" my-agentic-project
cd /tmp/my-agentic-project
bash scripts/bootstrap.sh
```

For a real project:

```bash
./bootstrap.sh /path/to/new-project "My Project" my-project
cd /path/to/new-project
git init
git add -A
git commit -m "Initial scaffold from Agentic SDLC Framework"
```

The generated project receives `.gitignore` from
`template/project.gitignore`. Local agent state remains private by default.

## Where to Start

For framework architecture and governance:

1. `governance/README.md`;
2. `PROJECT_MAP.md`;
3. `FILE_REGISTRY.yml`;
4. the active Work Block under `docs/plans/`;
5. relevant architecture decisions under `docs/architecture/decisions/`.

For generated-project operation:

1. `AGENTS.md`;
2. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
3. `docs/session-bootstrap.md`;
4. the active specification and Work Block;
5. relevant `docs/engineering-memory/` entries;
6. runtime adapter instructions only when needed.

## Current Operating Paths

| Need | Start here |
|---|---|
| Runtime-neutral governance | `governance/README.md` |
| Minimal generated project | `docs/quickstart-minimal.md` |
| Existing profile selection | `docs/profiles.md` |
| Codex compatibility layer | `template/.codex/`, `runtimes/codex/` |
| Claude Code team layer | `template/.claude/`, `runtimes/claude-code/` |
| OpenCode evaluation | `runtimes/opencode/`, `framework/knowledge/opencode-runtime.md` |
| File-based external-team handoff | `handoff/README.md` |
| Skill selection | `skills/catalog.yml` |
| Tool/MCP policy | `docs/mcp-tool-policy.md` |

## Directory Structure

```text
agentic-sdlc-framework/
├── README.md
├── SETUP.md
├── PROJECT_MAP.md
├── FILE_REGISTRY.yml
├── governance/                 # runtime-neutral normative control plane
├── runtimes/                   # runtime-specific adapters and capability maps
├── docs/
│   ├── architecture/decisions/
│   └── plans/
├── template/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── .agent/
│   ├── .codex/
│   ├── .claude/
│   ├── memory_bank/
│   ├── docs/
│   └── scripts/
├── framework/                  # reference knowledge and migration background
├── skills/                     # portable skill library
├── handoff/                    # advanced audited file transport
├── examples/
├── scripts/
└── archive/                    # private/local, ignored for publication
```

## Requirements

- Linux, WSL, or macOS shell environment;
- `bash`, `git`, `find`, `sed`, `grep`, `chmod`;
- `jq` for current Claude Code hooks;
- optional `python3` for validation and future policy hooks;
- optional `node`/`npx` for JavaScript projects and MCP servers.

The current hook scripts assume a Unix-like environment. Windows users should
run them from WSL or Git Bash.

## Skills

Shared skills live in `skills/<name>/`. `skills/catalog.yml` is the
metadata-only navigation index. Consumer projects should eventually pin only
the skills they need through an immutable revision and keep resolved caches
local.

Bootstrap currently installs the core set into:

- `.agent/skills/<name>/` for runtime-neutral routing;
- `.claude/skills/<name>/` for the existing Claude Code layer.

Profile-aware installation is planned as part of the runtime-neutral migration.

## Local vs Published State

Generated projects start in local-first mode. Review any publication of
`.agent/`, `.codex/`, `.claude/agent-memory/`, `memory_bank/`, runtime logs, or
provider configuration for:

- secrets and credentials;
- private client/project context;
- raw transcripts;
- machine-local paths;
- generated output;
- unreviewed agent conclusions.

## Publication Check

Before publishing this framework repository:

```bash
bash scripts/validate-publication.sh
```

The check verifies required scaffold files, script syntax, placeholders,
generated Python bytecode, and known private/project-specific markers.

## License

MIT. See `LICENSE`.

Bundled third-party skills may retain their own license files. See
`THIRD_PARTY_NOTICES.md`.
