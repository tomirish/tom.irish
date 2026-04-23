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

```mermaid
flowchart TD
    A([resume.md <br> pushed to main]) --> B[GitHub Actions triggers]
    click A href "resume.md" "View resume.md" _blank
    B --> C[validate_resume.py]
    C --> D[convert_resume.py]
    D --> E[generate_pdf_browser.py]
    D --> F[generate_share_image.py]
    F --> G[pytest tests/]

    subgraph parallel [Parallel Tasks]
        direction LR
        E & F
    end

    G --> H[Wrangler deploys to Cloudflare Pages]
    E --> G
    H --> I[https://tom.irish]
    style A font-size:9px
    style B font-size:14px
```     
    
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
