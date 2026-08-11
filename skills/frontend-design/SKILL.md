---
name: frontend-design
description: Create or reshape distinctive, production-grade frontend interfaces from the real subject, audience, job, interface mode, and project design system. Use for visual direction, UI composition, typography, interaction, interface copy, and frontend design implementation while avoiding templated defaults.
license: Apache-2.0; see LICENSE.txt
source: https://github.com/anthropics/skills/tree/main/skills/frontend-design
metadata:
  upstream_repository: https://github.com/anthropics/skills
  upstream_path: skills/frontend-design/SKILL.md
  upstream_revision: f17010c9bb483898c1d9c9f42dde2b3a98889434
  upstream_blob: decdff43d05908b4c1fc2cfd2d80fc5743440934
  last_checked: 2026-08-11
  local_modification: Adapted for Agentic SDLC roles, authority boundaries, handoff, verification, domain-aware interface modes, composition planning, repository design-system and approved DESIGN.md reuse, and rendered validation.
  additional_method_sources:
    - https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4
    - https://developers.openai.com/api/docs/guides/frontend-prompt
    - https://developers.openai.com/codex/use-cases/frontend-designs
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(rg *)
  - Bash(jq *)
---

# Frontend Design

Create interfaces with a point of view that belongs to the actual subject rather
than to a reusable AI aesthetic. Treat the brief, accepted product constraints,
existing brand system, interface mode, and repository design system as inputs to
design, not decoration added after the layout is chosen.

This local version combines Anthropic's subject-grounded `frontend-design`
method with selected provider-neutral lessons from current official OpenAI
frontend guidance and an optional portable `DESIGN.md` artifact model. It does
not grant write authority, expand a Work Block, choose a runtime or model,
require a particular browser or design tool, or waive review and verification
requirements.

## Ground the Direction in the Subject

Before designing, establish four facts:

1. **Subject** — the concrete product, service, organization, or experience.
2. **Audience** — the people who must understand or use it.
3. **Single job** — the primary thing this page or flow must accomplish.
4. **Constraints** — accepted brand, content, accessibility, framework,
   performance, implementation, and repository design-system boundaries.

Use the subject's real vocabulary, materials, tools, artifacts, workflows, and
visual culture as design evidence. If the brief already fixes a direction, obey
it. Do not replace an explicit brief with a preferred house style.

## Load Approved DESIGN.md When Present

Before inventing palette, typography, spacing, shape, component, or other
reusable design-system rules, determine whether the project has an approved
`DESIGN.md` and what scope it governs.

Resolve the artifact in this order:

1. the path explicitly named by the current Owner instruction or active Work
   Block;
2. a registered project design-system path in repository navigation;
3. root `DESIGN.md`;
4. other candidate files only as non-authoritative discovery input until their
   role is established.

When an approved `DESIGN.md` exists:

- read its machine-readable values and human-readable rationale before making
  free visual-system choices;
- treat it as design-domain authority only, subordinate to higher product,
  architecture, brand, accessibility, governance, and Work Block contracts;
- preserve custom or unknown sections even when the current consumer does not
  use them;
- do not edit it unless its path is explicitly inside the approved write-set;
- surface token/prose contradictions as design drift rather than choosing one
  silently; and
- when implementation and `DESIGN.md` disagree, follow the reconciliation
  direction recorded by the active Work Block:
  `design_md_drives_implementation`, `implementation_drives_extraction`, or
  temporary `bidirectional_reconciliation`.

If no approved `DESIGN.md` exists, continue with subject-grounded design and the
repository's existing design system. Absence is not a failure and does not
authorize creating a `DESIGN.md`.

The framework source repository documents this artifact model at
`docs/design/design-md-artifact-contract.md`. A consumer project that installs
only this skill is not required to contain that framework-source path; the rules
above remain self-contained and project-local authority still comes from that
project's own Owner instruction, navigation, and Work Block.

## Choose the Interface Mode Before Composition

Do not apply the same composition defaults to every frontend. Classify the
surface before deciding hierarchy, density, motion, and chrome.

Typical modes include:

- **Marketing / brand surface** — persuasion, identity, narrative, visual recall,
  and conversion may justify large visual anchors, expressive hierarchy, and
  stronger art direction.
- **Operational application** — repeated work, scanning, comparison, navigation,
  and state management usually favor calm hierarchy, organized density,
  predictable placement, restrained decoration, and efficient controls.
- **Focused tool / utility** — the primary workspace and task controls should
  dominate; explanatory marketing content should not displace the usable
  experience.
- **Expressive / game / experimental UI** — playfulness, illustration, motion,
  and atmosphere may carry more weight when they support the actual experience.

