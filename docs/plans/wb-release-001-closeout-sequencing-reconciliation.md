---
schema_version: 1
artifact_type: work_block
artifact_id: wb-release-001-closeout-sequencing-reconciliation
work_block_id: WB-RELEASE-001
status: in_progress
owner_role: Owner
created_at: 2026-08-24
last_updated: 2026-08-24
governance_profile: Managed
branch: agent/wb-release-001-closeout-sequencing
base_revision: bc05d3c554225d77aa23a4d63c5a8dd41c37ea34
write_gate: READY
critic_gate: READY
review_gate: PENDING
verification_verdict: PENDING
drift_gate: PENDING
evaluation_verdict: NOT_REQUIRED
closeout_mode: pending
owner_approval: Owner authorized a corrective PR-history rewrite/force-push and directed prevention of recurrence after the exact-head Framework Contracts failure on 2026-08-24. Revision r5 adds its named direct CI consumer only; refreshed r5 Define assurance supports the exact approved Execute write-set. No candidate, push, PR, or merge authority is implied.
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

- **Current Stage:** Execute
- **Stage State:** in_progress
- **Write Gate:** READY
- **Critic Gate:** READY
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Evaluation Verdict:** NOT_REQUIRED
- **Drift Gate:** PENDING
- **Closeout Mode:** pending

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
before creating a new candidate. No source/config commit will be appended after
the renewed evidence-only commit.

## Repository Preflight

- **Clean isolated worktree:**
  `/home/azur/Projects/WSL/agentic-sdlc-framework-wb-release-001`.
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

### Source Write-Set: r4 Executed; r5 Expansion Proposed

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
proposes only `.github/workflows/framework-contracts.yml` and the corresponding
extension of `scripts/test-release-state-contracts.py`; it remains unexecuted
while the r5 Write Gate is `BLOCKED`.

| Path | Owner / smallest sufficient change |
| --- | --- |
| `governance/release-state.md` | Defines the authoritative two-mode release-state semantics and default fail-closed boundary. |
| `.agent/workflows/sdd-protocol.md` | Owns the self-hosting operational Close sequence. |
| `FILE_REGISTRY.yml` | Owns the machine-readable accepted evidence sequence. |
| `scripts/validate-release-state.py` | Owns deterministic ordinary/candidate validation and retains the fail-closed candidate-manifest boundary. |
| `scripts/test-release-state-contracts.py` | Executed r4 owner of canonical checkout-history regression proof; r5 proposes the smallest extension to cover the second named consumer. |
| `.github/workflows/release-state-contract.yml` | Owns CI checkout depth for the ancestry-dependent release-state validator. |
| `.github/workflows/framework-contracts.yml` | Proposed r5 owner of CI checkout depth for the separate `contracts` job that directly runs governance/release-state validation. |

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
python3 scripts/validate-release-state.py
python3 scripts/test-release-state-contracts.py
```

The future implementation must retain ordinary-mode checks unchanged, add the
full-history checkout to both named direct-consumer jobs, and make each
canonical workflow setting part of the release-state fixture proof.

## Resumption Rule

WB-CORE-003G may resume only after WB-RELEASE-001 reaches a validated and
approved closeout. Its existing status-only projection must then be rebuilt or
rechecked against the current `main` and the accepted candidate procedure; no
old local candidate is silently promoted.
