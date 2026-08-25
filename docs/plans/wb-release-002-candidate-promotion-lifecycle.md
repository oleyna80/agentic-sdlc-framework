---
schema_version: 1
artifact_type: work_block
artifact_id: wb-release-002-candidate-promotion-lifecycle
work_block_id: WB-RELEASE-002
status: in_progress
owner_role: Owner
created_at: 2026-08-25
last_updated: 2026-08-25
governance_profile: Managed
branch: agent/wb-release-002-candidate-promotion
base_revision: 73cd1cab36af327683991c768ea887911547df06
write_gate: BLOCKED
critic_gate: PENDING
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
evaluation_verdict: NOT_REQUIRED
closeout_mode: pending
owner_approval: Owner authorized Define-only investigation for WB-RELEASE-002 on 2026-08-25. This does not authorize source changes, canonical projection changes, commit, push, pull request, merge, or thread resolution.
---

# WB-RELEASE-002 — Sequential Candidate Promotion and Next-Candidate Lifecycle

## Stage and objective

- **Current Stage:** Define
- **Stage State:** in_progress
- **Role:** Orchestrator → Architect
- **Objective:** define a truthful, fail-closed transition from an evidence-complete `pre_closeout_candidate` to the next candidate without discarding effective completion history or weakening ordinary release-state validation.

## Context and confirmed trigger

The accepted WB-RELEASE-001 contract supports one local `pre_closeout_candidate` and derives effective completion only after four exact evidence artifacts bind the candidate. It does not specify how that effective candidate is promoted or archived before another candidate is declared. The WB-CORE-003G pilot exposed the resulting sequencing gap: adding a next Work Block to the raw completed list while the prior candidate declaration remains active violates the predecessor invariant.

This Define run investigates the transition only. It does not repair WB-CORE-003G, change WB-RELEASE-001, or implement a validator.

## Expected final result

An approved future specification and implementation plan define one serial candidate lifecycle with explicit promotion prerequisites, durable effective-completion history, exact predecessor binding, and a fail-closed next-candidate transition. Historical raw records remain truthful; no evidence or Owner decision is fabricated.

## Done criteria for Define

- [ ] Current release-state candidate and completed-record inventory is evidence-backed.
- [ ] Historical impact of candidate promotion options is classified.
- [ ] A prospective invariant scope and transition model are selected.
- [ ] Future implementation owners and smallest proposed write-set are recorded.
- [ ] Requirements, acceptance criteria, and tasklist are structurally traceable.
- [ ] Requirements review, consistency analysis, and Critic remain pending until their separate read-only stages.

## Normative baseline

- **Release-state contract:** `governance/release-state.md`
- **Lifecycle contract:** `governance/lifecycle.md`
- **Artifact authority contract:** `governance/artifacts.md`
- **Authority contract:** `governance/authority.md`
- **SDD protocol:** `.agent/workflows/sdd-protocol.md`
- **Machine state:** `FILE_REGISTRY.yml`
- **Human projection:** `PROJECT_MAP.md`
- **Existing candidate Work Block:** `docs/plans/wb-release-001-closeout-sequencing-reconciliation.md`
- **Existing candidate specification:** `docs/specs/wb-release-001-closeout-sequencing-reconciliation.md`
- **Existing candidate tasklist:** `docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md`

## Baseline and repository preflight

- **Base revision:** `73cd1cab36af327683991c768ea887911547df06`
- **Branch:** `agent/wb-release-002-candidate-promotion`
- **Expected tracked state:** clean at the baseline.
- **Pre-existing untracked file:** `Repository Graph Evaluation Brief.md`; out of scope and untouched.
- **Define-only authorized files:** the three WB-RELEASE-002 artifacts created by this Work Block.

## Scope

### In scope

- read-only analysis of candidate promotion, effective completion, and next-candidate sequencing;
- repository-wide inventory of completed Work Blocks and explicit separate-specification bindings;
- requirements and acceptance criteria for a prospective serial transition;
- a proposed, not authorized, implementation write-set.

