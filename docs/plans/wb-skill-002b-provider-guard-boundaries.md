---
schema_version: 1
artifact_type: work_block
artifact_id: wb-skill-002b-provider-guard-boundaries
work_block_id: WB-SKILL-002B
status: in_progress
owner_role: Owner
created_at: 2026-08-23
last_updated: 2026-08-23
governance_profile: Managed
branch: agent/wb-skill-002a-post-merge-reconciliation
base_revision: 4e10b8a4a2b6d390a3b6f3f0e6b6864d0df88dde
write_gate: READY
critic_gate: READY
review_gate: READY
verification_verdict: READY
drift_gate: ALIGNED
evaluation_verdict: NOT_REQUIRED
closeout_mode: pending
owner_approval: Owner prospectively approved WB-SKILL-002B specification revision execute-r1-2026-08-23 and exactly the one-path source write-set scripts/test-sdd-contract.sh on 2026-08-23. This approval is limited to bounded source Execute and grants no commit, push, pull-request, merge, or GitHub-thread authority.
---

# WB-SKILL-002B — Provider Guard Imperative and Fence Boundary Correction

## Objective

Correct two confirmed post-merge P2 defects in the target-only mandatory
provider semantic guard without reverting WB-SKILL-002's valid provider-neutral
skill correction or reopening WB-SKILL-002A's completed lifecycle reconciliation:

1. detect bounded direct imperative provider-assurance mandates, including
   normal Markdown wrapping; and
2. make fenced-code exclusion respect compatible delimiter character, run
   length, and closing-tail boundaries.

**Current Result:** the one approved source path rejects the two defect classes
through its own predicate fixtures, remains restricted to the existing target
skill, and has independent Reviewer, fresh-clone Verifier, and Drift assurance.
Only terminal closeout remains pending.

## Current State

- **Current Stage:** Assure
- **Stage State:** completed
- **Write Gate:** READY — Owner prospectively approved specification revision
  `execute-r1-2026-08-23` and exactly `scripts/test-sdd-contract.sh` for
  bounded source Execute, which completed on final frozen subject
  `39c07db01ce0b08290dbf6721ecb4a53e457b606` →
  `8669bfa2522e3a38c27adc913f60213d7d3aea38`.
- **Critic Gate:** READY — `docs/reports/reviews/wb-skill-002b-provider-guard-boundaries-critic.md`
- **Review Gate:** READY — independent read-only review of frozen source subject
  `39c07db01ce0b08290dbf6721ecb4a53e457b606` →
  `8669bfa2522e3a38c27adc913f60213d7d3aea38`; see
  `docs/reports/reviews/wb-skill-002b-provider-guard-boundaries.md`.
- **Verification Verdict:** READY — fresh detached local temporary-clone
  verification of the same final source subject; see
  `docs/reports/verification/wb-skill-002b-provider-guard-boundaries.md`.
- **Drift Gate:** ALIGNED — independent read-only source-to-specification audit
  of the same final source subject; see
  `docs/reports/drift/wb-skill-002b-provider-guard-boundaries.md`.
- **Evaluation Verdict:** NOT_REQUIRED — deterministic tooling reconciliation;
  no non-deterministic product behavior is introduced.
- **Closeout Mode:** pending
- **Task Status:** in_progress — terminal closeout (TASK-009) remains open.

## Confirmed Findings

### P2-001 — Direct imperative provider assurance was not detected

The pre-correction `require_absent_mandatory_provider_semantics`
implementation did not reliably classify direct imperatives such as `Ask Codex
to review the implementation.` as a mandatory provider review. Its modal-based
logic left a bypass despite the target-only guard's intended provider-neutral
boundary.

### P2-002 — Fence closure boundary was not compatible-delimiter aware

The pre-correction fence handling toggled exclusion too broadly. A mismatched
delimiter, shorter closing run, or closing suffix could terminate exclusion and
cause code content to be scanned as prose. The final correction requires a
compatible closer and permits later ordinary prose only after a valid closure.

Both findings derive from the GitHub Codex review of PR #44. They are recorded
as repository corrective inputs only; this Work Block does not resolve, alter,
or otherwise mutate GitHub review threads.

## Normative Baseline

