# Tom Irish - Production Website

**Production Site:**  
[![Live Site](https://img.shields.io/badge/Live-tom.irish-green)](https://tom.irish)
[![Host: Cloudflare](https://img.shields.io/badge/Host-Cloudflare-F38020)](https://cloudflare.com)

**Tech Stack:**  
[![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Template: Carrd.co](https://img.shields.io/badge/Template-Carrd.co-3E4374)](https://carrd.co)

Production repository for [tom.irish](https://tom.irish). Automatically deploys to Cloudflare.

A personal website using a simple one-page design that simulates multiple pages using section breaks.

---

## 📋 About

This is the **production repository** for tom.irish. 

- **Development/Staging:** Changes are developed and tested in [tomirish/tomirish.github.io](https://github.com/tomirish/tomirish.github.io)
- **Preview:** Changes can be previewed at [tomirish.github.io](https://tomirish.github.io/)
- **Production:** Verified changes from the dev repo are manually deployed here
- **Deployment:** Pushes to this repo automatically deploy to [tom.irish](https://tom.irish) via Cloudflare

## 🚀 Deployment Workflow

```
1. Edit resume.md in dev repo (tomirish/tomirish.github.io)
   ↓
2. GitHub Actions generates index.html + resume.pdf
   ↓
3. Preview at tomirish.github.io
   ↓
4. Verify changes look correct
   ↓
5. Manually copy index.html + resume.pdf to this repo
   ↓
6. Push to main branch
   ↓
7. Cloudflare automatically deploys to tom.irish
```

## 📁 Repository Structure

```
tom.irish/
├── assets/          # Website styling & images
├── index.html       # Main website
├── resume.pdf       # Downloadable resume
└── README.md        # This file
```

## 🔄 How to Deploy

1. Verify changes at [tomirish.github.io](https://tomirish.github.io/)
2. Copy `index.html` and `resume.pdf` from dev repo
3. Replace files in this repo
4. Commit and push:
   ```bash
   git add index.html resume.pdf
   git commit -m "Deploy: [description of changes]"
   git push
   ```
5. Cloudflare will automatically deploy to production

## ⚠️ Important Notes

- **Do not edit files directly in this repo** - all changes should come from the dev repo
- This ensures the dev repo and production stay in sync
- The dev repo has automation for generating HTML/PDF from markdown

## 🔗 Related Repositories

- **Development Repo:** [tomirish/tomirish.github.io](https://github.com/tomirish/tomirish.github.io)
- **Preview Site:** [tomirish.github.io](https://tomirish.github.io/)

## 📄 License

Personal website - all rights reserved.
