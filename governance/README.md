# Governance Core

This directory contains the runtime-neutral control contract for the Agentic
SDLC Framework.

The governance core answers these questions independently of Codex, Claude Code,
OpenCode, Antigravity, or any future agent runtime:

- What outcome is approved?
- Which artifacts are authoritative?
- Which role may decide, write, review, verify, or approve?
- Which side effects require a hard stop?
- What evidence is required before work advances?
- What happens when a capability, review, or verification step is unavailable?
- When may a Work Block be declared successful?

## Normative Documents

| Document | Purpose |
|---|---|
| `authority.md` | Stable logical roles, authority boundaries, runtime/model/isolation separation |
| `lifecycle.md` | Runtime-neutral lifecycle functions, stage transitions, degraded paths |
| `artifacts.md` | Portable artifact chain, status, versioning, evidence, and SSOT rules |
| `runtime-capabilities.md` | Capability negotiation and topology selection |

## Boundary

Runtime-specific instructions, model names, plugins, hooks, MCP servers, CLI
commands, provider credentials, and transport mechanisms do not belong in this
directory. They belong under `runtimes/`, `integrations/`, user-level runtime
configuration, or project-local private configuration.

## Core Principle

The SDLC manages the work. Agent runtimes execute the contracts.

A runtime may implement several logical roles in one process for low-risk work,
or distribute them across independent agents, sessions, worktrees, or machines
for higher assurance. The selected topology must preserve the authority,
artifact, evidence, and closeout rules defined here.

## Migration Status

The repository still contains compatibility documents written around the
previous Codex → Claude Code topology. During migration:

1. this directory defines the target architecture;
2. existing templates and hooks remain operational;
3. later Work Blocks will remove duplicated or provider-specific core rules only
   after equivalent runtime adapters and validation exist.

See the accepted ADR:
`docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.
