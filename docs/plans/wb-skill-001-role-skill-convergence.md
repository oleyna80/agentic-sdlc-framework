---
schema_version: 1
artifact_type: work_block
artifact_id: wb-skill-001-role-skill-convergence
work_block_id: WB-SKILL-001
status: in_progress
owner_role: Owner
created_at: 2026-08-18
last_updated: 2026-08-19
governance_profile: Managed
branch: agent/wb-skill-001-role-skill-convergence
base_revision: 3ec044953a854dd8906a4849df507357bd3b87f0
write_gate: READY
critic_gate: READY
---

# WB-SKILL-001 — Framework-Native Role Skill Convergence

## Metadata

- **Work Block ID:** WB-SKILL-001
- **Title:** Framework-Native Role Skill Convergence
- **Date:** 2026-08-18
- **Owner:** Owner-authorized framework maintenance initiated in this conversation.
- **Owner role:** Owner
- **Orchestrator:** Codex, responsible for bounded Define synchronization and
  transition coordination.
- **Governance Profile:** Managed
- **Execution Mode:** staged approval
- **Verification Tier:** standard
- **Evaluation Required:** no
- **Reason:** The target is deterministic framework procedure/documentation
  consistency. No materially non-deterministic output or autonomous
  consequential behavior is being introduced.
- **Base Revision:** `3ec044953a854dd8906a4849df507357bd3b87f0`
- **Branch:** `agent/wb-skill-001-role-skill-convergence`

## Lifecycle State

- **Current Stage:** Execute
- **Stage State:** in_progress
- **Write Gate:** READY — final independent consistency recheck completed;
  limited to the exact twelve Coder source paths.
- **Critic Gate:** READY — operational state after the separate Critic
  `SUPPLEMENT` was bound and its Define requirements were addressed; this is
  distinct from the Critic functional verdict.
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation Verdict:** NOT_REQUIRED
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
- **Owner Approval Evidence:** Owner message on 2026-08-19: “подтверждаю
  продолжение воркблока. оформляй синхронизацию и переходи к реализации
  write-set.” It authorizes the exact twelve source paths bound below after the
  current Define synchronization. It does not authorize staging, commit, push,
  PR creation, merge, deploy, or destructive action.

### Define Quality Prerequisite

- **Required:** yes
- **Status:** READY
- **Requirements Review Evidence:** Historical round 1 —
  `docs/reports/requirements/wb-skill-001.md`; subject
  `83e6f7df063056a3c8c579bd518df17d279f6f6e`; evidence commit
  `97e7be5aa502d410a8636c32634e621c40c90801`; verdict
  `CHANGES_REQUIRED`; finding: specification authority wording required
  correction. This evidence is historical / superseded for current readiness
  purposes and is not passing evidence. Fresh re-review:
  `docs/reports/requirements/wb-skill-001-rereview.md`; subject
  `073b6c4ca2bde67f0ddbb16e180ed5838abdfe3b`; verdict `READY`.
- **Traceability Evidence:** PASS — `validate-define-traceability.py` against
  `docs/specs/wb-skill-001-role-skill-convergence.md`
  (`2e58550c1619bf690ebde36a54782e610f9fc072`) and
  `docs/tasklist/wb-skill-001-role-skill-convergence.md`
  (`348b9b924c47425b5c58ea6f64440157545c08b6`): READY
- **Consistency Analysis Evidence:** `READY` —
  `docs/reports/requirements/wb-skill-001-consistency.md`; initial documentary
  gaps were resolved, then independently rechecked in a separate delegated
  context in the same runtime/session (not OS-isolated).

Managed Define quality is complete. The source Write Gate is READY only for the
exact twelve Coder source paths bound below; no Git/publication authority is
created by this transition.

## Objective

Converge the reusable framework role-skill layer with the current accepted
runtime-neutral Agentic SDLC contracts so agents routed through
`.agent/ROSTER.md` receive procedures consistent with current authority;
Define → Execute → Assure → Close; Work Block/write-set semantics;
Critic/Reviewer/Verifier contracts; Git authority; runtime neutrality;
proportional engineering; and skill-library reuse boundaries.

The Work Block removes legacy project semantics from current operational role
skills without redesigning accepted governance. A skill supplies procedure, not
authority: stale reusable skills must converge to accepted governance, not the
reverse.

## Expected Final Result

At completion:

1. Critic, Coder, Reviewer, and Verifier procedure routes are framework-native
   and subordinate to accepted governance.
