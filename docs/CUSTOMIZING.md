# Style Guide

Design reference for the web layer (`index.template.html` + `assets/main.css`).
The PDF layer (`resume.template.html` + `assets/pdf.css`) shares the palette and typefaces but runs on a tighter scale and is not fully covered here.

---

## Design intent

The site is intentionally minimal: one crimson accent, a serif-sans pairing, a warm off-white canvas, and a quiet two-column resume view that feels like stationery. It signals reliability and empathy over flash — the design should mirror that.

**Signature motifs to never break:**
- **The 4px crimson stripe** — both views open with `border-top: 4px solid #9b2335`. It's the single strongest brand signal. Always flat, never gradient.
- **The chevron bullet (`›`)** — achievements, job bullets, and certifications all use `›` positioned absolutely at `left: 0`, colored crimson. Never `•`, never `–`, never checkmarks.

---

## Voice and tone

**Numbers over adjectives.** Achievements are stated as metrics ("99.5%+ availability", "$465K savings, a 38.4% reduction"), not adjectives ("significant", "major").

**Casing.** Sentence case for section headings ("Key Achievements"). Title case for job titles ("Senior Manager"). All-caps only on micro-labels (`.landing-location`, `.skill-group-label`) with generous letter-spacing.

**Pronouns.** "My" and "I" in the professional summary. Bullet points use implicit subject with present-tense verbs for current roles, past-tense for historical ones ("Own the global connectivity platform…").

**No emoji** in the web or PDF layer.

---

## Typography

### Typefaces

| Role | Family | Fallback |
|---|---|---|
| Display / headings | Playfair Display | Georgia, serif |
| Body / UI | DM Sans | -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |

Both loaded from Google Fonts via `index.template.html`:
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Playfair Display:wght@400;700&display=swap"/>
```

Playfair Display 700 is used for names and section headings only — nothing else. DM Sans covers all body, UI, labels, and metadata.

### Type Scale

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Landing name | Playfair Display | 56px | 700 | `#111` |
| Resume name (header) | Playfair Display | 22px | 700 | `#111` |
| Section headings | Playfair Display | 18px | 700 | `#9b2335` |
| Job title | DM Sans | 15px | 700 | `#111` |
| Body text (summary, achievements, bullets) | DM Sans | 15px | 400 | `#333` |
| Landing tagline | DM Sans | 17px | 400 | `#333` |
| Landing role | DM Sans | 16px | 500 | `#555` |
| Job company | DM Sans | 13px | 400 | `#555` |
| Job dates | DM Sans | 13px | 400 | `#767676` |
| Education name | DM Sans | 14px | 600 | `#111` |
| Education items | DM Sans | 13px | 400 | `#555` |
| Certifications | DM Sans | 13px | 400 | `#333` |
| Skill tags | DM Sans | 13px | 400 | `#333` |
| Skill group labels | DM Sans | 11px | 600 | `#666` |
| Contact pills | DM Sans | 12px | 400 | `#333` |
| Landing location | DM Sans | 11px | 400 | `#666` |

### Line Heights

| Context | Line Height |
|---|---|
| Summary / achievements / bullets | 1.6–1.7 |
| Body default | 1.5 |
| Landing name | 1.05 |

---

## Color

### Light mode

