"""
Unit tests for scripts/validate_resume.py
"""

import sys
import os

# Allow importing from the scripts/ directory without installing as a package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validate_resume import validate_resume

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_RESUME = """\
# Tom Irish

**Email:** [tom@tom.irish](mailto:tom@tom.irish)
**Location:** Seattle, Washington

---

## Professional Summary

A summary paragraph.

---

## Work Experience

### ACME Corp - Engineer (2020 - Present)

- Built things
- Fixed things

---

## Skills

- Python
- Leadership

---

## Education

### University of Example

- Bachelor of Science in Computer Science

---

## Certifications

- Some Cert
"""


# ---------------------------------------------------------------------------
# Valid resume
# ---------------------------------------------------------------------------

def test_valid_resume_passes():
    is_valid, warnings, errors = validate_resume(VALID_RESUME)
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert errors == []


# ---------------------------------------------------------------------------
# Required sections
# ---------------------------------------------------------------------------

def test_missing_professional_summary():
    content = VALID_RESUME.replace("## Professional Summary", "## Removed")
    is_valid, warnings, errors = validate_resume(content)
    assert not is_valid
    assert any("Professional Summary" in e for e in errors)


def test_missing_work_experience():
    content = VALID_RESUME.replace("## Work Experience", "## Removed")
    is_valid, warnings, errors = validate_resume(content)
    assert not is_valid
    assert any("Work Experience" in e for e in errors)


def test_missing_skills():
    content = VALID_RESUME.replace("## Skills", "## Removed")
    is_valid, warnings, errors = validate_resume(content)
    assert not is_valid
    assert any("Skills" in e for e in errors)


def test_missing_education():
    content = VALID_RESUME.replace("## Education", "## Removed")
    is_valid, warnings, errors = validate_resume(content)
    assert not is_valid
    assert any("Education" in e for e in errors)


# ---------------------------------------------------------------------------
# Warnings (non-blocking)
# ---------------------------------------------------------------------------

def test_missing_location_warns():
    content = VALID_RESUME.replace("**Location:** Seattle, Washington", "")
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid  # Warnings don't fail validation
    assert any("Location" in w for w in warnings)


def test_no_jobs_warns():
    # Remove job heading but keep the section
    content = VALID_RESUME.replace("### ACME Corp - Engineer (2020 - Present)", "")
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert any("No job entries" in w for w in warnings)


def test_job_without_dates_warns():
    content = VALID_RESUME.replace(
        "### ACME Corp - Engineer (2020 - Present)",
        "### ACME Corp - Engineer"
    )
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert any("missing dates" in w for w in warnings)


def test_tab_character_warns():
    content = VALID_RESUME + "\t- Tabbed item\n"
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert any("tab" in w.lower() for w in warnings)


def test_trailing_whitespace_warns():
    # Insert a line with a single trailing space (not a Markdown hard line break)
    content = VALID_RESUME.replace(
        "A summary paragraph.",
        "A summary paragraph. "  # one trailing space
    )
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert any("trailing whitespace" in w for w in warnings)


def test_double_trailing_space_markdown_linebreak_does_not_warn():
    """Two trailing spaces are valid Markdown hard line break syntax."""
    content = VALID_RESUME.replace(
        "**Email:** [tom@tom.irish](mailto:tom@tom.irish)",
        "**Email:** [tom@tom.irish](mailto:tom@tom.irish)  "  # two trailing spaces
    )
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert not any("trailing whitespace" in w for w in warnings), (
        "Validator should not flag two trailing spaces (Markdown hard line break)"
    )


def test_no_skills_warns():
    # Remove all skill bullets
    content = VALID_RESUME.replace("- Python\n- Leadership", "")
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert any("No skills" in w for w in warnings)


def test_no_schools_warns():
    content = VALID_RESUME.replace("### University of Example", "")
    is_valid, warnings, errors = validate_resume(content)
    assert is_valid
    assert any("No schools" in w for w in warnings)
