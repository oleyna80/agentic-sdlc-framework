---
name: cinematography-director
description: Specify camera, framing, lens character, lighting, depth, motion, and continuity for generated or edited website video. Use whenever a video prompt includes cinematic, premium, macro, dynamic, documentary, architectural, or product-shot language.
user-invocable: true
argument-hint: "[brief, script, or storyboard]"
allowed-tools:
  - Read
  - Write
  - Agent
---

# Cinematography Director

Convert aesthetic intent into physically coherent shot instructions.

## Shot specification

Produce:

```yaml
shot_scale:
camera_height:
camera_angle:
lens_character:
depth_of_field:
camera_movement:
movement_speed:
subject_movement:
lighting:
color_temperature:
contrast:
motion_blur:
focus_behavior:
continuity_locks: []
```

## Selection rules

### Shot scale
- `wide`: environment and context;
- `medium`: person or product relationship;
- `close-up`: detail and emotion;
- `macro`: material, texture, jewelry, food, mechanisms.

### Camera movement
- `locked`: stability and factual clarity;
- `dolly-in/out`: reveal or emphasis without perspective distortion from digital zoom;
- `truck/track`: lateral relationship;
- `orbit`: form and dimensionality, risky for exact products;
- `tilt/pan`: controlled reframing;
- `handheld`: documentary energy, generally unsuitable for calm background loops.

Use one dominant camera movement. Do not stack orbit, zoom, pan, and handheld movement in the same short shot.

### Lens and depth
- Wider perspective increases spatial movement and edge distortion.
- Longer or macro character compresses space and isolates detail.
- Extremely shallow depth of field can hide artifacts but may make website text-safe composition unstable.
- Keep the focal plane on the business-critical subject.

### Lighting
Define direction, softness, contrast, and behavior over time. “Cinematic lighting” alone is not a specification.

## Product fidelity

When shape matters:
- prefer locked or shallow-angle camera motion;
- restrict subject rotation;
- avoid full orbit unless a validated multi-view reference exists;
- name immutable geometry;
- avoid reflective highlights that invent edges or markings.

## Website background mode

Default to:
- slow movement;
- stable horizon;
- low-frequency changes;
- no fast focus pulls;
- no flashing light;
- no abrupt exposure changes;
- protected negative space.

## Output prose

Write one compact camera paragraph that can be inserted into a model prompt, followed by a structured shot specification for QC.

## Exit criteria

The camera and subject movements are independently understandable, physically compatible, and appropriate for the final placement.
