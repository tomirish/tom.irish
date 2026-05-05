# resume.md Format Reference

`resume.md` is the single source of truth for the website and PDF resume. Edit it, push to `main`, and the site updates automatically within a few minutes.

---

## How the parser works

The build pipeline reads `resume.md` and injects content into the HTML template and PDF. It looks for specific **section markers** (`##` headings) and **entry markers** (`###` headings). The text after those markers is your content — none of it is hardcoded or required to be a specific value.

---

## Required vs optional

### Required sections
These must be present or the build will fail:

| Section | Marker |
|---|---|
| Professional Summary | `## Professional Summary` |
| Work Experience | `## Work Experience` |
| Skills | `## Skills` |
| Education | `## Education` |

### Optional sections
These are recognized if present, ignored if absent:

| Section | Marker |
|---|---|
| Key Achievements | `## Key Achievements` |
| Certifications | `## Certifications` |

### Required header fields
These must appear at the top of the file:

| Field | Format |
|---|---|
| Name | `# Tom Irish` (the `#` heading) |
| Email | `**Email:** [text](mailto:...)` |
| Mobile | `**Mobile:** [text](tel:...)` |
| Website | `**Website:** [text](https://...)` |
| LinkedIn | `**LinkedIn:** [text](https://...)` |
| Location | `**Location:** City, State` |

### Optional header fields

| Field | Format |
|---|---|
| GitHub | `**GitHub:** [text](https://...)` |
| Tagline | `**Tagline:** Plain text (no link)` |

The `Tagline` field populates the short bio line on the landing page, the OG/meta description for social sharing, and the share image. Keep it under ~80 characters so it renders on a single line everywhere.

---

## Section-by-section guide

### Header

```markdown
# Tom Irish

**Email:** [tom@tom.irish](mailto:tom@tom.irish)
**Mobile:** [253-299-4348](tel:2532994348)
**Website:** [tom.irish](https://tom.irish)
**LinkedIn:** [linkedin.com/in/tom-irish](https://linkedin.com/in/tom-irish)
**GitHub:** [github.com/tomirish](https://github.com/tomirish)
**Location:** Seattle, Washington
```

The link text (e.g. `tom@tom.irish`) is what's displayed. The URL in parentheses is where it links. Both can be updated independently.

---

### Professional Summary

```markdown
## Professional Summary

One or more paragraphs. Separate paragraphs with a blank line.
```

---

### Key Achievements

```markdown
## Key Achievements

- First achievement with a specific metric
- Second achievement with a specific metric
```

Plain bullet list. Each bullet is one achievement. Order them however you like — they render in the order written.

---

### Work Experience

```markdown
## Work Experience

### Company - Title (Start Year - End Year)

- Bullet point
- Bullet point

### Company - Title (Start Year - Present)

- Bullet point
```

**Rules:**
- The `###` line must follow the pattern `Company - Title (dates)` exactly
- The date range is always in the last set of parentheses — so titles that contain parentheses are fine: `Manager (Operations)` works correctly
- Add as many jobs as you want, each as a new `###` block
- Add as many bullets as you want under each job
- Entries render in the order written (put most recent first)

**To add a new job:**
```markdown
### New Company - New Title (2027 - Present)

- What you did
- What you achieved
```

---

### Skills

Two formats are supported and can be mixed:

**Grouped (recommended):**
```markdown
- **Category Name:** item one, item two, item three
```

**Flat (simple tag):**
```markdown
- Skill name
```

**Example:**
```markdown
## Skills

- **Reliability & SRE:** SRE, SLA/SLO/SLI, DORA metrics, incident command, OKRs
- **Infrastructure:** Hybrid on-prem/Azure, Nomad, RHEL, DB2/MSSQL/Postgres
- **DevSecOps:** CI/CD, test automation, blue-green deployments, Entra ID
- Leadership
- Strategic Thinking
```

**To add a new skill category:**
```markdown
- **New Category:** skill one, skill two
```

**To add a new flat skill:**
```markdown
- New skill
```

---

### Education

```markdown
## Education

### School Name

- Degree information
- Additional detail if needed

### Another School

- Another degree
```

**Rules:**
- Each `###` is one institution — the text after `###` is the school name
- Bullets under it are the degree(s) and any detail you want shown
- Add as many schools as you want, each as a new `###` block

**To add a second degree from a different school:**
```markdown
### Washington State University

- Bachelor of Arts in Management Information Systems

### University of Washington

- Master of Science in Computer Science
```

**To add a second degree from the same school:**
```markdown
### Washington State University

- Bachelor of Arts in Management Information Systems
- Master of Business Administration
```

---

### Certifications

```markdown
## Certifications

- Certification name — Issuing organization
- Another certification
```

Plain bullet list. Add or remove lines freely. If the section is empty or removed entirely, it won't appear on the site.

---

## Full example

```markdown
# Tom Irish

**Email:** [tom@tom.irish](mailto:tom@tom.irish)
**Mobile:** [253-299-4348](tel:2532994348)
**Website:** [tom.irish](https://tom.irish)
**LinkedIn:** [linkedin.com/in/tom-irish](https://linkedin.com/in/tom-irish)
**GitHub:** [github.com/tomirish](https://github.com/tomirish)
**Location:** Seattle, Washington
**Tagline:** Engineering leader building the systems that keep global freight moving.

---

## Professional Summary

Brief summary paragraph here.

---

## Key Achievements

- Achievement with specific metric
- Achievement with specific metric

---

## Work Experience

### Expeditors - Senior Manager (2025 - Present)

- Led something measurable
- Achieved something specific

### Expeditors - Manager (2016 - 2025)

- Did something impactful

### Expeditors - Earlier Career (2004 - 2016)

- Progressed through Developer, Lead, and Supervisor roles building deep expertise in systems and integration.

---

## Skills

- **Reliability & SRE:** SRE, SLA/SLO/SLI, DORA metrics, incident command, OKRs
- **Infrastructure:** Hybrid on-prem/Azure, Nomad, RHEL
- **DevSecOps:** CI/CD, blue-green deployments, security gates
- Leadership
- Strategic Thinking

---

## Education

### Washington State University

- Bachelor of Arts in Management Information Systems

---

## Certifications

- SAFe Agilist — Scaled Agile
- SAFe DevOps Practitioner — Scaled Agile
- Path Forward Leadership Platform
```

---

## What happens after you push

GitHub Actions runs the following steps in order. If any step fails, the deploy stops and **the live site is unchanged**.

1. **`pip-audit`** — scans Python dependencies for known vulnerabilities
2. **`stylelint`** — lints `src/*.css`
3. **`validate_resume.py`** — fails fast if `resume.md` is missing a required section or has a formatting error
4. **`check_links.py`** — verifies all URLs in `resume.md` are reachable
5. **`convert_resume.py`** — injects content into `src/index.template.html` → produces `index.html`
6. **`generate_pdf_browser.py`** + **`generate_share_image.py`** — run in parallel; headless Chromium renders `resume.pdf`, Pillow generates `assets/images/share.jpg` (the OG preview image)
7. **`pytest tests/`** — verifies the generated files match expected output
8. **Sync to `public/`** — copies `index.html`, `resume.pdf`, `robots.txt`, `sitemap.xml`, `_headers`, `404.html`, `.well-known/security.txt`, and `assets/` into the deploy directory
9. **Wrangler** — deploys `public/` to Cloudflare Pages; site is live within a few minutes
