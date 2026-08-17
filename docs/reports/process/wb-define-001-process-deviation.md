---
schema_version: 1
artifact_type: material_process_finding
artifact_id: wb-define-001-process-deviation
work_block_id: WB-DEFINE-001
created_at: 2026-08-16
category: assurance
status: disposition_recorded
---

# WB-DEFINE-001 — Material Process Deviation

## Observed Condition

The original `WB-DEFINE-001` implementation was executed under the Managed
governance profile while its required pre-execution Critic gate remained
`pending`. The implementation was later frozen and independently assured, but
post-execution assurance cannot satisfy the missing historical pre-execution
Critic requirement retroactively.

## Concrete Effect

The deviation weakens the assurance quality of the original execution path: the
implementation did not receive the mandatory independent challenge of scope,
assumptions, authority, risk, topology, verification design, and evaluation
design before source mutation began. It therefore blocks truthful
`success-closeout` for the original frozen subject until the deviation is
explicitly dispositioned and the current technical findings are corrected under
a governance-correct corrective loop.

The deviation does **not** by itself require deleting or recreating otherwise
usable implementation. Historical ordering cannot be repaired by relabeling a
later review as the missing Critic.

## Evidence / Decision References

- `governance/lifecycle.md` — Managed requires Critic before execution.
- `.agent/workflows/sdd-protocol.md` — Managed Stage 0 requires a resolved Critic
  before Execute.
- `docs/plans/wb-define-001-requirements-quality-traceability.md` — the Work Block
  recorded Managed governance with `critic_gate: pending` and later recorded
  completed implementation pending assurance.
- Independent read-only assurance of frozen head
  `77ab09bc7d9ba1d74cf4d5b69621dc539b48e873` returned `ASSURANCE NOT READY` and
  identified the missing pre-execution Critic as process finding `P-01`.
- On 2026-08-16 the Owner approved proceeding with the proposed corrective
  course after reviewing that finding. This approval authorizes the corrective
  process; it does not rewrite the historical gate state.

## Disposition

1. Preserve the historical fact that the original implementation ran without the
   required pre-execution Critic. Do not set a retrospective `Critic READY`
   verdict for that execution.
2. Keep the source write gate `BLOCKED` while corrective planning is prepared.
3. Synchronize the stacked PRs non-destructively with the accepted current
   `main` baseline before designing corrections.
4. Submit the bounded corrective plan to an independent Critic **before** any
   corrective source write is authorized.
5. Only after that corrective Critic is resolved may the source write gate be
   reopened for the approved corrective write-set.
6. Freeze the corrected subject and rerun independent Reviewer, Verifier, and
   specification-drift assurance.
7. Final closeout must reference this deviation rather than representing the
   original execution as fully governance-conformant.

## Current Scope Boundary

The corrective loop is limited to findings materially attributable to
`WB-DEFINE-001`:

- `R-01`: implementation coverage must count only `type=requirement` tasks;
- `V-01`: adversarial traceability fixtures must cover the promised fail-closed
  cases, including the non-requirement coverage bypass;
- `R-02`: mandatory Define-quality readiness must become machine-observable with
  the smallest sufficient aggregate prerequisite rather than a new parallel
  authority system;
- `R-03`: the Work Block template regression is resolved by inheriting the
  accepted current-main template during stack synchronization and must not be
  reintroduced.

The pre-existing generic Reviewer verdict wording drift (`D-01`) is excluded and
should be handled separately if still relevant.

This report is evidence only. It grants no source-write authority, does not open
any Hard Stop, and does not replace the corrective Critic, Reviewer, Verifier, or
drift functions.
