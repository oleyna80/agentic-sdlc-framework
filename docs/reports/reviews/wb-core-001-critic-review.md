---
schema_version: 1
artifact_type: critic_review
artifact_id: wb-core-001-critic-review
work_block_id: WB-CORE-001
status: imported_and_resolved
verdict: APPROVE_WITH_CHANGES
created_at: 2026-07-29
source_framework_revision: 0fce7389d27690482e910e942a1f3138c2fef123
historical_framework_revision: 0c632db0b0444e556251c384f6254141c9df59bc
superpowers_reference_revision: 44c9b2d6e889982ac18c27d05a19fefe335194e1
---

# Critic Review — Portable Agentic SDLC Project Kit

## Evidence Source

This document preserves the supplied Critic review findings and verdict for
WB-CORE-001. Formatting, immutable source revisions, and the
`Orchestrator Resolution` section were added for repository use. The original
conclusions are not reinterpreted as unconditional approval.

Evidence revisions used by the Critic:

- current framework:
  `agentic-sdlc-framework@0fce7389d27690482e910e942a1f3138c2fef123`;
- practical framework baseline:
  `agentic-sdlc-framework@0c632db0b0444e556251c384f6254141c9df59bc`;
- external reference:
  `obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1`.

## Evidence Limitation

The Critic reported that the named audit attachment
`agentic-sdlc-framework-core-recovery-audit.md` was not available or retrievable
in that agent's execution environment. Exact line citations to that attachment
could therefore not be produced by the Critic.

This is an execution-environment evidence limitation. It is not evidence that
the audit did not exist, and it does not invalidate the audit direction supplied
to the Orchestrator. The Critic cross-checked the proposed direction against the
immutable repository revisions and the Superpowers reference listed above.

## Scope Reviewed

The Critic reviewed the proposed recovery direction for:

- product boundary;
- role packaging and authority;
- skill inventory;
- canonical memory location;
- process-level classification;
- installation and runtime neutrality;
- WB-CORE-001 scope;
- Git branch, commit, push, PR, and merge authority.

## Verdict

**APPROVE_WITH_CHANGES**

The direction is sound only after the changes below are incorporated. The target
must be a portable, self-contained Agentic SDLC project kit that preserves the
practical lifecycle, role separation, committed project memory, collision-safe
installation, fresh verification, and Owner-controlled integration. It must not
retain framework ownership of runtimes, providers, hooks, plugins, MCP, or
provider-specific agent configuration.

## Findings

### CRIT-001 — Product boundary is too close to a skills library

- **Severity:** High
- **Finding:** The proposed boundary under-described the complete operating
  system around the skills. Skills alone do not provide the entry contract, SDD
  lifecycle, Work Blocks, plans, mission briefs, memory, logs, assurance
  artifacts, or closeout.
- **Required change:** Define the product as a complete Portable Agentic SDLC
  Project Kit, not a skills package.

### CRIT-002 — A single `roles.md` over-consolidates role contracts

- **Severity:** High
- **Finding:** Combining all roles in one file weakens bounded loading, manual
  handoff, and separate role procedures. It also encourages duplicated runtime
  mirrors.
- **Required change:** Specify separate portable contracts for Orchestrator,
  Architect, Critic, Coder, Reviewer, and Verifier while keeping common authority
  canonical in `AGENTS.md`.

### CRIT-003 — The proposed eight-skill inventory is too compressed

- **Severity:** Medium
- **Finding:** Specification and implementation planning were not represented as
  distinct procedures, leaving an incomplete Define stage.
- **Required change:** Define nine core procedural skills, including separate
  `specification` and `implementation-planning`, and give every relevant current
  or historical mechanism an explicit disposition.

### CRIT-004 — Canonical memory should remain `memory_bank/`

- **Severity:** High
- **Finding:** Moving canonical project memory under a generic `project/` path
  would break the proven practical contract and blur committed knowledge with
  runtime-local state.
- **Required change:** Keep the committed `memory_bank/` structure and define a
  separate ignored local path for scratch, caches, transcripts, and traces.

### CRIT-005 — Keep a generic installer; remove runtime profiles

- **Severity:** High
- **Finding:** Removing installation entirely would make the project kit
  impractical, while retaining runtime profiles would preserve the control-plane
  coupling the recovery is intended to remove.
