#!/usr/bin/env python3
"""
Check that all HTTP/HTTPS links in resume.md are reachable.

Connection errors are treated as failures. HTTP 4xx responses are warnings
(not failures) because some sites like LinkedIn block automated requests.
HTTP 5xx responses are treated as failures.
"""

import os
import re
import sys
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RESUME_PATH = os.path.join(REPO_ROOT, 'src', 'resume.md')
TIMEOUT = 10
LINK_RE = re.compile(r'\[(?:[^\]]*)\]\((https?://[^)]+)\)')


def extract_urls(content):
    """Return a list of unique HTTP/HTTPS URLs found in markdown content."""
    seen = set()
    urls = []
    for url in LINK_RE.findall(content):
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def check_url(url):
    """
    Return (status, error) for a URL.
    status is the HTTP status code, or None on connection error.
    error is a string description on failure, or None on success.
    """
    headers = {'User-Agent': 'tom-irish-link-checker/1.0 (https://github.com/tomirish/tom.irish)'}
    for method in ('HEAD', 'GET'):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status, None
        except urllib.error.HTTPError as e:
            if e.code == 405 and method == 'HEAD':
                continue  # retry with GET
            return e.code, None
        except Exception as e:
            return None, str(e)
    return None, 'all methods failed'


def main():
    with open(RESUME_PATH, encoding='utf-8') as f:
        content = f.read()

    urls = extract_urls(content)
    print(f'Checking {len(urls)} link(s) in {RESUME_PATH}...\n')

    failures = []
    warnings = []

    for url in urls:
        status, error = check_url(url)
        if error:
            print(f'  ✗ {url}  —  {error}')
            failures.append((url, error))
        elif status is not None and 500 <= status < 600:
            print(f'  ✗ {url}  —  HTTP {status}')
            failures.append((url, f'HTTP {status}'))
        elif status is not None and status >= 400:
            print(f'  ⚠ {url}  —  HTTP {status} (may be bot-blocking)')
            warnings.append((url, f'HTTP {status}'))
        else:
            print(f'  ✓ {url}  —  HTTP {status}')

    print()
    if failures:
        print(f'❌ {len(failures)} unreachable link(s). Fix before deploying.')
        sys.exit(1)
    elif warnings:
        print(f'✅ All links reachable ({len(warnings)} warning(s) — likely bot-blocking).')
    else:
        print('✅ All links OK.')


if __name__ == '__main__':
    main()
