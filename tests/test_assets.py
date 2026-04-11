"""
Tests for static assets and index.html structure.

These tests guard against accidental deletion of asset files, regression in
the CSS design tokens, and removal of the key structural sections in the
Jinja2 templates.
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
    'assets/pdf.css',
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
# main.css design tokens and structure
# ---------------------------------------------------------------------------

def test_main_css_accent_color():
    css = read('assets/main.css')
    assert '#9b2335' in css, 'Accent color #9b2335 missing from main.css'


def test_main_css_css_target_toggle():
    css = read('assets/main.css')
    assert '#resume:target' in css, 'CSS :target section toggle missing from main.css'


def test_main_css_no_external_resources():
    """main.css must not reference external URLs (no Google Fonts, no CDN)."""
    css = read('assets/main.css')
    assert '@import' not in css, 'main.css must not @import external resources'


def test_main_css_no_typo_in_units():
    """Catch invalid CSS unit values like '0.25.in' (double period)."""
    css = read('assets/main.css')
    bad_units = re.findall(r'\d+\.\d+\.\w+', css)
    assert not bad_units, f"Invalid CSS unit values found: {bad_units}"


# ---------------------------------------------------------------------------
# pdf.css design tokens
# ---------------------------------------------------------------------------

def test_pdf_css_print_color_adjust():
    css = read('assets/pdf.css')
    assert 'print-color-adjust: exact' in css, 'print-color-adjust missing from pdf.css'


def test_pdf_css_accent_color():
    css = read('assets/pdf.css')
    assert '#9b2335' in css, 'Accent color #9b2335 missing from pdf.css'


# ---------------------------------------------------------------------------
# index.template.html structural sections
# ---------------------------------------------------------------------------

def test_index_html_has_home_section():
    soup = BeautifulSoup(read('index.template.html'), 'html.parser')
    assert soup.find(id='home') is not None, 'index.template.html is missing <section id="home">'


def test_index_html_has_resume_section():
    soup = BeautifulSoup(read('index.template.html'), 'html.parser')
    assert soup.find(id='resume') is not None, 'index.template.html is missing <section id="resume">'


def test_index_html_has_head():
    soup = BeautifulSoup(read('index.template.html'), 'html.parser')
    assert soup.find('head') is not None, 'index.template.html is missing <head>'


def test_index_html_links_main_css():
    soup = BeautifulSoup(read('index.template.html'), 'html.parser')
    link = soup.find('link', {'rel': 'stylesheet', 'href': 'assets/main.css'})
    assert link is not None, 'index.template.html must link to assets/main.css'


def test_index_html_no_inline_style_blocks_in_body():
    """Styles should live in main.css, not in inline <style> tags in the body."""
    soup = BeautifulSoup(read('index.template.html'), 'html.parser')
    body = soup.find('body')
    if body:
        inline_styles = body.find_all('style')
        assert not inline_styles, (
            f"Found {len(inline_styles)} inline <style> block(s) in <body>. "
            "CSS belongs in assets/main.css."
        )


# ---------------------------------------------------------------------------
# resume.template.html structural sections
# ---------------------------------------------------------------------------

def test_resume_template_exists():
    assert os.path.isfile(os.path.join(REPO_ROOT, 'resume.template.html')), \
        'resume.template.html does not exist'


def test_resume_template_links_pdf_css():
    soup = BeautifulSoup(read('resume.template.html'), 'html.parser')
    link = soup.find('link', {'rel': 'stylesheet', 'href': 'assets/pdf.css'})
    assert link is not None, 'resume.template.html must link to assets/pdf.css'


def test_resume_template_has_header():
    soup = BeautifulSoup(read('resume.template.html'), 'html.parser')
    assert soup.find('header') is not None, 'resume.template.html is missing <header>'