| Swatch | Hex | Name | Usage |
|:---:|---|---|---|
| ![](https://placehold.co/12x12/9b2335/9b2335.png) | `#9b2335` | Accent / crimson | Section headings, bullets, top borders, icon hover, PDF pill, landing separator |
| ![](https://placehold.co/12x12/111111/111111.png) | `#111` | Ink | Names, job titles, education names |
| ![](https://placehold.co/12x12/333333/333333.png) | `#333` | Body text | Summary, bullets, skill tags |
| ![](https://placehold.co/12x12/444444/444444.png) | `#444` | Contact pill text | Default pill color |
| ![](https://placehold.co/12x12/555555/555555.png) | `#555` | Secondary text | Job company, landing role, education items |
| ![](https://placehold.co/12x12/666666/666666.png) | `#666` | Muted | Tagline, landing location, skill group labels |
| ![](https://placehold.co/12x12/767676/767676.png) | `#767676` | Faint | Job dates |
| ![](https://placehold.co/12x12/faf9f7/faf9f7.png) | `#faf9f7` | Page background | Warm off-white |
| ![](https://placehold.co/12x12/edeae5/edeae5.png) | `#edeae5` | Sidebar background | Warm stone — clearly distinct from main column |
| ![](https://placehold.co/12x12/dedad5/dedad5.png) | `#dedad5` | Sidebar border | Divider between main and sidebar |
| ![](https://placehold.co/12x12/e4e4e4/e4e4e4.png) | `#e4e4e4` | Section rule | Horizontal rule under section headings |
| ![](https://placehold.co/12x12/eeeeee/eeeeee.png) | `#eee` | Job rule | Separator between job entries |
| ![](https://placehold.co/12x12/e0e0e0/e0e0e0.png) | `#e0e0e0` | Border light | Contact pill borders, icon-link rings |

### Dark mode

Triggered by `prefers-color-scheme: dark` or `html[data-theme="dark"]`.

| Swatch | Variable | Value | Notes |
|:---:|---|---|---|
| ![](https://placehold.co/12x12/131313/131313.png) | `--bg` | `#131313` | Near-black |
| ![](https://placehold.co/12x12/1c1b1a/1c1b1a.png) | `--bg-sidebar` | `#1c1b1a` | Slightly warm |
| ![](https://placehold.co/12x12/c4394e/c4394e.png) | `--accent` | `#c4394e` | Brighter crimson for contrast |
| ![](https://placehold.co/12x12/e0506a/e0506a.png) | `--accent-text` | `#e0506a` | Even brighter for text readability |
| ![](https://placehold.co/12x12/f0ece8/f0ece8.png) | `--text-1` | `#f0ece8` | Warm cream |
| ![](https://placehold.co/12x12/cccccc/cccccc.png) | `--text-body` | `#ccc` | |
| ![](https://placehold.co/12x12/484848/484848.png) | `--border` | `#484848` | |
| ![](https://placehold.co/12x12/363636/363636.png) | `--border-sm` | `#363636` | |

Photos lose the box-shadow and get `box-shadow: 0 0 0 1px rgba(255,255,255,0.10)` instead — a subtle ring to separate them from the dark background.

---

## Shadows

Three tiers, all soft black — never colored:

| Usage | Value |
|---|---|
| Landing photo | `0 4px 24px rgba(0,0,0,0.13)` |
| Resume header photo | `0 2px 8px rgba(0,0,0,0.10)` |
| Sticky header | `0 2px 8px rgba(0,0,0,0.04)` |

No inner shadows, no colored glows, no drop shadows on content surfaces.

---

## Animation

A single entrance motion — `fade-up`: `translateY(20px)` + `opacity: 0` → rest, `0.6s cubic-bezier(0.22, 1, 0.36, 1)`, staggered `0.08s` across photo → name → role → tagline → location → icon links. No bounces, no scroll-driven motion. Theme swaps use `0.2s ease` on background/color/border. Hover transitions are `0.15s`. Always respects `prefers-reduced-motion`.

---

## Layout

### Landing Page (`#home`)

- Full viewport height (`min-height: 100dvh`), centered flex column
- 4px crimson top border
- Horizontal layout — photo left, text right, `gap: 56px`, `max-width: 900px`
- Photo: 240px, `border-radius: 20px`, large shadow
- Text stack: name → role → tagline → location → crimson separator → icon links
- Safe area padding: `env(safe-area-inset-*)` so content clears the Dynamic Island
- **Mobile (≤767px):** collapses to centered vertical stack; photo 140px; name 44px; text center-aligned

### Resume View (`#resume`)

- Sticky header: full-width, `max-width: 1200px` inner, 4px crimson top border, faint shadow
- Two-column body: `1fr clamp(220px, 30%, 360px)` grid, `max-width: 1200px`
  - Main column: `padding: 28px 32px`, `border-right: 1px solid #dedad5`
  - Sidebar: `padding: 28px 16px`, `background: #edeae5`
- Job entries separated by `border-top: 1px solid #eee`

### Section Toggle

Zero JavaScript — pure CSS `:target`:
```css
#resume { display: none; }
#resume:target { display: block; }
:root:has(#resume:target) #home { display: none; }
```

---

## Components

### Icon Links (landing)

38×38px circles, `1.5px solid #e0e0e0`, 18×18px SVG icons.
- Default: `#555` icon, `#e0e0e0` border
- Hover: `#9b2335` icon and border
- Primary (resume button): `#9b2335` fill, white icon, pill shape

### Contact Pills (resume header)

`border-radius: 12px`, `1px solid #e0e0e0`, `4px 13px` padding.
- Default: `#333` text
- Hover: `#9b2335` text and border
- `← Home` pill: `font-weight: 500`
- `↓ PDF` pill: crimson text and border; hover inverts to white text on crimson fill

### Section Headings

Playfair Display, 18px, `#9b2335`. Followed by `1px solid #e4e4e4` rule. First heading in each column has no top margin.

### Bullet Markers

`›` positioned absolutely at `left: 0`, colored `#9b2335`. Used in achievements, job bullets, and certifications.

### Skill Tags

`border-radius: 10px`, `1px solid #eee`, white background, `4px 11px` padding, 13px.

---

## Iconography

Inline SVG, 24×24 viewBox, `currentColor`. No icon font, no CDN library.

**Two styles — keep them separate:**
- **Brand icons** (mail, LinkedIn, GitHub, file) — solid fill, no stroke. 18×18 inside 38×38 circular frames.
- **UI icons** (moon, sun) — 2px stroke, `fill: none`, round caps and joins. 17×17.

Brand marks read as glyphs; UI affordances read as line drawings. Don't mix strokes into the brand set or fills into the UI set.

**Unicode glyphs in use:** `›` as bullet marker, `←` and `↓` in contact pill labels.

If adding a new brand icon, [Simple Icons](https://simpleicons.org/) matches the solid-fill aesthetic.

---

## Responsive Breakpoints

| Breakpoint | Changes |
|---|---|
| `≤ 767px` | Landing stacks vertically (photo 140px, name 44px, text centered); resume body switches to single column; sidebar loses background, gets top border |
| `≤ 470px` | Resume photo hidden; resume name 18px; icon links 34px; contact pill padding tightens |
