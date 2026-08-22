---
schema_version: 1
artifact_type: work_block
artifact_id: wb-skill-002a-post-merge-reconciliation
work_block_id: WB-SKILL-002A
status: in_progress
owner_role: Owner
created_at: 2026-08-21
last_updated: 2026-08-21
governance_profile: Managed
branch: agent/wb-skill-002a-post-merge-reconciliation
base_revision: f206e6bd845bfaa8d78082610a7d784b6669cf2c
write_gate: READY
critic_gate: READY
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
evaluation_verdict: NOT_REQUIRED
owner_approval: Owner prospectively approved WB-SKILL-002A specification revision execute-r1-2026-08-21 and exactly the recorded five-path source write-set on 2026-08-21. The approval is limited to bounded source Execute; it does not prove or retroactively cure historical WB-SKILL-002 approval, and grants no GitHub or merge authority.
---

# WB-SKILL-002A — Post-Merge Specification and Regression-Guard Reconciliation

## Objective

Reconcile two confirmed post-merge WB-SKILL-002 defects without reverting its
valid provider-neutral source correction:

1. restore truthful specification/lifecycle state without fabricating historical
   Owner approval;
2. make the target-only mandatory-provider regression guard resistant to normal
   Markdown line wrapping; and
3. add the smallest justified deterministic protection against successful
   closeout with a non-authoritative separate specification, only after an
   evidence-based impact inventory.

**Expected Final Result:** the implemented correction truthfully reconciles the
WB-SKILL-002 specification, detects wrapped mandatory-provider semantics in the
existing target-only guard, and rejects the same eligible condition at the
latest-completed release-state boundary without changing the accepted skill.
Frozen independent assurance remains required before any terminal claim.

## Current Execute Authorization State

- **Current Stage:** Execute
- **Stage State:** in_progress — Define investigation, requirements quality,
  consistency analysis, Critic review, the P1 decision, and prospective source
  authorization are complete. The approved source corrections and the bounded
  follow-up correction from independent review have been implemented; frozen
  independent assurance remains pending.
- **Write Gate:** READY — Owner approval is limited to the exact five-path
  source write-set recorded below.
- **Critic Gate:** READY
- **Review Gate:** PENDING
- **Verification:** PENDING
- **Drift:** PENDING
- **Evaluation:** NOT_REQUIRED — the target behavior is deterministic
  governance/tooling reconciliation; no non-deterministic product behavior is
  introduced.

## Historical Fact Investigation — P1

### Classification

**B — TRACKED PRE-EXECUTE APPROVAL EVIDENCE DOES NOT EXIST.**

Repository-proven evidence is limited and time-ordered:

| Time / revision | Repository evidence | What it establishes | What it does not establish |
| --- | --- | --- | --- |
| `af0c1615f7186b42939cd35435b630a91a6c14fc` (2026-08-21 10:25:18 +02:00) | Creation of `docs/specs/wb-skill-002-provider-neutral-verifier.md` | `define-r2-2026-08-21` was recorded as `status: draft`; its `owner_approval` grants Define-only creation and explicitly grants no source-write, GitHub, or merge authority. | Approval of that exact specification revision for Execute. |
| `0abcc39760efb24a40ec92512f69d0cc49eb08ac` (2026-08-21 10:25:28 +02:00) | First WB-SKILL-002 source Execute commit | Execute began after the draft specification was recorded. | Any untracked Owner decision. |
| WB-SKILL-002 Work Block history | `Write Gate: READY` states that the Owner approved the exact two-path Execute write-set after Define readiness and Critic approval. | A recorded source write-set authorization. | Approval of the separate specification revision as authoritative. |
| `48e324f67b8c58b128b17fc959bdf0bc47f8d3b4` and `c7c4d037149077d10b72c3791bd54324015d1f7e` | source assurance and terminal closeout evidence | Historical assurance and closeout were recorded. | A pre-Execute Owner approval of `define-r2-2026-08-21`; the specification blob remained `draft`. |

The file's complete `git log --all --follow` history has only the creation
commit above; no subsequent commit changes its status. Requirements reviews,
consistency reports, Critic evidence, source/terminal assurance, and closeout
refer to `define-r2-2026-08-21` but do not record an Owner approval of that
revision for Execute.

