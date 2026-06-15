# Knowledge Base

Operational knowledge for running the Agentic SDLC framework with external
agent teams, CLI tools, plugins, hooks, MCP servers, and repeatable handoff
patterns.

## Index

| Topic | File | Use |
|---|---|---|
| Claude Code CLI | `claude-code-cli.md` | Treat Claude Code as an external delivery team: CLI modes, settings, subagents, hooks, plugins, observability, and safety notes. |
| Claude Code global bootstrap | `claude-code-global-bootstrap.md` | User-level setup for provider env, global agents, portable hooks, and project-local gate boundaries. |

## Update Rules

- Prefer official vendor documentation for tool behavior.
- Add third-party workflows only with source URL, date checked, and framework
  implication.
- Keep private project names, credentials, hostnames, and client details out of
  this directory.
- Record assumptions as assumptions, not verified facts.
- When behavior affects automation or safety, note the exact command, flag, or
  config surface involved.

## Suggested Future Entries

- `claude-code-hooks.md` — project hook patterns and failure handling.
- `claude-code-subagents.md` — recommended team topology and memory strategy.
- `claude-code-plugins.md` — approved plugins, review checklist, and version log.
- `codex-claude-handoff.md` — tested orchestration patterns between Codex and
  Claude Code.
