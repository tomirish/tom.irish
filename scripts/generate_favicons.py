#!/usr/bin/env python3
"""
Generates assets/images/favicon.png and assets/images/favicon-dark.png from scratch.

Uses Playwright + embedded font for browser-accurate faux-bold rendering.
Deletes any existing files and rebuilds both on every run.
Tweak the parameters below and rerun to adjust the icons.
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

# --- Parameters ---
CANVAS = 256

LIGHT_BG   = "#9b2335"
DARK_BG    = "#131313"
TEXT_COLOR = "#faf9f7"

FONT_SIZE   = 186    # CSS px
VERT_OFFSET = -3     # px nudge from center (negative = up)
# ------------------

REPO_ROOT = Path(__file__).parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"

VARIANTS = [
    {"out": "favicon.png",      "bg": LIGHT_BG},
    {"out": "favicon-dark.png", "bg": DARK_BG},
]

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
@font-face {{
  font-family: 'DM Serif Display';
  src: url('data:font/truetype;base64,{font_b64}') format('truetype');
  font-weight: normal;
  font-style: normal;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{
  width:  {canvas}px;
  height: {canvas}px;
  background: {bg};
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.ti {{
  font-family: 'DM Serif Display', serif;
  font-weight: bold;
  font-size: {fs}px;
  color: {text};
  line-height: 1;
  margin-top: {vo}px;
  -webkit-font-smoothing: antialiased;
}}
</style>
</head>
<body>
<div class="ti">Ti</div>
</body>
</html>
"""


def render_with_playwright(html: str, out_path: Path) -> None:
    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(html)
        tmp = f.name

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": CANVAS, "height": CANVAS})
            page.goto(f"file://{tmp}")
            page.wait_for_load_state("networkidle")
            page.screenshot(path=str(out_path), type="png", full_page=False)
            browser.close()
    finally:
        os.unlink(tmp)


def main() -> None:
    if not FONT_PATH.exists():
        print(f"ERROR: Font not found: {FONT_PATH}", file=sys.stderr)
        sys.exit(1)

    images_dir = REPO_ROOT / "assets" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    font_b64 = base64.b64encode(FONT_PATH.read_bytes()).decode()

    for variant in VARIANTS:
        out_path = images_dir / variant["out"]

        if out_path.exists():
            out_path.unlink()
            print(f"Removed existing {out_path.name}")

        print(f"Generating {out_path.name} ({CANVAS}x{CANVAS}px) via Playwright…")

        html = HTML_TEMPLATE.format(
            font_b64=font_b64,
            canvas=CANVAS,
            bg=variant["bg"],
            text=TEXT_COLOR,
            fs=FONT_SIZE,
            vo=VERT_OFFSET,
        )

        try:
            render_with_playwright(html, out_path)
        except ImportError:
            print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium",
                  file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"ERROR: Failed to generate {out_path.name}: {exc}", file=sys.stderr)
            sys.exit(1)

        if not out_path.exists():
            print(f"ERROR: {out_path.name} was not created.", file=sys.stderr)
            sys.exit(1)

        size_kb = out_path.stat().st_size // 1024
        print(f"  Saved {out_path.name} ({CANVAS}x{CANVAS}, {size_kb} KB)")


if __name__ == "__main__":
    main()
