---
schema_version: 1
artifact_type: architecture_decision
artifact_id: 2026-08-11-repository-graph-provider-boundary
status: accepted
created_at: 2026-08-11
---

# ADR — Optional Repository Graph Provider Boundary

## Context

Repository graph tools can provide useful derived navigation and analysis, but
their generated local state and external-provider behavior must not become a
shadow authority system.

## Decision

The framework declares only an optional, provider-neutral Repository Graph
Provider capability. It owns no provider installation, configuration, process,
index, query, MCP/API surface, hook, runtime configuration, embedding, upload,
credential, or key.

Graph output/state is local, derived, rebuildable, non-authoritative, and not
published by default. It cannot grant authority, a write-set, approval,
assurance verdict, or canonical/durable-memory effect, and cannot be the sole
basis for a change. Material findings require direct canonical repository-source
confirmation.

If a future project separately admits one, its operator records canonical root
and revision, provider/version, local state location, and creation/refresh
status. The state is refreshed or rebuilt after material changes or integration.
The provider state is locally excluded before indexing using `.git/info/exclude`
or a global exclusion, never a committed generic graph ignore rule.

## Consequences

This boundary preserves optional local analysis without treating it as an
integration adapter or portable authority. A future invocation/admission remains
separately Owner-approved and must document its data, secret, side-effect, and
assurance constraints.
