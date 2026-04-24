#!/usr/bin/env python3
"""
Generates assets/images/apple-touch-icon.png from scratch.

Uses Playwright + embedded font for browser-accurate faux-bold rendering.
Deletes any existing file and rebuilds on every run.
Tweak the parameters below and rerun to adjust the icon.
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

# --- Parameters ---
CANVAS = 1024
BG_COLOR   = "#9b2335"
TEXT_COLOR = "#faf9f7"

TI_FONT_SIZE = 720    # CSS px
TI_Y_OFFSET  = 0      # px nudge from center (negative = up)

NUM_FONT_SIZE = 110   # CSS px
NUM_X         = 155   # px from left edge
NUM_Y         = 75    # px from top edge
# ------------------

REPO_ROOT = Path(__file__).parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"
OUT_PATH  = REPO_ROOT / "assets" / "images" / "apple-touch-icon.png"

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
}}
body {{ position: relative; }}
.ti {{
  font-family: 'DM Serif Display', serif;
  font-weight: bold;
  font-size: {ti_fs}px;
  color: {text};
  line-height: 1;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translateY({ti_yo}px);
  -webkit-font-smoothing: antialiased;
}}
.num {{
  font-family: 'DM Serif Display', serif;
  font-weight: bold;
  font-size: {num_fs}px;
  color: {text};
  line-height: 1;
  position: absolute;
  top:  {num_y}px;
  left: {num_x}px;
  -webkit-font-smoothing: antialiased;
}}
</style>
</head>
<body>
<div class="ti">Ti</div>
<div class="num">22</div>
</body>
</html>
"""


def render_with_playwright(html: str) -> None:
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
            page.screenshot(path=str(OUT_PATH), type="png", full_page=False)
            browser.close()
    finally:
        os.unlink(tmp)


def main() -> None:
    if not FONT_PATH.exists():
        print(f"ERROR: Font not found: {FONT_PATH}", file=sys.stderr)
        sys.exit(1)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if OUT_PATH.exists():
        OUT_PATH.unlink()
        print(f"Removed existing {OUT_PATH.name}")

    print(f"Generating {OUT_PATH.name} ({CANVAS}x{CANVAS}px) via Playwright…")

    font_b64 = base64.b64encode(FONT_PATH.read_bytes()).decode()

    html = HTML_TEMPLATE.format(
        font_b64=font_b64,
        canvas=CANVAS,
        bg=BG_COLOR,
        text=TEXT_COLOR,
        ti_fs=TI_FONT_SIZE,
        ti_yo=TI_Y_OFFSET,
        num_fs=NUM_FONT_SIZE,
        num_x=NUM_X,
        num_y=NUM_Y,
    )

    try:
        render_with_playwright(html)
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium",
              file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if not OUT_PATH.exists():
        print("ERROR: Output file was not created.", file=sys.stderr)
        sys.exit(1)

    size_kb = OUT_PATH.stat().st_size // 1024
    print(f"Saved {OUT_PATH} ({CANVAS}x{CANVAS}, {size_kb} KB)")


if __name__ == "__main__":
    main()
