# Work Block WB-002 — Runtime-Neutral Template Convergence

## Status

- **Stage:** Assure
- **State:** in_progress
- **Branch:** `agent/runtime-neutral-control-plane`
- **Governance profile:** Managed
- **Side-effect class:** public repository change
- **Verification tier:** standard
- **Parent decision:** `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`

## Objective

Align the generated-project contract with the runtime-neutral governance core.
The scaffold must describe management functions, authority, artifacts, and
evidence without requiring Codex, Claude Code, OpenCode, a specific model family,
or native subagents.

## Expected Final Result

A newly bootstrapped project contains:

- the portable governance core and runtime adapter documentation;
- a concise runtime-neutral `AGENTS.md`;
- a Define / Execute / Assure / Close lifecycle;
- distinct Critic, Reviewer, Verifier, and Specification Drift functions;
- specification-first SSOT rules;
- Work Blocks that record governance, runtime, model class, capability, and
  isolation separately;
- structural contract tests that reject provider-authoritative core terminology.

## Normative Inputs

- `governance/authority.md`
- `governance/lifecycle.md`
- `governance/artifacts.md`
- `governance/runtime-capabilities.md`
- `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`

## In Scope

- shorten and normalize `template/AGENTS.md`;
- replace provider-named core roles with logical roles;
- converge the lifecycle on Define / Execute / Assure / Close;
- separate Critic, Reviewer, Verifier, and Specification Drift responsibilities;
- place approved specifications above plans and tasklists in the SSOT;
- add portable runtime capability and isolation fields to Work Blocks;
- add the reusable `spec-drift-audit` skill and report template;
- reframe framework profiles as governance levels plus runtime/integration
  adapters;
- copy governance and runtime adapter documentation into generated projects;
- normalize generated-project navigation, registry, and session bootstrap;
- update structural SDLC contract checks.

## Out of Scope

- executable Codex write/scope hooks;
- final Codex custom-agent TOML definitions;
- replacement or removal of existing Claude Code hooks and agents;
- deletion of the file-based handoff runtime;
- provider/model benchmarking;
- profile-aware selective bootstrap;
- claiming cross-runtime conformance before smoke tests.

## Write Set

```text
docs/plans/wb-001-runtime-neutral-control-plane.md
docs/plans/wb-002-runtime-neutral-template-convergence.md
docs/profiles.md
template/AGENTS.md
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
template/.agent/ROSTER.md
template/.agent/workflows/sdd-protocol.md
template/docs/session-bootstrap.md
template/docs/templates/work-block-template.md
template/docs/templates/spec-drift-report-template.md
skills/spec-drift-audit/SKILL.md
skills/catalog.yml
bootstrap.sh
template/scripts/bootstrap.sh
scripts/test-sdd-contract.sh
PROJECT_MAP.md
FILE_REGISTRY.yml
```

## Acceptance Criteria

- [x] No provider-named role is required by the generated-project core contract.
- [x] Core logical roles are Owner, Orchestrator, Architect, Critic, Coder,
      Reviewer, and Verifier.
- [x] Standard lifecycle explicitly includes independent review, technical
      verification, and specification drift audit.
- [x] Specification authority is higher than implementation plans and tasklists.
- [x] A Work Block records governance, runtime, capability, model class, and
      isolation separately.
- [x] `spec-drift-audit` exists in the skill library and catalog.
- [x] Bootstrap copies governance and runtime adapter documentation into generated
      projects.
- [x] Generated-project map, registry, and session bootstrap use progressive,
      runtime-neutral navigation.
- [x] Existing `.codex/`, `.claude/`, MCP, plugin, and handoff layers remain
      available as adapters.
- [ ] Structural and publication checks pass in a normal checkout or CI.
- [ ] The complete PR diff receives final review and verification.

## Assurance Plan

### Review

Inspect:

- role/runtime/model separation;
- duplicated or conflicting SSOT statements;
- distinction between Review, Verification, and Drift Audit;
- bootstrap path correctness;
- compatibility with existing runtime adapters and hooks;
- provider-specific language remaining in portable core files.

### Verification

Run in a normal checkout:

```bash
bash scripts/validate-governance.sh
bash scripts/test-sdd-contract.sh
bash scripts/validate-publication.sh
```

Also bootstrap a disposable project and confirm required paths:

```bash
./bootstrap.sh /tmp/agentic-sdlc-wb002-smoke "WB002 Smoke" wb002-smoke
```

### Drift Audit

Compare the accepted ADR and governance core against generated project contracts,
bootstrap behavior, profiles, skill catalog, and navigation.

## Current Limitation

The GitHub connector can inspect and change repository content but does not
provide a local checkout for executing shell validation. The PR remains draft
until the commands above run in a normal checkout or CI environment.

## Follow-up

- WB-003 — Codex-native custom agents and executable write/scope gates.
- WB-004 — normalize Claude Code plugins, MCP, OpenCode, and file handoff as
  explicit integrations/adapters.
- WB-005 — profile-aware bootstrap and cross-runtime conformance tests.
