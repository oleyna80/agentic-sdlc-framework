# Framework Profiles

The framework separates **installation composition** from **Work Block control**.
Do not collapse these dimensions into one vendor-specific preset.

A generated project has one recorded installation profile:

```yaml
installation_profile: codex
```

Each Work Block then selects independently:

```yaml
governance_profile: Managed
runtime_profile: codex
integration_profile: none
model_class: balanced_engineering
isolation: separate_subagent
```

Installation determines which project-local runtime surfaces and skills were
copied. Governance determines required control and evidence. Runtime determines
who executes a logical function. Integration determines an admitted external
bridge/tool/transport. Model and isolation record actual execution.

## 1. Installation Profiles

Source of truth: `bootstrap/profiles.json`.

Detailed guide: `docs/bootstrap-profiles.md`.

| Installation profile | Project-local implementation surfaces | Default use |
|---|---|---|
| `core` | none; generic guidance only | smallest runtime-neutral scaffold |
| `codex` | `.codex/` | Codex-primary project |
| `claude-code` | `CLAUDE.md`, `.claude/` | Claude Code-primary project |
| `opencode` | `opencode.json`, `.opencode/` | OpenCode-primary project after smoke |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | backward-compatible default and mixed-runtime evaluation |

Aliases:

- `minimal`, `generic` → `core`;
- `full` → `multi-runtime`.

Rules:

- installation profile is chosen at scaffold time;
- `.agent/bootstrap-profile.json` records the resolved result;
- installed files do not grant Work Block authority;
- runtime documentation may exist even when its executable surface is absent;
- installed runtime files do not prove the CLI, auth, provider, hooks, sandbox,
  or isolation actually work;
- changing installation composition is a deliberate migration, not an automatic
  reaction to a Work Block runtime choice;
- no profile activates plugins, MCP servers, external runtime calls, credentials,
  watchers, or services.

## 2. Governance Profiles

Governance profiles describe how much control and assurance a Work Block needs.
They are independent from installation and runtime choice.

### Advisory

Use for read-only research, architecture discussion, explanation, audit, or
decision support without repository mutation.

Required:

- objective and scope;
- inspected sources;
- assumptions and inspection gaps;
- no write authority;
- no external/live mutation.

### Controlled

Use for small, bounded, low-risk changes.

Required:

- explicit objective and write-set;
- one Coder;
- side-effect and Hard Stop classification;
- targeted review/checks;
- rollback path;
- closeout summary.

Upgrade when behavior, contracts, architecture, security, runtime, integration,
or multiple domains are affected.

### Managed

Default for non-trivial product and engineering work.

Required:

- approved specification and revision;
- accepted architecture baseline;
- implementation plan and task decomposition;
- Critic when triggered;
- one Coder per write-set;
- independent Reviewer;
- Verifier with reproducible evidence;
- durable reports and SSOT synchronization.

```text
Define -> Critic -> Execute -> Review -> Verify -> Close
```

### Assured

Use when failure cost or ambiguity is materially higher, including:

- authentication/authorization;
- payments, orders, stock, CRM, or consequential mutations;
- DB schemas and migrations;
- webhooks/external providers;
- deployment, infrastructure, runtime configuration, or security headers;
- sensitive data or credentials;
- major architecture or public API changes.

Managed controls plus:

- stronger Reviewer/Verifier isolation;
- threat/abuse analysis where relevant;
- Full verification tier;
- Specification Drift Audit;
- runtime evidence when accessible;
- explicit degraded-mode handling;
- residual risk and recovery evidence.

### Distributed

Use when work is deliberately split across multiple runtimes, machines,
worktrees, or teams.

Assured controls plus:

- explicit handoff contract;
- capability snapshot for every participant;
- non-overlapping write-sets;
- separate roots/worktrees for parallel writers;
- durable queue/status/recovery when needed;
- consolidation report;
- assurance of the merged result;
- one Orchestrator accountable for closure.

Distributed does not mean “use more agents by default.”

## 3. Runtime Profiles

Runtime profiles describe how logical functions execute. Select from installed
or otherwise explicitly approved runtime capability.

### Codex

Adapter: `runtimes/codex/`.

Project-local surface exists only in `codex` or `multi-runtime` installation
profiles. Native subagents/custom agents may bind logical roles, but model or
agent names do not redefine authority.

### Claude Code

Adapter: `runtimes/claude-code/`.

Project-local surface exists only in `claude-code` or `multi-runtime` profiles.
`.claude/agents`, hooks, skills, and memory are runtime mechanics mapped to the
logical roles and gates.

