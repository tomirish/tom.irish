#!/usr/bin/env python3
"""
Generate PDF using Playwright (headless browser) - same as manual browser print.
"""

from playwright.sync_api import sync_playwright
import http.server
import socketserver
import threading
import time
import sys

def start_local_server(port=8000, max_attempts=10):
    """Start a simple HTTP server, trying different ports if needed"""
    for attempt in range(max_attempts):
        try:
            handler = http.server.SimpleHTTPRequestHandler
            
            class QuietHTTPServer(socketserver.TCPServer):
                allow_reuse_address = True
                
                def handle_error(self, request, client_address):
                    pass  # Suppress error messages
            
            httpd = QuietHTTPServer(("", port), handler)
            
            # Run server in a background thread
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()
            
            print(f'✓ HTTP server started on port {port}')
            return httpd, port
            
        except OSError as e:
            if attempt < max_attempts - 1:
                port += 1
            else:
                raise RuntimeError(f"Could not find available port after {max_attempts} attempts") from e
    
    raise RuntimeError("Unexpected error in start_local_server")

def main():
    server = None
    try:
        # Start local HTTP server so assets load properly
        print('Starting local HTTP server...')
        server, port = start_local_server(8000)
        time.sleep(1)  # Give server time to start
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load via HTTP so SVG icons and other assets load properly
            page.goto(f'http://localhost:{port}/index.html#resume')
            
            # Wait for the page to be fully loaded
            page.wait_for_load_state('networkidle')
            page.wait_for_load_state('domcontentloaded')
            
            # Wait for resume section to be visible
            try:
                page.wait_for_selector('#resume-section', state='visible', timeout=10000)
            except Exception:
                print('Warning: Resume section not found, continuing anyway...')
            
            # Give extra time for any SVG/fonts to load
            time.sleep(2)
            
            # Generate PDF using browser's print function
            # Optimized for ONE PAGE with maximum readability
            page.pdf(
                path='resume.pdf',
                format='Letter',
                print_background=True,
                prefer_css_page_size=False,
                margin={
                    'top': '0.2in',
                    'right': '0.2in',
                    'bottom': '0.2in',
                    'left': '0.2in'
                },
                scale=0.98  # Slightly smaller to fit more content on one page
            )
            
            browser.close()
            print('✓ PDF generated using browser print (Chromium)')
    
    except Exception as e:
        print(f'ERROR: PDF generation failed: {e}')
        sys.exit(1)
    
    finally:
        # Shutdown server
        if server:
            try:
                server.shutdown()
            except Exception:
                pass  # Ignore cleanup errors

if __name__ == '__main__':
    main()
