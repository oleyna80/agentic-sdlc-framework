---
schema_version: 1
artifact_type: work_block
artifact_id: wb-004-integration-adapter-normalization
status: in_progress
owner_role: orchestrator
work_block_id: wb-004
created_at: 2026-07-25
last_verified: 2026-07-25
---

# WB-004 — Integration Adapter Normalization

## Objective

Normalize Claude Code plugins, MCP, OpenCode, and file-based handoff as explicit
runtime or integration adapters that implement the Governance Core without
creating provider-specific authority.

## Expected Final Result

- Claude Code exposes only logical-role agents in its default runtime profile.
- The official Codex plugin for Claude Code is documented as the preferred
  Codex-from-Claude integration.
- Codex MCP remains an optional compatibility integration and is disabled by
  default in generated projects.
- OpenCode receives a project-scoped, fail-safe baseline with logical-role
  subagents and explicit permissions.
- File handoff is runtime-neutral and uses a portable task/result envelope.
- Integration admission, capability, authority, trust, secret, and evidence
  requirements are machine-testable.
- Generated projects receive the normalized adapters without credentials or
  automatically enabled external integrations.

## Scope

### In Scope

- `integrations/**`
- `runtimes/claude-code/**`
- `runtimes/opencode/**`
- `docs/mcp-tool-policy.md`
- `handoff/README.md`
- `handoff/templates/**`
- `template/.claude/**`
- `template/.mcp.json`
- `template/.opencode/**`
- `template/opencode.json`
- bootstrap, navigation, registry, and validation changes required to deliver
  and verify these contracts

### Out of Scope

- production credentials or provider endpoints;
- automatic installation of Claude Code, Codex, OpenCode, plugins, or MCP
  servers;
- live cross-runtime smoke tests requiring paid accounts;
- removal of compatibility shims before migration evidence exists;
- profile-aware minimal installation, reserved for WB-005.

## Normative Baseline

- `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`
- `governance/authority.md`
- `governance/lifecycle.md`
- `governance/artifacts.md`
- `governance/runtime-capabilities.md`
- `docs/mcp-tool-policy.md`

## Design Decisions

1. **Runtime adapters execute roles; integrations connect runtimes or tools.**
2. **No external integration is enabled by default.** Generated projects may
   ship reviewed examples, but activation is an explicit Owner action.
3. **Native or official integration precedes generic transport.** Preferred
   order for Claude Code to Codex is official plugin, reviewed MCP, file
   handoff, then manual/sequential exchange.
4. **Provider-named agents are compatibility specializations.** They cannot
   appear as authority roles in portable lifecycle contracts.
5. **Permissions fail safe.** OpenCode project defaults deny external-directory
   access, deny direct edit for read-only roles, and require approval for Bash
   and consequential actions.
6. **Handoff is direction-neutral.** Task envelopes use logical functions,
   runtime identifiers, authority, scope, and evidence contracts rather than a
   hard-coded Codex-to-Claude topology.
7. **Capabilities require evidence.** Runtime or integration features remain
   `unknown` or `experimental` until a target-environment smoke is recorded.

## Implementation Tasks

1. Add `integrations/` entry point and adapters for:
   - official Claude Code Codex plugin;
   - MCP;
   - file handoff.
2. Replace the Claude Code adapter placeholder with an operational mapping,
   activation policy, capability snapshot, and degraded-mode rules.
3. Replace the OpenCode experimental placeholder with:
   - `template/opencode.json` safe defaults;
   - project agents under `template/.opencode/agents/`;
   - capability and activation guidance.
4. Disable Codex MCP and provider-named external agents in the generated-project
   default Claude Code settings.
5. Convert `.mcp.json` into an empty opt-in registry and document reviewed
   examples outside the active config.
6. Generalize handoff documentation and add a portable runtime task envelope.
7. Add contract and generated-project tests for integration boundaries.
8. Update `README.md`, `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, bootstrap, and
   publication validation.
9. Open a draft PR and run final review before merge.

## Assurance Plan

### Review

Check:

- no provider-specific authority remains in portable contracts;
- no integration is activated by default;
- OpenCode permissions match logical role authority;
- plugin, MCP, and file handoff are clearly differentiated;
- compatibility paths are labelled and bounded;
- bootstrap and registries match delivered files.

### Verification

Run through GitHub Actions:

```bash
bash scripts/test-sdd-contract.sh
bash scripts/test-integration-contracts.sh
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

Also bootstrap a disposable project and parse:

- `.claude/settings.json`;
- `.mcp.json`;
- `opencode.json`;
- OpenCode agent frontmatter;
- integration adapter documentation and task envelope.

## Risks

| Risk | Mitigation |
|---|---|
| Runtime config syntax changes | Use current official documentation and parse fixtures |
| Compatibility break for old Codex MCP users | Keep an explicit opt-in compatibility adapter and migration instructions |
| Permissions appear stronger than runtime guarantees | Record hooks/permissions as guardrails, not OS isolation |
| Handoff runner remains Claude-specific internally | Normalize public envelope first; retain runner implementation as a compatibility transport |
| Large migration obscures defects | Separate contract tests, generated-project smoke, and final review report |

## Current State

- **Stage:** Define
- **Stage State:** in_progress
- **Write Gate:** READY for this branch and documented scope
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
