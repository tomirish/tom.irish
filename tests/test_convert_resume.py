"""
Unit tests for scripts/convert_resume.py

Focuses on parse_markdown_resume() and parse_summary_paragraphs(), which
contain the core logic including the job-title regex that was previously
vulnerable to parentheses in the title portion.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from convert_resume import parse_markdown_resume, parse_summary_paragraphs

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
