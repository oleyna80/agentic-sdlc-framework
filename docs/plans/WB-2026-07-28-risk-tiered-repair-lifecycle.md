---
schema_version: 1
artifact_type: work_block
artifact_id: wb-009-risk-tiered-repair-lifecycle
work_block_id: wb-009
status: changes_required
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
| Governance profile for this WB | `Managed` — this changes framework contracts and CI gates |
| Target profile | `Controlled / Narrow Deterministic Repair` |
| Stage | Stage 1 — Execute |
| Execution state | `changes_required` |
| Base revision | `f83afc1041e5bd33bf9ef8f0c50dd8d29e5a72cb` |
| Implementation passes | one |
| Correction rounds | one for this WB; Integration Stabilization permits at most two |
| Source finding | HardwareLab pilot, merged PR #13 |

## Objective

Add a proportionate, fail-closed repair path to the framework. It must reduce
avoidable governance churn for deterministic compatibility repairs without
weakening the normal lifecycle, Hard Stops, required contracts, or the
independence of assurance.

The result is not a new top-level profile. **Narrow Deterministic Repair (NDR)**
is a submode of `Controlled`. **Integration Stabilization** is the bounded
execution envelope that may group sequentially discovered eligible repairs.

## Pilot Evidence

HardwareLab PR #13 was merged at
`72ada873d66d19de2609515b443766065fe132c9` after final head
`81b996238aee78766f2073e0b8e68bf291e675a7` passed Agent Guards, quality, E2E,
and Lighthouse checks.

The pilot found deterministic compatibility defects in sequence (lockfile, CI
Node runtime, skill-index classification). Existing controls caught them, but a
manual closeout counter reported four branch commits while the final branch had
five. That `4 -> 5` discrepancy is a pilot finding; it must not be repaired with
another HardwareLab evidence commit.

## Owner-Approved Contract

### Narrow Deterministic Repair

NDR is allowed only when every condition holds:

- the repair is deterministic and reversible;
- no architecture decision is required;
- no product, auth, security-boundary, public API, schema, data, deploy, or
  dependency-upgrade change is involved;
- the write-set is an exact path allowlist wholly within the approved
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
verification commands, and stop condition. One combined assurance report records
the logical review, deterministic verification, and final verdict. Separate
Critic, Review, Verification, and Drift documents are not required for an
eligible NDR; the reviewer/verifier boundary remains a different read-only
agent or session.

NDR permits one implementation pass and at most one correction round. A failed
eligibility condition or a second required correction moves work to an Owner
decision: accept residual risk, open another Work Block, change the
specification, or stop.

### Integration Stabilization

Integration Stabilization is an execution envelope, not a governance profile.
It may contain at most three sequentially discovered eligible repair items and
two correction rounds. Exceeding either limit requires an Owner decision.

Every item keeps an exact allowlist inside CI/bootstrap/runtime-validation. It
must not change product behavior, security, APIs, schemas, data, deployment, or
dependencies. The next newly visible deterministic compatibility defect remains
in the same envelope only while these conditions remain true; otherwise work
stops for Owner decision rather than silently creating a new gate cycle.

### CI and closeout evidence

- GitHub ruleset `19916164`, with required checks `contracts` and
  `release-state`, is the sole live merge authority for `main`.
- Provider-native required-check state is read live from GitHub and remains
  time-dependent; a later rerun may change it.
- A JSON provider snapshot is a portable point-in-time artifact with
  `authority: none`. It records the current `contracts` job identity and result
  as `PARTIAL`, or reports `UNVERIFIED` when that evidence cannot be bound.
- The snapshot does not block merge, replace or duplicate required checks,
  guarantee the absence of future reruns, or provide a final provider verdict.
- Dynamic Git/CI counters are never copied manually into tracked closeout files.
- An unknown path classification fails closed to the full suite.
- Required SDD, governance, publication, and release-state contracts always run.
- No `final-aggregator` is a merge gate. Historical aggregator results are
  non-required and non-authoritative.

## Exact Implementation Write-Set

Only the following paths may change during the one implementation pass. They are
inside framework governance, template/bootstrap, CI, or runtime-validation
surfaces; no product surface is admitted.

