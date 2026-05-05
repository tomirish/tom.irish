#!/usr/bin/env python3
"""
Generate a PDF version of the resume using a headless Chromium browser.

Starts a local HTTP server so all assets (SVG icons, CSS, images) load
correctly, then uses Playwright to load the page and invoke the browser's
native print-to-PDF function. The result is identical to manually choosing
File → Print → Save as PDF in Chrome.

PDF layout is controlled by the constants at the top of this file. Adjust
PDF_MARGIN_* and PDF_SCALE to fit more or less content on a single page.

Usage:
    python3 scripts/generate_pdf_browser.py

Output:
    resume.pdf  (written to the repository root)
"""

from playwright.sync_api import sync_playwright
import http.server
import socketserver
import threading
import time
import sys

# ---------------------------------------------------------------------------
# PDF layout constants — tweak these to adjust the generated PDF appearance.
# ---------------------------------------------------------------------------

# Page format passed to Playwright's page.pdf(). "Letter" = 8.5 × 11 in.
PDF_FORMAT = 'Letter'

# Margins around the printed content.
PDF_MARGIN_TOP = '0.2in'
PDF_MARGIN_RIGHT = '0.2in'
PDF_MARGIN_BOTTOM = '0.2in'
PDF_MARGIN_LEFT = '0.2in'

# Scale factor for the page content. Values < 1.0 shrink the content so more
# fits on one page; 1.0 is 100% (native browser size).
PDF_SCALE = 0.98

# ---------------------------------------------------------------------------
# Server constants
# ---------------------------------------------------------------------------

# Seconds to wait after starting the server before loading the page.
SERVER_START_DELAY = 1

# Seconds of extra wait time after the page reports networkidle,
# to allow fonts and SVGs to finish rendering.
PAGE_RENDER_DELAY = 2

# Timeout in milliseconds to wait for the resume section to become visible.
PAGE_SELECTOR_TIMEOUT_MS = 10_000


def start_local_server():
    """Start a simple HTTP server on an OS-assigned port.

    Binds to port 0 so the OS picks any available port, avoiding conflicts
    with other processes.

    Returns:
        Tuple of (httpd, port) where httpd is the running server instance.
    """
    handler = http.server.SimpleHTTPRequestHandler

    class QuietHTTPServer(socketserver.TCPServer):
        """TCPServer that suppresses per-request error output."""

        allow_reuse_address = True

        def handle_error(self, request, client_address):
            pass  # Suppress connection-reset noise in CI logs

    httpd = QuietHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    print(f'✓ HTTP server started on port {port}')
    return httpd, port


def generate_pdf(port):
    """Load the resume page in headless Chromium and save it as a PDF.

    Args:
        port: Port where the local HTTP server is listening.

    Raises:
        Exception: Re-raises any Playwright error after printing a helpful message.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        url = f'http://localhost:{port}/resume.html'
        print(f'  Loading {url}...')
        page.goto(url)

        # Wait for the network to go idle, then for the DOM to be ready.
        page.wait_for_load_state('networkidle')
        page.wait_for_load_state('domcontentloaded')

        # Wait for the PDF body to confirm content is rendered.
        try:
            page.wait_for_selector(
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

        # Extra delay for fonts and SVGs to finish rendering.
        time.sleep(PAGE_RENDER_DELAY)

        page.pdf(
            path='resume.pdf',
            format=PDF_FORMAT,
            print_background=True,
            prefer_css_page_size=False,
            margin={
                'top': PDF_MARGIN_TOP,
                'right': PDF_MARGIN_RIGHT,
                'bottom': PDF_MARGIN_BOTTOM,
                'left': PDF_MARGIN_LEFT,
            },
            scale=PDF_SCALE,
        )

        browser.close()
        print('✓ PDF generated using browser print (Chromium)')


def main():
    """Entry point: start the HTTP server, generate the PDF, shut down."""
    server = None
    try:
        print('Starting local HTTP server...')
        server, port = start_local_server()
        time.sleep(SERVER_START_DELAY)

        generate_pdf(port)

    except Exception as e:
        print(f'❌ ERROR: PDF generation failed: {e}', file=sys.stderr)
        sys.exit(1)

    finally:
        if server:
            try:
                server.shutdown()
            except Exception:
                pass  # Ignore cleanup errors on exit


if __name__ == '__main__':
    main()