2. No critical role skill uses `Control Tower` as an authority-bearing term,
   invents Stage 0.5 or a parallel lifecycle, or cites nonexistent AGENTS.md
   sections.
3. Critical reusable role skills do not hardcode unrelated product paths,
   language/product topology, deployment assumptions, or framework-external
   project conventions.
4. Coder preserves one Coder per approved write-set and uses current Git
   authority: normal reversible staging, local commit, normal feature-branch
   push, and PR update may occur within approved scope when permitted; Hard
   Stops remain hard stops.
5. Critic remains read-only and uses `APPROVE | SUPPLEMENT | RECONSIDER`
   distinctly from the operational Critic gate state.
6. Reviewer remains read-only and uses
   `READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED`.
7. Verifier uses `READY | BLOCKED | UNVERIFIED` but does not claim exclusive
   lifecycle blocking authority.
8. Each materially revised reusable skill receives truthful decision provenance;
   unresolved provenance is recorded rather than invented.
9. Direct live adapters are corrected where required, otherwise a bounded
   follow-up states why they are not in this Work Block.
10. A small deterministic extension of an existing contract test prevents this
    critical-role vocabulary drift from silently recurring.
11. No unrelated shared-skill cleanup, governance redesign, or historical
    evidence rewrite is performed.

## Done Criteria

- [ ] The approved critical and required supporting paths converge to the
  governing contracts without creating a second lifecycle or authority model.
- [ ] Required provenance, Critic, independent review, verification, and drift
  evidence are recorded for the frozen implementation subject.
- [ ] The scoped deterministic regression check passes, and unrelated legacy or
  historical surfaces remain outside this Work Block unless separately approved.

## Normative Baseline

- **Approved Specification:** `docs/specs/wb-skill-001-role-skill-convergence.md`.
- **Specification Status:** approved on 2026-08-19 after Owner confirmation and
  requirements-quality re-review `READY`.
- **Specification Revision:** current working revision; no commit or publication
  is implied by this state.
- **Accepted Architecture Decisions:** `AGENTS.md`, `governance/authority.md`,
  `governance/lifecycle.md`, `governance/artifacts.md`, and
  `governance/decision-provenance.md`.
- **Runtime/role contracts:** `.agent/ROSTER.md`,
  `template/.agent/workflows/sdd-protocol.md`,
  `template/.agent/critic-gate.md`, `skills/SKILL-CONVENTION.md`, and
  `skills/catalog.yml`.
- **External Contracts:** not applicable.
- **Approved Evaluation Plan:** not required.
- **Active Tasklist:** `docs/tasklist/wb-skill-001-role-skill-convergence.md`;
  no active machine Work Block state is changed by this Define run.

## Repository Preflight

- **Git baseline:** `main` and `origin/main` both resolved to
  `3ec044953a854dd8906a4849df507357bd3b87f0` before branch creation.
- **Pre-existing dirty files:** none tracked.
- **Untracked artifacts:** `Repository Graph Evaluation Brief.md` was present
  before work and is out of scope.
- **Current diff:** initially none; this Work Block is the sole authorized
  tracked change.
- **Proceed rule:** do not add, edit, delete, move, stage, or commit the
  untracked evaluation brief; stop for unexpected tracked dirt or subject move.

## Dependency Check

### Must Resolve Before Source Execute

- Material-revision provenance for every reusable skill actually changed.

### May Resolve During Future Work

- Whether a mechanically checkable referenced helper exists in each corrected
  adapter. If an adapter cannot be made coherent within the bounded paths below,
  return to Define rather than broaden the write-set silently.

## Scope

### In Scope Now

- Complete Define synchronization and its independent recheck.
- Execute only the exact twelve source paths in the approved Coder write-set,
  including the narrow existing-contract-test extension.

### Out of Scope

- Redesigning `governance/authority.md`, the macro lifecycle, governance
  profiles, define-quality, or runtime capability policy.
- Removing `APPROVE | SUPPLEMENT | RECONSIDER`, changing Spec Kit mechanisms or
  convergence, canonical aggregate correction, deployment/release/credential/
  branch-protection changes, and production changes.
- Wholesale skill modernization, translation/reformatting, or deletion of
  truthful historical evidence because it contains legacy terminology.
- `Repository Graph Evaluation Brief.md`.

## Write-Set

**Role-authorized coordination/evidence paths:**

