#!/usr/bin/env python3
"""
Generates assets/images/ti-element.png — a periodic-table-style element icon.

Uses Playwright + Google Fonts to render DM Serif Display with browser-accurate
faux-bold (matching icon.kitchen's rendering exactly).

Deletes any existing file and rebuilds on every run.
Tweak the parameters below and rerun to adjust the icon.
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

# --- Parameters ---
CANVAS = 2048

BG_COLOR     = "#9b2335"   # red — outer rect and inner content
BORDER_COLOR = "#faf9f7"   # cream — the inset ring

# Outer rounded rectangle
OUTER_RADIUS = 344

# Cream border ring
BORDER_INSET = 88          # px from canvas edge to cream ring
BORDER_WIDTH = 86          # px wide cream ring

# Inner red content area
INNER_INSET  = BORDER_INSET + BORDER_WIDTH   # 174px

# "Ti" text — font-size in CSS px; nudge vertically if needed
TI_FONT_SIZE = 1240        # CSS px
TI_Y_OFFSET  = -40         # px nudge from flexbox center (negative = up)

# "22" atomic number — position from top-left of canvas
NUM_FONT_SIZE = 190        # CSS px
NUM_X         = 270        # px from left canvas edge
NUM_Y         = 220        # px from top canvas edge
# ------------------

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH  = REPO_ROOT / "assets" / "images" / "ti-element.png"
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"

# Computed geometry
_RING_RADIUS  = OUTER_RADIUS - BORDER_INSET          # 128
_INNER_RADIUS = max(OUTER_RADIUS - INNER_INSET, 30)  # 85

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
body {{
  width:  {canvas}px;
  height: {canvas}px;
  background: transparent;
  overflow: hidden;
}}
.outer {{
  width:  {canvas}px;
  height: {canvas}px;
  background: {bg};
  border-radius: {outer_r}px;
  position: relative;
}}
.ring {{
  position: absolute;
  inset: {b_inset}px;
  background: {border};
  border-radius: {ring_r}px;
}}
.inner {{
  position: absolute;
  inset: {i_inset}px;
  background: {bg};
  border-radius: {inner_r}px;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.ti {{
  font-family: 'DM Serif Display', serif;
  font-weight: bold;
  font-size: {ti_fs}px;
  color: {border};
  line-height: 1;
  margin-top: {ti_yo}px;
  -webkit-font-smoothing: antialiased;
}}
.num {{
  position: absolute;
  top:  {num_y}px;
  left: {num_x}px;
  font-family: 'DM Serif Display', serif;
  font-weight: bold;
  font-size: {num_fs}px;
  color: {border};
  line-height: 1;
  -webkit-font-smoothing: antialiased;
}}
</style>
</head>
<body>
<div class="outer">
  <div class="ring"></div>
  <div class="inner">
    <div class="ti">Ti</div>
  </div>
  <div class="num">22</div>
</div>
</body>
</html>
"""


def render_with_playwright(html: str) -> None:
    """Write html to a temp file, screenshot it, save to OUT_PATH."""
    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(html)
        tmp = f.name

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            # Use the system Edge installation (no separate download required)
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": CANVAS, "height": CANVAS})
            page.goto(f"file://{tmp}")
            page.wait_for_load_state("networkidle")
            page.screenshot(path=str(OUT_PATH), type="png", full_page=False, omit_background=True)
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
        border=BORDER_COLOR,
        outer_r=OUTER_RADIUS,
        b_inset=BORDER_INSET,
        ring_r=_RING_RADIUS,
        i_inset=INNER_INSET,
        inner_r=_INNER_RADIUS,
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
