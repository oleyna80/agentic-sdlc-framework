# Release-State and SSOT Reconciliation Contract

## Purpose

This contract defines the repository-owned lifecycle state required before a
framework change may be treated as release-ready. It prevents completed Work
Blocks, navigation maps, machine registries, and closeout evidence from describing
contradictory states.

## Ownership Boundary

The repository owns and versions:

- Work Block lifecycle and verdicts;
- completed and active migration paths;
- review, verification, evaluation, drift, and closeout evidence;
- release-readiness classification based on repository evidence.

GitHub owns mutable operational state such as:

- whether a pull request is Draft or Ready;
- whether it is open, closed, or merged;
- merge timestamps and merge commit SHAs;
- requested reviewers and branch deletion state.

Mutable GitHub state may be cited in an external notification or appended by a
separate post-merge record, but it must not be required as normative content of a
pre-merge closeout commit. A closeout report records `repository closeout`, not a
prediction of later GitHub state.

## Canonical Sources

1. Work Block frontmatter and current-state section define the lifecycle of that
   Work Block.
2. `FILE_REGISTRY.yml:migration_state` is the machine-readable index of completed
   and active migration Work Blocks.
3. `PROJECT_MAP.md` is the human-readable projection of the same migration state.
4. Closeout reports provide evidence and classification; they do not override the
   Work Block or registry.
5. GitHub PR/merge state is external operational evidence and cannot override
   repository authority.

## Required Invariants

### Completed Work Blocks

A path listed in `completed_work_blocks` must:

- exist under `docs/plans/`;
- contain Work Block frontmatter;
- use `status: completed`;
- not be the active Work Block;
- not contain a current-state claim that review, verification, evaluation, drift,
  or closeout is still pending when the corresponding successful closeout exists.

### Active Work Block

A non-null `active_work_block` must:

- exist;
- not appear in `completed_work_blocks`;
- have an active frontmatter status such as `draft`, `planned`, `in_progress`, or
  `blocked`;
- be represented as active in `PROJECT_MAP.md`.

When `active_work_block` is null, the map must explicitly state that there is no
active implementation Work Block.

### Closeout

A successful closeout must identify:

- completed repository execution state;
- review, verification, evaluation when required, and drift verdicts;
- closeout classification;
- residual risks and follow-up work.

A closeout must not claim that a future PR merge already occurred, and it must not
remain stale after merge by encoding `Draft`, `Ready`, `open`, `not merged`, or
similar mutable GitHub state as a normative release condition.

### Fail-Closed Release Readiness

Missing or contradictory evidence yields `BLOCKED`, never `READY`. A release-state
validator must reject at least:

- missing completed Work Block paths;
- completed Work Blocks with non-completed frontmatter;
- active/completed overlap;
- missing or invalid active Work Block paths;
- map/registry disagreement;
- successful closeout with pending internal verdicts;
- normative mutable GitHub-state claims in closeout evidence.

## Enforcement

`scripts/validate-release-state.py` validates the repository state.
`scripts/test-release-state-contracts.py` provides positive and adversarial
fixtures. `.github/workflows/release-state-contract.yml` runs both on pushes and
pull requests.

The release-state gate is assurance evidence only. It does not authorize merge,
deployment, publication, credentials, or Hard Stop exceptions.
