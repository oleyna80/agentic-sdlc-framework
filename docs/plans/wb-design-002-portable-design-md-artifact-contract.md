---
schema_version: 1
artifact_type: work_block
artifact_id: wb-design-002-portable-design-md-artifact-contract
work_block_id: WB-DESIGN-002
status: in_progress
owner_role: orchestrator
created_at: 2026-08-11
last_updated: 2026-08-11
process_level: Standard
governance_profile: Controlled
branch: agent/design-md-artifact-contract
owner_approval: current explicit Owner confirmation to expand WB-DESIGN-002 and close internal DESIGN.md drift before assurance
critic_gate: APPROVE_WITH_CHANGES — unify the portable artifact contract and existing Impeccable consumer while preserving backward compatibility and provider neutrality
write_gate: READY
writer: one Coder, Orchestrator disclosed
base_revision: d07d5e8e3cee30b1bc6f057f58fd1ef05f8c0fef
---

# WB-DESIGN-002 — Portable DESIGN.md Artifact Contract and Consumer Reconciliation

## Objective

Define one optional, provider-neutral `DESIGN.md` design-domain artifact for the
Agentic SDLC Framework, supply a reusable template, teach `frontend-design` how
to consume it, and reconcile the existing Impeccable DESIGN.md generator/parser
so the repository does not ship two incompatible interpretations of the same
artifact.

The Work Block must not make Google Stitch, `@google/design.md`, MCP, Figma, or
any design provider part of framework authority or installation requirements.

## Discovery finding

The repository already contains substantial `DESIGN.md` support through the
`impeccable` skill. Its current `document` workflow and parser were written for
an older six-section subset:

- `Overview`;
- `Colors`;
- `Typography`;
- `Elevation`;
- `Components`;
- `Do's and Don'ts`.

The current upstream Google `design.md` format remains `alpha`, but at the pinned
revision used by this Work Block it supports a broader interoperable model:

- `Overview` / `Brand & Style`;
- `Colors`;
- `Typography`;
- `Layout` / `Layout & Spacing`;
- `Elevation & Depth` / `Elevation`;
- `Shapes`;
- `Components`;
- `Do's and Don'ts`;
- CSS color values including wide-gamut formats such as OKLCH;
- `omitted` declarations in frontmatter; and
- preservation of unknown/custom sections.

Leaving the old Impeccable interpretation unchanged would create immediate
internal contract drift after the new portable artifact contract is accepted.
The Owner therefore authorized expanding this Work Block before assurance to
reconcile the existing consumer in the same bounded change.

## External method/specification input

Reviewed on 2026-08-11 at immutable upstream revision:

`google-labs-code/design.md@9bf8eae67128b6cc55ad9bf86665767deb4c11cd`

Relevant upstream artifacts:

- `docs/spec.md` — format specification;
- `PHILOSOPHY.md` — prose/rationale philosophy;
- `README.md` — CLI/interoperability behavior.

The upstream project is Apache-2.0. The local framework does not copy Google
runtime code or make the external package a dependency.

## Approved design

### 1. Optional domain artifact

`DESIGN.md` is optional. Projects without a meaningful visual/UI design system
must not receive an empty or ceremonial file merely because the framework is
installed.

When an approved `DESIGN.md` exists, it is authoritative only for its declared
visual/design-system scope. It remains subordinate to Owner instructions,
approved specifications, accepted architecture/brand/accessibility contracts,
and the active Work Block.

### 2. No dual source of truth

For an existing project, a generated or extracted `DESIGN.md` begins as a draft.
The active Work Block must declare the reconciliation direction before treating
it as design-domain authority:

- `design_md_drives_implementation`;
- `implementation_drives_extraction`; or
- `bidirectional_reconciliation` as a temporary migration state.

Do not silently create a second design system beside existing CSS variables,
Tailwind tokens, Figma variables, component libraries, or other accepted design
artifacts.

### 3. Two complementary layers

A compatible `DESIGN.md` combines:

- machine-readable token values where exact reusable values are useful; and
- human-readable prose explaining visual intent, usage, exclusions, and
  subject-specific character.

Exact tokens and prose must not contradict one another. Token values answer
"what exact value?"; prose answers "why, where, and how?". A contradiction is
design drift, not permission for an agent to choose whichever layer it prefers.

### 4. Provider-neutral interoperability

The framework may use a Google-compatible `DESIGN.md` structure for
interoperability while remaining provider-neutral. Google Stitch, Google
`@google/design.md`, Figma, or another tool may consume or produce the artifact,
but those tools do not own its authority.

Unknown/custom sections must be preserved rather than discarded merely because
a consumer does not understand them.

### 5. Impeccable compatibility

Impeccable remains an optional design skill and a consumer/producer of the same
portable artifact. It must not redefine DESIGN.md authority.

Compatibility requirements:

- legacy six-section DESIGN.md files continue to parse;
- the eight-section interoperable form parses without loss of recognized
  sections;
