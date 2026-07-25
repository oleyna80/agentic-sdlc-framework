# Work Block WB-001 — Runtime-Neutral Control Plane

## Status

- **State:** completed
- **Closeout:** success
- **Branch:** `agent/runtime-neutral-control-plane`
- **Side-effect class:** public repository change
- **Verification tier:** standard
- **Superseded active work by:** `docs/plans/wb-002-normalize-portable-sdlc-contracts.md`

## Objective

Refactor the framework's architectural direction so that the Agentic SDLC core
manages work independently of any specific agent runtime, model provider, or
integration mechanism.

## Expected Final Result

The repository contains a clear runtime-neutral governance core, explicit
runtime adapter boundaries, and an accepted architectural decision that treats
Codex, Claude Code, OpenCode, and future runtimes as interchangeable execution
adapters rather than as authority-bearing parts of the SDLC.

## Delivered

- Accepted architecture decision:
  `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`.
- Added the runtime-neutral control plane under `governance/`.
- Added Codex, Claude Code, OpenCode, and generic adapter boundaries under
  `runtimes/`.
- Separated logical role, runtime, model, specialization, isolation, and tool
  capability.
- Repositioned plugins, MCP, and file handoff as integrations/transports rather
  than governance authority.
- Updated repository overview, navigation, and machine-readable registry.
- Added structural governance validation.

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
scripts/validate-governance.sh
```

## Acceptance Criteria

- [x] The core architecture is explicitly runtime-neutral.
- [x] Logical roles are separated from runtime, model, and isolation level.
- [x] Governance lifecycle functions do not require one process per role.
- [x] Runtime adapters expose capabilities and limitations without changing
      authority rules.
- [x] Existing implementation layers are classified as adapters or legacy
      transports rather than the core SDLC.
- [x] Repository navigation points agents to the new normative documents.
- [x] Existing integrations remain usable during migration.

## Verification Evidence

- GitHub compare confirmed the branch was based on `main` and not behind.
- Governance, runtime, ADR, README, map, and registry paths were inspected.
- `scripts/validate-governance.sh` was added for machine-executed validation.
- Shell execution was moved to the GitHub Actions contract workflow during
  WB-002.

## Closeout

The architectural foundation is complete. Template convergence, generated
project contracts, drift audit, and CI validation continue under WB-002.

## Follow-up Work Blocks

1. WB-002 — Normalize roles, SSOT, lifecycle, review, verification, and drift
   audit across current templates.
2. WB-003 — Add Codex-native agents and executable Codex hooks.
3. WB-004 — Convert Claude Code, Codex plugin, OpenCode, and file handoff into
   explicit runtime/integration adapters.
4. WB-005 — Add profile-aware bootstrap and cross-runtime conformance tests.
