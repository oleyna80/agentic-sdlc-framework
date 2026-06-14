# Claude Code CLI Knowledge Base

> Working notes for treating Claude Code as an independent external delivery
> team inside the Agentic SDLC framework.

Last verified: 2026-06-14

## Purpose

Claude Code is not just another model endpoint. It is an agentic coding product
with its own CLI, configuration hierarchy, memory, subagents, hooks, plugins,
MCP connections, background sessions, and permission model.

In this framework, Codex remains the Control Tower. Claude Code is treated as an
external delivery team: it receives a scoped mission, runs its own internal
process, returns evidence, and writes a summary-level delivery log when asked.

## Primary Sources

Refresh these before changing automation or security assumptions:

| Topic | Source |
|---|---|
| Product overview and surfaces | https://code.claude.com/docs/en/overview |
| CLI commands and flags | https://code.claude.com/docs/en/cli-reference |
| Settings, scopes, permissions | https://code.claude.com/docs/en/settings |
| Subagents and agent teams | https://code.claude.com/docs/en/sub-agents |
| Hooks lifecycle and event schemas | https://code.claude.com/docs/en/hooks |
| OpenAI Codex plugin for Claude Code | https://github.com/openai/codex-plugin-cc |

## Mental Model

Claude Code has several control planes:

| Layer | What it controls | Framework implication |
|---|---|---|
| CLI invocation | Session mode, prompt, output format, budget, turns, tools | Runner owns process launch and timeout |
| Settings | User/project/local/managed defaults | Project settings can shape the external team |
| CLAUDE.md | Standing project instructions | Use for stable team policy, not per-task detail |
| Subagents | Specialized roles with own context, tools, permissions, memory | CC can operate as a team with lead/reviewer/coder roles |
| Hooks | Lifecycle automation and gates | Use for audit, policy, formatting, review gates |
| MCP | External tools and data sources | Scope carefully; MCP can expand blast radius |
| Plugins | Packaged commands, agents, hooks, integrations | Treat as third-party extensions with review gates |

## Headless Operation

Use print mode for non-interactive handoff:

```bash
claude -p "review this change"
cat task.md | claude -p
```

Important flags for orchestration:

| Flag | Use |
|---|---|
| `-p`, `--print` | Run without interactive UI and exit after the response |
| `--output-format json` | Machine-readable final output |
| `--output-format stream-json --verbose` | Event stream for detailed observability |
| `--input-format stream-json` | Programmatic multi-message input |
| `--json-schema` | Constrain final output shape |
| `--max-budget-usd` | Bound API spend for a handoff task |
| `--max-turns` | Bound agentic turn count |
| `--no-session-persistence` | Avoid saving resumable local sessions for runner jobs |
| `--name` | Make runner-created sessions identifiable |
| `--permission-mode` | Start in `plan`, `auto`, `dontAsk`, or `bypassPermissions` |
| `--tools` / `--disallowedTools` | Restrict tool surface for a run |
| `--settings` | Inject a task-specific settings file |
| `--mcp-config` / `--strict-mcp-config` | Control MCP server availability |
| `--plugin-dir` / `--plugin-url` | Load plugins for one session |
| `--worktree` | Ask Claude Code to use an isolated git worktree |

Current runner default:

```bash
claude \
  --dangerously-skip-permissions \
  --no-session-persistence \
  --max-budget-usd "$HANDOFF_CLAUDE_MAX_BUDGET_USD" \
  --name "handoff-$TASK_ID" \
  -p \
  -- "$PROMPT"
```

This is viable only because the framework adds outer controls: isolated
`project_root`, private `TMPDIR`, timeout, scope audit, runtime guard, and
ignored append-only logs. For normal manual use, prefer narrower permission
modes and explicit tool restrictions.

## Configuration Scopes

Claude Code configuration is layered:

| Scope | Typical location | Use |
|---|---|---|
| Managed | System/enterprise policy | Organization-wide non-overridable policy |
| Command line | CLI flags | One run or one handoff task |
| Local | `.claude/settings.local.json` | Personal project overrides; usually gitignored |
| Project | `.claude/settings.json` | Team-shared permissions, hooks, MCP, plugins |
| User | `~/.claude/` | Personal defaults and authentication |

Framework rule:

- Put stable team policy in project files.
- Put secrets and personal auth in user/local scope.
- Put per-task constraints in the handoff task and CLI flags.
- Do not rely on user-level state for publishable framework behavior.

## Current Model Strategy

Template agents use `model: inherit`. This is intentional: the active Claude
Code runtime/provider configuration owns model selection today, including
DeepSeek-backed setups.

Do not hard-code per-agent Claude model names in the framework template until a
LiteLLM-based routing layer has been tested end-to-end. When LiteLLM is added,
document the routing policy, fallback behavior, cost limits, and failure modes
before changing agent frontmatter.

## Claude Team Contract

For delegated state-changing work, the handoff task should tell Claude Code:

1. Act as an external delivery team with its own internal process.
2. Stay inside `allowed_scope` and respect `forbidden_scope`.
3. Do not expose private chain-of-thought.
4. Write summary-level traceability to `memory_bank/external-team-log.md`.
5. Return status, actions, files changed, checks, risks, and next step.

Use:

