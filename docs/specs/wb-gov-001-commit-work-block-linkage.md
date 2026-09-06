---
schema_version: 1
artifact_type: specification
artifact_id: wb-gov-001-commit-work-block-linkage
work_block_id: WB-GOV-001
status: approved
revision: owner-approved-pr51-correction-r2-2026-09-06
governance_profile: Managed
base_revision: be988807c38543eb90a728fcb4349bc97dd5695a
---

# WB-GOV-001 — Runtime-neutral commit ↔ Work Block linkage

## Objective and boundary

Add a cooperative, runtime-neutral project-local Git trailer contract to the
generated framework scaffold. It improves traceability and ordinary local
commit discipline; it is not a security boundary and does not replace GitHub
protections, write-set enforcement, runtime capability checks, Owner authority,
or external Hard Stops.

The change is prospective and does not redesign schema v3, add branch binding,
add authority modes, or consume WB-CORE-004 through WB-CORE-007.

## Requirements

- REQ-001: The hook parses `.agent/active-work-block.json` as structured JSON,
  requires schema version 3, and uses its exact non-empty `work_block_id` as the
  only linkage authority.
- REQ-002: Linkage is active exactly when `work_block_id` is a non-empty string
  and `closeout_mode` is `pending`; terminal retained records are inactive.
- REQ-003: A pending Work Block remains linkage-active when `write_gate` is
  `BLOCKED`; write authority and linkage are separate concepts.
- REQ-004: Commits intended to participate in an active Work Block are expected
  by governance to carry exactly one canonical `Work-Block` Git trailer whose
  value equals the state ID exactly. The installed `commit-msg` hook enforces this
  for hook-invoking commit flows by rejecting missing, empty, duplicate, or unequal
  trailers.
- REQ-005: Invalid or contradictory active state fails closed with actionable
  output. The hook uses no Work Block ID regex and does not infer from prose,
  branch names, or gate markdown.
- REQ-006: Inactive default, success-closeout, and reporting-only states allow
  ordinary commits without a trailer.
- REQ-007: `template/.githooks/commit-msg` is executable, runtime-neutral, and
  included in every generated installation profile.
- REQ-008: Bootstrap remains backward-compatible by default and only explicit
  `--install-git-hooks` may set repository-local `core.hooksPath` to `.githooks`.
  `--check-git-hooks` is strictly read-only, validating hooks and returning
  immediately without modifying Git configuration or writing operational files;
  global/system Git configuration is untouched.
- REQ-009: Real disposable repository fixtures prove ordinary missing-trailer
  rejection, exact-trailer acceptance, `--check-git-hooks` read-only invariance,
  and document known cooperative enforcement limitations (including `--no-verify`,
  `git cherry-pick`, `git revert`, and uninstalled hooks).
- REQ-010: Existing profiles, bootstrap generation, and framework CI run the
  new contract without making any runtime adapter the authority for it.
- REQ-011: Documentation has one normative linkage contract and referential
  installation guidance; it distinguishes traceability from security authority.
- REQ-012: The implementation remains within the approved framework paths and
  leaves the reserved Portable Kit roadmap untouched.

## Acceptance criteria

- AC-001 [req=REQ-001]: malformed/unsupported/non-object state is rejected and
  valid state is interpreted from structured JSON only.
- AC-002 [req=REQ-002]: empty, success-closeout, and reporting-only records allow
  a no-trailer commit; pending non-empty records require linkage.
- AC-003 [req=REQ-003]: pending plus BLOCKED write gate still requires linkage.
- AC-004 [req=REQ-004]: for hook-invoking commit flows, missing, mismatched,
  empty, and duplicate trailers fail; one exact canonical trailer passes.
- AC-005 [req=REQ-005]: no framework-specific WB-ID grammar is introduced and
  invalid state errors identify the corrective action.
- AC-006 [req=REQ-006]: default and retained terminal compatibility is tested.
- AC-007 [req=REQ-007]: generated core and runtime-specific profiles contain an
  executable `.githooks/commit-msg`.
- AC-008 [req=REQ-008]: default bootstrap leaves hooksPath unchanged, install
  changes only local hooksPath, and check is strictly read-only without operational
  file or config mutation while detecting configured/unconfigured state.
- AC-009 [req=REQ-009]: actual hook enforcement rejects an ordinary missing-trailer
  commit, accepts an exact-trailer commit, allows `--no-verify` bypass, and tests
  observed behavior for commit-producing commands like `git cherry-pick` and
  `git revert` as documented cooperative limitations in a disposable repository.
- AC-010 [req=REQ-010]: existing bootstrap/profile/runtime contracts remain green.
- AC-011 [req=REQ-011]: normative and referential docs agree on active state,
  trailer, installation, and cooperative limitations.
- AC-012 [req=REQ-012]: application/runtime provider surfaces and reserved roadmap
  paths are unchanged.
- AC-013 [req=REQ-008]: hook activation never writes global or system config.
- AC-014 [req=REQ-004]: canonical key handling is strict and tested.
- AC-015 [req=REQ-010]: Framework Contracts CI executes the fixture suite.
- AC-016 [req=REQ-005]: schema-v3 authority/assurance fields are not expanded.
- AC-017 [req=REQ-010]: publication/release-state validation passes.
- AC-018 [req=REQ-012]: WB-CORE-004 through WB-CORE-007 remain future and unused.

## Non-goals

No `subject_branch`, date-slug regex, automatic resubmission-like behavior,
universal Git commit interception, remote commit enforcement, security-boundary
claim, default hook activation, schema-v3 redesign, or protected/default branch
operation.
