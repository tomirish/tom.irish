"""
Tests for static assets and index.html structure.

These tests guard against accidental deletion of asset files, corruption of
the custom CSS section we own in main.css, and removal of the HTML element
IDs that the build pipeline depends on.
"""

import os
import re
import sys

from bs4 import BeautifulSoup

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..')


def read(path):
    with open(os.path.join(REPO_ROOT, path), 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Asset file presence
# ---------------------------------------------------------------------------

EXPECTED_ASSETS = [
    'assets/main.css',
    'assets/main.js',
    'assets/noscript.css',
    'assets/icons.svg',
    'assets/images/favicon.png',
    'assets/images/apple-touch-icon.png',
    'assets/images/share.jpg',
    'assets/images/tom-irish.jpg',
]


def test_asset_files_exist():
    missing = [
        path for path in EXPECTED_ASSETS
        if not os.path.isfile(os.path.join(REPO_ROOT, path))
    ]
    assert not missing, f"Missing asset files: {missing}"


# ---------------------------------------------------------------------------
# Custom CSS section in main.css
# ---------------------------------------------------------------------------

def test_main_css_has_custom_section():
    css = read('assets/main.css')
    assert 'Custom styles' in css, 'Custom styles section missing from main.css'


def test_main_css_scrollbar_hiding():
    css = read('assets/main.css')
    assert '::-webkit-scrollbar' in css, 'WebKit scrollbar rule missing from main.css'
    assert '-ms-overflow-style: none' in css, 'IE scrollbar rule missing from main.css'
    assert 'scrollbar-width: none' in css, 'Firefox scrollbar rule missing from main.css'


def test_main_css_no_print_rule():
    css = read('assets/main.css')
    assert '.no-print' in css, '.no-print rule missing from main.css'


def test_main_css_print_color_adjust():
    css = read('assets/main.css')
    assert 'print-color-adjust: exact' in css, 'print-color-adjust missing from main.css'


def test_main_css_page_margins():
    css = read('assets/main.css')
    assert '@page' in css, '@page rule missing from main.css'


def test_main_css_no_typo_in_units():
    """Catch invalid CSS unit values like '0.25.in' (double period)."""
    css = read('assets/main.css')
    bad_units = re.findall(r'\d+\.\d+\.\w+', css)
    assert not bad_units, f"Invalid CSS unit values found: {bad_units}"


# ---------------------------------------------------------------------------
# index.html required element IDs
# ---------------------------------------------------------------------------

# These IDs must be present in index.html for convert_resume.py to function.
# Mirrors the required_ids list in validate_html_structure() in convert_resume.py.
REQUIRED_IDS = [
    'resume-buttons-contact-2',
    'resume-text-summary',
    'resume-section-work',
    'resume-divider-work',
    'resume-buttons-skills',
    'resume-section-education',
    'resume-divider-education',
    'resume-list-education-certifications',
]


def test_index_html_required_ids_present():
    soup = BeautifulSoup(read('index.html'), 'html.parser')
    missing = [id_ for id_ in REQUIRED_IDS if not soup.find(id=id_)]
    assert not missing, (
        f"index.html is missing required element IDs: {missing}\n"
        "These IDs are required by convert_resume.py. "
        "Do not remove them from index.html."
    )


def test_index_html_has_head():
    soup = BeautifulSoup(read('index.html'), 'html.parser')
    assert soup.find('head') is not None, 'index.html is missing <head>'


def test_index_html_has_footer():
    soup = BeautifulSoup(read('index.html'), 'html.parser')
    assert soup.find(id='footer') is not None, 'index.html is missing <footer id="footer">'


def test_index_html_no_inline_style_blocks_in_body():
    """Styles should live in main.css, not in inline <style> tags in the body."""
    soup = BeautifulSoup(read('index.html'), 'html.parser')
    body = soup.find('body')
    if body:
        inline_styles = body.find_all('style')
        assert not inline_styles, (
            f"Found {len(inline_styles)} inline <style> block(s) in <body>. "
            "CSS belongs in assets/main.css."
        )
