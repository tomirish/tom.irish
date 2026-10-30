"""m365-logo.png is the Microsoft 365 theme's alternate (dark-mode) logo:
the profile tile without its outer crimson band, so the cream ring frames it,
padded so the tile fills 80% of the height.

The M365 admin center loads it from a commit-pinned raw.githubusercontent.com
URL, so that copy never changes. These tests keep the file on main matching
what the theme shows, so the next change starts from the right image.
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


def _middle_column(img):
    rgba = img.convert("RGBA")
    return [rgba.getpixel((48, y)) for y in range(48)]


def test_m365_logo_has_transparent_padding():
    # Microsoft scales the logo to the header's full height, so the margin
    # above and below the tile has to be inside the image (tile = 80%).
    with Image.open(LOGO) as img:
        column = _middle_column(img)
        assert img.convert("RGBA").getpixel((0, 0))[3] == 0
        assert all(alpha == 0 for *_, alpha in column[:7])


def test_m365_logo_is_ringed_tile_without_outer_band():
    # The first opaque pixels are the cream ring, so it reads on a dark bar;
    # the crimson tile starts inside it.
    with Image.open(LOGO) as img:
        opaque = [rgb for *rgb, alpha in _middle_column(img) if alpha == 255]
        assert all(channel > 240 for channel in opaque[0])
        assert tuple(opaque[5]) == ACCENT


def test_m365_logo_under_microsoft_size_limit():
    assert os.path.getsize(LOGO) < MAX_BYTES
