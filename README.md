# Tom Irish - Personal Website

[![Production Site](https://img.shields.io/badge/Site-tom.irish-green)](https://tom.irish)
[![Cloudflare](https://img.shields.io/badge/Host-Cloudflare-F38020)](https://cloudflare.com)
[![Build and Deploy](https://github.com/tomirish/tom.irish/actions/workflows/build.yml/badge.svg)](https://github.com/tomirish/tom.irish/actions/workflows/build.yml)
[![Markdown](https://img.shields.io/badge/Markdown-000000?logo=markdown)](https://www.markdownguide.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

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
| [`docs/CUSTOMIZING.md`](docs/CUSTOMIZING.md) | Style reference css and html: typography, color, layout, components, design intent |
| [`index.template.html`](index.template.html) | Web page layout and structure |
| [`resume.template.html`](resume.template.html) | PDF layout and structure |
| `assets/` | fonts, CSS, and images |

### Pipeline internals

| File | Purpose |
|------|---------|
| `scripts/` | Build automation |
| `tests/` | Test suite |
| `.github/workflows/build.yml` | CI/CD config — build on push, nightly dependency audit + Lighthouse |

