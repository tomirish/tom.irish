# Tom Irish - Personal Website

[![Production Site](https://img.shields.io/website?url=https%3A%2F%2Ftom.irish&label=tom.irish&logo=cloudflare&logoColor=F38020&labelColor=343B42)](https://tom.irish)
[![Build and Deploy](https://github.com/tomirish/tom.irish/actions/workflows/build.yml/badge.svg)](https://github.com/tomirish/tom.irish/actions/workflows/build.yml)
[![CodeQL](https://github.com/tomirish/tom.irish/actions/workflows/codeql.yml/badge.svg)](https://github.com/tomirish/tom.irish/actions/workflows/codeql.yml)

Personal website and resume for [Tom Irish](https://tom.irish) — a clean, single-page design driven entirely by Markdown.

---

## How It Works

Edit [`resume.md`](resume.md) and the site and PDF update automatically:

```
resume.md pushed to main
        ↓
┌── GitHub Actions ───────────────────────────────────────────────────┐
│  validate_resume.py       — checks format and required sections     │
│  convert_resume.py        — updates index.html from resume.md       │
│  generate_pdf_browser.py  — generates resume.pdf                    │
│  generate_share_image.py  — regenerates OG preview image            │
│  Wrangler                 — deploys to Cloudflare Pages             │
└─────────────────────────────────────────────────────────────────────┘
        ↓
https://tom.irish
```

---

## Files

### Content & style

| File | Purpose |
|------|---------|
| [`resume.md`](resume.md) | Resume content |
| [`docs/EDITING.md`](docs/EDITING.md) | Format reference for `resume.md`: required sections, field formats, section-by-section examples |
| [`docs/CUSTOMIZING.md`](docs/CUSTOMIZING.md) | Style and customization reference: typography, color, layout, CSS/HTML components, design intent |
| [`index.template.html`](index.template.html) | Web page layout and structure |
| [`resume.template.html`](resume.template.html) | PDF layout and structure |
| `assets/` | fonts, CSS, and images |

### Pipeline internals

| File | Purpose |
|------|---------|
| `scripts/` | Build automation |
| `tests/` | Test suite |
| `.github/workflows/build.yml` | CI/CD config — build on push, nightly dependency audit + Lighthouse |

