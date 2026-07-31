---
schema_version: 1
artifact_type: architecture_decision
artifact_id: 2026-07-29-portable-kit-product-boundary
status: accepted
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

The portable successor requires an unambiguous product boundary and assurance
model before candidate implementation.

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
- Critic, Reviewer, Verifier, evaluation, and closeout artifacts;
- a generic, collision-safe installation contract.

Artifacts are the portability boundary. The kit must work through native
subagents, sequential single-agent passes, and manual copy-and-paste handoffs.
No execution mode is authoritative by itself.

The kit does not own or require provider-specific agent definitions, model
routing, capability negotiation, hooks, runtime permission configuration, MCP,
plugins, provider snapshots, runtime profiles, queues, daemons, duplicated skill
mirrors, or runtime-specific conformance control planes.

The practical lifecycle is retained:

```text
Work Block
  → discovery / specification / architecture
  → implementation plan and tasks
  → Critic when required
  → scoped implementation
  → Reviewer and Verifier assurance against an exact normative subject
  → Owner-authorized status finalization when applicable
  → final applicable assurance
  → evidence-only reports
  → CI on the resulting PR head
  → SSOT and memory synchronization
  → truthful closeout
  → separate Owner-controlled integration
```

This decision defines the accepted migration **target architecture**, not an
immediate replacement of the current operational repository architecture.
`PROJECT_MAP.md` and `FILE_REGISTRY.yml` distinguish:

1. the runtime-neutral control plane as current operational architecture;
2. WB-CORE-001 as current active migration Work Block while in progress;
3. this ADR, the portable-kit specification, and the companion ADR as accepted
   target architecture that has not been promoted.

WB-CORE-006 owns the atomic promotion and legacy-archive reconciliation that
changes the operational architecture identifier.

### Assurance identity, verdicts, and evidence discovery

Reviewer and Verifier assurance binds to an exact **normative subject**: the
commit or artifact revision containing applicable specification, ADRs, Work
Block, authoritative plans/tasks, normative navigation/registry content,
delivered artifact, and status changes.

Critic, Reviewer, and Verifier verdicts are role-specific:

- Critic: `APPROVE`, `APPROVE_WITH_CHANGES`, `RECONSIDER`, `BLOCKED`;
- Reviewer: `READY`, `CHANGES_REQUIRED`, `BLOCKED`, `UNVERIFIED`;
- Verifier: `READY`, `NOT_READY`, `BLOCKED`, `UNVERIFIED`.

An evidence-only commit changes only approved assurance or closeout report paths.
It may follow the normative subject it evaluates and does not invalidate the
verdict it records. Any applicable normative-subject change invalidates prior
readiness.

Navigation and registry are normative-subject surfaces only for authority,
architecture, canonical paths, active lifecycle state, and accepted/proposed
status. Mutable assurance verdicts, reviewed or verified SHAs, findings,
coverage, limitations, and another-pass state are prohibited from normative
navigation.

Reports require no per-report navigation registration. They are discovered from
canonical directories and structured frontmatter. Adding a report-only commit
does not require a map or registry update and indexing evidence would not grant
authority.

### Acceptance-state transition

Preliminary Reviewer and Verifier assurance returned `READY` against exact
normative subject `9c169fd97bdbe90bb2fc1133fff29878d1373396`. On 2026-07-30,
the Owner explicitly authorized accepted-status finalization only. This
status-only normative commit changes this ADR to `accepted`.

```text
preliminary Reviewer and Verifier assurance
  → Owner authorizes accepted-status finalization
  → status-only normative commit
  → final Reviewer/Verifier assurance against that normative subject as required
  → evidence-only report commit
  → CI on the resulting PR head
  → separate Owner merge approval
```

Final applicable assurance must now evaluate the resulting new normative subject.
The assurance report may be committed afterward and does not need to be contained
in the commit it evaluates. Acceptance does not promote the target into the
current operational architecture, complete WB-CORE-001, or authorize merge.

## Rationale

A project kit preserves scope control, explicit decisions, bounded authority,
role separation, evidence, and reusable memory. Removing runtime ownership
prevents duplication and provider drift. Exact subject identity avoids
self-referential assurance. Keeping mutable assurance state in self-contained
reports prevents each review result from manufacturing a new normative subject.

## Rejected Alternatives

### Continue the runtime-neutral control plane as the target

Rejected. Provider-neutral naming does not remove ownership of adapters,
profiles, hooks, plugins, MCP, or conformance state.

### Publish only the nine core skills

Rejected. Skills alone do not supply the entry contract, source-of-truth
hierarchy, Work Blocks, durable memory, assurance artifacts, or closeout.

### Maintain first-class provider adapters inside the kit

Rejected. Adapters age with provider behavior and encourage duplicate sources of
truth.

### Require one fixed multi-agent topology

Rejected. Portability requires artifact-compatible native subagents, sequential
passes, and manual handoffs.

### Require reports inside the commit they verify

Rejected. That creates a self-referential subject. Reports follow the completed
subject as evidence-only commits.

### Mirror the latest assurance result in normative navigation

Rejected. Each new verdict, reviewed SHA, finding, or limitation would mutate the
normative subject and invalidate the assurance being indexed.

## Consequences

### Positive

- The product is provider-independent.
- Role authority and evidence remain stable as runtimes change.
- Reports can follow the exact subject without changing it.
- Future reviews and verification reports do not require normative navigation
  churn.

### Tradeoffs

- Runtime enforcement is not promised by the core kit.
- Existing control-plane assets require explicit migration and archival.
- Local runtime configuration varies and is unmanaged.
- Consumers discover evidence through canonical directories/frontmatter rather
  than a mutable “current report” pointer.

## Compatibility

The current runtime-neutral control-plane repository remains operationally
canonical until promotion. During WB-CORE-001, navigation registers the active
migration Work Block, accepted but unpromoted target architecture, and static
evidence directory classes only. It does not mirror current assurance results.
Candidate content remains noncanonical. Promotion still requires applicable
pilot evidence, final assurance, closeout, green CI, and explicit Owner approval.

## Review Triggers

Review this decision when:

- a proposed core feature requires provider/runtime ownership;
- artifact contracts cannot support a major execution mode;
- an extension attempts to redefine authority;
- assurance tooling cannot distinguish normative and evidence-only commits;
- normative navigation begins mirroring mutable assurance state;
- pilot evidence shows the product is incomplete without an excluded capability.
