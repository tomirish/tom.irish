# Style Guide

Design system reference for the web layer (`index.template.html` + `assets/main.css`).
The PDF layer (`resume.template.html` + `assets/pdf.css`) is intentionally separate and is not covered here.

---

## Typography

### Typefaces

| Role | Family | Fallback |
|---|---|---|
| Display / headings | Playfair Display | Georgia, serif |
| Body / UI | DM Sans | -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |

Both loaded from Google Fonts via `index.template.html`:
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Playfair+Display:wght@400;700&display=swap"/>
```

### Type Scale

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Landing name | Playfair Display | 56px | 700 | ![](https://placehold.co/12x12/111111/111111.png) `#111` |
| Resume name (header) | Playfair Display | 30px | 700 | ![](https://placehold.co/12x12/111111/111111.png) `#111` |
| Section headings | Playfair Display | 18px | 700 | ![](https://placehold.co/12x12/9b2335/9b2335.png) `#9b2335` |
| Job title | DM Sans | 15px | 700 | ![](https://placehold.co/12x12/111111/111111.png) `#111` |
| Body text (summary, achievements, job bullets) | DM Sans | 15px | 400 | ![](https://placehold.co/12x12/333333/333333.png) `#333` |
| Job company | DM Sans | 13px | 400 | ![](https://placehold.co/12x12/555555/555555.png) `#555` |
| Job dates | DM Sans | 13px | 400 | ![](https://placehold.co/12x12/767676/767676.png) `#767676` |
| Landing role | DM Sans | 16px | 500 | ![](https://placehold.co/12x12/555555/555555.png) `#555` |
| Tagline | DM Sans | 15px | 400 | ![](https://placehold.co/12x12/666666/666666.png) `#666` |
| Education name | DM Sans | 14px | 600 | ![](https://placehold.co/12x12/111111/111111.png) `#111` |
| Education items | DM Sans | 13px | 400 | ![](https://placehold.co/12x12/555555/555555.png) `#555` |
| Certifications | DM Sans | 13px | 400 | ![](https://placehold.co/12x12/444444/444444.png) `#444` |
| Skill tags | DM Sans | 13px | 400 | ![](https://placehold.co/12x12/333333/333333.png) `#333` |
| Skill group labels | DM Sans | 11px | 600 | ![](https://placehold.co/12x12/666666/666666.png) `#666` |
| Contact pills | DM Sans | 12px | 400 | #444 |
| Landing location | DM Sans | 11px | 400 | #666 |

### Line Heights

| Context | Line Height |
|---|---|
| Summary / achievements / bullets | 1.6–1.7 |
| Body default | 1.5 |
| Landing name | 1.05 |

---

## Color

| Swatch | Hex | Name | Usage |
|:---:|---|---|---|
| ![](https://placehold.co/12x12/9b2335/9b2335.png) | `#9b2335` | Accent / crimson | Section headings, bullet markers, top borders, icon hover, PDF pill, landing separator |
| ![](https://placehold.co/12x12/111111/111111.png) | `#111` | Body text | Names, job titles, education names |
| ![](https://placehold.co/12x12/333333/333333.png) | `#333` | Primary text | Summary, bullets, skill tags |
| ![](https://placehold.co/12x12/444444/444444.png) | `#444` | Contact pill text | Default pill color |
| ![](https://placehold.co/12x12/555555/555555.png) | `#555` | Secondary text | Job company, landing role, education items |
| ![](https://placehold.co/12x12/666666/666666.png) | `#666` | Muted text | Tagline, landing location, skill group labels |
| ![](https://placehold.co/12x12/767676/767676.png) | `#767676` | Faint text | Job dates |
| `—` | `#fff` | Background | Page, skill tags, resume header |
| ![](https://placehold.co/12x12/edeae5/edeae5.png) | `#edeae5` | Sidebar background | Resume sidebar (warm, clearly distinct from main column) |
| ![](https://placehold.co/12x12/dedad5/dedad5.png) | `#dedad5` | Sidebar border | Divider between main column and sidebar |
| ![](https://placehold.co/12x12/e4e4e4/e4e4e4.png) | `#e4e4e4` | Section rule | Horizontal rule under section headings |
| ![](https://placehold.co/12x12/eeeeee/eeeeee.png) | `#eee` | Job rule | Separator between job entries |
| ![](https://placehold.co/12x12/e0e0e0/e0e0e0.png) | `#e0e0e0` | Border light | Contact pill borders |

---

## Layout

### Landing Page (`#home`)

- Full viewport height (`min-height: 100dvh`), centered flex column
- 4px crimson top border, white background
- **Horizontal layout** — photo left, text right, `gap: 56px`, `max-width: 780px`
- Photo: 210px circle, `box-shadow: 0 4px 24px rgba(0,0,0,0.13)` (no border ring)
- Text stack (`.landing-right`): name → role → tagline → location → separator → icon links
- Separator: `1px solid #9b2335` above icon links
- Safe area: `env(safe-area-inset-top/left/right)` included in padding so content clears the Dynamic Island in all orientations
- **Mobile (≤767px):** collapses to centered vertical stack; photo shrinks to 120px; name 44px; text center-aligned

### Resume View (`#resume`)

- Sticky header (full-width wrapper, max-width 1200px inner content)
  - `position: sticky; top: 0; z-index: 10`
  - 4px crimson top border, subtle `box-shadow: 0 2px 8px rgba(0,0,0,0.04)`
  - Safe area: `env(safe-area-inset-top/left/right)` on wrapper so header content clears Dynamic Island
  - Header photo: 52px circle, `box-shadow: 0 2px 8px rgba(0,0,0,0.10)`
- Two-column body: `1fr clamp(220px, 30%, 360px)` grid, max-width 1200px
  - Main column: `padding: 28px 32px`, `border-right: 1px solid #dedad5`
  - Sidebar: `padding: 28px 16px`, `background: #edeae5`
- Job entries separated by `border-top: 1px solid #eee` via `.job + .job`

### Section Toggle

Zero-JavaScript. Pure CSS `:target`:
```css
#resume { display: none; }
#resume:target { display: block; }
:root:has(#resume:target) #home { display: none; }
```

---

## Components

### Icon Links (landing)

38×38px circles, `1.5px solid #e0e0e0` border, 18×18px SVG icons.
- Default: `#555` icon, `#e0e0e0` border
- Hover: `#9b2335` icon, `#9b2335` border
- Primary (resume button): `#9b2335` fill, white icon

### Contact Pills (resume header)

`border-radius: 12px`, `1px solid #e0e0e0`, `4px 13px` padding.
- Default: `#444` text
- Hover: `#9b2335` text and border
- `← Home` pill: `font-weight: 500`
- `↓ PDF` pill: `#9b2335` text and border; hover inverts to white text on `#9b2335` fill

### Section Headings

Playfair Display, 18px, `#9b2335`. Followed by `1px solid #e4e4e4` rule.
First heading in each column has no top margin.

### Bullet Markers

En dash (`–`) positioned absolutely at `left: 0`, colored `#9b2335`. Used in: achievements, job bullets, certifications.

### Skill Tags

`border-radius: 10px`, `1px solid #e8e8e8`, white background, `4px 11px` padding, 13px.

---

## Responsive Breakpoints

| Breakpoint | Changes |
|---|---|
| `≤ 767px` | Landing stacks vertically (photo 120px, name 44px, text centered); resume header padding tightens; body switches to single column; sidebar loses background, gets top border |
| `≤ 479px` | Resume photo 56px; resume name 18px; icon links 34px |

---

## Fonts Note

DM Sans and Playfair Display are loaded from Google Fonts in both `index.template.html` and `resume.template.html`. The PDF uses the same typefaces as the web — Playwright has internet access during generation so Google Fonts load correctly.
