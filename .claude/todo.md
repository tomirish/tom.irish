# tom.irish — Todo

## Open

## Done

9. **Revisit Syncthing ignore config for `.venv/`** — confirmed correct: `~/GitHub/` syncs to RPi/NAS but `.venv/` is Mac-architecture-specific and regeneratable from `requirements.txt`. Excluding from both `.stignore` and `.gitignore` is intentional — no backup needed.

1. **Resume content** — Rewrote Professional Summary (1 tight paragraph), Key Achievements (8 verified metric-driven bullets), work experience bullets (real numbers replacing AI placeholders), skills (Leadership & Management / Engineering & Platform), and added SAFe DevOps Practitioner cert.

2. **Front-end rewrite** — replaced Carrd-generated `main.js`/`main.css` with clean hand-written code. Jinja2 templating, zero JS, CSS `:target` toggle, separate PDF template, Google Fonts (Playfair Display + DM Sans), horizontal landing layout, sticky resume header. Deployed on `frontend-rewrite` branch, pending merge to main.

3. **Security red team (2026-04-20)** — reviewed all findings: CSP unsafe-inline (accepted), CORS * (accepted), HTML injection in share image script (fixed), HSTS max-age (accepted), no SRI for CF Insights (accepted), Actions not SHA-pinned (fixed), missing COOP/COEP (accepted), build SHA in meta tags (accepted), ROT13 email (accepted), link checker UA spoof (fixed).

4. **Fix fragile CWD-relative paths** — `validate_resume.py` and `check_links.py` now compute `REPO_ROOT` explicitly; bundled with Phase 4 reorganization.

5. **Resolve `share.jpg` identity crisis** — chose Option A (gitignore); `share.jpg` is always regenerated in CI, consistent with `index.html`/`resume.pdf` pattern.

6. **`workflow_dispatch` for build job** — added to `build.yml` so manual redeployment works without a dummy commit.

7. **Python linting with `ruff`** — added to `requirements.txt` and CI; `ruff check scripts/build/ scripts/tools/ tests/` runs before tests on every push.

8. **Makefile** — `make validate`, `make build`, `make test`, `make pdf`, `make serve`, `make all`.

9. **Pre-commit hooks** — trailing-whitespace, end-of-file-fixer, ruff, validate-resume; wired to `.pre-commit-config.yaml`.

10. **Phase 4 reorganization** — split `scripts/` into `scripts/build/` (CI pipeline) and `scripts/tools/` (manual generators); moved source files into `src/` (`resume.md`, templates, CSS, `history.html`, `robots.txt`, `sitemap.xml`, `_headers`); cleaned `assets/` to deployed-only files; fixed `pdf.css` font paths; updated all path references in scripts, tests, and workflows.

11. **Python 3.14 + `.python-version`** — added `.python-version` (3.14); CI reads it via `python-version-file` in both workflows; `.venv/` added to `.gitignore` and `.stignore`; Makefile and CLAUDE.md updated to `.venv/bin/pytest`.

12. **Pin stylelint via `package.json`** — exact-pinned to 16.26.1; `npm ci && npx stylelint` in CI; `node_modules/` added to `.gitignore`.

13. **Nightly failure alerting** — `nightly.yml` opens a GitHub issue on any failure; added `issues: write` permission.

14. **Nightly Checks badge** — added to README alongside Build and Deploy; badge rule updated to 5 badges (Site, Build, Nightly, CodeQL, Version).

15. **Version tagging convention** — confirmed manual and intentional; tags mark design milestones (currently `v7.0`), not deploys. No automation needed. Documented in CLAUDE.md.

16. **generate_github_profile.py** — confirmed it belongs in `scripts/tools/`; generates the GitHub profile picture, not deployed to the site. Documented in CLAUDE.md.

17. **Caching strategy in `src/_headers`** — already optimal: `/assets/*` has `max-age=31536000, immutable`; HTML/PDF intentionally use Cloudflare's default. No changes needed.

18. **Composite action for CI setup** — extracted Python setup (set up Python, pip cache, pip install) into `.github/actions/setup/action.yml`; both `build` and `nightly` use it. Checkout remains explicit in each workflow (local actions require checkout first).

19. **Evaluate link checker scope** — audited `src/history.html` (only local asset paths, no external URLs) and `src/index.template.html` (all hrefs are Jinja2 template variables from `resume.md`). Scope is already correct; no extension needed.

20. **Add type annotations to scripts** — annotated all functions in `scripts/build/`; `scripts/tools/` was already annotated. Added `mypy==1.16.0` to `requirements.txt`, `pyproject.toml` with `[tool.mypy]` config, `Type-check Python` step in `build.yml`, and `make lint` target. `mypy` passes clean on all 9 source files.

21. **Cloudflare dashboard audit** — Platform features (Early Hints ✅, HTTP/2 ✅, Brotli on by default ✅), SSL/TLS (Full strict, Always HTTPS, TLS 1.3, min 1.2 ✅), DNSSEC ✅, CF preview deployments disabled ✅, Dependabot auto-merge re-enabled with `dependabot.yml` workflow ✅.

22. **Update README to reflect the pipeline's philosophy** — replaced one-liner with 3-sentence philosophy (DevSecOps, pipeline is the CMS); fixed Phase 4 file paths (`src/resume.md`, `src/index.template.html`, `src/resume.template.html`); trimmed redundant "How It Works" lead-in.

23. **README overhaul** — pipeline diagram expanded to two phases (Quality gates + Build & deploy); Files section replaced with single Repo Structure table at directory level; section renamed from Files to Repo Structure.

24. **security.txt** — `src/.well-known/security.txt` deployed at `/.well-known/security.txt`; 1-day cache header; annual renewal noted in CLAUDE.md (expires 2027-05-05).

25. **Custom 404 page** — `src/404.html` deployed automatically by CF Pages; matches site design (Playfair/DM Sans, crimson accent, dark mode); respects localStorage theme toggle.

26. **Live Lighthouse performance badge** — nightly workflow writes averaged performance score to a public GitHub Gist after each Lighthouse run; shields.io endpoint badge reads from Gist; score is earned nightly not hardcoded. GIST_TOKEN secret (classic PAT, gist scope, expires 2027-05-05) stored in password vault.
