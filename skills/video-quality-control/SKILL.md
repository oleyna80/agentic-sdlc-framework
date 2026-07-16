---
name: video-quality-control
description: Review AI-generated video for visual fidelity, temporal stability, technical validity, responsive composition, loop quality, accessibility risk, and rights/compliance defects. Use after every generation and before post-production or publication.
user-invocable: true
argument-hint: "[candidate video and approved production artifacts]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Agent
---

# Video Quality Control

Review against the approved brief, storyboard, prompt locks, and rights report. Attractive output is not enough.

## Evidence preparation

For each candidate:
- inspect metadata with `ffprobe` or equivalent;
- extract the opening, closing, and storyboard keyframes;
- generate a contact sheet at regular intervals;
- inspect at normal speed and frame-by-frame around transitions and the loop seam;
- compare source references beside extracted frames;
- test the expected desktop and mobile crops.

Do not use OCR as the primary visual review method.

## Blocking visual defects

Reject for:
- subject identity or product geometry drift;
- changed object count, markings, stones, windows, doors, or structural facts;
- deformed hands, faces, limbs, reflections, or shadows;
- added pseudo-text, logos, labels, or UI;
- flicker, texture crawling, exposure pumping, or unstable focus;
- unintended scene cuts or object teleportation;
- camera motion that conflicts with the storyboard;
- loss of the HTML text-safe zone;
- a visible watermark in a production candidate;
- unsafe or misleading content.

## Technical checks

Record:
- codec and container;
- dimensions and aspect ratio;
- duration;
- frame rate;
- audio presence;
- decode errors;
- file size;
- first-frame suitability;
- loop-seam difference;
- crop tests.

## Review result

```yaml
candidate:
result: approved | rejected | revise
blocking_findings:
  - code:
    time_range:
    evidence:
    responsible_stage:
non_blocking_findings: []
technical:
  decode:
  dimensions:
  duration:
  audio:
  size:
visual:
  fidelity:
  temporal_stability:
  composition:
  loop:
  text_safe_zone:
rights:
  visible_watermark:
  source_compliance:
recommended_action:
```

## Responsible-stage routing

- Wrong concept or hierarchy → `media-art-director`
- Missing constraints → `video-creative-brief`
- Timing or loop problem → `short-video-scriptwriter`
- Composition problem → `storyboard-director`
- Camera/light problem → `cinematography-director`
- Prompt ambiguity → `video-prompt-engineer`
- Model capability problem → `video-provider-router`
- Corrupt/incomplete output → `video-generator`

## Approval rule

Approve only when there are no blocking findings. Human aesthetic preference may select among technically approved candidates, but it may not waive rights or safety blocks.
