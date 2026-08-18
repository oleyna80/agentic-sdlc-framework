---
schema_version: 1
artifact_type: work_block
artifact_id: wb-skill-001-role-skill-convergence
work_block_id: WB-SKILL-001
status: in_progress
owner_role: Owner
created_at: 2026-08-18
last_updated: 2026-08-18
governance_profile: Managed
branch: agent/wb-skill-001-role-skill-convergence
base_revision: 3ec044953a854dd8906a4849df507357bd3b87f0
write_gate: BLOCKED
critic_gate: PENDING
---

# WB-SKILL-001 — Framework-Native Role Skill Convergence

## Metadata

- **Work Block ID:** WB-SKILL-001
- **Title:** Framework-Native Role Skill Convergence
- **Date:** 2026-08-18
- **Owner:** Owner-authorized framework maintenance initiated in this conversation.
- **Owner role:** Owner
- **Orchestrator:** logical Orchestrator; Codex is currently bound only to Define inventory.
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

- **Current Stage:** Define
- **Stage State:** in_progress
- **Write Gate:** BLOCKED
- **Critic Gate:** PENDING
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation Verdict:** NOT_REQUIRED
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
- **Owner Approval Evidence:** this Owner instruction, limited to Define
  coordination and this Work Block path

### Define Quality Prerequisite

- **Required:** yes
- **Status:** PENDING
- **Requirements Review Evidence:** Historical round 1 —
  `docs/reports/requirements/wb-skill-001.md`; subject
  `83e6f7df063056a3c8c579bd518df17d279f6f6e`; evidence commit
  `97e7be5aa502d410a8636c32634e621c40c90801`; verdict
  `CHANGES_REQUIRED`; finding: specification authority wording required
  correction. This evidence is historical / superseded for current readiness
  purposes and is not passing evidence. Current state: **PENDING FRESH
  INDEPENDENT RE-REVIEW**.
- **Traceability Evidence:** PASS — `validate-define-traceability.py` against
  `docs/specs/wb-skill-001-role-skill-convergence.md`
  (`2e58550c1619bf690ebde36a54782e610f9fc072`) and
  `docs/tasklist/wb-skill-001-role-skill-convergence.md`
  (`348b9b924c47425b5c58ea6f64440157545c08b6`): READY
- **Consistency Analysis Evidence:** pending

No implementation/source write is authorized yet. Creating or updating this
Work Block is coordination work only. The Managed aggregate remains pending
until its required independent evidence bindings are established; this inventory
does not claim to open the source Write Gate.

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
- **Specification Status:** proposed; pending independent requirements-quality
  review.
- **Specification Revision:** local pending Define revision based on
  `da86496723ec9d4474181d366cf3761069a3def2` until this artifact set is committed.
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

- Managed Define-quality evidence bindings and a separate Critic review of the
  exact proposed source write-set.
- Owner approval of the exact source write-set after Critic disposition permits
  progression.
- Material-revision provenance for every reusable skill actually changed.

### May Resolve During Future Work

- Whether a mechanically checkable referenced helper exists in each corrected
  adapter. If an adapter cannot be made coherent within the bounded paths below,
  return to Define rather than broaden the write-set silently.

## Scope

### In Scope Now

- Create this Work Block and record a repository-wide read-only inventory.
- Define the future bounded corrective write-set, acceptance criteria, assurance
  model, and regression-test recommendation.

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

```text
docs/plans/wb-skill-001-role-skill-convergence.md
```

- **One Coder per write-set:** yes; this Define coordination write has no source
  implementation Coder.
- **Parallel writers:** no.
- **Scope guard:** `git status --short`, `git diff --check`, and changed-path
  validation before local commit.

The proposed future source write-set is recorded below only; it is not approved
for implementation and the source Write Gate remains BLOCKED.

## Risk and Authority

- **Side-Effect Class:** local-docs.
- **DB/Data Action Mode:** none.
- **Sensitive Domains:** governance procedure consistency.
- **Output Non-Determinism:** none; the subject is deterministic text and
  contract-test alignment.
- **Autonomous Tool/Trajectory Risk:** none in this Define run.
- **Threat Model Required:** no new threat model; future review must preserve
  existing authority and Hard Stop boundaries.
- **Rollback / Recovery:** revert only this known Work Block commit if Owner
  later directs it; no destructive action is authorized here.

## Hard Stops in Scope

- [x] Push, PR creation, merge, rebase, force push, branch deletion, and
  production/deployment/credential/destructive actions are forbidden.
