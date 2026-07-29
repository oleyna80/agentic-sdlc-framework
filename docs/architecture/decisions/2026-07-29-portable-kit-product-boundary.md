---
schema_version: 1
artifact_type: architecture_decision
artifact_id: 2026-07-29-portable-kit-product-boundary
status: proposed
created_at: 2026-07-29
source_framework_revision: 0fce7389d27690482e910e942a1f3138c2fef123
historical_framework_revision: 0c632db0b0444e556251c384f6254141c9df59bc
superpowers_reference_revision: 44c9b2d6e889982ac18c27d05a19fefe335194e1
---

# ADR — Portable Kit Product Boundary

## Context

The framework began as a practical repository-local Agentic SDLC: an entry
contract, Work Blocks, specification and plan artifacts, scoped implementation,
independent review and verification, memory, logs, and closeout. It later grew
into a runtime-neutral control plane with runtime adapters, capability
negotiation, hooks, provider profiles, MCP/plugin guidance, evaluation
infrastructure, release-state contracts, and provider-specific configuration.

The later architecture improved authority semantics but expanded framework
ownership into concerns already owned by AI runtimes and project tooling. The
portable successor requires an unambiguous product boundary before candidate
implementation.

## Decision

The target product is a complete **Portable Agentic SDLC Project Kit**. It is not
merely a skills library and it is not a runtime control plane.

The kit owns repository artifacts that define and record software-delivery work:

- `AGENTS.md` shared authority and Hard Stops;
- SDD lifecycle and process levels;
- role contracts and procedural skills;
- Work Blocks, specifications, ADRs, plans, tasklists, mission briefs, and
  handoffs;
- canonical `memory_bank/` and logs;
- Critic, Reviewer, Verifier, and closeout artifacts;
- a generic, collision-safe installation contract.

Artifacts are the portability boundary. The kit must work through native
subagents, sequential single-agent passes, and manual copy-and-paste handoffs.
No execution mode is authoritative by itself.

The kit does not own or require:

- `.codex/`, `.claude/`, `.opencode/`, or provider-specific agent definitions;
- model routing or capability negotiation;
- hooks, runtime permission configuration, MCP, or plugins;
- provider snapshots, runtime profiles, queues, daemons, or duplicated skill
  mirrors;
- runtime-specific installation or conformance control planes.

Projects and users may maintain local runtime configuration independently. It
must not redefine kit authority and is not installed, synchronized, or verified
by the kit.

The practical lifecycle is retained:

```text
Work Block
  → discovery / specification / architecture
  → implementation plan and tasks
  → Critic when required
  → scoped implementation
  → Review
  → Verification
  → SSOT and memory synchronization
  → truthful closeout
```

Optional engineering capabilities remain outside the core: nondeterministic
evaluation, advanced security tooling, browser/UI testing, worktree automation,
Git branch finishing, external second-model review, skill provenance tooling,
and all runtime/provider integrations.

If this ADR is accepted, it supersedes the target-product conclusion of
`2026-07-25-runtime-neutral-control-plane.md`. That earlier ADR remains historical
evidence during migration; its runtime-neutral authority principles are retained,
but its control-plane and adapter ownership are not carried into the promoted
kit.

## Rationale

A project kit preserves the framework's demonstrated value where it is durable:
scope control, explicit decisions, bounded authority, role separation, evidence,
and reusable project memory. Removing runtime ownership prevents duplication,
provider drift, and a false expectation that the framework must emulate every
runtime's hooks, agents, plugins, or permission system.

A skills-library-only product was rejected because skills do not supply the
entry contract, source-of-truth hierarchy, Work Blocks, durable memory, review
artifacts, or closeout needed for a complete SDLC.

## Rejected Alternatives

### Continue the runtime-neutral control plane

Rejected. Provider-neutral naming does not remove ownership of capability
negotiation, adapters, runtime profiles, hooks, plugins, MCP, or conformance
state. Those concerns remain runtime/tooling responsibilities.

### Publish only the nine core skills

Rejected. This would discard the practical lifecycle, role authority, memory,
plans, assurance artifacts, and collision-safe project installation.

### Maintain first-class provider adapters inside the kit

Rejected. Adapters inevitably age with provider behavior and encourage duplicate
sources of truth. Users may create local configuration outside the kit.

### Require one fixed multi-agent topology

Rejected. Portability requires artifact-compatible native subagents, sequential
passes, and manual handoffs.

## Consequences

### Positive

- The product can be installed into projects without selecting an AI provider.
- The portable contract stays understandable without hidden runtime state.
- Role authority and evidence remain stable as agent runtimes change.
- The candidate can be tested as a concrete project kit rather than an abstract
  governance layer.
- Optional tooling can evolve independently without becoming a core dependency.

### Tradeoffs

- Runtime enforcement is no longer promised by the core kit.
- Existing control-plane assets require explicit migration and archival.
- Local runtime configuration may vary between users and is not validated by the
  kit.
- Some current features become optional extensions or historical evidence.

## Compatibility

The current repository remains operationally canonical until the six-Work-Block
migration completes. The candidate under
`candidate/portable-agentic-sdlc-kit/` is noncanonical. Promotion requires pilot
evidence and explicit Owner approval.

## Review Triggers

Review this decision when:

- a proposed core feature requires owning provider/runtime configuration;
- the artifact contracts cannot support a major execution mode;
- a proposed extension attempts to redefine authority or source of truth;
- pilot evidence shows the product is incomplete without a currently excluded
  capability.