These are decision aids, not fixed presets. Existing product conventions and
accepted design-system rules outrank generic mode expectations.

## Design Plan Before Code

For a new interface or material redesign, create a compact design plan before
implementation.

### Working thesis

Capture three short planning statements when they add clarity:

- **Visual thesis:** the intended mood, material quality, energy, and hierarchy.
- **Content plan:** what each major section or region must communicate or enable,
  in the order the user needs it.
- **Interaction thesis:** the few interaction or motion ideas that materially
  improve comprehension, state change, navigation, or character.

The interaction thesis may contain zero, one, or several ideas. Do not invent
motion merely to satisfy a quota.

### Design system

Define or confirm:

- **Color:** use approved `DESIGN.md` or repository-native canonical tokens when
  they exist; otherwise establish a small named palette with exact values and a
  reason each color belongs to this subject.
- **Type:** use approved design-system roles when present; otherwise define at
  least the deliberate roles the content needs, normally display and body, with
  hierarchy, weight, width, spacing, and fallback behavior.
- **Layout:** preserve approved layout/spacing rules when present; otherwise
  create one or more short layout concepts. Use a small ASCII wireframe when it
  clarifies hierarchy, rhythm, or an unusual composition.
- **Signature:** one memorable element that makes the interface specific to the
  brief. This is the primary aesthetic risk; it must be explainable and must not
  contradict the approved design system.
- **Content:** identify the real or representative copy, data, imagery, states,
  and calls to action the design must carry.

When an existing repository already has canonical components, tokens,
typography, spacing, icons, routing, state, or data-fetch patterns, reuse them.
If `DESIGN.md` is present, reconcile it with those implementation primitives
according to the active Work Block before introducing new ones. Translate a
reference design into the repository's system instead of creating a parallel
design system simply to match a screenshot.

For large or multi-page work, surface the design direction for review before a
broad implementation. For a bounded component or page, the active Work Block or
Owner instruction determines whether a separate approval gate is required.

## Critique the Plan Before Building

Run a short specificity check:

- Could the same palette, typography, hero, and layout be pasted into another
  project in the same category with almost no change?
- Are structural devices such as numbering, labels, dividers, or badges carrying
  real information, or merely decorating the page?
- Is the signature element derived from this subject, or just a fashionable
  effect?
- Is any free design choice falling back to a familiar model-generated pattern
  simply because it is easy to generate?
- Does the composition fit the interface mode, or is an operational workspace
  accidentally being treated like a marketing landing page?
- If `DESIGN.md` exists, does the proposal obey its approved scope and
  reconciliation direction without creating a second token/component system?

Common patterns are not forbidden. They require contextual justification. In
particular, do not default mechanically to warm editorial cream/serif palettes,
dark interfaces with one neon accent, newspaper-like grids, oversized metrics,
gradient-led hero sections, or dashboard-card mosaics when the brief gives no
reason for them.

If the answer reveals a generic default or design-system conflict, revise that
part before coding and note what changed and why.

## Design Principles

### Composition Before Components

Establish hierarchy, visual anchor, reading order, density, and spatial rhythm
before deciding which reusable component containers to place everywhere.
Components implement the composition; they should not determine it by default.

Use whitespace, alignment, scale, cropping, contrast, grouping, and media before
adding decorative chrome. Cards are appropriate when the card itself represents
a meaningful object, interaction, grouping, or state boundary. Do not use a card
only because it is the easiest generic container to generate.

For a marketing or branded surface, the first viewport should read as one
coherent composition. For an operational application, the same viewport may
properly read as a workspace with navigation, primary work area, secondary
context, and visible state. The interface mode decides which structure is
correct.

### Hero as Thesis When a Hero Is Appropriate

When the surface genuinely needs a hero, it should express the most
characteristic thing about the subject. That may be a headline, image, product
interaction, animation, live example, or other content. Choose the form because
it communicates the page's thesis, not because it is a standard hero template.

Do not force a hero onto operational software, focused tools, or flows where the
user's primary need is to act immediately.

### Typography as Identity

Typography is part of the interface personality. Choose display and body roles
for the specific brief, then use an intentional scale, line length, weight,
tracking, and spacing system. Do not ban a font merely because it is common; do
not select one merely because it is a familiar default either.

### Structure as Information

Layout conventions should encode meaning. Sequence numbers are for actual
sequences. Eyebrows, rules, cards, grids, badges, and labels should help a user
understand grouping, priority, state, or progression. Remove devices that do not
carry information or support the intended visual rhythm.

### Controls Match the Task