```text
docs/plans/wb-skill-001-role-skill-convergence.md
docs/specs/wb-skill-001-role-skill-convergence.md
docs/tasklist/wb-skill-001-role-skill-convergence.md
docs/reports/reviews/wb-skill-001-critic.md
docs/reports/requirements/wb-skill-001-consistency.md
```

**Approved Coder source write-set (exactly twelve paths):**

```text
skills/critic-review/SKILL.md
skills/scoped-coder/SKILL.md
skills/reviewer/SKILL.md
skills/verifier/SKILL.md
template/.claude/agents/critic.md
template/.claude/agents/scoped-coder.md
template/.claude/agents/reviewer.md
template/.claude/agents/verifier.md
template/.codex/AGENTS.md
template/.codex/critic.md
template/.codex/instructions.md
scripts/test-sdd-contract.sh
```

- **One Coder per source write-set:** yes.
- **Parallel writers:** no.
- **Scope guard:** `git status --short`, `git diff --check`, and changed-path
  validation. The untracked evaluation brief remains excluded.
- **Gate state:** READY for these twelve paths only; no source path may be added
  by a report or coordination update.

## Risk and Authority

- **Side-Effect Class:** local-docs.
- **DB/Data Action Mode:** none.
- **Sensitive Domains:** governance procedure consistency.
- **Output Non-Determinism:** none; the subject is deterministic text and
  contract-test alignment.
- **Autonomous Tool/Trajectory Risk:** low; the source subject is deterministic
  text and a shell contract test, but authority/lifecycle drift is material.
- **Threat Model Required:** no new threat model; future review must preserve
  existing authority and Hard Stop boundaries.
- **Rollback / Recovery:** revert only this known Work Block commit if Owner
  later directs it; no destructive action is authorized here.

## Hard Stops in Scope

- [x] Push, PR creation, merge, rebase, force push, branch deletion, and
  production/deployment/credential/destructive actions are not authorized.
- [x] No source path outside the exact twelve paths, no governance/machine Work
  Block state, no Spec Kit, and no canonical aggregate change is authorized.
- [x] Staging and local commit are not authorized by the current Owner message.

## Function Bindings

| Function | Logical Role | Runtime | Isolation | Authority | Evidence |
|---|---|---|---|---|---|
| Orchestration | Orchestrator | Codex | same runtime/session | coordination paths only | this Work Block and bound evidence |
| Consistency | Consistency Analyzer | Codex delegated subagent | separate delegated context in same runtime/session; not OS-isolated | read-only | consistency report |
| Critic | Critic | Codex delegated subagent | separate delegated context in same runtime/session; not OS-isolated | read-only | `docs/reports/reviews/wb-skill-001-critic.md` |
| Implementation | Coder | Codex main thread | one active writer, same runtime/session | exact twelve source paths after gate READY | scoped diff/self-check |
| Review | Reviewer | not yet bound | not yet established | read-only | required after source change |
| Verification | Verifier | not yet bound | not yet established | read-only | required after source change |
| Evaluation | not required | n/a | n/a | n/a | deterministic subject |

## Skills

- **Checked:** `skills/SKILL-CONVENTION.md`, `skills/catalog.yml`, and all
  relevant role/reusable skill surfaces in the inventory.
- **Matched / Used:** current repo procedures `skills/critic-review/SKILL.md`
  and `skills/scoped-coder/SKILL.md` were read as procedural inputs; authority
  remains in the governing contracts and this approved Work Block.
- **Completed:** separate Critic review and initial consistency analysis.
- **Pending:** final consistency recheck, then Coder execution; independent
  implementation review and verification remain post-Execute requirements.

## Define Requirements and Traceability

The authoritative behavioral requirements and measurable acceptance criteria
are `REQ-001` through `REQ-012` and `AC-001` through `AC-014` in
`docs/specs/wb-skill-001-role-skill-convergence.md`. The traceable proposed
implementation and assurance tasks are in
`docs/tasklist/wb-skill-001-role-skill-convergence.md`.

This Work Block is the implementation/assurance plan. The tasklist source paths
are now the exact Owner-authorized Coder write-set stated above, contingent on
the final Define consistency recheck; coordination evidence cannot expand it.

## Implementation Plan