```text
.github/workflows/framework-contracts.yml
FILE_REGISTRY.yml
PROJECT_MAP.md
bootstrap/profiles.json
docs/plans/WB-2026-07-28-risk-tiered-repair-lifecycle.md
docs/profiles.md
governance/artifacts.md
governance/lifecycle.md
scripts/ci-contract-router.py                         (new)
scripts/test-ci-contract-router.py                    (new)
scripts/test-repair-lifecycle-contracts.py            (new)
scripts/test-sdd-contract.sh
scripts/validate_publication.py
template/AGENTS.md
template/FILE_REGISTRY.yml
template/PROJECT_MAP.md
template/.agent/workflows/sdd-protocol.md
template/docs/templates/closeout-report-template.md
template/docs/templates/combined-assurance-report-template.md (new)
template/docs/templates/repair-record-template.md     (new)
template/scripts/repair-lifecycle.py                  (new)
```

Assurance and closeout evidence may be written only at their canonical paths
under `docs/reports/` by the lifecycle roles after the implementation diff is
frozen. The provider-generated JSON snapshot is uploaded as a CI artifact and
is not committed.

## Explicitly Excluded

- `governance/release-state.md`, release-state validator/fixtures, and
  `.github/workflows/release-state-contract.yml`: the existing release-state
  workflow already runs on every push and pull request, and its repository vs
  mutable-hosting-state boundary remains correct.
- `.agent/active-work-block*.json`, runtime adapters, role definitions, and
  Hard Stop hooks: their existing schema can point the logical Review,
  Verification, and Drift fields to one combined report, so a schema migration
  would add risk without enforcement value.
- Any HardwareLab file or PR #13 alteration.
- Product code, security/auth controls, external APIs, schemas, data,
  deployments, secrets, and dependency upgrades.

## Implementation Tasks

| Task | Role | Paths | Expected evidence |
| --- | --- | --- | --- |
| Define NDR and Integration Stabilization | Coder | governance/docs/template protocol | eligibility and escalation contracts agree |
| Publish repair and assurance artifacts | Coder | template docs/scripts/bootstrap inventory | generated project contains deterministic tools |
| Implement CI routing/evidence | Coder | router/tests/workflow | unknown path selects full suite; snapshot records current `contracts` job as `PARTIAL` or `UNVERIFIED` |
| Freeze and assure | Reviewer/Verifier | read-only diff and CI artifact | one independent combined assurance verdict |

## Acceptance Criteria

1. NDR is a mechanically constrained `Controlled` submode, not a new profile.
2. An eligible repair has one record and one independent combined assurance
   report, with one implementation pass and one correction limit.
3. Integration Stabilization enforces three repair-item and two correction-round
   ceilings plus exact path allowlists and escalation.
4. Generated projects receive the required repair templates and validator through
   the installation manifest.
5. Unknown CI paths select the full suite; SDD, governance, publication, and
   release-state checks never skip.
6. The provider snapshot binds the current `Framework Contracts` / `contracts`
   job identity and result to the workflow run and PR head as time-bounded
   `PARTIAL` evidence, or reports `UNVERIFIED`. It has no merge authority; only
   ruleset-required `contracts` and `release-state` checks determine live merge
   readiness.
7. Normal Managed/Assured lifecycle and existing Hard Stops remain unchanged.

## Hard Stops and Stop Conditions

Stop for Owner decision if any proposed edit leaves the exact allowlist; requires
an architecture decision; changes a prohibited domain; adds a dependency; makes
the release-state workflow path-filtered; permits a required contract to skip;
or cannot preserve an independent assurance pass.

Stop after the stated correction limit rather than opening another unbounded
cycle. The allowed next decisions are: accept residual risk, change the
specification, open a separate Work Block, or stop the pilot.

## Verification Plan

Run locally before push:

```text
bash scripts/test-sdd-contract.sh
python scripts/test-repair-lifecycle-contracts.py
python scripts/test-ci-contract-router.py
python scripts/test-bootstrap-profiles.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
python scripts/validate-release-state.py
```

CI supplies the live ruleset-required `contracts` and `release-state` checks.
The non-required `provider-snapshot` job uploads time-bounded evidence only; it
is explicitly non-blocking and no final aggregator supplies a merge verdict. A
clean generated-project bootstrap remains included in Framework Contracts.

## Current State

WB-009.1 remains a historical `CHANGES_REQUIRED` result and its evidence is not
rewritten. WB-009.3 is `SUCCESS` on its separate durable branch and is not mixed
into PR #9. WB-009.2 is the only resumed repair scope. Parent WB-009 remains
`CHANGES_REQUIRED` until WB-009.2 completes and a final parent verification is
recorded; PR #9 must not be merged without separate Owner approval.
