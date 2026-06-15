# Handoff Env Contract Work Block Log — 2026-06-15

## Final Outcome

`handoff-runner.sh` can run Claude Code from an explicit project-local env
contract instead of relying on VS Code terminal environment injection. The real
credential file remains ignored and local, the runner logs only whether it was
loaded, and live handoff smoke passes when run as an unrestricted user process.

## Scope

In scope:
- Document DeepSeek Anthropic-compatible provider setup.
- Add `ANTHROPIC_API_KEY` to the handoff env whitelist and examples.
- Load optional local handoff env before launching Claude Code.
- Verify with a non-secret fake CLI smoke and a minimal live Claude Code handoff
  smoke.

Out of scope:
- Committing real provider credentials.
- Changing Claude Code agent model frontmatter away from `model: inherit`.
- LiteLLM routing.
- systemd service installation on this host.

## Execution Log

| Time UTC | Step | Evidence | Status |
|---|---|---|---|
| 2026-06-15T09:10Z | DeepSeek provider setup added to Claude Code KB | Official DeepSeek Anthropic-compatible guide captured with env-contract notes | Complete |
| 2026-06-15T09:18Z | Handoff env whitelist synchronized | `ANTHROPIC_API_KEY` added to `sanitize-env.sh`, README, and env example | Complete |
| 2026-06-15T09:25Z | Local env file checked safely | `handoff/runtime/handoff.env` is ignored and mode `600`; contents were not read | Complete |
| 2026-06-15T09:27Z | Runner env loading implemented | `handoff-runner.sh` loads optional `handoff/runtime/handoff.env`; logs only path and loaded flag | Complete |
| 2026-06-15T09:27Z | Fake CLI env smoke passed | Fake `claude` received `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` through `HANDOFF_ENV_FILE`; runner returned `complete` | Complete |
| 2026-06-15T09:35Z | Sandbox live smoke failed | Runner loaded env file, but Claude Code returned `API Error: Unable to connect to API (ConnectionRefused)` | Expected sandbox boundary |
| 2026-06-15T09:39Z | Escalated live smoke passed | Runner loaded env file, Claude Code created `memory_bank/handoff-live-smoke.txt`, scope audit passed | Complete |

## Verification Evidence

Checks run:
- `bash -n handoff/runner/handoff-runner.sh handoff/runner/sanitize-env.sh`
- `bash scripts/validate-publication.sh`
- `git diff --check`
- Fake CLI env smoke with `HANDOFF_ENV_FILE`
- Live Claude Code handoff smoke outside the sandbox

Live smoke result:
- status: `complete`
- changed paths: `memory_bank/handoff-live-smoke.txt`
- scope audit: `passed`
- violations: `[]`

## Closeout Notes

The previous `ConnectionRefused` failure was not caused by a missing
project-local env file after this fix. The same task failed in sandbox context
and passed as an unrestricted user process. Future live Claude Code handoff
checks should run outside the Codex sandbox, while unit tests can keep using fake
CLI binaries.