**Historical external Owner approval: UNVERIFIED.** This is not a claim that
such approval did not happen outside tracked repository artifacts. It is only a
repository-evidence boundary.

### Historical Owner Decision Boundary

At Define, the remediation required one of these distinct branches:

- **A — verified historical pre-Execute approval:** classify the issue as a
  recording/projection defect and cite independent dated evidence.
- **B — no verifiable historical approval and no later Owner confirmation of
  that fact:** record a historical process deviation; a current approval is
  prospective only.
- **C — historical fact remains unresolved:** retain `UNVERIFIED`, record a
  truthful corrective lifecycle state, and request an Owner decision on current
  prospective authority without inventing the past.

The later Owner may confirm verifiable historical evidence, acknowledge a
historical process deviation, or approve current authority prospectively. These
are distinct decisions. The subsequent bounded Execute selected B and recorded
a prospective-only approval of the old specification; it did not rewrite the
historical `draft` state or claim retroactive compliance.

### Required Owner Decision Before P1 Execute

Before TASK-001 could alter
`docs/specs/wb-skill-002-provider-neutral-verifier.md`, the Owner must record
at this exact plan location one and only one remediation decision:

- **A — verified historical pre-Execute approval**, with independent dated
  repository or Owner evidence sufficient to establish the timing;
- **B — historical process deviation**, acknowledging that no verifiable
  pre-Execute approval is being asserted and separately stating any current
  prospective authority; or
- **C — historical fact unresolved**, retaining `UNVERIFIED` for that fact and
  stating the current prospective-authority decision without resolving history.

The record must name the selected letter, date, Owner authority evidence, and
the decision's historical or prospective temporal scope. Before the recorded
selection, **P1 Execute and prior-specification metadata changes were BLOCKED**.
The gate did not permit a C record to silently select a historical answer.

#### Recorded Owner Decision — 2026-08-21

**Selected branch: B — historical process deviation.** The Owner's explicit
instruction in this coordination record, “выбираю B — historical process
deviation,” is the authority evidence for selecting this corrective historical
classification on 2026-08-21. It is not evidence of an external historical
approval before WB-SKILL-002 Execute.

The repository-proven fact remains classification **B**: no verifiable
pre-Execute Owner approval is asserted in tracked repository evidence.
Historical external Owner approval remains **UNVERIFIED**. This decision records
historical classification only; it does not authorize P1 source Execute, alter
the prior specification metadata, or grant prospective approval for
WB-SKILL-002A.

### Recorded Prospective Owner Approval — WB-SKILL-002 Specification

The Owner's explicit instruction, “одобряю prospective approval старой
WB-SKILL-002 specification,” prospectively approves the current reconciled
`docs/specs/wb-skill-002-provider-neutral-verifier.md` revision on 2026-08-21.
Accordingly, its status is now `approved` and its reconciliation record states
that the status takes effect only from this date. This is a separate current
authority decision for the prior Work Block's specification. It does not prove
pre-Execute approval, retroactively cure, or rewrite the recorded historical
process deviation, and grants no source-write, GitHub, or merge authority.

### Recorded Prospective Owner Approval for WB-SKILL-002A Execute

The Owner's explicit instruction, “одобряю,” given after the required approval
was requested, prospectively approves specification revision
`execute-r1-2026-08-21` in `approved` status and exactly this frozen source
write-set:

```text
docs/specs/wb-skill-002-provider-neutral-verifier.md
scripts/test-sdd-contract.sh
governance/release-state.md
scripts/validate-release-state.py
scripts/test-release-state-contracts.py
```

This is bounded WB-SKILL-002A source Execute authority only. It neither proves
pre-Execute approval for WB-SKILL-002 nor retroactively cures that historical
process record. It grants no GitHub, push, pull-request, merge, rebase, or
default-branch authority. Any source path outside the five-path list remains
out of scope.

## Historical Impact Inventory — P1 Recurrence Candidate

The inventory inspected every completed Work Block with an explicit current
`governance_profile` of Managed, Assured, or Distributed. Historical completed
records that omit that profile are not assigned one by inference. A separate
specification counts only where the Work Block explicitly binds it as normative;
a path merely appearing in a write-set is not treated as that declaration.

