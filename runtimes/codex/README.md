# Codex Runtime Adapter

## Status

Migration target. The repository currently contains Codex policy and routing
material under `template/.codex/` and `framework/workflow/`. Later Work Blocks
will normalize those files against the governance core.

## Intended Role Mapping

| Logical role | Codex implementation |
|---|---|
| Orchestrator | Main Codex thread / control tower |
| Architect | Read-only custom agent or delegated subagent |
| Critic | Read-only custom agent with strong reasoning profile |
| Coder | Workspace-write custom agent limited to approved write set |
| Reviewer | Read-only custom agent reviewing a frozen diff |
| Verifier | Read-only custom agent plus approved evidence output path |

The mapping is configurable. Model selection does not change authority.

## Adapter Responsibilities

The completed adapter should provide:

- project-scoped custom agent examples under `.codex/agents/`;
- safe public configuration templates without credentials;
- executable pre-tool write and scope gates where supported;
- effective-model and fallback recording;
- read-only Reviewer and Verifier profiles;
- a Coder profile with explicit write-set instructions;
- capability smoke tests;
- compatibility guidance for Codex plugins and MCP integrations;
- honest degraded behavior when subagents, models, or hooks are unavailable.

## Target Capability Record

Capabilities must remain `unknown` or `conditional` until verified in the target
environment.

```yaml
runtime: codex
capabilities:
  native_subagents: conditional
  custom_agent_profiles: conditional
  separate_readonly_context: conditional
  workspace_write_sandbox: conditional
  hooks_or_policy_interception: conditional
  skills: conditional
  mcp: conditional
  parallel_read: conditional
  parallel_write: conditional
  worktrees: conditional
  structured_tool_output: conditional
```

## Migration Sources

- `template/.codex/config.toml.template`
- `template/.codex/critic.md`
- `template/.codex/write-gate.md`
- `framework/workflow/codex-model-routing.md`
- `skills/codex-verification/`

These files remain active compatibility sources until the adapter is completed
and templates are migrated.
