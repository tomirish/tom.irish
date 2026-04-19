"""
Tests for static assets and template structure.

Guards against accidental deletion of asset files, and verifies that
both Jinja2 templates contain the expected structural markers.
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
    'assets/images/favicon.png',
    'assets/images/apple-touch-icon.png',
    'assets/images/share.jpg',
    'assets/images/tom-irish-480.jpg',
    'assets/images/tom-irish-480.webp',
    'robots.txt',
    'sitemap.xml',
]

def test_required_assets_exist():
    missing = [p for p in REQUIRED_ASSETS if not exists(p)]
    assert not missing, f"Missing asset files: {missing}"


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
    assert 'fonts.googleapis.com' not in css, 'Google Fonts should be in the HTML template, not main.css'


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


def test_index_template_javascript_limited_to_theme_toggle():
    tmpl = read('index.template.html')
    # JSON-LD and theme-toggle scripts are permitted; no other JS
    script_blocks = re.findall(r'<script([^>]*)>(.*?)</script>', tmpl, re.DOTALL)
    for attrs, content in script_blocks:
        if 'application/ld+json' in attrs:
            continue
        assert 'theme' in content.lower() or 'localStorage' in content, \
            f'Unexpected executable script in index.template.html: {content[:80]}'


def test_index_template_loads_local_fonts():
    tmpl = read('index.template.html')
    assert 'assets/fonts.css' in tmpl, 'Local fonts.css link missing from index.template.html'
    assert 'fonts.googleapis.com' not in tmpl, 'Google Fonts CDN should not be used — fonts are self-hosted'


def test_index_template_has_head():
    tmpl = read('index.template.html')
    assert '<head>' in tmpl, 'index.template.html is missing <head>'


def test_csp_compatible_with_template_stylesheets():
    headers = read('_headers')
    csp_line = next((l for l in headers.splitlines() if 'Content-Security-Policy' in l), '')
    style_src = next(
        (d.strip() for d in csp_line.split(';') if d.strip().startswith('style-src')),
        ''
    )
    allows_inline = not style_src or "'unsafe-inline'" in style_src
    tmpl = read('index.template.html')
    has_inline_styles = '<style>' in tmpl or '<style ' in tmpl
    if not allows_inline:
        assert not has_inline_styles, (
            'index.template.html uses <style> tags but CSP style-src lacks '
            "'unsafe-inline'. Use external stylesheets or update the CSP."
        )


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


def test_resume_template_has_pdf_body():
    tmpl = read('resume.template.html')
    assert 'class="pdf-body"' in tmpl, 'resume.template.html missing class="pdf-body" on <main>'
