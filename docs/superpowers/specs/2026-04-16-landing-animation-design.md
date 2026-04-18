# Landing Page Animation Redesign

**Date:** 2026-04-16  
**Status:** Approved

## Problem

The existing `fade-up` animation only animates `transform: translateY` — no opacity. Elements are always fully visible and just slide up 16px, making the animation feel incomplete. The easing curve (`ease`) is generic and doesn't give the polished settle that modern sites use.

## Solution: Approach A — Fix + Refine

### Keyframe

Add opacity to make it a true fade-and-rise:

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Easing

Replace `ease` with `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-expo) on all animated elements. Fast off the mark, graceful settle.

### Duration + stagger

- Text elements (name, role, tagline, location, icon-links): `0.6s`, stagger `0.08s` apart
- Photo: `0.7s` at `0s` delay — slightly slower to feel more substantial

### Selectors affected

`assets/main.css` only — no template or script changes:

- `@keyframes fade-up`
- `.landing-photo` animation shorthand
- `.landing-name` animation shorthand
- `.landing-role` animation shorthand
- `.landing-tagline` animation shorthand
- `.landing-location` animation shorthand
- `.icon-links` animation shorthand

### Reduced motion

No changes needed — existing `prefers-reduced-motion` block already disables all animation on these selectors.
