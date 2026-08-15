---
schema_version: 1
artifact_type: review_report
work_block_id: WB-CORE-003G
review_cycle: 1
review_type: independent_separate_chat
status: changes_required
subject_base: 4c4cc08f22c999777f75dc2f6bf801c68042c0be
subject_head: 2f38ff1406ff62730e07d72a63fb1e0d21da8a28
recorded_at: 2026-08-15
---

# WB-CORE-003G Independent Review — Cycle 1

## Provenance

This report records the result of a separate-context, read-only review supplied
back to the Orchestrator by the Owner. The reviewer inspected the frozen stacked
subject
`4c4cc08f22c999777f75dc2f6bf801c68042c0be -> 2f38ff1406ff62730e07d72a63fb1e0d21da8a28`
for Draft PR #38 rather than the cumulative diff relative to `main`.

## Verdict

**CHANGES_REQUIRED**

No blocker finding was attributed to the WB-CORE-003G stacked diff.

## Findings

### MATERIAL — critical `@AGENTS.md` import lacked deterministic regression protection

The generated Claude profile required and copied `CLAUDE.md`, but existing
bootstrap/profile and runtime-conformance checks did not verify the semantic
integrity of its critical first instruction. Removing `@AGENTS.md` could
therefore silently detach Claude Code from the canonical portable project
contract while neighboring executable checks still passed.

Recommended minimum correction: add one targeted assertion to an existing
contract test rather than create a new validator or test framework.

**Disposition:** accepted. `scripts/test-sdd-contract.sh` now requires the first
non-empty line of `template/CLAUDE.md` to equal `@AGENTS.md`. Final resolution is
pending independent re-review of the corrected frozen subject.

### MINOR — `.mcp.json` wording exceeded actual profile semantics

The runtime adapter described `.mcp.json` as empty/inert by default without
making clear that the plain `claude-code` profile does not install the separate
`integration:mcp-config` component.

**Disposition:** accepted. The adapter now states that `.mcp.json` is empty/inert
when the optional MCP integration component is installed and that the Claude
profile does not enable MCP integration automatically. Final resolution is
pending re-review.

## Positive review conclusions

The reviewer found the core architecture sound:

- `template/CLAUDE.md` is a runtime shim rather than a second governance contract;
- `@AGENTS.md` is the correct Claude Code import mechanism for the shared portable
  contract;
- shared behavior, workflows, skills, runtime mechanics, and engineering memory
  are separated appropriately;
- material Claude-specific runtime information remains discoverable through the
  runtime adapter and `.claude/` surfaces;
- no new governance, hook, permission, integration, or runtime mechanism is
  needed for the convergence itself.

## External prerequisite noted by review

The reviewer observed an inherited Framework Contracts failure on the stacked
base PR #37 involving the parent `template/AGENTS.md` ordering contract. The same
failure was present on the base revision and was not attributed to WB-CORE-003G.
It remains a parent-stack prerequisite for fully green closeout evidence.

The reviewer also noted a separate root self-hosting workflow drift outside this
Work Block's generated Claude surface. It is not repaired under WB-CORE-003G.

## Re-review requirement

A second independent read-only review must use the final corrected head and the
same stacked base. Cycle 1 remains `CHANGES_REQUIRED` until that pass establishes
a new verdict.