- **Approved Specification:** `docs/specs/wb-skill-002b-provider-guard-boundaries.md`
- **Specification Status:** approved — prospective source authority limited to
  the exact one-path write-set below.
- **Specification Revision:** `execute-r1-2026-08-23`
- **Accepted Architecture Decisions:** not applicable; use the existing bounded
  contract-script pattern.
- **External Contracts:** GitHub review findings are advisory external input;
  no external mutation is authorized.
- **Derived Implementation Plan:** this Work Block
- **Approved Evaluation Plan:** not required
- **Active Tasklist:** `docs/tasklist/wb-skill-002b-provider-guard-boundaries.md`

## Define Quality Prerequisite

```json
"define_quality": {
  "required": true,
  "status": "READY",
  "requirements_review": "READY — docs/reports/requirements/wb-skill-002b-provider-guard-boundaries.md",
  "traceability": "READY — requirements=6 acceptance=9 tasks=9",
  "consistency_analysis": "READY — docs/reports/requirements/wb-skill-002b-provider-guard-boundaries-consistency.md"
}
```

Managed Define quality is required and is READY because the independent
requirements review, structural traceability result, and independent
consistency analysis are all recorded above. The separately recorded Owner
approval made specification revision `execute-r1-2026-08-23` authoritative and
opened the one-path Write Gate; it did not grant terminal-closeout authority.

## Repository Preflight

- **Git baseline:** branch `agent/wb-skill-002a-post-merge-reconciliation`,
  `4e10b8a4a2b6d390a3b6f3f0e6b6864d0df88dde`.
- **Pre-existing dirty files:** none tracked.
- **Untracked artifacts:** `Repository Graph Evaluation Brief.md` (Owner
  artifact; out of scope and must not be modified, staged, moved, deleted, or
  committed).
- **Current diff:** Define artifacts, source commits, and final source-assurance
  evidence are recorded. The final source subject is
  `39c07db01ce0b08290dbf6721ecb4a53e457b606` →
  `8669bfa2522e3a38c27adc913f60213d7d3aea38`.
- **Proceed rule:** only a separately approved terminal coordination/evidence
  write set may proceed. All unrelated working-tree state remains preserved.

## Scope

### In Scope Now

```text
docs/plans/wb-skill-002b-provider-guard-boundaries.md
docs/specs/wb-skill-002b-provider-guard-boundaries.md
docs/tasklist/wb-skill-002b-provider-guard-boundaries.md
```

### Approved Source Write-Set — Execute Only

```text
scripts/test-sdd-contract.sh
```

The Owner prospectively approved this exact one-path source write-set on
2026-08-23 for WB-SKILL-002B Execute only. This single script owns the
target-only predicate and its executable fixtures. No smaller source owner
exists. It must normalize only the bounded imperative and fence behavior needed
by these findings; it must not change the target skill, add a parser dependency,
or scan other repository paths.

### Authorized Current Define-Evidence Paths

```text
docs/reports/requirements/wb-skill-002b-provider-guard-boundaries.md
docs/reports/requirements/wb-skill-002b-provider-guard-boundaries-consistency.md
docs/reports/reviews/wb-skill-002b-provider-guard-boundaries-critic.md
```

These paths persist pre-Execute Define evidence only. They do not create
source, commit, push, pull-request, merge, or GitHub-thread authority.

### Recorded Source-Assurance Evidence Paths

```text
docs/reports/reviews/wb-skill-002b-provider-guard-boundaries.md
docs/reports/verification/wb-skill-002b-provider-guard-boundaries.md
docs/reports/drift/wb-skill-002b-provider-guard-boundaries.md
```

These records bind only the final frozen source subject
`39c07db01ce0b08290dbf6721ecb4a53e457b606` →
`8669bfa2522e3a38c27adc913f60213d7d3aea38`. They do not cover a later
coordination/evidence or terminal-closeout revision.

### Proposed Future Closeout Evidence Path — Not Authorized

```text
docs/reports/closeout/wb-skill-002b-provider-guard-boundaries.md
```

### Out of Scope

- WB-SKILL-002A terminal evidence, P1 lifecycle correction, and closeout.
- `skills/codex-verification/SKILL.md`, governance, release-state validators,
  `FILE_REGISTRY.yml`, and `PROJECT_MAP.md`.
