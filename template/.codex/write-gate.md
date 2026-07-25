# Codex Write Gate — Compatibility View

> Human-readable compatibility note. The executable source of truth is
> `.agent/active-work-block.json`.

## Default State

- **Status:** BLOCKED
- **Active Work Block:** unset
- **Specification:** unset
- **Base commit:** unset
- **Expiry:** unset
- **Critic:** PENDING
- **Approved write-set:** empty

The generated project starts fail-closed.

## Executable Gate

Codex `PreToolUse` reads `.agent/active-work-block.json` and checks:

- schema version;
- Work Block ID;
- specification path and revision;
- `write_gate.status`;
- timezone-aware expiry;
- current `HEAD` against `base_commit`;
- required Critic status and verdict;
- source targets against the approved write-set;
- Hard Stop approval flags for supported Bash operations.

Do not set this Markdown file to READY. Updating it alone does not authorize a
write.

## Coordination Before READY

While the source gate remains BLOCKED, the hook permits only the configured
coordination write-set, normally:

```text
.agent/active-work-block.json
.agent/critic-gate.md
.agent/verification-gate.md
.codex/write-gate.md
docs/architecture/drafts/**
docs/specs/**
docs/plans/**
docs/tasklist/**
docs/reports/**
memory_bank/**
```

These paths allow Define-stage and evidence work. They do not authorize source,
configuration, runtime, infrastructure, credential, or data mutations.

## Opening the Source Gate

Populate the machine-readable gate only after:

1. the human Work Block is approved;
2. the active specification and revision are recorded;
3. the architecture baseline and implementation plan are resolved;
4. the source write-set is explicit;
5. the required Critic function completed or an allowed degraded/skip state is
   documented;
6. `base_commit` matches the current Git `HEAD`;
7. `expires_at` is short-lived and timezone-aware;
8. relevant Hard Stop approvals are recorded.

Then set:

```json
"write_gate": {
  "status": "READY",
  "opened_at": "2026-07-25T12:00:00+02:00",
  "expires_at": "2026-07-25T18:00:00+02:00"
}
```

After a commit changes `HEAD`, renew the gate before further source writes.

## Limitations

Hooks are project guardrails, not OS-level isolation. Project hooks must be
reviewed and trusted in Codex. Live parent permission overrides can affect
subagents. Stronger assurance may require a separate read-only root, worktree,
runtime, container, or OS boundary.
