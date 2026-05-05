"""
Unit tests for scripts/convert_resume.py

Covers parse_markdown_resume(), parse_summary_paragraphs(), and
render_templates(). The parser tests include the job-title regex,
grouped skills, Key Achievements, and GitHub field. The rendering
tests verify that both Jinja2 templates produce correct output.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts', 'build'))

from convert_resume import parse_markdown_resume, parse_summary_paragraphs

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MINIMAL_RESUME = """\
# Tom Irish

**Email:** [test@example.com](mailto:test@example.com)
**Mobile:** [555-555-5555](tel:5555555555)
**Website:** [https://example.com](https://example.com)
**LinkedIn:** [linkedin.com/in/test](https://linkedin.com/in/test)
**Location:** Seattle, Washington

---

## Professional Summary

A summary.

---

## Work Experience

### Expeditors - Senior Manager (2025 - Present)

- Led things
- Built things

### Expeditors - Manager (2016 - 2025)

- Managed things

---

## Skills

- Leadership
- Python

---

## Education

### Washington State University

- Bachelor of Arts in MIS

---

## Certifications

- Some Cert
"""


# ---------------------------------------------------------------------------
# Location parsing
# ---------------------------------------------------------------------------

def test_name_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['name'] == 'Tom Irish'


def test_email_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['email']['display'] == 'test@example.com'
    assert data['email']['href'] == 'mailto:test@example.com'


def test_phone_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['phone']['display'] == '555-555-5555'
    assert data['phone']['href'] == 'tel:5555555555'


def test_website_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['website']['display'] == 'https://example.com'
    assert data['website']['href'] == 'https://example.com'


def test_linkedin_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['linkedin']['display'] == 'linkedin.com/in/test'
    assert data['linkedin']['href'] == 'https://linkedin.com/in/test'


def test_location_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['location'] == 'Seattle, Washington'


def test_location_missing():
    content = MINIMAL_RESUME.replace("**Location:** Seattle, Washington", "")
    data = parse_markdown_resume(content)
    assert data['location'] == ''


# ---------------------------------------------------------------------------
# Summary parsing
# ---------------------------------------------------------------------------

def test_summary_single_paragraph():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert len(data['summary']) == 1
    assert 'summary' in data['summary'][0].lower()


def test_summary_multiple_paragraphs():
    content = MINIMAL_RESUME.replace(
        "A summary.",
        "First paragraph.\n\nSecond paragraph."
    )
    data = parse_markdown_resume(content)
    assert len(data['summary']) == 2
    assert data['summary'][0] == 'First paragraph.'
    assert data['summary'][1] == 'Second paragraph.'


def test_parse_summary_paragraphs_empty_input():
    result = parse_summary_paragraphs([])
    assert result == ['']


def test_parse_summary_paragraphs_blank_separator():
    lines = ['Hello world', '', 'Second para']
    result = parse_summary_paragraphs(lines)
    assert result == ['Hello world', 'Second para']


# ---------------------------------------------------------------------------
# Work experience parsing — standard cases
# ---------------------------------------------------------------------------

def test_work_experience_count():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert len(data['work_experience']) == 2


def test_work_experience_title_and_dates():
    data = parse_markdown_resume(MINIMAL_RESUME)
    job = data['work_experience'][0]
    assert job['title'] == 'Expeditors - Senior Manager'
    assert job['dates'] == '2025 - Present'


def test_work_experience_bullets():
    data = parse_markdown_resume(MINIMAL_RESUME)
    job = data['work_experience'][0]
    assert 'Led things' in job['bullets']
    assert 'Built things' in job['bullets']


def test_work_experience_second_job():
    data = parse_markdown_resume(MINIMAL_RESUME)
    job = data['work_experience'][1]
    assert job['title'] == 'Expeditors - Manager'
    assert job['dates'] == '2016 - 2025'
    assert 'Managed things' in job['bullets']


# ---------------------------------------------------------------------------
# Job title parentheses edge case (regression test for the regex fix)
# ---------------------------------------------------------------------------

def test_job_title_with_parentheses_in_name():
    """
    A job title that itself contains parentheses must still parse correctly.
    e.g. "Manager (Operations) - ACME (2020 - 2022)"
         title  = "Manager (Operations) - ACME"
         dates  = "2020 - 2022"
    """
    content = MINIMAL_RESUME.replace(
        "### Expeditors - Senior Manager (2025 - Present)",
        "### Manager (Operations) - ACME (2020 - 2022)"
    )
    data = parse_markdown_resume(content)
    job = data['work_experience'][0]
    assert job['title'] == 'Manager (Operations) - ACME', (
        f"Expected 'Manager (Operations) - ACME', got '{job['title']}'"
    )
    assert job['dates'] == '2020 - 2022', (
        f"Expected '2020 - 2022', got '{job['dates']}'"
    )


def test_job_title_multiple_parentheses_groups():
    """Multiple parenthesized groups in the title; only the last is the date range."""
    content = MINIMAL_RESUME.replace(
        "### Expeditors - Senior Manager (2025 - Present)",
        "### Director (Eng) (Ops) - Corp (2018 - 2023)"
    )
    data = parse_markdown_resume(content)
    job = data['work_experience'][0]
    assert job['dates'] == '2018 - 2023'
    assert '2018 - 2023' not in job['title']


# ---------------------------------------------------------------------------
# Skills parsing
# ---------------------------------------------------------------------------

def test_skills_count():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert len(data['skills']) == 2  # unchanged — still 2 items


def test_skills_content():
    data = parse_markdown_resume(MINIMAL_RESUME)
    flat_labels = [s['label'] for s in data['skills'] if s['type'] == 'flat']
    assert 'Leadership' in flat_labels
    assert 'Python' in flat_labels


# ---------------------------------------------------------------------------
# Education parsing
# ---------------------------------------------------------------------------

def test_education_count():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert len(data['education']) == 1


def test_education_name():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['education'][0]['name'] == 'Washington State University'


def test_education_items():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert 'Bachelor of Arts in MIS' in data['education'][0]['items']


# ---------------------------------------------------------------------------
# Certifications parsing
# ---------------------------------------------------------------------------

def test_certifications():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert 'Some Cert' in data['certifications']


def test_no_certifications():
    content = MINIMAL_RESUME.replace("## Certifications\n\n- Some Cert", "")
    data = parse_markdown_resume(content)
    assert data['certifications'] == []


# ---------------------------------------------------------------------------
# Empty / minimal content
# ---------------------------------------------------------------------------

def test_no_work_experience():
    content = MINIMAL_RESUME.replace(
        "### Expeditors - Senior Manager (2025 - Present)\n\n- Led things\n- Built things\n\n"
        "### Expeditors - Manager (2016 - 2025)\n\n- Managed things",
        ""
    )
    data = parse_markdown_resume(content)
    assert data['work_experience'] == []



# ---------------------------------------------------------------------------
# Extended fixture — includes GitHub, Tagline, Key Achievements, grouped skills
# ---------------------------------------------------------------------------

MINIMAL_RESUME_V2 = """\
# Tom Irish

**Email:** [test@example.com](mailto:test@example.com)
**Mobile:** [555-555-5555](tel:5555555555)
**Website:** [https://example.com](https://example.com)
**LinkedIn:** [linkedin.com/in/test](https://linkedin.com/in/test)
**GitHub:** [github.com/test-user](https://github.com/test-user)
**Location:** Seattle, Washington
**Tagline:** Engineering leader who builds things.

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


def test_tagline_parsed():
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    assert data['tagline'] == 'Engineering leader who builds things.'


def test_tagline_missing_returns_empty():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert data['tagline'] == ''


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


def test_job_title_no_separator_falls_back():
    """Job title with no ' - ' separator sets company and role both to full_title."""
    content = MINIMAL_RESUME.replace(
        "### Expeditors - Senior Manager (2025 - Present)",
        "### SomeCo (2020 - 2022)"
    )
    data = parse_markdown_resume(content)
    job = data['work_experience'][0]
    assert job['company'] == 'SomeCo'
    assert job['role'] == 'SomeCo'
    assert job['title'] == 'SomeCo'


def test_key_achievements_after_work_does_not_drop_last_job():
    """Key Achievements section after Work Experience must not drop the last job."""
    content = """\
# Tom Irish

**Email:** [test@example.com](mailto:test@example.com)
**Mobile:** [555-555-5555](tel:5555555555)
**Website:** [https://example.com](https://example.com)
**LinkedIn:** [linkedin.com/in/test](https://linkedin.com/in/test)
**Location:** Seattle, Washington

---

## Professional Summary

A summary.

---

## Work Experience

### Expeditors - Senior Manager (2025 - Present)

- Led things

## Key Achievements

- An achievement

---

## Skills

- Leadership

---

## Education

### Washington State University

- Bachelor of Arts in MIS
"""
    data = parse_markdown_resume(content)
    assert len(data['work_experience']) == 1
    assert data['work_experience'][0]['title'] == 'Expeditors - Senior Manager'
    assert len(data['achievements']) == 1
    assert 'An achievement' in data['achievements']


# ---------------------------------------------------------------------------
# Jinja2 rendering tests
# ---------------------------------------------------------------------------

def test_render_index_html_contains_name(tmp_path, monkeypatch):
    """Rendered index.html should contain the person's name."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'index.html').read_text()
    assert 'Tom Irish' in html


def test_render_resume_html_contains_name(tmp_path, monkeypatch):
    """Rendered resume.html (PDF template) should contain the person's name."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'resume.html').read_text()
    assert 'Tom Irish' in html


def test_render_index_html_contains_build_meta(tmp_path, monkeypatch):
    """Rendered index.html should have build-sha and build-time meta tags."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'index.html').read_text()
    assert 'name="build-sha"' in html
    assert 'name="build-time"' in html


def test_render_index_html_json_ld_is_valid(tmp_path, monkeypatch):
    """JSON-LD block in rendered index.html must be valid JSON."""
    import json
    import re
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'index.html').read_text()
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match, 'No JSON-LD script block found in rendered index.html'
    try:
        json.loads(match.group(1))
    except json.JSONDecodeError as e:
        raise AssertionError(f'JSON-LD block is not valid JSON: {e}')


def test_render_index_html_og_tags_have_content(tmp_path, monkeypatch):
    """OG meta tags in rendered index.html must have non-empty content."""
    import re
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    from convert_resume import render_templates
    data = parse_markdown_resume(MINIMAL_RESUME_V2)
    render_templates(data, index_out=str(tmp_path / 'index.html'),
                     resume_out=str(tmp_path / 'resume.html'))
    html = (tmp_path / 'index.html').read_text()
    for prop in ('og:title', 'og:description', 'og:image', 'og:url'):
        match = re.search(rf'property="{re.escape(prop)}"\s+content="([^"]*)"', html)
        assert match, f'Missing OG tag: {prop}'
        assert match.group(1).strip(), f'OG tag {prop} has empty content'