### Out of scope

- changing `governance/release-state.md`, validators, fixtures, `FILE_REGISTRY.yml`, or `PROJECT_MAP.md`;
- changing WB-RELEASE-001, WB-CORE-003G, or any historical Work Block;
- source implementation, GitHub mutation, commit, push, PR, merge, rebase, or thread resolution;
- Gemini recommendations, converge loops, extensions, presets, workflows, bundles, or unrelated governance redesign.

## Historical impact inventory

The current baseline has 29 paths in `migration_state.completed_work_blocks` and one candidate declaration. Explicit formal profiles and separate specifications are recorded below; older records that omit those fields are not inferred.

| WB | Profile | Separate Spec | Spec Status | Completed | Would serial-candidate invariant fail? | Disposition |
|---|---|---|---|---|---|---|
| WB-RELEASE-001 | Managed | `docs/specs/wb-release-001-closeout-sequencing-reconciliation.md` | approved | effective only; not raw completed | yes, it is the active candidate that requires promotion semantics | design transition; preserve its evidence and effective history |
| WB-SKILL-002B | Managed | `docs/specs/wb-skill-002b-provider-guard-boundaries.md` | approved | yes, raw latest | no | remains the raw predecessor of the current candidate |
| WB-SKILL-002A | Managed | `docs/specs/wb-skill-002a-post-merge-reconciliation.md` | approved | yes | no | historical completed record remains unchanged |
| WB-SKILL-002 | Managed | `docs/specs/wb-skill-002-provider-neutral-verifier.md` | approved prospectively; historical closeout deviation recorded | yes | no new transition failure | historical truth is preserved |
| WB-SKILL-001 | Managed | `docs/specs/wb-skill-001-role-skill-convergence.md` | approved | yes | no | conforms to existing completed state |
| WB-REPO-GRAPH-001 | Managed | binding not explicitly declared; a spec path appears in a write-set | approved if resolved | yes | unverified; do not infer | no retroactive binding |
| 19 earlier completed records | unverified | unverified | unverified | yes | unverified | no profile/spec binding is inferred from legacy prose |
| WB-CORE-003G pilot projection | not on baseline `main` | not on baseline `main` | not applicable | no | not applicable | do not mutate or register from this Define branch |

**Historical impact classification: BOUNDED COLLATERAL IMPACT.** The direct impact is the one active evidence-complete candidate; older records lack sufficient structured metadata for a safe retroactive rule. The proposed invariant is therefore prospective and transition-scoped, not a rewrite of all historical Work Blocks.

## Candidate transition design decision to resolve

The Define recommendation is a separate promotion contract (option d) with prospective effect:

1. retain exactly one active `pre_closeout_candidate`;
2. require the existing evidence-persistence proof and unchanged normative manifest before promotion;
3. persist an immutable, evidence-bound record of the promoted candidate in an effective-completion history or equivalent canonical machine state;
4. only then replace the candidate declaration with a next candidate whose predecessor is the raw latest completed Work Block under the chosen state model;
5. keep ordinary mode fail-closed when any candidate is incomplete, ambiguous, duplicated, or missing evidence.

The implementation design must compare a durable promotion ledger with an alternative that promotes into `completed_work_blocks`; it must not silently turn derived completion into a false raw historical fact.

## Proposed future implementation write-set (not authorized)

