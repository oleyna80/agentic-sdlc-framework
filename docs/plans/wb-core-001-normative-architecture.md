---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-001-normative-architecture
work_block_id: WB-CORE-001
status: planned
owner_role: orchestrator
created_at: 2026-07-29
base_revision: 0fce7389d27690482e910e942a1f3138c2fef123
branch: agent/portable-kit-normative-architecture
process_level: Standard
---

# WB-CORE-001 — Normative Architecture for the Portable Agentic SDLC Project Kit

## Objective

Define the normative architecture for the Portable Agentic SDLC Project Kit
before any candidate, installer, role, skill, template, test, or migration
implementation begins.

The Work Block preserves the practical SDLC and removes framework ownership of
specific runtimes, providers, models, hooks, plugins, MCP integrations,
capability negotiation, and provider-specific agent configuration.

## Evidence Baseline

- Current repository base:
  `agentic-sdlc-framework@0fce7389d27690482e910e942a1f3138c2fef123`
- Practical framework baseline:
  `agentic-sdlc-framework@0c632db0b0444e556251c384f6254141c9df59bc`
- External methodology reference:
  `obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`
- `Agentic SDLC Framework Core Recovery Audit`
- `Critic Review — Portable Agentic SDLC Project Kit`
- Current repository contracts and history

The current `main` SHA matched the previously reviewed baseline at Work Block
start. No intervening `main` change required scope adjustment.

## Process and Authority Classification

- **Process level:** Standard. The change is documentation-only but materially
  changes target product boundary, role packaging, memory ownership,
  installation, and migration architecture.
- **Side effects:** feature-branch documentation commits and pull request only.
- **Write authority:** scoped Architect / Documentation Coder for the approved
  paths below.
- **Merge authority:** none. Merge requires separate explicit Owner approval.
- **Deployment/data/secrets:** none.
- **Final verification:** independent Verifier pass after the PR exists; no final
  verification report is created by the current Architect / Documentation Coder
  pass.
- **Post-PR Verifier artifact:** the independent pass must use a separately
  approved write-set for
  `docs/reports/verification/wb-core-001-normative-architecture.md` and verify the
  final PR head. That artifact is intentionally not created in this Work Block.

## Approved Write-Set

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
docs/plans/wb-core-001-normative-architecture.md
docs/reports/reviews/wb-core-001-critic-review.md
```

Creating missing parent directories for those paths is allowed.

## Legacy Release-State Boundary

This file is a **planned migration Work Block proposal**, not the registered
active Work Block of the current control-plane release-state ledger.
`PROJECT_MAP.md` and `FILE_REGISTRY.yml` therefore continue to record no active
Work Block for the current operational baseline. Modifying those projections is
outside this Work Block's approved write-set.

Consequently, a green legacy release-state check proves that the current
operational ledger remains internally consistent; it does not constitute final
verification or closeout of WB-CORE-001. WB-CORE-001 becomes normative only after
the independent post-PR assurance artifact exists and the Owner separately
approves merge.

## Out of Scope

- `candidate/portable-agentic-sdlc-kit/` content;
- installer or packaging code;
- role and skill implementation files;
- templates, tests, fixtures, or migration scripts;
- `.codex/`, `.claude/`, `.opencode/`, hooks, MCP, plugins, model routing, or
  runtime profiles;
- repository settings, secrets, credentials, deployment, live state, or data;
- default-branch writes or merge;
- final verification report in the current pass; it is reserved for the separate
  independent Verifier pass described above.

## Required Decisions

1. Product is a complete project kit, not a skills library or control plane.
2. Runtime neutrality is achieved by non-ownership of runtime/provider concerns.
3. Six roles receive separate portable contracts; shared authority stays in
   `AGENTS.md`.
4. Exactly nine procedural skills form the core.
5. `memory_bank/` remains canonical committed project memory; `.agentic-local/`
   is ignored scratch.
6. Quick, Standard, and High-Risk are risk-based and operationally precise.
7. One active write Work Block is allowed per working tree.
8. Feature-branch commits, push, and PR are allowed within the approved Work
   Block; merge/default-branch push remain Owner-controlled.
9. Candidate and installer contracts are specified without implementation.
10. Optional extensions remain outside the core.
11. Six migration Work Blocks are bounded with no equal unresolved alternatives.

## Execution Plan

1. Resolve current `main` and compare it with the reviewed base.
2. Inspect the practical baseline, current contracts, current skill catalog, and
   immutable Superpowers reference.
3. Preserve the supplied Critic findings and verdict, including the audit-access
   evidence limitation.
4. Draft the normative specification with the required 24-section structure.
5. Draft the product-boundary ADR.
6. Draft the roles/memory/installation ADR.
7. Check terminology, path consistency, source revisions, internal links,
   runtime-neutrality, and approved write-set.
8. Commit and push only the approved paths on
   `agent/portable-kit-normative-architecture`.
9. Open a PR to `main`; do not merge.
10. Hand the final PR head to an independent Verifier using the separately
    approved artifact path defined above.

## Acceptance Criteria

- [x] Complete project-kit boundary is defined.
- [x] Runtime/provider ownership is excluded.
- [x] Six separate role contracts are specified and common authority remains in
  `AGENTS.md`.
- [x] Nine core skills are fully specified.
- [x] Relevant current and historical mechanisms have a disposition.
- [x] Project memory and local scratch boundaries are explicit.
- [x] Process levels and concurrency rules are precise.
- [x] Git and Owner authority rules are precise.
- [x] Candidate, installer, optional extensions, and six migration Work Blocks are
  bounded without implementation.
- [x] Exact evidence revisions are recorded.
- [x] No unresolved equal architectural alternatives or placeholder markers remain.
- [x] Changes are limited to the approved write-set.
- [x] A persistent artifact path is specified for the separate post-PR Verifier
  pass without creating that report in the current scope.
- [ ] PR assurance is completed by an independent Reviewer/Verifier.
- [ ] Owner separately approves merge.

## Self-Checks

The documentation set must be checked for:

- exact required specification headings `1` through `24`;
- internal Markdown path references and path spelling;
- consistent use of `Quick`, `Standard`, and `High-Risk`;
- consistent candidate and promotion paths;
- absence of Codex, Claude Code, OpenCode, MCP, hooks, or plugins as authorities
  or core dependencies;
- absence of candidate implementation files and installer code;
- absence of placeholder markers, equal alternatives, or silent open decisions;
- diff/write-set restricted to the five approved paths.

## Current State

- **Define:** complete as a proposed architecture.
- **Critic:** imported with verdict `APPROVE_WITH_CHANGES`; required changes are
  resolved in the proposed specification and ADRs.
- **Execute:** documentation write-set complete on the feature branch.
- **Legacy release state:** this planned proposal is intentionally not registered
  as the current operational active Work Block.
- **Review/Verification:** pending independent post-PR assurance against the final
  head and the separately approved verification artifact.
- **Closeout:** reporting-only until assurance and separate Owner merge decision.
- **Merge:** prohibited without a new explicit Owner instruction.
