import os
from PIL import Image

SHARE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'share.jpg')


def test_share_image_is_jpeg():
    with Image.open(SHARE_IMAGE_PATH) as img:
        assert img.format == "JPEG"


def test_share_image_dimensions():
    with Image.open(SHARE_IMAGE_PATH) as img:
        assert img.size == (1200, 630), f"Expected 1200x630, got {img.size}"
