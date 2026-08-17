---
schema_version: 1
artifact_type: verification_report
artifact_id: wb-repository-graph-001-corrective-verification
work_block_id: WB-REPO-GRAPH-001-CORRECTIVE
verified_stage: assure
assured_subject_sha: c94640950e528294b3cfab1a0b3f12c88923f7a8
parent_sha: a75ee9a0782ba84f555a2ce34c99b8e7f30420c1
verdict: READY
created_at: 2026-08-17
isolation: independent_github_repository_strict_read_only
recorded_by_role: orchestrator
---

# Corrective Verification Evidence — WB-REPO-GRAPH-001

## Recorded independent verdict

**READY.** This evidence-only record faithfully preserves the supplied
independent GitHub/repository strict-read-only Verifier result. The Verifier
did not mutate this repository; the Orchestrator records its supplied outcome.

## Assured subject and CI evidence

- **Assured subject SHA:** `c94640950e528294b3cfab1a0b3f12c88923f7a8`
- **Parent SHA:** `a75ee9a0782ba84f555a2ce34c99b8e7f30420c1`
- **Ancestry/path/stat proof:** one parent; exactly three paths; 189 additions
  and 5 deletions.

The ordered manifest is:

```text
bootstrap/profiles.json
docs/plans/wb-repository-graph-001-corrective-reconciliation.md
scripts/test-integration-contracts.py
```

Reported CI evidence for this exact head:

| Check | Result | Head SHA |
| --- | --- | --- |
| Release State Contract #843 | SUCCESS | `c94640950e528294b3cfab1a0b3f12c88923f7a8` |
| Framework Contracts #1261 | SUCCESS | `c94640950e528294b3cfab1a0b3f12c88923f7a8` |

## Verified evidence

- Installation-profile/runtime and integration-adapter full suites succeeded,
  as did governance, release-state, and publication-scaffold validation.
- A disposable generated-project bootstrap succeeded; the primary worktree was
  not used destructively.
- `scripts/test-integration-contracts.py` was invoked. Both Repository Graph
  documents are `common_required_paths`, all profiles and aliases are covered,
  and generated `required_paths` includes both documents.
- Deleting either document causes a non-zero installation-validator result and
  reports the exact missing path on stderr.
- Generated components and integrations contain no Repository Graph activation.

## Residual limitation

Successful redirected integration stdout was not retained as a standalone
artifact. Job success plus inspected invocation and source provide the recorded
evidence. Historical checksum
`6f9edc54a475eb3b380f5a9601e8a7eb7b822c6e6a9787600ff1e729e2b2df6f`
remains historically non-reproducible.
