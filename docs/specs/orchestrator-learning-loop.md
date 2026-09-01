---
schema_version: 1
artifact_type: specification
artifact_id: orchestrator-learning-loop
status: approved
owner_role: owner
work_block_id: WB-LEARNING-001
revision: 1
created_at: 2026-08-31
last_verified: 2026-08-31
---

# Orchestrator Learning Loop

## Objective

Make evidence-backed reusable engineering learning a normal part of every non-trivial Work Block closeout without requiring a separate Owner reminder, while preserving Work Block authority and preventing Engineering Memory from becoming a chat archive.

## Requirements

- **REQ-001 — Mandatory learning review.** Every non-trivial Work Block performs an Orchestrator learning review during Close, for both `success-closeout` and `reporting-only`.
- **REQ-002 — Lifecycle-wide coverage.** The review considers material findings from Define, Execute, Assure, and Close.
- **REQ-003 — Classification.** Material reusable lesson candidates receive exactly one disposition: `promoted`, `operational-only`, or `not-applicable`.
- **REQ-004 — Utility filter.** Durable promotion requires evidence-backed knowledge that can change future planning, execution strategy, review, verification, recovery, or invariant enforcement.
- **REQ-005 — Noise exclusion.** Do not promote one-off noise, speculation, raw transcripts, hidden/private reasoning, secrets/private data, ordinary status history, or code facts cheaper to re-verify live.
- **REQ-006 — Deduplication.** Before promotion, compare existing Engineering Memory and update/extend an existing lesson when appropriate instead of creating duplicates.
- **REQ-007 — Durable record shape.** A promoted lesson identifies evidence, scope, reusable principle, replacement/mitigation/recovery, authority boundary, review trigger, and last-verified date.
- **REQ-008 — No separate reminder.** Learning review is an ordinary Orchestrator Close responsibility and does not depend on a separate Owner request such as “record the lesson”.
- **REQ-009 — No implicit authority.** Classification, candidate discovery, or promotion eligibility never expands the approved write-set, Hard Stops, specification, governance, or other authority. Promotion may mutate only already-approved Engineering Memory paths; otherwise return to Define.
- **REQ-010 — Project/framework boundary.** Project-specific lessons remain project-local. Generalization into framework policy/templates requires a separate evidence-backed framework Work Block.
- **REQ-011 — Portable propagation.** Fresh generated projects receive a canonical project lessons log and the same learning/classification semantics.
- **REQ-012 — Runtime neutrality.** The mechanism is provider/model/runtime neutral; runtime adapters implement but do not redefine it.

## Acceptance Criteria

- **AC-001 [req=REQ-001]:** `governance/lifecycle.md` makes learning review part of non-trivial Close.
- **AC-002 [req=REQ-002]:** self-hosting and portable SDD procedures explicitly cover Define, Execute, Assure, and Close findings.
- **AC-003 [req=REQ-003]:** lifecycle, skill, templates, and memory contract converge on `promoted | operational-only | not-applicable`.
- **AC-004 [req=REQ-004]:** the durable filter is future-use/evidence based rather than issue-count based.
- **AC-005 [req=REQ-005]:** forbidden/noise categories remain explicit.
- **AC-006 [req=REQ-006]:** closeout procedure requires deduplication against existing Engineering Memory before promotion.
- **AC-007 [req=REQ-007]:** the portable lessons log defines the durable lesson fields.
- **AC-008 [req=REQ-008]:** the procedure says no separate Owner reminder is needed after the WB/write authority is already approved.
- **AC-009 [req=REQ-009]:** classification is explicitly non-authorizing and out-of-scope memory mutation returns to Define.
- **AC-010 [req=REQ-010]:** project-to-framework promotion requires a separate framework Work Block.
- **AC-011 [req=REQ-011]:** `template/docs/engineering-memory/lessons-learned.md` exists and is a required common bootstrap path.
- **AC-012 [req=REQ-012]:** no provider-specific lifecycle requirement is introduced; canonical/OpenCode closeout skill semantics remain aligned.

## Non-goals

- No automatic project-to-framework synchronization.
- No new memory daemon, vector database, transcript summarizer, or runtime service.
- No new machine lifecycle state or schema field in this Work Block.
- No changes to `WB-RELEASE-002`, release-state promotion, current framework lessons history, protected-branch policy, or production/external capability controls.

## Authority Boundary

Engineering Memory remains below current Owner instruction, governance, specifications/ADRs, and the active Work Block. Learning classification is evidence and disposition, never permission. A promoted lesson can influence future planning/review/verification but cannot override current higher authority.
