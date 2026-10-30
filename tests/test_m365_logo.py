"""m365-logo.png is the Microsoft 365 theme's alternate (dark-mode) logo:
the profile tile without its outer crimson band, so the cream ring frames it.

The M365 admin center loads it by URL from raw.githubusercontent.com on main,
so renaming or replacing it breaks that logo with no error on this site.
"""

import os

from PIL import Image

LOGO = os.path.join(
    os.path.dirname(__file__), "..", "assets", "images", "m365-logo.png"
)
ACCENT = (0x9B, 0x23, 0x35)
CREAM = (0xFA, 0xF9, 0xF7)
MAX_BYTES = 10 * 1024  # Microsoft's limit for a theme logo


def test_m365_logo_is_png():
    with Image.open(LOGO) as img:
        assert img.format == "PNG"


def test_m365_logo_dimensions():
    with Image.open(LOGO) as img:
        assert img.size == (96, 96), f"Expected (96, 96), got {img.size}"


def test_m365_logo_corners_are_transparent():
    with Image.open(LOGO) as img:
        assert img.convert("RGBA").getpixel((0, 0))[3] == 0


def test_m365_logo_is_ringed_tile_without_outer_band():
    # Outermost opaque pixels are the cream ring, so it reads on a dark bar;
    # the crimson tile starts inside it.
    with Image.open(LOGO) as img:
        rgba = img.convert("RGBA")
        assert rgba.getpixel((48, 1)) == (*CREAM, 255)
        assert rgba.getpixel((48, 6)) == (*ACCENT, 255)


def test_m365_logo_under_microsoft_size_limit():
    assert os.path.getsize(LOGO) < MAX_BYTES
