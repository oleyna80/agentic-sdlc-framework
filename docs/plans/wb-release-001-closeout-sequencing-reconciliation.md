---
schema_version: 1
artifact_type: work_block
artifact_id: wb-release-001-closeout-sequencing-reconciliation
work_block_id: WB-RELEASE-001
status: closeout_candidate
owner_role: Owner
created_at: 2026-08-24
last_updated: 2026-08-24
governance_profile: Managed
branch: agent/wb-release-001-closeout-sequencing
base_revision: bc05d3c554225d77aa23a4d63c5a8dd41c37ea34
write_gate: BLOCKED
critic_gate: READY
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
evaluation_verdict: NOT_REQUIRED
closeout_mode: candidate
owner_approval: Owner authorized the local pre-closeout candidate and its bounded final assurance/evidence-persistence sequence on 2026-08-24. This grants no PR, merge, or default-branch authority.
---

# WB-RELEASE-001 — Release-State Closeout Sequencing Reconciliation

## Objective

Repair the release-state sequencing contract exposed by the WB-CORE-003G pilot:
the accepted terminal-assurance sequence requires a status-only normative
subject, but the ordinary release-state validator correctly rejects that
intermediate subject before its closeout evidence exists.

## Expected Final Result

The framework has one bounded, prospective, fail-closed procedure for a local
pre-closeout candidate. A persistent machine-readable `closeout_candidate` /
`assurance_pending` record and projection permit independent final assurance
without claiming successful closeout. The authoritative contract derives
completion only from that immutable declaration plus bound terminal evidence;
an evidence-only persistence commit is cross-revision checked before ordinary
release-state validation or CI can pass. WB-CORE-003G can then resume without
relying on a contract-invalid published intermediate state.

## Current State

- **Current Stage:** Close
- **Stage State:** assurance_pending
- **Write Gate:** BLOCKED
- **Critic Gate:** READY
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation Verdict:** NOT_REQUIRED
- **Drift Gate:** PENDING
- **Closeout Mode:** candidate

Evaluation is not required because this is deterministic governance and
validator reconciliation; it introduces no non-deterministic product behavior.

## Normative Baseline

- **Approved Specification:** `docs/specs/wb-release-001-closeout-sequencing-reconciliation.md`
  (revision r5; refreshed requirements, consistency, and Critic assurance recorded below).
- **Derived Tasklist:** `docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md`.
- **Governing contracts:** `governance/release-state.md`,
  `governance/lifecycle.md`, `governance/artifacts.md`, `governance/authority.md`,
  `.agent/workflows/sdd-protocol.md`, and `FILE_REGISTRY.yml`.
- **Implementation owners under investigation:**
  `scripts/validate-release-state.py` and
`scripts/test-release-state-contracts.py`.

The published first candidate/evidence pair was deliberately abandoned before
force-push: CI showed that `.github/workflows/release-state-contract.yml`
checked out a shallow repository, so the ancestry proof could not run. Revision
r4 corrected it, but exact-head CI then showed the independently checked out
`contracts` job in `.github/workflows/framework-contracts.yml` runs the same
ancestry-dependent validation with shallow history. The replacement must cover
both identified direct consumers and a narrowly-owned regression assertion
before creating a new candidate.

### Corrective Reopening r7

The exact-head independent review of r6 identified three implementation
fail-open defects within the existing REQ-002, REQ-004, REQ-005, REQ-007 and
AC-005, AC-006, AC-008 boundaries: the ordinary validator did not bind the
current HEAD to the persisted candidate normative manifest; it did not apply
the existing formal-specification authority check to an effective candidate;
and it accepted a candidate while an unrelated active Work Block existed.

The r6 candidate declaration and its reports are historical, superseded
assurance artifacts. They do not cover the forthcoming corrective source
subject and must not be used to claim closeout. This Work Block is returned to
ordinary active state before source changes. The corrective implementation is
limited to the validator, its deterministic fixture suite, and the one
governing sentence that otherwise overstates later-merge safety.

Fresh r7 Critic review assessed this bounded interpretation of the existing
approved requirements as `APPROVE_WITH_CHANGES`: every declared manifest path
must be bound at current HEAD; fixtures must cover direct and merge-result
mutations, formal-specification authority, and candidate/active coexistence;
and candidate-mode formal-specification policy must not be broadened. Those
conditions are the exact scope of TASK-020.

