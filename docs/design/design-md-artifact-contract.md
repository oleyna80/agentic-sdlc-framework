---
schema_version: 1
artifact_type: domain_artifact_contract
artifact_id: portable-design-md
status: review
owner_role: architect
created_at: 2026-08-11
upstream_reference: google-labs-code/design.md
upstream_revision: 9bf8eae67128b6cc55ad9bf86665767deb4c11cd
upstream_format_version: alpha
---

# Portable DESIGN.md Artifact Contract

## Purpose

`DESIGN.md` is an optional repository artifact for preserving a product's visual
system across humans, agent sessions, coding runtimes, and design tools.

It exists to answer two different questions in one inspectable file:

- **exact reusable values** — colors, typography, spacing, shape, and component
  tokens when the project benefits from machine-readable values; and
- **design intent** — why those values exist, how the interface should feel and
  behave, where the rules apply, and what the system intentionally avoids.

The artifact is portable context. It is not a runtime configuration file, a
provider profile, or a replacement for source code.

## Optionality

Do not create `DESIGN.md` merely because the Agentic SDLC Framework is present.
A project may legitimately have no UI or no stable visual system.

Create or adopt it only when at least one is true:

- the project has a reusable visual/design system that multiple tasks must honor;
- a redesign needs a stable design baseline before implementation;
- an existing codebase needs its visual system extracted and reconciled;
- multiple agents or tools need a shared design handoff artifact; or
- the active Work Block explicitly requires a design-system contract.

The framework bootstrap must not install an empty root `DESIGN.md` by default.

## Authority Boundary

An approved `DESIGN.md` is **design-domain authority only**. It can constrain
palette, typography, spacing, layout language, elevation, shapes, component
appearance, interaction character, and explicit visual do/don't rules.

It does not override, expand, or grant authority beyond:

1. current explicit Owner instruction;
2. root operating contract and accepted governance;
3. approved product/specification requirements;
4. accepted architecture, brand, legal, accessibility, or external contracts;
5. the active Work Block and its write-set.

If a higher-authority artifact requires behavior that conflicts with
`DESIGN.md`, stop and reconcile the design artifact rather than silently ignoring
the higher contract.

`DESIGN.md` does not authorize:

- source edits outside the active write-set;
- asset/font/package installation;
- remote design services;
- browser tooling;
- Stitch, Figma, MCP, or provider access;
- deployment or publication.

## Location and Discovery

The preferred project location is:

```text
PROJECT_ROOT/DESIGN.md
```

A project may use another explicit path when its accepted repository navigation
or Work Block says so. Agents must not treat every file named `DESIGN.md` in a
vendor, example, archive, or dependency directory as project authority.

Discovery order:

1. path explicitly named by the current Owner instruction or active Work Block;
2. registered project design-system path in repository navigation;
3. root `DESIGN.md`;
4. other candidate files only as non-authoritative discovery input until their
   role is established.

## Lifecycle

### Seed mode — design before implementation

A pre-implementation `DESIGN.md` starts as a proposed design contract. It may
capture a specific creative reference, visual rationale, initial tokens, and
constraints before code exists.

The active Work Block must define when the seed becomes approved design-domain
authority. Once implementation exists, material divergence is resolved through
explicit design drift/reconciliation rather than silent token replacement.

### Extract mode — implementation before document

When a project already has CSS variables, Tailwind tokens, theme objects,
component libraries, Figma variables, or other implemented design primitives,
an extracted `DESIGN.md` begins as **draft evidence**, not automatic authority.

Extraction must identify the observed source paths and unresolved conflicts.
The document becomes authoritative only after the Work Block explicitly accepts
the reconciliation.

### Evolve mode — coordinated design change

For an established approved `DESIGN.md`, a material visual-system change should
name both the design artifact and affected implementation surfaces in the Work
Block. Review and verification compare the intended design change with the
rendered/implemented result.

## No Dual Source of Truth

Before adopting `DESIGN.md` in an existing project, declare one relationship:

### `design_md_drives_implementation`

Use when `DESIGN.md` is the accepted design-system contract and code/tokens must
implement it.

### `implementation_drives_extraction`

Use while documenting an existing system. Source implementation remains the
baseline until extraction has been reconciled and approved.

### `bidirectional_reconciliation`

Use only as a temporary migration state when neither side can yet be declared
canonical. The Work Block must name the conflicts to resolve and the condition
that ends the transitional state.

Do not leave `DESIGN.md` and a token/theme system as two indefinite competing
sources of truth.

## File Model

The interoperability baseline follows the open Google `DESIGN.md` format at the
revision recorded in this contract while remaining provider-neutral.

A compatible file has two complementary layers:

```text
DESIGN.md
├── optional YAML frontmatter
│   └── exact reusable design tokens
└── Markdown body
    └── rationale, usage, character, constraints, examples
```

### Machine-readable values

When present, frontmatter may express design-system primitives such as:

- `colors`;
- `typography`;
- `spacing`;
- `rounded`;
- `components`;
- explicitly `omitted` categories when useful for compatible tooling.

