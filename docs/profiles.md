# Framework Profiles

Profiles describe separate dimensions. They must not collapse governance,
runtime, integration, model, and isolation into one vendor-specific preset.

For each Work Block select:

```yaml
governance_profile: Managed
runtime_profile: codex
integration_profile: none
model_class: balanced_engineering
isolation: separate-subagent
```

A higher-risk Work Block might use:

```yaml
governance_profile: Assured
runtime_profile: claude-code
integration_profile: claude-code-codex-plugin
model_class: strong_reasoning
isolation: separate-runtime-same-machine-same-checkout
```

The Governance Core remains unchanged.

## 1. Governance Profiles

### Advisory

Use for research, explanation, architecture discussion, read-only audit, and
decision support without repository mutation.

Required:

- objective and scope;
- inspected sources;
- assumptions and inspection gaps;
- no write authority;
- no external or live mutation.

```text
Intake -> inspect -> analyze -> report
```

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

- approved specification/revision and architecture baseline;
- implementation plan and task decomposition;
- Critic when triggered;
- one Coder per write-set;
- independent Reviewer;
- Verifier with reproducible evidence;
- durable reports and SSOT synchronization.

```text
Define -> Critic -> Execute -> Review -> Verify -> Close
```

Use native subagents when available, but preserve functions through separate
passes/sessions/runtimes when unavailable.

### Assured

Use when failure cost or ambiguity is materially higher, commonly for:

- authentication/authorization;
- payments, orders, stock, CRM, or consequential mutations;
- DB schemas/migrations;
- webhooks and external providers;
- deployment, infrastructure, runtime configuration, security headers;
- sensitive data or credentials;
- major architecture or public contract changes.

Managed controls plus:

- stronger Critic/Reviewer/Verifier isolation;
- threat or abuse analysis where relevant;
- Full-tier verification;
- Specification Drift Audit;
- runtime/integration evidence;
- explicit degraded-mode handling;
- residual risk and recovery evidence.

### Distributed

Use when work is split across runtimes, machines, worktrees, users, or teams.

Assured controls plus:

- portable handoff contract;
- capability snapshot for every participant;
- integration admission for every automated bridge/transport;
- non-overlapping write-sets and separate roots/worktrees for parallel writers;
- durable queue/status/recovery where needed;
- consolidation report and assurance of the merged result;
- one accountable Orchestrator.

Distributed is not “more agents by default.” Use it only when independence,
parallelism, recovery, or auditability justifies the overhead.

## 2. Runtime Profiles

Runtime profiles map logical functions to an execution system.

### Codex

Adapter: `runtimes/codex/`

Generated baseline includes project-scoped logical-role agents, machine-readable
write gates, shared Hard Stops, and Codex-specific wrappers. Concrete models,
provider settings, auth, and private MCP configuration remain user-local.

### Claude Code

Adapter: `runtimes/claude-code/`

Generated baseline includes logical-role agents, machine-readable source-write
and assurance hooks, skills, and operational memory. No provider-named authority
agents or external integrations are enabled by default.

### OpenCode

Adapter: `runtimes/opencode/`

Generated baseline includes `opencode.json` and logical-role project subagents.
It denies secret paths/external directories, requires approval for edits/Bash/
web/MCP, denies commit/push/destructive commands, and starts with empty plugin
and MCP collections.

Use for Managed/Assured work only after a target-environment capability and
denied-action smoke.

### Generic / Sequential

Adapter: `runtimes/generic/`

Use for an IDE assistant, manual CLI, local model, or runtime without subagents.
Perform required functions as separate documented passes or sessions and record
reduced independence honestly.

### Custom Runtime

A custom adapter declares:

- supported logical functions;
- read/write and side-effect controls;
- isolation mechanisms;
- hooks/permissions/enforcement;
- skills, tools, plugins, and MCP capabilities;
- secret/data/network boundaries;
- known limitations and fallback;
- capability evidence and version.

## 3. Integration Profiles

Integrations connect runtimes, tools, services, or transports. They do not define
roles or governance.

Every non-`none` automated integration requires:

- admission record based on
  `docs/templates/integration-admission-template.md`;
- active Work Block binding to a logical function;
- exact authority, tools, scope, data/secret boundary, Hard Stops, evidence,
  failure/recovery, and disable procedure;
- target-environment smoke.

### None

Default. One runtime performs the Work Block without an automated external
bridge. Manual reading of public documentation is not an integration profile.

### Claude Code Codex Plugin

ID: `claude-code-codex-plugin`

Adapter: `integrations/claude-code-codex-plugin/`

