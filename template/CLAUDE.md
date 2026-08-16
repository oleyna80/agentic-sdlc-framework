@AGENTS.md

# Claude Code

This file is the Claude Code runtime entry point for `{{PROJECT_NAME}}`.
`AGENTS.md` is the canonical portable project contract; this file only adds
Claude-specific routing and must not duplicate or override shared governance.

## Runtime-specific guidance

- Runtime adapter and capability notes: `runtimes/claude-code/README.md`.
- Claude settings and hooks: `.claude/settings.json` and `.claude/hooks/`.
- Claude logical-role subagents: `.claude/agents/`.
- Installed Claude skill mirror: `.claude/skills/`; canonical portable skills are
  also indexed under `.agent/skills/`.
- Detailed lifecycle procedure: `.agent/workflows/sdd-protocol.md`.
- Runtime/profile availability evidence: `.agent/bootstrap-profile.json` plus
  current live runtime inspection when capability matters.

Claude-specific permissions, hooks, agents, plugins, MCP tools, and runtime
features implement or constrain the shared contract; they do not create scope,
authority, acceptance, or external Hard Stop exceptions.

Keep this file thin. Put shared project behavior in `AGENTS.md`, reusable
procedures in skills/workflows, and detailed Claude Code mechanics in the runtime
adapter or `.claude/` configuration rather than copying them here.
