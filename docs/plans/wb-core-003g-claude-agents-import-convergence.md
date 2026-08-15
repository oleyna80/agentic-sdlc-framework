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
owner_approval: current Owner instruction to make CLAUDE.md a thin @AGENTS.md import and continue the approved Work Block
critic_gate: APPROVE_WITH_REVIEW_CORRECTION
write_gate: READY
writer: one scoped Coder
base_revision: 935c2d29123b5c4fe3dbf99ceb0f6fc7c9dc57cf
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
existing SDD contract test rather than new test machinery. That correction was
accepted as proportional and implemented.

The same review identified one minor runtime-adapter wording issue: `.mcp.json`
is not part of the plain `claude-code` profile unless the separate MCP integration
component is selected. The wording was corrected without changing profile
composition.

A second independent read-only re-review of the corrected stacked subject
`4c4cc08f22c999777f75dc2f6bf801c68042c0be -> ae62a5448b6fc5f521ceff7239940001abc88507`
returned **READY** with both findings resolved and no new BLOCKER/MATERIAL issue.
That review also correctly noted that Framework Contracts #1113 failed on an
inherited parent PR #37 contract before the new `@AGENTS.md` assertion executed.
The parent failure was therefore an integration-evidence gap, not a WB-CORE-003G
implementation defect.

Because PR #37 and the later self-hosting reconciliation PR #39 are now merged,
this branch has been synchronized non-destructively with current `main`. The
base/head pair changed, so final closeout requires green CI and one narrow
independent re-review of the new frozen subject.

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
4. Preserve the logical child delta while synchronizing the branch to current
   `main` without rebase or force-push.
5. Verify the final `main -> head` diff remains limited to the five intended
   WB-CORE-003G files.
6. Run current Framework Contracts and Release State Contract on the synchronized
   head.
7. Freeze the synchronized head and obtain final narrow independent assurance.

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
9. The synchronized diff against current `main` contains only the intended five
   WB-CORE-003G files and does not reintroduce parent/root governance changes.
10. Current CI is green on the final frozen head before closeout.

## Assurance

- **Evaluation:** NOT_REQUIRED — deterministic documentation/scaffold contract;
  no nondeterministic model-output behavior is an acceptance criterion.
- **Review:** original review CHANGES_REQUIRED, corrected stacked re-review READY;
  one final narrow re-review is required because synchronization changed the
  frozen base/head pair.
- **Verification:** current bootstrap/profile contracts plus the targeted import
  assertion in `scripts/test-sdd-contract.sh`; current CI must execute that
  assertion successfully on the synchronized head.
- **Drift:** confirm shared policy remains in `AGENTS.md`/governance/workflows and
  Claude-specific detail remains in the runtime adapter.

The previous inherited PR #37 CI failure has been resolved and PR #37 is merged.
WB-CORE-003H / PR #39 is also merged, so the root self-hosting authority drift
noted by the earlier review is no longer an outstanding dependency. Historical
red CI on `ae62a544...` is retained as provenance but is not current closeout
evidence.

## Dependency / synchronization

PR #37 was the original stacked parent. It has been independently assured and
squash-merged into `main`; WB-CORE-003H / PR #39 was subsequently assured and
merged as well.

On 2026-08-15 current `main` at
`935c2d29123b5c4fe3dbf99ceb0f6fc7c9dc57cf` was merged non-destructively into
`agent/wb-core-003g-claude-agents-import`. Conflict resolution used current
`main` as the baseline and preserved only the WB-CORE-003G child delta. In
particular, `scripts/test-sdd-contract.sh` kept all current parent/root contract
additions and added only the previously reviewed two-line `@AGENTS.md` assertion.
No rebase, force-push, or history rewrite was used.

After this synchronization PR #38 was retargeted from
`agent/engineering-decision-principles` to `main`. The immediate synchronized
head before this Work Block record update was
`d8c5f5227b98701472a6b68bf2a00a7483b31f0a`, and its diff against current
`main` contained exactly the same five logical WB-CORE-003G files.

No merge of PR #38 is authorized by this Work Block; final merge remains
Owner-controlled after current CI and final independent assurance.
