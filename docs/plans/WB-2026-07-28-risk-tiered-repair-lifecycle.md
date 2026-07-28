---
schema_version: 1
artifact_type: work_block
artifact_id: wb-009-risk-tiered-repair-lifecycle
work_block_id: wb-009
status: completed
owner_role: orchestrator
created_at: 2026-07-28
last_verified: 2026-07-28
---

# WB-009 — Risk-tiered repair lifecycle and machine-derived closeout evidence

## Meta

| Field | Value |
| --- | --- |
| Work Block | `WB-009` |
| Owner | Repository Owner |
| Orchestrator | Codex |
| Governance profile | `Managed` — framework contracts and CI behavior |
| Target profile | `Controlled / Narrow Deterministic Repair` |
| Stage | Close |
| Execution state | `completed` |
| Current verdict | `READY` |
| Base revision | `f83afc1041e5bd33bf9ef8f0c50dd8d29e5a72cb` |
| Implementation passes | one |
| Correction accounting | one lifecycle correction plus Owner-authorized administrative publication corrections |
| Source finding | HardwareLab public pilot |

## Objective

Add a proportionate, fail-closed repair path to the framework. It reduces
avoidable governance churn for deterministic compatibility repairs without
weakening the normal lifecycle, Hard Stops, required contracts, or independent
assurance.

The result is not a new top-level profile. **Narrow Deterministic Repair (NDR)**
is a submode of `Controlled`. **Integration Stabilization** is its bounded
execution envelope for sequentially discovered eligible repairs.

## Delivered Contract

### Narrow Deterministic Repair

NDR is allowed only when every condition holds:

- the repair is deterministic and reversible;
- no architecture decision is required;
- no product, auth, security-boundary, public API, schema, data, deployment, or
  dependency-upgrade change is involved;
- the write-set is an exact path allowlist inside the approved
  CI/bootstrap/runtime-validation envelope;
- deterministic commands or lint fully verify the result; and
- risk is low or medium.

Lifecycle:

```text
Owner/Orchestrator scope decision
  -> one repair record
  -> one Coder implementation pass
  -> one independent read-only combined assurance pass
  -> CI
  -> machine-generated closeout summary
```

The repair record states the problem, root cause, allowlist, prohibited changes,
verification commands, and stop condition. One combined assurance report may
record logical review, deterministic verification, and final verdict. Separate
Critic, Review, Verification, and Drift documents are not required for an
eligible NDR, but assurance remains read-only and independent from implementation.

NDR permits one implementation pass and normally one correction round. Any
additional correction requires explicit Owner direction and must remain within
an exact administrative or implementation scope.

### Integration Stabilization

Integration Stabilization is an execution envelope, not a governance profile. It
may contain at most three sequentially discovered eligible repair items and two
correction rounds unless the Owner explicitly authorizes a narrower exception.

Every item keeps an exact allowlist inside CI/bootstrap/runtime-validation. It
cannot change product behavior, security, APIs, schemas, data, deployment, or
dependencies. A newly visible defect remains in the same envelope only while all
eligibility conditions remain true.

### CI and closeout evidence

- GitHub ruleset `19916164`, with required checks `contracts` and
  `release-state`, is the sole live merge authority for `main`.
- Required-check state is read live from GitHub and remains time-dependent.
- The JSON provider snapshot is point-in-time evidence with `authority: none`.
- It records the current `contracts` job identity and terminal result as
  `PARTIAL`, or reports `UNVERIFIED` when evidence cannot be bound.
- The snapshot cannot block merge, replace or duplicate required checks,
  guarantee the absence of future reruns, or provide a final provider verdict.
- Dynamic Git/CI counters are not manually copied as live closeout authority.
- Unknown path classification fails closed to the full suite.
- SDD, governance, publication, and release-state contracts always run.
- `final-aggregator` is removed and has no gate or verdict role.

## Implementation Scope

The implementation remained inside framework governance, template/bootstrap,
CI, and runtime-validation paths. It introduced or updated:

- governance for NDR and Integration Stabilization;
- repair-record and combined-assurance templates;
- generated-project repair lifecycle tooling;
- bootstrap and registry coverage;
- fail-closed CI routing;
- deterministic routing and repair-lifecycle fixtures;
- non-authoritative provider snapshot generation;
- parent and child review/verification evidence.

No product code, auth/security boundary, external API, schema, data, deployment,
secret, or dependency upgrade was included.

## Acceptance Result

- [x] NDR is a mechanically constrained `Controlled` submode.
- [x] Eligible repairs use one record, one implementation pass, deterministic
      checks, and independent assurance.
- [x] Integration Stabilization enforces bounded repair-item and correction
      accounting with Owner escalation.
- [x] Generated projects receive the repair templates and validator.
- [x] Unknown CI paths select the full suite.
- [x] Required SDD, governance, publication, and release-state contracts never
      skip.
- [x] Provider evidence binds the current `contracts` job result and identity as
      `PARTIAL`, or reports `UNVERIFIED`.
- [x] Provider evidence declares `authority: none` and no merge verdict.
- [x] Required checks remain the only live merge authority.
- [x] Checks API polling and `final-aggregator` are removed.
- [x] Publication-facing fixtures and evidence are project-neutral.
- [x] Framework Contracts and Release State Contract pass on the verified
      implementation revision.
- [x] Normal Managed/Assured lifecycle and Hard Stops remain unchanged.

## Evidence

- Child repair plan:
  `docs/plans/WB-009-2-provider-evidence-temporal-semantics.md`
- Independent review:
  `docs/reports/reviews/wb-009-2-provider-evidence-temporal-semantics.md`
- Verification:
  `docs/reports/verification/wb-009-2-provider-evidence-temporal-semantics.md`
- Workflow: `.github/workflows/framework-contracts.yml`
- Router: `scripts/ci-contract-router.py`
- Fixtures: `scripts/test-ci-contract-router.py`
- Verified implementation revision:
  `49b9f137c8e6f994bf169e56301ee4934c7f4537`
- Framework Contracts run 675: success
- Release State Contract run 242: success
- Provider artifact: `provider-contracts-snapshot-30393457599-1`

WB-009.1 remains historical evidence and is not rewritten. WB-009.3 remains a
separate durable branch result and is not mixed into the implementation diff.
The Owner-authorized WB-009.2 repair supplies the final provider-evidence
semantics used for this closeout.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic contract validation and provider checks are sufficient
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

Repository lifecycle and closeout evidence are aligned. Mutable hosting-platform
state and any external integration or merge action remain non-normative and
Owner-controlled.