---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003g-claude-agents-import-convergence
work_block_id: WB-CORE-003G
status: in_progress
owner_role: orchestrator
created_at: 2026-08-14
last_updated: 2026-08-14
process_level: Standard
governance_profile: Managed
branch: agent/wb-core-003g-claude-agents-import
owner_approval: current Owner instruction to make CLAUDE.md a thin @AGENTS.md import and start the Work Block
critic_gate: APPROVE
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
repeats substantial shared policy and has already drifted from the current
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
- `runtimes/claude-code/README.md` — document the import-shim model and remove
  redundant bootstrap wording that assumes separate manual reading of both files.
- this Work Block and bounded assurance evidence.

### Out of scope

- changes to root or template `AGENTS.md`;
- changes to governance, Hard Stops, permissions, hooks, subagent authority, or
  integration admission;
- new tests, validators, skills, commands, plugins, MCP servers, or runtime
  dependencies solely for this convergence;
- Portable Kit promotion or any use of reserved `WB-CORE-004` through
  `WB-CORE-007` product Work Block IDs.

## Critic result

**APPROVE.** The smallest sufficient change is a thin import shim plus runtime
adapter documentation. Existing bootstrap/profile tests already verify that the
selected Claude surface is generated and valid; adding a dedicated validator or
new test mechanism for one import line would be disproportionate.

## Write-set

```text
docs/plans/wb-core-003g-claude-agents-import-convergence.md
template/CLAUDE.md
runtimes/claude-code/README.md
docs/reports/reviews/wb-core-003g-claude-agents-import-convergence.md
docs/reports/verification/wb-core-003g-claude-agents-import-convergence.md
```

One Coder owns the implementation paths. No parallel writers are required.

## Implementation plan

1. Replace `template/CLAUDE.md` with `@AGENTS.md` plus concise Claude-specific
   pointers and non-expansion rules.
2. Reconcile `runtimes/claude-code/README.md` to describe `CLAUDE.md` as an import
   shim rather than a second project contract.
3. Review the frozen diff for accidental loss of Claude-specific runtime guidance.
4. Verify the existing bootstrap/profile contract still includes the Claude
   surface and inspect the generated-template import contract directly.

## Acceptance criteria

1. `template/CLAUDE.md` imports `AGENTS.md` using `@AGENTS.md`.
2. `template/CLAUDE.md` contains only Claude Code-specific runtime guidance and
   pointers; shared role, lifecycle, Hard Stop, closeout, and skill procedures are
   not duplicated there.
3. Claude-specific settings, hooks, subagents, skills, runtime capability, and
   adapter locations remain discoverable.
4. `runtimes/claude-code/README.md` accurately describes the import behavior and
   does not tell agents to manually load duplicated shared policy.
5. Existing authority, hooks, permissions, integrations, and bootstrap profile
   composition remain unchanged.
6. The existing Claude installation profile continues to require and copy
   `CLAUDE.md`; direct inspection confirms the template import survives normal
   placeholder replacement because `@AGENTS.md` contains no template variable.
7. No new framework mechanism is introduced solely to support this convergence.

## Assurance

- **Evaluation:** NOT_REQUIRED — deterministic documentation/scaffold contract;
  no nondeterministic model-output behavior is an acceptance criterion.
- **Review:** required against the frozen stacked diff.
- **Verification:** existing bootstrap/profile contract plus direct template and
  profile inspection; CI remains the executable repository contract boundary.
- **Drift:** confirm shared policy remains in `AGENTS.md`/governance/workflows and
  Claude-specific detail remains in the runtime adapter.

## Dependency / stacking

This branch is based on `agent/engineering-decision-principles` / Draft PR #37.
Its PR should target that branch while #37 is open. After #37 is merged, the
follow-up may be rebased/retargeted to `main` without changing its logical scope.

No merge is authorized by this Work Block.
