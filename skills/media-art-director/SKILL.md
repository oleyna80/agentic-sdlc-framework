---
name: media-art-director
description: Decide whether and how motion should be used in a website or digital product. Use for hero videos, animated backgrounds, product reveals, image animation, motion concepts, and any request where an agent might otherwise add video merely because generation is available.
user-invocable: true
argument-hint: "[page or visual objective]"
allowed-tools:
  - Read
  - Write
  - Agent
---

# Media Art Director

Choose the smallest motion medium that communicates the intended message.

## Core decision

Classify the request:

| Need | Preferred medium |
|---|---|
| Microinteraction, button, icon, state feedback | CSS, Motion, GSAP, or Rive |
| Vector illustration with interactive states | Rive or Lottie |
| Scroll choreography using existing page elements | GSAP/Motion |
| Photorealistic atmosphere or product scene | Generated or filmed video |
| Exact product geometry or legally sensitive subject | Controlled photography/3D first; generative motion only with strict references |
| Decorative movement with no message | Prefer static media |

Do not recommend generative video when:
- it competes with the primary CTA;
- it cannot survive mobile cropping;
- it adds substantial page weight without narrative value;
- the source asset requires exact factual representation that the model may alter;
- the page already has high motion density;
- reduced-motion users would lose essential information.

## Direction statement

Produce:

```yaml
media_decision:
  medium:
  purpose:
  placement:
  focal_subject:
  viewer_action:
  motion_intensity: none | low | medium | high
  desktop_strategy:
  mobile_strategy:
  reduced_motion_strategy:
  expected_value:
  key_risks: []
```

## Website composition rules

- Reserve stable negative space for HTML text and controls.
- Keep logos, prices, labels, and legal text outside generated pixels.
- Avoid critical action at the extreme edges.
- Treat desktop and mobile as separate compositions when the subject cannot remain legible through cropping.
- Prefer calm, low-amplitude motion for background video.
- Avoid camera movement and subject movement competing at the same intensity.
- Ensure the first frame works as a static poster.

## Approval criteria

Approve the direction only when:
- the medium matches the communication need;
- the mobile and reduced-motion alternatives are explicit;
- the subject, safe zone, and visual hierarchy are clear;
- the expected value justifies generation and delivery cost;
- the request can proceed without inventing rights to third-party material.

Return `static_or_interactive_alternative` when generative video is not the best choice.
