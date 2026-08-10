---
name: frontend-design
description: Create or reshape distinctive, production-grade frontend interfaces from the real subject, audience, and job of the page. Use for visual direction, UI composition, typography, interaction, interface copy, and frontend design implementation while avoiding templated defaults.
license: Apache-2.0; see LICENSE.txt
source: https://github.com/anthropics/skills/tree/main/skills/frontend-design
metadata:
  upstream_repository: https://github.com/anthropics/skills
  upstream_path: skills/frontend-design/SKILL.md
  upstream_revision: f17010c9bb483898c1d9c9f42dde2b3a98889434
  upstream_blob: decdff43d05908b4c1fc2cfd2d80fc5743440934
  last_checked: 2026-08-10
  local_modification: Adapted for Agentic SDLC roles, authority boundaries, handoff, and verification; upstream guidance condensed and reorganized.
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
and existing brand system as inputs to design, not decoration added after the
layout is chosen.

This local version adapts Anthropic's `frontend-design` guidance to the Agentic
SDLC. It does not grant write authority, expand a Work Block, choose a runtime,
or waive review and verification requirements.

## Ground the Direction in the Subject

Before designing, establish four facts:

1. **Subject** — the concrete product, service, organization, or experience.
2. **Audience** — the people who must understand or use it.
3. **Single job** — the primary thing this page or flow must accomplish.
4. **Constraints** — accepted brand, content, accessibility, framework,
   performance, and implementation boundaries.

Use the subject's real vocabulary, materials, tools, artifacts, workflows, and
visual culture as design evidence. If the brief already fixes a direction, obey
it. Do not replace an explicit brief with a preferred house style.

## Design Plan Before Code

For a new interface or material redesign, create a compact design plan before
implementation:

- **Color:** 4–6 named color tokens with exact values and a reason each belongs
  to this subject.
- **Type:** at least two deliberate roles, normally display and body; add a
  utility/data role only when the content needs it. Define hierarchy, weight,
  width, spacing, and fallback behavior.
- **Layout:** one or more short layout concepts. Use a small ASCII wireframe when
  it clarifies hierarchy, rhythm, or an unusual composition.
- **Signature:** one memorable element that makes the interface specific to the
  brief. This is the primary aesthetic risk; it must be explainable.
- **Content:** identify the real or representative copy, data, imagery, states,
  and calls to action the design must carry.

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

Common patterns are not forbidden. They require contextual justification. In
particular, do not default mechanically to warm editorial cream/serif palettes,
dark interfaces with one neon accent, newspaper-like grids, oversized metrics,
or gradient-led hero sections when the brief gives no reason for them.

If the answer reveals a generic default, revise that part before coding and note
what changed and why.

## Design Principles

### Hero as Thesis

The hero should express the most characteristic thing about the subject. That
may be a headline, image, product interaction, animation, live example, or other
content. Choose the form because it communicates the page's thesis, not because
it is a standard hero template.

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

### Motion with a Job

Use motion when it clarifies state, reinforces hierarchy, demonstrates the
subject, or creates one intentional moment. Prefer one coordinated motion idea
to many unrelated effects. Respect reduced-motion preferences and avoid motion
that delays or obscures interaction.

### Complexity Matches the Vision

A maximal direction needs enough detail to feel intentional. A minimal direction
needs precision in typography, spacing, alignment, and state design. Do not use
visual complexity as a substitute for a clear concept.

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
- content and layout that still work with realistic text lengths and data.

## Visual Review Loop

When the environment supports rendered inspection:

1. render the changed interface at representative desktop and mobile sizes;
2. capture screenshots or equivalent visual evidence;
3. compare the result to the accepted design plan and real brief;
4. check hierarchy, overflow, alignment, typography, interaction states, and
   whether the signature element dominates appropriately;
5. remove one unnecessary visual treatment before declaring the design ready;
6. repeat after material correction.

A graph, DOM inspection, test suite, or successful build does not replace visual
review for a visual change.

## Agentic SDLC Integration

- **Orchestrator / Architect:** establish whether the task needs a new design
  direction, a constrained extension of an existing system, or implementation
  only. Preserve accepted brand and product constraints in the Work Block.
- **Critic:** for material design work, challenge generic defaults, unjustified
  aesthetic choices, missing states, accessibility omissions, and mismatch
  between the brief and the proposed signature element.
- **Coder:** implement only the approved write-set and accepted design direction.
  The skill does not authorize dependencies, assets, fonts, remote services, or
  files outside that scope.
- **Reviewer:** compare the implementation with the brief and design plan, check
  consistency and regressions, and require direct inspection of important code
  rather than trusting screenshots alone.
- **Verifier:** use fresh rendered evidence and applicable deterministic checks.
  Missing screenshot/browser capability must be reported as a limitation rather
  than converted into visual success.

The Owner or active Work Block remains the authority for approvals and Hard
Stops. This skill supplies design method, not permission.

## Relationship to Other Design Skills

- **`theme-factory`** — use when the project has a structured theme contract or
  needs reusable theme tokens; do not let a preset replace subject grounding.
- **`brand-guidelines`** — when installed, accepted brand rules constrain this
  skill's free design choices.
- **`impeccable`** — use for focused UI polish and critique where its narrower
  procedures fit the task.
- **specialized aesthetic skills** — treat them as candidate directions or
  references, not automatic defaults. The brief and subject still win.

## Handoff

- **Success condition:** the interface has a subject-specific design rationale,
  a coherent token/layout system, one justified signature element, clear UI
  copy, required states, and fresh visual evidence when rendering is available.
- **Next:** Reviewer checks implementation against the design plan; Verifier
  confirms applicable responsive, accessibility, deterministic, and rendered
  evidence.
- **Auto-proceed:** only inside the active Work Block and its approved write-set.
- **Hard stop:** follow the Owner instruction and Work Block; this skill creates
  no new Hard Stop and waives none.
- **Primary agent:** Scoped Coder for implementation; Critic/Reviewer/Verifier
  remain independent assurance roles where required.

## Upstream Provenance

Adapted from Anthropic `skills/frontend-design/SKILL.md` at immutable commit
`f17010c9bb483898c1d9c9f42dde2b3a98889434` (upstream blob
`decdff43d05908b4c1fc2cfd2d80fc5743440934`), checked 2026-08-10.
Licensed under Apache License 2.0; see the adjacent `LICENSE.txt`.

Local changes intentionally add Agentic SDLC authority boundaries, role routing,
visual-evidence handoff, and relationships to the framework's design skill
library while preserving the upstream subject-grounded design philosophy.
