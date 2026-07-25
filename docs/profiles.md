# Framework Profiles

Profiles now describe **how much governance is required**, not which vendor or
agent runtime must be used.

Choose three independent settings for each Work Block:

```yaml
governance_profile: Managed
runtime_profile: codex-native
integration_profile: none
```

A different Work Block might use:

```yaml
governance_profile: Assured
runtime_profile: claude-code
integration_profile: codex-plugin
```

The governance contract remains the same.

## 1. Governance Profiles

### Advisory

Use for:

- research;
- architecture discussion;
- code explanation;
- read-only audit or recommendations;
- decision support without repository mutation.

Required controls:

- objective and scope;
- inspected sources;
- assumptions and inspection gaps;
- no write authority;
- no external or live mutation.

Typical flow:

```text
Intake -> inspect -> analyze -> report
```

### Controlled

Use for small, bounded, low-risk changes.

Required controls:

- explicit objective and write-set;
- one Coder;
- side-effect and Hard Stop classification;
- targeted review and checks;
- rollback path;
- closeout summary.

Typical flow:

```text
Define scope -> Execute -> targeted assurance -> Close
```

Upgrade when behavior, contracts, architecture, security, runtime, or multiple
domains are affected.

### Managed

Default for non-trivial product and engineering work.

Required controls:

- approved specification and revision;
- accepted architecture baseline;
- implementation plan and task decomposition;
- Critic when triggered;
- one Coder per write-set;
- independent Reviewer;
- Verifier with reproducible evidence;
- durable reports and SSOT synchronization.

Typical flow:

```text
Define -> Critic -> Execute -> Review -> Verify -> Close
```

Use native subagents when available, but preserve the functions through separate
passes or sessions when they are not.

### Assured

Use when failure cost or ambiguity is materially higher.

Triggers commonly include:

- authentication or authorization;
- payments, orders, stock, CRM, or consequential mutations;
- DB schemas and migrations;
- webhooks and external providers;
- deployment, infrastructure, runtime configuration, or security headers;
- sensitive data or credentials;
- major architecture changes;
- public APIs and durable contracts.

Managed controls plus:

- stronger Reviewer/Verifier isolation;
- threat or abuse analysis where relevant;
- Full-tier verification;
- Specification Drift Audit;
- runtime evidence when accessible;
- explicit degraded-mode handling;
- residual risk and recovery evidence.

Typical flow:

```text
Define -> independent Critic -> Execute -> independent Review
       -> Full Verification -> Drift Audit -> Close
```

### Distributed

Use when work is split across multiple runtimes, machines, worktrees, or teams.

Assured controls plus:

- explicit handoff contract;
- runtime capability snapshot for every participant;
- non-overlapping write-sets;
- separate worktrees for parallel writers;
- durable queue/status/recovery when needed;
- consolidation report;
- assurance of the merged result;
- one Orchestrator accountable for final closure.

Distributed does not mean "use more agents by default." Use it only when
parallelism, independent execution, recovery, or formal auditability provides a
clear benefit.

## 2. Runtime Profiles

Runtime profiles describe how logical functions are executed.

### Codex Native

Adapter: `runtimes/codex/`

Use when Codex provides the primary orchestration, coding, review, or verification
runtime. Native subagents and custom agents may execute logical roles, but model
or agent names do not redefine authority.

Project-specific `.codex/` configuration may add hooks, agents, MCP servers, and
sandbox settings. Keep credentials and user-level provider settings private.

### Claude Code

Adapter: `runtimes/claude-code/`

Use when Claude Code provides the primary runtime or an external implementation
team. Existing `.claude/agents`, hooks, skills, and memory are runtime mechanics.
They must map to the logical roles and gates in the governance core.

### OpenCode

Adapter: `runtimes/opencode/`

Use after a capability smoke check establishes available agents, providers,
permissions, tools, and isolation. Do not assume feature parity with another
runtime.

### Generic / Sequential

Adapter: `runtimes/generic/`

