#!/usr/bin/env python3
"""
Converts scripts/tools/tom-irish-original.jpg to:
  - assets/images/tom-irish-280.webp
  - assets/images/tom-irish-280.jpg

Deletes any existing files and rebuilds both on every run.
"""

import sys
from pathlib import Path

SIZE = 280

REPO_ROOT   = Path(__file__).parent.parent.parent
SOURCE      = REPO_ROOT / "scripts" / "tools" / "tom-irish-original.jpg"
IMAGES_DIR  = REPO_ROOT / "assets" / "images"
OUT_WEBP    = IMAGES_DIR / "tom-irish-280.webp"
OUT_JPG     = IMAGES_DIR / "tom-irish-280.jpg"


def main() -> None:
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        sys.exit(1)

    if not SOURCE.exists():
        print(f"ERROR: Source not found: {SOURCE}", file=sys.stderr)
        sys.exit(1)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.open(SOURCE).convert("RGB")
    img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)

    for out_path, label, kwargs in [
        (OUT_WEBP, "WEBP", {"quality": 90}),
        (OUT_JPG,  "JPEG", {"quality": 90, "optimize": True}),
    ]:
        if out_path.exists():
            out_path.unlink()
            print(f"Removed existing {out_path.name}")

        img.save(out_path, format=label, **kwargs)
        size_kb = out_path.stat().st_size // 1024
        print(f"Saved {out_path.name} ({SIZE}x{SIZE}, {size_kb} KB)")


if __name__ == "__main__":
    main()