- [x] Source skill, governance, runtime-hook, machine Work Block state, Spec
  Kit, and canonical aggregate changes are forbidden in this Define run.
- [ ] A local commit of this sole Work Block file is explicitly authorized by the
  Owner instruction after the stated validations; it does not authorize push.

## Function Bindings

| Function | Logical Role | Runtime | Isolation | Authority | Evidence |
|---|---|---|---|---|---|
| Orchestration | Orchestrator | Codex | same session | Define coordination only | this Work Block |
| Critic | Critic | not yet bound | not yet established | read-only | required before source Execute |
| Implementation | Coder | not yet bound | not yet established | no source write authority | future approved write-set only |
| Review | Reviewer | not yet bound | not yet established | read-only | required after source change |
| Verification | Verifier | not yet bound | not yet established | read-only | required after source change |
| Evaluation | not required | n/a | n/a | n/a | deterministic subject |

## Skills

- **Checked:** `skills/SKILL-CONVENTION.md`, `skills/catalog.yml`, and all
  relevant role/reusable skill surfaces in the inventory.
- **Matched / Used:** no external procedural skill was invoked; this is an
  Owner-scoped framework Define inventory.
- **Skipped:** implementation, Critic, independent review, and verification are
  deferred by the blocked source Write Gate.

## Define Requirements and Traceability

The authoritative behavioral requirements and measurable acceptance criteria
are `REQ-001` through `REQ-012` and `AC-001` through `AC-014` in
`docs/specs/wb-skill-001-role-skill-convergence.md`. The traceable proposed
implementation and assurance tasks are in
`docs/tasklist/wb-skill-001-role-skill-convergence.md`.

This Work Block is the implementation/assurance plan. The tasklist's source
paths are an inventory-derived candidate write-set, not a Critic-approved or
Owner-authorized implementation write-set.

## Implementation Plan

| Task | Owner Role | Write-Set | Dependencies | Expected Evidence | Status |
|---|---|---|---|---|---|
| Define inventory | Orchestrator | this Work Block only | baseline contracts | inventory below | completed in this revision |
| Critical role correction | one Coder | proposed A paths | Define quality, Critic, Owner approval | scoped diff/self-check | planned, blocked |
| Adapter/test coherence | same Coder | proposed B paths | approved critical design | focused test diff | planned, blocked |
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

The exact source write-set above is proposed, not approved. It must be reviewed
by a separate Critic, bound explicitly in the Work Block, and receive Owner
approval before Execute.

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
reusable skill, the future Coder/Reviewer must record the primary provenance
class, source chain, local delta, and novelty claim according to
`governance/decision-provenance.md`. The currently known correction is a
convergence to accepted local governance, not a novelty claim. Exact prior
source-history provenance is **unresolved pending the future material diff**;
it must be recorded as unresolved rather than fabricated if it cannot be
established confidently.

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
- **Expected report:** `docs/reports/reviews/wb-skill-001-critic.md` or an
  approved current reporting path, determined before source Execute.

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

- **Files added/moved/removed:** this Work Block only in Define.
- **PROJECT_MAP / FILE_REGISTRY update:** no; this is an in-progress plan and no
  active machine Work Block state is changed.
- **Runtime adapter update:** proposed only, listed above.
- **Engineering memory candidate:** no new durable memory in this Define run.

## Commit / Publication Scope

- **Files to stage:** `docs/plans/wb-skill-001-role-skill-convergence.md` only,
  after the stated validation passes or its documented result is understood.
- **Files to leave unstaged:** `Repository Graph Evaluation Brief.md` and every
  path outside the single coordination file.
- **Commit/push approval:** local commit explicitly approved by this instruction;
  push is not approved.
- **Release/deploy approval:** not applicable.

## Execution Log

| Date | Stage | Function | Action / Decision | Evidence | Status |
|---|---|---|---|---|---|
| 2026-08-18 | Define | Orchestrator | Verified exact `main`/`origin/main`; preserved expected untracked brief; created local branch. | Git preflight | completed |
| 2026-08-18 | Define | Orchestrator | Read governing contracts and completed read-only repository-wide role-skill/direct-adapter inventory. | inventory above | completed |
| 2026-08-18 | Define | Orchestrator | Recorded source write gate as BLOCKED and proposed future bounded write-set only. | lifecycle state | completed |

## Closeout

This Work Block is not closed. Source implementation, source assurance, push,
and PR creation have not been performed. The next action is a separate Critic
review of the exact proposed source scope after Managed Define-quality evidence
is resolved as applicable.