Do not invent token categories or values solely to make the file look complete.
Use the project's own names where they are already established.

### Human-readable intent

The prose carries the design reasoning agents need when exact values alone are
insufficient. Prefer a concrete reference and domain-specific character over a
stack of generic adjectives.

Useful prose explains:

- the product/audience/design register;
- the visual or material reference;
- where colors and typography belong and where they do not;
- density, layout rhythm, elevation, shape, and component character;
- interaction/motion character when relevant;
- explicit negative constraints and anti-patterns.

### Token/prose consistency

Exact values and prose are complementary. Where a token exists, it answers the
exact-value question. Prose explains intent and application.

They must not contradict each other. For example, prose must not call one color
the primary action accent while the structured component tokens bind another
without an explicit rationale. Treat such disagreement as design drift.

## Section Compatibility

For compatibility with the referenced upstream `alpha` format, the reusable
local template uses this core order when sections are present:

1. `Overview`;
2. `Colors`;
3. `Typography`;
4. `Layout`;
5. `Elevation & Depth`;
6. `Shapes`;
7. `Components`;
8. `Do's and Don'ts`.

Sections may be omitted when not relevant. Project-specific sections such as
`Motion`, `Iconography`, `Data Visualization`, or domain-specific component
rules may be added when useful.

Consumers must preserve unknown sections they do not understand. A partial
consumer may ignore unsupported sections for its own rendering, but it must not
rewrite the source file in a way that deletes them.

## Existing Design-System Reconciliation

Before creating new visual primitives, inspect the existing repository for:

- CSS custom properties;
- Tailwind/theme configuration;
- component library tokens and variants;
- typography/font declarations;
- spacing/radius/elevation scales;
- responsive breakpoints;
- icon and motion conventions;
- existing design/brand documentation.

The Work Block should state whether the proposed `DESIGN.md`:

- documents these values unchanged;
- intentionally replaces named values;
- maps one naming system to another; or
- records unresolved drift for later decision.

A screenshot or external design export does not justify creating a parallel token
system when repository-native primitives can express the intended design.

## Agent Responsibilities

### Orchestrator / Architect

- establish whether the project needs `DESIGN.md`;
- record its authority scope and reconciliation direction;
- keep higher product, accessibility, brand, and architecture contracts intact;
- prevent provider tooling from becoming implicit authority.

### Coder / Designer

- read approved `DESIGN.md` before inventing free design-system choices;
- reuse repository-native primitives where they implement the accepted contract;
- do not modify `DESIGN.md` unless it is inside the approved write-set;
- surface design/code drift instead of silently choosing one side.

### Reviewer

- inspect both design rationale and implementation impact;
- look for parallel token systems, contradictory values, unjustified defaults,
  accidental provider coupling, and unsupported deletion of custom sections.

### Verifier

- use deterministic structure/token checks when available and in scope;
- use rendered evidence for material visual changes when capability permits;
- report missing optional tooling as a limitation, not a fabricated pass.

## Optional Tooling

The framework does not install or require a DESIGN.md CLI.

A compatible tool already available in the approved environment may provide
additional evidence. At the referenced Google revision, examples include:

```text
lint   — structural/token/reference/contrast findings
diff   — token/prose change and regression comparison
export — interoperability output for Tailwind/DTCG consumers
```

Using an external CLI may require dependency/network approval under the active
Work Block. The existence of a CLI command does not grant permission to install
or run it.

Warnings from a third-party linter are evidence to interpret against the active
acceptance criteria. They are not automatically framework Hard Stops.

## Provider Neutrality

Google Stitch, `@google/design.md`, Figma, design-token tools, and future design
systems are optional producers/consumers/integrations.

The portable contract is:

```text
accepted project intent
        ↓
optional DESIGN.md
        ↓
repository-native implementation
        ↓
rendered verification
```

not:

```text
Google/Stitch/tool
        ↓
project authority
```

Provider configuration, credentials, MCP servers, remote projects, and tool
memory stay outside this artifact contract unless separately authorized.

## Upstream Maturity and Drift

The referenced upstream Google format reports version `alpha`. The local
framework therefore treats the format as an interoperability input, not a remote
spec that silently updates itself.

Future upstream changes require a new revision-bound comparison before local
contract/template behavior changes. Existing project `DESIGN.md` files remain
valid local artifacts until an approved migration says otherwise.

## Template

Use:

```text
docs/templates/design-md-template.md
```

as a starting point only when the project actually needs a design-system
artifact. Copying or instantiating the template is a write action governed by the
active Work Block.

## Provenance

Method and interoperability reference:

- repository: `google-labs-code/design.md`;
- revision: `9bf8eae67128b6cc55ad9bf86665767deb4c11cd`;
- reviewed: 2026-08-11;
- referenced files: `docs/spec.md`, `PHILOSOPHY.md`, `README.md`;
- upstream format maturity: `alpha`;
- upstream license: Apache-2.0.

This local contract is an Agentic SDLC adaptation. It does not make the external
repository, CLI, or provider an authority-bearing dependency.
