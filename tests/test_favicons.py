import os
import pytest
from PIL import Image

IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')

VARIANTS = {
    "favicon.png":      {"bg": (0x9b, 0x23, 0x35), "size": (256, 256)},
    "favicon-dark.png": {"bg": (0x13, 0x13, 0x13), "size": (256, 256)},
}


def favicon_path(name):
    return os.path.join(IMAGES_DIR, name)


def skipif_missing(name):
    return pytest.mark.skipif(
        not os.path.exists(favicon_path(name)),
        reason=f"{name} not found (run generate_favicons.py first)"
    )


@skipif_missing("favicon.png")
def test_favicon_is_png():
    with Image.open(favicon_path("favicon.png")) as img:
        assert img.format == "PNG"


@skipif_missing("favicon-dark.png")
def test_favicon_dark_is_png():
    with Image.open(favicon_path("favicon-dark.png")) as img:
        assert img.format == "PNG"


@pytest.mark.parametrize("name", VARIANTS.keys())
def test_favicon_dimensions(name):
    if not os.path.exists(favicon_path(name)):
        pytest.skip(f"{name} not found (run generate_favicons.py first)")
    expected = VARIANTS[name]["size"]
    with Image.open(favicon_path(name)) as img:
        assert img.size == expected, f"Expected {expected}, got {img.size}"


@pytest.mark.parametrize("name", VARIANTS.keys())
def test_favicon_is_rgba(name):
    if not os.path.exists(favicon_path(name)):
        pytest.skip(f"{name} not found (run generate_favicons.py first)")
    with Image.open(favicon_path(name)) as img:
        assert img.mode in ("RGBA", "RGB"), f"Expected RGB/RGBA mode, got {img.mode}"


@pytest.mark.parametrize("name,meta", VARIANTS.items())
def test_favicon_background_color(name, meta):
    if not os.path.exists(favicon_path(name)):
        pytest.skip(f"{name} not found (run generate_favicons.py first)")
    expected_bg = meta["bg"]
    with Image.open(favicon_path(name)) as img:
        r, g, b = img.convert("RGB").getpixel((0, 0))
        assert (r, g, b) == expected_bg, (
            f"{name}: expected background #{expected_bg[0]:02x}{expected_bg[1]:02x}{expected_bg[2]:02x}, "
            f"got #{r:02x}{g:02x}{b:02x}"
        )