| WB | Profile | Separate Spec | Spec Status | Completed | Would New Invariant Fail? | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| WB-CORE-003F | Managed | none explicitly declared | n/a | yes | no | no separate-spec obligation |
| WB-DEFINE-001 | Managed | none explicitly declared | n/a | yes | no | no separate-spec obligation |
| WB-OPENCODE-002 | Managed | none explicitly declared | n/a | yes | no | no separate-spec obligation |
| WB-REPO-GRAPH-001 | Managed | UNVERIFIED — `docs/specs/repository-graph-provider-contract.md` appears in the write-set but no normative binding is declared | approved | yes | no; outside explicit-binding selector | do not infer a binding retroactively |
| WB-SKILL-001 | Managed | `docs/specs/wb-skill-001-role-skill-convergence.md` explicitly marked Approved Specification | approved | yes | no | conforms |
| WB-SKILL-002 | Managed | `docs/specs/wb-skill-002-provider-neutral-verifier.md` explicitly marked Specification | `draft` at historical closeout; prospectively `approved` on 2026-08-21 | yes | historically yes; currently no | corrective target reconciled without retroactive cure |

Nineteen earlier completed Work Blocks omit `governance_profile`; their profile
and separate-spec applicability are **UNVERIFIED**, not inferred from old
`process_level` labels or prose references.

**Historical impact classification: BOUNDED COLLATERAL IMPACT.** The candidate
identified WB-SKILL-002, the current latest completed Work Block, and no other
completed Work Block with both an explicit formal profile and explicit separate
normative-specification binding. The bounded correction reconciled its current
authority prospectively while retaining the historical deviation record.

## Proposed Completion-Invariant Scope

The implemented smallest scope is **(a) latest completed Work Block only**,
with prospective effect at every successful closeout.
`validate-release-state.py`
already owns the canonical `release_state.latest_completed_work_block` boundary
and validates its plan and closeout projection. The implemented rule inspects
that Work Block only when all of the following are explicit and resolvable:

1. its `governance_profile` is Managed, Assured, or Distributed;
2. its deterministic sibling tasklist at
   `docs/tasklist/<latest-work-block-basename>` has an exact `work_block_id`
   and a present, non-empty, unique root-relative `specification` field; and
3. the field resolves to an existing `specification` artifact with the same
   `work_block_id` and status exactly `approved` under
   `governance/artifacts.md`.

The tasklist `specification` field is binding evidence for path resolution only;
the resolved approved specification remains the authority. A missing field
means no separate specification is declared and the invariant is skipped. The
validator fails closed when the deterministic sibling tasklist is
absent; a present field is empty, duplicated, malformed, or non-repository; the
target file does not exist or has the wrong artifact type; or the Work Block IDs
mismatch. It must not infer bindings for historical records that omit the field.

This gives every successful closeout the protection when it becomes the
latest completed record, avoids a speculative global migration of legacy plans,
and does not infer profile or specification authority for incomplete historical
metadata. WB-SKILL-002 was the genuine corrective target because it was latest
and explicitly bound a separate `draft` specification; its current
specification status is now prospectively `approved` without a retroactive cure.

The existing release-state validator owns the appropriate cross-artifact
enforcement point. The bounded correction added the corresponding narrowly
stated normative contract in `governance/release-state.md` before adding
validator behavior.

## Multiline Regression-Guard Investigation — P2

`require_absent_mandatory_provider_semantics` in
Before this correction, `scripts/test-sdd-contract.sh` lowered and evaluated
one physical line at a time. Its predicate required relevant
modal/provider/assurance or prerequisite terms to coexist in that line.
Ordinary Markdown wrapping therefore bypassed it:

```text
Provider review is
mandatory.

Installation is required
before verification.
```

The implemented guard uses paragraph-scoped normalization: the existing target
file remains the only scanned path; the predicate receives one normal-prose
paragraph at a time after internal ordinary-prose line breaks and repeated
whitespace are joined. Continuation lines within one list item are also joined.
Blank lines, ATX headings, separate list items, and fenced-code boundaries are
hard statement boundaries; fenced code is excluded from semantic matching. It
does not join the whole file, so terms in unrelated paragraphs, headings,
separate list items, or code cannot create a false match. A later bounded
corrective iteration also splits ordinary `, but` and `, however` contrasts
before applying negation and recognizes direct prerequisite imperatives after
common polite or purpose-clause introductions.

