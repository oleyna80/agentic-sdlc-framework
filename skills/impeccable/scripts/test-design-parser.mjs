import assert from 'node:assert/strict';
import { assessCoverage, parseDesignMd } from './design-parser.mjs';

const legacy = `---
name: Legacy
colors:
  primary: "#112233"
---
# Design System: Legacy
## Overview
**Creative North Star: "Quiet Tool"**
A calm working interface.
## Colors
### Primary
- **Ink** (#112233): text.
## Typography
**Body Font:** Inter (with sans-serif)
### Hierarchy
- **Body** (400, 16px, 1.5): Reading.
## Elevation
Flat at rest.
## Components
### Buttons
- **Primary:** Filled action.
- **Shape:** 4px.
## Do's and Don'ts
- **Do** keep controls direct.
- **Don't** add decoration without a job.
`;

const legacyModel = parseDesignMd(legacy);
assert.equal(legacyModel.schemaVersion, 2);
assert.equal(legacyModel.overview.creativeNorthStar, 'Quiet Tool');
assert.equal(legacyModel.colors.groups.length, 1);
assert.ok(legacyModel.elevation);
assert.equal(legacyModel.layout, null);
assert.equal(legacyModel.shapes, null);
assert.equal(legacyModel.customSections.length, 0);
assert.equal(legacyModel.diagnostics.length, 0);

const richLegacy = `# Rich Legacy
## Overview
### The "Layering" Principle
Surfaces remain flat until interaction requires depth.
## Colors
- **Primary (#00478d):** Primary action.
- **Secondary (#b8422e):** Sparse annotation.
## Typography
- **Display & Headlines (Noto Serif):** Editorial display voice.
- **UI & Body (Public Sans):** Utility and body text.
## Elevation
### Shadow Vocabulary
- **Ambient** (\`box-shadow: 0 12px 40px rgba(0,0,0,.16)\`): Floating overlays only.
## Components
### Buttons
- **Primary:** Filled action.
## Do's and Don'ts
- **Do** preserve hierarchy.
`;

const richLegacyModel = parseDesignMd(richLegacy);
assert.equal(richLegacyModel.typography.fonts.display.family, 'Noto Serif');
assert.equal(richLegacyModel.typography.fonts.body.family, 'Public Sans');
assert.equal(richLegacyModel.colors.groups[0].role, 'Primary');
assert.equal(richLegacyModel.colors.groups[1].role, 'Secondary');
assert.equal(richLegacyModel.elevation.shadows[0].name, 'Ambient');
assert.match(richLegacyModel.elevation.shadows[0].value, /0 12px 40px/);
assert.match(richLegacyModel.overview.philosophy[0], /Surfaces remain flat/i);
assert.equal(richLegacyModel.diagnostics.length, 0);

const modern = `---
version: alpha
name: Modern
omitted:
  - spacing
  - section: rounded
    reason: "Square geometry"
colors:
  primary: "oklch(62% 0.18 250)"
  surface: "#ffffff"
typography:
  body:
    fontFamily: "Public Sans"
    fontSize: 1rem
components:
  button-primary:
    backgroundColor: "{colors.primary}"
---
# Modern System
## Brand & Style
**Specific reference: "Laboratory field notebook"**
Dense, practical, annotated.
## Colors
- **Primary (oklch(62% 0.18 250)):** action accent.
## Typography
Public Sans carries reading text.
## Layout & Spacing
A fixed-max-width grid with 24px gutters.
- Align data columns across sections.
## Elevation & Depth
Depth comes from tonal layers.
## Shapes
Square controls with one reserved pill status shape.
## Components
### Button
- **Primary:** uses {colors.primary}.
- **Focus:** visible ring.
## Do’s and Don’ts
- **Do** keep metadata aligned.
- **Don't** add marketing hero chrome.
## Motion
Fast mechanical transitions; respect reduced motion.
`;

const modernModel = parseDesignMd(modern);
assert.equal(modernModel.designMdFormatVersion, 'alpha');
assert.equal(modernModel.frontmatter.colors.primary, 'oklch(62% 0.18 250)');
assert.deepEqual(modernModel.omitted, [
  { section: 'spacing', reason: null },
  { section: 'rounded', reason: 'Square geometry' },
]);
assert.match(modernModel.layout.description, /fixed-max-width grid/i);
assert.match(modernModel.shapes.description, /Square controls/i);
assert.equal(modernModel.customSections.length, 1);
assert.equal(modernModel.customSections[0].name, 'Motion');
assert.deepEqual(modernModel.sectionOrder, [
  'Overview',
  'Colors',
  'Typography',
  'Layout',
  'Elevation & Depth',
  'Shapes',
  'Components',
  "Do's and Don'ts",
]);
assert.equal(modernModel.diagnostics.length, 0);

const duplicate = `# Duplicate
## Overview
First.
## Overview
Second.
`;
const duplicateModel = parseDesignMd(duplicate);
assert.equal(duplicateModel.diagnostics[0].code, 'duplicate-section');
assert.match(duplicateModel.overview.philosophy[0], /First/);

const coverage = assessCoverage(modernModel);
assert.equal(coverage.omitted, 2);
assert.equal(coverage.customSections, 1);
assert.equal(coverage.diagnostics, 0);
assert.notEqual(coverage.layout, 'missing');
assert.notEqual(coverage.shapes, 'missing');

console.log('impeccable DESIGN.md parser compatibility: PASS');
