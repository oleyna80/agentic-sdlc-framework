---
schema_version: 1
artifact_type: specification
artifact_id: repository-graph-provider-contract
status: approved
created_at: 2026-08-11
owner_approval: WB-REPO-GRAPH-001 exact documentation-first scope
---

# Repository Graph Provider Contract

## Purpose

A Repository Graph Provider is an optional, external capability that may derive
a local graph from a project's canonical repository source. This contract is
provider-neutral: it neither selects nor admits a provider.

## Authority Boundary

Provider output and state are local, derived, rebuildable, and
non-authoritative. They are not published by default. They cannot grant
authority, a write-set, an approval, an assurance verdict, or a canonical or
durable-memory effect, and they cannot be the sole basis for a change.

Important findings require direct confirmation against canonical repository
source before they affect a specification, decision, implementation, review, or
verification result.

## State Binding

When a project separately elects to use a provider, its local record must bind:

- canonical repository root and revision;
- selected provider and version;
- local state location; and
- creation/refresh status.

Refresh or rebuild the state after material repository changes or integration.
Stale, missing, or unbound state is not evidence of current repository behavior.

## Opt-In and Hard Stops

This contract does not install, configure, invoke, start, index, query, or
admit a provider. It does not enable MCP, APIs, hooks, runtime configuration,
embeddings, uploads, credentials, or keys. A future project invocation or
admission requires a separately Owner-approved Work Block with its data,
credential, local-state, and assurance boundaries.

Provider-local state must be excluded locally before indexing. Use
`.git/info/exclude` or an operator-managed global exclusion; do not add a
generic graph directory or committed ignore rule for this optional state.