Choose controls for the user's action rather than for visual novelty. Preserve
familiar interaction semantics and the existing product's control vocabulary.
Feature-complete states matter more than decorative novelty: selected, disabled,
loading, error, success, empty, hover, focus, and permission states should exist
where the workflow requires them.

### Motion with a Job

Use motion when it clarifies state, reinforces hierarchy, demonstrates the
subject, or creates one intentional moment. Prefer a small coherent motion
system to many unrelated effects. Respect reduced-motion preferences and avoid
motion that delays or obscures interaction.

### Complexity Matches the Vision

A maximal direction needs enough detail to feel intentional. A minimal direction
needs precision in typography, spacing, alignment, and state design. Do not use
visual complexity as a substitute for a clear concept.

## References and Existing Design Systems

When screenshots, Figma exports, design briefs, or other visual references are
provided, treat them as visual targets while preserving the repository's
canonical implementation patterns and any approved `DESIGN.md` constraints.

Before inventing new primitives, identify:

- approved `DESIGN.md`, when present;
- existing component wrappers;
- color, typography, spacing, radius, and icon tokens;
- responsive breakpoints;
- routing and navigation conventions;
- state-management and data-fetch patterns;
- existing accessibility and interaction behavior.

Match the reference's hierarchy, spacing, proportion, imagery, and responsive
intent using those project-native primitives. When a detail is ambiguous,
choose the simplest implementation consistent with the accepted direction and
record the assumption when it materially affects review. A screenshot, Figma
export, Stitch project, or other external producer does not silently supersede
an approved repository design contract.

## Interface Copy Is Design Material

Write from the user's side of the screen:

- name things by what users recognize and control, not implementation details;
- prefer specific plain language over clever filler;
- use active labels that describe the action, such as `Save changes` rather than
  `Submit`;
- keep action vocabulary consistent through the flow (`Publish` → `Published`);
- make errors state what happened and what the user can do next;
- make empty states direct the next useful action;
- let each text element do one job: label, explain, demonstrate, or guide.

Match tone to the audience and brand while keeping navigation language clear.
Operational interfaces should avoid explanatory marketing copy where direct
controls, labels, state, and contextual help communicate the workflow more
clearly.

## Restraint and Quality Floor

Spend boldness in one place. Let the signature element carry the main visual
risk and keep supporting choices disciplined. Remove decoration that does not
serve the brief.

Before handoff, ensure the implementation has a baseline of:

- responsive behavior down to the required mobile viewport;
- visible keyboard focus and usable interaction states;
- reduced-motion handling where animation exists;
- deliberate loading, empty, error, success, and disabled states where relevant;
- no accidental CSS specificity conflicts or component styles cancelling one
  another;
- content and layout that still work with realistic text lengths and data;
- no unnecessary parallel component/token system when the repository already
  has an accepted one;
- alignment with approved `DESIGN.md` where one is in scope, or an explicit drift
  finding instead of silent divergence.

## Rendered Browser Review Loop

A successful build is not visual evidence. When the environment provides a safe
rendered-inspection capability, use a real browser or equivalent renderer to
inspect the implemented interface.

1. Render representative desktop and mobile viewport sizes.
2. Exercise important navigation and interaction flows, not only the initial
   static screen.
3. Inspect loading, empty, error, selected, hover/focus, and other material
   states when they are in scope.
4. Check hierarchy, overflow, clipping, overlap, alignment, typography,
   responsive transitions, tap targets, and persistent UI chrome.
5. When visual references exist, compare the implementation directly against
   them for both appearance and behavior.
6. Verify that repository-native tokens and components, plus approved
   `DESIGN.md` when present, still preserve one coherent design system rather
   than drifting into parallel systems.
7. Remove unnecessary visual treatment and repeat after material correction.

Playwright is one valid implementation of this loop, not a framework
requirement. Browser automation, computer-use tooling, manual screenshots, or
another approved rendered-inspection method may satisfy the need when they
produce adequate evidence. Missing browser/screenshot capability must be stated
as a limitation rather than converted into visual success.

A graph, DOM inspection, unit test, lint pass, or successful build does not
replace rendered review for a material visual change.

## Agentic SDLC Integration

- **Orchestrator / Architect:** classify the interface mode; establish whether
  an approved `DESIGN.md` exists, its design-domain authority scope, and the
  reconciliation direction with implementation; then decide whether the task
  needs a new design direction, a constrained extension of an existing system,
  or implementation only. Preserve accepted brand, product, accessibility,
  design-system, and repository constraints in the Work Block.
- **Critic:** for material design work, challenge generic defaults, incorrect
  interface-mode assumptions, unjustified aesthetic choices, parallel design
  systems, unresolved `DESIGN.md`/implementation conflicts, missing states,
  accessibility omissions, and mismatch between the brief and the proposed
  signature element.
