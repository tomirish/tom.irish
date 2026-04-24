import os
import pytest
from PIL import Image

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
        assert img.size == (1024, 1024), f"Expected 1024x1024, got {img.size}"


def test_ti_element_center_is_red():
    """Center pixel should be the red inner content area."""
    with Image.open(ICON_PATH) as img:
        r, g, b = img.convert("RGB").getpixel((512, 512))
        assert r > 140 and g < 60 and b < 60, (
            f"Expected red at center, got #{r:02x}{g:02x}{b:02x}"
        )


def test_ti_element_corners_are_white():
    """Corners outside the rounded rect should be white (transparent bg rendered on white)."""
    with Image.open(ICON_PATH) as img:
        rgb = img.convert("RGB")
        for coord in [(0, 0), (1023, 0), (0, 1023), (1023, 1023)]:
            r, g, b = rgb.getpixel(coord)
            assert r > 240 and g > 240 and b > 240, (
                f"Expected white corner at {coord}, got #{r:02x}{g:02x}{b:02x}"
            )


def test_ti_element_cream_border_present():
    """The cream border ring should be visible at the inset edges (≈44px in)."""
    with Image.open(ICON_PATH) as img:
        rgb = img.convert("RGB")
        # Sample midpoint of the top cream ring
        r, g, b = rgb.getpixel((512, 55))
        assert r > 220 and g > 210 and b > 200, (
            f"Expected cream border at (512, 55), got #{r:02x}{g:02x}{b:02x}"
        )


def test_ti_element_has_cream_text_region():
    """Upper-left inner area where '22' sits should contain light (cream) pixels."""
    with Image.open(ICON_PATH) as img:
        rgb = img.convert("RGB")
        # Sample a solid cream stroke of the "22" text
        r, g, b = rgb.getpixel((170, 130))
        assert r > 200 and g > 190 and b > 180, (
            f"Expected cream '22' text near (170,130), got #{r:02x}{g:02x}{b:02x}"
        )