- aliases accepted by the portable contract map to one canonical internal model;
- `omitted` arrays are represented rather than discarded;
- OKLCH and other supported CSS color strings are not rejected merely because
  they are not hex;
- unknown/custom H2 sections are preserved in parser output;
- duplicate canonical sections surface a deterministic diagnostic rather than
  silently replacing earlier content;
- Impeccable-specific `.impeccable/design.json` remains derived/local consumer
  state and cannot become design authority;
- current live consumers retain the existing parser API fields while gaining
  additive `layout`, `shapes`, `omitted`, `customSections`, and diagnostics.

`skills/impeccable/reference/init.md` was inspected during Define. It does not
encode the old six-section limitation and therefore does not require a write for
this reconciliation.

### 6. Verification

The framework itself does not install a DESIGN.md linter. When an approved
runtime already provides a compatible deterministic validator, it may be used as
evidence. The current Google CLI `lint` and `diff` commands are examples, not
requirements.

This Work Block adds a dependency-free Impeccable parser regression test and
runs it from the existing governance validation path so CI proves both backward
compatibility and the new parser contract without installing Google tooling.

A missing optional Google CLI does not block ordinary design work unless the
active Work Block explicitly makes that validator part of acceptance.

## Execute write-set

Exactly:

```text
docs/plans/wb-design-002-portable-design-md-artifact-contract.md
docs/design/design-md-artifact-contract.md
docs/templates/design-md-template.md
skills/frontend-design/SKILL.md
skills/impeccable/reference/document.md
skills/impeccable/scripts/design-parser.mjs
skills/impeccable/scripts/test-design-parser.mjs
scripts/validate-governance.sh
```

Lifecycle/assurance-only paths may be added only at the later Assure/Closeout
stage:

```text
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/reports/reviews/wb-design-002-portable-design-md-artifact-contract-review.md
docs/reports/verification/wb-design-002-portable-design-md-artifact-contract-verification.md
docs/reports/closeout/wb-design-002-portable-design-md-artifact-contract.md
```

No runtime adapter, package manifest, dependency, MCP configuration, Stitch
configuration, bootstrap profile, generated-project installation set, live-mode
protocol, or Portable Kit candidate path is writable in Execute.

## Explicit exclusions

- Do not install `@google/design.md`.
- Do not configure Stitch or any MCP server.
- Do not make `DESIGN.md` mandatory for every project.
- Do not automatically copy root `DESIGN.md` through bootstrap profiles.
- Do not make Google-specific tooling authoritative.
- Do not redesign Impeccable live mode, session state, browser transport, or
  variant-generation behavior.
- Do not change `.impeccable/design.json` into a canonical artifact.
- Do not modify the Portable Kit candidate or promote any candidate content.
- Do not change global Owner/role authority ordering.

## Critic gate

**APPROVE_WITH_CHANGES.** The expanded change is acceptable only if:

- one portable DESIGN.md contract governs both `frontend-design` and Impeccable;
- backward compatibility with the legacy six-section subset is preserved;
- existing design systems require explicit reconciliation;
- `DESIGN.md` authority is limited to design-domain decisions;
- higher project contracts retain precedence;
- prose and tokens are complementary, not competing authorities;
- unknown sections survive partial consumption;
- the Impeccable sidecar remains derived and non-authoritative;
- external tools remain optional verification/integration capabilities; and
- the upstream `alpha` status is recorded so future format changes require a new
  comparison rather than silently changing local behavior.

These constraints are incorporated above.

## Acceptance

- A normative local contract clearly defines authority, lifecycle,
  reconciliation, provider neutrality, and verification semantics.
- A reusable template is compatible with the pinned upstream section model while
  remaining useful without Google tooling.
- `frontend-design` discovers and obeys an approved `DESIGN.md` when present, but
  does not create or modify one without scope.
- Impeccable `document` guidance emits the same portable model rather than the
  obsolete six-section-only contract.
- Impeccable parser accepts both legacy and current portable forms, including
  Layout, Shapes, aliases, `omitted`, OKLCH, and custom sections.
- Parser output preserves its existing public fields and adds compatibility data
  additively.
- Deterministic parser fixtures cover legacy, current, alias/custom, omission,
  duplicate-section, and coverage behavior.
- Existing project design systems cannot be silently superseded by an extracted
  file.
- No dependencies, runtime integrations, MCP, Stitch setup, bootstrap behavior,
  live transport, or candidate promotion are changed.
- Google upstream provenance is revision-bound and the `alpha` maturity is clear.

## Lifecycle note

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` remain unchanged during Execute. Before
PR-readiness or closeout, lifecycle synchronization must be added from the
predeclared lifecycle write-set and the branch reconciled to one release-state
projection. No release-state consistency claim is made for the intermediate
Execute branch.

## Assurance and handoff

- Targeted Reviewer and Verifier are required under the Controlled profile.
- Deterministic repository CI is required before closeout.
- Evaluation is not required because no nondeterministic agent behavior benchmark
  is part of acceptance.
- Merge remains separately Owner-controlled.
