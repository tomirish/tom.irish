import os
from PIL import Image

ICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'apple-touch-icon.png')


def test_apple_touch_icon_is_png():
    with Image.open(ICON_PATH) as img:
        assert img.format == "PNG"


def test_apple_touch_icon_dimensions():
    with Image.open(ICON_PATH) as img:
        assert img.size == (1024, 1024), f"Expected 1024x1024, got {img.size}"


def test_apple_touch_icon_is_rgba():
    with Image.open(ICON_PATH) as img:
        assert img.mode in ("RGBA", "RGB"), f"Expected RGB/RGBA mode, got {img.mode}"


def test_apple_touch_icon_background_color():
    with Image.open(ICON_PATH) as img:
        r, g, b = img.convert("RGB").getpixel((0, 0))
        assert (r, g, b) == (0x9b, 0x23, 0x35), (
            f"Expected background #9b2335, got #{r:02x}{g:02x}{b:02x}"
        )
