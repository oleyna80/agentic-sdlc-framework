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
write_gate: BLOCKED
critic_gate: READY
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
evaluation_verdict: NOT_REQUIRED
owner_approval: Owner approved Define-only investigation and creation of exactly this Work Block's plan, specification, and tasklist on 2026-08-21; no source implementation, GitHub action, or merge authority is granted.
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

**Expected Final Result:** a future frozen correction can truthfully reconcile
the WB-SKILL-002 specification, detect wrapped mandatory-provider semantics in
the existing target-only guard, and reject the same eligible condition at the
latest-completed release-state boundary without changing the accepted skill.

## Current Define State

- **Current Stage:** Define
- **Stage State:** completed — Define investigation, requirements quality,
  consistency analysis, and Critic review are complete; the Work Block itself
  remains in progress and has not entered Execute.
- **Write Gate:** BLOCKED — neither required Owner precondition for source
  Execute has been recorded.
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

### Future Owner Decision Boundary

No branch is selected in this Define-only run:

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
are distinct decisions. This Define run does not change the old specification
from `draft` to `approved`.

### Required Owner Decision Before P1 Execute

Before TASK-001 may alter
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
the decision's historical or prospective temporal scope. Until it exists,
**P1 Execute and prior-specification metadata changes are BLOCKED**. This gate
does not permit a C record to silently select a historical answer, and this
Define-only artifact intentionally records no selection.

### Required Owner Approval Before WB-SKILL-002A Execute

After the P1 historical decision is recorded but before any source Execute, the
Owner must separately approve both this Work Block's then-current specification
in `approved` status and the exact frozen source write-set. The approval record
must identify the specification revision, every authorized source path, and the
prospective execution scope. It must expressly state that it neither proves
pre-Execute approval for WB-SKILL-002 nor retroactively cures that historical
process record. Until that approval is recorded, **all WB-SKILL-002A source
Execute remains BLOCKED**.

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
| WB-SKILL-002 | Managed | `docs/specs/wb-skill-002-provider-neutral-verifier.md` explicitly marked Specification | draft | yes | yes | corrective target |

Nineteen earlier completed Work Blocks omit `governance_profile`; their profile
and separate-spec applicability are **UNVERIFIED**, not inferred from old
`process_level` labels or prose references.

**Historical impact classification: BOUNDED COLLATERAL IMPACT.** The candidate
would identify WB-SKILL-002, the current latest completed Work Block, and no
other completed Work Block with both an explicit formal profile and explicit
separate normative-specification binding.

## Proposed Completion-Invariant Scope

The smallest justified scope is **(a) latest completed Work Block only**, with
prospective effect at every successful closeout. `validate-release-state.py`
already owns the canonical `release_state.latest_completed_work_block` boundary
and validates its plan and closeout projection. The future rule should inspect
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
future validator must fail closed when the deterministic sibling tasklist is
absent; a present field is empty, duplicated, malformed, or non-repository; the
target file does not exist or has the wrong artifact type; or the Work Block IDs
mismatch. It must not infer bindings for historical records that omit the field.

This gives every future successful closeout the protection when it becomes the
latest completed record, avoids a speculative global migration of legacy plans,
and does not infer profile or specification authority for incomplete historical
metadata. WB-SKILL-002 remains a genuine current corrective target because it
is presently latest and explicitly binds a separate `draft` specification.

The existing release-state validator owns the appropriate cross-artifact
enforcement point, but `governance/release-state.md` does not yet define this
requirement. The future correction therefore needs a narrowly stated normative
contract before adding validator behavior.

## Multiline Regression-Guard Investigation — P2

`require_absent_mandatory_provider_semantics` in
`scripts/test-sdd-contract.sh` lowers and evaluates one physical line at a time.
Its predicate requires relevant modal/provider/assurance or prerequisite terms
to coexist in that line. Ordinary Markdown wrapping therefore bypasses it:

```text
Provider review is
mandatory.

Installation is required
before verification.
```

