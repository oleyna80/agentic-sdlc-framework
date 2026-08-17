---
schema_version: 1
artifact_type: drift_report
artifact_id: wb-repository-graph-001-corrective-drift
work_block_id: WB-REPO-GRAPH-001-CORRECTIVE
subject_base_revision: a75ee9a0782ba84f555a2ce34c99b8e7f30420c1
assured_subject_sha: c94640950e528294b3cfab1a0b3f12c88923f7a8
verdict: ALIGNED
created_at: 2026-08-17
isolation: external_read_only_drift_pass
recorded_by_role: orchestrator
---

# Corrective Drift Evidence — WB-REPO-GRAPH-001

## Recorded independent verdict

**ALIGNED.** This record faithfully preserves the supplied external read-only
Drift pass. It is an evidence-only Orchestrator record, not a claim that the
Drift role wrote implementation or evidence in this repository.

## Assured comparison

```text
a75ee9a0782ba84f555a2ce34c99b8e7f30420c1
->
c94640950e528294b3cfab1a0b3f12c88923f7a8
```

The assured subject is `c94640950e528294b3cfab1a0b3f12c88923f7a8` with this
ordered manifest:

```text
bootstrap/profiles.json
docs/plans/wb-repository-graph-001-corrective-reconciliation.md
scripts/test-integration-contracts.py
```

The comparison contains exactly one corrective commit and exactly three
corrective paths. The parent already incorporates exact main
`1f1ca40de1fb93abdf36715e5dbb0f8b9b19dd37`.

## Alignment result

- The correction maps only to F-01, F-02, and F-03.
- No Repository Graph architecture expansion, provider activation, provider
  admission, permanent governance redesign, or hidden lifecycle-authority
  change was found.
- The simplest sufficient correction is preserved:
  `EXACT_SINGLE_PARENT`, `EXACT_3_PATH_189_5`, and an exact SHA-plus-manifest
  assurance subject.

## Residual limitation

Historical checksum
`6f9edc54a475eb3b380f5a9601e8a7eb7b822c6e6a9787600ff1e729e2b2df6f`
remains an unreconstructable historical assurance subject. This evidence does
not rewrite that history.
