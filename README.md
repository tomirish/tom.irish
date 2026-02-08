# Tom Irish - Personal Website

**Status & Links:**  
[![Preview Site](https://img.shields.io/badge/Preview-tomirish.github.io/tom.irish-blue)](https://tomirish.github.io/tom.irish/)
[![Production Site](https://img.shields.io/badge/Production-tom.irish-green)](https://tom.irish)
[![Build Status](https://img.shields.io/badge/Build-Automated-success)](https://github.com/tomirish/tom.irish/actions)

**Platform & Infrastructure:**  
[![Host: Cloudflare](https://img.shields.io/badge/Host-Cloudflare-F38020)](https://cloudflare.com)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-222222?logo=github)](https://pages.github.com)

**Tech Stack:**  
[![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/Markdown-000000?logo=markdown)](https://www.markdownguide.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Carrd.co](https://img.shields.io/badge/Carrd.co-3E4374)](https://carrd.co)

Personal website and resume for Tom Irish using automated markdown-to-HTML conversion and PDF generation with a two-branch workflow for preview and production deployment.

---

## 🚀 Quick Start

### Update Your Resume (Easiest Way)

1. Go to [resume.md on preview branch](https://github.com/tomirish/tom.irish/blob/preview/resume.md)
2. Click the pencil icon (✏️) to edit directly on GitHub
3. Make your changes
4. Commit directly to the `preview` branch
5. Wait ~2 minutes for GitHub Actions to build
6. Review at [tomirish.github.io/tom.irish](https://tomirish.github.io/tom.irish/)
7. When happy, merge to production (see below)

**Your website and PDF stay in sync automatically!**

---

## 📋 About

This repository uses a **two-branch workflow**:

- **Preview Branch:** Development and testing → [tomirish.github.io/tom.irish](https://tomirish.github.io/tom.irish/)
- **Main Branch:** Production → [tom.irish](https://tom.irish) via Cloudflare Pages

All content is managed through a single `resume.md` file.

---

## 📁 Repository Structure

```
tom.irish/
├── .github/
│   └── workflows/
│       ├── build-preview.yml        # Preview automation
│       └── build-main.yml           # Production automation
├── scripts/                         # Automation scripts
│   ├── validate_resume.py           # Format validation
│   ├── convert_resume.py            # Markdown → HTML
│   └── generate_pdf_browser.py      # HTML → PDF
├── assets/                          # Website styling & images
│   ├── main.css
│   ├── images/
│   └── icons.svg
├── public/                          # Production-ready files
│   ├── index.html                   # Deployed HTML
│   ├── resume.pdf                   # Deployed PDF
│   └── assets/                      # Deployed assets
├── index.html                       # Generated from resume.md
├── resume.md                        # ✏️ EDIT THIS - Source of truth
├── resume.pdf                       # Auto-generated PDF
└── README.md                        # This file
```

---

## ✏️ How to Update Your Resume

### Method 1: Edit on GitHub (Recommended)

1. Go to [resume.md on preview branch](https://github.com/tomirish/tom.irish/blob/preview/resume.md)
2. Click the pencil icon (✏️)
3. Make changes
4. Commit to `preview` branch
5. Wait for GitHub Actions (~2 min)
6. Check [preview site](https://tomirish.github.io/tom.irish/)

### Method 2: Edit Locally

```bash
cd ~/GitHub/tom.irish
git checkout preview
# Edit resume.md in your editor
git add resume.md
git commit -m "Update resume"
git push
```

### Resume Format

```markdown
# Tom Irish

**Email:** [your@email.com](mailto:your@email.com)
**Location:** Your City, State

## Professional Summary

Your summary here...

## Work Experience

### Company - Job Title (Start - End)

- Bullet point 1
- Bullet point 2
- Bullet point 3

## Skills

- Skill 1
- Skill 2
- Skill 3

## Education

### School Name

- Degree information
- Graduation year

## Certifications

- Certification 1
- Certification 2
```

---

## 🚀 Deploying to Production

### Option 1: Command Line (No PDF conflicts)

```bash
git checkout main
git merge preview
git push
```

### Option 2: Pull Request (May have PDF conflicts)

Pull requests work but require command line to resolve binary PDF conflicts. Command line merge is simpler for this single-maintainer workflow.

---

## 🤖 How The Automation Works

### The Build Pipeline

```
You edit resume.md
       ↓
GitHub Actions triggers
       ↓
scripts/validate_resume.py
  - Checks markdown format
  - Validates required sections
  - Reports warnings
       ↓
scripts/convert_resume.py
  - Parses resume.md
  - Updates index.html (preserves styling)
  - Handles unlimited jobs, skills, education
       ↓
scripts/generate_pdf_browser.py
  - Starts local HTTP server
  - Opens page in headless Chromium
  - Generates PDF (just like manual browser print)
       ↓
Files synced to public/ directory
       ↓
Changes committed & pushed
       ↓
Deploys automatically
```

### Preview Branch Workflow

1. ✅ Validates `resume.md` format
2. 🔄 Converts markdown → HTML (if resume.md changed)
3. 📄 Generates PDF (always)
4. 📂 Syncs all files to `public/` directory
5. 🚀 Auto-commits changes
6. 📡 Deploys to GitHub Pages

### Main Branch Workflow

1. 📄 Regenerates PDF
2. 📂 Syncs files to `public/` directory
3. 🚀 Auto-commits if changed
4. 📡 Triggers Cloudflare deployment

### Key Scripts Explained

**`scripts/validate_resume.py`**
- Validates markdown structure
- Checks for required sections (Professional Summary, Work Experience, Skills, Education)
- Reports warnings for potential issues
- Runs before every build on preview branch

**`scripts/convert_resume.py`**
- Parses `resume.md` content using BeautifulSoup
- Updates specific sections in `index.html` by ID
- Dynamically generates work experience entries
- Dynamically generates education entries
- Preserves all website styling and structure

**`scripts/generate_pdf_browser.py`**
- Uses Playwright with headless Chromium
- Loads actual website locally via HTTP
- Generates PDF using browser's native print function
- Same result as manually printing from Chrome
- Customizable margins and scaling

---

## 🎨 Customization

### Change Website Styling

Edit files in `assets/`:
- `assets/main.css` - Main stylesheet
- `assets/images/` - Images and photos
- `assets/icons.svg` - Icon definitions

Changes to CSS/images take effect immediately. The automation only modifies text content in `index.html`, not styling.

### Adjust PDF Margins/Sizing

Edit `scripts/generate_pdf_browser.py` and modify the `margin` and `scale` values:

```python
page.pdf(
    path='resume.pdf',
    format='Letter',
    margin={
        'top': '0.25in',
        'right': '0.3in',
        'bottom': '0.25in',
        'left': '0.3in'
    },
    scale=0.95
)
```

---

## 🛠️ Local Development

### Prerequisites

```bash
pip install beautifulsoup4 playwright
playwright install --with-deps chromium
```

### Test Locally Before Pushing

```bash
# Validate resume format
python scripts/validate_resume.py

# Convert markdown to HTML
python scripts/convert_resume.py

# Generate PDF
python scripts/generate_pdf_browser.py

# View the site locally
python -m http.server 8000
# Open http://localhost:8000
```

---

## 🔒 Security

- **Production deployment:** Only serves files from `public/` directory
- **Source files protected:** `resume.md`, `scripts/`, and `.github/` are not publicly accessible on tom.irish
- **Preview site:** All files accessible (for development purposes)

---

## 📝 File Descriptions

| File | Purpose | Edit? |
|------|---------|-------|
| `resume.md` | Resume content source | ✅ Yes - edit this! |
| `index.html` | Website HTML | ❌ Auto-generated |
| `resume.pdf` | PDF resume | ❌ Auto-generated |
| `public/*` | Production-ready files | ❌ Auto-generated |
| `scripts/validate_resume.py` | Format validator | 🔧 Only if changing automation |
| `scripts/convert_resume.py` | Markdown → HTML script | 🔧 Only if changing automation |
| `scripts/generate_pdf_browser.py` | HTML → PDF script | 🔧 Only if changing PDF settings |
| `.github/workflows/*.yml` | GitHub Actions config | 🔧 Only if changing automation |
| `assets/` | CSS, images, icons | ✅ Yes - to change styling |

---

## 🔄 Branch Strategy

### Preview Branch
- **Purpose:** Development and testing
- **URL:** [tomirish.github.io/tom.irish](https://tomirish.github.io/tom.irish/)
- **Deployment:** GitHub Pages
- **Edit here first!** All changes start on preview

### Main Branch  
- **Purpose:** Production
- **URL:** [tom.irish](https://tom.irish)
- **Deployment:** Cloudflare Pages (from `public/` directory)
- **Only receives changes via merge from preview**

---

## 🚨 Troubleshooting

### Resume didn't update after push

1. Check [GitHub Actions](https://github.com/tomirish/tom.irish/actions) for build status
2. Click on the latest "Build Preview" workflow run
3. Review the logs for errors
4. Wait 2-3 minutes for deployment
5. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

### Build failed

Common issues:
- **Missing required sections:** Ensure resume.md has Professional Summary, Work Experience, Skills, and Education
- **Incorrect markdown format:** Check that job entries follow the format: `### Company - Job Title (Start - End)`
- **Dependency issues:** Actions logs will show if Python packages failed to install

Run validation locally to debug:
```bash
python scripts/validate_resume.py
```

### PDF looks different than website

The PDF is generated using Chromium's print function. If it looks wrong:
1. Verify the website looks correct at the preview URL first
2. Check that `generate_pdf_browser.py` completed successfully in Actions logs
3. Try adjusting margins or scale in `scripts/generate_pdf_browser.py`

### Changes to CSS/images not showing

- Clear browser cache or hard refresh (Cmd+Shift+R / Ctrl+Shift+R)
- Wait 2-3 minutes for deployment to complete
- Check [GitHub Actions](https://github.com/tomirish/tom.irish/actions) to ensure workflow completed

### Cloudflare not deploying

1. Check [Cloudflare dashboard](https://dash.cloudflare.com/) for deployment status
2. Verify build output directory is set to `/public` in Cloudflare settings
3. Ensure commit doesn't have `[skip ci]` in message
4. Check that you're on main branch

### Workflow not triggering

Make sure you:
1. Pushed to the correct branch (`preview` for testing, `main` for production)
2. Have the workflow files in `.github/workflows/`
3. Committed actual changes (not just whitespace)

---

## 🔗 Links

- **Production:** [tom.irish](https://tom.irish)
- **Preview:** [tomirish.github.io/tom.irish](https://tomirish.github.io/tom.irish/)
- **Repository:** [github.com/tomirish/tom.irish](https://github.com/tomirish/tom.irish)
- **Actions:** [github.com/tomirish/tom.irish/actions](https://github.com/tomirish/tom.irish/actions)

---

## 📄 License

Personal website - all rights reserved.
