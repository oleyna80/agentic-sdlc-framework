---
schema_version: 1
artifact_type: closeout_projection
artifact_id: wb-define-001-final-closeout-projection
work_block_id: WB-DEFINE-001
created_at: 2026-08-16
status: exact_preflight_ready
assured_normative_subject: 2075cafdecdb75ac5f747c466abb3c1a5f71c611
assurance_report: docs/reports/reviews/wb-define-001-final-reassurance.md
projection_class: exact_normative_terminal_state_preflight
exact_projection_manifest: docs/reports/reviews/wb-define-001-final-closeout-exact-projection.json
projection_definition_sha256: 7042963bdca4f22734442e178466efcc20413984fc9ac9a60148f61e6bcb2be6
recorded_by: orchestrator
---

# WB-DEFINE-001 — Exact Prospective Final Closeout Projection

## Purpose

Prepare the exact byte-bound terminal-state projection for independent final-close preflight without changing the normative subject prematurely.

The already obtained `ASSURANCE READY` verdict applies to normative subject:

`2075cafdecdb75ac5f747c466abb3c1a5f71c611`

The current PR head may contain evidence-only reports after that subject, but no normative projection below has been applied.

## Previous preflight disposition

The first final-close preflight returned `NOT_READY` with two MATERIAL findings:

- `FC-01` — `FILE_REGISTRY.yml` also contains a dedicated WB-DEFINE-001 entry whose `role` and `lifecycle_status` must move from active/in-progress to completed/completed when migration state becomes completed/no-active.
- `FC-02` — semantic equivalence is insufficient. The prospective terminal subject must be byte-bound before application so actual projection can be proven identical to the subject independently inspected.

The three-path normative allowlist itself was accepted as sufficient. No fourth normative path is introduced by this supplement.

## Exact normative allowlist

Exactly three normative paths may change:

```text
docs/plans/wb-define-001-requirements-quality-traceability.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

Any requirement for a fourth normative path, new lifecycle/authority semantics, or source/runtime change returns to Define/Critic.

## Exact byte-bound projection definition

The canonical machine-readable definition is:

`docs/reports/reviews/wb-define-001-final-closeout-exact-projection.json`

Its projection-definition digest is:

`7042963bdca4f22734442e178466efcc20413984fc9ac9a60148f61e6bcb2be6`

Digest verification is deterministic: parse the JSON, remove the top-level `projection_definition_sha256` field, serialize the remaining object as UTF-8 JSON with recursively sorted keys, `ensure_ascii=false`, and separators `(',', ':')`, then compute SHA-256. The result must equal the value above.

The manifest binds each target path to its exact current baseline blob plus an ordered list of exact string replacements:

```text
docs/plans/wb-define-001-requirements-quality-traceability.md
  base blob: 676b893eb2d71eac77d482ccbcc6f54c8edfffdd

PROJECT_MAP.md
  base blob: 32808a5a10b4168ef6a3a0d73b491a232b575dc5

FILE_REGISTRY.yml
  base blob: 0cae97b700969c10816cfac14d7c5775629d9ef9
```

### Deterministic reproduction rule

For every file, the independent preflight must:

1. fetch the exact baseline blob named in the manifest;
2. require every `from` byte sequence to occur exactly once before mutation;
3. apply replacements in manifest order using UTF-8/LF bytes without whitespace normalization, formatting, reflow, YAML reserialization, or other edits;
4. reject a missing or multiply occurring `from` sequence;
5. compute the resulting Git blob SHA and SHA-256 for each projected file;
6. build a canonical manifest sorted by path containing `path`, `baseline_blob_sha`, `projected_git_blob_sha`, and `projected_sha256` separated by a single TAB per field and terminated by LF per record;
7. compute a final aggregate SHA-256 over those UTF-8 canonical manifest bytes.

The preflight must report all three projected blob SHAs, all three projected SHA-256 values, the exact canonical three-line manifest, and the aggregate SHA-256. Those reported values become the only permitted terminal projection subject.

After approval, actual application must reproduce the same exact replacements against the same baseline blobs. `Semantically equivalent` is not sufficient. Actual projected file blobs and aggregate must exactly equal the values returned by the approved preflight.

## Work Block terminal projection

The exact manifest changes only terminal lifecycle/evidence state while retaining implementation design, corrective chronology, P-01 history, scope boundaries, and stop conditions.

Target frontmatter includes:

```yaml
status: completed
implementation_state: completed_assurance_ready
final_assurance: ASSURANCE_READY
final_assurance_subject: 2075cafdecdb75ac5f747c466abb3c1a5f71c611
final_assurance_report: docs/reports/reviews/wb-define-001-final-reassurance.md
closeout_mode: success-closeout
```

Existing historical/corrective fields remain, including:

```yaml
critic_gate: READY
corrective_critic_round_1: SUPPLEMENT
corrective_critic_round_2: APPROVE
corrective_critic_round_3: APPROVE
write_gate: BLOCKED
process_deviation: docs/reports/process/wb-define-001-process-deviation.md
```

The projection also records R-01/R-02/R-02A/R-03/V-01 as resolved, AC1–AC16 as satisfied, and replaces the pending Assure section with terminal state:

```text
Stage State: completed
Write Gate: CLOSED
Review Gate: READY
Verification Verdict: READY
Evaluation Verdict: SKIPPED — deterministic framework contracts and executable fixtures were sufficient; no non-deterministic output evaluation was required
Drift Gate: ALIGNED
Closeout Mode: success-closeout
Task Status: completed
```

P-01 remains a historical material process deviation. Successful corrective closeout must explicitly state that it does not make the original Managed Execute governance-conformant retroactively.

## PROJECT_MAP terminal projection

The exact manifest performs only these lifecycle/navigation changes:

- append WB-DEFINE-001 to machine-readable `completed_work_blocks`;
- set `active_work_block: null`;
- change the Key Paths WB-DEFINE-001 row from active to completed;
- add WB-DEFINE-001 as completed item 23 in Migration Work;
- replace the active WB entry with `No active implementation Work Block.`;
- preserve WB-CORE-004 as the next planned product Work Block.

Authority order, current/target architecture, Portable Kit promotion state, PR #37/#38/#39 semantics, and unrelated Work Block history remain untouched.

## FILE_REGISTRY terminal projection

The exact manifest includes the complete reconciliation required by `FC-01`:

```yaml
migration_state:
  completed_work_blocks:
    # append WB-DEFINE-001
  active_work_block: null
  next_planned_work_block: WB-CORE-004

