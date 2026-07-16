---
name: video-creative-brief
description: Convert a website, product, brand, or campaign goal into a production-ready short-video brief. Use before any AI video generation, image-to-video animation, hero loop, product animation, or multi-format social/site deliverable.
user-invocable: true
argument-hint: "[asset objective and available source media]"
allowed-tools:
  - Read
  - Write
  - Agent
---

# Video Creative Brief

Create a concise production contract that downstream skills can execute without guessing.

## Required inputs

Inspect the project and capture:
- business objective;
- page placement and intended viewer action;
- brand tone and visual system;
- source assets and their ownership status;
- factual elements that must not change;
- target devices and aspect ratios;
- duration, loop, audio, and autoplay requirements;
- budget and candidate limit;
- delivery deadline when relevant.

Do not infer permission to use a source asset merely because it exists in the repository.

## Brief format

```yaml
asset_id:
purpose:
business_goal:
placement:
audience:
brand_attributes: []
focal_subject:
source_assets:
  - path:
    role:
    rights_status:
must_preserve: []
must_avoid: []
duration_seconds:
loop:
audio:
motion_intensity:
deliverables:
  - name:
    aspect_ratio:
    viewport:
    subject_zone:
    text_safe_zone:
    target_resolution:
poster_requirement:
candidate_limit:
max_cost:
approval_owner:
```

## Brief quality rules

- Write observable objectives, not vague adjectives alone.
- Define one focal subject.
- Translate “premium,” “modern,” or “dynamic” into composition, light, material, movement, and pacing.
- Separate immutable facts from stylistic preferences.
- State whether the output is a background, foreground narrative, product demonstration, or transition.
- For a background, prohibit dialogue, embedded text, abrupt cuts, and dominant motion unless explicitly required.
- For image-to-video, specify what may move and what must remain locked.
- Create separate deliverable rows for desktop and mobile when composition differs.

## Examples of precise constraints

Prefer:

```yaml
must_preserve:
  - pendant silhouette
  - stone count and placement
  - warm ivory fabric color
motion:
  subject: subtle clockwise rotation under 5 degrees
  camera: slow macro dolly-in
  environment: fabric remains nearly still
```

Avoid:

```yaml
style: make it beautiful and luxurious
```

## Exit criteria

The brief is ready only when:
- downstream agents can derive timing and shots without inventing business intent;
- rights status is explicit;
- aspect ratio and safe zones are measurable;
- the budget and candidate count are bounded;
- the approval owner is named by role or user.
