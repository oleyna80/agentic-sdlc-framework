---
schema_version: 1
artifact_type: review_report
artifact_id: pr-6-final-review
work_block_id: wb-006
reviewed_revision: 2b34e5cfa743c9973f431758b775b93e2021172f
review_date: 2026-07-26
verdict: READY
reviewer_role: reviewer
---

# PR #6 Final Review - Bootstrap Restore Hardening

## Scope

Reviewed WB-006 changes for the two unresolved P2 Codex review findings from
merged PR #5:

- required installation-profile paths must validate expected filesystem kinds;
- `.agent/active-work-block.default.json` must validate as a safe blocked
  default before restoring ignored active Work Block state.

## Review Findings

No unresolved blocking findings remain.

### F-01 - Required files could be satisfied by directories

**Severity:** P2  
**Status:** Resolved

`scripts/validate-installation-profile.py` previously used `.exists()` for
required paths. A directory named `AGENTS.md` could satisfy the check even though
agents could not read the operating contract as a file.

**Resolution:**

- generated `.agent/bootstrap-profile.json` now records `required_path_kinds`;
- generated validator checks required paths with `.is_file()` or `.is_dir()`;
- missing legacy kind metadata falls back to file expectations for compatibility;
- regression fixture replaces `AGENTS.md` with a directory and expects failure.

### F-02 - Blocked default Work Block was blindly restored

**Severity:** P2  
**Status:** Resolved

After clone, ignored `.agent/active-work-block.json` could be restored by
copying the tracked default without proving that the default was still blocked
and approval-free.

**Resolution:**

- generated validator parses `.agent/active-work-block.default.json`;
- validator requires schema version 1, `write_gate.status == BLOCKED`, no
  approval window, empty `integrations.approved`, empty
  `integrations.admission_records`, empty `write_set`, and all Hard Stop
  approvals set to `false`;
- `scripts/bootstrap.sh` validates this before restoring local active state;
- regression fixture corrupts the default to `READY` with write scope,
  integration approval, and push approval, then verifies restore is denied and
  active state is not created.

## Additional Review Notes

- The test harness now uses `sys.executable` for Python subprocesses and a
  configurable `BASH`, improving local Windows verification without changing
  Ubuntu CI semantics.
- Documentation and navigation were updated in framework and generated-project
  maps/registries.
- No installation profile composition, governance authority, runtime adapter
  behavior, integration admission, or live smoke behavior changed.

## Verification Evidence

Local verification passed:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-bootstrap-profiles.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
git diff --check
```

GitHub Actions Framework Contracts:

| Run | Event | Result |
|---|---|---|
| 317 | push | success |
| 318 | pull_request | success |

## Drift Audit

| Contract | Result |
|---|---|
| Installation profile remains composition evidence only | ALIGNED |
| Required paths validate expected filesystem kind | ALIGNED |
| Blocked default validates before active state restore | ALIGNED |
| Restore remains idempotent and preserves existing active state | ALIGNED |
| Default Work Block remains approval-free and empty-write-set | ALIGNED |
| Framework and generated-project navigation reflect new checks | ALIGNED |

**Drift verdict:** `READY` / `ALIGNED`.

## Closeout

- **Review verdict:** `READY`
- **Verification verdict:** `READY`
- **Drift verdict:** `READY / ALIGNED`
- **Closeout mode:** `success-closeout`
- **Residual risk:** live runtime smoke tests remain outside WB-006 scope; this
  PR hardens generated-project bootstrap contracts only.

## Final Verdict

`READY`

PR #6 may be moved from Draft to Ready for review after this closeout commit
passes Framework Contracts.
