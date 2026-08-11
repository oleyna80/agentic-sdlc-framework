Generate or refresh a project `DESIGN.md` that captures the reusable visual system
and its design rationale so humans and coding agents can make consistent visual
decisions across tasks.

This Impeccable workflow is a **producer/consumer of the framework's portable
DESIGN.md artifact model**. It does not redefine artifact authority and does not
require Google Stitch, Google CLI, MCP, Figma, or another provider.

Interoperability baseline reviewed on 2026-08-11:

`google-labs-code/design.md@9bf8eae67128b6cc55ad9bf86665767deb4c11cd`

The upstream format identifies itself as `alpha`. Treat future upstream changes
as a new comparison, not as permission to silently change local behavior.

## Authority and overwrite rules

Before writing:

1. resolve the project DESIGN.md path from the active Work Block or repository
   navigation; otherwise prefer root `DESIGN.md`;
2. determine whether an existing DESIGN.md is approved design-domain authority,
   draft extraction evidence, or only an unregistered candidate;
3. identify the active reconciliation direction when code and DESIGN.md both
   exist:
   - `design_md_drives_implementation`;
   - `implementation_drives_extraction`; or
   - temporary `bidirectional_reconciliation`;
4. never silently overwrite an existing approved DESIGN.md;
5. never create DESIGN.md merely because Impeccable is installed.

If the user/Work Block has not authorized creating or updating the artifact,
stop at analysis or a proposed draft.

## File model

A portable DESIGN.md contains two complementary layers:

```text
DESIGN.md
├── optional YAML frontmatter
│   └── exact reusable token values
└── Markdown body
    └── rationale, usage, character, constraints, examples
```

Structured values answer **what exact value?**. Prose answers **why, where, and
how?**. Do not let them contradict one another.

The prose is not filler. Prefer a precise visual reference or domain-specific
world over generic adjective bundles such as "modern, premium, clean".

## Frontmatter

Use only real project tokens. Preserve established project names when possible.
Do not fabricate categories merely to make the document look complete.

```yaml
---
version: alpha
name: <project or design-system name>
description: <one-line description>

# Optional: document intentionally absent categories.
# omitted:
#   - spacing
#   - section: rounded
#     reason: "Square geometry is intentional."

colors:
  primary: "#b8422e"
  surface: "#faf7f2"

typography:
  display:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: 3rem
    fontWeight: 300
    lineHeight: 1
  body:
    fontFamily: "Inter, sans-serif"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5

spacing:
  sm: 0.5rem
  md: 1rem
  lg: 2rem

rounded:
  sm: 0.25rem
  md: 0.5rem

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: 1rem
---
```

### Frontmatter rules

- Token references use `{path.to.token}`.
- Colors may use valid CSS color strings, including hex, rgb/hsl families,
  OKLCH/OKLab/Lab/LCH, named colors, or other compatible CSS color syntax.
  Preserve the project's canonical value rather than forcing hex solely for a
  provider.
- Typography roles are objects. Include only properties the project actually
  defines.
- `spacing` and `rounded` keys are open-ended; keep existing project naming.
- Component variants may be represented as sibling keys such as
  `button-primary`, `button-primary-hover`, and `button-primary-active`.
- The portable baseline recognizes component properties such as
  `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`,
  `height`, and `width`. Project-specific extensions may still be documented in
  prose or custom sections.
- `omitted` is for intentional absence. Do not use it to hide extraction gaps.

## Markdown sections

When present, use this interoperable order:

1. `## Overview` (alias: `Brand & Style`)
2. `## Colors`
3. `## Typography`
4. `## Layout` (alias: `Layout & Spacing`)
5. `## Elevation & Depth` (alias: `Elevation`)
6. `## Shapes`
7. `## Components`
8. `## Do's and Don'ts`

Sections may be omitted when irrelevant. Additional project-specific sections
such as `Motion`, `Iconography`, `Data Visualization`, or domain-specific
component rules are allowed.

**Preserve unknown/custom sections.** A consumer that does not understand a
section may ignore it for its own UI, but must not rewrite DESIGN.md in a way
that deletes that content.

Legacy Impeccable DESIGN.md files containing only Overview, Colors, Typography,
Elevation, Components, and Do's/Don'ts remain valid inputs and must continue to
parse.

## When to run

Use `/impeccable document` when:

- `/impeccable init` has established project/product context and the user wants a
  reusable visual system artifact;
- a project already has stable visual primitives that should be extracted;
- an approved DESIGN.md has materially drifted from implementation;
- a redesign needs an explicit baseline or new proposed design contract; or
- multiple agents/tools need one repository-local design handoff.

If no stable design system exists and the current task does not need one, skip
DESIGN.md rather than creating ceremony.

## Two modes

### Scan mode — existing implementation

Use when the project already has CSS/theme/component/rendered design evidence.

A scan result is initially **extraction evidence**, not automatic authority.
The Work Block must define when and how the extracted artifact is accepted.

### Seed mode — pre-implementation

Use when the design system is being established before code. A seed is a
proposed contract. Keep it minimal and mark assumptions clearly; do not invent a
large token taxonomy before implementation needs it.

`/impeccable document --seed` may force seed mode when the user explicitly wants
pre-implementation design definition.

## Scan mode

### Step 1: discover existing design sources

Inspect, in practical priority order:

