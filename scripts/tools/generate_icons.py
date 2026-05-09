#!/usr/bin/env python3
"""
Generates all site icons:
  - assets/images/favicon.png         — 256×256, crimson bg
  - assets/images/favicon-dark.png    — 256×256, dark bg
  - assets/images/apple-touch-icon.png — 1024×1024, crimson bg with atomic number

Deletes any existing files and rebuilds all three on every run.
Tweak the parameters below and rerun to adjust the icons.
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

# --- Shared parameters ---
TEXT_COLOR = "#faf9f7"
LIGHT_BG   = "#9b2335"
DARK_BG    = "#131313"

# Favicon parameters (256×256)
FAVICON_CANVAS      = 256
FAVICON_FONT_SIZE   = 186
FAVICON_VERT_OFFSET = -3

# Apple touch icon parameters (1024×1024)
TOUCH_CANVAS        = 1024
TOUCH_TI_FONT_SIZE  = 720
TOUCH_TI_Y_OFFSET   = 0
TOUCH_NUM_FONT_SIZE = 110
TOUCH_NUM_X         = 155
TOUCH_NUM_Y         = 75
# ------------------

REPO_ROOT  = Path(__file__).parent.parent.parent
FONT_PATH  = REPO_ROOT / "scripts" / "tools" / "DMSerifDisplay-Regular.ttf"
IMAGES_DIR = REPO_ROOT / "assets" / "images"

# Template for favicons — "Ti" only, no atomic number
HTML_FAVICON = """\
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

# Template for apple touch icon — "Ti" + "22" atomic number
HTML_TOUCH = """\
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


def render_with_playwright(html: str, out_path: Path, canvas: int) -> None:
    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(html)
        tmp = f.name

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": canvas, "height": canvas})
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

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    font_b64 = base64.b64encode(FONT_PATH.read_bytes()).decode()

    variants = [
        (
            IMAGES_DIR / "favicon.png",
            FAVICON_CANVAS,
            HTML_FAVICON.format(
                font_b64=font_b64,
                canvas=FAVICON_CANVAS,
                bg=LIGHT_BG,
                text=TEXT_COLOR,
                fs=FAVICON_FONT_SIZE,
                vo=FAVICON_VERT_OFFSET,
            ),
        ),
        (
            IMAGES_DIR / "favicon-dark.png",
            FAVICON_CANVAS,
            HTML_FAVICON.format(
                font_b64=font_b64,
                canvas=FAVICON_CANVAS,
                bg=DARK_BG,
                text=TEXT_COLOR,
                fs=FAVICON_FONT_SIZE,
                vo=FAVICON_VERT_OFFSET,
            ),
        ),
        (
            IMAGES_DIR / "apple-touch-icon.png",
            TOUCH_CANVAS,
            HTML_TOUCH.format(
                font_b64=font_b64,
                canvas=TOUCH_CANVAS,
                bg=LIGHT_BG,
                text=TEXT_COLOR,
                ti_fs=TOUCH_TI_FONT_SIZE,
                ti_yo=TOUCH_TI_Y_OFFSET,
                num_fs=TOUCH_NUM_FONT_SIZE,
                num_x=TOUCH_NUM_X,
                num_y=TOUCH_NUM_Y,
            ),
        ),
    ]

    for out_path, canvas, html in variants:
        if out_path.exists():
            out_path.unlink()
            print(f"Removed existing {out_path.name}")

        print(f"Generating {out_path.name} ({canvas}x{canvas}px) via Playwright…")

        try:
            render_with_playwright(html, out_path, canvas)
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
        print(f"  Saved {out_path.name} ({canvas}x{canvas}, {size_kb} KB)")


if __name__ == "__main__":
    main()
