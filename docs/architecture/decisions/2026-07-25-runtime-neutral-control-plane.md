# ADR — Runtime-Neutral Agentic SDLC Control Plane

- **ID:** 2026-07-25-runtime-neutral-control-plane
- **Status:** accepted
- **Scope:** framework architecture, agent roles, runtime integrations, project templates
- **Last verified:** 2026-07-25

## Decision

The Agentic SDLC Framework is a **runtime-neutral control plane for managed
software delivery**. It defines authority, lifecycle state, required artifacts,
risk gates, evidence, and closeout semantics. Codex, Claude Code, OpenCode,
Antigravity, and future agent systems are execution runtimes that implement this
contract through adapters.

The governance core must not make a specific runtime, model family, plugin, MCP
server, CLI command, or handoff transport authoritative.

## Context

The framework originally grew around a practical topology in which Codex acted
as a control tower and delegated bounded execution or second-opinion work to
Claude Code. At that time, native subagent behavior and cross-runtime control
were less consistent, so file-based handoff, provider-named roles, explicit
queues, and runtime-specific gates provided useful operational control.

Agent runtimes now increasingly provide native subagents, custom roles, skills,
hooks, plugins, provider routing, and direct integrations. Re-implementing these
mechanisms inside the core SDLC would duplicate runtime behavior and make the
framework age whenever one provider changes its orchestration model.

The durable value of the framework is therefore management, not process
launching:

- scope and authority control;
- decision and specification management;
- risk and side-effect classification;
- execution topology and isolation requirements;
- independent review and verification contracts;
- evidence, drift detection, and closeout;
- durable, runtime-independent project knowledge.

## Architectural Rules

### 1. Stable logical roles

The core recognizes these logical roles:

- **Owner** — approves objectives, policy exceptions, and hard-stop actions.
- **Orchestrator** — owns scope, topology, stage transitions, consolidation, and
  closeout.
- **Architect** — produces evidence-backed architecture and specification
  proposals.
- **Critic** — independently challenges plans, risks, assumptions, and proposed
  verification before execution.
- **Coder** — modifies only the approved write set.
- **Reviewer** — inspects the frozen diff for defects, regressions, security,
  architecture, and maintainability.
- **Verifier** — gathers evidence against acceptance criteria and contracts.

These are functions and authority classes. They do not require separate
processes for low-risk work. A runtime may map several functions to one agent
when the selected governance profile permits it.

### 2. Runtime, model, role, and isolation are separate dimensions

Every delegated function may be described independently:

```yaml
function: verification
role: verifier
runtime: codex
model_class: balanced_engineering
isolation: separate_subagent
authority: read_only
```

Changing the runtime or model never expands authority.

### 3. Capability negotiation

The Orchestrator selects an execution topology from declared capabilities, not
from provider names. Relevant capabilities include:

- native subagents;
- custom agent profiles;
- read-only and write sandboxes;
- hooks or policy interception;
- parallel read and write execution;
- worktree support;
- skills;
- MCP or plugin integrations;
- browser/runtime verification;
- independent session or OS isolation.

If a runtime lacks a required capability, the framework selects a documented
fallback and records the degraded assurance level.

### 4. Artifacts are the interoperability boundary

Agents exchange approved, versioned artifacts rather than depending on hidden
chat history. The minimum portable chain is:

```text
objective → specification → implementation plan → frozen diff
          → review report → verification report → drift report → closeout
```

Operational logs may support this chain but do not override normative artifacts.

### 5. Native integrations are preferred; transports are optional

Use the smallest reliable mechanism available:

1. native runtime capability;
2. official plugin or supported integration;
3. approved MCP integration;
4. file-based handoff with audit and recovery;
5. manual session handoff.

The existing Codex → Claude Code file handoff remains supported as an advanced
transport for observability, recovery, cross-machine execution, or runtimes
without a direct integration. It is no longer part of the governance core.

### 6. The core fails closed

Missing runtime capabilities, unavailable reviewers, failed gates, or incomplete
verification may lead to diagnostics, corrective planning, or reporting-only
closeout. They must not silently upgrade a blocked or unverified change to
release-ready status.

## Target Layers

```text
Governance Core
  authority · lifecycle · risks · artifacts · verification · closeout · SSOT

Runtime Adapters
  Codex · Claude Code · OpenCode · Generic sequential agent

Integration Adapters
  official plugins · MCP · file handoff · manual handoff

Project Artifacts
  specifications · plans · decisions · reports · engineering memory
```

## Consequences

### Positive

- Project documentation can be used by any capable agent runtime.
- Runtime upgrades do not require redesigning the SDLC authority model.
- Provider-specific functionality can evolve independently in adapters.
- Cross-runtime comparison and conformance testing become possible.
- The framework focuses on its strongest value: controlled delivery and
  evidence-based management.

### Tradeoffs

- Existing provider-specific language must be migrated gradually.
- Some current files will temporarily contain compatibility terminology.
- Runtime adapters need explicit capability maps and smoke tests.
- A generic core cannot guarantee enforcement unless an adapter supplies hooks,
  sandboxes, or an external policy boundary.

## Migration Strategy

1. Add the governance core and runtime adapter boundaries.
2. Normalize roles, lifecycle stages, SSOT, Reviewer, Verifier, and drift audit.
3. Add Codex-native custom agents and executable write gates.
4. Reclassify Claude Code hooks, official Codex integration, OpenCode support,
   and file handoff as adapters.
5. Add profile-aware bootstrap and cross-runtime conformance scenarios.
6. Deprecate duplicated provider-specific policy only after equivalent adapter
   documentation and validation exist.

## Evidence

- Work Block: `docs/plans/wb-001-runtime-neutral-control-plane.md`
- Existing framework map: `PROJECT_MAP.md`
- Existing runtime profiles: `docs/profiles.md`
- Existing Codex routing guidance: `framework/workflow/codex-model-routing.md`
- Existing file transport: `handoff/`

## Review Trigger

Review this decision when the framework introduces a new authority-bearing role,
when a runtime-specific adapter attempts to override core governance, or when
cross-runtime conformance tests show that the artifact contracts are
insufficient.
