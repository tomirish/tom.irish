# CLAUDE.md — Working notes for this repo

This file is committed to a public repo. Keep it free of credentials, vault names, local paths, and anything that shouldn't be public. Use a `.local.` file (e.g. `notes.local.md`) for machine-specific or private notes — `.gitignore` will keep it out of the repo.

---

## Session start
When working in this repo, the global MEMORY.md is not auto-loaded. Read it manually at the start of each session from your Claude project memory directory.
Then read any topic files referenced in it — they contain important context.

---

## What this repo represents

**Philosophy:** *"Overengineered by design, built on DevSecOps principles. The pipeline is the CMS."* The complexity is intentional — `resume.md` is the only file edited by hand, the pipeline handles everything else. The site itself is intentionally minimal: a clean single-page design that signals reliability and empathy over flash.

**Purpose:** Tom uses this repo as a personal site, a deliberate learning tool, and a leadership credibility artifact. He shows it to his team to demonstrate what's possible and to hold himself accountable — he won't ask his team to do something he isn't willing to do and learn himself.

**How this should inform decisions:** Never treat this as "just a personal site" when making tradeoffs. If something is worth doing on a production team codebase, it's worth doing here. The overhead and rigor are the point, not a side effect. Skipping something because it's "good enough for a personal site" is the wrong frame.

---

## How Tom likes to work

**Focused and done right** — stay on the task at hand; don't add scope. But within the task, do it properly — no shortcuts, no hacks, no half-measures.

- Don't add features, abstractions, or error handling that the task doesn't require
- Build what's needed correctly; don't design for requirements that don't exist yet
- No dead code, no stale comments, no debugging artifacts
- Keep styling consistent with whatever's already in the file (indentation, naming, quote style, etc.)
- If something is unused, delete it — don't rename it or add a comment saying it was removed

**When in doubt, talk first** — if something is unclear, uncertain, or has multiple valid approaches, stop and discuss before making changes. Never guess on a live repo.

**Main branch is live** — be confident before pushing. Tom monitors deploys and gets alerts on failure — no need to babysit every push.

**Quality matters** — this is a personal website and resume, which means it's a direct reflection of Tom's professionalism. It should work correctly, look polished, and have no bugs. "Good enough" isn't the bar — it should be the best we can make it. Run tests, validate, and verify before considering anything done.

---

## What this repo is

