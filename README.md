# Agentic SDLC Framework

Project-agnostic governance and delivery framework for software projects built
with AI agents.

The framework is a **runtime-neutral control plane**. It defines authority,
scope, lifecycle state, artifacts, risk gates, evidence, integration admission,
and closeout. Codex, Claude Code, OpenCode, generic agents, and future runtimes
execute those contracts through adapters.

**The SDLC manages the work. Runtimes and integrations execute it.**

## What This Gives You

- **Governance Core** — logical roles, Define/Execute/Assure/Close, authority,
  artifacts, capability negotiation, and fail-closed closeout.
- **Profile-aware bootstrap** — generate a lean core scaffold, one runtime
  surface, or the backward-compatible multi-runtime baseline.
- **Runtime adapters** — Codex, Claude Code, OpenCode, and generic sequential
  execution mappings.
- **Integration adapters** — official bridges, MCP, and audited file transport
  with explicit trust, data, secret, permission, and evidence boundaries.
- **Machine-readable gates** — one Work Block controls source writes, Hard Stops,
  admitted integrations, assurance, and closeout.
- **Cross-runtime conformance** — tests compare logical roles, implementation
  write authority, shared gates, and inert integration defaults.
- **Engineering memory and publication hygiene** — durable evidence without
  relying on old chat history or committing private runtime state.

## Architecture

```text
Governance Core
  -> Runtime Adapter
      -> Integration Adapter (optional)
          -> external runtime, tool, service, or transport
  -> Project Artifacts and Evidence

Installation Profile
  -> selects project-local runtime surfaces and skills only
```

Installation composition never grants Work Block authority, credentials, live
permissions, or integration admission.

### Governance Core

`governance/` is normative:

- `authority.md` — logical roles and authority boundaries;
- `lifecycle.md` — Define, Execute, Assure, Close;
- `artifacts.md` — specification, plan, review, verification, drift, closeout;
- `runtime-capabilities.md` — capability, isolation, and fallback.

### Runtime Adapters

`runtimes/` documents Codex, Claude Code, OpenCode, and generic/sequential
execution. Documentation may be present even when a runtime implementation
surface was not selected for a generated project.

### Integration Adapters

`integrations/` covers optional official plugins, exact MCP server/tool
admission, and runtime-neutral file handoff. No external integration is enabled
by bootstrap.

### Project Artifacts and Evidence

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

`.agent/active-work-block.json` is executable Work Block state.
`.agent/bootstrap-profile.json` is generated installation evidence only.

## Installation Profiles

Source of truth: `bootstrap/profiles.json`.