release_state:
  latest_completed_work_block: docs/plans/wb-define-001-requirements-quality-traceability.md
  closeout_report: docs/reports/closeout/wb-define-001-requirements-quality-traceability.md
  external_vcs_state: non_normative
  authority: assurance_only
```

The dedicated entry changes from:

```yaml
role: active_managed_define_stage_requirements_quality_and_traceability_work_block
lifecycle_status: in_progress
```

to:

```yaml
role: completed_managed_define_stage_requirements_quality_and_traceability_work_block
lifecycle_status: completed
```

`status: log`, owner, current architecture, bounded authority, Define-quality registration, runtime/integration mappings, installation profiles, and all unrelated registry content remain byte-identical.

## Closeout evidence boundary

The closeout report remains future evidence-only output:

`docs/reports/closeout/wb-define-001-requirements-quality-traceability.md`

It must be created only after the exact three-file projection has been applied and actual projected blob/aggregate values exactly match the approved preflight values.

The closeout report must bind the actual resulting normative revision/aggregate and record Stage completed, Reviewer READY, Verifier READY, Evaluation SKIPPED with deterministic rationale, Drift ALIGNED, closeout classification SUCCESS, task status completed, P-01 preserved as historical residual process deviation, external PR/merge/VCS state non-normative and separately controlled, and WB-CORE-004 as next planned product Work Block.

The report cannot manufacture assurance for its own preceding normative projection.

Release-state/framework CI must run only after the terminal normative projection and required closeout report coexist. A transient write sequence before the report exists is not a READY release-state claim.

## Tasklist and memory

No new `docs/tasklist/...` file is required. The release-state contract does not require one for WB-DEFINE-001 and creating one now would add unnecessary normative scope.

Memory-bank synchronization and any engineering-memory classification are lower-authority bookkeeping after successful repository closeout. They are not part of the three-file final projection and cannot affect its readiness.

## Acceptance for repeated exact preflight

The repeated preflight may return READY only if it independently proves:

1. current PR head differs from the assured normative subject only by evidence-only reports;
2. the exact projection manifest digest is `7042963bdca4f22734442e178466efcc20413984fc9ac9a60148f61e6bcb2be6` under the canonicalization rule above;
3. all three manifest baseline blob SHAs match the current normative files;
4. every exact replacement source occurs once and only once;
5. generated projected bytes produce reported per-file Git blob SHA and SHA-256 values plus one aggregate SHA-256;
6. `FC-01` is resolved inside `FILE_REGISTRY.yml` with completed role/lifecycle state;
7. Work Block, PROJECT_MAP and FILE_REGISTRY agree on completed/no-active state;
8. P-01 remains historical and is not retroactively repaired;
9. no fourth normative path or new authority/lifecycle behavior is required;
10. release-state will become structurally complete once the evidence-only closeout report is appended after exact application.

If READY, the final preflight must explicitly return the expected three projected Git blob SHAs and the final aggregate SHA-256. Actual application is authorized only when those exact values can be reproduced.

## Provider evidence boundary

Current PR head and current CI are mutable hosting-platform evidence and are intentionally not embedded as self-invalidating normative/evidence claims here. The repeated preflight must query GitHub directly and confirm that the current head differs from `2075cafdecdb75ac5f747c466abb3c1a5f71c611` only by approved evidence paths and that applicable checks are green.

This artifact and its JSON manifest are evidence/preflight material only. They do not close WB-DEFINE-001, do not change the normative subject, do not authorize merge, and do not alter external GitHub authority.