The contract tests exercise the actual predicate against
single-line, reordered, and wrapped prohibited prose; allowed advisory prose;
negative paragraph-separation; a prohibited same-list-item wrapping case; an
allowed cross-list-item case; ATX-heading-boundary; and fenced-code cases. This
corrects the prior AC-006 overclaim without changing
`skills/codex-verification/SKILL.md`.

## Approved Source Write-Set — Bounded Execute

| Path | Defect / invariant owner | Governing contract | Smallest sufficient change | Why no smaller owner exists |
| --- | --- | --- | --- | --- |
| `docs/specs/wb-skill-002-provider-neutral-verifier.md` | P1 current specification authority record | `governance/artifacts.md`, `governance/lifecycle.md` | Record the selected evidence-supported reconciliation with explicit temporal scope; no invented historical approval. | It is the artifact whose `draft` metadata caused P1. |
| `scripts/test-sdd-contract.sh` | P2 target-only semantic predicate and adversarial coverage | WB-SKILL-002A REQ-003/REQ-004 | Normalize only normal-prose paragraphs; test wrapped/allowed/separated plus heading/list/fenced-code boundaries through the same predicate. | The defective physical-line predicate and its executable contract live here. |
| `governance/release-state.md` | Normative statement of the new latest-completed invariant | `governance/release-state.md`, `governance/artifacts.md` | Define the tasklist field as binding evidence only and the resolved approved specification as authority. | Current release-state policy lacks this cross-artifact obligation; code alone would create undeclared policy. |
| `scripts/validate-release-state.py` | Deterministic enforcement at the release-state boundary | `governance/release-state.md` | Resolve the deterministic sibling tasklist; skip a missing field; fail every present malformed binding; validate the resolved approved specification only for the latest eligible completed Work Block. | It already owns `latest_completed_work_block`, closeout, and terminal projection validation. |
| `scripts/test-release-state-contracts.py` | Regression fixtures for the release-state invariant | `scripts/validate-release-state.py` contract suite | Add missing sibling tasklist, malformed present field, wrong type/ID, eligible-draft failure, eligible-approved pass, and no-declared-binding skip fixtures. | This is the existing executable fixture owner for that validator. |

The five paths above have been used for the bounded source Execute. In
particular, `skills/codex-verification/SKILL.md` remains expressly excluded.

Following independent-review findings, the bounded corrective iteration is
also authorized only for `scripts/test-sdd-contract.sh` and these two
coordination artifacts: this plan and its deterministic sibling tasklist. It
must not alter the accepted provider-neutral skill, historical authority facts,
or any pending Reviewer, Verifier, or Drift gate.

## Define Quality Prerequisite

```json
"define_quality": {
  "required": true,
  "status": "READY",
  "requirements_review": "READY — independent requirements-quality review",
  "traceability": "READY — python3 scripts/validate-define-traceability.py (requirements=8 acceptance=11 tasks=9)",
  "consistency_analysis": "READY — independent consistency analysis"
}
```

Define quality is READY: independent requirements-quality review, deterministic
traceability, and independent consistency analysis are complete. Critic is also
READY. The Owner has selected P1 branch B and separately prospectively approved
this specification revision plus the exact five-path source write-set. The
Write Gate is therefore READY for bounded source Execute only.

## Scope and Hard Stops

### Original Define-only authorized write-set

```text
docs/plans/wb-skill-002a-post-merge-reconciliation.md
docs/specs/wb-skill-002a-post-merge-reconciliation.md
docs/tasklist/wb-skill-002a-post-merge-reconciliation.md
```

### Explicitly out of scope

- any WB-SKILL-002 specification change beyond the approved prospective
  authority reconciliation recorded above;
- source/test/fixture/validator/governance changes outside the exact bounded
  Execute write-set and its later three-file corrective iteration;
- `skills/codex-verification/SKILL.md` or its accepted semantics;
- GitHub thread resolution, push, PR creation, merge, rebase, or default-branch
  mutation;
- Gemini recommendations, extensions, presets, workflows, bundles, converge
  loops, context pruning, verifier manifests, and broad legacy-skill cleanup;
- the unrelated untracked `Repository Graph Evaluation Brief.md`.

The approved source Execute and its narrow post-review correction are complete.
Frozen independent Reviewer, Verifier, and Drift assurance remain required
before terminal closeout. Any further expansion, GitHub action, or merge
remains prohibited without separate Owner authority.
