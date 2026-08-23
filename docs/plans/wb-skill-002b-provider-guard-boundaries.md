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
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
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

**Expected Final Result:** the one allowed future source path rejects the two
defect classes through its own predicate fixtures, remains restricted to the
existing target skill, and receives independent Reviewer, fresh-clone Verifier,
and Drift assurance before closeout.

## Current State

- **Current Stage:** Execute
- **Stage State:** in_progress
- **Write Gate:** READY — Owner prospectively approved specification revision
  `execute-r1-2026-08-23` and exactly `scripts/test-sdd-contract.sh` for
  bounded source Execute. No source task has started.
- **Critic Gate:** READY — `docs/reports/reviews/wb-skill-002b-provider-guard-boundaries-critic.md`
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Drift Gate:** PENDING
- **Evaluation Verdict:** NOT_REQUIRED — deterministic tooling reconciliation;
  no non-deterministic product behavior is introduced.
- **Closeout Mode:** pending
- **Task Status:** in_progress

## Confirmed Findings

### P2-001 — Direct imperative provider assurance is not detected

The current `require_absent_mandatory_provider_semantics` implementation does
not reliably classify direct imperatives such as `Ask Codex to review the
implementation.` as a mandatory provider review. Its modal-based logic leaves
a bypass despite the target-only guard's intended provider-neutral boundary.

### P2-002 — Fence closure boundary is not compatible-delimiter aware

The current fence handling toggles exclusion too broadly. A mismatched
delimiter, shorter closing run, or closing suffix can terminate exclusion and
cause code content to be scanned as prose. Conversely, valid closure must
allow later ordinary prose to be scanned.

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

Managed Define quality is required and is READY only because the independent
requirements review, structural traceability result, and independent
consistency analysis are all recorded above. This does not approve the draft
specification or open the source Write Gate.

## Repository Preflight

- **Git baseline:** branch `agent/wb-skill-002a-post-merge-reconciliation`,
  `4e10b8a4a2b6d390a3b6f3f0e6b6864d0df88dde`.
- **Pre-existing dirty files:** none tracked.
- **Untracked artifacts:** `Repository Graph Evaluation Brief.md` (Owner
  artifact; out of scope and must not be modified, staged, moved, deleted, or
  committed).
- **Current diff:** Define artifacts and approved Define evidence are recorded;
  no source implementation has started.
- **Proceed rule:** source Execute may change only the exact approved one-path
  write-set below; all unrelated working-tree state remains preserved.

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

### Proposed Future Assurance and Closeout Evidence Paths — Not Authorized

```text
docs/reports/reviews/wb-skill-002b-provider-guard-boundaries.md
docs/reports/verification/wb-skill-002b-provider-guard-boundaries.md
docs/reports/drift/wb-skill-002b-provider-guard-boundaries.md
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

## Design Boundary and Future Test Matrix

The future implementation should retain paragraph/list/heading boundaries from
WB-SKILL-002A and make only two bounded changes:

| Area | Required design | Adversarial controls |
| --- | --- | --- |
| Imperative mandate | Recognize only: optional `To verify,`; optional `please`/`kindly`; `ask`/`request`; recognized alias (`provider`, `Codex`, `additional model`, `second model`); `to`; `review`/`verify`/`perform verification`, with ordinary wrapping. | one-line and wrapped variants; `Do not ask Codex to review the implementation.`; optional advisory prose; paragraph-separated terms. |
| Fenced code | Accept a regular opener of at most three leading spaces, matching backtick/tilde run of at least three, and optional info tail; close only with at most three leading spaces, the same character, equal-or-longer run, and whitespace-only tail. | four-backtick opener plus three-backtick non-closer; mismatched character; invalid suffix; unclosed fence; valid equal-or-longer closure then prohibited prose. |

The eventual fixtures must call the same predicate used for the target skill,
not a duplicate test-only approximation.

## Risk and Authority

- **Side-Effect Class:** local-docs in this Define stage; future local-test
  source correction only.
- **DB/Data Action Mode:** none.
- **Sensitive Domains:** provider governance only; no credentials or external
  provider execution.
- **Output Non-Determinism:** none.
- **Autonomous Tool/Trajectory Risk:** none in Define; bounded in later source
  correction because a false-positive guard can block contract validation.
- **Threat Model Required:** no; this is deterministic repository governance,
  not a security boundary.
- **Rollback / Recovery:** revert only the future one-path source commit if
  independent assurance identifies an issue; no history rewrite.

## Hard Stops

- [ ] Source execution — authorized only for one Coder and exactly
  `scripts/test-sdd-contract.sh`; no source task has started.
- [x] Commit or push — requires separate Owner authorization.
- [x] Pull-request creation, merge, rebase, or GitHub-thread resolution — not
  authorized by this Work Block.
- [x] Scope expansion, dependency, governance/release-state, registry/map, or
  target-skill change — return to Define and Owner approval.

## Execution and Assurance Sequence

1. Define quality and Critic evidence are READY. The Owner prospectively
   approved specification revision `execute-r1-2026-08-23` and exactly the
   one-path source write-set `scripts/test-sdd-contract.sh`; the Write Gate is
   READY for bounded source Execute only.
2. One Coder changes only `scripts/test-sdd-contract.sh` and runs targeted plus
   standard deterministic validation: `bash -n scripts/test-sdd-contract.sh`,
   `bash scripts/test-sdd-contract.sh`, `bash scripts/validate-governance.sh`,
   `python3 scripts/validate-release-state.py`,
   `python3 scripts/test-release-state-contracts.py`, `git diff --check`, and
   an exact one-path `git diff --name-status <frozen-base>..<frozen-head>`
   manifest.
3. Freeze the exact source subject; an independent Reviewer examines the diff,
   a Verifier runs the suite in a fresh clone, then a Drift audit compares
   source behavior to this specification.
4. Persist evidence and perform terminal closeout only with separately approved
   coordination/evidence write sets.

No parallel writers are permitted: one Coder owns each approved write-set.
Immediately before Execute and source-subject freeze, re-read live PR #44 base
and head. Record the values dynamically in the implementation/assurance
evidence; the observation creates no approval or execution authority.