| Task | Owner Role | Write-Set | Dependencies | Expected Evidence | Status |
|---|---|---|---|---|---|
| Define inventory | Orchestrator | this Work Block only | baseline contracts | inventory below | completed in this revision |
| Critical role correction | one Coder | approved A paths | Define quality READY | scoped diff/self-check | in progress |
| Adapter/test coherence | same Coder | approved B paths | Define quality READY | focused test diff | in progress |
| Assurance | Critic, Reviewer, Verifier | reports only | frozen subject | required reports/checks | planned, blocked |

## Define Inventory — Legacy Role-Skill Convergence

| Path | Current role/use | Finding | Classification A-E | Governing contract | Proposed disposition |
|---|---|---|---|---|---|
| `skills/critic-review/SKILL.md` | Routed Critic procedure | Calls the Orchestrator `Control Tower`; defines `Stage 0.5`, `Plan & Discover`, and `Stage 1`; cites `AGENTS.md § Structural Authority Model`; says Critic is not a gate without preserving the functional-verdict/gate-state distinction. | A — CRITICAL / FIX IN THIS WB | `governance/lifecycle.md`; `template/.agent/workflows/sdd-protocol.md`; `template/.agent/critic-gate.md`; `.agent/ROSTER.md` | Replace parallel lifecycle/authority terms; retain read-only `APPROVE | SUPPLEMENT | RECONSIDER`; state that functional verdict and operational gate state are separate. |
| `skills/scoped-coder/SKILL.md` | Routed Coder procedure | Limits writes to `web/*`, `scripts/*`, `05_ai/*`; cites nonexistent Structural Authority Model; says `Commit, push, deploy` are forbidden; repeatedly delegates authority to `Control Tower`; treats VPS/Docker/email and public-repo rules as universal. | A — CRITICAL / FIX IN THIS WB | `AGENTS.md` §5; `governance/authority.md`; `governance/lifecycle.md`; `.agent/ROSTER.md` | Keep one approved write-set and Hard Stops; use generic repository paths; permit current normal reversible Git operations when approved/permitted; remove project topology. |
| `skills/reviewer/SKILL.md` | Routed Reviewer procedure | Declares `No BLOCKED`; says only Verifier/Control Tower can decide; requires `fr/ru` copy review; invokes missing `.claude/skills/reviewer/scripts/*`; assumes form/API/email and app-route flows; cites nonexistent Structural Authority Model. | A — CRITICAL / FIX IN THIS WB | `governance/artifacts.md`; `governance/authority.md`; `.agent/ROSTER.md` | Preserve read-only frozen-subject review; adopt `READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED`; replace project checks/helper path with scoped evidence selection. |
| `skills/verifier/SKILL.md` | Routed Verifier procedure | Claims it is the only agent able to stop the pipeline; cites nonexistent Structural Authority Model/Security Review Baseline; invokes missing `.claude/skills/verifier/scripts/*`; presents Next.js/routes/CSP/CSRF/npm/VPS checks as universal. | A — CRITICAL / FIX IN THIS WB | `governance/artifacts.md`; `governance/authority.md`; `governance/lifecycle.md`; `.agent/ROSTER.md` | Preserve read-only `READY | BLOCKED | UNVERIFIED` and reproducible evidence; remove exclusive-blocker claim and choose checks proportionally to the Work Block. |
| `template/.claude/agents/critic.md` | Direct Claude Critic adapter | Uses Control Tower and old Stage 0/0.5/1/2/3 labels; permits a Critic memory write despite read-only contract; describes advisory status without current gate distinction. | A — CRITICAL / FIX IN THIS WB | `template/.agent/workflows/sdd-protocol.md`; `template/.agent/critic-gate.md`; `governance/authority.md` | Make it a read-only adapter to the current macro lifecycle and Critic functional verdict/gate-state model. |
| `template/.claude/agents/scoped-coder.md` | Direct Claude Coder adapter | Retains authority-bearing `Control Tower` wording, so a corrected routed skill would still encounter a conflicting current adapter. | A — CRITICAL / FIX IN THIS WB | `AGENTS.md` §4–5; `governance/authority.md` | Replace only the conflicting authority/lifecycle wording; retain adapter-specific, non-authority instructions that remain compatible. |
| `template/.claude/agents/reviewer.md` | Direct Claude Reviewer adapter | Says Reviewer is not `BLOCKED` and Control Tower/Verifier decide, conflicting with the current Reviewer verdict contract. | A — CRITICAL / FIX IN THIS WB | `governance/artifacts.md`; `governance/authority.md` | Align read-only reviewer verdict and frozen-subject semantics to current governance. |
| `template/.claude/agents/verifier.md` | Direct Claude Verifier adapter | Uses Control Tower gate authority and stale Security Review Baseline reference; otherwise contains current verifier vocabulary. | A — CRITICAL / FIX IN THIS WB | `governance/artifacts.md`; `governance/lifecycle.md` | Retain verifier vocabulary/evidence role while removing stale authority/reference language. |
| `template/.codex/AGENTS.md` | Direct Codex runtime adapter | Defines `Stage 0.5`, assigns formal READY/BLOCKED exclusively to Verifier, and retains an old Plan → Spec → Implementation mapping. | B — SUPPORTING / INCLUDE ONLY IF REQUIRED | `AGENTS.md`; `governance/lifecycle.md`; `governance/artifacts.md` | Include because it remains a live direct adapter that would contradict corrected role skills; converge minimally to current lifecycle/gate semantics. |
| `template/.codex/critic.md` | Direct Codex Critic adapter | Uses Stage 0/0.5/1/2/3 as a parallel lifecycle and old stage naming while exposing the routed Critic’s functional verdict. | B — SUPPORTING / INCLUDE ONLY IF REQUIRED | `template/.agent/workflows/sdd-protocol.md`; `template/.agent/critic-gate.md` | Include only the terminology/gate clarification needed to make the adapter agree with current Critic procedure. |
| `template/.codex/instructions.md` | Direct Codex runtime instruction | Calls the main thread `Control Tower`, requires old Stage 0 preflight/Stage 0.5/Stage 1 mapping, and cites obsolete AGENTS authority labels. | B — SUPPORTING / INCLUDE ONLY IF REQUIRED | `AGENTS.md`; `governance/lifecycle.md`; `governance/authority.md` | Include the smallest lifecycle/authority correction because this instruction otherwise remains a live contradictory consumer. |
| `scripts/test-sdd-contract.sh` | Existing deterministic portable contract test | It checks Verifier vocabulary but does not protect the four role skills or direct adapters against the identified authority/lifecycle vocabulary drift. | B — SUPPORTING / INCLUDE ONLY IF REQUIRED | `skills/SKILL-CONVENTION.md`; current contract-test ownership | Extend narrowly; do not add a policy engine or scan reports/historical evidence. |
| `skills/codex-verification/SKILL.md`, `skills/subagent-mission-brief/SKILL.md`, `skills/context-snapshot/SKILL.md`, `skills/memory-bank-manager/SKILL.md`, `skills/merge-protocol/SKILL.md`, `skills/orchestrator-log/SKILL.md`, `skills/scoped-commit-guard/SKILL.md`, `skills/security-verification-gate/SKILL.md`, `skills/ssot-sync-closeout/SKILL.md` | Reusable but non-routed legacy procedures | Inventory found legacy Control Tower/stage terminology and, in several cases, project/runtime-specific procedure assumptions. They are not direct consumers required to make the four live role routes coherent. | C — FOLLOW-UP CANDIDATE | `skills/SKILL-CONVENTION.md`; `.agent/ROSTER.md` | Defer to bounded follow-up(s), grouped by trigger/consumer; do not turn WB-SKILL-001 into a shared-library rewrite. |
| `skills/agent-operations-review/SKILL.md`, `skills/architecture-discovery/SKILL.md`, `skills/impeccable/SKILL.md`, `skills/project-estimation/SKILL.md`, `skills/technical-discovery/SKILL.md`, `skills/taste-skill/SKILL.md`, `skills/theme-factory/SKILL.md`, `template/.claude/agents/solution-architect.md` | Non-critical reusable/design procedures | Search hits show old coordination terms or project/design-specific language, but no direct dependency from the four role routes was established in this inventory. | C — FOLLOW-UP CANDIDATE | `skills/SKILL-CONVENTION.md`; proportional-engineering rule in `AGENTS.md` | Defer; separately assess trigger/reuse boundary before any correction. |
| `docs/reports/**`, prior completed Work Blocks, research/evidence examples | Historical/evidence surfaces | Some truthful historical artifacts use the previous terminology. They are not current operational instructions. | D — HISTORICAL / NO CHANGE | `AGENTS.md` §6 | Preserve historical accuracy; do not run a terminology purge. |
| `.agent/ROSTER.md`, `.agent/workflows/sdd-protocol.md`, `template/.agent/workflows/sdd-protocol.md`, `template/.agent/critic-gate.md`, `governance/lifecycle.md`, `governance/artifacts.md`, `skills/SKILL-CONVENTION.md`, `skills/catalog.yml`, `template/.opencode/agents/**`, `runtimes/**` | Current framework contracts and adapters | These surfaces either contain the accepted lifecycle/verdict semantics or had no conflicting legacy hit in this inventory. In particular, `Stage 0` in the accepted lifecycle is a macro-stage label, not a competing lifecycle. | E — FALSE POSITIVE / KEEP | listed accepted contracts | No change in this Work Block. |