```text
handoff/templates/claude-team-task-template.md
```

## Subagents And Agent Teams

Claude Code subagents are Markdown-defined specialists with custom prompts,
tool access, permission modes, optional skills, optional MCP servers, and
optional persistent memory.

Useful patterns:

| Pattern | When to use |
|---|---|
| Lead + implementer + reviewer | Larger delegated feature work |
| Read-only reviewer | Release review, security review, drift review |
| Tool-scoped specialist | Browser tests, DB read-only checks, API docs lookup |
| Memory-enabled specialist | Repeated work in the same codebase |
| Worktree-isolated agent | Parallel implementation with lower merge conflict risk |

Control Tower should not micromanage these roles. It should constrain scope,
observe artifacts, and adjust future team policy when the outputs show process
problems.

## Hooks

Hooks run at Claude Code lifecycle events. They can observe, add context, or
return decisions depending on the event.

High-value events for this framework:

| Event | Use |
|---|---|
| `SessionStart` / `SessionEnd` | Session audit and setup/cleanup |
| `PreToolUse` | Block risky shell/MCP operations before execution |
| `PostToolUse` | Record tool usage or trigger formatting/lint checks |
| `Stop` | Final response gate; require delivery log or review result |
| `StopFailure` | Capture API/auth/billing/rate-limit failures |
| `SubagentStart` / `SubagentStop` | Observe internal team topology |
| `TaskCreated` / `TaskCompleted` | Track CC internal task lifecycle |
| `FileChanged` | React to specific files such as `.env` or lockfiles |

Hook output is event-specific. `PreToolUse` uses
`hookSpecificOutput.permissionDecision`, while `Stop` blocks continuation with
top-level `decision: "block"` plus `reason`.

Recommended first hook ideas:

- Stop hook that blocks closeout unless `external-team-log.md` was updated for
  state-changing handoff tasks.
- PreToolUse hook that denies destructive shell commands outside the approved
  project root.
- PostToolUse hook that records summary tool events to an ignored debug log.

Do not use hooks as the only safety layer. Keep runner-level timeout, scope
audit, and runtime guard.

## Plugins And External Extensions

Plugins can add slash commands, subagents, hooks, and integrations. Treat them
as code dependencies:

1. Prefer known source repositories.
2. Record version/source/date in this KB.
3. Review plugin commands, hooks, and transitive dependencies before enabling
   them in project scope.
4. Keep powerful plugins disabled by default unless the work block needs them.
5. Avoid passing secrets through plugin commands unless explicitly required and
   reviewed.

### OpenAI Codex Plugin For Claude Code

Source: https://github.com/openai/codex-plugin-cc

Purpose:

- Use Codex from inside Claude Code.
- Run read-only Codex review from CC.
- Run adversarial review.
- Delegate background work to Codex and manage status/result/cancel.

Notable commands:

| Command | Purpose |
|---|---|
| `/codex:setup` | Check Codex installation/authentication and optional review gate |
| `/codex:review` | Read-only Codex review of current work or branch diff |
| `/codex:adversarial-review` | Steerable challenge review for assumptions and tradeoffs |
| `/codex:rescue` | Delegate investigation or fixes to Codex |
| `/codex:status` | Check background Codex jobs |
| `/codex:result` | Read final stored Codex output |
| `/codex:cancel` | Cancel active background Codex work |

Framework usage:

- Good fit for CC self-review or adversarial review before returning to Codex.
- Do not enable an automatic review gate by default; long Claude/Codex loops can
  drain budget and obscure ownership.
- Prefer explicit task contract: "run `/codex:review` before closeout and
  include the finding summary".

## Observability

Runner-level observability:

- `handoff/logs/session-*.log`: process metadata, Claude stdout/stderr, guard
  status, scope audit, exit code.
- `handoff/runtime/status.json`: mutable machine-readable runner status.
- `handoff/done/*-result.md` or `handoff/failed/*-result.md`: compact result.

Project-level observability:

- `memory_bank/external-team-log.md`: external team execution trace.
- `memory_bank/review-log.md`: Control Tower consolidation of reviewer outputs.
- `memory_bank/orchestrator-log.md`: Control Tower decisions and rationale.

The session log answers "what happened at the process boundary". The external
team log answers "how did the delegated team execute the mission".

## Safety Notes

- `--dangerously-skip-permissions` is a process convenience, not a safety
  model. Use it only inside an outer guard such as handoff-runner.
- `auto` and permission modes are not a replacement for explicit scope control.
- MCP and plugins can expand capabilities beyond file edits and shell commands.
- Persistent memory is useful but can accumulate stale or sensitive context.
- Claude Code can run its own subagents; the handoff result should report the
  team topology at summary level.
- Never ask for private chain-of-thought. Ask for decisions, evidence, risks,
  and rejected alternatives at summary level.

## Knowledge Base Update Policy

Add new entries when:

- Anthropic changes CLI flags, settings, hooks, subagents, plugins, or MCP
  behavior.
- A third-party team publishes a useful Claude Code extension or workflow.
- A handoff run exposes a new failure mode or useful operating pattern.
- We change runner defaults that depend on Claude Code behavior.

Each update should include:

- source URL
- date checked
- short summary
- framework implication
- risk or follow-up