TASK-020 completed those three deterministic guards. Its corrected frozen r7
source subject received independent Review, fresh-clone Verification, and Drift
assurance before the renewed candidate declaration.

Fresh r7 Verification blocked the first source subject because it exposed a
remaining fail-open: a Managed candidate missing its sibling tasklist could
avoid formal-specification validation. The same-scope correction was completed
and freshly assured before the renewed candidate declaration.

The corrected frozen r7 subject `0a9fa6eec4f585592c06f7168071265598b90219`
received independent Reviewer `READY`, fresh-clone Verifier `READY`, and Drift
`ALIGNED`. The earlier blocked verification remains historical evidence of the
defect discovery; it is not relabelled or used as current assurance.

### Pre-Closeout Candidate r8

The current raw state is a local-only `closeout_candidate` for the already
assured r7 source subject. Its normative manifest is restricted to this Work
Block, `FILE_REGISTRY.yml`, and `PROJECT_MAP.md`; it declares no successful
closeout, promotion, CI result, PR, or merge. Independent final Reviewer,
fresh-clone Verifier, and Drift assurance must bind this exact candidate before
the separately persisted evidence-only completion record may be validated in
ordinary mode.

## Repository Preflight

- **Clean isolated worktree:** dedicated to this Work Block and separate from
  the Owner's normal checkout.
- **Branch/baseline:** `agent/wb-release-001-closeout-sequencing` at
  `bc05d3c554225d77aa23a4d63c5a8dd41c37ea34`.
- **Original pilot checkout:** remains on
  `agent/wb-core-003g-define-refresh` with four uncommitted status-only
  projection files plus the Owner's unrelated
  `Repository Graph Evaluation Brief.md`; none are in this worktree or scope.

## Findings and Design Boundary

The ordinary validator requires `latest_completed_work_block` to be the final
registry entry and requires its successful closeout report. The accepted
`FILE_REGISTRY.yml` evidence sequence instead places a `status_only_normative_commit`
before final applicable assurance and an `evidence_only_report_commit` after it.
The WB-CORE-003G candidate exposed the contradiction: `git diff --check` and
source checks passed, while ordinary release-state/governance validation failed
solely because no final closeout report could truthfully exist yet.

Historical WB-SKILL-002A/B terminal projection commits included a success
closeout before later terminal assurance reports were persisted. Their later
reports correctly bound the terminal subject, but the recorded sequence leaves
the completion claim temporally ambiguous. This Work Block corrects the
prospective contract only; it does not rewrite those records.

## Scope

### Define and Coordination Artifacts

```text
docs/plans/wb-release-001-closeout-sequencing-reconciliation.md
docs/specs/wb-release-001-closeout-sequencing-reconciliation.md
docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md
```

### Executed Source Write-Set and Corrective r7 Write-Set

```text
governance/release-state.md
.agent/workflows/sdd-protocol.md
FILE_REGISTRY.yml
scripts/validate-release-state.py
scripts/test-release-state-contracts.py
.github/workflows/release-state-contract.yml
.github/workflows/framework-contracts.yml
```

The first six paths were executed and assured under revision r4. Revision r5
executes only `.github/workflows/framework-contracts.yml` and the corresponding
extension of `scripts/test-release-state-contracts.py`. Corrective r7 changes
only `governance/release-state.md`, `scripts/validate-release-state.py`, and
`scripts/test-release-state-contracts.py`; fresh assurance of that complete
subject completed before the current candidate was declared.

| Path | Owner / smallest sufficient change |
| --- | --- |
| `governance/release-state.md` | Defines the authoritative two-mode release-state semantics and default fail-closed boundary. |
| `.agent/workflows/sdd-protocol.md` | Owns the self-hosting operational Close sequence. |
| `FILE_REGISTRY.yml` | Owns the machine-readable accepted evidence sequence. |
| `scripts/validate-release-state.py` | Owns deterministic ordinary/candidate validation and retains the fail-closed candidate-manifest boundary. |
| `scripts/test-release-state-contracts.py` | Executed r4 owner of canonical checkout-history regression proof; r5 extends it only to cover the second named consumer. |
| `.github/workflows/release-state-contract.yml` | Owns CI checkout depth for the ancestry-dependent release-state validator. |
| `.github/workflows/framework-contracts.yml` | Executed r5 owner of CI checkout depth for the separate `contracts` job that directly runs governance/release-state validation. |

