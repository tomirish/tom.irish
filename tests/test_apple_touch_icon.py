import os
import pytest
from PIL import Image

ICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'apple-touch-icon.png')


@pytest.mark.skipif(
    not os.path.exists(ICON_PATH),
    reason="apple-touch-icon.png not found (run generate_apple_touch_icon.py first)"
)
def test_apple_touch_icon_is_png():
    with Image.open(ICON_PATH) as img:
        assert img.format == "PNG"


@pytest.mark.skipif(
    not os.path.exists(ICON_PATH),
    reason="apple-touch-icon.png not found (run generate_apple_touch_icon.py first)"
)
def test_apple_touch_icon_dimensions():
    with Image.open(ICON_PATH) as img:
        assert img.size == (1024, 1024), f"Expected 1024x1024, got {img.size}"


@pytest.mark.skipif(
    not os.path.exists(ICON_PATH),
    reason="apple-touch-icon.png not found (run generate_apple_touch_icon.py first)"
)
def test_apple_touch_icon_is_rgba():
    with Image.open(ICON_PATH) as img:
        assert img.mode in ("RGBA", "RGB"), f"Expected RGB/RGBA mode, got {img.mode}"


@pytest.mark.skipif(
    not os.path.exists(ICON_PATH),
    reason="apple-touch-icon.png not found (run generate_apple_touch_icon.py first)"
)
def test_apple_touch_icon_background_color():
    """Verify the corner pixel matches the expected crimson background."""
    with Image.open(ICON_PATH) as img:
        pixel = img.convert("RGB").getpixel((0, 0))
        r, g, b = pixel
        assert (r, g, b) == (0x9b, 0x23, 0x35), (
            f"Expected background #9b2335, got #{r:02x}{g:02x}{b:02x}"
        )
