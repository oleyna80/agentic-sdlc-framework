# Runtime Adapters

Runtime adapters explain how a specific agent system implements the normative
contracts in `governance/`.

An adapter may define:

- native agent and subagent configuration;
- runtime-specific skills, commands, plugins, hooks, or MCP integrations;
- capability and limitation maps;
- model-routing examples without credentials;
- sandbox and isolation mechanisms;
- smoke tests;
- mappings from logical roles to runtime profiles;
- integration and handoff options.

An adapter may not:

- redefine core authority;
- weaken hard stops;
- silently change artifact verdict semantics;
- treat a model or provider as inherently authoritative;
- represent an unavailable check as passed;
- grant write access because a tool exists.

## Current Adapters

| Adapter | Status | Purpose |
|---|---|---|
| `codex/` | migration target | Native Codex agents, hooks, skills, MCP, model routing |
| `claude-code/` | existing implementation to normalize | Claude Code agents, hooks, skills, plugins, memory |
| `opencode/` | experimental | OpenCode agent/provider integration after smoke testing |
| `generic/` | baseline | Sequential or manually coordinated agents with no native orchestration assumptions |

## Integration vs Runtime

A runtime is the environment executing a logical role. An integration is the
transport or supported bridge between runtimes.

Examples:

- Claude Code is a runtime.
- Codex is a runtime.
- An official Codex plugin for Claude Code is an integration.
- MCP is an integration mechanism.
- `handoff/` is an audited file transport.

Integration documentation will be moved under a dedicated `integrations/`
boundary in a later Work Block. Existing paths remain supported during
migration.
