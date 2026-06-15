# Codex Stage 0 Write Gate

Status: BLOCKED
Expires: 2099-12-31
Work Block: TBD
Approved Scope: TBD
Codex Critic: REQUIRED
Critic Verdict: N/A
Critic Report: N/A
Critic Skip Reason: N/A
Orchestrator Response: N/A
Orchestrator Log: memory_bank/orchestrator-log.md
Review Log: memory_bank/review-log.md

Codex must not modify repository files until the Owner-approved scope for the
current workblock is recorded here or in the active conversation.

Set `Status: READY` only after Stage 0 preflight is complete and the approved
scope is clear.

For non-trivial Work Blocks, also set `Codex Critic` before writes:

- `READY` when a read-only Codex critic subagent or external critic completed.
- `FALLBACK` when a same-session critic pass completed because native subagents
  were unavailable.
- `SKIPPED` only for valid skip conditions in `.codex/critic.md` or explicit
  Owner approval.
- `REQUIRED` means the critic requirement is not resolved yet and writes must
  remain blocked.

When `Codex Critic` is `READY` or `FALLBACK`, set `Critic Verdict` to
`APPROVE`, `SUPPLEMENT`, or `RECONSIDER`. When `Codex Critic` is `SKIPPED`,
write a concrete `Critic Skip Reason`.

If `Critic Verdict` is `SUPPLEMENT` or `RECONSIDER`, set a concrete
`Orchestrator Response` before marking `Status: READY`. For `RECONSIDER`, the
response must explain that Stage 0 was rerun or why the Owner explicitly
accepted proceeding.
