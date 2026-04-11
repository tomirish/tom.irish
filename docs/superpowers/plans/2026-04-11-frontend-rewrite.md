# Frontend Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Carrd-generated JS/CSS with clean hand-written code, switch the build pipeline from BeautifulSoup injection to Jinja2 templating, add a separate PDF template, and extend `resume.md` with Key Achievements and grouped skills.

**Architecture:** `resume.md` → `convert_resume.py` (Jinja2) → `index.html` (web) + `resume.html` (PDF input) → `generate_pdf_browser.py` → `resume.pdf`. The web template uses CSS `:target` for zero-JS section toggling. The PDF template is a separate, print-optimized Jinja2 template.

**Tech Stack:** Python 3.9+, Jinja2, Playwright (PDF), pytest. No BeautifulSoup, no Google Fonts, no JS.

**Branch:** `frontend-rewrite` — do NOT merge to main until all tasks complete and verified.

**Run tests with:** `/Users/tom/Library/Python/3.9/bin/pytest tests/ -v`

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `resume.md` | Modify | Content — single source of truth |
| `scripts/validate_resume.py` | Modify | Validate resume.md structure |
| `scripts/convert_resume.py` | Rewrite | Parse resume.md, render both Jinja2 templates |
| `index.template.html` | Rewrite | Jinja2 web template — landing + resume sections |
| `resume.template.html` | Create | Jinja2 PDF template — print-optimized, single column |
| `assets/main.css` | Rewrite | All web styles — responsive, CSS :target toggle |
| `assets/pdf.css` | Create | Print styles for PDF template |
| `assets/main.js` | Delete | Obsolete |
| `assets/noscript.css` | Delete | Obsolete |
| `requirements.txt` | Modify | Remove beautifulsoup4, add jinja2 |
| `tests/test_convert_resume.py` | Rewrite | Parser tests + Jinja2 rendering tests |
| `tests/test_assets.py` | Rewrite | Updated asset/template structure checks |
| `tests/test_validate_resume.py` | Modify | Add tests for new sections and grouped skills |

---

## Task 1: Update resume.md structure

**Files:**
- Modify: `resume.md`

Add the GitHub field, Key Achievements section, and convert Skills to grouped format. Use placeholder content for Key Achievements — Tom will fill in real content separately.

- [ ] **Step 1: Update resume.md**

Replace the entire file with this structure (preserve existing Summary, Work Experience, Education, Certifications content exactly):

```markdown
# Tom Irish

**Email:** [tom@tom.irish](mailto:tom@tom.irish)  
**Mobile:** [253-299-4348](tel:2532994348)  
**Website:** [tom.irish](https://tom.irish)  
**LinkedIn:** [linkedin.com/in/tom-irish](https://linkedin.com/in/tom-irish)  
**GitHub:** [github.com/tom-irish](https://github.com/tom-irish)  
**Location:** Seattle, Washington

---

## Professional Summary

I am a dynamic and motivated leader with over 20 years of experience in information services and logistics, specializing in customer integration solutions. With a proven track record of enhancing customer experience through seamless integrations and managing systems that handle over a billion transactions annually, I bring a wealth of expertise to any organization.

My expertise includes leading multiple high-performing agile teams, leveraging microservices architecture with continuous integration and continuous deployment pipelines. My goal is to inspire my teams to reach their full potential in a collaborative and inclusive environment, focusing on coaching, mentoring, and fostering continuous innovation and growth.

As a data-driven decision-maker, I am passionate about leveraging technology to solve complex problems. I successfully manage a $10 million budget, optimizing resources, reducing costs, and planning for the future. My commitment to delivering results-based customer service and continuous improvement is unwavering.

---

## Key Achievements

- Placeholder — add metric-driven achievement here
- Placeholder — add metric-driven achievement here

---

## Work Experience

### Expeditors - Senior Manager (2025 - Present)

- Spearheaded the development and optimization of new systems infrastructure, retiring legacy systems to enhance customer integration efficiency, facilitating over a billion transactions annually.
- Led cross-functional teams in implementing DevSecOps and agile methodologies, increasing system efficiency by 20% and reducing operational costs by 5%.
- Cultivated a high-performance culture through continuous coaching and mentoring, increasing team productivity by 25% and fostering professional growth.

### Expeditors - Manager (2016 - 2025)

- Pioneered customized integration solutions, consistently exceeding customer expectations by delivering exceptional onboarding experiences.
- Directed multiple high-impact projects, ensuring on-time delivery and achieving a 90% success rate.
- Developed and implemented comprehensive training programs, enhancing team skills and fostering a culture of continuous improvement.

---

## Skills

- **Leadership & Management:** Leadership, Strategic Thinking, Coaching and Mentoring, Financial Management
- **Engineering Practices:** Agile Development, DevSecOps, Project Management, Creative Problem-Solving
- **Soft Skills:** Communication, Customer Service

---

## Education

### Washington State University

- Bachelor of Arts in Management Information Systems

---

## Certifications

- Path Forward - Leadership Platform Course
- Scaled Agile - Leading SAFe Agilist Certified
```

- [ ] **Step 2: Validate the file parses cleanly with existing validator**

```bash
python3 scripts/validate_resume.py
```

Expected: passes (Key Achievements is an unknown section — validator ignores unknown sections, so no errors. Grouped skills are just bullets with bold text — pass as-is until Task 2 adds awareness of them.)

- [ ] **Step 3: Commit**

```bash
git add resume.md
git commit -m "feat: add GitHub field, Key Achievements, grouped skills to resume.md"
```

---

## Task 2: Update validate_resume.py

**Files:**
- Modify: `scripts/validate_resume.py`
- Modify: `tests/test_validate_resume.py`

Add recognition of Key Achievements (optional), grouped skill format, and GitHub field.

- [ ] **Step 1: Write failing tests for new validation behavior**

Add to `tests/test_validate_resume.py`:

```python
# Add to the VALID_RESUME fixture at the top — add GitHub field and Key Achievements:
VALID_RESUME_WITH_NEW_SECTIONS = """\
# Tom Irish

**Email:** [tom@tom.irish](mailto:tom@tom.irish)
**GitHub:** [github.com/tom-irish](https://github.com/tom-irish)
**Location:** Seattle, Washington

---

## Professional Summary

A summary paragraph.

---

## Key Achievements

- Reduced costs by 38%
- Improved uptime to 99.5%

---

## Work Experience

### ACME Corp - Engineer (2020 - Present)

- Built things

---

## Skills

- **Reliability:** SRE, DORA metrics, incident command
- **Infrastructure:** Azure, Nomad, RHEL
- Leadership

---

## Education

### University of Example

- Bachelor of Science in Computer Science
"""


def test_key_achievements_section_is_valid():
    """Key Achievements is a recognized optional section — should not cause errors or warnings."""
    is_valid, warnings, errors = validate_resume(VALID_RESUME_WITH_NEW_SECTIONS)
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert errors == []


def test_grouped_skills_are_valid():
    """Skills formatted as '- **Label:** item, item' should pass without warnings."""
    is_valid, warnings, errors = validate_resume(VALID_RESUME_WITH_NEW_SECTIONS)
    assert is_valid
    skill_warnings = [w for w in warnings if 'skill' in w.lower()]
    assert not skill_warnings, f"Unexpected skill warnings: {skill_warnings}"


def test_github_field_no_warning():
    """GitHub field in header should not generate warnings."""
    is_valid, warnings, errors = validate_resume(VALID_RESUME_WITH_NEW_SECTIONS)
    assert is_valid
    github_warnings = [w for w in warnings if 'github' in w.lower()]
    assert not github_warnings, f"Unexpected GitHub warnings: {github_warnings}"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_validate_resume.py -v -k "new_sections or grouped_skills or github"
```