The future smallest design is paragraph-scoped normalization: the existing
target file remains the only scanned path; the predicate receives one normal
prose paragraph at a time after internal ordinary-prose line breaks and repeated
whitespace are joined. Continuation lines within one list item are also joined.
Blank lines, ATX headings, separate list items, and fenced-code boundaries are
hard statement boundaries; fenced code is excluded from semantic matching. It
must not join the whole file, so terms in unrelated paragraphs, headings,
separate list items, or code cannot create a false match.

The future contract tests must exercise the actual predicate against
single-line, reordered, and wrapped prohibited prose; allowed advisory prose;
negative paragraph-separation; a prohibited same-list-item wrapping case; an
allowed cross-list-item case; ATX-heading-boundary; and fenced-code cases. This
corrects the prior AC-006 overclaim without changing
`skills/codex-verification/SKILL.md`.

## Proposed Future Implementation Write-Set — NOT AUTHORIZED

| Path | Defect / invariant owner | Governing contract | Smallest sufficient change | Why no smaller owner exists |
| --- | --- | --- | --- | --- |
| `docs/specs/wb-skill-002-provider-neutral-verifier.md` | P1 current specification authority record | `governance/artifacts.md`, `governance/lifecycle.md` | Record the selected evidence-supported reconciliation with explicit temporal scope; no invented historical approval. | It is the artifact whose `draft` metadata caused P1. |
| `scripts/test-sdd-contract.sh` | P2 target-only semantic predicate and adversarial coverage | WB-SKILL-002A REQ-003/REQ-004 | Normalize only normal-prose paragraphs; test wrapped/allowed/separated plus heading/list/fenced-code boundaries through the same predicate. | The defective physical-line predicate and its executable contract live here. |
| `governance/release-state.md` | Normative statement of the new latest-completed invariant | `governance/release-state.md`, `governance/artifacts.md` | Define the tasklist field as binding evidence only and the resolved approved specification as authority. | Current release-state policy lacks this cross-artifact obligation; code alone would create undeclared policy. |
| `scripts/validate-release-state.py` | Deterministic enforcement at the release-state boundary | `governance/release-state.md` | Resolve the deterministic sibling tasklist; skip a missing field; fail every present malformed binding; validate the resolved approved specification only for the latest eligible completed Work Block. | It already owns `latest_completed_work_block`, closeout, and terminal projection validation. |
| `scripts/test-release-state-contracts.py` | Regression fixtures for the release-state invariant | `scripts/validate-release-state.py` contract suite | Add missing sibling tasklist, malformed present field, wrong type/ID, eligible-draft failure, eligible-approved pass, and no-declared-binding skip fixtures. | This is the existing executable fixture owner for that validator. |

No source path is authorized by this Define artifact. In particular,
`skills/codex-verification/SKILL.md` is expressly excluded.

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
READY. These results complete Define investigation only; they do not open the
Write Gate or grant source authority. Source Execute remains BLOCKED until both
the P1 A/B/C Owner decision and the separate prospective approval of this Work
Block's approved specification plus exact source write-set are recorded.

## Scope and Hard Stops

### Define-only authorized write-set

```text
docs/plans/wb-skill-002a-post-merge-reconciliation.md
docs/specs/wb-skill-002a-post-merge-reconciliation.md
docs/tasklist/wb-skill-002a-post-merge-reconciliation.md
```

### Explicitly out of scope

- any current change to the WB-SKILL-002 specification or its `draft` status;
- source/test/fixture/validator/governance changes;
- `skills/codex-verification/SKILL.md` or its accepted semantics;
- GitHub thread resolution, push, PR creation, merge, rebase, or default-branch
  mutation;
- Gemini recommendations, extensions, presets, workflows, bundles, converge
  loops, context pruning, verifier manifests, and broad legacy-skill cleanup;
- the unrelated untracked `Repository Graph Evaluation Brief.md`.

Source implementation is prohibited until Define-quality readiness, independent
consistency analysis, Critic review, and a separately approved future write-set
produce a READY Write Gate.
