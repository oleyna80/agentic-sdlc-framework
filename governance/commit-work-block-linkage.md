# Commit ↔ Work Block linkage

Generated projects may opt into the cooperative project-local hook
`template/.githooks/commit-msg` with:

```bash
./scripts/bootstrap.sh --install-git-hooks
./scripts/bootstrap.sh --check-git-hooks
```

The hook reads `.agent/active-work-block.json` as structured schema-v3 JSON.
Linkage is active only when `work_block_id` is a non-empty string and
`closeout_mode` is `pending`. A pending Work Block remains linkage-active when
its `write_gate` is `BLOCKED`; write authority and traceability are separate.
Retained `success-closeout` and `reporting-only` records, and the empty default
ID, are inactive.

While active, a commit must contain exactly one canonical Git trailer:

```text
Work-Block: <exact-current_work_block_id>
```

The key is strict and the value is compared exactly. Missing, empty, duplicate,
mismatched, malformed, unsupported, or contradictory state fails closed with an
actionable message. No framework-specific Work Block ID grammar is introduced;
the lifecycle state's exact ID is authoritative.

Bootstrap without flags remains a health check and does not change Git config.
Install writes only repository-local `core.hooksPath=.githooks`; check is
read-only. Global and system Git configuration are not modified.

This is a cooperative local guard, not a security boundary. `--no-verify`,
GitHub/API-created commits, remote merges, and commits made outside an installed
local hook are outside its guaranteed enforcement. GitHub protections, external
capabilities, runtime checks, write-set controls, and Owner authority remain the
actual authority boundaries.
