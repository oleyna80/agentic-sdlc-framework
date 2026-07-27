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

GitHub pull-request and merge state is **mutable external operational metadata**,
including:

- whether a pull request is Draft or Ready;
- whether it is open, closed, or merged;
- merge timestamps and merge commit SHAs;
- requested reviewers and branch deletion state.

Mutable GitHub state may be cited in an external notification or appended by a
separate post-merge record, but it must not be normative content of a pre-merge
closeout commit. A closeout records `repository closeout`, not a prediction or
copy of later hosting-platform state.

## Canonical Sources

1. Work Block frontmatter and its single `Final State` or legacy `Closeout State`
   section define the lifecycle of that Work Block.
2. `FILE_REGISTRY.yml:migration_state` is the machine-readable index of completed
   and active migration Work Blocks.
3. The machine block and visible `Migration Work` section in `PROJECT_MAP.md` are
   the human-readable projection of the same migration state.
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
- contain exactly one terminal state section;
- declare terminal successful review, verification, drift, and closeout values;
- reject `PENDING`, `BLOCKED`, `UNVERIFIED`, `MISALIGNED`, or any other adverse or
  non-terminal value;
- use `READY` or documented `SKIPPED` when an evaluation verdict is present.

Legacy `Drift Gate: READY` remains accepted for historical Work Blocks created
before `ALIGNED` became the canonical terminal drift token. New Work Blocks use
`ALIGNED`.

### Active Work Block

A non-null `active_work_block` must:

- exist;
- not appear in `completed_work_blocks`;
- have an active frontmatter status such as `draft`, `planned`, `in_progress`, or
  `blocked`;
- be represented as active inside the unique visible `## Migration Work` section
  of `PROJECT_MAP.md`.

When `active_work_block` is null, that section must explicitly state that there is
no active implementation Work Block.

### Closeout

A successful closeout must identify:

- completed repository execution state;
- exact `READY` review and verification verdicts;
- exact `ALIGNED` drift verdict;
- evaluation evidence whenever the latest Work Block declares an evaluation
  verdict, with the same terminal `READY` or `SKIPPED` token;
- `SUCCESS` closeout classification and completed task state;
- non-normative external VCS state;
- one non-empty `## Residual Risks and Limitations` section;
- one non-empty `## Follow-Up Work` section.

Normalized closeout marker keys must be unique. Contradictory repeated markers fail
closed rather than using first-value-wins or last-value-wins behavior.

A closeout must not assert ordinary mutable hosting-platform facts such as
`PR #9 is open`, `PR #9 is Draft`, `PR #9 was merged`, merge timestamps, merge
commit state, or equivalent pull-request status claims.

### Fail-Closed Release Readiness

Missing or contradictory evidence yields `BLOCKED`, never `READY`. A release-state
validator must reject at least:

- missing completed Work Block paths or terminal sections;
- completed Work Blocks with non-completed frontmatter or adverse lifecycle values;
- active/completed path or Work Block ID overlap;
- missing or invalid active Work Block paths;
- map/registry or machine/visible-map disagreement;
- closeout identity mismatch or duplicate markers;
- missing required evaluation evidence;
- missing residual-risk or follow-up sections;
- normative mutable GitHub-state claims in closeout evidence.

## Enforcement

`scripts/validate-release-state.py` validates repository state.
`scripts/test-release-state-contracts.py` provides positive and adversarial
fixtures. `.github/workflows/release-state-contract.yml` runs both on pushes and
pull requests, while Framework Contracts invokes the same governance validation.

The release-state gate is assurance evidence only. It does not authorize merge,
deployment, publication, credentials, or Hard Stop exceptions.
