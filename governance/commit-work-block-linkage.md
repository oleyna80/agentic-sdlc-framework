# Commit ↔ Work Block linkage

The framework source stores the cooperative project-local hook at
`template/.githooks/commit-msg`. After bootstrap, a generated project's hook is
at `.githooks/commit-msg` and can be enabled with:

```bash
./scripts/bootstrap.sh --install-git-hooks
./scripts/bootstrap.sh --check-git-hooks
```

## Governance requirement and hook guarantee

1. **Governance requirement:** Commits intended to participate in an active
   Work Block are expected to carry exactly one canonical Git trailer:

```text
Work-Block: <exact-current_work_block_id>
```

2. **Local hook guarantee:** When an active pending Work Block exists in
   `.agent/active-work-block.json`, an installed `.githooks/commit-msg` rejects
   hook-invoking commit flows whose message does not contain exactly one correct
   trailer matching `work_block_id`.

3. **Lifecycle state interpretation:** The hook reads `.agent/active-work-block.json`
   as structured schema-v3 JSON. Linkage is active only when `work_block_id` is a
   non-empty string and `closeout_mode` is `pending`. A pending Work Block remains
   linkage-active when its `write_gate` is `BLOCKED`; write authority and
   traceability are separate. Retained `success-closeout` and `reporting-only`
   records, and the empty default ID, are inactive.

4. **Strict key and exact value:** The key is strict (`Work-Block`) and the value
   is compared exactly. Missing, empty, duplicate, mismatched, malformed,
   unsupported, or contradictory state fails closed with an actionable message.
   No framework-specific Work Block ID grammar is introduced; the lifecycle state's
   exact ID is authoritative.

## Bootstrap operations

- Bootstrap without flags remains a health check and does not change Git config.
- Explicit `--install-git-hooks` writes only repository-local `core.hooksPath=.githooks`.
- `--check-git-hooks` is strictly read-only: it validates hook presence, executable
  mode, and repository-local `core.hooksPath == .githooks`, then exits immediately
  without mutating Git configuration or creating/rewriting operational files.
- Global and system Git configuration are never modified.

## Known enforcement boundaries and non-guaranteed paths

This is a cooperative local governance guard, not an operating-system or server-side
security boundary. Known commit-producing paths outside the guaranteed enforcement
of this project-local `commit-msg` hook include:

- `git commit --no-verify` (cooperative bypass);
- `git cherry-pick` when Git does not invoke the `commit-msg` hook;
- `git revert` when Git does not invoke the `commit-msg` hook;
- GitHub Web / API / merge-button created commits;
- remote merges and upstream commits;
- local commits made when the hook is not installed or `core.hooksPath` is unconfigured.

GitHub protections, branch rulesets, external capabilities, runtime checks,
write-set controls, and Owner authority remain the actual authority boundaries.
