"""
Unit tests for scripts/convert_resume.py

Focuses on parse_markdown_resume() and parse_summary_paragraphs(), which
contain the core logic including the job-title regex that was previously
vulnerable to parentheses in the title portion.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from bs4 import BeautifulSoup, NavigableString
from convert_resume import parse_markdown_resume, parse_summary_paragraphs, inject_build_info, update_html_with_data

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MINIMAL_RESUME = """\
# Tom Irish

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
    assert len(data['skills']) == 2


def test_skills_content():
    data = parse_markdown_resume(MINIMAL_RESUME)
    assert 'Leadership' in data['skills']
    assert 'Python' in data['skills']


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
# Build info injection
# ---------------------------------------------------------------------------

MINIMAL_HTML = """\
<!DOCTYPE html>
<html>
<head>
<title>Test</title>
</head>
<body></body>
</html>
"""


def _make_soup(html=MINIMAL_HTML):
    return BeautifulSoup(html, 'html.parser')


def test_inject_build_info_adds_meta_tags():
    soup = _make_soup()
    inject_build_info(soup)
    assert soup.find('meta', attrs={'name': 'build-sha'}) is not None
    assert soup.find('meta', attrs={'name': 'build-time'}) is not None


def test_inject_build_info_meta_tags_in_head():
    soup = _make_soup()
    inject_build_info(soup)
    head = soup.find('head')
    sha_tag = head.find('meta', attrs={'name': 'build-sha'})
    time_tag = head.find('meta', attrs={'name': 'build-time'})
    assert sha_tag is not None, 'build-sha meta tag not in <head>'
    assert time_tag is not None, 'build-time meta tag not in <head>'



def test_inject_build_info_local_fallback(monkeypatch):
    """Without GITHUB_SHA set, sha should fall back to 'local'."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    soup = _make_soup()
    sha, _ = inject_build_info(soup)
    assert sha == 'local'
    tag = soup.find('meta', attrs={'name': 'build-sha'})
    assert tag['content'] == 'local'


def test_inject_build_info_truncates_sha(monkeypatch):
    """Full GitHub SHA (40 chars) should be truncated to 7."""
    monkeypatch.setenv('GITHUB_SHA', 'a' * 40)
    soup = _make_soup()
    sha, _ = inject_build_info(soup)
    assert sha == 'aaaaaaa'
    tag = soup.find('meta', attrs={'name': 'build-sha'})
    assert tag['content'] == 'aaaaaaa'


def test_inject_build_info_timestamp_format(monkeypatch):
    """Timestamp should be in ISO 8601 UTC format: YYYY-MM-DDTHH:MM:SSZ."""
    import re
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    soup = _make_soup()
    _, build_time = inject_build_info(soup)
    assert re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', build_time), (
        f"Timestamp '{build_time}' does not match expected format"
    )


def test_inject_build_info_no_head():
    """Should handle missing <head> gracefully without raising."""
    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    sha, build_time = inject_build_info(soup)  # Should not raise
    assert sha is not None
    assert build_time is not None


def test_inject_build_info_does_not_duplicate(monkeypatch):
    """Calling inject_build_info twice should not produce duplicate meta tags."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    soup = _make_soup()
    inject_build_info(soup)
    inject_build_info(soup)

    sha_tags = soup.find_all('meta', attrs={'name': 'build-sha'})
    time_tags = soup.find_all('meta', attrs={'name': 'build-time'})

    assert len(sha_tags) == 1, f"Expected 1 build-sha tag, found {len(sha_tags)}"
    assert len(time_tags) == 1, f"Expected 1 build-time tag, found {len(time_tags)}"


def test_inject_build_info_no_blank_line_accumulation(monkeypatch):
    """Repeated calls must not accumulate blank lines before the build meta tags.

    Each single '\n' between elements is fine; the bug was multiple consecutive
    whitespace-only text nodes piling up (e.g. '\n\n\n\n') with each run.
    """
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    soup = _make_soup()
    inject_build_info(soup)
    inject_build_info(soup)
    inject_build_info(soup)

    head = soup.find('head')
    # Check that no two consecutive children are both whitespace-only text nodes.
    consecutive_blanks = sum(
        1
        for a, b in zip(head.contents, head.contents[1:])
        if isinstance(a, NavigableString) and not a.strip()
        and isinstance(b, NavigableString) and not b.strip()
    )
    assert consecutive_blanks == 0, (
        f"Found {consecutive_blanks} consecutive blank text node pair(s) in <head> "
        "— whitespace is accumulating between inject_build_info calls"
    )


# ---------------------------------------------------------------------------
# HTML generation — h2 and CSS class for job titles
# ---------------------------------------------------------------------------

MINIMAL_HTML_FOR_GENERATION = """\
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<div id="resume-buttons-contact-2">
  <a class="button n02" role="button"><span class="label">Old Location</span></a>
</div>
<p id="resume-text-summary"></p>
<p id="resume-section-work">Work Experience</p>
<hr id="resume-divider-work"/>
<ul id="resume-buttons-skills"></ul>
<p id="resume-section-education">Education</p>
<hr id="resume-divider-education"/>
<p id="resume-text-education-certifications">Certifications</p>
<div id="resume-list-education-certifications"></div>
</body>
</html>
"""


def test_work_experience_generates_h2(monkeypatch):
    """Job title headers should use <h2>, not <h1>."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    data = parse_markdown_resume(MINIMAL_RESUME)
    html_out = update_html_with_data(MINIMAL_HTML_FOR_GENERATION, data)
    soup = BeautifulSoup(html_out, 'html.parser')
    assert not soup.find('h1', class_='style2'), '<h1 class="style2"> should not exist; use <h2>'
    h2_tags = soup.find_all('h2', class_='style2')
    assert len(h2_tags) == 2, f"Expected 2 job title <h2> tags, found {len(h2_tags)}"


def test_work_experience_uses_job_dates_class(monkeypatch):
    """Date spans on job titles should use class 'job-dates', not inline style."""
    monkeypatch.delenv('GITHUB_SHA', raising=False)
    data = parse_markdown_resume(MINIMAL_RESUME)
    html_out = update_html_with_data(MINIMAL_HTML_FOR_GENERATION, data)
    assert 'class="job-dates"' in html_out, "'job-dates' class missing from generated HTML"
    assert 'style="color:' not in html_out and 'style="color :' not in html_out, (
        "Inline color style should not appear in generated HTML"
    )