- **Required change:** Specify a runtime-neutral, collision-safe `plan`/`apply`
  installer with no provider agents, hooks, plugins, MCP, or capability profiles.

### CRIT-006 — Process levels need risk-based operational rules

- **Severity:** High
- **Finding:** Quick/Standard/High-Risk cannot be selected primarily by file count
  or task size. The original proposal lacked sufficiently precise escalation and
  degraded-assurance rules.
- **Required change:** Classify using ambiguity, behavior, architecture, system
  boundaries, authority, side effects, reversibility, security/data risk,
  verification cost, and nondeterminism. Missing required independence must
  remain blocked or unverified.

### CRIT-007 — WB-CORE-001 is over-scoped if it includes implementation

- **Severity:** High
- **Finding:** Combining normative architecture with candidate, installer, role,
  skill, template, test, or migration implementation would make review and source
  authority ambiguous.
- **Required change:** Limit WB-CORE-001 to the approved documentation write-set.
  Candidate and installer implementation must begin only in later Work Blocks.

### CRIT-008 — A blanket branch/commit/PR prohibition is incorrect

- **Severity:** Medium
- **Finding:** Prohibiting feature-branch commits, push, or PR creation conflicts
  with a reviewable documentation Work Block. The real Hard Stop is integration
  into the default/protected branch and other consequential actions.
- **Required change:** Allow feature-branch commits, push, and PR creation inside
  the approved Work Block. Preserve explicit Owner approval for merge,
  default-branch push, deployment, secrets, destructive actions, live data, and
  material scope expansion. Do not require final verification before every
  checkpoint commit.

## Required Approval Conditions

The Critic's `APPROVE_WITH_CHANGES` verdict requires all of the following:

1. Complete project-kit boundary.
2. Separate portable role contracts.
3. Nine core procedural skills.
4. Canonical committed `memory_bank/` and separate local scratch.
5. Risk-based Quick/Standard/High-Risk levels.
6. One write Work Block per working tree and one Coder per write-set.
7. Generic collision-safe installer with no runtime/provider output.
8. Documentation-only WB-CORE-001.
9. Feature-branch/PR workflow allowed; merge remains separately Owner-approved.
10. Candidate isolation and a bounded migration sequence before promotion.

## Orchestrator Resolution

| Finding | Resolution |
|---|---|
| CRIT-001 | `docs/specs/portable-agentic-sdlc-project-kit.md` sections 1–3 define a complete project kit and explicitly reject a skills-library-only product. |
| CRIT-002 | Specification sections 7–8 and `2026-07-29-portable-kit-roles-memory-installation.md` define six separate role files with common authority in `AGENTS.md`. |
| CRIT-003 | Specification section 12 defines exactly nine core skills and a disposition table for current and historical mechanisms. |
| CRIT-004 | Specification section 14 and the roles/memory/installation ADR retain canonical `memory_bank/` and define ignored `.agentic-local/`. |
| CRIT-005 | Specification section 19 and the roles/memory/installation ADR define runtime-neutral `plan`/`apply` installation and exclude runtime profiles and provider output. |
| CRIT-006 | Specification section 6 defines mandatory High-Risk triggers, Standard escalation, strict Quick eligibility, and blocked/unverified assurance semantics. |
| CRIT-007 | `docs/plans/wb-core-001-normative-architecture.md` restricts writes to five documentation paths and explicitly excludes all candidate and installer implementation. |
| CRIT-008 | Specification section 18 allows feature-branch commits, push, and PR creation while requiring separate Owner approval for merge and other Hard Stops. |

All required architectural changes are incorporated into the proposed WB-CORE-001
document set. This resolution does not change the original verdict to
`APPROVE`. The PR still requires independent review/verification, and merge still
requires a separate explicit Owner decision.

## Residual Risks

- The current repository still contains accepted control-plane and
  runtime/provider assets; migration has not begun.
- The portable roles, skills, templates, memory skeleton, installer, and tests do
  not yet exist.
- Installer path and symlink safety remain conceptual until WB-CORE-003 tests them.
- A single HardwareLab pilot cannot prove universal compatibility.
- Archive and promotion operations may break historical links unless WB-CORE-006
  verifies repository maps and provenance.
