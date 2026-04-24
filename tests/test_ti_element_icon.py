import os
import sys
import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from generate_ti_element_icon import CANVAS, NUM_X, NUM_Y, BORDER_INSET, BORDER_WIDTH

ICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'ti-element.png')

pytestmark = pytest.mark.skipif(
    not os.path.exists(ICON_PATH),
    reason="ti-element.png not found (run generate_ti_element_icon.py first)"
)


def test_ti_element_is_png():
    with Image.open(ICON_PATH) as img:
        assert img.format == "PNG"


def test_ti_element_dimensions():
    with Image.open(ICON_PATH) as img:
        assert img.size == (CANVAS, CANVAS), f"Expected {CANVAS}x{CANVAS}, got {img.size}"


def test_ti_element_center_is_red():
    """Center pixel should be the red inner content area."""
    with Image.open(ICON_PATH) as img:
        r, g, b = img.convert("RGB").getpixel((CANVAS // 2, CANVAS // 2))
        assert r > 140 and g < 60 and b < 60, (
            f"Expected red at center, got #{r:02x}{g:02x}{b:02x}"
        )


def test_ti_element_corners_are_white():
    """Corners outside the rounded rect should be white (transparent bg rendered on white)."""
    with Image.open(ICON_PATH) as img:
        rgb = img.convert("RGB")
        for coord in [(0, 0), (CANVAS - 1, 0), (0, CANVAS - 1), (CANVAS - 1, CANVAS - 1)]:
            r, g, b = rgb.getpixel(coord)
            assert r > 240 and g > 240 and b > 240, (
                f"Expected white corner at {coord}, got #{r:02x}{g:02x}{b:02x}"
            )


def test_ti_element_cream_border_present():
    """The cream border ring should be visible at the inset edges."""
    mid_x = CANVAS // 2
    ring_mid_y = BORDER_INSET + BORDER_WIDTH // 2
    with Image.open(ICON_PATH) as img:
        r, g, b = img.convert("RGB").getpixel((mid_x, ring_mid_y))
        assert r > 220 and g > 210 and b > 200, (
            f"Expected cream border at ({mid_x}, {ring_mid_y}), got #{r:02x}{g:02x}{b:02x}"
        )


def test_ti_element_has_cream_text_region():
    """Upper-left inner area where '22' sits should contain light (cream) pixels."""
    # Sample into the glyph body — offset from NUM_X/NUM_Y into a solid stroke
    sample_x = NUM_X + 35
    sample_y = NUM_Y + 20
    with Image.open(ICON_PATH) as img:
        r, g, b = img.convert("RGB").getpixel((sample_x, sample_y))
        assert r > 200 and g > 190 and b > 180, (
            f"Expected cream '22' text near ({sample_x}, {sample_y}), got #{r:02x}{g:02x}{b:02x}"
        )
