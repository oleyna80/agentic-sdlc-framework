# Live Handoff Smoke Work Block Log - 2026-06-15

## Expected Final Result

A freshly bootstrapped framework project can be used as a real Claude Code
handoff target:

- Codex writes a task file to `handoff/queue/`.
- `handoff/runner/handoff-runner.sh` launches Claude Code.
- The task moves through the handoff lifecycle and finishes in `handoff/done/`.
- A runner result file and session log are created.
- Claude Code writes the requested smoke output and external-team log entry.
- Scope audit passes, including the Claude Code team's own audit trail files.
- `handoff/runtime/handoff.env` contents are not read or printed during this
  Work Block, and the smoke project has no forbidden secret-like artifact paths
  after the run.

## Scope

In scope:
- Bootstrap a clean smoke project under `/tmp`.
- Run a live Claude Code handoff through the runner.
- Verify result file, session log, status file, smoke output, external-team log,
  and scope audit.
- Capture publication-safe evidence in this report.

Out of scope:
- Committing ignored handoff runtime artifacts.
- Reading or printing `handoff/runtime/handoff.env` contents or other
  credential values.
- Changing runner architecture.
- Installing systemd service or watcher.
- Using project-specific application repositories.

## Execution Log

| Time UTC | Step | Evidence | Status |
|---|---|---|---|
| 2026-06-15T18:26Z | Clean smoke project bootstrapped | `/tmp/agentic-sdlc-live-handoff-20260615T182616Z`; bootstrap verification passed | Complete |
| 2026-06-15T18:31Z | First live run inside Codex sandbox failed | `API Error: Unable to connect to API (ConnectionRefused)` | Expected sandbox boundary |
| 2026-06-15T18:36Z | Second live run outside sandbox reached Claude Code but failed scope audit | Claude changed CC audit files outside the narrow two-file allowlist | Useful finding |
| 2026-06-15T18:37Z | Fresh smoke project bootstrapped | `/tmp/agentic-sdlc-live-handoff-20260615T183749Z`; bootstrap verification passed | Complete |
| 2026-06-15T18:41Z | Third live run passed with CC audit trail in scope | `status=complete`, `exit_code=0`, result in `handoff/done/` | Complete |

## Live Run Result

Final task:

- task id: `20260615T183749Z-live-handoff-smoke`
- project root: `/tmp/agentic-sdlc-live-handoff-20260615T183749Z`
- result: `handoff/done/20260615T183749Z-live-handoff-smoke-result.md`
- log: `handoff/logs/session-20260615T183749Z-live-handoff-smoke-20260615T183827Z-767204.log`
- status file: `/tmp/agentic-sdlc-live-handoff-status-20260615T183749Z.json`

Final status:

```text
status=complete
exit_code=0
```

Scope audit:

```text
status=passed
reason=changed-files-within-scope
changed_paths=[
  .agent/critic-gate.md,
  .agent/verification-gate.md,
  memory_bank/external-team-log.md,
  memory_bank/handoff-smoke.txt,
  memory_bank/orchestrator-log.md
]
violations=[]
```

Smoke output:

```text
handoff smoke ok
```

Forbidden artifact check returned no matching files for:

- `.env`
- `.env.*`
- `secrets/**`
- `*.pem`
- `*.key`

Credential handling note: the runner reported only whether its ignored
project-local env file was loaded. This Work Block did not read or print
`handoff/runtime/handoff.env` contents or credential values.

## Findings

Live Claude Code handoff should be run outside the restricted Codex sandbox.
When run inside the sandbox, Claude Code can start but may fail model API access
with `ConnectionRefused`.

The handoff scope for Claude Code tasks must account for the CC team's own
process audit trail. For even a trivial quick-fix, Claude Code may update:

- `.agent/critic-gate.md`
- `.agent/verification-gate.md`
- `memory_bank/orchestrator-log.md`
- `memory_bank/external-team-log.md`

For tasks where those files are expected, they should be explicitly listed in
`allowed_scope`. This keeps scope enforcement strict without breaking the
independent-team model.

Generated projects intentionally ignore `.agent/` and `memory_bank/` in git by
default. For handoff verification, runner filesystem snapshots are the right
source of truth; `git status` alone is insufficient for ignored workflow
artifacts.

## Verification

Passed:

- `bash -n handoff/runner/handoff-runner.sh handoff/runner/sanitize-env.sh handoff/runner/cleanup.sh handoff/runner/watch-queue.sh scripts/test-handoff-scope-audit.sh scripts/validate-publication.sh`
- `scripts/test-handoff-scope-audit.sh`
- `bash scripts/validate-publication.sh`
- `git diff --check`
- result file exists and is non-empty
- session log exists and is non-empty
- status file reports `complete`
- lifecycle check shows final task and result only in `handoff/done/`
- smoke file content equals `handoff smoke ok`
- external-team log contains the live task id and `complete` status
- `handoff/runtime/handoff.env` contents and credential values were not read or
  printed during verification
- forbidden artifact name check found no `.env`, `.env.*`, `secrets/**`,
  `*.pem`, or `*.key` files in the smoke project

## Risks And Follow-Up

The runner stores live handoff artifacts under ignored directories. That is the
right default for logs and runtime details, but publication evidence needs a
curated report like this file.

Future task templates should document that Claude Code's audit files may need
to be included in `allowed_scope` when CC is expected to operate as an
independent team rather than a single-file patch tool.

This lesson is encoded as the reusable `handoff-live-smoke` skill so future live
smoke Work Blocks start from the correct sandbox, scope, and evidence rules.

## Outcome

Live Handoff Smoke passed. The Codex-to-Claude Code handoff layer is usable for
real delegated tasks when run as an unrestricted user process with an explicit
scope that includes expected CC audit trail files.
