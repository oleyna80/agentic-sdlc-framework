# OpenCode Runtime Knowledge Base

> Working notes for evaluating OpenCode as an optional agent runtime next to
> Codex and Claude Code.

Last verified: 2026-06-26

## Purpose

OpenCode is a separate agent runtime with a TUI, CLI commands, configurable
agents, subagents, permissions, providers, plugins, and server/web modes. It is
interesting for this framework as an experimental execution lane, not as a
replacement for the existing control model.

Default framework position:

```text
Codex
  Control Tower, planning, risk decisions, critic review, acceptance.

Claude Code
  Independent external delivery team with its own orchestrator, hooks,
  subagents, skills, logs, and provider environment.

OpenCode
  Optional alternative coding runtime and model-routing lab. Keep experimental
  until installation, auth, permissions, headless runs, and audit artifacts are
  verified on a real project.
```

## Primary Sources

Refresh these before changing automation or security assumptions:

| Topic | Source |
|---|---|
| CLI and headless commands | https://opencode.ai/docs/cli/ |
| Agents and subagents | https://opencode.ai/docs/agents/ |
| Project repository | https://github.com/anomalyco/opencode |

## What Was Verified

Official CLI documentation says:

- `opencode` without arguments starts the TUI.
- `opencode run "..."` runs a prompt programmatically.
- `opencode agent create` can create custom agents.
- `opencode agent create` supports non-interactive creation when `--path`,
  `--description`, `--mode`, and `--permissions` are all provided.
- Agent creation supports `--model` in `provider/model` format.
- Agent permissions can limit capabilities such as `bash`, `read`, `edit`,
  `glob`, `grep`, `webfetch`, `task`, `todowrite`, `websearch`, `lsp`, and
  `skill`.
- Global environment/config surfaces include `OPENCODE_CONFIG`,
  `OPENCODE_CONFIG_DIR`, `OPENCODE_PERMISSION`, default-plugin disable flags,
  Claude Code compatibility disable flags, and experimental model/subagent
  flags.

Local install and CLI check on 2026-06-26:

```bash
command -v opencode
# pre-install: not installed
# post-install: $HOME/.nvm/versions/node/v22.22.3/bin/opencode

node --version
# v22.22.3

npm --version
# 10.9.8

npm i -g opencode-ai@latest
# added 3 packages

opencode --version
# 1.17.11
```

Useful `opencode run` flags from the installed CLI:

| Flag | Use |
|---|---|
| `--model provider/model` | Select a provider/model for one run. |
| `--agent` | Select the agent profile for one run. |
| `--format json` | Emit raw JSON events. |
| `--file` | Attach one or more files to the prompt. |
| `--dir` | Set the run directory, including remote-server runs. |
| `--variant` | Provider-specific reasoning effort, such as `high`, `max`, or `minimal`. |
| `--thinking` | Show thinking blocks; do not enable for framework handoff artifacts unless policy explicitly allows it. |
| `--dangerously-skip-permissions` | Auto-approve non-denied permissions; avoid outside isolated spikes. |

## Framework Fit

Use OpenCode only behind an explicit Work Block until it has enough evidence.

Good candidate uses:

- read-only discovery with a constrained agent;
- isolated implementation spike in a temporary project;
- comparison against Claude Code for the same bounded task;
- model/provider routing experiments;
- independent reviewer when Codex should not be the only reviewer.

Do not use OpenCode yet for:

- production deploys;
- database or migration work;
- secrets/env handling;
- payment/order/checkout changes;
- autonomous changes in a primary project without scope audit;
- replacing the Codex critic or Claude Code team gate.

## Relationship To Codex

Codex remains the authority-bearing orchestrator in this framework. OpenCode can
be a worker runtime only after a Work Block defines:

- task objective;
- allowed and forbidden paths;
- required model/provider;
- permission profile;
- expected result file;
- audit/log output;
- verification command;
- rollback or quarantine behavior.

Do not give OpenCode direct authority to approve its own changes. Acceptance
belongs to Codex Orchestrator and, when triggered, Codex Critic.

## Relationship To Claude Code

Claude Code remains the better-tested external team runtime in this framework:
it already has documented handoff, runner, hooks, scope audit, process logs, and
team-role conventions.

OpenCode may become useful where:

- its provider routing is easier for a given model;
- its permission model is simpler for a bounded task;
- it offers a stronger read-only reviewer or scout workflow;
- a project wants an alternative executor without changing the Codex control
  plane.

Avoid mixing `.claude/` assumptions into OpenCode spikes unless the spike
explicitly tests compatibility. If OpenCode auto-loads Claude Code prompts,
skills, or defaults, document whether that behavior should be enabled or
disabled for the task.

## Suggested Spike Contract

Work Block: `OpenCode Runtime Spike`

Final result:

- OpenCode installed locally and `opencode --version` recorded
  (`1.17.11` on 2026-06-26).
- `opencode --help` and `opencode run --help` captured.
- Headless behavior checked with a no-risk prompt, or explicitly marked blocked
  by missing provider/auth.
- A read-only custom agent is created in a temporary project.
- Permissions are verified before any write-capable task.
- Findings are recorded in this knowledge base or a dated research note.

Suggested temporary project:

```text
$PROJECTS_ROOT/opencode-runtime-spike
```

Suggested read-only agent shape:

```bash
opencode agent create \
  --path .opencode/agents \
  --description "Read-only reviewer for SDLC/runtime experiments" \
  --mode subagent \
  --permissions read,glob,grep \
  --model provider/model
```

Use a placeholder model in committed examples. Real provider names, API keys,
and auth files belong in user-level runtime configuration, not the base
framework.

## Installation Notes

Preferred local experiment path:

```bash
npm i -g opencode-ai@latest
opencode --version
opencode --help
opencode run --help
```

This is a machine-level developer tool installation. It must be approved before
running because it downloads packages and writes outside the repository.

If provider authentication is missing, stop after CLI verification and document
the blocked live-model test. Do not add API keys to this framework repository.

## Decision

OpenCode is `PROMISING / EXPERIMENTAL`.

It is worth installing and testing, but not yet worth adding to the default
generated project template or handoff runner. The first integration should be a
separate spike and a reference doc, not a new mandatory framework layer.
