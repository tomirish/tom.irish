"""The Microsoft 365 branding images (docs/M365-BRANDING.md).

m365-logo.png is the org theme's alternate (dark-mode) logo: the mark without
its outer crimson band, so the cream ring frames it, padded so the ring fills
80% of the height. The admin center loads it from a commit-pinned
raw.githubusercontent.com URL, so that copy never changes; these tests keep
the file on main matching what the theme shows.

m365-default-logo.png (uploaded) keeps the outer band and is padded so its
ring lands in the same place, and entra-square-logo.png is the Entra square
logo Outlook mobile crops to a circle.
"""

import os

from PIL import Image

IMAGES = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
LOGO = os.path.join(IMAGES, "m365-logo.png")
DEFAULT_LOGO = os.path.join(IMAGES, "m365-default-logo.png")
ENTRA_SQUARE = os.path.join(IMAGES, "entra-square-logo.png")
ACCENT = (0x9B, 0x23, 0x35)
CREAM = (0xFA, 0xF9, 0xF7)
MAX_BYTES = 10 * 1024  # Microsoft's limit for a theme logo
ENTRA_MAX_BYTES = 50 * 1024  # Entra's limit for a square logo


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


def test_default_logo_is_96px_png_under_limit():
    with Image.open(DEFAULT_LOGO) as img:
        assert img.format == "PNG"
        assert img.size == (96, 96)
    assert os.path.getsize(DEFAULT_LOGO) < MAX_BYTES


def test_both_theme_logos_put_the_ring_in_the_same_place():
    # The two modes look the same size only while their cream rings line up.
    for path in (LOGO, DEFAULT_LOGO):
        with Image.open(path) as img:
            assert _middle_column(img)[12] == (*CREAM, 255), path


def test_default_logo_keeps_the_outer_band():
    # On the crimson bar the band merges into the background; on transparent
    # padding it is the first opaque thing above the ring.
    with Image.open(DEFAULT_LOGO) as img:
        column = _middle_column(img)
        assert img.convert("RGBA").getpixel((0, 0))[3] == 0
        assert column[7][3] == 255 and column[7][0] < 200


def test_entra_square_logo_is_solid_tile():
    # Outlook crops it to a circle, so it is edge-to-edge crimson with no ring.
    with Image.open(ENTRA_SQUARE) as img:
        assert img.format == "PNG"
        assert img.size == (240, 240)
        rgba = img.convert("RGBA")
        for xy in ((0, 0), (239, 239), (120, 2)):
            assert rgba.getpixel(xy) == (*ACCENT, 255), xy
    assert os.path.getsize(ENTRA_SQUARE) < ENTRA_MAX_BYTES
