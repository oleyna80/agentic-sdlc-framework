---
schema_version: 1
artifact_type: work_block
artifact_id: wb-repository-graph-001-corrective-reconciliation
work_block_id: WB-REPO-GRAPH-001-CORRECTIVE
status: assurance_pending
created_at: 2026-08-17
governance_profile: Managed
base_revision: a75ee9a0782ba84f555a2ce34c99b8e7f30420c1
---

# WB-REPO-GRAPH-001-CORRECTIVE — Assurance and Profile Reconciliation

## Objective

Correct exactly three unresolved PR #27 findings without reopening, changing,
or recharacterising the completed WB-REPO-GRAPH-001 provider boundary. This
corrective Work Block records the historical assurance-subject limitation,
separates implementation from evidence authority prospectively, and makes the
two existing Repository Graph documentation files required in every generated
profile. It does not select, install, configure, invoke, index, query, or admit
a provider.

## Historical assurance limitation

The historical Reviewer READY, Verifier READY, and Drift ALIGNED records name
`6f9edc54a475eb3b380f5a9601e8a7eb7b822c6e6a9787600ff1e729e2b2df6f` as a
corrected implementation freeze. It is not a Git object, and no committed
algorithm or path manifest proves which exact integrated Git revision it
identified. `4f2d55f` and `d930eb4` are archival delivery commits on different
bases, not evidence that either was the checksum subject.

Accordingly, this corrective record does not retrofit a Git SHA into the
historical assurance records or claim that they assured the corrective state.
Those records remain honest historical evidence with a non-reproducible subject
limitation.

## Authority and write sets

### Coder implementation write set

The one Coder may change only:

```text
bootstrap/profiles.json
scripts/test-integration-contracts.py
```

This is limited to required documentation inventory and its deterministic
contract coverage. It does not grant authority to write evidence records or
expand the historical WB-REPO-GRAPH-001 implementation scope.

### Orchestrator coordination and evidence write set

The Orchestrator may write this corrective Work Block and, only after the named
role has supplied its independent result, faithfully record that result in:

```text
docs/plans/wb-repository-graph-001-corrective-reconciliation.md
docs/reports/reviews/wb-repository-graph-001-corrective-review.md
docs/reports/reviews/wb-repository-graph-001-corrective-drift.md
docs/reports/verification/wb-repository-graph-001-corrective-verification.md
docs/reports/closeout/wb-repository-graph-001-corrective-reconciliation.md
```

Reviewer, Verifier, Critic, and Drift roles remain read-only over the
implementation subject. An evidence record is a coordination artifact written
by its designated authority only; it never enlarges the Coder write set. The
historical mismatch is corrected prospectively rather than asserted as
historical Coder authority.

## Fresh assurance subject

After deterministic implementation checks pass, the Owner-authorized one local
corrective commit freezes the subject. Push, PR metadata changes, review-thread
resolution, merge, rebase, reset, and every remote action remain prohibited.

Independent Reviewer, Verifier, and Drift assurance must bind to both the exact
post-correction commit SHA and this ordered normative path manifest:

```text
bootstrap/profiles.json
docs/plans/wb-repository-graph-001-corrective-reconciliation.md
scripts/test-integration-contracts.py
```

The assurance records themselves are excluded from that subject to prevent
circular self-attestation. Each independent role must recompute the manifest
from the named commit, reject missing or duplicate paths, and record the exact
SHA and ordered paths in its own evidence. Any later normative edit invalidates
that assurance and requires a new freeze.

## Required behavior and checks

- `common_required_paths` must include
  `integrations/repository-graph/README.md` and
  `docs/templates/repository-graph-opt-in-template.md`.
- Every supported profile and alias must resolve both files into generated
  `.agent/bootstrap-profile.json.required_paths`.
- A temporary generated project missing either file must fail
  `scripts/validate-installation-profile.py` with that path reported missing.
- Documentation inventory is not provider activation: no profile or alias may
  select a Repository Graph component or integration, and no component may own
  either documentation path.
- Existing non-activation boundaries remain intact: no provider selection,
  installation, configuration, invocation, indexing/querying, MCP/API,
  hooks, runtime configuration, credentials, embeddings, uploads, or generic
  graph ignore rule.

Run the Owner-required deterministic suite, including the disposable negative
deletion fixtures. Preserve the sole unrelated local item, untracked
`Repository Graph Evaluation Brief.md`, unchanged and uncommitted.

## Lifecycle state

- **Stage:** Assure
- **Execution state:** completed; deterministic implementation checks passed,
  including the required disposable deletion fixtures and publication validation
  in the prescribed clean copy.
- **Critic gate:** APPROVE_WITH_CHANGES — incorporated: local commit freeze is
  explicitly authorized and structural non-activation assertions are required.
- **Review / Verification / Drift:** pending independent assurance after the
  local corrective commit.
- **Closeout mode:** pending; this record must not claim READY, ALIGNED, or
  successful closeout before those independent results exist.

## Out of scope and hard stops

Provider choice or operation; provider installation/configuration; MCP/API;
indexing/querying; embeddings/uploads; credentials/keys; runtime or hook
configuration; new graph ignore rules; dependencies; broad refactors; changes
to historical evidence; modifying the untracked brief; push; review-thread
resolution; PR metadata changes; merge; rebase; reset; destructive operations;
and default-branch changes are out of scope.
