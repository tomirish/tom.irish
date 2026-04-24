#!/usr/bin/env python3
"""
Generates assets/images/apple-touch-icon.png from scratch.

Deletes any existing file and rebuilds on every run.
Tweak the parameters below and rerun to adjust the icon.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- Parameters ---
CANVAS = 1024
BG_COLOR = "#9b2335"
TEXT_COLOR = "#faf9f7"

TI_FONT_SIZE = 720        # pt — increase to make Ti larger
TI_STROKE = 6             # px — adds weight to the letterforms (0 = none)

NUM_FONT_SIZE = 110       # pt — size of the "22"
NUM_X = 155               # px from left edge
NUM_Y = 75                # px from top edge
# ------------------

REPO_ROOT = Path(__file__).parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"
OUT_PATH = REPO_ROOT / "assets" / "images" / "apple-touch-icon.png"


def hex_to_rgba(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def main() -> None:
    # Validate dependencies upfront
    if not FONT_PATH.exists():
        print(f"ERROR: Font not found: {FONT_PATH}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Delete any existing file — always build from scratch
    if OUT_PATH.exists():
        OUT_PATH.unlink()
        print(f"Removed existing {OUT_PATH.name}")

    print(f"Generating {OUT_PATH.name} ({CANVAS}x{CANVAS}px)...")

    try:
        img = Image.new("RGBA", (CANVAS, CANVAS), hex_to_rgba(BG_COLOR))
        draw = ImageDraw.Draw(img)

        # Draw centered "Ti"
        ti_font = ImageFont.truetype(str(FONT_PATH), TI_FONT_SIZE)
        bbox = draw.textbbox((0, 0), "Ti", font=ti_font, stroke_width=TI_STROKE)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (CANVAS - tw) / 2 - bbox[0]
        ty = (CANVAS - th) / 2 - bbox[1]
        draw.text(
            (tx, ty), "Ti",
            fill=TEXT_COLOR, font=ti_font,
            stroke_width=TI_STROKE, stroke_fill=TEXT_COLOR,
        )

        # Draw "22" in upper-left area
        num_font = ImageFont.truetype(str(FONT_PATH), NUM_FONT_SIZE)
        nb = draw.textbbox((0, 0), "22", font=num_font)
        draw.text((NUM_X - nb[0], NUM_Y - nb[1]), "22", fill=TEXT_COLOR, font=num_font)

        img.save(OUT_PATH, format="PNG", optimize=True)
    except Exception as exc:
        print(f"ERROR: Failed to generate icon: {exc}", file=sys.stderr)
        sys.exit(1)

    # Verify the output is valid
    if not OUT_PATH.exists():
        print("ERROR: Output file was not created.", file=sys.stderr)
        sys.exit(1)

    try:
        with Image.open(OUT_PATH) as verification:
            actual_size = verification.size
            actual_format = verification.format
    except Exception as exc:
        print(f"ERROR: Output file is not a valid image: {exc}", file=sys.stderr)
        sys.exit(1)

    if actual_size != (CANVAS, CANVAS):
        print(f"ERROR: Expected {CANVAS}x{CANVAS}, got {actual_size}", file=sys.stderr)
        sys.exit(1)

    size_kb = OUT_PATH.stat().st_size // 1024
    print(f"Saved {OUT_PATH} ({actual_format}, {actual_size[0]}x{actual_size[1]}, {size_kb} KB)")
    print(f"  Ti: {tw}x{th}px, centered")
    print(f"  22: x={NUM_X}, y={NUM_Y}")


if __name__ == "__main__":
    main()
