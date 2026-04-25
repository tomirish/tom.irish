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

### Full type scale

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

| ![](https://placehold.co/88x44/faf9f7/555555?text=Page) | ![](https://placehold.co/88x44/edeae5/555555?text=Sidebar) | ![](https://placehold.co/88x44/ffffff/555555?text=Tags) |
|:---:|:---:|:---:|
| `#faf9f7` bone | `#edeae5` stone | `#ffffff` white |

### Light / Dark

| ![](https://placehold.co/280x64/faf9f7/9b2335?text=Light+mode) | ![](https://placehold.co/280x64/131313/e0506a?text=Dark+mode) |
|:---:|:---:|
| Bone `#faf9f7` · crimson `#9b2335` | Near-black `#131313` · accent `#e0506a` |

Dark mode is triggered by `prefers-color-scheme: dark` or `html[data-theme="dark"]`. Photos lose their box-shadow and gain `box-shadow: 0 0 0 1px rgba(255,255,255,0.10)` — a subtle ring to lift them off the near-black background. Note that `--accent` and `--accent-text` are different values in dark mode — `--accent` is for fills and borders, `--accent-text` is the brighter value used for text.

### Light mode tokens

| Swatch | Hex | Variable | Usage |
|:---:|---|---|---|
| ![](https://placehold.co/12x12/9b2335/9b2335.png) | `#9b2335` | `--accent` | Section headings, bullets, top borders, icon hover, PDF pill, landing separator |
| ![](https://placehold.co/12x12/111111/111111.png) | `#111` | `--text-1` | Names, job titles, education names |
| ![](https://placehold.co/12x12/333333/333333.png) | `#333` | `--text-body` | Summary, bullets, skill tags |
| ![](https://placehold.co/12x12/555555/555555.png) | `#555` | `--text-2` | Job company, landing role, education items |
| ![](https://placehold.co/12x12/666666/666666.png) | `#666` | `--text-3` | Tagline, landing location, skill group labels |
| ![](https://placehold.co/12x12/767676/767676.png) | `#767676` | `--text-dates` | Job dates |
| ![](https://placehold.co/12x12/faf9f7/faf9f7.png) | `#faf9f7` | `--bg` | Page background — warm off-white |
| ![](https://placehold.co/12x12/edeae5/edeae5.png) | `#edeae5` | `--bg-sidebar` | Resume sidebar — warm stone |
| ![](https://placehold.co/12x12/dedad5/dedad5.png) | `#dedad5` | `--border-mid` | Divider between main column and sidebar |
| ![](https://placehold.co/12x12/eeeeee/eeeeee.png) | `#eee` | `--border-sm` | Section rules, job separators |
| ![](https://placehold.co/12x12/e0e0e0/e0e0e0.png) | `#e0e0e0` | `--border` | Contact pill borders, icon-link rings |

### Dark mode tokens

| Swatch | Variable | Value | Notes |
|:---:|---|---|---|
| ![](https://placehold.co/12x12/131313/131313.png) | `--bg` | `#131313` | Near-black page background |
| ![](https://placehold.co/12x12/1c1b1a/1c1b1a.png) | `--bg-sidebar` | `#1c1b1a` | Slightly warm dark sidebar |
| ![](https://placehold.co/12x12/222222/222222.png) | `--bg-skill` | `#222222` | Skill tag background |
| ![](https://placehold.co/12x12/c4394e/c4394e.png) | `--accent` | `#c4394e` | Brighter crimson for fills and borders |
| ![](https://placehold.co/12x12/e0506a/e0506a.png) | `--accent-text` | `#e0506a` | Even brighter — for text on dark backgrounds |
| ![](https://placehold.co/12x12/f0ece8/f0ece8.png) | `--text-1` | `#f0ece8` | Warm cream — names, titles |
| ![](https://placehold.co/12x12/cccccc/cccccc.png) | `--text-body` | `#ccc` | Body text |
| ![](https://placehold.co/12x12/aaaaaa/aaaaaa.png) | `--text-2` | `#aaa` | Secondary text |
| ![](https://placehold.co/12x12/888888/888888.png) | `--text-3` | `#888` | Muted text |
| ![](https://placehold.co/12x12/878787/878787.png) | `--text-dates` | `#878787` | Job dates |
| ![](https://placehold.co/12x12/484848/484848.png) | `--border` | `#484848` | |
| ![](https://placehold.co/12x12/363636/363636.png) | `--border-sm` | `#363636` | |
| ![](https://placehold.co/12x12/383634/383634.png) | `--border-mid` | `#383634` | |

---

## Shadows

Three tiers, all soft black — never colored. No inner shadows, no colored glows, no drop shadows on content surfaces.

| Usage | Value |
|---|---|
| Landing photo | `0 4px 24px rgba(0,0,0,0.13)` |
| Resume header photo | `0 2px 8px rgba(0,0,0,0.10)` |
| Sticky header | `0 2px 8px rgba(0,0,0,0.04)` |

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
