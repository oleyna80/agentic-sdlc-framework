---
name: short-video-scriptwriter
description: Write visual beat scripts for very short website videos, loops, product reveals, and AI-generated clips. Use for 3–15 second media where timing, progression, and loop structure matter, including clips without dialogue.
user-invocable: true
argument-hint: "[creative brief]"
allowed-tools:
  - Read
  - Write
  - Agent
---

# Short Video Scriptwriter

Write for visible change over time. Do not turn a six-second website loop into a conventional screenplay.

## Script types

Choose one:
- `ambient_loop`: subtle continuous atmosphere;
- `product_reveal`: controlled reveal of a product or material;
- `feature_demonstration`: one clear action and outcome;
- `brand_moment`: emotional visual statement;
- `transition`: start and end states are the product;
- `micro_narrative`: setup, change, resolution within 6–15 seconds.

## Beat design

Use 2–4 beats. Each beat must contain:
- time range;
- visible action;
- camera behavior;
- continuity requirement;
- purpose.

Example:

```text
0.0–1.5 — The pendant is already readable. A soft highlight enters from the upper right. Camera remains nearly static. Establish premium material.
1.5–4.5 — Slow macro dolly-in. Pendant rotates no more than five degrees. Preserve shape and stone placement. Create depth.
4.5–6.0 — Motion settles toward the opening pose. Highlight fades to the initial position. Prepare seamless loop.
```

## Loop architecture

For looping backgrounds, choose:
- `return`: end state returns to the opening pose;
- `ping_pong_safe`: motion can reverse without looking artificial;
- `continuous`: cyclical movement naturally crosses the seam;
- `hidden_cut`: seam occurs during occlusion, blur, or uniform motion.

Do not rely on an abrupt generated endpoint and “fix it later.”

## Writing rules

- One principal action per shot.
- Prefer verbs that can be observed: rotates, settles, reflects, passes, opens, reveals.
- Keep product and camera motion independently specified.
- Make the first frame useful as a poster.
- Avoid dialogue and audio unless the brief requires foreground storytelling.
- Do not write embedded typography, logos, prices, or UI into the scene.
- State immovable elements explicitly.
- Use restrained pacing for autoplay backgrounds.

## Deliverable

```yaml
script_type:
duration_seconds:
opening_state:
beats:
  - time:
    visible_action:
    camera:
    continuity:
    purpose:
closing_state:
loop_strategy:
audio_notes:
```

## Exit criteria

The script is ready when every second has a purpose, the loop strategy is explicit, and no beat requires the model to guess what must remain unchanged.
