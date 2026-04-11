# Frontend Rewrite Design Spec
**Date:** 2026-04-11  
**Branch:** `frontend-rewrite`  
**Status:** Approved

---

## Overview

Replace the Carrd-generated `main.js` (68KB) and `main.css` (54KB) with clean, hand-written code. The result should be a fast, minimal, professional personal site that works on every screen and browser, with `resume.md` remaining the single source of truth for all content.

---

## Goals

- Zero JavaScript — CSS-only section toggling via `:target`
- No external resources — system font stack, no Google Fonts, no CDN dependencies
- Fully responsive — mobile, tablet, desktop, large monitors; iOS, Android, any browser
- Consistent design across HTML (web) and PDF (print) — no jarring contrast between sections
- Markdown-as-CMS — `resume.md` stays the single source of truth; editing it updates both the website and the PDF
- Clean, readable `resume.md` — format is obvious to edit without special knowledge

---

## Design Decisions

### Colors
- **Background:** `#ffffff` (pure white)
- **Primary text:** `#111111`
- **Secondary text / metadata:** `#888888`
- **Border / divider:** `#eeeeee`
- **Accent:** `#9b2335` (deep crimson — pulled from photo tie, used for top border, section headings, bullet markers, resume button)
- **Sidebar background:** `#fafafa`
- **Skill tag background:** `#f5f5f5`

### Typography
- **Font stack:** `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- No Google Fonts, no web font requests
- Weights: 400 (body), 600 (subheadings), 700 (name, section titles)

### Layout — Landing Section
- Full-viewport centered card
- Circular photo (96px), border `#eeeeee`
- Name: 24px, weight 700, letter-spacing -0.4px
- Location: 11px, uppercase, letter-spacing 0.8px, color `#999`
- Icon link row: 5 circle buttons (38px) — Email, Phone, LinkedIn, GitHub, Resume
  - Default: border `#e0e0e0`, icon color `#555`
  - Hover: border and icon color `#9b2335`
  - Resume button: filled `#9b2335`, white icon
- 4px crimson top border on the page

### Layout — Resume Section
- 4px crimson top border (consistent with landing)
- Nav bar: "← Back" link (crimson) + "↓ PDF Resume" pill button
- Header: circular photo (72px) + name (22px 700) + contact pills
- Two-column body:
  - **Main column** (~65%): Professional Summary → Key Achievements → Work Experience
  - **Sidebar** (~35%, `#fafafa` background): Technical Skills → Education → Certifications
- Section headings: 10px, uppercase, letter-spacing 1.4px, color `#9b2335`
- Thin `#eeeeee` rule under each section heading
- Job entries: Title (bold) + Company + date range right-aligned, then bullets
- Bullet markers: crimson `–` dash
- Skill tags: grouped by category, pill style on white background
- On mobile (< 768px): collapses to single column, sidebar moves below main

### Section Toggle
- CSS `:target` selector — `#home` and `#resume` anchor targets
- Landing section (`id="home"`) is visible by default (no `:target` match needed); resume section (`id="resume"`) is hidden by default and only shown when `:target` matches
- Clicking "Resume" navigates to `#resume`, hiding landing and showing resume
- "← Back" navigates to `#home`, restoring the default state
- No JavaScript required

### Print / PDF
- **Separate PDF template** (`resume.template.html`) — a dedicated Jinja2 template rendered from the same `resume.md` data, producing `resume.html` (gitignored, build artifact)
- The PDF template is optimized purely for paper: single column, compact header, tighter type, no landing section, no nav bar, no interactive elements, no crimson top border
- Accent color (`#9b2335`) retained in PDF for section headings and bullet markers — adds polish and prints well
- `generate_pdf_browser.py` loads `resume.html` directly (no hash navigation, no CSS `:target` needed)
- Single-page layout enforced via `generate_pdf_browser.py` margin/scale constants (unchanged)
- Web design and PDF design are fully decoupled — each can evolve independently

---

## `resume.md` Structure

