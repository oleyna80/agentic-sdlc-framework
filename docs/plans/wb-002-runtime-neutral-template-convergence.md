# Work Block WB-002 — Runtime-Neutral Template Convergence

## Status

- Stage: Execute
- State: in_progress
- Branch: `agent/runtime-neutral-control-plane`
- Parent decision: `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`

## Objective

Align the generated-project contract with the new runtime-neutral governance core.
The template must describe management functions and evidence contracts without
requiring Codex, Claude Code, OpenCode, a specific model family, or native
subagents.

## In Scope

- shorten and normalize `template/AGENTS.md`;
- replace provider-named core roles with logical roles;
- converge the four-stage lifecycle on Define / Execute / Assure / Close;
- separate Critic, Reviewer, Verifier, and Spec Drift Audit responsibilities;
- place approved specifications above plans and tasklists in the SSOT order;
- add portable runtime capability and isolation fields to Work Blocks;
- add a reusable `spec-drift-audit` skill and report template;
- reframe framework profiles as governance levels plus runtime adapters;
- make generated projects receive the governance core and runtime adapter docs.

## Out of Scope

- executable Codex write-gate hooks;
- Codex custom agent TOML definitions;
- replacement of existing Claude Code hooks and agents;
- deletion of the file-based handoff runtime;
- provider/model benchmarking;
- profile-aware selective bootstrap.

## Write Set

```text
docs/plans/wb-002-runtime-neutral-template-convergence.md
template/AGENTS.md
template/.agent/ROSTER.md
template/.agent/workflows/sdd-protocol.md
template/docs/templates/work-block-template.md
template/docs/templates/spec-drift-report-template.md
docs/profiles.md
skills/spec-drift-audit/SKILL.md
skills/catalog.yml
bootstrap.sh
template/scripts/bootstrap.sh
```

## Acceptance Criteria

- [ ] No provider-named role is required by the generated-project core contract.
- [ ] Standard lifecycle explicitly includes independent review, technical verification, and specification drift audit.
- [ ] Specification authority is higher than implementation plans and tasklists.
- [ ] A Work Block records runtime, capability, model class, and isolation separately.
- [ ] `spec-drift-audit` exists in the skill library and catalog.
- [ ] Bootstrap copies governance and runtime adapter documentation into generated projects.
- [ ] Existing `.codex/`, `.claude/`, and handoff layers remain available as adapters.

## Verification Plan

- inspect all changed Markdown contracts for terminology consistency;
- verify skill catalog coverage conceptually and through existing validation when available;
- verify bootstrap path references;
- compare the branch against `main` through GitHub;
- keep the PR in draft until shell checks run in a normal checkout or CI.

## Follow-up

- WB-003: Codex-native custom agents and executable write/scope gates.
- WB-004: normalize existing Claude Code, plugin, MCP, OpenCode, and handoff integrations against runtime adapters.
- WB-005: profile-aware bootstrap and cross-runtime conformance tests.
