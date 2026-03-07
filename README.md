# Tom Irish - Personal Website

**Status:**
[![Production Site](https://img.shields.io/badge/Site-tom.irish-green)](https://tom.irish)
[![Cloudflare](https://img.shields.io/badge/Host-Cloudflare-F38020)](https://cloudflare.com)
[![Build and Deploy](https://github.com/tomirish/tom.irish/actions/workflows/build.yml/badge.svg)](https://github.com/tomirish/tom.irish/actions/workflows/build.yml)

**Tech Stack:**
[![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/Markdown-000000?logo=markdown)](https://www.markdownguide.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)

Personal website and resume for [Tom Irish](https://tom.irish). `resume.md` is the single source of truth — editing it automatically rebuilds the site and PDF.

---

## Updating the Resume

1. Open [resume.md](https://github.com/tomirish/tom.irish/blob/main/resume.md) on GitHub
2. Click the pencil icon to edit
3. Commit directly to `main`
4. GitHub Actions builds and deploys automatically

---

## How It Works

```
resume.md pushed to main
       ↓
GitHub Actions triggers
       ↓
validate_resume.py      — checks format and required sections
convert_resume.py       — updates index.html from resume.md
generate_pdf_browser.py — generates resume.pdf via headless Chromium
       ↓
Wrangler deploys to Cloudflare Pages → https://tom.irish
```

---

## Files

| File | Purpose | Edit? |
|------|---------|-------|
| `resume.md` | Resume content — single source of truth | ✅ Yes |
| `index.html` | Website HTML | ❌ Auto-generated |
| `resume.pdf` | PDF resume | ❌ Auto-generated |
| `public/` | Transient build artifact, deployed by Wrangler | ❌ Not committed |
| `assets/` | CSS, images, icons | ✅ Yes — to change styling |
| `scripts/` | Build automation | 🔧 Only if changing the pipeline |
| `.github/workflows/build.yml` | CI/CD configuration | 🔧 Only if changing automation |

---

## License

Personal website — all rights reserved.