No template, source skill, historical Work Block, closeout report, or
`PROJECT_MAP.md` change is authorized for Execute. `PROJECT_MAP.md` may be an
approved terminal-projection path only during WB-RELEASE-001 Close, if the
contract change itself completes successfully.

### Out of Scope

- Modifying the four uncommitted WB-CORE-003G pilot files or closing that Work
  Block before this contract is accepted.
- Retrofitting old closeout reports, relabeling old assurance, or changing
  historical completed Work Blocks.
- Any source/product/runtime/provider change, dependency, credential, GitHub
  thread action, push, PR, merge, rebase, or default-branch mutation.

## Design Options Considered

| Option | Result | Disposition |
| --- | --- | --- |
| Keep the current sequence and tolerate failed ordinary validation | Preserves wording but leaves a known contract-invalid intermediate state. | Rejected. |
| Put a successful closeout report in the terminal projection before terminal assurance | Lets ordinary validation pass but makes the success claim temporally ambiguous. | Rejected. |
| Add a blanket validator exception for any missing latest closeout | Weakens the default fail-closed guarantee and permits accidental incomplete heads. | Rejected. |
| Explicit local-only pre-closeout candidate mode plus ordinary final mode | Uses a persistent `closeout_candidate`/`assurance_pending` record, a two-part canonical completion rule, distinct `CANDIDATE_READY` output, and an exact candidate-to-evidence diff proof; it is deliberate, testable, non-promotable, and limited to terminal assurance sequencing. | Recommended, pending refreshed Define assurance. |

## Define Quality and Assurance Plan

Managed Define quality is required. The current evidence is:

```text
Requirements Review: READY — `docs/reports/requirements/wb-release-001-closeout-sequencing-reconciliation-workflow-history-r5.md`.
Traceability: READY — `requirements=11 acceptance=12 tasks=18` on revision r5.
Consistency Analysis: READY — `docs/reports/requirements/wb-release-001-closeout-sequencing-reconciliation-workflow-history-r5-consistency.md`.
Critic: READY — `docs/reports/reviews/wb-release-001-closeout-sequencing-reconciliation-workflow-history-r5-critic.md`.
Aggregate: READY
```

The prior independent requirements/consistency pass and Critic critique found
that durable candidate semantics and cross-revision evidence proof must be
specified before source approval. Revision r4 added one discovered CI history
prerequisite, but exact-head CI demonstrated that its named-consumer inventory
was incomplete. Revision r5 adds only the second observed direct consumer and
extends the narrow deterministic guard to both known jobs. Fresh requirements,
consistency, Critic, and traceability evidence supports the r5 Write Gate for
the exact source write-set. After execution, require independent Reviewer,
fresh-clone Verifier, and Drift assurance on the frozen implementation subject;
no candidate mode may authorize a push, PR, merge, CI claim, or external action.

## Validation Plan

Define structural validation:

```bash
git diff --check
python3 scripts/validate-define-traceability.py \
  --spec docs/specs/wb-release-001-closeout-sequencing-reconciliation.md \
  --tasks docs/tasklist/wb-release-001-closeout-sequencing-reconciliation.md
bash scripts/test-sdd-contract.sh
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
python3 scripts/validate-release-state.py
python3 scripts/test-release-state-contracts.py
```

The future implementation must retain ordinary-mode checks unchanged, add the
full-history checkout to both named direct-consumer jobs, and make each
canonical workflow setting part of the release-state fixture proof. Before a
candidate is declared, the same publication validator used by Framework
Contracts must pass in the isolated checkout; this prevents local-path or
private-marker publication failures from surfacing only after push.

## Resumption Rule

WB-CORE-003G may resume only after WB-RELEASE-001 reaches a validated and
approved closeout. Its existing status-only projection must then be rebuilt or
rechecked against the current `main` and the accepted candidate procedure; no
old local candidate is silently promoted.