### Proposed Critical Write-Set

```text
skills/critic-review/SKILL.md
skills/scoped-coder/SKILL.md
skills/reviewer/SKILL.md
skills/verifier/SKILL.md
template/.claude/agents/critic.md
template/.claude/agents/scoped-coder.md
template/.claude/agents/reviewer.md
template/.claude/agents/verifier.md
```

### Proposed Supporting Write-Set (only because direct consistency requires it)

```text
template/.codex/AGENTS.md
template/.codex/critic.md
template/.codex/instructions.md
scripts/test-sdd-contract.sh
```

The exact twelve-path source write-set above received separate Critic review
(`SUPPLEMENT`, addressed by this synchronization) and Owner confirmation on
2026-08-19. It remains blocked only until the final independent consistency
recheck of this synchronized Work Block.

### Deferred Legacy Surfaces

- `skills/codex-verification/SKILL.md`
- `skills/subagent-mission-brief/SKILL.md`
- `skills/context-snapshot/SKILL.md`
- `skills/memory-bank-manager/SKILL.md`
- `skills/merge-protocol/SKILL.md`
- `skills/orchestrator-log/SKILL.md`
- `skills/scoped-commit-guard/SKILL.md`
- `skills/security-verification-gate/SKILL.md`
- `skills/ssot-sync-closeout/SKILL.md`
- `skills/agent-operations-review/SKILL.md`
- `skills/architecture-discovery/SKILL.md`
- `skills/impeccable/SKILL.md`
- `skills/project-estimation/SKILL.md`
- `skills/technical-discovery/SKILL.md`
- `skills/taste-skill/SKILL.md`
- `skills/theme-factory/SKILL.md`
- `template/.claude/agents/solution-architect.md`

