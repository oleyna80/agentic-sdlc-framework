---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003e-closure-evidence-correction
work_block_id: WB-CORE-003E
status: in_progress
owner_role: orchestrator
created_at: 2026-08-03
base_revision: 0f616a2343d18be9cefc7276f3a72bddad10635d
branch: agent/wb-core-003d-parallel-write-set-orchestration
process_level: Managed
---

# WB-CORE-003E — WB-CORE-003D Closure Evidence Correction

## Objective and authority

Resolve the two PR-review findings against WB-CORE-003D without reopening its
parallel-write-set design or changing its runtime-neutral protocol. This is a
new, bounded corrective Work Block because the required correction to the
WB-CORE-003D tasklist changes a path in that Work Block's former frozen
normative subject. It records a new frozen subject and fresh applicable
assurance rather than representing the earlier WB-CORE-003D assurance as proof
of that later state.

The Owner authorized this Work Block and its document-only write-set on
2026-08-03. Any later VCS handoff is a separately Owner-authorized operational
action outside this repository Work Block record. Authority order remains the
current Owner instruction, root `AGENTS.md` and accepted governance, accepted
specifications and ADRs, this Work Block, then evidence and memory.

## Scope and write boundaries

### Corrected WB-CORE-003D paths

```text
docs/reports/reviews/wb-core-003d-parallel-write-set-drift.md
docs/reports/closeout/wb-core-003d-parallel-write-set-orchestration.md
docs/tasklist/wb-core-003d-parallel-write-set-orchestration.md
```

The correction must: state that WB-CORE-003D is completed with no active Work
Block; keep hosting-platform/VCS state non-normative; and record the Owner's
separately authorized VCS handoff without claiming that a repository document
independently proves external state. It must preserve the historical
`1bf301...` assurance as an earlier, superseded subject rather than rewriting
its result.

### WB-CORE-003E lifecycle, assurance, and projection paths

```text
docs/plans/wb-core-003e-closure-evidence-correction.md
docs/tasklist/wb-core-003e-closure-evidence-correction.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

The same single Coder owns all normative changes in these seven paths: it first
validates the active candidate, then, only after the required independent
preflight findings, applies the already-reviewed completed/no-active projection.
The Orchestrator records independent read-only findings only in the separate
evidence-only paths below. Reviewer, Verifier, and drift analyst are
independent read-only roles.

### Evidence-only recording paths

```text
docs/reports/reviews/wb-core-003e-closure-evidence-correction-critic.md
docs/reports/reviews/wb-core-003e-closure-evidence-correction-review.md
docs/reports/reviews/wb-core-003e-closure-evidence-correction-drift.md
docs/reports/verification/wb-core-003e-closure-evidence-correction-verification.md
docs/reports/closeout/wb-core-003e-closure-evidence-correction.md
```

The Orchestrator may create or append only these evidence-only records after
the corresponding separate read-only role has returned its result. The Critic
record is written at Define; preliminary and final Reviewer, Verifier, and
drift results are appended after their respective inspections; the closeout is
written only after the final exact subject is present and the final read-only
results exist. These paths are explicitly excluded from the frozen manifest and
do not update authority, lifecycle, map, registry, or release-state content.

### Frozen corrected subject

This Work Block has two frozen eleven-path subjects, both computed with
`sha256sum`/`LC_ALL=C sort` manifest lines: an active candidate for preliminary
assurance after the Coder pass, then a completed/no-active close projection for
final assurance after the preliminary verdicts. Each subject preserves the nine
WB-CORE-003D paths that require renewed assurance and adds this corrective Work
Block's plan/task record:

```text
AGENTS.md
.agent/workflows/sdd-protocol.md
.agent/ROSTER.md
docs/templates/subagent-mission-brief-template.md
docs/templates/integration-plan-template.md
docs/plans/wb-core-003d-parallel-write-set-orchestration.md
docs/tasklist/wb-core-003d-parallel-write-set-orchestration.md
docs/plans/wb-core-003e-closure-evidence-correction.md
docs/tasklist/wb-core-003e-closure-evidence-correction.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

After preliminary `READY`/`READY`/`ALIGNED`, the single Coder prepares the
exact completed/no-active projection in an ephemeral, non-repository preflight
tree. Independent roles assess its eleven-path manifest before it is applied.
Only when those preflight findings are `READY`/`READY`/`ALIGNED` may that same
Coder apply byte-equivalent normative files in this worktree and freeze the
matching final aggregate. Evidence-only records are then appended from the
already obtained findings. This avoids both a premature terminal claim and a
post-assurance normative rewrite. Evidence-only reports are excluded from both
manifests. The prior aggregate
`1bf30158a0e05d4831187396884f16a92c949f3220ec3e751cbeea26b4b35558`
is historical evidence for the pre-correction subject; it is not a readiness
claim for the new aggregate.

