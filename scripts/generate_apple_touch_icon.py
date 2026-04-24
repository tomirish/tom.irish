#!/usr/bin/env python3
"""
Generates assets/images/apple-touch-icon.png.

Tweak the parameters below and rerun to adjust the icon.
"""

from PIL import Image, ImageDraw, ImageFont
import os

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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
FONT_PATH = os.path.join(REPO_ROOT, "assets", "fonts", "DMSerifDisplay-Regular.ttf")
OUT_PATH = os.path.join(REPO_ROOT, "assets", "images", "apple-touch-icon.png")


def hex_to_rgba(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)


def main():
    img = Image.new("RGBA", (CANVAS, CANVAS), hex_to_rgba(BG_COLOR))
    draw = ImageDraw.Draw(img)

    ti_font = ImageFont.truetype(FONT_PATH, TI_FONT_SIZE)
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

    num_font = ImageFont.truetype(FONT_PATH, NUM_FONT_SIZE)
    nb = draw.textbbox((0, 0), "22", font=num_font)
    draw.text((NUM_X - nb[0], NUM_Y - nb[1]), "22", fill=TEXT_COLOR, font=num_font)

    img.save(OUT_PATH)
    print(f"Saved {OUT_PATH}")
    print(f"Ti: {tw}x{th}px centered")
    print(f"22: x={NUM_X}, y={NUM_Y}")


if __name__ == "__main__":
    main()
