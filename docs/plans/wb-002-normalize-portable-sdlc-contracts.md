# Work Block WB-002 — Normalize Portable SDLC Contracts

## Status

- **State:** in_progress
- **Branch:** `agent/runtime-neutral-control-plane`
- **Governance profile:** managed
- **Side-effect class:** public repository change
- **Verification tier:** standard

## Objective

Migrate the generated-project operating contracts to the accepted runtime-neutral
control-plane architecture so that Codex, Claude Code, OpenCode, and generic
agents can execute the same documented lifecycle and produce compatible
artifacts.

## Expected Final Result

A generated project receives the portable governance core, a concise
runtime-neutral `AGENTS.md`, a lifecycle with explicit Critic, Reviewer,
Verifier, and specification-drift functions, governance profiles independent of
runtime selection, and templates that record runtime capability and isolation
without making provider-named agents authoritative.

## Normative Inputs

- `governance/authority.md`
- `governance/lifecycle.md`
- `governance/artifacts.md`
- `governance/runtime-capabilities.md`
- `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`

## In Scope

- Normalize `template/AGENTS.md` and the canonical generated-project lifecycle.
- Replace provider-named core roles with stable logical roles.
- Put specification above plan and tasklist in the generated-project SSOT.
- Separate post-implementation Review from Verification.
- Add specification-drift audit and report contracts.
- Replace runtime-named framework profiles with governance profiles plus runtime
  adapter selection.
- Copy the governance core into generated projects under `.agent/governance/`.
- Update generated-project navigation, registry, session bootstrap, and contract
  tests.

## Out of Scope

- Implementing final Codex `.codex/agents/*.toml` profiles and executable Codex
  hooks.
- Removing Claude Code agents, hooks, or current dual-model integrations.
- Moving all existing integrations to a final `integrations/` directory.
- Profile-aware selective bootstrap installation.
- Declaring cross-runtime conformance until runtime smoke tests exist.

## Write Set

```text
docs/plans/wb-001-runtime-neutral-control-plane.md
docs/plans/wb-002-normalize-portable-sdlc-contracts.md
docs/profiles.md
template/AGENTS.md
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
template/.agent/ROSTER.md
template/.agent/workflows/sdd-protocol.md
template/docs/session-bootstrap.md
template/docs/templates/work-block-template.md
template/docs/templates/spec-drift-report-template.md
skills/spec-drift-audit/**
skills/catalog.yml
bootstrap.sh
template/scripts/bootstrap.sh
scripts/test-sdd-contract.sh
PROJECT_MAP.md
FILE_REGISTRY.yml
```

## Acceptance Criteria

- [ ] Generated projects contain `.agent/governance/` copied from one framework
      source.
- [ ] Core roles are Owner, Orchestrator, Architect, Critic, Coder, Reviewer,
      and Verifier.
- [ ] Runtime, model class, specialization, isolation, and tool availability are
      recorded separately from role authority.
- [ ] Specification and acceptance criteria outrank implementation plans and
      tasklists.
- [ ] Review, Verification, and Drift Audit have distinct inputs, outputs, and
      verdicts.
- [ ] Governance profile and runtime adapter are selected independently.
- [ ] A generic sequential agent can follow the contract without native
      subagents or provider-specific commands.
- [ ] Existing Claude Code and Codex compatibility layers remain available.
- [ ] Contract tests detect reintroduction of provider-specific core authority or
      collapsed Review/Verification semantics.

## Verification Plan

- Inspect all changed authority-bearing files against `governance/`.
- Validate new paths through generated-project bootstrap requirements.
- Run `scripts/test-sdd-contract.sh` in a normal checkout.
- Run `scripts/validate-governance.sh` and
  `scripts/validate-publication.sh` in a normal checkout.
- Compare the PR branch against `main` and inspect all changed files.

## Follow-up

- WB-003 — Codex-native custom agents and executable gates.
- WB-004 — Integration adapters for Claude Code plugins, MCP, OpenCode, and file
  handoff.
- WB-005 — Profile-aware bootstrap and cross-runtime conformance tests.
