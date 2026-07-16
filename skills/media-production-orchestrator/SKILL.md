---
name: media-production-orchestrator
description: Coordinate end-to-end AI media production for websites and digital products. Use whenever a task involves creating, animating, generating, reviewing, optimizing, licensing, or integrating video or motion assets, even when the user only asks for a hero animation or “make this image move.”
user-invocable: true
argument-hint: "[page, asset, campaign, or media objective]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
---

# Media Production Orchestrator

Run a controlled production pipeline instead of jumping directly to a generation API.

## Authority model

- You own routing, stage transitions, scope, budget, and evidence.
- Only `video-generator` may initiate a paid generation request.
- `media-rights-compliance` may block generation or publication.
- `video-quality-control` may reject an output but may not silently regenerate it.
- Human approval is required before a generated asset is published to a client-facing production environment.
- Never expose, print, commit, or copy provider credentials into project files.

## Required pipeline

1. **Need assessment**
   - Invoke `media-art-director`.
   - Decide whether the requirement calls for generative video, conventional editing, Rive/Lottie, CSS/GSAP, or a static image.
   - Stop if motion adds no clear communication or business value.

2. **Brief**
   - Invoke `video-creative-brief`.
   - Produce a structured brief with placement, objective, source assets, aspect ratios, duration, safe zones, motion intensity, budget, and ownership status.

3. **Rights preflight**
   - Invoke `media-rights-compliance`.
   - Require evidence for source-asset rights, model commercial terms, watermark policy, and consent where identifiable people are involved.
   - Do not continue when the status is `blocked`.

4. **Creative development**
   - Invoke `short-video-scriptwriter` for timing and visual beats.
   - Invoke `storyboard-director` when there is more than one beat, a loop seam, a text-safe composition, or multiple deliverables.
   - Invoke `cinematography-director` for framing, camera, lens, lighting, continuity, and motion.

5. **Prompt and provider**
   - Invoke `video-prompt-engineer` to build the generation prompt.
   - Invoke `video-provider-router` to select an approved provider/model from the project registry.
   - Record the estimated cost and fallback route before generation.

6. **Generation**
   - Invoke `video-generator`.
   - Generate only the approved number of candidates.
   - Persist a generation manifest for every request and result.

7. **Review**
   - Invoke `video-quality-control`.
   - Reject outputs with identity drift, geometry drift, text artifacts, flicker, unsafe content, unusable safe zones, or loop discontinuity.
   - A rejected output returns to the smallest responsible stage; do not restart the entire pipeline automatically.

8. **Post-production**
   - Invoke `video-postproduction`.
   - Produce delivery variants, posters, metadata, and optimization evidence.

9. **Integration**
   - Invoke `web-video-integration`.
   - Integrate with accessibility, reduced-motion, performance, responsive art direction, and fallback behavior.

10. **Closeout**
    - Record selected asset, rejected candidates, provider/model, terms verification date, total cost, source assets, checks, and human approval.

## Standard artifacts

Use a dedicated workspace:

```text
media/<asset-id>/
├── brief.md
├── rights-check.md
├── script.md
├── storyboard.md
├── prompt.md
├── provider-decision.md
├── generation-manifest.json
├── candidates/
├── review/
├── delivery/
└── closeout.md
```

The project may use another location, but keep the same separation of planning, raw candidates, review evidence, and final delivery.

## Budget gate

Before each paid call, confirm:

```yaml
generation_gate:
  purpose: approved
  provider: approved
  model: approved
  candidate_count: approved
  estimated_cost: within_budget
  source_rights: cleared
  commercial_terms: verified
  visible_watermark: forbidden_for_production
  human_approval_before_publish: required
```

If any field is unknown, do not generate.

## Retry policy

- Retry transport or provider errors at most twice with bounded backoff.
- Do not count technical retries as creative iterations when the provider produced no billable output.
- Do not automatically regenerate an aesthetically weak result. Return the QC evidence and revise the responsible brief, shot, or prompt.
- Never use an expensive fallback without updating the cost estimate.

## Reference

> **Reference:** [`reference/production-contract.md`](reference/production-contract.md) — read when creating a new project profile, defining stage artifacts, or wiring this pipeline into an existing SDLC.