```markdown
# Tom Irish

**Email:** [tom@tom.irish](mailto:tom@tom.irish)
**Mobile:** [253-299-4348](tel:2532994348)
**Website:** [tom.irish](https://tom.irish)
**LinkedIn:** [linkedin.com/in/tom-irish](https://linkedin.com/in/tom-irish)
**GitHub:** [github.com/tom-irish](https://github.com/tom-irish)
**Location:** Seattle, Washington

---

## Professional Summary

3–4 sentences. Years of experience, specialization, top proof point.

---

## Key Achievements

- Metric-driven bullet
- Metric-driven bullet

---

## Work Experience

### Company - Title (Start - End)

- Achievement-oriented bullet with metrics

### Company - Earlier Career (Start - End)

- Condensed single entry for older roles

---

## Skills

- **Reliability & SRE:** SRE, SLA/SLO/SLI, DORA metrics, MTTD/MTTR, incident command, OKRs
- **Observability:** Grafana, Prometheus, operational dashboards, alerting standards
- **Infrastructure:** Hybrid on-prem/Azure, VMs, Nomad, RHEL, DB2/MSSQL/Postgres
- **DevSecOps:** CI/CD, test automation, blue-green deployments, security gates, Entra ID
- **Integration:** IBM webMethods, REST APIs, EDI, AS2, sFTP

---

## Education

### Washington State University

- Bachelor of Arts in Management Information Systems

---

## Certifications

- Certification name
```

### Parsing rules
- **Grouped skills:** A bullet starting with `**Label:**` is a skill group — label becomes the category heading, remainder is a comma-separated tag list
- **Flat skills:** A bullet without `**...**` at the start is a simple tag (backward compatible)
- **Key Achievements:** New section, parsed as a flat bullet list, rendered in a distinct block in the main column
- **GitHub contact field:** New optional field in the header, parsed alongside existing contact fields
- All other parsing rules unchanged (job title regex, section splitting, etc.)

---

## File Structure Changes

| File | Change |
|------|--------|
| `assets/main.css` | Replace entirely — new hand-written CSS (~200–300 lines) |
| `assets/pdf.css` | New — print-specific stylesheet for the PDF template |
| `assets/main.js` | Delete — no JavaScript |
| `assets/noscript.css` | Delete — no longer needed |
| `index.template.html` | Rewrite as Jinja2 template — web site, landing + resume sections, CSS `:target` toggle |
| `resume.template.html` | New Jinja2 template — PDF-only, single column, print-optimized, no interactive elements |
| `index.html` | Generated by convert script from `index.template.html` (gitignored) |
| `resume.html` | New — generated by convert script from `resume.template.html`, loaded by PDF generator (gitignored) |
| `resume.md` | Add GitHub field, Key Achievements section, grouped skills format |
| `scripts/convert_resume.py` | Switch from BeautifulSoup injection to Jinja2 rendering; extend parser for new sections; render both templates |
| `scripts/validate_resume.py` | Update: recognize Key Achievements as valid section, grouped skill format, GitHub field |
| `scripts/generate_pdf_browser.py` | Load `resume.html` directly instead of `index.html#resume` |
| `requirements.txt` | Remove `beautifulsoup4`, add `jinja2` |
| `tests/` | Update tests to cover new sections, parsing rules, and both rendered outputs |

---

## Assets Kept

- `assets/images/tom-irish.jpg` — profile photo
- `assets/images/favicon.png` — favicon
- `assets/images/apple-touch-icon.png` — touch icon
- `assets/images/share.jpg` — OG share image
- `assets/icons.svg` — icon sprite (review which icons are still needed; remove unused)

> **Not deployed:** `resume.html` is a build artifact used only for PDF generation — it is gitignored and not served by Cloudflare Pages.

---

## Responsive Breakpoints

| Breakpoint | Behavior |
|---|---|
| < 480px | Landing: icons wrap if needed; Resume: single column, tighter padding |
| 480px–767px | Landing: comfortable centered card; Resume: single column |
| 768px+ | Resume: two-column layout activates |
| 1200px+ | Max-width cap on resume container, centered |

---

## Definition of Done

- [ ] `python3 scripts/validate_resume.py` — passes clean
- [ ] `python3 scripts/convert_resume.py --dry-run` — succeeds
- [ ] `/Users/tom/Library/Python/3.9/bin/pytest tests/ -v` — all pass
- [ ] Local preview looks correct on narrow (375px), medium (768px), and wide (1440px) viewports
- [ ] `resume.pdf` is exactly one page
- [ ] No `main.js`, no `noscript.css`, no Google Fonts link in output HTML
- [ ] GitHub Actions passes and Wrangler deploy succeeds after merge to main
