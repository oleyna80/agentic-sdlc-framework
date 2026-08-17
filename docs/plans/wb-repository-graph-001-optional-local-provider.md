---
schema_version: 1
artifact_type: work_block
work_block_id: WB-REPO-GRAPH-001
status: completed
created_at: 2026-08-11
governance_profile: Managed
base_revision: 13c9f8fbb1659db8224cc0173d9e811abcf790af
---

# WB-REPO-GRAPH-001 — Optional Local Repository Graph Provider

## Lifecycle State

- **Current Stage:** Close
- **Stage State:** completed
- **Write Gate:** READY — single-Coder write gate
- **Critic Gate:** APPROVE_WITH_CHANGES — all conditions incorporated below
- **Review / Verification / Drift:** final Reviewer READY; final Verifier READY; drift ALIGNED
- **Evaluation lifecycle meaning:** `not_required`; this is deterministic documentation, registry,
  scaffold-fixture, and static-contract work with no provider evaluation.
- **Closeout lifecycle meaning:** `success`; the completed close is limited to
  this deterministic documentation-only capability.

## Completion Record

- **Implementation base:** `13c9f8fbb1659db8224cc0173d9e811abcf790af`
- **Corrected implementation freeze:**
  `6f9edc54a475eb3b380f5a9601e8a7eb7b822c6e6a9787600ff1e729e2b2df6f`
- **Critic:** APPROVE_WITH_CHANGES; all conditions were incorporated before Execute.
- **Preliminary Reviewer:** CHANGES_REQUIRED for (1) the template registry's
  incorrect `integration_adapter` classification and (2) insufficient explicit
  negative-boundary assertions. Both corrections were made, refrozen, and the
  final Reviewer verdict is READY.
- **Final Verifier:** READY. **Drift:** ALIGNED.
- **Publication evidence:** the publication validator passed in a temporary
  clean copy of the changed subject after excluding only the preserved untracked
  `Repository Graph Evaluation Brief.md`; the primary worktree was not mutated
  or staged to obtain that evidence.

Evidence records preserve the independent read-only verdicts; they are not
reports authored by assurance agents in this repository.

## Objective and Acceptance Criteria

Declare a provider-neutral optional Repository Graph Provider boundary without
admitting or operating any provider. Delivery must provide the contract, ADR,
unadmitted integration guide, generated opt-in record, navigation/registry
classification, deterministic positive/negative assertions, and publication
inventory coverage.

Acceptance requires that all materials state local derived rebuildable
non-authoritative state; direct canonical-source confirmation for important
findings; state binding and material-change refresh; no default publication;
and no authority, write-set, approval, assurance, canonical-memory, or sole
change-basis effect. Every supported bootstrap profile must receive the opt-in
record and relevant graph-provider documentation without invoking a provider.

## Scope and Write-Set

Only these paths are authorized:

```text
docs/specs/repository-graph-provider-contract.md
docs/architecture/decisions/2026-08-11-repository-graph-provider-boundary.md
docs/plans/wb-repository-graph-001-optional-local-provider.md
integrations/repository-graph/README.md
integrations/README.md
README.md
SETUP.md
PROJECT_MAP.md
FILE_REGISTRY.yml
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
template/docs/templates/repository-graph-opt-in-template.md
scripts/test-integration-contracts.py
scripts/validate_publication.py
```

Out of scope: provider installation/configuration/index/query; MCP/API keys;
hooks/runtime configuration; embeddings/uploads/credentials; `.gitignore` or
bootstrap-profile changes; provider performance/compatibility claims; network
activity; candidate promotion; downstream project work; staging, commit, push,
or publication.

## Final State

- **Stage State:** completed
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Evaluation Verdict:** SKIPPED — deterministic documentation and contract
  validation; no provider evaluation is claimed.
- **Closeout Mode:** success-closeout
- **Task status:** completed
- **Closeout classification:** SUCCESS
- **Critic evidence:** `docs/reports/reviews/wb-repository-graph-001-critic.md`
- **Review evidence:** `docs/reports/reviews/wb-repository-graph-001-review.md`
- **Verification evidence:**
  `docs/reports/verification/wb-repository-graph-001-verification.md`
- **Drift evidence:** `docs/reports/drift/wb-repository-graph-001-drift.md`
- **Closeout record:**
  `docs/reports/closeout/wb-repository-graph-001-optional-local-provider.md`

The Final State values above are the repository release-state projection tokens
required by `governance/release-state.md`. Semantically, evaluation is
`not_required` and Close completed successfully; `SKIPPED` and
`success-closeout` do not record provider evaluation or a different lifecycle.

Residual limitation: no provider was chosen, installed, configured, indexed,
queried, or evaluated. Future provider admission requires a separate
Owner-approved Work Block, and local exclusion verification remains the
project/operator's responsibility.

## Hard Stops and Assurance

The Work Block prohibits provider installation/configuration, indexing, MCP/API,
hooks, runtime configuration, embeddings/uploads, credentials, and provider
admission or invocation. Any future project use requires separately
Owner-approved scope. Preserve the untracked `Repository Graph Evaluation
Brief.md` unchanged. Freeze the integrated subject before independent Reviewer,
Verifier, and drift assurance. This completed closeout is limited to the
deterministic documentation-only capability and does not select, install,
configure, index, query, evaluate, invoke, or admit a provider.

## Checks

Run `git diff --check`, integration contracts (including the equivalent
all-supported-profile fixture), bootstrap-profile contracts, SDD/governance and
release-state contracts, plus publication validation on a temporary clean copy
that excludes only the known untracked brief. The primary worktree is not staged
or mutated to obtain publication evidence.
