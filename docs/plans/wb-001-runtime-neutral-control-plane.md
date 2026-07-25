# Work Block WB-001 — Runtime-Neutral Control Plane

## Status

- **State:** in_progress
- **Branch:** `agent/runtime-neutral-control-plane`
- **Side-effect class:** public repository change
- **Verification tier:** standard

## Objective

Refactor the framework's architectural direction so that the Agentic SDLC core
manages work independently of any specific agent runtime, model provider, or
integration mechanism.

## Expected Final Result

The repository contains a clear runtime-neutral governance core, explicit
runtime adapter boundaries, and an accepted architectural decision that treats
Codex, Claude Code, OpenCode, and future runtimes as interchangeable execution
adapters rather than as authority-bearing parts of the SDLC.

## In Scope

- Record the runtime-neutral control-plane architecture decision.
- Introduce top-level `governance/` and `runtimes/` navigation.
- Define stable logical roles, lifecycle functions, artifacts, and runtime
  capability negotiation.
- Update public repository navigation and positioning.
- Preserve existing Codex, Claude Code, and handoff implementations as current
  adapters pending later migration Work Blocks.

## Out of Scope

- Rewriting every existing skill or hook.
- Removing the current file-based Codex → Claude Code handoff.
- Implementing final Codex custom-agent TOML files.
- Replacing all provider-specific terminology in one change.
- Declaring OpenCode integration production-ready without runtime smoke tests.

## Write Set

```text
docs/plans/wb-001-runtime-neutral-control-plane.md
docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md
governance/**
runtimes/**
README.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

## Acceptance Criteria

- [ ] The core architecture is explicitly runtime-neutral.
- [ ] Logical roles are separated from runtime, model, and isolation level.
- [ ] Governance lifecycle functions do not require one process per role.
- [ ] Runtime adapters expose capabilities and limitations without changing
      authority rules.
- [ ] Existing implementation layers are classified as adapters or legacy
      transports rather than the core SDLC.
- [ ] Repository navigation points agents to the new normative documents.
- [ ] Existing integrations remain usable during migration.

## Verification Plan

- Review all new normative documents for conflicting authority statements.
- Confirm links and paths referenced by `README.md`, `PROJECT_MAP.md`, and
  `FILE_REGISTRY.yml` exist.
- Compare branch to `main` and inspect the complete diff.
- Keep the pull request in draft state until later migration Work Blocks align
  templates, profiles, hooks, and skills with this architecture.

## Follow-up Work Blocks

1. WB-002 — Normalize roles, SSOT, lifecycle, review, verification, and drift
   audit across current templates.
2. WB-003 — Add Codex-native agents and executable Codex hooks.
3. WB-004 — Convert Claude Code, Codex plugin, OpenCode, and file handoff into
   explicit runtime/integration adapters.
4. WB-005 — Add profile-aware bootstrap and cross-runtime conformance tests.