Expected: FAIL — the new test functions don't exist yet / validation doesn't know about these sections.

- [ ] **Step 3: Update validate_resume.py**

In `scripts/validate_resume.py`, update the `validate_resume` function. The only changes needed are:
1. Recognize `## Key Achievements` as a known optional section (so it doesn't need to be listed as unknown)
2. Count grouped skills (`- **Label:** ...`) as valid skills in the Skills section check

Find this block in `validate_resume`:
```python
    # Check skills section
    skills_section = content.split("## Skills")
    if len(skills_section) > 1:
        skills_content = re.split(r'\n## ', skills_section[1])[0]
        skill_count = len(re.findall(r'^[-*] ', skills_content, re.MULTILINE))
        if skill_count == 0:
            warnings.append("No skills found in Skills section")
```

This already works — `- **Label:** items` starts with `- ` so it's counted. No change needed for skills.

The only real change is ensuring no spurious warning is generated for Key Achievements. Check: does the current validator warn about unknown sections? Looking at the code — it doesn't. It only validates specific known sections. So Key Achievements is silently ignored already.

Run the tests to verify:

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_validate_resume.py -v
```

Expected: all PASS (existing tests plus new ones — the new sections already pass through validation cleanly).

- [ ] **Step 4: Commit**

```bash
git add tests/test_validate_resume.py scripts/validate_resume.py
git commit -m "test: add validation tests for Key Achievements, grouped skills, GitHub field"
```

---

## Task 3: Extend the markdown parser

**Files:**
- Modify: `scripts/convert_resume.py`
- Modify: `tests/test_convert_resume.py`

Add parsing for: `github` contact field, `achievements` section, grouped skills format. Add `company`/`role` split to job entries.

- [ ] **Step 1: Write failing parser tests**

Add to `tests/test_convert_resume.py` (keep all existing tests, add these below):

```python
# ---------------------------------------------------------------------------
# Updated MINIMAL_RESUME with new fields (used in new tests only)
# ---------------------------------------------------------------------------

MINIMAL_RESUME_V2 = """\
# Tom Irish

**Email:** [test@example.com](mailto:test@example.com)
**Mobile:** [555-555-5555](tel:5555555555)
**Website:** [https://example.com](https://example.com)
**LinkedIn:** [linkedin.com/in/test](https://linkedin.com/in/test)
**GitHub:** [github.com/test-user](https://github.com/test-user)
**Location:** Seattle, Washington

---

## Professional Summary

A summary.

---

## Key Achievements

- Reduced costs by 38%
- Improved uptime to 99.5%

---

## Work Experience

### Expeditors - Senior Manager (2025 - Present)

- Led things

---

## Skills

- **Reliability:** SRE, DORA metrics
- **Infrastructure:** Azure, Nomad
- Leadership

---

## Education

### Washington State University

- Bachelor of Arts in MIS

---

## Certifications

- Some Cert
"""


def test_github_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    assert data['github']['display'] == 'github.com/test-user'
    assert data['github']['href'] == 'https://github.com/test-user'


def test_github_missing_returns_empty():
    data = parse_markdown_resume(MINIMAL_RESUME)  # original fixture, no GitHub field
    assert data['github']['display'] == ''
    assert data['github']['href'] == ''


def test_achievements_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    assert len(data['achievements']) == 2
    assert 'Reduced costs by 38%' in data['achievements']
    assert 'Improved uptime to 99.5%' in data['achievements']


def test_achievements_missing_returns_empty():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['achievements'] == []


def test_grouped_skill_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    groups = [s for s in data['skills'] if s['type'] == 'group']
    assert len(groups) == 2
    reliability = next(g for g in groups if g['label'] == 'Reliability')
    assert 'SRE' in reliability['items']
    assert 'DORA metrics' in reliability['items']


def test_flat_skill_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    flats = [s for s in data['skills'] if s['type'] == 'flat']
    assert len(flats) == 1
    assert flats[0]['label'] == 'Leadership'


def test_job_company_and_role_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    job = data['work_experience'][0]
    assert job['company'] == 'Expeditors'
    assert job['role'] == 'Senior Manager'


def test_job_company_role_title_remains():
    """Original 'title' field kept for backward compatibility."""
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    job = data['work_experience'][0]
    assert job['title'] == 'Expeditors - Senior Manager'
```

Also update these two **existing** tests in `tests/test_convert_resume.py` which will break when skills changes from a list of strings to a list of dicts:

```python
def test_skills_count():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert len(data['skills']) == 2  # unchanged — still 2 items


def test_skills_content():
    data = parse_markdown_resume(MINIMAL_RESUME)
    flat_labels = [s['label'] for s in data['skills'] if s['type'] == 'flat']
    assert 'Leadership' in flat_labels
    assert 'Python' in flat_labels
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_convert_resume.py -v -k "github or achievements or grouped or company_and_role or company_role_title"
```

Expected: FAIL — `KeyError: 'github'`, `KeyError: 'achievements'`, `'type'` not in skills dict, `'company'`/`'role'` not in job dict.

- [ ] **Step 3: Update parse_markdown_resume in convert_resume.py**

Replace the `data` dict initialization and update the parsing logic. Edit `scripts/convert_resume.py`:

**Change 1 — update data dict initialization** (around line 61):
```python
    data = {
        'name': '',
        'email': {'display': '', 'href': ''},
        'phone': {'display': '', 'href': ''},
        'website': {'display': '', 'href': ''},
        'linkedin': {'display': '', 'href': ''},
        'github': {'display': '', 'href': ''},   # NEW
        'location': '',
        'summary': [],
        'achievements': [],                        # NEW
        'work_experience': [],
        'skills': [],
        'education': [],
        'certifications': []
    }
```

**Change 2 — add GitHub parsing** (after the LinkedIn block, around line 104):
```python
        elif '**GitHub:**' in line:
            m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
            if m and urlparse(m.group(2)).scheme in ALLOWED_URL_SCHEMES:
                data['github'] = {'display': m.group(1), 'href': m.group(2)}
```

**Change 3 — add Key Achievements section detection** (in the section header block, after the Certifications block, around line 144):
```python
        elif line_stripped == '## Key Achievements':
            current_section = 'achievements'
            print(f"  🏆 Parsing Key Achievements (line {line_num})")
```

**Change 4 — add achievements to bullet handling** (in the bullet point block, around line 183):
```python
            elif current_section == 'achievements':
                data['achievements'].append(bullet)
```

**Change 5 — update skills parsing** to detect grouped format. Replace the skills bullet handling:
```python
            elif current_section == 'skills':
                # Detect grouped skill: "- **Label:** item, item, item"
                group_match = re.match(r'^\*\*([^*]+):\*\*\s*(.+)$', bullet)
                if group_match:
                    label = group_match.group(1).strip()
                    items = [i.strip() for i in group_match.group(2).split(',') if i.strip()]
                    data['skills'].append({'type': 'group', 'label': label, 'items': items})
                else:
                    data['skills'].append({'type': 'flat', 'label': bullet})
```

**Change 6 — add company/role split to job parsing** (in the job title parsing block, around line 158):
```python
            if match:
                full_title = match.group(1).strip()
                # Split "Company - Role" into separate fields
                if ' - ' in full_title:
                    title_parts = full_title.split(' - ', 1)
                    company = title_parts[0].strip()
                    role = title_parts[1].strip()
                else:
                    company = full_title
                    role = full_title
                current_job = {
                    'title': full_title,   # kept for backward compat
                    'company': company,
                    'role': role,
                    'dates': match.group(2).strip(),
                    'bullets': []
                }
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_convert_resume.py -v
```

Expected: all PASS (including all existing tests — none of the existing behavior changed).

- [ ] **Step 5: Commit**

```bash
git add scripts/convert_resume.py tests/test_convert_resume.py
git commit -m "feat: extend parser with GitHub, Key Achievements, grouped skills, company/role split"
```

---

## Task 4: Switch convert_resume.py to Jinja2

**Files:**
- Modify: `scripts/convert_resume.py`
- Modify: `requirements.txt`

Remove BeautifulSoup rendering, add Jinja2 rendering. The markdown parser (`parse_markdown_resume`) is unchanged. Only the `update_html_with_data` / `validate_html_structure` functions are replaced with Jinja2 rendering.

- [ ] **Step 1: Install Jinja2 and update requirements.txt**

```bash
pip3 install jinja2
```

Edit `requirements.txt` — remove `beautifulsoup4` line, add `jinja2`:

```
jinja2==3.1.6
playwright==1.58.0
pygments==2.20.0
pypdf==6.9.2
pytest==8.4.2
```

Verify the installed version:
```bash
python3 -c "import jinja2; print(jinja2.__version__)"
```

- [ ] **Step 2: Write failing rendering test**

Add to `tests/test_convert_resume.py`:

```python
# ---------------------------------------------------------------------------
# Jinja2 rendering tests
# ---------------------------------------------------------------------------

def test_render_index_html_contains_name(tmp_path, monkeypatch):
    """Rendered index.html should contain the person's name."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    monkeypatch.chdir(os.path.join(os.path.dirname(__file__), '..'))
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'index.html').read_text()
    assert 'Tom Irish' in html


def test_render_resume_html_contains_name(tmp_path, monkeypatch):
    """Rendered resume.html (PDF template) should contain the person's name."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    monkeypatch.chdir(os.path.join(os.path.dirname(__file__), '..'))
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'resume.html').read_text()
    assert 'Tom Irish' in html


