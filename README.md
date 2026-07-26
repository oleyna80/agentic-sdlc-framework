# Agentic SDLC Framework

Project-agnostic governance and delivery framework for software projects built
with AI agents.

The framework is a **runtime-neutral control plane**. It defines authority,
scope, lifecycle state, artifacts, risk gates, evaluation, release-state
reconciliation, integration admission, and closeout. Codex, Claude Code,
OpenCode, generic agents, and future runtimes execute those contracts through
adapters.

**The SDLC manages the work. Runtimes and integrations execute it.**

## What This Gives You

- **Governance Core** — logical roles, Define/Execute/Assure/Close, authority,
  artifacts, capability negotiation, evaluation, release state, and fail-closed
  closeout.
- **Profile-aware bootstrap** — generate a lean core scaffold, one runtime
  surface, or the backward-compatible multi-runtime baseline.
- **Runtime adapters** — Codex, Claude Code, OpenCode, and generic sequential
  execution mappings.
- **Integration adapters** — official bridges, MCP, and audited file transport
  with explicit trust, data, secret, permission, and evidence boundaries.
- **Machine-readable gates** — one Work Block controls source writes, Hard Stops,
  admitted integrations, review, verification, evaluation, drift, and closeout.
- **Evaluation assurance** — deterministic tests, output rubrics, observable
  trajectory checks, frozen revisions, and strict LM-judge limits.
- **Release-state assurance** — Work Blocks, map, registry, and closeout must agree;
  mutable GitHub state is external operational metadata.
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
      -> deterministic tests
      -> output evaluation
      -> observable trajectory evaluation
      -> release-state reconciliation

Installation Profile
  -> selects project-local runtime surfaces and skills only
```

Installation composition, evaluation evidence, release-state evidence, and
hosting-platform state never grant Work Block authority, credentials, live
permissions, integration admission, or Hard Stop exceptions.

### Governance Core

`governance/` is normative:

- `authority.md` — logical roles and authority boundaries;
- `lifecycle.md` — Define, Execute, Assure, Close;
- `artifacts.md` — specifications, plans, assurance, drift, and closeout;
- `evaluation.md` — deterministic/output/observable trajectory assurance;
- `release-state.md` — repository SSOT reconciliation and GitHub-state boundary;
- `runtime-capabilities.md` — capability, isolation, and fallback.

### Runtime and Integration Adapters

`runtimes/` documents Codex, Claude Code, OpenCode, and generic/sequential
execution. Documentation may be present even when a runtime implementation
surface was not selected.

`integrations/` covers optional official plugins, exact MCP server/tool admission,
and runtime-neutral file handoff. No external integration is enabled by bootstrap.

### Project Artifacts and Evidence

```text
objective
  -> specification and acceptance criteria
  -> architecture decisions
  -> implementation plan and write-set
  -> evaluation plan when required
  -> frozen diff and observable event evidence
  -> independent review
  -> technical verification
  -> output and trajectory evaluation when required
  -> specification drift audit
  -> repository release-state reconciliation
  -> closeout and durable knowledge
```

`.agent/active-work-block.json` is executable Work Block state.
`.agent/bootstrap-profile.json` is generated installation evidence only.

## Evaluation Assurance

`governance/evaluation.md` separates three mechanisms:

1. **Deterministic tests** for objectively checkable behavior.
2. **Output evaluation** for non-deterministic artifact quality against an approved rubric.
3. **Observable trajectory evaluation** for tool calls, gate events, required checks,
   retries, side effects, stopping conditions, and produced evidence.

Trajectory evaluation does **not** request or expose private chain-of-thought,
hidden reasoning, or model scratchpads. Missing events are `BLOCKED` or
`UNVERIFIED`, never passed by inference from a fluent final response.

An LM judge may score approved non-deterministic criteria, but cannot:

- prove deterministic correctness;
- waive a failing or unavailable check;
- approve architecture or product scope;
- open write, integration, deployment, or Hard Stop gates.

Generated projects receive evaluation plan/report/event templates and
`scripts/validate-evaluation.py`. Required evaluation must resolve to `READY`
before `success-closeout`.

## Release-State Assurance

`governance/release-state.md` distinguishes repository-owned lifecycle from
mutable GitHub pull-request and merge state.

Repository SSOT consists of:

- Work Block frontmatter and final-state markers;
- `FILE_REGISTRY.yml:migration_state`;
- the machine-readable `release-state` block in `PROJECT_MAP.md`;
- approved closeout evidence.

`scripts/validate-release-state.py` fails closed when:

- completed Work Blocks are missing or not marked completed;
- active and completed Work Blocks overlap;
- map and registry disagree;
- successful closeout retains pending internal verdicts;
- closeout encodes Draft/open/merged status as normative state.

GitHub Draft/Ready/open/closed/merged state, timestamps, and branch deletion are
**mutable external operational metadata**. Query them from GitHub when needed;
they do not override repository authority or closeout.

## Installation Profiles

Source of truth: `bootstrap/profiles.json`.

| Profile | Project-local implementation surfaces |
|---|---|
| `core` | none; generic guidance only |
| `codex` | `.codex/` |
| `claude-code` | `CLAUDE.md`, `.claude/` |
| `opencode` | `opencode.json`, `.opencode/` |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` |