| Path | Owner / defect | Smallest sufficient future change | Why no smaller owner exists |
|---|---|---|---|
| `governance/release-state.md` | Architect; missing serial promotion semantics | define promotion prerequisites, effective-history representation, and next-candidate ordering | current contract has no normative transition to the next candidate |
| `scripts/validate-release-state.py` | deterministic release-state owner | validate one-candidate serialization, promotion evidence/manifest binding, and predecessor continuity | only this validator can enforce the machine invariant |
| `scripts/test-release-state-contracts.py` | contract fixture owner | add positive, incomplete, duplicate, stale-manifest, and next-candidate fixtures | regression proof belongs beside the validator |
| `FILE_REGISTRY.yml` | machine projection, only if a promotion ledger field is selected | persist the canonical promoted-candidate history and next candidate state | required only if the chosen state cannot be represented by existing fields |
| `PROJECT_MAP.md` | human projection, only if registry shape changes | mirror the same promotion/history state | required to keep the documented projection synchronized |
| `.agent/workflows/sdd-protocol.md` | lifecycle procedure, only if needed after design | add the operational Close transition step | no smaller owner if the transition is procedural rather than only release-state policy |

No path above is authorized in this Define run.

## Define quality state

- **Required:** yes — Managed formal specification.
- **Requirements Review:** PENDING.
- **Traceability:** PENDING until structural validation runs.
- **Consistency Analysis:** PENDING.
- **Aggregate:** PENDING.

## Gates and authority

- **Write Gate:** BLOCKED.
- **Critic Gate:** PENDING.
- **Review Gate:** PENDING.
- **Verification Verdict:** PENDING.
- **Drift Gate:** PENDING.
- **Evaluation Verdict:** NOT_REQUIRED — deterministic governance/release-state lifecycle design introduces no non-deterministic product behavior.
- **Closeout Mode:** pending.

## Acceptance criteria

- [ ] AC-001 [req=REQ-001]: The inventory distinguishes raw completed state, effective completion derived from bound evidence, and the active candidate without inferring missing historical metadata.
- [ ] AC-002 [req=REQ-002]: The specification records an evidence-backed transition that preserves WB-RELEASE-001 effective completion before any next candidate is declared.
- [ ] AC-003 [req=REQ-003]: The future state model permits exactly one active candidate and an explicit deterministic predecessor for each candidate.
- [ ] AC-004 [req=REQ-004]: Promotion is permitted only after all required evidence binds the exact candidate and its normative manifest remains unchanged.
- [ ] AC-005 [req=REQ-005]: Ordinary validation remains fail-closed for incomplete, duplicated, malformed, stale, or concurrently active candidate state.
- [ ] AC-006 [req=REQ-006]: Promoting a candidate retains immutable evidence and does not rewrite raw historical Work Block facts.
- [ ] AC-007 [req=REQ-007]: The design is prospective and does not register or mutate the WB-CORE-003G pilot projection from this branch.
- [ ] AC-008 [req=REQ-008]: Every proposed source path has one owning contract, a smallest sufficient change, and a recorded reason; no future path is pre-authorized.
- [ ] AC-009 [req=REQ-009]: The future validator design includes deterministic positive and adversarial fixtures for sequential promotion and next-candidate declaration.

## Assumptions and unresolved Owner decisions

- The current Owner fact is only authorization for Define investigation; no Execute or source-write authority is implied.
- The future design must choose whether the promoted effective history is a new registry field or a separate canonical artifact. That choice is material and remains unresolved until requirements review/Owner approval.
- Historical records without structured profile/specification fields remain `UNVERIFIED`; no historical compliance claim is made.

## Implementation plan

| Task | Owner Role | Write-Set | Dependencies | Expected Evidence | Status |
|---|---|---|---|---|---|
| Define inventory, transition alternatives, requirements, and proposed write-set | Architect | three WB-RELEASE-002 Define artifacts | current main and governing contracts | specification, plan, tasklist | in_progress |
| Requirements-quality review | Requirements Reviewer | read-only report path | Define artifacts | independent requirements verdict | planned |
| Consistency analysis | Architect/Reviewer | read-only report path | requirements review | spec/plan/task consistency report | planned |
| Critic review | Critic | read-only report path | Define quality evidence | Critic verdict | planned |
| Future Execute | Coder | only later Owner-approved write-set | approved specification and gates | implementation and tests | blocked |

