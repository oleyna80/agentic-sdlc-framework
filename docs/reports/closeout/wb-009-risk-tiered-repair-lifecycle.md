---
schema_version: 1
artifact_type: closeout_report
artifact_id: wb-009-risk-tiered-repair-lifecycle-closeout
status: approved
owner_role: orchestrator
work_block_id: wb-009
subject_revision: 49b9f137c8e6f994bf169e56301ee4934c7f4537
created_at: 2026-07-28
last_verified: 2026-07-28
---

# WB-009 Closeout — Risk-Tiered Repair Lifecycle and Provider Evidence

- **Stage execution state:** completed
- **Review verdict:** READY
- **Verification verdict:** READY
- **Evaluation verdict:** SKIPPED — deterministic contract validation and provider checks are sufficient
- **Drift verdict:** ALIGNED
- **Closeout classification:** SUCCESS
- **Task status:** completed
- **External VCS state:** non-normative; read from the hosting platform when needed

## Result

WB-009 adds a bounded Narrow Deterministic Repair submode to the Controlled
profile and an Integration Stabilization envelope for sequential deterministic
CI/bootstrap/runtime-validation repairs. The framework now supports
proportionate repair governance without weakening normal Managed/Assured
lifecycle controls.

Provider evidence is explicitly separated from live authority. Repository
required checks remain the only live hosting-platform gate, while the uploaded
snapshot records one current workflow job as time-bounded evidence with
`authority: none`.

## Delivered Changes

- defined NDR eligibility, exact allowlists, stop conditions, and correction
  accounting;
- defined Integration Stabilization as a bounded execution envelope rather than
  a new governance profile;
- added repair-record and combined-assurance templates;
- added generated-project repair lifecycle validation;
- integrated repair tooling into bootstrap manifests and navigation;
- added fail-closed targeted/full CI routing;
- preserved always-required SDD, governance, publication, and release-state
  validation;
- replaced Checks API polling with deterministic current-job snapshot capture;
- recorded PR head SHA and workflow SHA separately;
- emitted `PARTIAL` for bound terminal current-job evidence and `UNVERIFIED` for
  incomplete evidence;
- declared snapshot `authority: none`, point-in-time semantics, current-job-only
  coverage, and explicit limitations;
- removed `final-aggregator` and its false final-verdict semantics;
- anonymized publication-facing fixtures and historical evidence references.

## Enforced Invariants

- NDR does not admit product, auth/security-boundary, public API, schema, data,
  deployment, secret, or dependency-upgrade changes;
- every repair uses an exact path allowlist and deterministic verification;
- assurance remains read-only and independent from implementation;
- unknown CI paths fail closed to the full suite;
- required contract families always run;
- provider snapshot failure cannot become a required gate;
- provider evidence cannot replace, duplicate, or override required checks;
- provider evidence cannot claim a final hosting-platform verdict;
- incomplete identity or result cannot become a false pass;
- publication artifacts remain project-neutral;
- external hosting-platform state does not become repository lifecycle authority.

## Evidence

- Work Block: `docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md`
- Provider repair plan:
  `docs/plans/WB-009-2-provider-evidence-temporal-semantics.md`
- Independent review:
  `docs/reports/reviews/wb-009-2-provider-evidence-temporal-semantics.md`
- Verification:
  `docs/reports/verification/wb-009-2-provider-evidence-temporal-semantics.md`
- Workflow: `.github/workflows/framework-contracts.yml`
- Router: `scripts/ci-contract-router.py`
- Router fixtures: `scripts/test-ci-contract-router.py`
- Verified implementation revision:
  `49b9f137c8e6f994bf169e56301ee4934c7f4537`
- Framework Contracts run 675: success
- Release State Contract run 242: success
- Provider snapshot artifact:
  `provider-contracts-snapshot-30393457599-1`

Earlier failed and corrective runs remain historical evidence with their actual
outcomes. No failed result is relabelled as successful evidence.

## Acceptance Result

- [x] NDR is a Controlled submode, not a top-level profile.
- [x] Eligibility and prohibited domains are mechanically bounded.
- [x] Repair and combined-assurance templates are installed into generated
      projects.
- [x] Integration Stabilization has bounded item and correction accounting.
- [x] Unknown paths select full validation.
- [x] Required contract families never skip.
- [x] Snapshot captures current job identity/result and exact subject identity.
- [x] Missing evidence becomes `UNVERIFIED`.
- [x] Snapshot states `authority: none` and no final verdict.
- [x] Snapshot capture is non-required and non-blocking.
- [x] Checks API polling and aggregate verdict logic are absent.
- [x] Publication validation accepts the final fixture/evidence set.
- [x] Independent review and verification are READY.
- [x] Repository Work Block, registry, map, and closeout are synchronized.
- [x] No active implementation Work Block remains.

## Residual Risks and Limitations

- Provider snapshot evidence remains point-in-time and may not describe later
  hosting-platform reruns or state changes.
- The artifact covers only the current `contracts` workflow job and is not a
  complete representation of repository authority.
- NDR eligibility depends on exact classification; ambiguous or architectural
  repairs must escalate rather than enter the narrow path.
- CI and runtime hooks are governance controls, not an operating-system security
  boundary.
- Live provider authentication, runtime isolation, telemetry, plugin/MCP
  admission, and production behavior remain outside WB-009.

## Follow-Up Work

1. exercise NDR on additional public deterministic repair pilots;
2. measure whether repair-record and combined-assurance flows reduce cycle time
   without increasing escaped defects;
3. define provider-neutral run-ledger and observability contracts;
4. keep hosting-platform integration actions subject to explicit Owner direction.

## Final Decision

WB-009 satisfies repository `success-closeout`. The repository lifecycle is
complete and internally consistent. External hosting-platform actions remain
separate, non-normative Owner decisions.