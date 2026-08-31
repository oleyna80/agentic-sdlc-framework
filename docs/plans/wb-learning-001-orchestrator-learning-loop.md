---
schema_version: 1
artifact_type: work_block
artifact_id: wb-learning-001-orchestrator-learning-loop
work_block_id: WB-LEARNING-001
status: in_progress
owner_role: orchestrator
created_at: 2026-08-31
base_revision: 73cd1cab36af327683991c768ea887911547df06
branch: agent/wb-learning-001-orchestrator-learning-loop
governance_profile: Managed
verification_tier: Standard
---

# WB-LEARNING-001 — Orchestrator Learning Loop

## Owner Approval

Owner approved Define and the exact 12-path implementation write-set on 2026-08-31. This authorizes routine reversible branch implementation and assurance inside the approved Work Block. It does not authorize merge, release, deployment, destructive Git operations, or changes to `WB-RELEASE-002`.

## Objective

Implement the approved `docs/specs/orchestrator-learning-loop.md` contract so non-trivial Close systematically reviews lifecycle findings, classifies reusable knowledge, promotes durable lessons without a separate Owner reminder when the required memory path is already approved, and propagates the mechanism to fresh generated projects.

## Isolation

- Base: `main@73cd1cab36af327683991c768ea887911547df06`.
- Work branch: `agent/wb-learning-001-orchestrator-learning-loop`.
- Explicitly excluded: `agent/wb-release-002-candidate-promotion`, its commits/write-set/release-state work, and cleanup/residual work.
- `docs/engineering-memory/lessons-learned.md` is excluded from this WB; branch `agent/engineering-memory-lessons-2026-08-31@8fb9e2e5df6a74098862240dccd9d72782be37c7` remains independent.

## Exact Implementation Write-Set

```text
governance/lifecycle.md
.agent/workflows/sdd-protocol.md
template/.agent/workflows/sdd-protocol.md
skills/ssot-sync-closeout/SKILL.md
.opencode/skills/ssot-sync-closeout/SKILL.md
framework/memory/project-engineering-memory.md
template/docs/engineering-memory/README.md
template/docs/engineering-memory/lessons-learned.md
template/docs/templates/work-block-template.md
template/docs/templates/closeout-report-template.md
bootstrap/profiles.json
scripts/test-sdd-contract.sh
```

No implementation path outside this list may be changed without returning to Define and obtaining a revised Owner decision.

## Architecture

1. `governance/lifecycle.md` owns the short runtime-neutral MUST-level Close invariant.
2. Self-hosting and portable SDD workflows own the stage-by-stage learning-review procedure.
3. `ssot-sync-closeout` owns operational classification/dedup/promotion steps.
4. Engineering Memory contract owns eligibility, record shape, authority and project/framework boundary.
5. Portable lessons starter + bootstrap required path provide cross-project propagation.
6. Work Block/closeout templates make authority and learning-review evidence explicit without adding new machine lifecycle state.
7. `scripts/test-sdd-contract.sh` provides deterministic semantic/parity regression checks.

## Risks / Mitigations

- **Lesson spam:** require material future-use impact, evidence, and deduplication; `none identified` is valid.
- **Implicit permission expansion:** classification never grants write authority; pre-authorize exact closeout memory path or return to Define.
- **Framework contamination:** project lessons stay project-local; framework promotion needs a separate WB.
- **Runtime drift:** canonical procedure stays runtime-neutral; OpenCode mirror is checked for semantic parity.
- **Process bloat:** no new lifecycle state, hook, daemon, or validator schema in this WB.

## Assurance Plan

- Requirements quality: required and recorded under `docs/reports/requirements/`.
- Define consistency: repository-grounded analysis completed before Owner approval.
- Critic: required; same-context Define Critic recorded, plus post-implementation read-only review.
- Reviewer: read-only review of frozen implementation subject.
- Verifier: deterministic contract/bootstrap/governance/publication checks.
- Evaluation: NOT_REQUIRED; behavior is a deterministic documentation/bootstrap contract change.
- Drift: required because Governance Core and portable lifecycle semantics change.

Canonical verification commands:

```text
bash scripts/test-sdd-contract.sh
python3 scripts/test-bootstrap-profiles.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
git diff --check
```

## Lifecycle State

- Define: READY / Owner approved.
- Write Gate: READY for the exact implementation write-set above.
- Execute: in progress.
- Assure: pending.
- Close: pending.