Personal website and resume for Tom Irish at [tom.irish](https://tom.irish).

The single source of truth is `resume.md`. Every push to `main` triggers a GitHub Actions workflow that:
1. Validates `resume.md` format
2. Converts it to `index.html` (using BeautifulSoup to update specific elements by ID)
3. Generates `resume.pdf` (headless Chromium via Playwright)
4. Deploys directly to Cloudflare Pages via Wrangler

---

## Key commands

```bash
# Or use make — wraps all of the below:
make validate   # validate src/resume.md
make build      # validate + convert to index.html
make test       # run pytest
make pdf        # generate resume.pdf
make all        # validate + build + test
make lint       # ruff check + mypy type-check (scripts/build/ and scripts/tools/)
make serve      # local HTTP server at localhost:8000

# Individual scripts (build pipeline — in scripts/build/):
python3 scripts/build/validate_resume.py
python3 scripts/build/convert_resume.py --dry-run
python3 scripts/build/convert_resume.py
python3 scripts/build/generate_pdf_browser.py
python3 scripts/build/generate_share_image.py   # generated in CI, also runnable locally

# Manual generator tools (in scripts/tools/):
python3 scripts/tools/generate_icons.py             # favicon.png, favicon-dark.png, apple-touch-icon.png
python3 scripts/tools/generate_photo.py             # tom-irish-280.webp + tom-irish-280.jpg from original

# Run tests
.venv/bin/pytest tests/ -v

# Preview the site locally
python3 -m http.server 8000
# then open http://localhost:8000
# NOTE: index.html is gitignored and generated — always run convert_resume.py first
# or changes to src/index.template.html won't be visible at localhost.
# Never open src/index.template.html directly as a preview — it's the build template, not the site.
```

---

## Design quick reference

When making any CSS or HTML changes, keep these rules in mind:

- **Accent:** `#9b2335` light / `#c4394e` dark — one accent only, never a second color
- **Type:** Playfair Display 700 for names and section headings only; DM Sans 400/500/600 for everything else
- **Bullet:** single `›` character, absolutely positioned at `left: 0`, crimson — never `•`, `–`, or checkmarks
- **Stripe:** 4px solid crimson top border on every full section — always flat, never gradient
- **Icons:** inline SVG, 24×24 viewBox, `currentColor` — solid fill for brand icons, 2px stroke for UI icons
- **No** gradients, emoji, colored shadows, textures, or backdrop-filter

Full reference: `docs/CUSTOMIZING.md`

---

## Architecture notes

### mypy annotation gotcha
Local `[]` and `{}` variables inside a function typed to return `dict[str, Any]` still need explicit annotations: `summary_lines: list[str] = []`, `data: dict[str, Any] = {...}`. mypy doesn't infer them from the declared return type. Config lives in `pyproject.toml`.

### Pillow mypy gotchas
Use `Image.Resampling.LANCZOS` not `Image.LANCZOS` — the latter has no type stub. Avoid `img.save(path, **kwargs)` — pass `format=` explicitly: `img.save(path, format="WEBP", quality=90)`.

### HTML structure dependency
`convert_resume.py` reads `src/index.template.html`, injects resume content AND the contents of `src/main.css` (as `{{ main_css | safe }}`), and writes `index.html`. If `src/index.template.html` is modified and an expected ID is removed, the script will exit with a clear error. The required IDs are listed in `validate_html_structure()` in that script.

### CSS inlining
`src/main.css` is injected inline into `index.html` at build time to eliminate render-blocking CSS. Font paths in `main.css` must use absolute paths (`/assets/fonts/`) not relative ones (`fonts/`) — relative paths resolve from `src/` when the file is external but from the root when inlined.

### Lighthouse gotchas (mobile)
**Do not add font preloads** (`<link rel="preload" as="font">`). They consistently cause NO_LCP by competing with the LCP image for bandwidth under mobile throttling. This has been tried twice at every priority level.

`fetchpriority="high"` must be on the `<img>` element inside `.landing-photo`, not just the `<link rel="preload">` for the image. Moving it to the preload only causes NO_LCP.

`.landing-photo` uses a `slide-up` animation (transform only) instead of `fade-up` (opacity: 0→1) — elements starting at `opacity: 0` are excluded from LCP candidacy.

### Triggering workflows manually
```bash
gh workflow run nightly.yml --ref main  # nightly checks + Lighthouse only
gh workflow run build.yml --ref main    # full build + deploy
```
Each workflow has its own file and its own `workflow_dispatch` trigger. Inspect Lighthouse results by downloading the artifact:
```bash
gh run download <run-id> --repo tomirish/tom.irish --name lighthouse-results --dir /tmp/lh-results
```

### Job title format
Work experience entries in `resume.md` must follow:
```
### Company - Title (Start - End)
```
The regex matches the **last** set of parentheses as the date range, so titles that themselves contain parentheses (e.g. `Manager (Operations)`) work correctly.

### Extended sections
The parser supports these optional sections beyond the base format:
- **Key Achievements** (`## Key Achievements`) — bullet list, rendered before Work Experience
- **GitHub field** (`**GitHub:** [...]`) — parsed alongside other contact fields
- **Tagline field** (`**Tagline:** plain text`) — populates the landing page bio, OG/meta description, and share image; ~80 chars max so it fits on one line
- **Grouped skills** — skill bullets prefixed with `**Label:**` render as labeled rows; plain bullets render as flat items

### PDF layout
Margins and scale are named constants at the top of `scripts/build/generate_pdf_browser.py`. Adjust those rather than editing the `page.pdf()` call directly.

### Version tagging
Tags are manual and intentional — they mark significant design milestones (e.g. `v7.0` = current redesign), not individual deploys. The Version badge in the README links to `src/history.html`. Do not automate tagging on deploy.

### Image file tests
`tests/test_favicons.py` and `tests/test_apple_touch_icon.py` check exact dimensions and the color of pixel (0,0). Don't swap any file in `assets/images/` without running the tests first to understand what they expect.
- `favicon.png` — 256×256, `#9b2335` at (0,0)
- `favicon-dark.png` — 256×256, `#131313` at (0,0)
- `apple-touch-icon.png` — 1024×1024, `#9b2335` at (0,0)

### Section splitting in validator
The validator uses `re.split(r'\n## ', ...)` to split sections — not `split("##")` — because `##` is a substring of `###` (job-title headers) and would cause false splits.

---

## What NOT to edit manually

- `src/index.template.html` — the HTML template; `convert_resume.py` reads this and writes `index.html`
- `src/resume.template.html` — the PDF template; `convert_resume.py` reads this and writes `resume.html`
- `src/resume.md` — the single source of truth; edit this, not `index.html`
- `index.html` — gitignored, generated by `convert_resume.py` from `src/index.template.html`
- `resume.pdf` — gitignored, generated in CI and deployed via Wrangler
- `public/` — gitignored, transient build artifact
- `src/history.html` — intentional easter egg (design history timeline); leave it alone, don't document it publicly

---

## Test setup note

pytest is at `.venv/bin/pytest` — run `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` if the venv is missing. The Makefile uses `.venv/bin/pytest` automatically via `make test`. `test_pdf.py` requires `resume.pdf` which is gitignored and only generated in CI — all other tests pass locally.

---

## Backlog
- See `.claude/todo.md`

---

## Pre-commit hook gotcha

The pre-commit hook stashes unstaged changes before running, then restores them after the commit completes. Edits to files that weren't explicitly `git add`-ed will NOT be in the commit — they silently survive in the working tree. Always `git add` every file you've edited before committing, not just files you moved or renamed.

---

## Branching

Normally there are no feature branches — this repo works entirely on `main`.

---

## Definition of done

Before any change is considered complete, verify all of the following:

- [ ] `make validate` — passes with no warnings
- [ ] `make test` — all tests pass (`make test` uses `.venv/bin/pytest`)
- [ ] `make build` (or `python3 scripts/build/convert_resume.py --dry-run`) — conversion succeeds cleanly
- [ ] If `src/resume.md` changed: full conversion + local preview look correct
- [ ] If a script changed: run it end-to-end, not just the tests
- [ ] No dead code, no stale comments, no debugging artifacts left behind
- [ ] `resume.pdf` is exactly one page — CI enforces this, but verify locally after any CSS or content change
- [ ] If a new dependency was used anywhere (scripts, tests, CI), it is in `requirements.txt`
- [ ] After pushing, monitor alerts — the pipeline will notify on failure

When in doubt about any item on this list, do not commit — talk first.

---

## Resume format reference

See `docs/EDITING.md` for the full format reference and editing guide.

---

## Build verification

Every build injects the commit SHA and UTC timestamp into `index.html` as two meta tags in `<head>`:

```html
<meta name="build-sha" content="abc1234">
<meta name="build-time" content="2026-02-21T15:30:00Z">
```

These are invisible to visitors but queryable via the browser console (`document.querySelector('meta[name="build-sha"]').content`) or by parsing the live page source.

**Verifying the committed file** (most reliable):

```bash
git pull --no-rebase origin main
grep 'build-sha\|build-time' index.html
```

**Verifying the live site** (curl approach we use in practice):

```bash
curl -s https://tom.irish/ | python3 -c "
import sys
from html.parser import HTMLParser
class P(HTMLParser):
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta' and d.get('name') in ('build-sha', 'build-time'):
            print(d['name'], '=', d['content'])
P().feed(sys.stdin.read())
"
```

Wrangler deploying successfully = site is live. The SHA in `index.html` reflects the commit that triggered the build. When run locally outside of CI, the SHA shows as `local`.

---

## Deployment

- Hosted on Cloudflare Pages, deployed via GitHub Actions + Wrangler on every push to main
- HTTPS handled by Cloudflare
- `src/.well-known/security.txt` — the `Expires` field must be updated annually (currently set to 2027-05-05)
- `GIST_TOKEN` secret — classic PAT with `gist` scope, expires 2027-05-05; stored in password vault; used by nightly workflow to update the Lighthouse badge Gist (`cfcbef4e90b3367512488562c649334e`)
- Secrets: `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` stored in GitHub Actions secrets

---

## Security

### Automated scanning
- **CodeQL** (`.github/workflows/codeql.yml`) — static analysis of Python scripts; runs on every push to main and weekly on Saturdays. Results in GitHub Security → Code scanning alerts. Does not block pushes.
- **Dependabot** (`.github/dependabot.yml`) — opens PRs weekly (Mondays) for outdated GitHub Actions and pip dependencies. Auto-merge is disabled — review and merge manually via `gh pr merge <number> --squash`.
- **pip-audit** — runs in CI on every build and nightly; catches known CVEs in pinned Python dependencies. Separate from CodeQL (which analyzes your code, not your deps).

### Vulnerability reporting
`SECURITY.md` is in the repo root. It directs reporters to GitHub's private vulnerability reporting (already enabled on the repo). Do not add an email address to it.

### Branch protection
- `main` has a GitHub ruleset: force pushes and deletions are blocked.
- No PR requirement — this repo pushes directly to main.

### Auth/ownership checklist
When touching any code that handles auth, sessions, or data access, verify:
- Does this endpoint/function validate the JWT before acting?
- Does it check that the requesting user owns the resource?
- Is user input validated and sanitized before use?
- Could an unauthenticated user reach this path?

---

## CI: Playwright `--with-deps`

`playwright install --with-deps chromium` re-runs apt install on every build even on cache hit (~3.5 min on slow runners). The optimization of skipping `--with-deps` on cache hits was considered and rejected — it relies on the runner image having deps pre-installed rather than Playwright managing them explicitly, which cuts a corner. Leave it as is; slow runners are the exception, not a systematic problem.

---

## history.html

This is an intentional easter egg — not linked from the main site. Image delivery optimizations (srcset, resizing to display dimensions) are explicitly out of scope for it.
