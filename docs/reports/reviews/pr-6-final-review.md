---
schema_version: 1
artifact_type: review_report
artifact_id: pr-6-final-review
work_block_id: wb-006
reviewed_revision: e7b2622003c17736c7c4214dff2e99b4879e1212
review_date: 2026-07-26
verdict: READY
reviewer_role: reviewer
---

# PR #6 Final Review - Bootstrap Restore Hardening

## Scope

Reviewed WB-006 changes for the two unresolved P2 Codex review findings from
merged PR #5 and the follow-up P1 Codex review finding on PR #6:

- required installation-profile paths must validate expected filesystem kinds;
- `.agent/active-work-block.default.json` must validate as a safe blocked
  default before restoring ignored active Work Block state;
- authorization-bearing `coordination_write_set` must exactly match the
  canonical ordered safe paths before restore.

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

### F-03 - Blocked default accepted expanded coordination authority

**Severity:** P1
**Status:** Resolved

The generated validator did not inspect `coordination_write_set`. A corrupted
tracked default could therefore add `**` or another broad source pattern and
restore it into active state while `write_gate.status` remained `BLOCKED`.
Codex and Claude coordination checks trust this field, so the corruption could
bypass the source-write gate.

**Resolution:**

- generated validator now contains the canonical ordered blocked-default
  coordination paths as its independent expected value;
- restore requires exact list equality, including path order;
- missing, additional, reordered, malformed, and non-string entries fail;
- repository roots, POSIX and Windows absolute paths, traversal paths, and
  unauthorized wildcard patterns fail before exact-list comparison;
- only the canonical narrow documentation and coordination patterns remain
  valid;
- regression fixtures deny `**`, `src/**`, `.`, `/tmp/source.py`,
  `../source.py`, missing entries, additions, reordering, non-string values,
  and malformed values;
- the successful restore fixture confirms the unchanged canonical list is
  copied into active state.

## Additional Review Notes

- The test harness now uses `sys.executable` for Python subprocesses and a
  configurable `BASH`, improving local Windows verification without changing
  Ubuntu CI semantics.
- Documentation and navigation were updated in framework and generated-project
  maps/registries.
- The follow-up P1 changes only generated-project validation and restore
  fixtures; runtime coordination matching behavior itself is unchanged.
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
| 321 | push | success |
| 322 | pull_request | success |

## Drift Audit

| Contract | Result |
|---|---|
| Installation profile remains composition evidence only | ALIGNED |
| Required paths validate expected filesystem kind | ALIGNED |
| Blocked default validates before active state restore | ALIGNED |
| Restore remains idempotent and preserves existing active state | ALIGNED |
| Default Work Block remains approval-free and empty-write-set | ALIGNED |
| Coordination authority exactly matches the canonical ordered safe paths | ALIGNED |
| Broad glob, root, source, absolute, and traversal corruption fails closed | ALIGNED |
| Framework and generated-project navigation reflect new checks | ALIGNED |

**Drift verdict:** `READY` / `ALIGNED`.

## Closeout

- **Review verdict:** `READY`
- **Verification verdict:** `READY`
- **Drift verdict:** `READY / ALIGNED`
- **Closeout mode:** `success-closeout`
- **Residual risk:** live runtime smoke tests remain outside WB-006 scope; this
  PR hardens generated-project bootstrap contracts only. Canonical narrow
  documentation globs remain intentional coordination authority and are
  protected by exact-list validation.

## Final Verdict

`READY`

PR #6 remains Ready for review and must not be merged without explicit Owner
approval.
