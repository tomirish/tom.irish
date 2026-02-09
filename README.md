# Tom Irish - Personal Website

**Live Site:**  
[![Production Site](https://img.shields.io/badge/Live-tom.irish-green)](https://tom.irish)
[![Build Status](https://img.shields.io/badge/Build-Automated-success)](https://github.com/tomirish/tom.irish/actions)

**Tech Stack:**  
[![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Cloudflare](https://img.shields.io/badge/Host-Cloudflare-F38020)](https://cloudflare.com)

Personal website and resume for Tom Irish with automated markdown-to-HTML conversion and PDF generation. Edit one markdown file, push to GitHub, and your website and PDF update automatically.

---

## 🚀 Quick Start

### Update Your Resume (Easiest Way)

1. Go to [resume.md](https://github.com/tomirish/tom.irish/blob/main/resume.md)
2. Click the pencil icon (✏️) to edit directly on GitHub
3. Make your changes
4. Commit directly to the `main` branch
5. Wait ~2 minutes for GitHub Actions to build
6. Your site updates automatically at [tom.irish](https://tom.irish)

**Your website and PDF stay in sync automatically!**

---

## 📋 About

This is a simple, automated personal website that:
- Uses a single `resume.md` file as the source of truth
- Automatically generates HTML and PDF versions
- Deploys to Cloudflare Pages via the `public/` directory
- Runs on every push to `main` branch

---

## 📁 Repository Structure

```
tom.irish/
├── .github/
│   └── workflows/
│       └── build.yml                # Automation workflow
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
├── .gitattributes                   # Auto-resolves PDF merge conflicts
├── index.html                       # Generated from resume.md
├── resume.md                        # ✏️ EDIT THIS - Source of truth
├── resume.pdf                       # Auto-generated PDF
└── README.md                        # This file
```

---

## ✏️ How to Update Your Resume

### Method 1: Edit on GitHub (Recommended)

1. Go to [resume.md](https://github.com/tomirish/tom.irish/blob/main/resume.md)
2. Click the pencil icon (✏️)
3. Make changes
4. Commit to `main` branch
5. Wait for GitHub Actions (~2 min)
6. Check [tom.irish](https://tom.irish)

### Method 2: Edit Locally

```bash
# 1. Navigate to repository
cd ~/github/tom.irish

# 2. Pull latest changes
git pull origin main

# 3. Edit resume.md in your editor
code resume.md
# or
open -a "TextEdit" resume.md

# 4. Commit and push
git add resume.md
git commit -m "Update resume: [describe changes]"
git push origin main

# 5. If you get "rejected" error, pull and try again
git pull origin main --no-rebase
git push origin main

# 6. Wait for build (~2 min) and check live site
# https://tom.irish
```

### Resume Format

Your `resume.md` should follow this structure:

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

## 🤖 How The Automation Works

### The Build Pipeline

```
You edit resume.md and push to main
       ↓
GitHub Actions triggers automatically
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
Changes committed & pushed back to repo
       ↓
Cloudflare deploys from public/
       ↓
Your site is live at https://tom.irish
```

### Key Scripts Explained

**`scripts/validate_resume.py`**
- Validates markdown structure
- Checks for required sections (Professional Summary, Work Experience, Skills, Education)
- Reports warnings for potential issues
- Runs before every build

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

Changes to CSS/images take effect on next push. The automation only modifies text content in `index.html`, not styling.

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
# Install Python dependencies
pip3 install beautifulsoup4 playwright
playwright install --with-deps chromium
```

### Test Locally Before Pushing

```bash
# Validate resume format
python3 scripts/validate_resume.py

# Convert markdown to HTML
python3 scripts/convert_resume.py

# Generate PDF
python3 scripts/generate_pdf_browser.py

# View the site locally
python3 -m http.server 8000
# Open http://localhost:8000
```

---

## 🔒 Security

- **Production deployment:** Only serves files from `public/` directory
- **Source files protected:** `resume.md`, `scripts/`, and `.github/` are not publicly accessible on tom.irish
- Cloudflare Pages automatically handles HTTPS and security

---

## 📝 File Descriptions

| File | Purpose | Edit? |
|------|---------|-------|
| `resume.md` | Resume content source | ✅ Yes - edit this! |
| `index.html` | Website HTML | ❌ Auto-generated |
| `resume.pdf` | PDF resume | ❌ Auto-generated |
| `public/*` | Production-ready files | ❌ Auto-generated |
| `.gitattributes` | Auto-resolves PDF conflicts | ℹ️ Already configured |
| `scripts/validate_resume.py` | Format validator | 🔧 Only if changing automation |
| `scripts/convert_resume.py` | Markdown → HTML script | 🔧 Only if changing automation |
| `scripts/generate_pdf_browser.py` | HTML → PDF script | 🔧 Only if changing PDF settings |
| `.github/workflows/build.yml` | GitHub Actions config | 🔧 Only if changing automation |
| `assets/` | CSS, images, icons | ✅ Yes - to change styling |

---

## 🚨 Troubleshooting

### Resume didn't update after push

1. Check [GitHub Actions](https://github.com/tomirish/tom.irish/actions) for build status
2. Click on the latest workflow run
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
python3 scripts/validate_resume.py
```

### PDF looks different than website

The PDF is generated using Chromium's print function. If it looks wrong:
1. Verify the website looks correct first
2. Check that `generate_pdf_browser.py` completed successfully in Actions logs
3. Try adjusting margins or scale in `scripts/generate_pdf_browser.py`

### Changes to CSS/images not showing

- Clear browser cache or hard refresh (Cmd+Shift+R / Ctrl+Shift+R)
- Wait 2-3 minutes for deployment to complete
- Check [GitHub Actions](https://github.com/tomirish/tom.irish/actions) to ensure workflow completed

### Cloudflare not deploying

1. Check [Cloudflare dashboard](https://dash.cloudflare.com/) for deployment status
2. Verify build output directory is set to `/public` in Cloudflare settings
3. Ensure you're on main branch

### "Push rejected" error

This happens when the auto-build commits files while you're working:

```bash
# Pull the auto-build commits first
git pull origin main --no-rebase

# Then push your changes
git push origin main
```

This is normal behavior - the automation commits generated files back to the branch.

### Need to regenerate files locally

If automation isn't working and you need to fix things manually:

```bash
# Regenerate HTML from markdown
python3 scripts/convert_resume.py

# Regenerate PDF from HTML  
python3 scripts/generate_pdf_browser.py

# Commit the changes
git add index.html resume.pdf public/
git commit -m "Manual regeneration of HTML and PDF"
git push origin main
```

---

## 🔗 Links

- **Live Site:** [tom.irish](https://tom.irish)
- **Repository:** [github.com/tomirish/tom.irish](https://github.com/tomirish/tom.irish)
- **Actions:** [github.com/tomirish/tom.irish/actions](https://github.com/tomirish/tom.irish/actions)

---

## 📄 License

Personal website - all rights reserved.

---

**Last Updated:** February 2026
