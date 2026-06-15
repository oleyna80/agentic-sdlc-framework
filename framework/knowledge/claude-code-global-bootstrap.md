# Claude Code Global Bootstrap

> User-level setup pattern for making Claude Code usable across projects while
> keeping project gates project-local.

Last verified: 2026-06-15

## Purpose

Use this when one workstation should run Claude Code from any project with the
same provider environment, shared agents, and shared safety hooks.

This is an operator setup, not a publishable project artifact. Keep real
provider credentials in user-owned ignored files only.

## Recommended User Layout

```text
~/.config/claude-code/env      # provider environment, mode 600
~/.claude/settings.json        # user-level Claude Code settings
~/.claude/agents/              # global subagent definitions
~/.claude/agent-memory/        # global starter memory per agent
~/.claude/hooks/               # global hook scripts
~/.claude/skills/              # optional global CC skills
```

Do not store real keys in a repository, `.claude/settings.json`,
`.claude/settings.local.json`, or task files.

## Provider Env

Create a private user env file:

```bash
mkdir -p "$HOME/.config/claude-code"
install -m 600 /dev/null "$HOME/.config/claude-code/env"
```

Add provider variables locally. Example variable names for a
DeepSeek-backed Anthropic-compatible runtime:

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_API_KEY="<local-key>"
export ANTHROPIC_AUTH_TOKEN="<local-key>"
export ANTHROPIC_MODEL="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
```

Load this file before the interactive guard in `~/.bashrc`, so both interactive
and non-interactive Claude Code launches inherit it:

```bash
# Claude Code CLI settings
if [ -f "$HOME/.config/claude-code/env" ]; then
  . "$HOME/.config/claude-code/env"
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac
```

If a systemd user service launches Claude Code, do not assume it reads
`~/.bashrc`. Point the service or runner at the same file with an explicit
environment file or `HANDOFF_ENV_FILE`.

## Install Global CC Team Assets

Copy only the public Claude Code runtime layer from the framework template:

```bash
src="/path/to/agentic-sdlc-framework/template/.claude"
dst="$HOME/.claude"

mkdir -p "$dst"
cp -r "$src/agents" "$dst/"
cp -r "$src/agent-memory" "$dst/"
cp -r "$src/hooks" "$dst/"
cp -r "$src/skills" "$dst/"
cp "$src/settings.json" "$dst/settings.json"
chmod +x "$dst/hooks"/*.sh
```

Do not copy `settings.local.json.example` as active settings. Do not overwrite
existing `~/.claude/CLAUDE.md`, `~/.claude/.mcp.json`, or provider env files
unless the owner explicitly approves the merge.

When replacing existing files, create timestamped backups first.

## Portable Global Hooks

Project template hooks use project-relative commands such as:

```json
"command": "bash .claude/hooks/critic-gate.sh"
```

That is correct for project-local `.claude/settings.json`, but wrong for
user-level `~/.claude/settings.json` because Claude Code may be launched from
any directory.

For global settings, use absolute hook paths:

```json
"command": "bash /home/<user>/.claude/hooks/hard-stop.sh"
"command": "bash /home/<user>/.claude/hooks/critic-gate.sh"
"command": "bash /home/<user>/.claude/hooks/typecheck.sh"
"command": "bash /home/<user>/.claude/hooks/verification-gate.sh"
```

Only universal hooks should always enforce globally. The hard-stop hook is safe
as a global guard because it blocks dangerous shell intent and does not require
project files.

Project gates must no-op outside Agentic SDLC projects:

```bash
# critic-gate.sh
[ -f ".agent/critic-gate.md" ] || exit 0

# verification-gate.sh
[ -f ".agent/verification-gate.md" ] || exit 0
```

Inside a project with gate files, the same hooks enforce the Work Block and
verification contracts.

## Project-Local Runtime Remains Canonical

The global install is a convenience for using Claude Code from any directory.
It does not replace the project-local runtime layer.

Generated Agentic SDLC projects should still contain their own:

```text
.claude/settings.json
.claude/hooks/
.claude/agents/
.claude/agent-memory/
.agent/
memory_bank/
docs/
```

Project-local gates are stricter and should remain project-relative. They are
the canonical contract for a repository. The global setup makes manual CC use
and cross-project bootstrap smoother.

## Checks

Verify without printing secret values:

```bash
bash -n "$HOME/.bashrc"
bash -n "$HOME/.claude/hooks"/*.sh
jq empty "$HOME/.claude/settings.json"

bash -ic 'test -n "$ANTHROPIC_AUTH_TOKEN" && echo ANTHROPIC_AUTH_TOKEN=present'
bash -ic 'test -n "$ANTHROPIC_API_KEY" && echo ANTHROPIC_API_KEY=present'
claude --version
```

Check hook behavior outside a project:

```bash
tmp=$(mktemp -d)
cd "$tmp"
printf '{"tool_name":"Write","tool_input":{"file_path":"test.txt"}}' \
  | bash "$HOME/.claude/hooks/critic-gate.sh"
bash "$HOME/.claude/hooks/verification-gate.sh"
```

Expected result: both project gates exit `0` with no output.

Check hook behavior inside an Agentic SDLC project by running a controlled test
with `.agent/critic-gate.md` and `.agent/verification-gate.md` present.
Expected result: gates enforce the project contract instead of silently
exiting.

## Failure Patterns

| Symptom | Likely cause | Fix |
|---|---|---|
| Claude Code works in one terminal but not another | Provider env comes from an editor extension or old shell file | Load one user env file from `~/.bashrc` and restart the terminal |
| `ANTHROPIC_API_KEY` is missing but other variables exist | Old env file is still sourced | Source `~/.config/claude-code/env` instead of legacy provider files |
| Hook says `.claude/hooks/...` not found | User-level settings use project-relative hook paths | Use absolute paths in `~/.claude/settings.json` |
| CC blocks in `/home` or another non-project folder | Project gates run globally without no-op markers | Add `.agent/*-gate.md` existence checks before enforcing |
| systemd runner misses credentials | systemd does not read `~/.bashrc` | Use explicit `EnvironmentFile` or `HANDOFF_ENV_FILE` |

## Safety Notes

- Never print or paste real API keys into chat, logs, reports, or commits.
- Keep `~/.config/claude-code/env` mode `600`.
- Keep global settings portable, but keep repository governance project-local.
- Do not make global hooks depend on one repository path unless the hook is
  explicitly intended only for that workstation.
