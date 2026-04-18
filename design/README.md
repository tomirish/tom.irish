# Tom Irish Design System

A design system distilled from [tom.irish](https://tom.irish) — a single-page personal site and resume built by Tom Irish, a senior engineering leader at Expeditors (Seattle). The site is intentionally minimal: one crimson accent, a serif-sans pairing, a warm off-white canvas, and a quiet two-column resume view that feels like stationery.

**Source repository:** `tomirish/tom.irish` on GitHub (default branch `main`). The production site is [tom.irish](https://tom.irish). Raw imports live in `source/` for reference.

## Products represented

There is one product: **the personal website.** It has two views wired together via CSS `:target` and a hash — a landing hero (`#home`) and a resume view (`#resume`) — plus a printable PDF generated from a parallel template. The PDF is a separate layer (`source/resume.template.html` + `source/pdf.css`) and is not covered by the UI kit.

---

## Index

```
README.md              ← you are here
SKILL.md               ← Agent Skills front-matter + instructions
colors_and_type.css    ← design tokens + semantic type styles
assets/
  icons.svg            ← SVG sprite: mail, linkedin, github, file, moon, sun
preview/               ← small cards rendered in the Design System tab
source/                ← verbatim copies of the original repo's key files
ui_kits/
  website/             ← React recreation of the landing + resume views
```

No font files are shipped. DM Sans and Playfair Display are loaded from Google Fonts via CDN — the site was designed around that constraint. If you need offline fonts, download from Google Fonts and drop into `fonts/`.

---

## Content fundamentals

**Voice.** First-person, plain-spoken, quietly confident. No hype, no superlatives. Achievements are stated as numbers ("99.5%+ availability", "$465K in infrastructure cost savings, a 38.4% reduction") rather than adjectives. The tagline — "Engineering leader building the systems that keep global freight moving." — is representative: a single declarative sentence.

**Casing.** Sentence case for headings in copy ("Key Achievements", "Professional Summary"). Title case for job titles ("Senior Manager"). All-caps only on tiny micro-labels (`.landing-location`, `.skill-group-label`) with generous letter-spacing.

**Pronouns.** "My" and "I" in the professional summary — the voice of the person, not the resume. Everything else is implicit subject ("Own the global connectivity platform…", "Lead a $10M+ cost center…") — bullet points start with present-tense verbs when the role is current, past-tense when historical.

**Emoji.** None in the web layer. A few emoji appear in the source's README tables (✅ 📖 🔧) but they are repo-scaffolding signals, not brand. Do not use emoji in site output.

**Tone specifics.** "Calm under pressure." "Genuinely investing in the growth and careers of the individuals on my team." The site signals reliability and empathy over flash — design mirrors that.

---

## Visual foundations

**Palette.** One accent: crimson `#9b2335` (light) / `#c4394e` (dark). Everything else is warm neutral — a bone page background (`#faf9f7`), a stone sidebar (`#edeae5`), ink text (`#111`), and a gentle grey ramp `#333 → #555 → #666 → #767676`. In dark mode the page drops to near-black (`#131313`) with warm cream text (`#f0ece8`). No gradients, no second accent, no semantic colors (there are no buttons to make green or red).

**Typography.** Playfair Display 700 for every name, every section heading, and nothing else. DM Sans 400/500/600 for everything operational — body, bullets, pills, labels. The pairing is the whole voice: an elegant serif for identity, a modern geometric sans for competence.

**Spacing.** Loose 8-point rhythm: `4 · 8 · 14 · 16 · 24 · 28 · 32 · 56`. Section padding is 28×32. The landing stacks photo + text with a `gap: 56px`. Bullets sit `18px` from their chevron. Skill tags ride a `6px` gap.

**Backgrounds.** Flat color only. No textures, no patterns, no illustrations, no photography outside the single portrait slot on the landing and resume header. The resume sidebar's warm stone surface is the only background contrast — and even that shifts to the bone page color on mobile.

**Signature motif: the 4 px crimson stripe.** Both views begin with a 4 px accent stripe at the top edge. It is the single strongest brand signal and it is always flat `#9b2335`. Do not gradient it.

**Signature motif: the chevron bullet (`›`).** Achievements, job bullets, and certifications all use a single-character `›` positioned absolutely at `left: 0`, colored crimson. Never `•`, never em-dashes, never checkmarks.

**Borders.** Hairline (`1px`) for rules and dividers, in a narrow ramp — `#eeeeee` (section rules, job separators), `#e0e0e0` (pill borders, icon-link rings), `#dedad5` (the warm divider between resume main and sidebar). Dark mode uses `#484848 / #363636 / #383634` equivalents.

**Corner radii.** `6px` (resume header photo), `10px` (skill tag), `12px` (contact pill), `20px` (landing photo), `50%` (icon-link circles). No sharp 0-radius corners except the 4 px accent stripe itself.

**Shadows.** Three tiers, all soft and warm, all black — not colored:
- `0 4px 24px rgba(0,0,0,0.13)` — landing photo (the hero lift)
- `0 2px 8px rgba(0,0,0,0.10)` — resume header photo
- `0 2px 8px rgba(0,0,0,0.04)` — sticky header (barely there)

No inner shadows. No colored glows. In dark mode photos get a `0 0 0 1px rgba(255,255,255,0.10)` ring instead of a shadow, to separate them from the near-black background.

**Animation.** A single entrance motion: `fade-up` — `translateY(20px)` + `opacity 0` → rest, `0.6s cubic-bezier(0.22, 1, 0.36, 1)`, staggered by `0.08s` across landing-name → role → tagline → location → icon-links. No bounces, no springs, no scroll-driven motion. Theme swaps ride a `0.2s ease` on background/color/border. Hover transitions are `0.15s`. Everything respects `prefers-reduced-motion`.

**Hover states.** Border and text swap to `--accent` (crimson). The icon-link's ring and glyph both crimson on hover. The PDF pill inverts to white on crimson fill. No scale, no lift, no shadow changes.

**Press states.** None defined in source. Browsers' native focus/active states apply.

**Focus states.** Default browser outline — intentionally not overridden.

**Protection gradients / capsules.** None. Everything sits on flat color.

**Transparency / blur.** None. The sticky header uses an opaque `--bg` with a faint shadow, not a backdrop-filter.

**Imagery.** One portrait slot, one size, one treatment — soft-cornered rectangle with warm color. No duotone, no b&w, no grain. The site doesn't ship generic imagery; designs derived from this system should stay imagery-light by default.

**Layout rules.** Landing is centered flex within `max-width: 900px`. Resume is two-column `1fr clamp(220px, 30%, 360px)` within `max-width: 1200px`. Sticky header is full-width wrapper with a 1200px max-width inner row. Mobile collapses both to single column at 767px.

**Cards.** There are no card components in the source. If you add one, follow the resume-sidebar precedent: warm stone background, no border, no shadow, hairline rule for internal division. Avoid drop shadows on content surfaces.

---

## Iconography

**System.** Inline SVG, 24×24 viewBox, `currentColor`, no icon font and no CDN library. All icons live in `assets/icons.svg` as `<symbol>` definitions, and are also exported as React components in `ui_kits/website/Icons.jsx`.

**Two styles, clear split.**
- **Brand icons** (mail, LinkedIn, GitHub, file) — solid fill, no stroke. Single `<path>`. 18×18 render size inside 38×38 circular frames.
- **UI icons** (moon, sun) — 2 px stroke, `fill: none`, `stroke-linecap: round`, `stroke-linejoin: round`. 17×17 render size.

This split is deliberate: brand marks read as glyphs, UI affordances read as line drawings. If you add icons, match the style of whichever half they belong to — don't mix strokes into the brand set or fills into the UI set.

**Emoji.** Not used in the web layer.

**Unicode as glyphs.** Two intentional uses — `›` (chevron) as bullet marker, `←` and `↓` in contact pill labels ("← Home", "↓ PDF"). Typography-native, not icons.

**Substitutions.** If you need an icon not in the set (e.g. Bluesky, Mastodon), match one that matches the solid-fill style — [Simple Icons](https://simpleicons.org/) is the closest aesthetic neighbor. Flag the addition so Tom can vet it.

---

## Caveats

- No real logo. The site uses the name "Tom Irish" set in Playfair Display 700 as its wordmark. The system doesn't ship a separate logomark.
- Portrait (`assets/images/tom-irish-{480,960}.png`) is Tom's real headshot at two resolutions plus a 128 px favicon. Replace if you have a preferred crop.
- Fonts are CDN-only (Google Fonts). No `.woff2` files are packaged.
- The PDF layer (`source/pdf.css`) is not part of the UI kit. It shares the palette and type choices but runs on a separate stylesheet with tighter scale.