1. CSS custom properties and global styles;
2. Tailwind/theme configuration;
3. CSS-in-JS or typed theme files;
4. token JSON/DTCG/Style Dictionary sources;
5. component-library primitives and variants;
6. brand assets and documented rules;
7. rendered/computed styles when approved browser tooling is available;
8. any existing DESIGN.md and its authority status.

Record the actual source paths used for extraction.

### Step 2: establish reconciliation before drafting

If implementation already exists, state one direction:

- `implementation_drives_extraction` — default for documenting an existing
  system;
- `design_md_drives_implementation` — only when DESIGN.md is already the approved
  design-domain contract;
- `bidirectional_reconciliation` — temporary migration when both have unresolved
  authoritative content.

Do not silently replace existing CSS variables, Tailwind tokens, or components
with newly invented DESIGN.md names.

### Step 3: extract machine-readable values

Extract only values that are actually reusable:

- colors and semantic roles;
- typography roles;
- spacing rhythm/grid values;
- rounded/shape scale where used;
- recurring component primitives and state variants.

Use `omitted` only when a category is intentionally absent, not merely unseen.

### Step 4: collect qualitative design language

Ask only for design intent that cannot be derived reliably from code. Useful
questions include:

- What specific reference or material world should this design evoke?
- Which visual behaviors are essential to preserve?
- What should this explicitly not become?
- What role does elevation/depth play?
- What character should recurring controls/components have?

Use PRODUCT.md or accepted brand guidance where available. Do not invent brand
personality that conflicts with higher project artifacts.

### Step 5: write the interoperable body

A useful baseline:

```markdown
# Design System: <Name>

## Overview

**Specific reference:** <precise visual/material/domain reference>

<Audience, register, density, visual character, and reconciliation direction.>

## Colors

<Palette logic, usage, scarcity rules, and prohibited misuse.>

## Typography

<Type roles, hierarchy, line length, tone, and usage constraints.>

## Layout

<Grid/max-width/density/spacing/responsive intent and grouping rules.>

## Elevation & Depth

<Shadows, tonal layering, borders, overlap, or deliberate flatness.>

## Shapes

<Corner and geometry language, including any reserved special shapes.>

## Components

<Recurring component appearance and material states: hover, focus, selected,
loading, error, disabled, etc.>

## Do's and Don'ts

- **Do** <specific rule>.
- **Don't** <specific anti-pattern>.

## Motion

<Optional project-specific section: motion character and reduced-motion rules.>
```

The body should explain application and character, not simply repeat YAML values.

## Seed mode

When no implementation exists:

1. establish subject, audience, product/brand register, and specific visual
   reference;
2. define only the small set of tokens needed to make early screens coherent;
3. include the eight canonical sections only where meaningful;
4. clearly mark unresolved assumptions;
5. plan to rerun scan mode after implementation exists.

A seed should not pretend to be extracted evidence.

## `.impeccable/design.json` sidecar

The sidecar is **Impeccable-specific derived/local consumer state** for the live
panel and other Impeccable tooling. It is not the portable design SSOT and does
not outrank DESIGN.md or implementation.

It may cache or materialize information useful to Impeccable, for example:

- display metadata for tokens;
- tonal ramps computed or curated for the panel;
- richer component preview snippets;
- motion/breakpoint metadata used by live tooling;
- narrative fragments used by the panel.

Do not move authoritative design decisions into the sidecar merely because an
older DESIGN.md parser could not represent them. The portable DESIGN.md format
allows custom sections and extensible content; keep canonical rationale in the
repository artifact when it belongs there.

When regenerating the sidecar:

- preserve DESIGN.md unless the active write-set also authorizes updating it;
- derive rather than contradict canonical values;
- treat stale sidecar data as cache drift;
- never let sidecar existence grant tool or source-write authority.

## Parser compatibility expectations

Impeccable's parser must remain dependency-free and backward compatible while
representing the current portable model additively.

Expected behavior:

- legacy six-section files parse;
- current eight-section files parse;
- `Brand & Style`, `Layout & Spacing`, and `Elevation` aliases map to their
  canonical internal sections;
- `omitted` frontmatter arrays are retained;
- OKLCH and other CSS color strings are accepted as values;
- custom sections are returned to consumers rather than discarded;
- duplicate canonical sections produce a deterministic diagnostic;
- existing fields (`overview`, `colors`, `typography`, `elevation`, `components`,
  `dosDonts`) remain available for current live consumers;
- new fields are additive (`layout`, `shapes`, `omitted`, `customSections`,
  diagnostics).

## Verification

When the Google CLI or another compatible validator is already approved and
available, its `lint`/`diff` output may be additional evidence. It is not
required by Impeccable.

For framework maintenance, run the dependency-free parser regression fixture:

```bash
node skills/impeccable/scripts/test-design-parser.mjs
```

The fixture must prove legacy compatibility plus current Layout/Shapes/aliases,
`omitted`, OKLCH/custom-section preservation, duplicate diagnostics, and coverage
reporting.

## Handoff

On completion, report:

- DESIGN.md path and authority status;
- reconciliation direction;
- implementation/token sources inspected;
- custom/omitted sections intentionally retained;
- unresolved drift or assumptions;
- sidecar status if Impeccable generated one;
- validation evidence actually run.

Do not claim DESIGN.md is authoritative merely because this workflow generated
it. Authority comes from the Owner/Work Block and repository lifecycle.