### OpenCode

Adapter: `runtimes/opencode/`.

Project-local surface exists only in `opencode` or `multi-runtime` profiles.
Use after a target-environment smoke establishes provider, agent, permission,
tool, and denied-action behavior. Static configuration is not OS isolation.

### Generic / Sequential

Adapter: `runtimes/generic/`.

Available as guidance in every installation profile. Use for an IDE assistant,
manual CLI session, local model, or runtime without native subagents. Required
functions run as separate documented passes/sessions; degraded independence is
recorded honestly.

### Custom Runtime

A custom adapter declares:

- supported logical functions;
- read/write and side-effect controls;
- isolation mechanisms;
- hooks/enforcement;
- skills/tools/integrations;
- limitations and fallback;
- capability evidence.

## 4. Integration Profiles

Integrations connect runtimes or external tools. They do not define governance
or become active because a configuration file is installed.

### None

One runtime performs the Work Block without an external bridge.

### Official Plugin

Use a maintained official integration only after admission covers exact
capability, scope, data, credentials, side effects, recovery, and evidence.

### MCP

Use for structured tool/runtime access when the exact server and tool names,
authority, credentials, data boundary, side effects, and output contract are
understood. An installed empty `.mcp.json` is not admission.

### File-Based Handoff

Use `handoff/` when durable queueing, crash recovery, cross-machine execution,
formal scope audit, or observable delivery logs justify the overhead.

### Direct Runtime CLI

Launching `codex`, `claude`, or `opencode` as a child process is an integration.
It requires an active/fresh Work Block, matching integration ID, and concrete
admission-evidence path. It does not grant child write authority.

### Manual Handoff

Use a portable task/result artifact when automation is unavailable. Preserve
Work Block ID, scope, write-set, authority, acceptance criteria, evidence, and
actual runtime/isolation.

## 5. Model Routing Overlay

Use portable model classes:

- `strong_reasoning` — architecture, ambiguity, Critic, high-risk decisions;
- `balanced_engineering` — implementation, review, verification;
- `fast_readonly` — discovery, classification, documentation sync;
- `local_executor` — bounded work after smoke testing.

Concrete model names belong in runtime/user configuration or execution evidence.
A stronger model does not grant broader authority; a cheaper model does not
remove assurance requirements.

Record requested class, actual runtime/model when observable, effort/reasoning,
fallback, quality limitations, and budget posture.

## 6. Isolation Levels

Record the actual boundary, not the desired label:

```text
same_context
separate_subagent
separate_session
separate_worktree
separate_runtime
os_isolated
```

Different model names in one context are not independent assurance. Sensitive
credentials/live data/deploy verification may require OS isolation.

## 7. Selection Matrix

| Work characteristic | Installation | Governance | Runtime | Integration |
|---|---|---|---|---|
| Read-only discussion | any/core | Advisory | any capable runtime | none |
| Small isolated fix | core or one runtime | Controlled | one safe runtime | none |
| Normal product feature | one runtime or multi | Managed | capable installed/approved runtime | optional |
| Auth/DB/payment/deploy/security | suitable runtime surface | Assured | stronger isolation/evidence | admitted only if needed |
| Parallel independent work | multi or approved external runtimes | Distributed | multiple isolated roots/runtimes | handoff/native coordination |
| Cross-machine durable delegation | any documented scaffold | Distributed | mixed | file handoff |

## 8. Selection Rules

- Start with the smallest installation profile needed for expected project use.
- Start each Work Block with the smallest governance profile that can safely
  prove the objective.
- Increase governance because of risk/evidence needs, not because more runtimes
  are installed.
- Select a runtime after checking both installation state and actual capability.
- Prefer native or official integrations when they satisfy the admitted contract.
- Use file handoff only when durability/recovery justify it.
- Keep provider credentials and private runtime configuration outside the public
  framework.
- A missing preferred capability produces a recorded fallback, not a missing
  logical function.
- Never describe same-context review as independent.
- Reassess profiles when scope or risk changes.

## 9. Generated Project Evidence

Every generated project contains common portable contracts plus:

```text
.agent/bootstrap-profile.json
scripts/validate-installation-profile.py
```

Run:

```bash
bash scripts/bootstrap.sh
```

This checks selected required paths and known unselected paths. It does not prove
live runtime authentication, network access, plugin installation, or OS
isolation.

Runtime-specific directories may coexist only when selected by installation
profile or deliberately migrated later. Their presence is implementation
availability, not authority.