- Broad Markdown parsing, dependencies, or repository-wide scanning.
- GitHub thread resolution, push, PR creation, merge, rebase, or other external
  mutation.
- Gemini backlog, legacy role-skill convergence, extensions, presets,
  workflows, and bundles.

## Delivered Design and Test Matrix

The delivered implementation retains paragraph/list/heading boundaries from
WB-SKILL-002A and makes only these two bounded changes:

| Area | Required design | Adversarial controls |
| --- | --- | --- |
| Imperative mandate | Recognize only: optional `To verify,`; optional `please`/`kindly`; `ask`/`request`; recognized alias (`provider`, `Codex`, `additional model`, `second model`); `to`; `review`/`verify`/`perform verification`, with ordinary wrapping. | one-line and wrapped variants; `Do not ask Codex to review the implementation.`; optional advisory prose; paragraph-separated terms. |
| Fenced code | Accept a regular opener of at most three leading spaces, matching backtick/tilde run of at least three, and optional info tail; close only with at most three leading spaces, the same character, equal-or-longer run, and whitespace-only tail. | four-backtick opener plus three-backtick non-closer; mismatched character; invalid suffix; unclosed fence; valid equal-or-longer closure then prohibited prose. |

The delivered fixtures call the same predicate used for the target skill, not a
duplicate test-only approximation.

## Risk and Authority

- **Side-Effect Class:** completed local-test source correction; terminal
  evidence coordination remains pending.
- **DB/Data Action Mode:** none.
- **Sensitive Domains:** provider governance only; no credentials or external
  provider execution.
- **Output Non-Determinism:** none.
- **Autonomous Tool/Trajectory Risk:** bounded: a false-positive guard can
  block contract validation; final adversarial fixtures mitigate the identified
  false-closer regression gap.
- **Threat Model Required:** no; this is deterministic repository governance,
  not a security boundary.
- **Rollback / Recovery:** revert the bounded one-path source commits only if
  later applicable assurance identifies an issue; no history rewrite.

## Hard Stops

- [x] Source execution — one Coder changed only
  `scripts/test-sdd-contract.sh`; final frozen source assurance is recorded.
- [x] Commit or push — requires separate Owner authorization.
- [x] Pull-request creation, merge, rebase, or GitHub-thread resolution — not
  authorized by this Work Block.
- [x] Scope expansion, dependency, governance/release-state, registry/map, or
  target-skill change — return to Define and Owner approval.

## Execution and Assurance Sequence

1. Define quality and Critic evidence became READY. The Owner prospectively
   approved specification revision `execute-r1-2026-08-23` and exactly the
   one-path source write-set `scripts/test-sdd-contract.sh`, opening the Write
   Gate for bounded source Execute.
2. One Coder changed only `scripts/test-sdd-contract.sh` and ran targeted plus
   standard deterministic validation: `bash -n scripts/test-sdd-contract.sh`,
   `bash scripts/test-sdd-contract.sh`, `bash scripts/validate-governance.sh`,
   `python3 scripts/validate-release-state.py`,
   `python3 scripts/test-release-state-contracts.py`, `git diff --check`, and
   an exact one-path `git diff --name-status <frozen-base>..<frozen-head>`
   manifest.
3. The final frozen subject `39c07db01ce0b08290dbf6721ecb4a53e457b606` →
   `8669bfa2522e3a38c27adc913f60213d7d3aea38` received independent Reviewer
   `READY`, fresh-clone Verifier `READY`, and Drift `ALIGNED` evidence. A prior
   verifier attempt at intermediate head `21747506fdaab57778944714a53f6a5aec79ebfd`
   was `BLOCKED` because its fixtures did not distinguish false fence closers;
   the separate correction commit `8669bfa2522e3a38c27adc913f60213d7d3aea38`
   added those discriminating fixtures, and the final assurance was re-run on
   the new frozen subject.
4. Perform terminal closeout only with a separately approved coordination/
   evidence write set and fresh assurance applicable to its later normative
   subject.

No parallel writers were permitted: one Coder owned the approved source
write-set. A live PR #44 base/head reread was an execution-time observation;
it did not create approval or execution authority. Terminal closeout has not
been authorized and TASK-009 remains open.