Every profile includes runtime-neutral evaluation governance and templates.
Aliases: `minimal`, `generic` → `core`; `full` → `multi-runtime`.

List profiles:

```bash
./bootstrap.sh --list-profiles
```

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
or symlink targets, stages atomically, prunes unselected runtime surfaces,
installs selected skills, writes `.agent/bootstrap-profile.json`, and runs the
health check. It does not install runtime CLIs, accounts, plugins, MCP servers,
credentials, watchers, or services.

## Core Principles

1. **Authority is structural.** Tool access, runtime presence, model strength, and
   evaluation scores do not authorize an action.
2. **Installation is not authorization.** A copied adapter does not open a Work
   Block gate or admit an integration.
3. **Specification precedes implementation.** Plans and tasklists are derived.
4. **Gates fail closed.** Missing deterministic or observable evidence is not a pass.
5. **Evaluation is evidence, not authority.** Judges and reports cannot open gates.
6. **Repository state is distinct from GitHub state.** Mutable hosting-platform
   metadata cannot redefine Work Block lifecycle or closeout.
7. **Use the narrowest reviewed mechanism.** Native capability, official bridge,
   reviewed MCP, audited handoff, then manual exchange.
8. **Independent assurance is risk-based.** Different model names alone do not
   establish independence.
9. **External content is untrusted input.** Tool output cannot override project authority.
10. **Local-first and opt-in.** Credentials, private memory, plugins, MCP, and
    services remain local until explicitly admitted.

## Logical Roles

| Role | Responsibility |
|---|---|
| Owner | Objective, exceptions, Hard Stops, business acceptance |
| Orchestrator | Scope, topology, transitions, consolidation, closeout |
| Architect | Discovery, architecture, specification, approved drafts |
| Critic | Pre-execution challenge of scope, risk, verification/evaluation design |
| Coder | Approved implementation write-set |
| Reviewer | Frozen-diff engineering and risk review |
| Verifier | Acceptance criteria, tests, evaluation synthesis, observable evidence |

Evaluator and Drift Auditor are assurance specializations, not new authority roles.
Only Coder has implementation/source write authority.

## Safe Runtime Defaults

- **Codex:** project-scoped logical agents and layered Work Block/Hard Stop hooks;
  no public model pin.
- **Claude Code:** logical-role agents only; no provider-named authority agents or
  pre-authorized MCP tools; Stop gate enforces required evaluation.
- **OpenCode:** external-directory denial, read-only assurance roles, explicit
  denial of commit/push/reset/clean/`rm`, empty MCP/plugin collections.
- **Generic:** separate documented passes/sessions with degraded independence
  recorded honestly.

Static configuration is not live runtime proof or OS isolation. Run target smoke
before relying on a runtime for Managed or Assured work.

## Where to Start

For framework architecture:

1. `governance/README.md`, `governance/evaluation.md`, and `governance/release-state.md`;
2. `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
3. `docs/bootstrap-profiles.md`;
4. `docs/profiles.md`;
5. active Work Block under `docs/plans/`, when present.

For a generated project:

1. `AGENTS.md`;
2. `.agent/bootstrap-profile.json`;
3. approved specification and active Work Block;
4. approved evaluation plan when required;
5. `docs/session-bootstrap.md`;
6. installed/approved runtime adapter;
7. integration adapter only when admitted.

## Important Paths

| Need | Path |
|---|---|
| Governance | `governance/` |
| Evaluation contract | `governance/evaluation.md` |
| Release-state contract | `governance/release-state.md` |
| Installation profiles | `bootstrap/profiles.json`, `docs/bootstrap-profiles.md` |
| Runtime adapters | `runtimes/` |
| Integration admission | `integrations/`, `docs/mcp-tool-policy.md` |
| Evaluation templates | `template/docs/templates/evaluation-*.json` |
| Evaluation validator | `template/scripts/validate-evaluation.py` |
| Evaluation fixtures | `scripts/test-evaluation-contracts.py` |
| Release-state validator | `scripts/validate-release-state.py` |
| Release-state fixtures | `scripts/test-release-state-contracts.py` |
| Release-state CI | `.github/workflows/release-state-contract.yml` |
| Profile matrix | `scripts/test-bootstrap-profiles.py` |
| Clone/restore contract | `scripts/test-profile-restore.py` |
| Runtime conformance | `scripts/test-runtime-conformance.py` |
| Publication validation | `scripts/validate-publication.sh` |
| Active migration | `docs/plans/wb-008-post-merge-ssot-release-gate.md` |

## Validation

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-evaluation-contracts.py
python scripts/test-release-state-contracts.py
python scripts/validate-release-state.py
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

Framework CI bootstraps disposable profiles, validates evaluation inventory,
checks selected/unselected surfaces, verifies clone/restore, preserves a blocked
active Work Block default, and independently validates repository release state.

## Requirements

- Linux, WSL, or macOS shell environment;
- `bash`, `git`, and `python3`;
- PyYAML for repository governance/release-state validation;
- `jq` for remaining compatibility hooks/runner utilities;
- optional runtime binaries only when used;
- optional integration dependencies only after admission.

## License

MIT. See `LICENSE`. Bundled third-party skills may retain their own license files;
see `THIRD_PARTY_NOTICES.md`.