def test_render_index_html_contains_build_meta(tmp_path, monkeypatch):
    """Rendered index.html should have build-sha and build-time meta tags."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    monkeypatch.chdir(os.path.join(os.path.dirname(__file__), '..'))
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'index.html').read_text()
    assert 'name="build-sha"' in html
    assert 'name="build-time"' in html
```

Run to confirm failure:
```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_convert_resume.py -v -k "render"
```

Expected: FAIL — `render_templates` not defined yet, and templates don't exist yet.

- [ ] **Step 3: Rewrite convert_resume.py**

Replace `scripts/convert_resume.py` entirely with this:

```python
#!/usr/bin/env python3
"""
Convert resume.md to HTML using Jinja2 templates.

Reads resume.md (single source of truth) and renders two Jinja2 templates:
  - index.template.html  → index.html  (web site)
  - resume.template.html → resume.html (PDF input for generate_pdf_browser.py)

Usage:
    python3 scripts/convert_resume.py            # writes both HTML files
    python3 scripts/convert_resume.py --dry-run  # parse only, no files written
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
ALLOWED_URL_SCHEMES = {'http', 'https', 'mailto', 'tel'}


def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: Could not read {filepath}: {e}")
        sys.exit(1)


def write_file(filepath, content, dry_run=False):
    if dry_run:
        print(f"🔍 DRY RUN: Would write {len(content)} bytes to {filepath} (skipped)")
        return
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Wrote {len(content)} bytes to {filepath}")
    except Exception as e:
        print(f"❌ ERROR: Could not write {filepath}: {e}")
        sys.exit(1)


def _parse_link(line):
    """Extract display text and href from a markdown link on a line."""
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
    if m and urlparse(m.group(2)).scheme in ALLOWED_URL_SCHEMES:
        return {'display': m.group(1), 'href': m.group(2)}
    return {'display': '', 'href': ''}


def parse_markdown_resume(md_content):
    """Parse resume.md into a structured dict for template rendering."""
    lines = md_content.split('\n')
    data = {
        'name': '',
        'email': {'display': '', 'href': ''},
        'phone': {'display': '', 'href': ''},
        'website': {'display': '', 'href': ''},
        'linkedin': {'display': '', 'href': ''},
        'github': {'display': '', 'href': ''},
        'location': '',
        'summary': [],
        'achievements': [],
        'work_experience': [],
        'skills': [],
        'education': [],
        'certifications': [],
    }

    current_section = None
    current_job = None
    current_school = None
    summary_lines = []

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        # Name
        if line.startswith('# ') and not data['name']:
            data['name'] = line[2:].strip()

        # Contact fields
        elif '**Email:**' in line:
            data['email'] = _parse_link(line)
        elif '**Mobile:**' in line:
            data['phone'] = _parse_link(line)
        elif '**Website:**' in line:
            data['website'] = _parse_link(line)
        elif '**LinkedIn:**' in line:
            data['linkedin'] = _parse_link(line)
        elif '**GitHub:**' in line:
            data['github'] = _parse_link(line)
        elif '**Location:**' in line:
            m = re.search(r'\*\*Location:\*\*\s*(.+)', line)
            if m:
                data['location'] = m.group(1).strip()

        # Section headers — finalize any in-progress job/school first
        elif stripped == '## Professional Summary':
            current_section = 'summary'
            summary_lines = []
        elif stripped == '## Key Achievements':
            current_section = 'achievements'
            if summary_lines:
                data['summary'] = _parse_paragraphs(summary_lines)
        elif stripped == '## Work Experience':
            current_section = 'work'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
            if summary_lines:
                data['summary'] = _parse_paragraphs(summary_lines)
        elif stripped == '## Skills':
            current_section = 'skills'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
        elif stripped == '## Education':
            current_section = 'education'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
        elif stripped == '## Certifications':
            current_section = 'certifications'
            if current_school:
                data['education'].append(current_school)
                current_school = None

        # Job entries
        elif current_section == 'work' and line.startswith('### '):
            if current_job:
                data['work_experience'].append(current_job)
            job_line = line[4:].strip()
            match = re.match(r'^(.*\S)\s*\(([^)]+)\)\s*$', job_line)
            if match:
                full_title = match.group(1).strip()
                if ' - ' in full_title:
                    parts = full_title.split(' - ', 1)
                    company, role = parts[0].strip(), parts[1].strip()
                else:
                    company = role = full_title
                current_job = {
                    'title': full_title,
                    'company': company,
                    'role': role,
                    'dates': match.group(2).strip(),
                    'bullets': [],
                }
            else:
                print(f"  ⚠️  Warning (line {line_num}): Job entry missing dates: {job_line}")

        # Education entries
        elif current_section == 'education' and line.startswith('### '):
            if current_school:
                data['education'].append(current_school)
            current_school = {'name': line[4:].strip(), 'items': []}

        # Bullets
        elif line.startswith('- ') or line.startswith('* '):
            bullet = line[2:].strip()
            if current_section == 'work' and current_job:
                current_job['bullets'].append(bullet)
            elif current_section == 'achievements':
                data['achievements'].append(bullet)
            elif current_section == 'skills':
                group_match = re.match(r'^\*\*([^*]+):\*\*\s*(.+)$', bullet)
                if group_match:
                    label = group_match.group(1).strip()
                    items = [i.strip() for i in group_match.group(2).split(',') if i.strip()]
                    data['skills'].append({'type': 'group', 'label': label, 'items': items})
                else:
                    data['skills'].append({'type': 'flat', 'label': bullet})
            elif current_section == 'certifications':
                data['certifications'].append(bullet)
            elif current_section == 'education' and current_school:
                current_school['items'].append(bullet)

        # Summary paragraphs
        elif current_section == 'summary':
            if stripped and not line.startswith('#') and not stripped.startswith('---') and not line.startswith('**'):
                summary_lines.append(stripped)
            elif not stripped and summary_lines and summary_lines[-1] != '':
                summary_lines.append('')

    # Finalize trailing items
    if current_job:
        data['work_experience'].append(current_job)
    if current_school:
        data['education'].append(current_school)
    if summary_lines and not data['summary']:
        data['summary'] = _parse_paragraphs(summary_lines)

    return data


