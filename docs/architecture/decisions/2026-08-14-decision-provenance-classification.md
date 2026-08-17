# ADR — Classify Framework Decision Provenance

- **ID:** 2026-08-14-decision-provenance-classification
- **Status:** proposed
- **Scope:** framework research, governance, reusable architecture and workflow mechanisms
- **Last verified:** 2026-08-14

## Decision

Framework-level reusable mechanisms will record one primary provenance class:

- `adopted`;
- `adapted`;
- `original_experience_derived`.

The classification records how the local mechanism was produced. It does not
change authority, establish legal permission to copy upstream material, or claim
global novelty.

The normative target contract is `governance/decision-provenance.md`.

## Context

The framework has always evolved from a combination of external experience,
selective reuse, internal experimentation, and mechanisms created in response to
repeated operating problems. As the project matures, comparisons with other
agentic SDLC systems are becoming a regular source of research input.

Without explicit provenance, later maintainers cannot easily distinguish:

- a practice intentionally kept close to an upstream design;
- a practice heavily reworked to fit this framework's runtime-neutral authority
  and assurance model;
- a mechanism that arose from direct project experience rather than a known
  external design basis.

That distinction matters for maintenance, upstream monitoring, benchmark work,
publication accuracy, and understanding why local divergence exists.

The repository already has a narrower provenance record for externally sourced
skills at `skills/skill-library-maintenance/reference/provenance-record.md`.
That record pins upstream revisions, local deltas, license evidence, and adoption
decisions, but it does not classify the origin of general architecture and
workflow ideas.

## Classification Rules

### Adopted

Use when an identifiable external mechanism is brought in with its essential
structure substantially preserved.

### Adapted

Use when external work materially shapes the mechanism but the local result
changes behavior, lifecycle placement, authority, composition, constraints, or
purpose.

When substantial original work is added on top of a materially influential
external design, the result is still `adapted` rather than
`original_experience_derived`.

### Original / Experience-Derived

Use when a mechanism originated from this project's own operating experience,
repeated failure modes, experiments, or internal design process without an
identified external mechanism used as its design basis.

`original_experience_derived` is explicitly not a claim of global novelty or
priority. Comparable ideas may exist elsewhere.

## No `Mixed` Category

A fourth `mixed` category would make classification less useful because most
mature engineering decisions combine multiple influences.

Instead:

- record all material sources;
- record the local delta;
- select the primary class according to how the mechanism was produced.

If multiple external sources materially influence a framework-specific result,
use `adapted` and list those sources.

## Recording Location

Provenance stays with the artifact that introduces or authorizes the mechanism:
ADR, specification, benchmark analysis, or Work Block. A separate central
provenance database is not introduced at this stage because it would create a
second synchronization surface.

A generated index may be added later for discovery, but it must remain derived
and non-authoritative.

## Legal Boundary

Design provenance is distinct from code/content licensing.

If implementation copies or modifies code, templates, text, assets, prompts,
schemas, or other protected expression, normal license review and third-party
publication controls still apply. A provenance classification neither grants nor
removes that permission.

## Adoption Strategy

Do not perform an immediate repository-wide historical backfill.

Apply the classification prospectively. Existing mechanisms receive provenance
when they are next materially revised, benchmarked, or re-documented. This keeps
current product work moving while gradually improving architectural memory.

The planned Spec Kit comparison is an appropriate first benchmark to use this
classification capability-by-capability rather than assigning one label to the
entire external framework.

## Consequences

### Positive

- External research remains visible without becoming authority.
- Intentional divergence from upstream systems becomes maintainable knowledge.
- Experience-derived mechanisms can be identified without overstating novelty.
- Benchmark analyses can distinguish `KEEP`, `ADOPT`, `ADAPT`, and `REJECT`
  decisions from the provenance of the resulting local mechanism.
- License/source provenance remains separate from architecture provenance.

### Tradeoffs

- Architecture and benchmark artifacts gain a small metadata burden.
- Some classifications will require judgment rather than mechanical detection.
- Historical coverage will remain incomplete until affected mechanisms are
  revisited.

## Evidence

- Existing source-provenance pattern:
  `skills/skill-library-maintenance/reference/provenance-record.md`
- Target contract: `governance/decision-provenance.md`
- Owner direction: 2026-08-14 discussion establishing the three-category model
  and prospective use for framework comparisons

## Provenance

- **Classification:** `original_experience_derived`
- **Sources:** no external design source used as the basis for this taxonomy
- **Internal evidence:** existing internal skill provenance practice plus Owner
  and framework-development experience
- **Local delta:** extends source provenance into design provenance and defines a
  three-class mechanism-origin taxonomy
- **Rationale:** created to describe the framework's actual development method
  without claiming that all underlying engineering ideas are novel
- **Novelty claim:** none

## Review Trigger

Review this decision if provenance becomes a machine-enforced release gate, a
central provenance registry is introduced, legal attribution is merged with
architecture provenance, or repeated classifications cannot be represented by
the three primary classes.
