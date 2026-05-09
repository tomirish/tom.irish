# Tom Irish - Personal Website

[![Production Site](https://img.shields.io/website?url=https%3A%2F%2Ftom.irish&label=tom.irish&logo=cloudflare&logoColor=F38020&labelColor=343B42&up_color=2EBC4F)](https://tom.irish)
[![Build, Test, Deploy](https://github.com/tomirish/tom.irish/actions/workflows/build.yml/badge.svg)](https://github.com/tomirish/tom.irish/actions/workflows/build.yml)
[![Nightly Audit](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/tomirish/cfcbef4e90b3367512488562c649334e/raw/lighthouse.json)](https://github.com/tomirish/tom.irish/actions/workflows/nightly.yml)
[![Version](https://img.shields.io/github/v/tag/tomirish/tom.irish?label=Version&labelColor=343B42&color=0075D8&logo=git&logoColor=959DA5)](https://tom.irish/history)

Personal website and resume for [Tom Irish](https://tom.irish). Overengineered by design using DevSecOps principles, because if it's worth doing it's worth doing right. The pipeline is the CMS: [`resume.md`](src/resume.md) is the single source of truth for both the site and PDF.

---

## How It Works

```
resume.md pushed to main
        ↓
┌── Quality gates ────────────────────────────────────────────────────┐
│  pip-audit                — dependency vulnerability scan           │
│  ruff + mypy              — Python linting and type checking        │
│  stylelint                — CSS linting                             │
│  validate_resume.py       — resume format check                     │
│  check_links.py           — link validation                         │
│  pytest                   — test suite                              │
│  CodeQL                   — static analysis (non-blocking)          │
└─────────────────────────────────────────────────────────────────────┘
        ↓
┌── Build & deploy ───────────────────────────────────────────────────┐
│  convert_resume.py        — generates index.html                    │
│  generate_pdf_browser.py  — generates resume.pdf                    │
│  generate_share_image.py  — generates OG share image                │
│  attest-build-provenance  — signs SLSA provenance for artifacts     │
│  Wrangler                 — deploys to Cloudflare Pages             │
└─────────────────────────────────────────────────────────────────────┘
        ↓
https://tom.irish
```

---

## Repo Structure

```
tom.irish/
|-- src/                 — templates, CSS, and static files
|   `-- resume.md        — the only file you edit
|-- assets/              — fonts and images
|-- docs/                — editing and customization guides
|-- scripts/
|   |-- build/           — CI scripts (validate, convert, generate HTML/PDF/OG image)
|   `-- tools/           — manual generators (favicons, profile picture)
|-- tests/               — test suite
`-- .github/workflows/   — build, nightly audit, Lighthouse, CodeQL, Dependabot
```