def _parse_paragraphs(lines):
    """Split summary lines into paragraphs on blank lines."""
    paragraphs, current = [], []
    for line in lines:
        if line == '':
            if current:
                paragraphs.append(' '.join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(' '.join(current))
    return paragraphs if paragraphs else ['']


# Keep old name as alias so existing tests importing parse_summary_paragraphs still work
parse_summary_paragraphs = _parse_paragraphs


def _build_info():
    """Return (sha, build_time) for template injection."""
    sha = os.environ.get('GITHUB_SHA', 'local')
    if sha != 'local':
        sha = sha[:7]
    build_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return sha, build_time


def render_templates(data, index_out='index.html', resume_out='resume.html', dry_run=False):
    """Render both Jinja2 templates with resume data and write output files."""
    env = Environment(loader=FileSystemLoader(REPO_ROOT), autoescape=True)
    sha, build_time = _build_info()

    context = {**data, 'build_sha': sha, 'build_time': build_time}

    index_tmpl = env.get_template('index.template.html')
    write_file(index_out, index_tmpl.render(**context), dry_run=dry_run)

    resume_tmpl = env.get_template('resume.template.html')
    write_file(resume_out, resume_tmpl.render(**context), dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser(description='Convert resume.md to HTML.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Parse and validate without writing files.')
    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - no files will be written\n")

    print("🚀 Starting resume conversion...\n")

    md_content = read_file(os.path.join(REPO_ROOT, 'resume.md'))
    print("📊 Parsing resume.md...")
    data = parse_markdown_resume(md_content)

    print("\n🔄 Rendering templates...")
    render_templates(
        data,
        index_out=os.path.join(REPO_ROOT, 'index.html'),
        resume_out=os.path.join(REPO_ROOT, 'resume.html'),
        dry_run=args.dry_run,
    )

    print("\n" + "=" * 50)
    print("✨ DRY RUN COMPLETE" if args.dry_run else "✨ SUCCESS")
    print("=" * 50)
    print(f"  👤 Name: {data['name'] or '(not set)'}")
    print(f"  📍 Location: {data['location'] or '(not set)'}")
    print(f"  📝 Summary: {len(data['summary'])} paragraph(s)")
    print(f"  🏆 Key Achievements: {len(data['achievements'])} item(s)")
    print(f"  💼 Work Experience: {len(data['work_experience'])} job(s)")
    print(f"  🛠️  Skills: {len(data['skills'])} item(s)")
    print(f"  🎓 Education: {len(data['education'])} school(s)")
    print(f"  📜 Certifications: {len(data['certifications'])} item(s)")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run all existing parser tests to confirm they still pass**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_convert_resume.py -v -k "not render"
```

Expected: all PASS. The rendering tests will still fail (templates not written yet) — that's expected.

- [ ] **Step 5: Commit**

```bash
git add scripts/convert_resume.py requirements.txt
git commit -m "refactor: switch convert_resume.py from BeautifulSoup to Jinja2"
```

---

## Task 5: Write index.template.html

**Files:**
- Rewrite: `index.template.html`

The web Jinja2 template. Replaces the Carrd HTML entirely. CSS `:target` toggle, no JS.

- [ ] **Step 1: Write index.template.html**

Replace the entire file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="color-scheme" content="light"/>
  <meta name="description" content="{{ name }} — Seattle-based engineering leader"/>
  <meta property="og:title" content="{{ name }}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{{ website.href }}"/>
  <meta property="og:description" content="{{ name }} — Seattle-based engineering leader"/>
  <meta property="og:image" content="{{ website.href }}/assets/images/share.jpg"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="build-sha" content="{{ build_sha }}"/>
  <meta name="build-time" content="{{ build_time }}"/>
  <link rel="canonical" href="{{ website.href }}"/>
  <link rel="icon" href="assets/images/favicon.png" type="image/png"/>
  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png"/>
  <link rel="stylesheet" href="assets/main.css"/>
  <title>{{ name }}</title>
</head>
<body>

  <!-- ═══════════════════════════════════════════ LANDING -->
  <section id="home">
    <div class="landing-inner">
      <div class="landing-photo">
        <img src="assets/images/tom-irish.jpg" alt="{{ name }}"/>
      </div>
      <h1 class="landing-name">{{ name }}</h1>
      <p class="landing-location">{{ location }}</p>
      <nav class="icon-links" aria-label="Contact links">
        {% if email.href %}
        <a class="icon-link" href="{{ email.href }}" title="Email" aria-label="Email">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        </a>
        {% endif %}
        {% if phone.href %}
        <a class="icon-link" href="{{ phone.href }}" title="Phone" aria-label="Phone">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
        </a>
        {% endif %}
        {% if linkedin.href %}
        <a class="icon-link" href="{{ linkedin.href }}" title="LinkedIn" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14m-.5 15.5v-5.3a3.26 3.26 0 00-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 011.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 001.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 00-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
        </a>
        {% endif %}
        {% if github.href %}
        <a class="icon-link" href="{{ github.href }}" title="GitHub" aria-label="GitHub" target="_blank" rel="noopener noreferrer">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 002 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/></svg>
        </a>
        {% endif %}
        <a class="icon-link primary" href="#resume" title="Resume" aria-label="View Resume">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zm-1 1.5L18.5 9H13V3.5zM6 20V4h5v7h7v9H6z"/></svg>
        </a>
      </nav>
    </div>
  </section>

  <!-- ═══════════════════════════════════════════ RESUME -->
  <section id="resume">
    <nav class="resume-nav" aria-label="Resume navigation">
      <a class="resume-back" href="#home">← Back</a>
      <a class="resume-pdf" href="resume.pdf" target="_blank">↓ PDF Resume</a>
    </nav>

    <header class="resume-header">
      <div class="resume-photo">
        <img src="assets/images/tom-irish.jpg" alt="{{ name }}"/>
      </div>
      <div class="resume-header-text">
        <h2 class="resume-name">{{ name }}</h2>
        <div class="contact-pills">
          {% if email.href %}<a class="contact-pill" href="{{ email.href }}">{{ email.display }}</a>{% endif %}
          {% if phone.href %}<a class="contact-pill" href="{{ phone.href }}">{{ phone.display }}</a>{% endif %}
          {% if website.href %}<a class="contact-pill" href="{{ website.href }}" target="_blank" rel="noopener noreferrer">{{ website.display }}</a>{% endif %}
          {% if linkedin.href %}<a class="contact-pill" href="{{ linkedin.href }}" target="_blank" rel="noopener noreferrer">{{ linkedin.display }}</a>{% endif %}
          {% if github.href %}<a class="contact-pill" href="{{ github.href }}" target="_blank" rel="noopener noreferrer">{{ github.display }}</a>{% endif %}
          {% if location %}<span class="contact-pill">{{ location }}</span>{% endif %}
        </div>
      </div>
    </header>

    <div class="resume-body">
      <main class="resume-main">

        {% if summary %}
        <h3 class="section-heading">Professional Summary</h3>
        <hr class="section-rule"/>
        <div class="summary-text">
          {% for para in summary %}<p>{{ para }}</p>{% endfor %}
        </div>
        {% endif %}

        {% if achievements %}
        <h3 class="section-heading">Key Achievements</h3>
        <hr class="section-rule"/>
        <ul class="achievements-list">
          {% for item in achievements %}<li>{{ item }}</li>{% endfor %}
        </ul>
        {% endif %}

        {% if work_experience %}
        <h3 class="section-heading">Work Experience</h3>
        <hr class="section-rule"/>
        {% for job in work_experience %}
        <div class="job">
          <div class="job-header">
            <span class="job-title">{{ job.role }}</span>
            <span class="job-dates">{{ job.dates }}</span>
          </div>
          <div class="job-company">{{ job.company }}</div>
          <ul class="job-bullets">
            {% for bullet in job.bullets %}<li>{{ bullet }}</li>{% endfor %}
          </ul>
        </div>
        {% endfor %}
        {% endif %}

      </main>

      <aside class="resume-sidebar">

        {% if skills %}
        <h3 class="section-heading">Skills</h3>
        <hr class="section-rule"/>
        {% for skill in skills %}
          {% if skill.type == 'group' %}
          <div class="skill-group">
            <div class="skill-group-label">{{ skill.label }}</div>
            <div class="skill-tags">
              {% for item in skill.items %}<span class="skill-tag">{{ item }}</span>{% endfor %}
            </div>
          </div>
          {% else %}
          <div class="skill-tags"><span class="skill-tag">{{ skill.label }}</span></div>
          {% endif %}
        {% endfor %}
        {% endif %}

        {% if education %}
        <h3 class="section-heading">Education</h3>
        <hr class="section-rule"/>
        {% for school in education %}
        <div class="edu-entry">
          <div class="edu-name">{{ school.name }}</div>
          {% for item in school.items %}<div class="edu-item">{{ item }}</div>{% endfor %}
        </div>
        {% endfor %}
        {% endif %}

        {% if certifications %}
        <h3 class="section-heading">Certifications</h3>
        <hr class="section-rule"/>
        {% for cert in certifications %}
        <div class="cert-item">{{ cert }}</div>
        {% endfor %}
        {% endif %}

      </aside>
    </div>
  </section>

</body>
</html>
```

- [ ] **Step 2: Run the dry-run to confirm template renders without error**

```bash
python3 scripts/convert_resume.py --dry-run
```

Expected: succeeds, no errors. (resume.template.html doesn't exist yet so it will fail — that's Task 6. If it errors on the resume template, that's expected. Focus on confirming the index template parses without Jinja2 syntax errors.)

- [ ] **Step 3: Commit**

```bash
git add index.template.html
git commit -m "feat: rewrite index.template.html as Jinja2 web template"
```

---

## Task 6: Write assets/main.css

**Files:**
- Rewrite: `assets/main.css`

Complete responsive stylesheet. CSS `:target` section toggle. No external resources.

- [ ] **Step 1: Write assets/main.css**

Replace the entire file:

```css
/* ── RESET & BASE ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #111;
  background: #fff;
  line-height: 1.5;
}

a { color: inherit; text-decoration: none; }
img { display: block; max-width: 100%; }

/* ── SECTION TOGGLE (CSS :target, zero JS) ────────────────── */
#home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 48px 24px;
  border-top: 4px solid #9b2335;
}

#resume { display: none; }
#resume:target { display: block; }
:root:has(#resume:target) #home { display: none; }
#home:target { display: flex; }

/* ── LANDING ──────────────────────────────────────────────── */
.landing-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.landing-photo {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #eee;
}
.landing-photo img { width: 100%; height: 100%; object-fit: cover; }

.landing-name {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.4px;
  text-align: center;
}

.landing-location {
  font-size: 11px;
  color: #999;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  text-align: center;
  margin-top: -4px;
}

.icon-links {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 8px;
}

.icon-link {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1.5px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #555;
  transition: border-color 0.15s, color 0.15s;
}
.icon-link:hover { border-color: #9b2335; color: #9b2335; }
.icon-link.primary {
  background: #9b2335;
  border-color: #9b2335;
  color: #fff;
}
.icon-link svg { width: 18px; height: 18px; fill: currentColor; }

/* ── RESUME NAV ───────────────────────────────────────────── */
.resume-nav {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 32px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
  border-top: 4px solid #9b2335;
}

.resume-back {
  font-size: 12px;
  font-weight: 600;
  color: #9b2335;
}
.resume-back:hover { text-decoration: underline; }

.resume-pdf {
  font-size: 12px;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 4px 14px;
}
.resume-pdf:hover { border-color: #9b2335; color: #9b2335; }

/* ── RESUME HEADER ────────────────────────────────────────── */
.resume-header {
  display: flex;
  gap: 24px;
  align-items: center;
  padding: 28px 32px 24px;
  border-bottom: 1px solid #eee;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.resume-photo {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  overflow: hidden;
  border: 2.5px solid #eee;
  flex-shrink: 0;
}
.resume-photo img { width: 100%; height: 100%; object-fit: cover; }

.resume-name {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.3px;
  margin-bottom: 10px;
}

.contact-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.contact-pill {
  font-size: 11px;
  color: #444;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 3px 12px;
  white-space: nowrap;
}
a.contact-pill:hover { border-color: #9b2335; color: #9b2335; }

/* ── RESUME BODY (two column) ─────────────────────────────── */
.resume-body {
  display: grid;
  grid-template-columns: 1fr 280px;
  max-width: 1000px;
  margin: 0 auto;
}

.resume-main { padding: 28px 32px; border-right: 1px solid #f0f0f0; }
.resume-sidebar { padding: 28px 24px; background: #fafafa; }

/* ── SECTION HEADINGS ─────────────────────────────────────── */
.section-heading {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  color: #9b2335;
  margin-top: 24px;
  margin-bottom: 6px;
}
.resume-main .section-heading:first-child,
.resume-sidebar .section-heading:first-child { margin-top: 0; }

.section-rule {
  border: none;
  border-top: 1px solid #eee;
  margin-bottom: 14px;
}

/* ── SUMMARY ──────────────────────────────────────────────── */
.summary-text { font-size: 13px; line-height: 1.7; color: #333; }
.summary-text p + p { margin-top: 10px; }

/* ── KEY ACHIEVEMENTS ─────────────────────────────────────── */
.achievements-list { list-style: none; }
.achievements-list li {
  font-size: 13px;
  color: #333;
  padding-left: 16px;
  position: relative;
  margin-bottom: 6px;
  line-height: 1.55;
}
.achievements-list li::before {
  content: "–";
  position: absolute;
  left: 0;
  color: #9b2335;
  font-weight: 600;
}

/* ── WORK EXPERIENCE ──────────────────────────────────────── */
.job { margin-bottom: 20px; }

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 2px;
}

.job-title { font-size: 14px; font-weight: 700; color: #111; }
.job-dates { font-size: 11px; color: #999; white-space: nowrap; }
.job-company { font-size: 12px; color: #555; margin-bottom: 8px; }

.job-bullets { list-style: none; }
.job-bullets li {
  font-size: 12.5px;
  color: #333;
  padding-left: 16px;
  position: relative;
  margin-bottom: 5px;
  line-height: 1.55;
}
.job-bullets li::before {
  content: "–";
  position: absolute;
  left: 0;
  color: #9b2335;
}

/* ── SKILLS ───────────────────────────────────────────────── */
.skill-group { margin-bottom: 14px; }

.skill-group-label {
  font-size: 10px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 5px;
}

.skill-tags { display: flex; flex-wrap: wrap; gap: 5px; }

.skill-tag {
  font-size: 11px;
  color: #333;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 3px 10px;
}

/* ── EDUCATION ────────────────────────────────────────────── */
.edu-entry { margin-bottom: 16px; }
.edu-name { font-size: 13px; font-weight: 600; color: #111; margin-bottom: 4px; }
.edu-item { font-size: 12px; color: #555; }

/* ── CERTIFICATIONS ───────────────────────────────────────── */
.cert-item {
  font-size: 12px;
  color: #444;
  padding-left: 14px;
  position: relative;
  margin-bottom: 6px;
  line-height: 1.5;
}
.cert-item::before {
  content: "–";
  position: absolute;
  left: 0;
  color: #9b2335;
}

/* ── RESPONSIVE ───────────────────────────────────────────── */
@media (max-width: 767px) {
  .resume-nav { padding: 12px 20px; }
  .resume-header { padding: 20px 20px 16px; gap: 16px; }
  .resume-body { grid-template-columns: 1fr; }
  .resume-main { padding: 20px; border-right: none; }
  .resume-sidebar { padding: 20px; background: #fff; border-top: 1px solid #eee; }
}

@media (max-width: 479px) {
  .resume-photo { width: 56px; height: 56px; }
  .resume-name { font-size: 18px; }
  .icon-link { width: 34px; height: 34px; }
  .icon-link svg { width: 16px; height: 16px; }
}
```

- [ ] **Step 2: Preview locally**

```bash
python3 scripts/convert_resume.py --dry-run
python3 -m http.server 8000
```

Open http://localhost:8000 in browser. Check:
- Landing section shows centered card with photo, name, location, icon links
- Clicking the Resume icon navigates to `#resume` and shows resume section
- Back link returns to landing
- On narrow viewport (resize browser to <768px), resume collapses to single column

- [ ] **Step 3: Commit**

```bash
git add assets/main.css
git commit -m "feat: write main.css — responsive styles, CSS :target toggle, no JS"
```

---

## Task 7: Write resume.template.html and assets/pdf.css

**Files:**
- Create: `resume.template.html`
- Create: `assets/pdf.css`

PDF-only Jinja2 template. Single column, print-optimized. No landing section, no nav.

- [ ] **Step 1: Write resume.template.html**

Create `resume.template.html` in the repo root:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link rel="stylesheet" href="assets/pdf.css"/>
  <title>{{ name }} — Resume</title>
</head>
<body>

  <header class="pdf-header">
    <div class="pdf-photo">
      <img src="assets/images/tom-irish.jpg" alt="{{ name }}"/>
    </div>
    <div class="pdf-header-text">
      <h1 class="pdf-name">{{ name }}</h1>
      <div class="pdf-contact">
        {% if email.display %}<span>{{ email.display }}</span>{% endif %}
        {% if phone.display %}<span>{{ phone.display }}</span>{% endif %}
        {% if website.display %}<span>{{ website.display }}</span>{% endif %}
        {% if linkedin.display %}<span>{{ linkedin.display }}</span>{% endif %}
        {% if github.display %}<span>{{ github.display }}</span>{% endif %}
        {% if location %}<span>{{ location }}</span>{% endif %}
      </div>
    </div>
  </header>

  <main class="pdf-body">

    {% if summary %}
    <section class="pdf-section">
      <h2 class="pdf-section-heading">Professional Summary</h2>
      <hr class="pdf-rule"/>
      {% for para in summary %}<p class="pdf-summary">{{ para }}</p>{% endfor %}
    </section>
    {% endif %}

    {% if achievements %}
    <section class="pdf-section">
      <h2 class="pdf-section-heading">Key Achievements</h2>
      <hr class="pdf-rule"/>
      <ul class="pdf-bullets">
        {% for item in achievements %}<li>{{ item }}</li>{% endfor %}
      </ul>
    </section>
    {% endif %}

    {% if work_experience %}
    <section class="pdf-section">
      <h2 class="pdf-section-heading">Work Experience</h2>
      <hr class="pdf-rule"/>
      {% for job in work_experience %}
      <div class="pdf-job">
        <div class="pdf-job-header">
          <strong class="pdf-job-title">{{ job.role }}</strong>
          <span class="pdf-job-dates">{{ job.dates }}</span>
        </div>
        <div class="pdf-job-company">{{ job.company }}</div>
        <ul class="pdf-bullets">
          {% for bullet in job.bullets %}<li>{{ bullet }}</li>{% endfor %}
        </ul>
      </div>
      {% endfor %}
    </section>
    {% endif %}

    {% if skills %}
    <section class="pdf-section">
      <h2 class="pdf-section-heading">Skills</h2>
      <hr class="pdf-rule"/>
      {% for skill in skills %}
        {% if skill.type == 'group' %}
        <div class="pdf-skill-row">
          <span class="pdf-skill-label">{{ skill.label }}:</span>
          <span class="pdf-skill-items">{{ skill.items | join(', ') }}</span>
        </div>
        {% else %}
        <div class="pdf-skill-row"><span class="pdf-skill-items">{{ skill.label }}</span></div>
        {% endif %}
      {% endfor %}
    </section>
    {% endif %}

    {% if education %}
    <section class="pdf-section">
      <h2 class="pdf-section-heading">Education</h2>
      <hr class="pdf-rule"/>
      {% for school in education %}
      <div class="pdf-edu">
        <strong>{{ school.name }}</strong>
        {% for item in school.items %}<div class="pdf-edu-item">{{ item }}</div>{% endfor %}
      </div>
      {% endfor %}
    </section>
    {% endif %}

    {% if certifications %}
    <section class="pdf-section">
      <h2 class="pdf-section-heading">Certifications</h2>
      <hr class="pdf-rule"/>
      <ul class="pdf-bullets">
        {% for cert in certifications %}<li>{{ cert }}</li>{% endfor %}
      </ul>
    </section>
    {% endif %}

  </main>
</body>
</html>
```

- [ ] **Step 2: Write assets/pdf.css**

Create `assets/pdf.css`:

```css
/* PDF / print stylesheet — loaded only by resume.template.html */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 11px;
  color: #111;
  background: #fff;
  line-height: 1.5;
  padding: 0;
}

a { color: inherit; text-decoration: none; }
img { display: block; }

/* Header */
.pdf-header {
  display: flex;
  gap: 18px;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 2px solid #eee;
}

.pdf-photo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #eee;
  flex-shrink: 0;
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
}
.pdf-photo img { width: 100%; height: 100%; object-fit: cover; }

.pdf-name {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.3px;
  margin-bottom: 5px;
}

.pdf-contact {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 14px;
  font-size: 10px;
  color: #555;
}
.pdf-contact span::before { content: ""; }

/* Body */
.pdf-body { }

.pdf-section { margin-bottom: 12px; }

.pdf-section-heading {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #9b2335;
  margin-bottom: 4px;
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
}

.pdf-rule {
  border: none;
  border-top: 1px solid #eee;
  margin-bottom: 8px;
}

.pdf-summary {
  font-size: 11px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 5px;
}

/* Bullets */
.pdf-bullets { list-style: none; }
.pdf-bullets li {
  font-size: 11px;
  color: #333;
  padding-left: 12px;
  position: relative;
  margin-bottom: 3px;
  line-height: 1.5;
}
.pdf-bullets li::before {
  content: "–";
  position: absolute;
  left: 0;
  color: #9b2335;
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
}

/* Jobs */
.pdf-job { margin-bottom: 10px; }
.pdf-job-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1px;
}
.pdf-job-title { font-size: 12px; font-weight: 700; }
.pdf-job-dates { font-size: 10px; color: #999; }
.pdf-job-company { font-size: 10.5px; color: #555; margin-bottom: 5px; }

/* Skills */
.pdf-skill-row { margin-bottom: 4px; font-size: 11px; }
.pdf-skill-label { font-weight: 600; color: #333; margin-right: 4px; }
.pdf-skill-items { color: #444; }

/* Education */
.pdf-edu { margin-bottom: 8px; font-size: 11px; }
.pdf-edu-item { color: #555; margin-top: 2px; }

@media print {
  body { padding: 0; }
  .pdf-section { page-break-inside: avoid; }
}
```

- [ ] **Step 3: Run the full conversion to confirm both templates render**

```bash
python3 scripts/convert_resume.py
```

Expected: "✨ SUCCESS", both `index.html` and `resume.html` written.

- [ ] **Step 4: Preview resume.html locally**

```bash
python3 -m http.server 8000
```

Open http://localhost:8000/resume.html — should show the resume content single-column, clean and print-ready.

- [ ] **Step 5: Commit**

```bash
git add resume.template.html assets/pdf.css
git commit -m "feat: add resume.template.html and pdf.css for PDF generation"
```

---

## Task 8: Update generate_pdf_browser.py

**Files:**
- Modify: `scripts/generate_pdf_browser.py`

Load `resume.html` directly instead of `index.html#resume`. Update the selector to wait for the right element.

- [ ] **Step 1: Edit generate_pdf_browser.py**

Change the URL and selector in the `generate_pdf` function:

```python
        url = f'http://localhost:{port}/resume.html'  # was: /index.html#resume
        print(f'  Loading {url}...')
        page.goto(url)

        page.wait_for_load_state('networkidle')
        page.wait_for_load_state('domcontentloaded')

        try:
            page.wait_for_selector(          # was: '#resume-section'
                '.pdf-body',
                state='visible',
                timeout=PAGE_SELECTOR_TIMEOUT_MS,
            )
        except Exception:
            print(
                '  ⚠️  Warning: .pdf-body not visible within '
                f'{PAGE_SELECTOR_TIMEOUT_MS / 1000:.0f}s — continuing anyway. '
                'The PDF may be incomplete.'
            )
```

- [ ] **Step 2: Generate the PDF**

```bash
python3 scripts/convert_resume.py
python3 scripts/generate_pdf_browser.py
```

Expected: `resume.pdf` written to repo root, no errors.

- [ ] **Step 3: Verify PDF is one page**

```bash
python3 -c "
import pypdf
r = pypdf.PdfReader('resume.pdf')
print(f'Pages: {len(r.pages)}')
assert len(r.pages) == 1, f'Expected 1 page, got {len(r.pages)}'
print('✅ PDF is exactly one page')
"
```

Expected: `Pages: 1`, `✅ PDF is exactly one page`

If PDF is more than one page, adjust `PDF_SCALE` in `generate_pdf_browser.py` (try `0.85` or `0.80`) and re-run until it fits.

- [ ] **Step 4: Commit**

```bash
git add scripts/generate_pdf_browser.py
git commit -m "feat: update PDF generator to load resume.html directly"
```

---

## Task 9: Rewrite test_assets.py

**Files:**
- Rewrite: `tests/test_assets.py`

Remove references to deleted files (`main.js`, `noscript.css`), old IDs, and Carrd-specific CSS. Add checks for new file structure.

- [ ] **Step 1: Write the new test_assets.py**

Replace the entire file:

```python
"""
Tests for static assets and template structure.

Guards against accidental deletion of asset files, and verifies that
both Jinja2 templates contain the expected template variables.
"""

import os
import re

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..')


def read(path):
    with open(os.path.join(REPO_ROOT, path), 'r', encoding='utf-8') as f:
        return f.read()


def exists(path):
    return os.path.isfile(os.path.join(REPO_ROOT, path))


# ---------------------------------------------------------------------------
# Asset file presence
# ---------------------------------------------------------------------------

REQUIRED_ASSETS = [
    'assets/main.css',
    'assets/pdf.css',
    'assets/icons.svg',
    'assets/images/favicon.png',
    'assets/images/apple-touch-icon.png',
    'assets/images/share.jpg',
    'assets/images/tom-irish.jpg',
]

DELETED_ASSETS = [
    'assets/main.js',
    'assets/noscript.css',
]


def test_required_assets_exist():
    missing = [p for p in REQUIRED_ASSETS if not exists(p)]
    assert not missing, f"Missing asset files: {missing}"


def test_deleted_assets_are_gone():
    still_present = [p for p in DELETED_ASSETS if exists(p)]
    assert not still_present, f"These files should have been deleted: {still_present}"


# ---------------------------------------------------------------------------
# main.css checks
# ---------------------------------------------------------------------------

def test_main_css_has_target_toggle():
    css = read('assets/main.css')
    assert '#resume:target' in css, 'CSS :target toggle rule missing from main.css'


def test_main_css_has_accent_color():
    css = read('assets/main.css')
    assert '#9b2335' in css, 'Accent color #9b2335 missing from main.css'


def test_main_css_no_google_fonts():
    css = read('assets/main.css')
    assert 'fonts.googleapis.com' not in css, 'Google Fonts reference found in main.css'


def test_main_css_responsive_breakpoint():
    css = read('assets/main.css')
    assert '@media' in css, 'No responsive media queries in main.css'


def test_main_css_no_typo_in_units():
    css = read('assets/main.css')
    bad_units = re.findall(r'\d+\.\d+\.\w+', css)
    assert not bad_units, f"Invalid CSS unit values found: {bad_units}"


# ---------------------------------------------------------------------------
# index.template.html checks
# ---------------------------------------------------------------------------

def test_index_template_has_jinja_variables():
    tmpl = read('index.template.html')
    assert '{{ name }}' in tmpl, 'Jinja2 {{ name }} variable missing from index.template.html'
    assert '{{ build_sha }}' in tmpl, 'Jinja2 {{ build_sha }} variable missing'
    assert '{{ build_time }}' in tmpl, 'Jinja2 {{ build_time }} variable missing'


def test_index_template_has_home_and_resume_sections():
    tmpl = read('index.template.html')
    assert 'id="home"' in tmpl, 'Landing section id="home" missing from index.template.html'
    assert 'id="resume"' in tmpl, 'Resume section id="resume" missing from index.template.html'


def test_index_template_no_javascript():
    tmpl = read('index.template.html')
    assert '<script' not in tmpl, 'Script tag found in index.template.html — should have zero JS'


def test_index_template_no_google_fonts():
    tmpl = read('index.template.html')
    assert 'fonts.googleapis.com' not in tmpl, 'Google Fonts link found in index.template.html'


def test_index_template_has_head():
    tmpl = read('index.template.html')
    assert '<head>' in tmpl, 'index.template.html is missing <head>'


# ---------------------------------------------------------------------------
# resume.template.html checks
# ---------------------------------------------------------------------------

def test_resume_template_exists():
    assert exists('resume.template.html'), 'resume.template.html does not exist'


def test_resume_template_has_jinja_variables():
    tmpl = read('resume.template.html')
    assert '{{ name }}' in tmpl, 'Jinja2 {{ name }} variable missing from resume.template.html'


def test_resume_template_no_javascript():
    tmpl = read('resume.template.html')
    assert '<script' not in tmpl, 'Script tag found in resume.template.html'
```

- [ ] **Step 2: Run the new tests**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_assets.py -v
```

Expected: all PASS. If any fail, the file/template they reference needs to exist (check Tasks 5–7 are done first).

- [ ] **Step 3: Commit**

```bash
git add tests/test_assets.py
git commit -m "test: rewrite test_assets.py for new file structure"
```

---

## Task 10: Update test_convert_resume.py

**Files:**
- Modify: `tests/test_convert_resume.py`

Remove BeautifulSoup imports and injection tests (they test deleted code). Keep all parser tests. Add rendering tests. The rendering tests were already written in Task 4 — just verify they now pass.

- [ ] **Step 1: Remove obsolete imports and tests**

In `tests/test_convert_resume.py`:

1. Remove this import at the top:
   ```python
   from bs4 import BeautifulSoup, NavigableString
   ```

2. Remove the import line:
   ```python
   from convert_resume import parse_markdown_resume, parse_summary_paragraphs, inject_build_info, update_html_with_data
   ```
   Replace with:
   ```python
   from convert_resume import parse_markdown_resume, parse_summary_paragraphs, render_templates
   ```

3. Remove these entire test functions and their fixtures (they tested BeautifulSoup injection that no longer exists):
   - `MINIMAL_HTML` constant and `_make_soup` helper
   - `test_inject_build_info_adds_meta_tags`
   - `test_inject_build_info_meta_tags_in_head`
   - `test_inject_build_info_local_fallback`
   - `test_inject_build_info_truncates_sha`
   - `test_inject_build_info_timestamp_format`
   - `test_inject_build_info_no_head`
   - `test_inject_build_info_does_not_duplicate`
   - `test_inject_build_info_no_blank_line_accumulation`
   - `MINIMAL_HTML_FOR_GENERATION` constant
   - `test_work_experience_generates_h2`
   - `test_work_experience_uses_job_dates_class`

- [ ] **Step 2: Run all tests to confirm passing**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/test_convert_resume.py -v
```

Expected: all PASS. The rendering tests added in Task 4 should now pass since both templates exist.

- [ ] **Step 3: Commit**

```bash
git add tests/test_convert_resume.py
git commit -m "test: remove BeautifulSoup injection tests, keep and verify parser + rendering tests"
```

---

## Task 11: Delete obsolete files and update .gitignore

**Files:**
- Delete: `assets/main.js`
- Delete: `assets/noscript.css`
- Modify: `.gitignore`

- [ ] **Step 1: Delete obsolete files**

```bash
git rm assets/main.js assets/noscript.css
```

- [ ] **Step 2: Add resume.html to .gitignore**

Add `resume.html` to `.gitignore` (it's a build artifact like `index.html`):

Open `.gitignore` and add `resume.html` next to the `index.html` line:
```
index.html
resume.html
```

- [ ] **Step 3: Run full test suite**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/ -v
```

Expected: all pass. `test_deleted_assets_are_gone` in `test_assets.py` will now confirm `main.js` and `noscript.css` are gone.

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: delete main.js and noscript.css, add resume.html to .gitignore"
```

---

## Task 12: End-to-end verification

Run every item in the definition of done before considering this complete.

- [ ] **Step 1: Run validate**

```bash
python3 scripts/validate_resume.py
```

Expected: `✅ VALIDATION PASSED` with no warnings.

- [ ] **Step 2: Run dry-run conversion**

```bash
python3 scripts/convert_resume.py --dry-run
```

Expected: `✨ DRY RUN COMPLETE`.

- [ ] **Step 3: Run full conversion**

```bash
python3 scripts/convert_resume.py
```

Expected: `✨ SUCCESS`, `index.html` and `resume.html` written.

- [ ] **Step 4: Run all tests**

```bash
/Users/tom/Library/Python/3.9/bin/pytest tests/ -v
```

Expected: all PASS.

- [ ] **Step 5: Generate PDF**

```bash
python3 scripts/generate_pdf_browser.py
```

Verify `resume.pdf` is one page:
```bash
python3 -c "
import pypdf
r = pypdf.PdfReader('resume.pdf')
assert len(r.pages) == 1, f'Expected 1 page, got {len(r.pages)}'
print(f'✅ PDF: {len(r.pages)} page')
"
```

- [ ] **Step 6: Preview at multiple viewports**

```bash
python3 -m http.server 8000
```

Check http://localhost:8000 at:
- **375px wide** (mobile): landing card centered, icon links wrap if needed; resume collapses to single column
- **768px wide** (tablet): resume two-column layout activates
- **1440px wide** (desktop): two-column, centered, max-width kicks in
- **Resume section**: Back link and PDF button in nav bar
- **No JS**: confirm browser devtools shows zero JS loaded

- [ ] **Step 7: Verify no forbidden assets in generated HTML**

```bash
python3 -c "
html = open('index.html').read()
checks = [
    ('main.js', 'main.js should not be in index.html'),
    ('noscript.css', 'noscript.css should not be in index.html'),
    ('fonts.googleapis.com', 'Google Fonts should not be in index.html'),
]
for term, msg in checks:
    assert term not in html, f'FAIL: {msg}'
    print(f'✅ {term} not found')
"
```

- [ ] **Step 8: Final commit if any loose ends**

If any small fixes were made during verification:
```bash
git add -p  # stage only what's needed
git commit -m "fix: end-to-end verification fixes"
```

---

## Spec Coverage Check

| Spec requirement | Covered by |
|---|---|
| Zero JavaScript | Task 5 (template), Task 6 (CSS :target), Task 9 (test) |
| No external resources | Task 6 (CSS), Task 5 (template), Task 9 (test) |
| Responsive all screens | Task 6 (CSS breakpoints), Task 12 (manual verify) |
| CSS :target section toggle | Task 6 |
| Deep crimson #9b2335 accent | Task 6, Task 7 |
| System font stack | Task 6 |
| Circular photo 96px landing / 72px resume | Task 6 |
| 5 icon links (Email, Phone, LinkedIn, GitHub, Resume) | Task 5 |
| Two-column resume (65/35) | Task 6 |
| Key Achievements in main column | Task 5 |
| Grouped skills in sidebar | Task 5 |
| Separate PDF template | Task 7 |
| PDF template single column, print-optimized | Task 7 |
| generate_pdf loads resume.html | Task 8 |
| GitHub contact field | Task 3, Task 5 |
| Jinja2 replaces BeautifulSoup | Task 4 |
| resume.html gitignored | Task 11 |
| All tests pass | Task 12 |
| PDF exactly one page | Task 8, Task 12 |
