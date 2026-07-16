---
name: storyboard-director
description: Turn a short-video brief and script into shot-level composition instructions. Use for multiple beats, first/last-frame control, responsive crops, text-safe layouts, continuity-sensitive product animation, or any generation where a written prompt alone is ambiguous.
user-invocable: true
argument-hint: "[brief and visual beat script]"
allowed-tools:
  - Read
  - Write
  - Agent
---

# Storyboard Director

Define the visual states that generation and review will use as evidence.

## When a storyboard is mandatory

Create one when:
- the clip contains more than one shot or distinct beat;
- the first and last frames must match;
- desktop and mobile need different compositions;
- product geometry or identity must remain fixed;
- HTML text needs a protected safe zone;
- the clip uses transitions, occlusion, or a hidden loop seam.

## Frame plan

For each shot or keyframe, record:

```yaml
shot_id:
time_range:
frame_role: opening | key | transition | closing
shot_scale:
camera_position:
camera_movement:
subject_position:
subject_action:
foreground:
background:
lighting_state:
text_safe_zone:
continuity_locks: []
allowed_changes: []
forbidden_changes: []
reference_asset:
```

## Composition rules

- Use a stable coordinate vocabulary: left/right/center and percentages.
- Define the subject zone separately from the text-safe zone.
- Keep critical subject detail away from crop-sensitive edges.
- Preserve horizon, architecture, product count, and object topology when factual fidelity matters.
- Match screen direction across cuts.
- Avoid unexplained object entrances and exits.
- Keep opening and closing frames structurally compatible for loops.
- For image-to-video, use the source image as the opening keyframe unless the brief says otherwise.

## Responsive storyboard

Do not derive mobile by blindly cropping desktop. For each format, specify:
- subject anchor;
- safe zone;
- relative scale;
- permitted crop;
- whether a separate generation is required.

## Output

Produce:
1. a shot table;
2. opening-frame specification;
3. closing-frame specification;
4. continuity locks;
5. responsive variations;
6. a list of review frames to extract after generation.

## Exit criteria

A reviewer should be able to compare the generated frames with the storyboard and identify drift without interpreting vague artistic language.
