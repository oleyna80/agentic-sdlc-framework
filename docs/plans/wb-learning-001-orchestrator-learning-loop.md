---
schema_version: 1
artifact_type: work_block
artifact_id: wb-learning-001-orchestrator-learning-loop
work_block_id: WB-LEARNING-001
status: completed
owner_role: orchestrator
created_at: 2026-08-31
base_revision: 73cd1cab36af327683991c768ea887911547df06
branch: agent/wb-learning-001-orchestrator-learning-loop
governance_profile: Managed
verification_tier: Standard
implementation_subject: 65cba2a107ab2cbd8d8eb0437d8dfe392e8200e0
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

The frozen implementation comparison from Define coordination commit `037c886fd98b3217ad990ffc4769696ef2a258f1` to implementation subject `65cba2a107ab2cbd8d8eb0437d8dfe392e8200e0` contains exactly these 12 paths.

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

## Assurance Evidence

- Requirements quality: `docs/reports/requirements/wb-learning-001-requirements-quality.md` — READY.
- Define Critic: `docs/reports/reviews/wb-learning-001-critic.md` — APPROVE, same-context read-only.
- Implementation Review: `docs/reports/reviews/wb-learning-001-implementation-review.md` — READY, same-context read-only.
- Verification: `docs/reports/verification/wb-learning-001-verification.md` — READY; provider-native deterministic CI bound to exact implementation SHA.
- Drift: `docs/reports/drift/wb-learning-001-drift.md` — ALIGNED, same-context read-only.
- Evaluation: NOT_REQUIRED; deterministic governance/template/bootstrap contract change.
- Framework Contracts run `33431711019` / #1342 on implementation subject — success.
- Release State Contract run `33431711049` / #926 on implementation subject — success; compatibility evidence only, no release-state ownership.
- Provider snapshot artifact `provider-contracts-snapshot-33431711019-1`, ID `9772898082`, digest `sha256:6255ccfc6a514263741c6b085589944a519829de3f97de15e8214a266fb89ae6`.

## Learning Review

Lifecycle stages reviewed: Define, Execute, Assure, Close.

| Candidate | Evidence / effect | Disposition |
| --- | --- | --- |
| Classification must not become write authority | Define found that default coordination authority excludes `docs/engineering-memory/**`; the design now requires pre-authorized target or return to Define | `not-applicable` to separate Engineering Memory promotion because the principle is now an explicit normative requirement of this WB |
| Line-oriented contract assertion vs Markdown wrapping | First PR CI captured `FAIL: .agent/workflows/sdd-protocol.md missing contract pattern: Define, Execute, Assure, and Close`; wording was made line-verifiable and final full suite passed | `operational-only`; one observed testability defect, insufficient recurrence evidence for a new durable lesson |

Overall Engineering Memory classification: `operational-only`.

No `docs/engineering-memory/` mutation is authorized or required by this closeout. No automatic project-to-framework promotion is performed.

## Lifecycle State

- Define: READY / Owner approved.
- Write Gate: CLOSED; implementation subject frozen.
- Execute: completed.
- Review Gate: READY.
- Verification Verdict: READY.
- Evaluation Verdict: NOT_REQUIRED.
- Drift Gate: READY / ALIGNED.
- Closeout Mode: success-closeout, subject to final terminal-state CI and closeout evidence-only persistence.
- Task Status: completed.
- Merge / release / deployment: not authorized by this Work Block closeout.