## Exclusions, risk, and hard stops

Out of scope: changes to `AGENTS.md`, SDD protocol, roster, templates,
governance contracts, ADRs, accepted specification, runtime adapters, hooks,
CI, scripts/tests, installer, dependencies, configuration, candidate
promotion, live parallel pilot, deployment, destructive operations, and branch
deletion. No hosting-platform state is written into repository authority.

**Profile:** Managed. **Side effect class:** local documentation/governance.
**Evaluation:** not required; deterministic document and contract checks are
sufficient. **Primary risks:** retroactive assurance, circular report evidence,
claiming external VCS facts, or unapproved scope expansion.

Hard stops: any changed path outside this allowlist; Critic `RECONSIDER` or
`BLOCKED`; absent independent assurance; digest mismatch; failed required
check; new material finding; a request to change the parallel orchestration
protocol; or any VCS action, which is outside this Work Block.

## Acceptance and lifecycle

1. The three WB-CORE-003D corrections resolve the cited temporal/state errors
   without changing the parallel-write-set policy or claiming mutable external
   VCS state.
2. A separate Critic challenges the correction and its anti-retroactivity
   boundary before Execute.
3. Reviewer, Verifier, and drift analyst independently recompute the active
   candidate, then independently assess the exact ephemeral final projection
   manifest. They return `READY`, `READY`, and `ALIGNED` at each applicable
   pass. The actual final aggregate must exactly match the assessed preflight
   aggregate.
4. After preflight assurance, the maps, registry, task, and release-state
   reference agree in the frozen close projection:
   WB-CORE-003D and WB-CORE-003E are completed and no active Work Block
   remains. Independent assurance evidence is recorded separately after that
   freeze. WB-CORE-004 remains the next planned product Work Block.
5. Whitespace, SDD, governance, release-state, and release-state-fixture
   checks pass. No runtime, generated surface, or external VCS state is
   presented as installed or authoritative.

Lifecycle:

1. **Define:** create this active corrective plan/tasklist and active
   map/registry projection; resolve a separate Critic gate. The three local
   WB-CORE-003D edits predate that gate and are only an unexecuted candidate.
2. **Execute:** one Coder validates or corrects only the candidate delta and
   freezes the active eleven-path candidate manifest. No terminal lifecycle or
   readiness claim is made in this pass.
3. **Preliminary Assure:** separate Reviewer, Verifier, and drift analyst
   inspect that active candidate. Any normative change returns to Define.
4. **Final preflight:** only after preliminary `READY`/`READY`/`ALIGNED`, the
   same Coder derives an ephemeral, non-repository tree containing the exact
   terminal plan/task/map/registry/release-state changes. Separate Reviewer,
   Verifier, and drift analyst assess that prospective eleven-path manifest;
   their conclusions are not yet a repository lifecycle claim.
5. **Final projection:** only after preflight `READY`/`READY`/`ALIGNED`, the
   same Coder applies byte-equivalent files, including the required successful
   terminal values and `release_state` latest-completed/closeout references,
   then freezes the matching actual aggregate. Any mismatch returns to Define.
6. **Close:** the Orchestrator appends the evidence-only reports and matching
   success closeout from the already obtained independent results, then runs
   the release-state validator against the actual final aggregate. Any VCS
   handoff remains separately Owner-authorized and outside this Work Block.

## Current state

- **Stage:** Define
- **Execution state:** candidate correction validated; preliminary assurance
  has not yet started.
- **Write gate:** OPEN only for this Work Block's approved document write-set.
- **Review / verification / drift:** pending preliminary independent assurance.
- **Task status:** in progress.

## Critic disposition

The initial independent Critic returned `RECONSIDER` on 2026-08-03, without
changing scope or authority. It required two bounded planning corrections:
(1) prepare the completed/no-active map, registry, plan, and task projection
before the final freeze because map/registry are normative subject paths; and
(2) label the pre-Critic three-file delta as a candidate rather than an Execute
result. The final independent Critic disposition is evidence outside this Coder
write-set; it is not restated here as an assurance outcome.

The initial direct-close interpretation was then rejected by the deterministic
release-state validator: a completed Work Block cannot carry pending terminal
assurance. This plan therefore uses the two-pass sequence above, with an exact
non-repository terminal preflight. It changes no policy, authority, or Owner
approved file boundary; a fresh Critic must confirm the corrected sequencing
before preliminary assurance begins.
