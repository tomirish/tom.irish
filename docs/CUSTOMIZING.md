# Style & Customization Guide

Design reference for the web layer (`index.template.html` + `assets/main.css`).
The PDF layer (`resume.template.html` + `assets/pdf.css`) shares the palette and typefaces but runs on a tighter scale — see [PDF layer](#pdf-layer) below.

---

## Design intent

The site is intentionally minimal: one crimson accent, a serif-sans pairing, a warm off-white canvas, and a quiet two-column resume view that feels like stationery. It signals reliability and empathy over flash — the design should mirror that.

> [!IMPORTANT]
> **Signature motifs — never break these**
>
> - **The 4px crimson stripe** — both views open with `border-top: 4px solid #9b2335`. It's the single strongest brand signal. Always flat, never gradient.
> - **The chevron bullet (`›`)** — achievements, job bullets, and certifications use `›` positioned absolutely at `left: 0`, colored crimson. Never `•`, never `–`, never checkmarks.

---

## Brand mark

The mark works on two levels: **Ti** are Tom Irish's initials, and Ti is the periodic table symbol for **Titanium — element 22**. Strong, lightweight, corrosion-resistant. One mark, two readings, no explanation required.

<table>
<tr valign="bottom">
  <td align="center" style="padding:12px 20px"><img src="../assets/images/ti-element.png" width="96" alt="Ti element mark"/><br/><br/><small>Master mark</small></td>
  <td align="center" style="padding:12px 20px"><img src="../assets/images/favicon.png" width="56" alt="Favicon light"/><br/><br/><small>Favicon · light</small></td>
  <td align="center" style="padding:12px 20px"><img src="../assets/images/favicon-dark.png" width="56" alt="Favicon dark"/><br/><br/><small>Favicon · dark</small></td>
  <td align="center" style="padding:12px 20px"><img src="../assets/images/apple-touch-icon.png" width="56" alt="Apple touch icon"/><br/><br/><small>Apple touch</small></td>
</tr>
</table>

**Files:**

| File | Size | Purpose |
|---|---|---|
| `assets/images/ti-element.png` | 1024×1024 | Master mark — periodic table element box |
| `assets/images/favicon.png` | 256×256 | Browser favicon, light mode |
| `assets/images/favicon-dark.png` | 256×256 | Browser favicon, dark mode (JS-swapped on load) |
| `assets/images/apple-touch-icon.png` | 1024×1024 | iOS home screen icon |

**Generation:** `scripts/generate_ti_element_icon.py` renders the master mark. `scripts/generate_favicons.py` renders the favicon pair (DM Serif Display "Ti" on solid background, via Playwright).

> [!NOTE]
> The favicon JS swap is in `index.template.html` — it reads `localStorage` on page load and sets `favicon.png` or `favicon-dark.png` based on the active theme. If you regenerate the favicons, re-run `convert_resume.py` to pick up the new files in the deployed `index.html`.

**Usage rules:**
- Don't rotate, skew, or recolor the mark
- The serif "Ti" is load-bearing — don't change the typeface
- Use crimson mark on light surfaces; dark variant on dark surfaces
- Don't pair with a second logo or icon — Ti/22 is the only mark

---

## Voice and tone

First-person, plain-spoken, quietly confident. No hype, no superlatives.

**Numbers over adjectives.** Achievements are stated as metrics ("99.5%+ availability", "$465K savings, a 38.4% reduction") — not adjectives ("significant", "major").

**Casing.** Sentence case for section headings ("Key Achievements"). Title case for job titles ("Senior Manager"). All-caps only on micro-labels (`.landing-location`, `.skill-group-label`) with generous letter-spacing.

**Pronouns.** "My" and "I" in the professional summary. Bullet points use implicit subject with present-tense verbs for current roles, past-tense for historical ones ("Own the global connectivity platform…").

**No emoji** in the web or PDF layer.

---

## Typography

Playfair Display 700 for every name and section heading — nothing else. DM Sans covers all body, UI, labels, and metadata. DM Serif Display is self-hosted but only used in generated icons, not the web layer.

### Typefaces

| Role | Family | Weight | Notes |
|---|---|---|---|
| Display / headings | Playfair Display | 700 | Names and section headings only |
| Body / UI | DM Sans | 400–600 | Everything operational |
| Icons / favicon | DM Serif Display | 400 | Used by generation scripts only — not in the web layer |

All three are self-hosted in `assets/fonts/` — no external network dependency.

### Type specimen

<table width="100%">
<tr>
<td style="padding:16px 20px;border-bottom:1px solid #eeeeee">
<div style="font-size:11px;color:#9b2335;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Display · Playfair Display 700</div>
<div style="font-size:36px;font-weight:700;color:#111111;line-height:1.05;letter-spacing:-1px">Tom Irish</div>
<div style="font-size:10px;color:#888888;font-family:monospace;margin-top:6px">56px · −2px tracking · line-height 1.05</div>
</td>
</tr>
<tr>
<td style="padding:16px 20px">
<div style="font-size:11px;color:#9b2335;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px">Body scale · DM Sans</div>
<table width="100%">
<tr><td style="padding:4px 0;font-size:17px;color:#333333;line-height:1.5">Engineering leader building the systems that keep global freight moving.</td><td align="right" style="padding-left:16px;font-size:10px;color:#888888;white-space:nowrap;vertical-align:bottom">tagline · 17 / 400</td></tr>
<tr><td style="padding:4px 0;font-size:16px;color:#555555;font-weight:500">Senior Manager, Expeditors</td><td align="right" style="padding-left:16px;font-size:10px;color:#888888;white-space:nowrap;vertical-align:bottom">role · 16 / 500</td></tr>
<tr><td style="padding:4px 0;font-size:15px;color:#333333">Senior engineering leader with 21 years in global logistics.</td><td align="right" style="padding-left:16px;font-size:10px;color:#888888;white-space:nowrap;vertical-align:bottom">body · 15 / 400</td></tr>
<tr><td style="padding:4px 0;font-size:15px;color:#111111;font-weight:700">Expeditors — Senior Manager</td><td align="right" style="padding-left:16px;font-size:10px;color:#888888;white-space:nowrap;vertical-align:bottom">title · 15 / 700</td></tr>
<tr><td style="padding:4px 0;font-size:13px;color:#555555">2003 – Present</td><td align="right" style="padding-left:16px;font-size:10px;color:#888888;white-space:nowrap;vertical-align:bottom">meta · 13 / 400</td></tr>
<tr><td style="padding:4px 0;font-size:11px;color:#666666;font-weight:600;text-transform:uppercase;letter-spacing:1px">Seattle, Washington</td><td align="right" style="padding-left:16px;font-size:10px;color:#888888;white-space:nowrap;vertical-align:bottom">label · 11 / 600 · caps</td></tr>
</table>
</td>
</tr>
</table>

> Light-mode colors only — dark mode swaps are in the token tables below.

### Full type scale

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Landing name | Playfair Display | 56px | 700 | ![](https://placehold.co/16x16/111111/111111.png) `#111` |
| Resume name (header) | Playfair Display | 22px | 700 | ![](https://placehold.co/16x16/111111/111111.png) `#111` |
| Section headings | Playfair Display | 18px | 700 | ![](https://placehold.co/16x16/9b2335/9b2335.png) `#9b2335` |
| Job title | DM Sans | 15px | 700 | ![](https://placehold.co/16x16/111111/111111.png) `#111` |
| Body text (summary, achievements, bullets) | DM Sans | 15px | 400 | ![](https://placehold.co/16x16/333333/333333.png) `#333` |
| Landing tagline | DM Sans | 17px | 400 | ![](https://placehold.co/16x16/333333/333333.png) `#333` |
| Landing role | DM Sans | 16px | 500 | ![](https://placehold.co/16x16/555555/555555.png) `#555` |
| Job company | DM Sans | 13px | 400 | ![](https://placehold.co/16x16/555555/555555.png) `#555` |
| Job dates | DM Sans | 13px | 400 | ![](https://placehold.co/16x16/767676/767676.png) `#767676` |
| Education name | DM Sans | 14px | 600 | ![](https://placehold.co/16x16/111111/111111.png) `#111` |
| Education items | DM Sans | 13px | 400 | ![](https://placehold.co/16x16/555555/555555.png) `#555` |
| Certifications | DM Sans | 13px | 400 | ![](https://placehold.co/16x16/333333/333333.png) `#333` |
| Skill tags | DM Sans | 13px | 400 | ![](https://placehold.co/16x16/333333/333333.png) `#333` |
| Skill group labels | DM Sans | 11px | 600 | ![](https://placehold.co/16x16/666666/666666.png) `#666` |
| Contact pills | DM Sans | 12px | 400 | ![](https://placehold.co/16x16/333333/333333.png) `#333` |
| Landing location | DM Sans | 11px | 400 | ![](https://placehold.co/16x16/666666/666666.png) `#666` |

### Line heights

| Context | Line height |
|---|---|
| Summary / achievements / bullets | 1.6–1.7 |
| Body default | 1.5 |
| Landing name | 1.05 |

---

## Color

One accent, warm neutrals. No gradients, no second accent, no semantic colors.

### Foreground

| ![](https://placehold.co/72x44/111111/ffffff?text=Aa) | ![](https://placehold.co/72x44/333333/ffffff?text=Aa) | ![](https://placehold.co/72x44/555555/ffffff?text=Aa) | ![](https://placehold.co/72x44/666666/ffffff?text=Aa) | ![](https://placehold.co/72x44/767676/ffffff?text=Aa) | ![](https://placehold.co/72x44/9b2335/ffffff?text=Aa) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| `#111` ink | `#333` body | `#555` secondary | `#666` muted | `#767676` dates | `#9b2335` accent |

### Surfaces

| ![](https://placehold.co/88x44/faf9f7/555555?text=Page) | ![](https://placehold.co/88x44/edeae5/555555?text=Sidebar) | ![](https://placehold.co/88x44/ffffff/555555?text=Tags) | ![](https://placehold.co/88x44/dedad5/555555?text=Divider) | ![](https://placehold.co/88x44/eeeeee/555555?text=Rule) | ![](https://placehold.co/88x44/e0e0e0/555555?text=Border) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| `#faf9f7` bone | `#edeae5` stone | `#ffffff` white | `#dedad5` divider | `#eee` rule | `#e0e0e0` border |

### Light / Dark

| ![](https://placehold.co/280x64/faf9f7/9b2335?text=Light+mode) | ![](https://placehold.co/280x64/131313/e0506a?text=Dark+mode) |
|:---:|:---:|
| Bone ![](https://placehold.co/16x16/faf9f7/faf9f7.png) `#faf9f7` · crimson ![](https://placehold.co/16x16/9b2335/9b2335.png) `#9b2335` | Near-black ![](https://placehold.co/16x16/131313/131313.png) `#131313` · accent ![](https://placehold.co/16x16/e0506a/e0506a.png) `#e0506a` |

Dark mode is triggered by `prefers-color-scheme: dark` or `html[data-theme="dark"]`. Photos lose their box-shadow and gain `box-shadow: 0 0 0 1px rgba(255,255,255,0.10)` — a subtle ring to lift them off the near-black background. Note that `--accent` and `--accent-text` are different values in dark mode — `--accent` is for fills and borders, `--accent-text` is the brighter value used for text.

### Light mode tokens

| Hex | Variable | Usage |
|---|---|---|
| <img src="https://placehold.co/24x24/9b2335/9b2335.png" style="border:1px solid white"/> `#9b2335` | `--accent` | Section headings, bullets, top borders, icon hover, PDF pill, landing separator |
| <img src="https://placehold.co/24x24/111111/111111.png" style="border:1px solid white"/> `#111` | `--text-1` | Names, job titles, education names |
| <img src="https://placehold.co/24x24/333333/333333.png" style="border:1px solid white"/> `#333` | `--text-body` | Summary, bullets, skill tags |
| <img src="https://placehold.co/24x24/555555/555555.png" style="border:1px solid white"/> `#555` | `--text-2` | Job company, landing role, education items |
| <img src="https://placehold.co/24x24/666666/666666.png" style="border:1px solid white"/> `#666` | `--text-3` | Tagline, landing location, skill group labels |
| <img src="https://placehold.co/24x24/767676/767676.png" style="border:1px solid white"/> `#767676` | `--text-dates` | Job dates |
| <img src="https://placehold.co/24x24/faf9f7/faf9f7.png" style="border:1px solid white"/> `#faf9f7` | `--bg` | Page background — warm off-white |
| <img src="https://placehold.co/24x24/edeae5/edeae5.png" style="border:1px solid white"/> `#edeae5` | `--bg-sidebar` | Resume sidebar — warm stone |
| <img src="https://placehold.co/24x24/dedad5/dedad5.png" style="border:1px solid white"/> `#dedad5` | `--border-mid` | Divider between main column and sidebar |
| <img src="https://placehold.co/24x24/eeeeee/eeeeee.png" style="border:1px solid white"/> `#eee` | `--border-sm` | Section rules, job separators |
| <img src="https://placehold.co/24x24/e0e0e0/e0e0e0.png" style="border:1px solid white"/> `#e0e0e0` | `--border` | Contact pill borders, icon-link rings |

### Dark mode tokens

| Hex | Variable | Usage |
|---|---|---|
| <img src="https://placehold.co/24x24/131313/131313.png" style="border:1px solid white"/> `#131313` | `--bg` | Near-black page background |
| <img src="https://placehold.co/24x24/1c1b1a/1c1b1a.png" style="border:1px solid white"/> `#1c1b1a` | `--bg-sidebar` | Slightly warm dark sidebar |
| <img src="https://placehold.co/24x24/222222/222222.png" style="border:1px solid white"/> `#222222` | `--bg-skill` | Skill tag background |
| <img src="https://placehold.co/24x24/c4394e/c4394e.png" style="border:1px solid white"/> `#c4394e` | `--accent` | Brighter crimson for fills and borders |
| <img src="https://placehold.co/24x24/e0506a/e0506a.png" style="border:1px solid white"/> `#e0506a` | `--accent-text` | Even brighter — for text on dark backgrounds |
| <img src="https://placehold.co/24x24/f0ece8/f0ece8.png" style="border:1px solid white"/> `#f0ece8` | `--text-1` | Warm cream — names, titles |
| <img src="https://placehold.co/24x24/cccccc/cccccc.png" style="border:1px solid white"/> `#ccc` | `--text-body` | Body text |
| <img src="https://placehold.co/24x24/aaaaaa/aaaaaa.png" style="border:1px solid white"/> `#aaa` | `--text-2` | Secondary text |
| <img src="https://placehold.co/24x24/888888/888888.png" style="border:1px solid white"/> `#888` | `--text-3` | Muted text |
| <img src="https://placehold.co/24x24/878787/878787.png" style="border:1px solid white"/> `#878787` | `--text-dates` | Job dates |
| <img src="https://placehold.co/24x24/484848/484848.png" style="border:1px solid white"/> `#484848` | `--border` | |
| <img src="https://placehold.co/24x24/363636/363636.png" style="border:1px solid white"/> `#363636` | `--border-sm` | |
| <img src="https://placehold.co/24x24/383634/383634.png" style="border:1px solid white"/> `#383634` | `--border-mid` | |

---

## Shadows

Three tiers, all soft black — never colored. No inner shadows, no colored glows, no drop shadows on content surfaces.

<table width="100%"><tr valign="bottom">
<td align="center" style="padding:28px 16px">
  <div style="width:80px;height:80px;border-radius:40px;background:#faf9f7;box-shadow:0 4px 24px rgba(0,0,0,0.13);border:1px solid #f0eeeb;margin:0 auto"></div>
  <div style="margin-top:14px;font-size:12px;font-weight:600;color:#333">Landing photo</div>
  <div style="margin-top:3px;font-size:11px;color:#999;font-family:monospace">0 4px 24px rgba(0,0,0,0.13)</div>
</td>
<td align="center" style="padding:28px 16px">
  <div style="width:56px;height:56px;border-radius:28px;background:#faf9f7;box-shadow:0 2px 8px rgba(0,0,0,0.10);border:1px solid #f0eeeb;margin:0 auto"></div>
  <div style="margin-top:14px;font-size:12px;font-weight:600;color:#333">Resume photo</div>
  <div style="margin-top:3px;font-size:11px;color:#999;font-family:monospace">0 2px 8px rgba(0,0,0,0.10)</div>
</td>
<td align="center" style="padding:28px 16px">
  <div style="box-shadow:0 2px 8px rgba(0,0,0,0.04);border:1px solid #f0eeeb">
    <div style="height:3px;background:#9b2335"></div>
    <div style="padding:10px 16px;font-size:12px;color:#555;background:#faf9f7">Tom Irish &nbsp;&nbsp;&nbsp; ← Home &nbsp; ↓ PDF</div>
  </div>
  <div style="margin-top:14px;font-size:12px;font-weight:600;color:#333">Sticky header</div>
  <div style="margin-top:3px;font-size:11px;color:#999;font-family:monospace">0 2px 8px rgba(0,0,0,0.04)</div>
</td>
</tr></table>

---

## Animation

A single entrance motion on the landing page. No scroll-driven motion, no bounces. Always respects `prefers-reduced-motion`.

The photo uses transform-only (`slide-up`) to stay eligible as an LCP candidate — starting at `opacity: 0` would disqualify it. Text elements use the full fade+translate (`fade-up`):

| Property | Photo (`slide-up`) | Text elements (`fade-up`) |
|---|---|---|
| Motion | `translateY(20px)` → rest | `translateY(20px)` + `opacity: 0` → rest |
| Duration | `0.7s` | `0.6s` |
| Easing | `cubic-bezier(0.22, 1, 0.36, 1)` | `cubic-bezier(0.22, 1, 0.36, 1)` |
| Delay | `0s` | `0.08s` stagger: name → role → tagline → location → icon links |

Other transitions: theme swap `0.2s ease` on background / color / border; hover `0.15s`.

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

## Spacing

Key dimensions used across both views.

### Landing

| Property | Value | Notes |
|---|---|---|
| Max width | 900px | Flex container |
| Photo diameter | 240px | 140px on mobile (≤767px) |
| Photo border-radius | 20px | |
| Photo / text gap | 56px | |
| Name size | 56px | 44px on mobile |

### Resume

| Property | Value | Notes |
|---|---|---|
| Max width | 1200px | Header and body container |
| Sidebar width | `clamp(220px, 30%, 360px)` | |
| Main column padding | `28px 32px` | |
| Sidebar padding | `28px 16px` | |

### Components

| Element | Value | Notes |
|---|---|---|
| Icon link circle | 38×38px | 34×34px on mobile (≤470px) |
| Icon SVG | 18×18px | |
| Contact pill border-radius | 12px | |
| Contact pill padding | `4px 13px` | |
| Skill tag border-radius | 10px | |
| Skill tag padding | `4px 11px` | |

---

## Components

<table width="100%" style="border:1px solid #eee;border-collapse:collapse">
<tr><td style="padding:20px 24px;border-bottom:1px solid #eee">
  <div style="font-family:Georgia,serif;font-size:18px;font-weight:700;color:#9b2335">Work Experience</div>
  <div style="height:1px;background:#e4e4e4;margin:5px 0 12px"></div>
  <div style="font-size:14px;color:#333;margin-bottom:6px"><span style="color:#9b2335">›</span>&nbsp;Achieved 99.5% platform availability across 12 global regions.</div>
  <div style="font-size:14px;color:#333"><span style="color:#9b2335">›</span>&nbsp;Reduced infrastructure cost by $465K, a 38.4% reduction year over year.</div>
</td></tr>
<tr><td style="padding:16px 24px">
  <span style="border:1px solid #e0e0e0;border-radius:12px;padding:4px 13px;font-size:12px;color:#333">← Home</span>
  &ensp;
  <span style="border:1px solid #9b2335;border-radius:12px;padding:4px 13px;font-size:12px;color:#9b2335">↓ PDF</span>
  &emsp;
  <span style="border:1px solid #eee;border-radius:10px;padding:4px 11px;font-size:13px;color:#333">Python</span>&thinsp;<span style="border:1px solid #eee;border-radius:10px;padding:4px 11px;font-size:13px;color:#333">Kubernetes</span>&thinsp;<span style="border:1px solid #eee;border-radius:10px;padding:4px 11px;font-size:13px;color:#333">Terraform</span>
</td></tr>
</table>

### Icon Links (landing)

38×38px circles, `1.5px solid #e0e0e0`, 18×18px SVG icons.
- Default: ![](https://placehold.co/16x16/555555/555555.png) `#555` icon, ![](https://placehold.co/16x16/e0e0e0/e0e0e0.png) `#e0e0e0` border
- Hover: ![](https://placehold.co/16x16/9b2335/9b2335.png) `#9b2335` icon and border
- Primary (resume button): ![](https://placehold.co/16x16/9b2335/9b2335.png) `#9b2335` fill, white icon, pill shape

### Contact Pills (resume header)

`border-radius: 12px`, `1px solid #e0e0e0`, `4px 13px` padding.
- Default: ![](https://placehold.co/16x16/333333/333333.png) `#333` text
- Hover: ![](https://placehold.co/16x16/9b2335/9b2335.png) `#9b2335` text and border
- `← Home` pill: `font-weight: 500`
- `↓ PDF` pill: crimson text and border; hover inverts to white text on crimson fill

### Section Headings

Playfair Display, 18px, ![](https://placehold.co/16x16/9b2335/9b2335.png) `#9b2335`. Followed by `1px solid #e4e4e4` rule. First heading in each column has no top margin.

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

---

## Accessibility

### Contrast

The palette targets WCAG AA (4.5:1 for normal text, 3:1 for large text). `#767676` on `#faf9f7` is the minimum-contrast pairing in the design — used only for job dates. If you lighten the page background or darken dates further, verify the new pair with a contrast checker. All other foreground/background combinations exceed AA.

In dark mode, `--accent-text` (![](https://placehold.co/16x16/e0506a/e0506a.png) `#e0506a`) is used for text specifically because `--accent` (![](https://placehold.co/16x16/c4394e/c4394e.png) `#c4394e`) doesn't meet AA contrast on the dark background — don't swap them.

### Focus

All interactive elements rely on the browser default `:focus-visible` ring. Don't suppress `outline` without providing a visible custom replacement.

### Motion

All entrance animations respect `prefers-reduced-motion: reduce` — see [Animation](#animation).

---

## PDF layer

The PDF is rendered by headless Chromium from `resume.template.html` + `assets/pdf.css`. It shares the palette and typefaces with the web layer but runs on a tighter scale. Fonts are self-hosted (woff2 files in `assets/fonts/`) — no network dependency at render time.

### Page setup

| Property | Value |
|---|---|
| Format | US Letter (8.5 × 11 in) |
| Margins | 0.2 in on all sides |
| Scale | 0.98 |
| Render | Headless Chromium via Playwright |

To adjust margins or scale, edit the constants at the top of `scripts/generate_pdf_browser.py`:

```python
PDF_FORMAT = 'Letter'
PDF_MARGIN_TOP = '0.2in'
PDF_MARGIN_RIGHT = '0.2in'
PDF_MARGIN_BOTTOM = '0.2in'
PDF_MARGIN_LEFT = '0.2in'
PDF_SCALE = 0.98
```

If your content overflows to a second page, reduce `PDF_SCALE` (e.g. `0.95`) or tighten margins before editing content.

### Type scale (PDF)

The PDF uses smaller sizes than the web layer to fit a single page.

| Element | Size | Weight |
|---|---|---|
| Name | 22px | 700 |
| Section headings | 13px | 700 |
| Job title | 12px | 700 |
| Body (summary, bullets) | 10.5px | 400 |
| Job company / education items | 10px | 400 |
| Job dates | 10px | 400 |
| Contact line | 10px | 400 |

### CSS classes

| Class | Role |
|---|---|
| `.pdf-header` | Name + contact row, 3px crimson top border |
| `.pdf-name` | Playfair Display, 22px |
| `.pdf-contact` | Flex row of contact fields |
| `.pdf-section` | Wrapper for each resume section |
| `.pdf-section-heading` | Playfair Display, 13px, crimson |
| `.pdf-rule` | 1px rule under section headings |
| `.pdf-job` | Single job entry, `page-break-inside: avoid` |
| `.pdf-job-header` | Flex row: title left, dates right |
| `.pdf-job-title` | 12px, bold |
| `.pdf-job-company` | 10px, `#555` |
| `.pdf-job-dates` | 10px, `#767676` |
| `.pdf-bullets` | `›` bullet list (achievements, job bullets, certifications) |
| `.pdf-skill-row` | One skill group or flat skill |
| `.pdf-skill-label` | Category label, bold |
| `.pdf-edu` | One school entry |
| `.pdf-edu-item` | Degree line, `#555` |

### Template

`resume.template.html` is a Jinja2 template. The build script populates these variables from `resume.md`:

| Variable | Content |
|---|---|
| `{{ name }}` | Name from the `#` heading |
| `{{ email }}`, `{{ phone }}`, `{{ location }}`, `{{ linkedin }}` | Header contact fields |
| `{{ summary }}` | List of paragraphs |
| `{{ achievements }}` | List of bullet strings |
| `{{ work_experience }}` | List of `{role, company, dates, bullets}` objects |
| `{{ skills }}` | List of `{type, label, items}` objects |
| `{{ education }}` | List of `{name, items}` objects |
| `{{ certifications }}` | List of bullet strings |
