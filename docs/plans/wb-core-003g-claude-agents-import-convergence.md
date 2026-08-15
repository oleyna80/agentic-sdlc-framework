---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003g-claude-agents-import-convergence
work_block_id: WB-CORE-003G
status: in_progress
owner_role: orchestrator
created_at: 2026-08-14
last_updated: 2026-08-15
process_level: Standard
governance_profile: Managed
branch: agent/wb-core-003g-claude-agents-import
owner_approval: current Owner instruction to make CLAUDE.md a thin @AGENTS.md import and start the Work Block
critic_gate: APPROVE_WITH_REVIEW_CORRECTION
write_gate: READY
writer: one scoped Coder
base_revision: 4c4cc08f22c999777f75dc2f6bf801c68042c0be
---

# WB-CORE-003G — Claude `@AGENTS.md` Import Convergence

## Objective

Make the generated-project `CLAUDE.md` a thin Claude Code runtime entry point
that imports the canonical portable `AGENTS.md` instead of duplicating shared
lifecycle, authority, Hard Stop, skill-routing, and memory instructions.

This Work Block applies the framework rule that always-on runtime files should
maximize signal and route to canonical detail rather than copy it.

## Why now

The parent change in PR #37 separates framework self-hosting instructions from
the portable project contract and makes `template/AGENTS.md` the canonical
cross-runtime project entry point. The existing `template/CLAUDE.md` still
repeated substantial shared policy and had already drifted from the current
feature-branch commit/push rule.

Current Anthropic documentation explicitly supports `@AGENTS.md` imports for
repositories that already use `AGENTS.md`, and recommends concise `CLAUDE.md`
files with multi-step procedures moved to skills or scoped rules.

Upstream references verified 2026-08-14:

- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/debug-your-config

## Scope

### In scope

- `template/CLAUDE.md` — replace duplicated shared policy with `@AGENTS.md` plus
  only Claude Code-specific routing notes.
- `runtimes/claude-code/README.md` — document the import-shim model and align
  installation-profile wording with actual Claude/MCP composition.
- `scripts/test-sdd-contract.sh` — add one narrow deterministic assertion that
  the first non-empty instruction in `template/CLAUDE.md` remains exactly
  `@AGENTS.md`.
- this Work Block and bounded assurance evidence.

### Out of scope

- changes to root or template `AGENTS.md`;
- changes to governance, Hard Stops, permissions, hooks, subagent authority, or
  integration admission;
- new skills, commands, plugins, MCP servers, runtime dependencies, validators,
  or test frameworks;
- unrelated self-hosting drift outside the generated Claude project surface;
- Portable Kit promotion or any use of reserved `WB-CORE-004` through
  `WB-CORE-007` product Work Block IDs.

## Critic and independent review

Initial Critic result: **APPROVE.** The smallest sufficient implementation was a
thin import shim plus runtime adapter documentation; no new governance, skill,
hook, or validator was justified.

Independent frozen-subject review of
`4c4cc08f22c999777f75dc2f6bf801c68042c0be -> 2f38ff1406ff62730e07d72a63fb1e0d21da8a28`
returned **CHANGES_REQUIRED** with one material finding: existing profile tests
proved that `CLAUDE.md` exists but did not protect the semantic integrity of the
critical `@AGENTS.md` import. The review recommended one assertion in the
existing SDD contract test rather than new test machinery. That correction is
accepted as proportional and within the objective of this Work Block.

The same review identified one minor runtime-adapter wording issue: `.mcp.json`
is not part of the plain `claude-code` profile unless the separate MCP integration
component is selected. The wording is corrected without changing profile
composition.

## Write-set

```text
docs/plans/wb-core-003g-claude-agents-import-convergence.md
template/CLAUDE.md
runtimes/claude-code/README.md
scripts/test-sdd-contract.sh
docs/reports/reviews/wb-core-003g-claude-agents-import-convergence.md
docs/reports/verification/wb-core-003g-claude-agents-import-convergence.md
```

One Coder owns the implementation paths. No parallel writers are required.

## Implementation plan

1. Replace `template/CLAUDE.md` with `@AGENTS.md` plus concise Claude-specific
   pointers and non-expansion rules.
2. Reconcile `runtimes/claude-code/README.md` to describe `CLAUDE.md` as an import
   shim rather than a second project contract and describe MCP profile semantics
   literally.
3. Protect the critical import with one deterministic assertion in the existing
   `scripts/test-sdd-contract.sh` contract suite.
4. Review the frozen diff for accidental loss of Claude-specific runtime guidance.
5. Verify bootstrap/profile contracts and generated Claude profile behavior.

## Acceptance criteria

1. `template/CLAUDE.md` imports `AGENTS.md` using `@AGENTS.md`.
2. `template/CLAUDE.md` contains only Claude Code-specific runtime guidance and
   pointers; shared role, lifecycle, Hard Stop, closeout, and skill procedures are
   not duplicated there.
3. Claude-specific settings, hooks, subagents, skills, runtime capability, and
   adapter locations remain discoverable.
4. `runtimes/claude-code/README.md` accurately describes the import behavior and
   installation-profile semantics without implying that the plain Claude profile
   installs MCP configuration.
5. Existing authority, hooks, permissions, integrations, and bootstrap profile
   composition remain unchanged.
6. Existing executable contract tests fail if the first non-empty instruction in
   `template/CLAUDE.md` is no longer exactly `@AGENTS.md`.
7. Generated Claude-capable profiles retain both `AGENTS.md` and the Claude import
   shim after placeholder replacement and validation.
8. No new framework mechanism is introduced solely to support this convergence.

## Assurance

- **Evaluation:** NOT_REQUIRED — deterministic documentation/scaffold contract;
  no nondeterministic model-output behavior is an acceptance criterion.
- **Review:** required against the final frozen stacked diff. First independent
  pass returned CHANGES_REQUIRED; a second independent pass is required after
  corrections.
- **Verification:** existing bootstrap/profile contracts plus the targeted import
  assertion in `scripts/test-sdd-contract.sh`.
- **Drift:** confirm shared policy remains in `AGENTS.md`/governance/workflows and
  Claude-specific detail remains in the runtime adapter.

The independent review also observed that Framework Contracts is already red on
the stacked base because of a parent PR #37 `template/AGENTS.md` ordering check.
That inherited prerequisite failure is not attributed to WB-CORE-003G and should
be resolved in the parent stack before final closeout evidence is considered
green.

## Dependency / stacking

This branch is based on `agent/engineering-decision-principles` / Draft PR #37.
Its PR targets that branch while #37 is open. After #37 is merged, the follow-up
may be rebased/retargeted to `main` without changing its logical scope.

No merge is authorized by this Work Block.
