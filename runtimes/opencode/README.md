# OpenCode Runtime Adapter

## Status

Implemented generated-project baseline for project instructions, logical-role
subagents, explicit permissions, and opt-in plugins/MCP.

Target-environment smoke evidence is still required before using OpenCode for a
Managed, Assured, or Distributed Work Block.

## Logical Role Mapping

| Logical role | OpenCode implementation | Default authority |
|---|---|---|
| Orchestrator | main OpenCode session / selected primary agent | workflow coordination |
| Architect | `.opencode/agents/architect.md` | read-only |
| Critic | `.opencode/agents/critic.md` | read-only |
| Coder | `.opencode/agents/coder.md` | permission-prompted approved write-set |
| Reviewer | `.opencode/agents/reviewer.md` | read-only |
| Verifier | `.opencode/agents/verifier.md` | read-only plus approved reports |

The built-in Plan and Build agents may still be used, but the Work Block must
record which logical function they perform and their effective permissions.

## Installed Project Files

```text
opencode.json
.opencode/
└── agents/
    ├── architect.md
    ├── critic.md
    ├── coder.md
    ├── reviewer.md
    └── verifier.md
```

No provider, model, plugin, MCP server, API key, or external directory is enabled
by the framework.

## Project Configuration

`opencode.json`:

- loads `AGENTS.md`, governance, lifecycle, roster, and this adapter as
  instructions;
- explicitly denies common secret paths;
- denies external-directory access;
- requires approval for edits, Bash, web, task delegation, and MCP tools;
- allows only harmless Git inspection commands without approval;
- denies commit, push, destructive Git, and `rm` commands;
- starts with empty `mcp` and `plugin` collections;
- ignores common generated and volatile paths in the file watcher.

OpenCode's runtime permission result is one of `allow`, `ask`, or `deny`.
Project, agent, session, and auto-mode behavior must be considered together.
Explicit `deny` rules must remain effective even when auto approval is enabled.

## Permission Boundary

Permissions are guardrails, not the Work Block authority source.

- `ask` means the runtime requests approval; it does not mean the action is
  approved by governance.
- `allow` means the runtime may execute without prompting; it does not expand
  role or scope.
- `deny` blocks the runtime action and should be used for immutable project
  boundaries such as secrets, external directories, commit, and push.

The generated Coder uses `edit: ask` because the baseline cannot prove the
machine-readable Work Block write-set at the tool interception layer. The human
or orchestrator must compare every proposed edit with the active write-set.

Do not use `--auto` for a state-changing Work Block until the project has
verified every applicable deny rule and recorded the residual risk.

## Subagents

Project agents live in `.opencode/agents/` and use `mode: subagent`.

They omit concrete models so provider and model routing remain private/runtime
configuration. Agent permissions are stricter than or equal to project defaults:

- Architect, Critic, Reviewer, and Verifier deny edits;
- Coder requires approval for edits and denies commit/push/destructive commands;
- nested task delegation is denied for all bundled subagents;
- external-directory access is denied;
- web and MCP capabilities require approval.

The main session may invoke subagents automatically or by explicit mention.
Record the actual child-session IDs or other launch evidence when assurance
independence matters.

## Plugins and MCP

OpenCode supports project plugins and MCP servers, but both collections are empty
in the framework baseline.

Before activation:

1. complete `docs/templates/integration-admission-template.md`;
2. identify exact plugin/MCP tools and permission names;
3. add allow/ask/deny rules for each tool;
4. confirm secret and external-directory boundaries;
5. run safe and denied-action smoke fixtures;
6. record version, provider, model, and capability evidence.

See `integrations/` and `docs/mcp-tool-policy.md`.

## Capability Snapshot

Start with evidence-backed values:

```yaml
runtime: opencode
status: available_unverified
capabilities:
  project_instructions: configured
  project_subagents: configured
  child_sessions: observed_or_unknown
  granular_permissions: configured
  per_agent_permissions: configured
  skills: observed_or_unknown
  mcp: disabled
  plugins: disabled
  websearch: provider_or_environment_dependent
  external_directory_guard: configured
  write_set_hook: unavailable
  worktrees: external_workflow
  os_isolation: false
limitations:
  - runtime permission prompts do not validate the Work Block write-set
  - provider/model availability depends on local configuration
  - plugins and MCP can add tools that need separate permission rules
  - same checkout and machine unless separately isolated
```

Upgrade `observed_or_unknown` only after a target-environment smoke.

## Activation

1. Bootstrap the project.
2. Review `opencode.json` and `.opencode/agents/`.
3. Run OpenCode in the project and initialize only if it will not overwrite the
   approved `AGENTS.md` contract.
4. Confirm the runtime reads the committed `AGENTS.md`.
5. Inspect effective provider/model and permissions.
6. Run one read-only Architect or Reviewer task.
7. Confirm a bundled read-only agent cannot edit.
8. Confirm commit, push, secret reads, and external-directory access are denied.
9. Run a disposable Coder edit inside a test write-set with explicit approval.
10. Record the capability snapshot and limitations.

## Assurance and Isolation

A separate OpenCode child session improves context separation but does not by
itself establish a separate checkout, OS identity, credential store, or provider.
Use separate worktrees, containers, machines, accounts, or human review when the
governance profile requires stronger independence.

## Degraded Mode

When agents or permissions do not behave as documented:

- stop state-changing work;
- label the runtime adapter degraded;
- use Plan/read-only mode or a separate verified runtime;
- preserve the same artifacts and logical functions;
- do not claim a passing assurance gate without evidence.

## Official References

- <https://opencode.ai/docs/>
- <https://opencode.ai/docs/agents/>
- <https://opencode.ai/docs/permissions/>
- <https://opencode.ai/docs/config/>
