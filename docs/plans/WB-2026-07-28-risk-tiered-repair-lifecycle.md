# WB-2026-07-28 — Risk-tiered repair lifecycle and machine-derived closeout evidence

## Meta

| Field | Value |
| --- | --- |
| Work Block | `WB-2026-07-28-risk-tiered-repair-lifecycle` |
| Date | 2026-07-28 |
| Owner | Repository Owner |
| Orchestrator | Codex |
| Current stage | Stage 0 — Scope and contract decisions |
| Execution state | `IN_PROGRESS` |
| Implementation write gate | `BLOCKED` pending Owner decisions below |
| Risk tier | Governance / CI contract; no product change authorized |
| Source finding | HardwareLab pilot, PR #13 |

## Objective

Turn the HardwareLab pilot finding into a proportionate framework contract: small,
deterministic, reversible repairs must retain an independent assurance boundary
without paying for a full multi-document lifecycle. Closeout evidence must be
derived from authoritative Git and CI data rather than copied manually.

This Work Block also defines an **Integration Stabilization** envelope for several
sequentially discovered deterministic compatibility defects. It prevents a new full
Work Block from being created merely because the next CI/bootstrap defect becomes
visible after the preceding repair.

## Pilot evidence

HardwareLab PR #13 was merged at
`72ada873d66d19de2609515b443766065fe132c9` after its final head
`81b996238aee78766f2073e0b8e68bf291e675a7` passed Agent Guards, quality, E2E,
and Lighthouse checks.

The pilot exposed real compatibility defects through deterministic controls
(lockfile, CI Node runtime, and skill-index classification), so the controls are
valuable. It also exposed avoidable governance churn: manually maintained closeout
metadata reported four PR commits while the final branch contained five. That
`4 -> 5` discrepancy is a pilot finding only. It must not be corrected by another
HardwareLab evidence commit.

## Target contract

### Narrow Deterministic Repair

The proposed profile applies only when all eligibility conditions hold:

- the change is deterministic and reversible;
- no architectural decision is required;
- auth, security boundaries, schema, public API, data, and product logic do not
  change;
- the write-set is bounded and declared before implementation;
- the result is fully checkable through deterministic commands or lint; and
- the risk is low or medium.

The expected lifecycle is:

```text
Owner / Orchestrator scope decision
        -> one repair record
        -> one Coder
        -> one independent assurance pass (review + deterministic verification)
        -> CI
        -> machine-generated closeout summary
```

The repair record must contain the problem, root cause, allowed write-set,
prohibited changes, verification commands, and a stop condition. The independent
assurance pass is performed by a different read-only agent or session and produces
one combined report with review findings, deterministic verification, and verdict.
Separate Critic, Review, Verification, and Drift documents are not mandatory for
this profile.

The profile must fail closed: any auth, security, schema, public API, data,
dependency, deploy, product-scope, or architectural decision moves the work back
to the normal lifecycle or a new Owner-approved Work Block.

### Integration Stabilization envelope

One Work Block may contain sequential deterministic compatibility repairs only
while every repair remains within a pre-approved CI, bootstrap, or integration
path envelope; product logic remains unchanged; no dependency upgrade or
architectural decision is needed; the correction limit is not exceeded; and the
maximal practical local equivalent of CI runs before push.

Discovery of another defect alone does not open a new Work Block. A new Work Block
or explicit Owner decision is required as soon as risk category, product scope,
or the approved path envelope changes.

## Approved scope for this opening

- Record this Stage 0 Work Block and the pilot finding in the framework repository.
- Inventory the existing lifecycle, templates, validators, CI triggers, and
  generated-contract surfaces before proposing implementation.
- Produce a bounded Stage 1 implementation proposal after Owner decisions.

## Out of scope

- Any further HardwareLab change, correction round, or alteration of PR #13.
- Product functionality, dependencies, deployments, credentials, provider access,
  public APIs, schemas, or data changes.
- Implementing the new profile, templates, generators, validators, or CI changes
  before Stage 0 decisions are approved.
- Copying historical HardwareLab governance artifacts into this repository.

## Owner decisions required before implementation

1. Classify Narrow Deterministic Repair as a controlled/Level 2 subprofile
   (recommended) or as a new top-level runtime profile.
2. Set the numeric correction limit and the exact allowed path envelope for an
   Integration Stabilization Work Block.
3. Select the authoritative source and retention model for machine-derived CI
   metadata (runner artifact, CI job output, or another deterministic source).
4. Approve the path-aware CI policy, including which contract checks must never be
   skipped.

## Candidate implementation write-set (not yet approved)

The Stage 0 inventory should assess only the minimum necessary subset of:

- `docs/profiles.md`;
- `template/.agent/workflows/sdd-protocol.md`;
- repair-record and combined-assurance templates under `template/docs/templates/`;
- `template/docs/templates/closeout-report-template.md`;
- runtime-neutral generated instructions and registry/map entries, if the new
  templates must be published to consumer repositories;
- deterministic validator or generator scripts and their tests; and
- path-aware framework CI workflow definitions.

No file on this list is approved for modification yet.

## Acceptance criteria for the future implementation

1. Eligibility is explicit, mechanically checkable where practical, and fails
   closed on excluded risk categories.
2. The repair record and one independent combined assurance report replace the
   redundant artifacts only for eligible work.
3. Integration Stabilization has a correction ceiling, a bounded path envelope,
   and deterministic escalation conditions.
4. Closeout derives Git and CI facts without a manually copied commit/check count.
5. Path-aware CI reduces irrelevant work without bypassing mandatory framework
   contract checks.
6. The normal lifecycle remains unchanged for non-eligible work.

## Hard stops

- Stop for Owner approval if the inventory reveals an architecture, dependency,
  secret, deploy, public API, schema, data, security-boundary, or product-scope
  change.
- Stop if independent assurance cannot be run from a distinct read-only session.
- Stop if machine-derived closeout would require unapproved credentials, mutable
  external state, or unverifiable CI data.
- Stop if a proposed path-aware trigger can bypass a mandatory contract check.

## Evidence and next action

This record opens the Work Block only. It does not authorize framework
implementation. Next: complete the Stage 0 contract inventory, return the four
Owner decisions above, and obtain an approved implementation write-set.
