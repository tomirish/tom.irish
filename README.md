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

Personal website and resume for [Tom Irish](https://tom.irish). It's a single-page design that simulates multiple sections, with automated markdown-to-HTML conversion and PDF generation.

Simply edit `resume.md`, push to GitHub, and everything updates automatically.

---

## Updating Your Resume

1. Go to [resume.md](https://github.com/tomirish/tom.irish/blob/main/resume.md)
2. Click the pencil icon (✏️) to edit directly on GitHub
3. Make your changes
4. Commit directly to the `main` branch
5. Wait ~2 minutes for GitHub Actions to build
6. Your site updates automatically at [tom.irish](https://tom.irish)

### Resume Format

```markdown
# Tom Irish

**Email:** [your@email.com](mailto:your@email.com)
**Location:** Your City, State

## Professional Summary

Your summary here...

## Work Experience

### Company - Job Title (Start - End)

- Bullet point

## Skills

- Skill 1

## Education

### School Name

- Degree information

## Certifications

- Certification name
```

---

## How It Works

```
resume.md edited and pushed to main
       ↓
GitHub Actions triggers
       ↓
validate_resume.py      — checks format and required sections
       ↓
convert_resume.py       — updates index.html from resume.md
       ↓
generate_pdf_browser.py — generates resume.pdf via headless Chromium
       ↓
Wrangler deploys public/ directly to Cloudflare Pages → https://tom.irish
```

---

## Files

| File | Purpose | Edit? |
|------|---------|-------|
| `resume.md` | Resume content source | ✅ Yes |
| `index.html` | Website HTML | ❌ Auto-generated |
| `resume.pdf` | PDF resume | ❌ Auto-generated |
| `public/` | Transient build artifact, deployed by Wrangler | ❌ Not committed to git |
| `assets/` | CSS, images, icons | ✅ Yes — to change styling |
| `scripts/` | Build automation | 🔧 Only if changing the pipeline |
| `.github/workflows/build.yml` | GitHub Actions config | 🔧 Only if changing automation |

---

## Local Development

```bash
# Install dependencies
pip3 install -r requirements.txt
playwright install --with-deps chromium

# Validate resume format
python3 scripts/validate_resume.py

# Dry-run conversion (no files written)
python3 scripts/convert_resume.py --dry-run

# Full conversion
python3 scripts/convert_resume.py

# Generate PDF
python3 scripts/generate_pdf_browser.py

# Run tests
python3 -m pytest tests/ -v

# Preview site locally
python3 -m http.server 8000
# Open http://localhost:8000
```

---

## Troubleshooting

### Resume didn't update after push

1. Check [GitHub Actions](https://github.com/tomirish/tom.irish/actions) for build status
2. Review the logs for errors — the Wrangler deploy step will show if deployment succeeded
3. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

### Build failed

- **Missing required sections:** `resume.md` must have Professional Summary, Work Experience, Skills, and Education
- **Incorrect format:** Job entries must follow `### Company - Job Title (Start - End)`
- **Dependency issues:** Check Actions logs for pip install errors

Run locally to debug: `python3 scripts/validate_resume.py`

### PDF is more than one page or content is cut off

Edit the named constants at the top of `scripts/generate_pdf_browser.py`:

```python
PDF_FORMAT        = 'Letter'
PDF_MARGIN_TOP    = '0.2in'
PDF_MARGIN_RIGHT  = '0.2in'
PDF_MARGIN_BOTTOM = '0.2in'
PDF_MARGIN_LEFT   = '0.2in'
PDF_SCALE         = 0.98   # < 1.0 shrinks content to fit more on one page
```

---

## License

Personal website — all rights reserved.
