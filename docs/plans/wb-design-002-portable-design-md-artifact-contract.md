---
schema_version: 1
artifact_type: work_block
artifact_id: wb-design-002-portable-design-md-artifact-contract
work_block_id: WB-DESIGN-002
status: in_progress
owner_role: orchestrator
created_at: 2026-08-11
process_level: Standard
governance_profile: Controlled
branch: agent/design-md-artifact-contract
owner_approval: current explicit Owner confirmation of the proposed portable DESIGN.md artifact approach
critic_gate: APPROVE_WITH_CHANGES — adopt interoperability and authority semantics, not provider/tool ownership
write_gate: READY
writer: one Coder, Orchestrator disclosed
base_revision: d07d5e8e3cee30b1bc6f057f58fd1ef05f8c0fef
---

# WB-DESIGN-002 — Portable DESIGN.md Artifact Contract

## Objective

Define an optional, provider-neutral `DESIGN.md` design-domain artifact for the
Agentic SDLC Framework, supply a reusable template, and teach the existing
`frontend-design` skill how to consume it without making Google Stitch, the
Google CLI, MCP, Figma, or any design provider part of the framework authority
model.

## Discovery finding

The repository already contains partial `DESIGN.md` support through the
`impeccable` skill. Its current `document` workflow references the Google Stitch
format and emits a six-section subset. Current upstream Google `design.md` has
continued evolving: the format remains `alpha`, supports a broader section set,
CSS color formats including OKLCH, an `omitted` declaration, and preservation of
unknown sections.

This Work Block therefore establishes one shared framework contract first. It
does not perform a broad rewrite of Impeccable's generator/live parser in the
same write-set. That compatibility update is a separately bounded follow-up if
needed after the common contract is accepted.

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

### 5. Verification

The framework itself does not install a DESIGN.md linter. When an approved
runtime already provides a compatible deterministic validator, it may be used as
evidence. The current Google CLI `lint` and `diff` commands are examples, not
requirements.

A missing optional CLI does not block ordinary design work unless the active Work
Block explicitly makes that validator part of acceptance. Tool warnings do not
automatically become framework failures; the Work Block defines materiality.

## Execute write-set

Exactly:

```text
docs/plans/wb-design-002-portable-design-md-artifact-contract.md
docs/design/design-md-artifact-contract.md
docs/templates/design-md-template.md
skills/frontend-design/SKILL.md
```

No runtime adapter, package manifest, dependency, MCP configuration, Stitch
configuration, bootstrap profile, generated-project installation set, or
Impeccable implementation file is writable in this Execute stage.

## Explicit exclusions

- Do not install `@google/design.md`.
- Do not configure Stitch or any MCP server.
- Do not make `DESIGN.md` mandatory for every project.
- Do not automatically copy root `DESIGN.md` through bootstrap profiles.
- Do not make Google-specific tooling authoritative.
- Do not rewrite Impeccable's generator/live parser in this Work Block.
- Do not modify the Portable Kit candidate or promote any candidate content.
- Do not change global Owner/role authority ordering.

## Critic gate

**APPROVE_WITH_CHANGES.** Adopt the useful interoperability contract only after:

- the file is optional rather than universal;
- existing design systems require explicit reconciliation;
- `DESIGN.md` authority is limited to design-domain decisions;
- higher project contracts retain precedence;
- prose and tokens are complementary, not competing authorities;
- external tools remain optional verification/integration capabilities;
- the upstream `alpha` status is recorded so future format changes require a new
  comparison rather than silently changing local behavior.

These constraints are incorporated above.

## Acceptance

- A normative local contract clearly defines authority, lifecycle, reconciliation,
  provider neutrality, and verification semantics.
- A reusable template is compatible with the current upstream section order while
  remaining useful without Google tooling.
- `frontend-design` discovers and obeys an approved `DESIGN.md` when present, but
  does not create or modify one without scope.
- Existing project design systems cannot be silently superseded by an extracted
  file.
- No dependencies, runtime integrations, MCP, Stitch setup, bootstrap behavior,
  or candidate promotion are changed.
- Google upstream provenance is revision-bound and the `alpha` maturity is clear.

## Lifecycle note

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` remain unchanged during the bounded
Execute stage. Before PR-readiness or closeout, lifecycle synchronization must be
explicitly added to the write-set and the branch must be reconciled to one
release-state projection. No release-state consistency claim is made for the
intermediate Execute branch.

## Assurance and handoff

- Targeted Reviewer and Verifier are required under the Controlled profile.
- Deterministic repository CI is required before closeout.
- Evaluation is not required because no nondeterministic agent behavior benchmark
  is part of acceptance.
- Merge remains separately Owner-controlled.