Reason: each is non-critical to the routed Critic/Coder/Reviewer/Verifier path
or needs an independent trigger/reuse-boundary assessment. Including it now
would exceed the smallest sufficient corrective scope.

### False Positives / Intentionally Preserved Semantics

- The Critic functional verdict `APPROVE | SUPPLEMENT | RECONSIDER` is
  intentional and remains distinct from operational Critic gate state
  `READY | BLOCKED | SKIPPED | DEGRADED`. It is not an undocumented defect and
  must not be collapsed or removed.
- The accepted lifecycle’s macro labels may refer to Stage 0/1/2/3; the defect
  is a critical role skill or adapter inventing `Stage 0.5` or an alternate
  Plan/Implement/Verify authority flow rather than the current
  Define → Execute → Assure → Close semantics.
- Current roster, `.agent` workflow/gate, catalog/convention, OpenCode adapter,
  and runtime documentation surfaces are retained because they are already
  compatible or are not a demonstrated direct inconsistency.

### Proposed Deterministic Regression Check

Extend `scripts/test-sdd-contract.sh`; it already owns portable lifecycle and
direct-consumer assertions. The future extension should inspect only the four
routed critical role skills and their corrected direct adapters for: no
authority-bearing `Control Tower`; no `Stage 0.5`; no nonexistent Structural
Authority Model reference; Reviewer and Verifier current verdict vocabulary;
Coder’s absence of blanket normal-feature-branch Git prohibition; and existence
of any newly retained mechanically referenced helper path. It must not scan
historical reports or create a general-purpose policy engine.

### Provenance Plan

No historical provenance gap alone blocks Define. Before materially revising any
reusable skill, the Coder/Reviewer must record the primary provenance class,
source chain, local delta, and novelty claim according to
`governance/decision-provenance.md`. The current correction is derived from
local operating experience and accepted local governance; each changed shared
skill will state `original_experience_derived`, its internal evidence, the
convergence delta, and no novelty claim. No external source is asserted.

### Define Stop Conditions