Preferred optional route when Claude Code invokes the official local Codex
plugin for review, adversarial review, or bounded delegation. It is a separate
runtime on the same machine/checkout/auth environment unless stronger isolation
is established.

### MCP

ID: project-defined server/tool ID.

Adapter: `integrations/mcp/`

Use only after exact server/tool admission. `.mcp.json` starts empty. Grant
individual tools, not the whole server, and keep credentials outside committed
configuration.

Codex MCP is a compatibility route, not the default Claude Code/Codex bridge.

### File Handoff

ID: `file-handoff` plus transport implementation.

Adapter: `integrations/file-handoff/` and `handoff/`.

Use when durable queueing, recovery, cross-machine execution, formal scope audit,
or an observable delivery log is needed. Use the runtime-neutral task envelope.
The existing Claude Code runner is a compatibility implementation.

### Hosted Connector / Tool

ID: project-defined.

Use for GitHub, issue trackers, browsers, documentation systems, monitoring, and
other connected services. Admit exact actions. Read-only access does not imply
write/send/deploy permission.

### Direct Runtime CLI / Process

IDs used by the shared gate include:

- `codex-cli`;
- `opencode-cli`;
- `claude-code-cli`.

Use only as an explicit integration. The active Work Block must list the ID and
admission record. Child-runtime writes require their own Coder authority and
write-set.

### Manual Handoff

No automated integration process. Use a portable task and result artifact with
Work Block ID, logical function, scope, authority, acceptance criteria, evidence,
and actual runtime/isolation.

## 4. Model Routing Overlay

Portable model classes:

- `strong_reasoning` — architecture, ambiguity, Critic, high-risk decisions;
- `balanced_engineering` — implementation, review, verification;
- `fast_readonly` — discovery, classification, documentation sync;
- `local_executor` — bounded work after capability smoke.

Concrete model/provider names belong in private runtime configuration or
execution evidence. A stronger model does not grant authority; a cheaper model
does not remove assurance requirements.

Record requested class, actual runtime/model when observable, effort setting,
fallback, limitations, and budget posture.

## 5. Selection Matrix

| Work characteristic | Governance | Runtime | Integration |
|---|---|---|---|
| Read-only discussion | Advisory | Any capable runtime | None |
| Small isolated fix | Controlled | Runtime with safe write boundary | None |
| Normal product feature | Managed | Codex, Claude Code, OpenCode, generic | None or admitted tool |
| Auth/DB/payment/deploy/security | Assured | Runtime supporting stronger evidence/isolation | Admitted second runtime/tool when useful |
| Independent frontend/backend work | Distributed | Multiple roots/worktrees/runtimes | Native coordination or file handoff |
| Cross-machine durable delegation | Distributed | Mixed | File handoff |
| Claude Code needs Codex review | Managed/Assured | Claude Code | Official Codex plugin preferred |
| Structured external tool access | Risk-based | Any supporting runtime | MCP/hosted connector after admission |

## 6. Selection Rules

- Start with the smallest governance profile that can safely prove the objective.
- Increase governance because of risk/evidence, not available agent count.
- Inspect actual runtime capabilities before selection.
- Keep integration profile `none` unless an external bridge/tool/transport adds
  necessary value.
- Prefer native capability, then official integration, reviewed MCP, audited
  handoff, manual exchange, and only then exceptional direct process bridges.
- Availability does not imply permission.
- Missing preferred capability produces a recorded fallback, not a missing
  function.
- Never describe same-context or same-checkout work as stronger isolation than it
  is.
- Reassess profiles when scope, risk, version, configuration, or tool inventory
  changes.

## 7. Generated Project Baseline

```text
AGENTS.md
CLAUDE.md
opencode.json
governance/
runtimes/
integrations/
.agent/
.codex/
.claude/
.opencode/
.mcp.json
docs/specs/
docs/plans/
docs/reports/
docs/engineering-memory/
docs/templates/
memory_bank/
```

Runtime-specific directories may coexist. External integrations remain inert
until admitted. Projects may deliberately remove unused adapters, but must not
treat a runtime configuration as authority-bearing core policy.

## 8. Publishing Agent and Integration State

Before publishing, review:

- credentials, auth, provider and MCP configuration;
- private client/user context and live identifiers;
- raw transcripts or hidden reasoning;
- local paths and external-directory grants;
- downloaded plugins/packages, logs, caches, and handoff runtime state;
- unverified runtime/integration conclusions;
- data sent to external providers or services;
- auto-approval and write/send/deploy permissions.

Publish reusable governance, adapter contracts, and evidence only after
deliberate review.