- **Coder:** implement only the approved write-set and accepted design direction.
  Do not edit `DESIGN.md` unless its path is explicitly writable. The skill does
  not authorize dependencies, assets, fonts, remote services, browser/design
  tools, or files outside scope.
- **Reviewer:** compare the implementation with the brief, interface mode,
  design plan, repository design system, and approved `DESIGN.md` when present;
  check consistency and regressions, and require direct inspection of important
  code rather than trusting screenshots alone.
- **Verifier:** use fresh rendered evidence and applicable deterministic checks.
  A compatible `DESIGN.md` linter or diff tool may provide additional evidence
  only when already available and authorized; it is not required by this skill.
  Verify representative responsive states and material interaction flows when
  capabilities permit. Missing rendered-inspection or optional DESIGN.md tooling
  remains an explicit limitation.

The Owner or active Work Block remains the authority for approvals and Hard
Stops. This skill supplies design method, not permission.

## Relationship to Design Artifacts and Other Skills

- **`DESIGN.md`** — when approved and in scope, use the artifact rules above. In
  the framework source repository, the fuller lifecycle/reconciliation contract
  is `docs/design/design-md-artifact-contract.md`; a consumer project need not
  contain that source-only documentation path.
- **`theme-factory`** — use when the project has a structured theme contract or
  needs reusable theme tokens; do not let a preset replace subject grounding or
  an approved `DESIGN.md`.
- **`brand-guidelines`** — when installed, accepted brand rules constrain this
  skill's free design choices and outrank lower design defaults.
- **`impeccable`** — use for focused UI polish and critique where its narrower
  procedures fit the task. Its DESIGN.md-aware workflows are consumers/producers
  and do not redefine the portable artifact contract.
- **`webapp-testing`** — when installed and inside the active scope, use it for
  browser/rendered execution and evidence; its availability does not authorize
  browser use or expand the Work Block.
- **specialized aesthetic skills** — treat them as candidate directions or
  references, not automatic defaults. The brief, approved design contracts, and
  subject still win.

## Handoff

- **Success condition:** the interface has a subject-specific design rationale,
  correct interface-mode assumptions, a coherent token/layout system, alignment
  with approved `DESIGN.md` when present, one justified signature element where
  appropriate, clear UI copy, required states, repository-native implementation,
  and fresh rendered evidence when rendering is available.
- **Next:** Reviewer checks implementation against the brief, mode, design plan,
  repository design system, and approved `DESIGN.md` where applicable; Verifier
  confirms applicable responsive, accessibility, deterministic, interaction,
  design-contract, and rendered evidence.
- **Auto-proceed:** only inside the active Work Block and its approved write-set.
- **Hard stop:** follow the Owner instruction and Work Block; this skill creates
  no new Hard Stop and waives none.
- **Primary agent:** Scoped Coder for implementation; Critic/Reviewer/Verifier
  remain independent assurance roles where required.

## Method Provenance

### Anthropic adapted base

Adapted from Anthropic `skills/frontend-design/SKILL.md` at immutable commit
`f17010c9bb483898c1d9c9f42dde2b3a98889434` (upstream blob
`decdff43d05908b4c1fc2cfd2d80fc5743440934`). Licensed under Apache License
2.0; see the adjacent `LICENSE.txt`.

The Anthropic-derived layer supplies subject grounding, specificity critique,
interface copy, restrained signature design, and the original design-planning
structure.

### OpenAI methodological delta

Official OpenAI frontend guidance was reviewed on 2026-08-11 from:

- `https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4`
- `https://developers.openai.com/api/docs/guides/frontend-prompt`
- `https://developers.openai.com/codex/use-cases/frontend-designs`

The local adaptation uses provider-neutral ideas from those sources: explicit
visual/content/interaction planning, domain-aware interface modes,
composition-before-components, repository design-system reuse, and rendered
browser verification across representative viewports and states.

OpenAI-specific model steering defaults, fixed visual constants, required icon
libraries, and mandatory tool choices are intentionally not promoted into the
portable framework.

### DESIGN.md interoperability reference

The portable design-system artifact contract maintained in the framework source
repository is:

`docs/design/design-md-artifact-contract.md`

Its interoperability baseline was compared on 2026-08-11 with
`google-labs-code/design.md@9bf8eae67128b6cc55ad9bf86665767deb4c11cd`,
including `docs/spec.md`, `PHILOSOPHY.md`, and `README.md`. The upstream format
identifies itself as `alpha`.

Google Stitch, `@google/design.md`, Figma, MCP, or any other producer/consumer is
optional. None is promoted into framework authority or required by this skill.
