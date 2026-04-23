# Tom Irish - Personal Website

[![Production Site](https://img.shields.io/badge/Site-tom.irish-green)](https://tom.irish)
[![Cloudflare](https://img.shields.io/badge/Host-Cloudflare-F38020)](https://cloudflare.com)
[![Build and Deploy](https://github.com/tomirish/tom.irish/actions/workflows/build.yml/badge.svg)](https://github.com/tomirish/tom.irish/actions/workflows/build.yml)

[![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/Markdown-000000?logo=markdown)](https://www.markdownguide.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)

Personal website and resume for [Tom Irish](https://tom.irish) — a clean, single-page design driven entirely by Markdown.

---

## How It Works

Edit [`resume.md`](resume.md), commit to `main`, and the site and PDF update automatically:

```
resume.md pushed to main
       ↓
GitHub Actions triggers
       ↓
validate_resume.py      — checks format and required sections
convert_resume.py       — updates index.html from resume.md
generate_pdf_browser.py — generates resume.pdf via headless Chromium  ┐ parallel
generate_share_image.py — regenerates OG preview image                ┘
pytest tests/           — verifies scripts and templates
       ↓
Wrangler deploys to Cloudflare Pages → https://tom.irish
```
flowchart TD
    A[resume.md pushed to main] --> B[GitHub Actions triggers]
    B --> C[validate_resume.py]
    B --> D[convert_resume.py]
    B --> E[generate_pdf_browser.py]
    B --> F[generate_share_image.py]
    B --> G[pytest tests/]
    C --> H[Wrangler deploys to Cloudflare Pages]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I[https://tom.irish]   
    
---

## Files

| File | Purpose | Edit? |
|------|---------|-------|
| `resume.md` | Resume content | ✅ Yes |
| `index.template.html` | Web page template | ✅ Yes — layout or structure |
| `resume.template.html` | PDF template | ✅ Yes — PDF layout or structure |
| `assets/` | CSS and images | ✅ Yes — styling |
| `docs/EDITING.md` | How to edit resume.md | 📖 Reference |
| `docs/CUSTOMIZING.md` | Style and design reference | 📖 Reference |
| `scripts/` | Build automation | 🔧 Pipeline changes only |
| `tests/` | Test suite | 🔧 Pipeline changes only |
| `.github/workflows/build.yml` | CI/CD config | 🔧 Automation changes only |

---

## Docs

- **[EDITING.md](docs/EDITING.md)** — format reference for `resume.md`: required sections, field formats, section-by-section examples
- **[CUSTOMIZING.md](docs/CUSTOMIZING.md)** — style reference: typography, color, layout, components, and design intent
