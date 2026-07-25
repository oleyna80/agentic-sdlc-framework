# Claude Code Runtime Adapter

## Status

Existing implementation to normalize. The framework already ships Claude Code
agents, hooks, settings, skills, MCP configuration, and per-agent memory under
`template/.claude/`.

## Intended Role Mapping

| Logical role | Claude Code implementation |
|---|---|
| Orchestrator | Main Claude Code session or project orchestrator agent |
| Architect | `solution-architect` or equivalent read-only agent |
| Critic | `critic` agent |
| Coder | `scoped-coder` agent |
| Reviewer | `reviewer` agent |
| Verifier | `verifier` agent |

Provider-named roles such as `gpt-critic`, `gpt-verifier`, and
`codex-reviewer` are integration specializations, not governance-core roles.
They should move to integration mappings during migration.

## Adapter Responsibilities

The normalized adapter should provide:

- mapping from logical roles to `.claude/agents/` definitions;
- hooks that enforce core write, critic, hard-stop, and verification gates;
- skills aligned with portable artifact contracts;
- plugin integration guidance;
- explicit capability and isolation records;
- separate handling of local agent memory and committed engineering memory;
- smoke tests after Claude Code or plugin updates.

## Current Sources

- `template/CLAUDE.md`
- `template/.claude/settings.json`
- `template/.claude/agents/`
- `template/.claude/hooks/`
- `template/.claude/skills/`
- `template/.claude/agent-memory/`

These remain operational while their provider-specific governance language is
migrated into adapter mappings.

## Codex Integration

A Codex plugin, MCP call, or file handoff used from Claude Code is an integration
mechanism. It may supply an independent Critic, Reviewer, or Verifier function,
but it does not create a new authority class and does not make one model family
automatically authoritative.