Use for an IDE assistant, manual CLI session, local model, or runtime without
native subagents. Required functions are performed as separate documented passes
or sessions. Record degraded independence honestly.

### Custom Runtime

A custom adapter must declare:

- supported functions;
- read/write and side-effect controls;
- isolation mechanisms;
- hooks or enforcement;
- skills/tools/integrations;
- known limitations;
- fallback behavior;
- capability evidence.

## 3. Integration Profiles

Integrations connect runtimes or external tools. They do not define governance.

### None

One runtime performs the Work Block.

### Official Plugin

Use an official integration when it provides the required capability, scope,
observability, and recovery. Examples include one agent runtime invoking another
through a maintained plugin.

### MCP

Use MCP for structured tool or runtime access when the server's authority,
credentials, side effects, and output contract are understood.

### File-Based Handoff

Use the existing `handoff/` layer when durable queueing, crash recovery,
cross-machine execution, formal scope audit, or an observable delivery log is
required.

### Manual Handoff

Use a portable task file and result report when no automated transport is
available. Preserve Work Block ID, scope, write-set, authority, acceptance
criteria, evidence, and actual runtime/isolation.

## 4. Model Routing Overlay

Model routing is separate from governance and runtime choice.

Use logical model classes in portable artifacts:

- `strong_reasoning` — architecture, ambiguity, critic, high-risk decisions;
- `balanced_engineering` — implementation, review, verification;
- `fast_readonly` — discovery, classification, documentation sync;
- `local_executor` — bounded work after smoke testing.

Concrete model names belong in runtime configuration or Work Block execution
evidence. A stronger model does not grant broader authority. A cheaper model does
not remove required review or verification.

Record:

- requested model class;
- actual runtime and model when observable;
- reasoning/effort setting when relevant;
- fallback used;
- quality limitations;
- budget posture.

## 5. Selection Matrix

| Work characteristic | Governance | Runtime | Integration |
|---|---|---|---|
| Read-only discussion | Advisory | Any capable runtime | None |
| Small isolated fix | Controlled | Any runtime with safe write scope | None |
| Normal product feature | Managed | Codex, Claude Code, OpenCode, or generic | Optional |
| Auth/DB/payment/deploy/security | Assured | Runtime supporting stronger isolation and evidence | Optional second runtime/plugin |
| Independent frontend/backend work | Distributed | Multiple worktrees/runtimes | Handoff or native coordination |
| Cross-machine durable delegation | Distributed | Mixed | File-based handoff |

## 6. Selection Rules

- Start with the smallest profile that can safely deliver the objective.
- Increase governance because of risk and evidence needs, not because more agents
  are available.
- Select a runtime after inspecting actual capabilities.
- Prefer native or official integrations when they satisfy the contract.
- Use file-based handoff when durability and recovery justify the overhead.
- Keep provider credentials and private runtime configuration outside the public framework.
- A missing preferred capability produces a recorded fallback, not a missing function.
- Never describe same-context review as independent.
- Reassess the profile when scope or risk changes.

## 7. Generated Project Baseline

A generated project should contain:

```text
AGENTS.md
governance/
runtimes/
.agent/ROSTER.md
.agent/workflows/sdd-protocol.md
docs/specs/
docs/plans/
docs/reports/
docs/engineering-memory/
docs/templates/work-block-template.md
docs/templates/spec-drift-report-template.md
memory_bank/
```

Runtime-specific directories such as `.codex/` and `.claude/` are adapters and
may coexist. Projects should customize or remove unused adapters deliberately,
not treat them as authority-bearing core policy.

## 8. Publishing Agent State

Generated projects are local-first. Before publishing agent/runtime state,
review for:

- credentials and provider configuration;
- private client or user context;
- raw transcripts or hidden reasoning;
- local machine paths;
- generated logs and caches;
- unverified conclusions;
- live data or operational identifiers.

Publish reusable governance, adapters, and evidence only after deliberate review.
