"""
Unit tests for scripts/check_links.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts', 'build'))

from check_links import extract_urls


def test_extracts_https_urls():
    content = "See [my site](https://example.com) for details."
    assert extract_urls(content) == ['https://example.com']


def test_extracts_http_urls():
    content = "Visit [here](http://example.com)."
    assert extract_urls(content) == ['http://example.com']


def test_skips_mailto():
    content = "Email [me](mailto:tom@example.com)."
    assert extract_urls(content) == []


def test_skips_tel():
    content = "Call [me](tel:5555555555)."
    assert extract_urls(content) == []


def test_deduplicates_urls():
    content = "[a](https://example.com) and [b](https://example.com)"
    assert extract_urls(content) == ['https://example.com']


def test_preserves_order():
    content = "[a](https://alpha.com) [b](https://beta.com) [c](https://gamma.com)"
    assert extract_urls(content) == ['https://alpha.com', 'https://beta.com', 'https://gamma.com']


def test_multiple_links_in_resume_format():
    content = """\
**Email:** [tom@tom.irish](mailto:tom@tom.irish)
**Website:** [https://tom.irish](https://tom.irish)
**LinkedIn:** [linkedin.com/in/tom-irish](https://linkedin.com/in/tom-irish)
**GitHub:** [github.com/tomirish](https://github.com/tomirish)
"""
    urls = extract_urls(content)
    assert 'https://tom.irish' in urls
    assert 'https://linkedin.com/in/tom-irish' in urls
    assert 'https://github.com/tomirish' in urls
    assert not any(u.startswith('mailto:') for u in urls)


def test_empty_content():
    assert extract_urls('') == []


def test_no_links():
    assert extract_urls('Just plain text with no links.') == []
