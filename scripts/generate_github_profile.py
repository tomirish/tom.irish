#!/usr/bin/env python3
"""
Generates two 2048x2048 GitHub profile pictures:
  - github-profile.png        — Ti card with cream border ring
  - github-profile-simple.png — same layout, no border (cleaner at small sizes)

Deletes any existing files and rebuilds both on every run.
Tweak the parameters below and rerun to adjust.
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

# --- Parameters ---
CANVAS    = 2048
CARD_SIZE = 1300        # px — size of the Ti element card; reduce for more crimson

BG_COLOR     = "#9b2335"   # crimson — fills entire canvas and inner card area
BORDER_COLOR = "#faf9f7"   # cream — the inset ring

# Card geometry (proportionally scaled from the 1024px original)
OUTER_RADIUS = 218      # border-radius of the card
BORDER_INSET = 56       # px from card edge to cream ring
BORDER_WIDTH = 55       # px wide cream ring
INNER_INSET  = BORDER_INSET + BORDER_WIDTH   # 111px

# "Ti" text
TI_FONT_SIZE = 787      # CSS px
TI_Y_OFFSET  = -25      # px nudge from flexbox center (negative = up)

# "22" atomic number — position from top-left of the card
NUM_FONT_SIZE = 121     # CSS px
NUM_X         = 171     # px from card left edge
NUM_Y         = 140     # px from card top edge
# ------------------

REPO_ROOT      = Path(__file__).parent.parent
FONT_PATH      = REPO_ROOT / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"
OUT_BORDER     = REPO_ROOT / "assets" / "images" / "github-profile.png"
OUT_SIMPLE     = REPO_ROOT / "assets" / "images" / "github-profile-simple.png"

_RING_RADIUS  = OUTER_RADIUS - BORDER_INSET
_INNER_RADIUS = max(OUTER_RADIUS - INNER_INSET, 30)

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
.card {{
  width:  {card_size}px;
  height: {card_size}px;
  background: {bg};
  border-radius: {outer_r}px;
  position: relative;
  flex-shrink: 0;
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
<div class="card">
  <div class="ring"></div>
  <div class="inner">
    <div class="ti">Ti</div>
  </div>
  <div class="num">22</div>
</div>
</body>
</html>
"""


HTML_SIMPLE = """\
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
  position: relative;
}}
.ti {{
  font-family: 'DM Serif Display', serif;
  font-weight: bold;
  font-size: {ti_fs}px;
  color: {border};
  line-height: 1;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translateY({ti_yo}px);
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
<div class="ti">Ti</div>
<div class="num">22</div>
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
            browser = pw.chromium.launch(channel="msedge")
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
    card_offset = (CANVAS - CARD_SIZE) // 2   # 374px — canvas edge to card edge

    variants = [
        (OUT_BORDER, "with border", HTML_TEMPLATE.format(
            font_b64=font_b64,
            canvas=CANVAS,
            card_size=CARD_SIZE,
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
        )),
        (OUT_SIMPLE, "no border", HTML_SIMPLE.format(
            font_b64=font_b64,
            canvas=CANVAS,
            bg=BG_COLOR,
            border=BORDER_COLOR,
            ti_fs=TI_FONT_SIZE,
            ti_yo=TI_Y_OFFSET,
            num_fs=NUM_FONT_SIZE,
            num_x=card_offset + NUM_X,
            num_y=card_offset + NUM_Y,
        )),
    ]

    for out_path, label, html in variants:
        if out_path.exists():
            out_path.unlink()
            print(f"Removed existing {out_path.name}")

        print(f"Generating {out_path.name} ({label}) via Playwright…")

        try:
            render_with_playwright(html, out_path)
        except ImportError:
            print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium",
                  file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        if not out_path.exists():
            print(f"ERROR: {out_path.name} was not created.", file=sys.stderr)
            sys.exit(1)

        size_kb = out_path.stat().st_size // 1024
        print(f"  Saved {out_path.name} ({CANVAS}x{CANVAS}, {size_kb} KB)")


if __name__ == "__main__":
    main()
