---
name: video-prompt-engineer
description: Translate an approved brief, script, storyboard, and cinematography plan into model-ready video prompts and constraints. Use before text-to-video, image-to-video, video-to-video, first/last-frame generation, or provider-specific prompt adaptation.
user-invocable: true
argument-hint: "[approved production artifacts and target provider]"
allowed-tools:
  - Read
  - Write
  - Agent
---

# Video Prompt Engineer

Produce prompts from approved production decisions. Do not invent a new creative direction at this stage.

## Prompt order

Use this order unless the selected provider documents another preferred grammar:

1. subject and immutable identity;
2. permitted subject action;
3. environment and material behavior;
4. shot scale and composition;
5. camera movement;
6. lens, focus, and lighting;
7. timing and pacing;
8. continuity and loop instruction;
9. exclusions and artifact prevention;
10. output format constraints.

## Image-to-video rule

When a reference image exists, describe motion rather than re-describing the entire image. Re-description can cause the model to replace details that should remain locked.

Prefer:

```text
Preserve the supplied pendant exactly. Over six seconds, add a very slow macro dolly-in while the pendant rotates clockwise by less than five degrees. Keep the stone count, silhouette, chain attachment, ivory fabric, and left-side negative space unchanged.
```

Avoid:

```text
Create a beautiful gold pendant on luxurious fabric...
```

## Prompt package

Produce:

```yaml
mode: text-to-video | image-to-video | first-last-frame | video-to-video
positive_prompt:
negative_constraints:
reference_files: []
locked_elements: []
allowed_motion:
camera:
duration:
aspect_ratio:
seed_policy:
provider_parameters: {}
```

## Negative constraints

Write observable exclusions:
- no added objects;
- no text or pseudo-text;
- no logo mutation;
- no extra fingers or limbs;
- no geometry changes;
- no camera shake;
- no flicker or exposure pumping;
- no scene cut;
- no crop into the protected zone.

Do not rely on huge generic negative-prompt lists. Include only risks relevant to the shot and provider.

## Provider adaptation

Before finalizing, inspect the selected provider profile for:
- supported durations and aspect ratios;
- whether negative prompts are supported;
- first/last-frame or reference-image limits;
- seed support;
- safety and moderation behavior;
- parameter names.

Keep the provider-neutral prompt and the adapted request separately so the creative intent survives provider changes.

## Exit criteria

The prompt contains no contradiction between storyboard, camera, duration, and loop strategy, and every immutable element appears in the lock list.
