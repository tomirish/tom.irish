#!/usr/bin/env python3
"""
Generates assets/images/favicon.png and assets/images/favicon-dark.png from scratch.

Deletes any existing files and rebuilds both on every run.
Tweak the parameters below and rerun to adjust the icons.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- Parameters ---
CANVAS = 256

# Light variant (default)
LIGHT_BG    = "#9b2335"
LIGHT_TEXT  = "#faf9f7"

# Dark variant
DARK_BG     = "#131313"
DARK_TEXT   = "#faf9f7"

FONT_SIZE   = 186         # pt — size of "Ti"
STROKE      = 2           # px — adds weight to letterforms (0 = none)
VERT_OFFSET = -3          # px — shift text up (-) or down (+) from center
# ------------------

REPO_ROOT = Path(__file__).parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"

VARIANTS = [
    {"out": "favicon.png",      "bg": LIGHT_BG, "text": LIGHT_TEXT},
    {"out": "favicon-dark.png", "bg": DARK_BG,  "text": DARK_TEXT},
]


def hex_to_rgba(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def generate_favicon(out_path: Path, bg: str, text_color: str) -> None:
    img = Image.new("RGBA", (CANVAS, CANVAS), hex_to_rgba(bg))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
    bbox = draw.textbbox((0, 0), "Ti", font=font, stroke_width=STROKE)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (CANVAS - tw) / 2 - bbox[0]
    ty = (CANVAS - th) / 2 - bbox[1] + VERT_OFFSET
    draw.text(
        (tx, ty), "Ti",
        fill=text_color, font=font,
        stroke_width=STROKE, stroke_fill=text_color,
    )

    img.save(out_path, format="PNG", optimize=True)


def main() -> None:
    if not FONT_PATH.exists():
        print(f"ERROR: Font not found: {FONT_PATH}", file=sys.stderr)
        sys.exit(1)

    images_dir = REPO_ROOT / "assets" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    for variant in VARIANTS:
        out_path = images_dir / variant["out"]

        if out_path.exists():
            out_path.unlink()
            print(f"Removed existing {out_path.name}")

        print(f"Generating {out_path.name} ({CANVAS}x{CANVAS}px)...")

        try:
            generate_favicon(out_path, variant["bg"], variant["text"])
        except Exception as exc:
            print(f"ERROR: Failed to generate {out_path.name}: {exc}", file=sys.stderr)
            sys.exit(1)

        if not out_path.exists():
            print(f"ERROR: {out_path.name} was not created.", file=sys.stderr)
            sys.exit(1)

        try:
            with Image.open(out_path) as v:
                actual_size = v.size
                actual_format = v.format
        except Exception as exc:
            print(f"ERROR: {out_path.name} is not a valid image: {exc}", file=sys.stderr)
            sys.exit(1)

        if actual_size != (CANVAS, CANVAS):
            print(f"ERROR: Expected {CANVAS}x{CANVAS}, got {actual_size}", file=sys.stderr)
            sys.exit(1)

        size_kb = out_path.stat().st_size // 1024
        print(f"  Saved ({actual_format}, {actual_size[0]}x{actual_size[1]}, {size_kb} KB)")


if __name__ == "__main__":
    main()
