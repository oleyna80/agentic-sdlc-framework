# WB-CORE-003H — Self-hosting workflow authority reconciliation

## Metadata

- **Work Block ID:** WB-CORE-003H
- **Date:** 2026-08-15
- **Owner:** Owner instruction in current session
- **Orchestrator:** ChatGPT / Orchestrator
- **Governance Profile:** Controlled
- **Execution Mode:** orchestrator
- **Verification Tier:** standard
- **Evaluation Required:** no; deterministic governance/documentation reconciliation

## Lifecycle State

- **Current Stage:** Assure
- **Stage State:** in_progress
- **Write Gate:** READY
- **Critic Gate:** SKIPPED; permitted for bounded low-risk Controlled work
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation Verdict:** NOT_REQUIRED
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
- **Implementation Result:** DONE; implementation write-set frozen pending CI and independent re-review
- **Owner Approval Evidence:** current-session approval: “Подтверждаю. Делай”

## Objective

Reconcile the framework self-hosting workflow with the canonical authority model so it no longer classifies normal reversible Git development operations as unconditional Hard Stops.

## Expected Final Result

`.agent/workflows/sdd-protocol.md` remains subordinate to `AGENTS.md` and `governance/`, stops for genuine scope/authority/risk/evidence/consequential boundaries, and explicitly leaves staging, local commits, and normal feature-branch pushes available inside an approved Work Block/write-set.

## Scope

### In Scope

- `.agent/workflows/sdd-protocol.md`
- `scripts/test-sdd-contract.sh`
- this Work Block

### Out of Scope

- portable `template/.agent/workflows/sdd-protocol.md`
- `AGENTS.md`
- `governance/authority.md` or `governance/lifecycle.md`
- runtime adapters, hooks, CI architecture, deployment/release behavior
- PR #38

## Write-Set

```text
.agent/workflows/sdd-protocol.md
scripts/test-sdd-contract.sh
docs/plans/wb-core-003h-self-hosting-authority-reconciliation.md
```

One Coder owns the write-set. No parallel writers.

## Risk and Authority

- **Side-Effect Class:** public-repo, governance-semantic documentation/test contract
- **DB/Data Action Mode:** none
- **Sensitive Domains:** governance only
- **Threat Model Required:** no; no security-boundary weakening intended
- **Rollback / Recovery:** revert the branch commits before merge

No production, live-data, secret, destructive Git, protected-branch direct mutation, release, or client-facing action is in scope.

The Work Block uses the `Controlled` profile because it is one bounded reversible implementation with an explicit write-set and deterministic contract verification. It is not using Narrow Deterministic Repair or Quick Fix, and no governance exception is required for the skipped Critic gate.

## Implementation Plan

1. Replace the stale blanket stop rule in the root self-hosting workflow with canonical scope/authority/risk/evidence/consequential stop semantics.
2. Explicitly preserve normal reversible staging/local-commit/feature-branch-push behavior inside approved scope.
3. Add one targeted deterministic regression contract to the existing `scripts/test-sdd-contract.sh`; do not add a validator or new test framework.
4. Run existing Framework Contracts and Release State Contract in the Draft PR.
5. Freeze the head and obtain independent read-only review before merge.

## Acceptance Criteria

- Root workflow no longer contains an unconditional `staging, commit, or push` stop.
- Root workflow does not treat configuration/hooks/CI/runtime work as a Hard Stop by category alone.
- Root workflow remains subordinate to `AGENTS.md` and `governance/`.
- Normal reversible development operations inside an approved Work Block/write-set are explicitly compatible with staging, local commits, and normal feature-branch pushes.
- Consequential external actions and material scope/authority/risk changes still stop/escalate.
- Existing contract suite deterministically protects the corrected invariant without new validation machinery.
- CI is green on the frozen head and independent review reports no unresolved MATERIAL/BLOCKER finding.

## Assurance Plan

Independent review is required because this changes self-hosting governance semantics. Technical verification is the existing contract/CI suite. Evaluation is not required. A specification-drift audit is satisfied by explicit comparison of the root workflow against canonical `AGENTS.md`, `governance/authority.md`, and `governance/lifecycle.md` semantics.

### Independent Review History

- Cycle 1 on frozen head `f82a6e4d47b8f49459531aa7165954fd2ca02e77`: `CHANGES_REQUIRED` solely because the Work Block declared `Managed` while recording `Critic Gate: SKIPPED` without an explicit governance exception.
- Disposition: corrected the Work Block classification to `Controlled`, which matches the bounded low-risk execution actually performed and permits a skipped Critic gate under the self-hosting protocol. Implementation files were not changed by this correction.
- Independent re-review is required on the new frozen head.

## Commit / Publication Scope

Normal feature-branch commits/pushes and Draft PR creation are approved as part of this Work Block. Merge remains Owner-controlled after assurance.