| Profile | Project-local implementation surfaces |
|---|---|
| `core` | none; generic guidance only |
| `codex` | `.codex/` |
| `claude-code` | `CLAUDE.md`, `.claude/` |
| `opencode` | `opencode.json`, `.opencode/` |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` |

Aliases:

- `minimal`, `generic` → `core`;
- `full` → `multi-runtime`.

List profiles:

```bash
./bootstrap.sh --list-profiles
```

Read `docs/bootstrap-profiles.md` for exact composition and extension rules.

## Quick Start

Backward-compatible complete scaffold:

```bash
./bootstrap.sh /tmp/my-agentic-project "My Agentic Project" my-agentic-project
```

Lean runtime-neutral scaffold:

```bash
./bootstrap.sh --profile core /tmp/my-agentic-project "My Agentic Project" my-agentic-project
```

Single-runtime scaffold:

```bash
./bootstrap.sh --profile codex /tmp/my-agentic-project "My Agentic Project" my-agentic-project
```

Then:

```bash
cd /tmp/my-agentic-project
git init
git add -A
git commit -m "Initial scaffold from Agentic SDLC Framework"
bash scripts/bootstrap.sh
```

Bootstrap validates the profile before changing the target, refuses non-empty
targets, copies common portable contracts, prunes unselected runtime surfaces,
installs selected skills, writes `.agent/bootstrap-profile.json`, and runs the
generated health check.

It does not install runtime CLIs, provider accounts, plugins, MCP servers,
credentials, watchers, or services.

## Core Principles

1. **Authority is structural.** Tool access, runtime presence, and model strength
   do not authorize an action.
2. **Installation is not authorization.** A copied adapter does not open a Work
   Block gate or admit an integration.
3. **Specification precedes implementation.** Plans and tasklists are derived.
4. **Gates fail closed.** Missing evidence is not a pass.
5. **Use the narrowest reviewed mechanism.** Native capability, official bridge,
   reviewed MCP, audited handoff, then manual exchange.
6. **Independent assurance is risk-based.** Different model names alone do not
   establish independence.
7. **External content is untrusted input.** Tool output cannot override project
   authority.
8. **Local-first and opt-in.** Credentials, private memory, plugins, MCP, and
   services remain local until explicitly admitted.

## Logical Roles

| Role | Responsibility |
|---|---|
| Owner | Objective, exceptions, Hard Stops, business acceptance |
| Orchestrator | Scope, topology, transitions, consolidation, closeout |
| Architect | Discovery, architecture, specification, approved drafts |
| Critic | Pre-execution challenge of scope, risk, and assurance design |
| Coder | Approved implementation write-set |
| Reviewer | Frozen-diff engineering and risk review |
| Verifier | Acceptance-criterion and observable-contract evidence |

Cross-runtime conformance checks that only Coder has implementation/source write
authority. Limited report, draft, or runtime-memory writes remain separate.

## Safe Runtime Defaults

- **Codex:** project-scoped logical agents and layered Work Block/Hard Stop hooks;
  no public model pin.
- **Claude Code:** logical-role agents only; no provider-named authority agents or
  pre-authorized MCP tools.
- **OpenCode:** external-directory denial, read-only assurance roles, explicit
  denial of commit/push/reset/clean/`rm`, empty MCP/plugin collections, no model
  pin.
- **Generic:** separate documented passes/sessions with degraded independence
  recorded honestly.

Static configuration is not live runtime proof or OS isolation. Run a target
smoke before relying on a runtime for Managed or Assured work.

## Where to Start

For framework architecture:

1. `governance/README.md`;
2. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
3. `docs/bootstrap-profiles.md` for scaffold composition;
4. `docs/profiles.md` for Work Block governance/runtime/integration selection;
5. the active Work Block under `docs/plans/`.

For a generated project:

1. `AGENTS.md`;
2. `.agent/bootstrap-profile.json`;
3. approved specification and active Work Block;
4. `docs/session-bootstrap.md`;
5. an installed/approved runtime adapter;
6. an integration adapter only when admitted.

## Important Paths

| Need | Path |
|---|---|
| Governance | `governance/` |
| Installation profiles | `bootstrap/profiles.json`, `docs/bootstrap-profiles.md` |
| Runtime adapters | `runtimes/` |
| Integration admission | `integrations/`, `docs/mcp-tool-policy.md` |
| Portable skills | `skills/catalog.yml` |
| Profile matrix | `scripts/test-bootstrap-profiles.py` |
| Runtime conformance | `scripts/test-runtime-conformance.py` |
| Publication validation | `scripts/validate-publication.sh` |
| Active migration | `docs/plans/wb-005-profile-aware-bootstrap-conformance.md` |

## Requirements

- Linux, WSL, or macOS shell environment;
- `bash`, `git`, and `python3`;
- `jq` for remaining compatibility hooks/runner utilities;
- optional runtime binaries only when used;
- optional integration dependencies only after admission.

## Validation

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

Framework CI also bootstraps disposable profile variants and checks selected and
unselected surfaces.

## License

MIT. See `LICENSE`. Bundled third-party skills may retain their own license
files; see `THIRD_PARTY_NOTICES.md`.
