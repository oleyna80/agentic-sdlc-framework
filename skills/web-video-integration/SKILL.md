---
name: web-video-integration
description: Integrate approved video assets into websites with responsive art direction, posters, autoplay constraints, reduced-motion behavior, lazy loading, accessibility, and performance safeguards. Use for React, Next.js, HTML, hero backgrounds, inline demos, and media components.
user-invocable: true
argument-hint: "[delivery assets and target component/page]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
---

# Web Video Integration

Treat video as a progressive enhancement. The page must remain understandable and usable without playback.

## Integration rules

- Use `muted`, `playsInline`, and `loop` for autoplay backgrounds.
- Do not autoplay meaningful audio.
- Supply a poster matching the opening frame.
- Keep headings, logos, CTAs, prices, and legal text in HTML.
- Preserve foreground contrast throughout the entire loop, not only on the poster.
- Provide a static reduced-motion alternative.
- Avoid loading below-the-fold video during initial navigation.
- Prefer responsive source selection or separate components when desktop and mobile compositions differ.
- Never stretch a source to a different aspect ratio.
- Ensure failure to load does not collapse layout.

## React/Next.js pattern

Use the project conventions, but preserve these semantics:

```tsx
type BackgroundVideoProps = {
  desktopWebm: string;
  desktopMp4: string;
  mobileWebm?: string;
  mobileMp4?: string;
  poster: string;
  className?: string;
};

export function BackgroundVideo(props: BackgroundVideoProps) {
  return (
    <video
      aria-hidden="true"
      autoPlay
      muted
      loop
      playsInline
      poster={props.poster}
      preload="metadata"
      className={props.className}
    >
      <source media="(max-width: 767px)" src={props.mobileWebm} type="video/webm" />
      <source media="(max-width: 767px)" src={props.mobileMp4} type="video/mp4" />
      <source src={props.desktopWebm} type="video/webm" />
      <source src={props.desktopMp4} type="video/mp4" />
    </video>
  );
}
```

Omit undefined mobile sources in the real implementation.

## Reduced motion

Use CSS or application state so `prefers-reduced-motion: reduce` receives:
- the poster or an equivalent static image;
- no essential information lost;
- no automatic playback.

Do not merely reduce playback speed.

## Loading strategy

- Above-the-fold hero: preload metadata or an intentionally selected source; avoid preloading every format.
- Below-the-fold: mount or set `src` near the viewport.
- Product demo initiated by the user: show controls and meaningful accessible labeling.
- Background decorative video: `aria-hidden="true"` and no controls.

## Verification

Test:
- desktop and mobile viewport crops;
- slow network and failed request;
- reduced-motion preference;
- autoplay behavior on mobile;
- layout shift;
- text contrast at multiple frames;
- page weight and loading waterfall;
- poster-to-video transition.

## Exit criteria

The component is accessible, responsive, fault-tolerant, performance-bounded, and visually consistent with the approved storyboard.