Return for a new Work Block or Owner decision if: accepted governance itself
must change; any additional direct consumer requires a material new lifecycle or
authority design; the required adapter scope grows into general runtime
modernization; provenance requires an unavailable external source; a new
dependency/config/credential/deployment change is needed; or Define-quality,
Critic, review, or verification evidence cannot support the proposed source
write-set.

## Assurance Plan

### Critic

- **Required:** yes — Managed reusable role/governance-adjacent procedure change.
- **Inputs:** exact future write-set, this inventory, accepted contracts,
  provenance plan, and deterministic test design.
- **Report:** `docs/reports/reviews/wb-skill-001-critic.md`; functional verdict
  `SUPPLEMENT`. Its bounded Define requirements are addressed by this
  synchronization; it does not itself open the source Write Gate.

### Independent Review

- **Required:** yes.
- **Frozen diff:** future exact implementation subject.
- **Review dimensions:** role authority, lifecycle/verdict drift, runtime adapter
  coherence, scope discipline, provenance, and regression-test proportionality.
- **Expected report:** approved current review-report path.

### Technical Verification

- **Canonical checks:** `git diff --check`; `bash scripts/validate-governance.sh`;
  `bash scripts/test-sdd-contract.sh`; `python3 scripts/validate-release-state.py`;
  plus the focused changed-path checks justified by the final diff.
- **Runtime/browser/API/integration smoke:** not applicable unless the final
  adapter change introduces a mechanically testable runtime behavior.
- **Evidence expected:** command output and verifier report against frozen head.
- **Skipped checks:** no evaluation; any unavailable runtime proof must be
  labelled unverified rather than inferred.

### Agent Evaluation

- **Required:** no — deterministic procedure/documentation convergence only.
- **Evaluation ID / Plan:** not required.

### Specification Drift Audit

- **Required:** yes — role text must remain aligned with governance, workflow,
  roster, catalog, direct runtime adapters, and contract tests.
- **Expected report:** approved current drift-report path after implementation.

## Navigation and Documentation Impact

- **Files added/moved/removed:** Define evidence and coordination artifacts only;
  no source path is changed before the gate is READY.
- **PROJECT_MAP / FILE_REGISTRY update:** no; this is an in-progress plan and no
  active machine Work Block state is changed.
- **Runtime adapter update:** proposed only, listed above.
- **Engineering memory candidate:** no new durable memory in this Define run.

## Commit / Publication Scope

- **Files to stage:** none; staging is not currently authorized.
- **Files to leave unstaged:** `Repository Graph Evaluation Brief.md` and every
  changed path until a separate Owner instruction authorizes staging.
- **Commit/push approval:** neither is authorized.
- **Release/deploy approval:** not applicable.

## Execution Log

| Date | Stage | Function | Action / Decision | Evidence | Status |
|---|---|---|---|---|---|
| 2026-08-18 | Define | Orchestrator | Verified exact `main`/`origin/main`; preserved expected untracked brief; created local branch. | Git preflight | completed |
| 2026-08-18 | Define | Orchestrator | Read governing contracts and completed read-only repository-wide role-skill/direct-adapter inventory. | inventory above | completed |
| 2026-08-18 | Define | Orchestrator | Recorded source write gate as BLOCKED and proposed future bounded write-set only. | lifecycle state | completed |
| 2026-08-19 | Define | Requirements-quality Reviewer | Fresh re-review of the corrected specification completed with `READY`; it does not open a write gate. | `docs/reports/requirements/wb-skill-001-rereview.md` | completed |
| 2026-08-19 | Define | Critic | Separate read-only review returned functional verdict `SUPPLEMENT`: proceed after binding evidence, exact scope, and provenance. | `docs/reports/reviews/wb-skill-001-critic.md` | completed |
| 2026-08-19 | Define | Orchestrator | Bound Owner confirmation, exact twelve source paths, Critic disposition, provenance approach, and coordination/source-path distinction. | this synchronized Work Block | completed |
| 2026-08-19 | Define | Consistency Analyzer | Final read-only recheck returned `READY`; exact scope, evidence separation, provenance plan, and no-commit/no-push boundary align. | `docs/reports/requirements/wb-skill-001-consistency.md` | completed |
| 2026-08-19 | Execute | Orchestrator | Opened the bounded source Write Gate and assigned the sole Coder write-set. | lifecycle state and exact source list | in progress |

## Closeout

This Work Block is not closed. Source implementation is in progress; source
assurance, staging, commit, push, and PR creation have not been performed. The
next action is Coder implementation and scoped self-check inside the exact
twelve-path source write-set.
