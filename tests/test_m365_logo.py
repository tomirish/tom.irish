"""m365-logo.png is the Microsoft 365 theme's alternate (dark-mode) logo.

The M365 admin center loads it by URL from raw.githubusercontent.com on main,
so renaming or replacing it breaks that logo with no error on this site.
"""

import os

from PIL import Image

LOGO = os.path.join(
    os.path.dirname(__file__), "..", "assets", "images", "m365-logo.png"
)
ACCENT = (0x9B, 0x23, 0x35)
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


def test_m365_logo_edge_is_accent():
    with Image.open(LOGO) as img:
        r, g, b, a = img.convert("RGBA").getpixel((48, 2))
        assert (r, g, b, a) == (*ACCENT, 255), f"got #{r:02x}{g:02x}{b:02x} alpha {a}"


def test_m365_logo_under_microsoft_size_limit():
    assert os.path.getsize(LOGO) < MAX_BYTES
