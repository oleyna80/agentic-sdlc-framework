---
name: video-postproduction
description: Prepare approved video for web delivery through trimming, loop finishing, audio removal, encoding, responsive variants, posters, metadata, and size budgets. Use only after quality control approves a candidate.
user-invocable: true
argument-hint: "[approved candidate and delivery brief]"
allowed-tools:
  - Read
  - Write
  - Bash
---

# Video Post-production

Transform an approved candidate without changing its approved meaning or hiding defects.

## Required outputs

For a website background, normally produce:

```text
delivery/
├── desktop.webm
├── desktop.mp4
├── mobile.webm
├── mobile.mp4
├── poster-desktop.webp
├── poster-mobile.webp
└── delivery-manifest.json
```

Generate only formats actually required by the target browser policy.

## Processing sequence

1. Preserve the untouched approved source in the candidate workspace.
2. Trim only approved in/out points.
3. Remove audio when the asset is an autoplay background.
4. Finish the loop using the approved loop strategy.
5. Create separate responsive crops only when crop safety was approved; otherwise use separate source generations.
6. Encode WebM and MP4 delivery variants.
7. Generate posters from an approved stable frame.
8. Verify duration, dimensions, decodeability, loop, and file size after encoding.
9. Record all commands and output hashes in the delivery manifest.

## Rules

- Do not use post-production to conceal identity or geometry drift.
- Do not remove visible or invisible watermarks or provenance metadata to evade provider policy.
- Do not upscale merely to advertise a higher resolution.
- Avoid unnecessary frame interpolation.
- Keep background audio absent unless the product explicitly requires sound controls.
- Preserve aspect ratio; never stretch.
- Prefer a shorter well-looped clip to a large long clip.
- Use a poster that matches the first rendered state to reduce visual jumps.

## Size budget

Set a page-specific budget before encoding. Report when visual quality cannot fit the budget rather than silently delivering an oversized file.

## Delivery manifest

```json
{
  "source": "",
  "operations": [],
  "outputs": [
    {
      "path": "",
      "container": "",
      "codec": "",
      "width": 0,
      "height": 0,
      "duration": 0,
      "bytes": 0,
      "sha256": ""
    }
  ],
  "posterFiles": [],
  "loopStrategy": "",
  "audioRemoved": true,
  "verifiedAt": ""
}
```

## Exit criteria

All delivery files decode, meet dimensions and size budgets, preserve the approved content, and have reproducible processing evidence.
