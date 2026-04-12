#!/usr/bin/env python3
"""Generate share.jpg — the OG preview image for tom.irish."""

import base64
import os
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "assets" / "images" / "share.jpg"
PHOTO_PATH = REPO_ROOT / "assets" / "images" / "tom-irish.jpg"


def load_resume_data():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from convert_resume import parse_markdown_resume
    md = (REPO_ROOT / "resume.md").read_text(encoding="utf-8")
    return parse_markdown_resume(md)


def photo_data_uri():
    with open(PHOTO_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{b64}"


HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Playfair+Display:wght@400;700&display=swap"/>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 1200px;
  height: 630px;
  background: #fff;
  font-family: 'DM Sans', -apple-system, sans-serif;
  overflow: hidden;
  border-top: 8px solid #9b2335;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.card {{
  display: flex;
  align-items: center;
  gap: 64px;
  padding: 0 80px;
  width: 100%;
}}
.photo {{
  width: 180px;
  height: 180px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 8px 40px rgba(0,0,0,0.15);
}}
.photo img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
}}
.text {{
  flex: 1;
}}
.name {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 56px;
  font-weight: 700;
  color: #111;
  letter-spacing: -1px;
  line-height: 1.05;
  margin-bottom: 12px;
}}
.role {{
  font-size: 18px;
  font-weight: 500;
  color: #555;
  margin-bottom: 10px;
}}
.tagline {{
  font-size: 16px;
  font-weight: 400;
  color: #777;
  line-height: 1.5;
  margin-bottom: 28px;
  white-space: nowrap;
}}
.divider {{
  width: 48px;
  height: 3px;
  background: #9b2335;
  margin-bottom: 24px;
}}
.meta-item {{
  font-size: 15px;
  color: #999;
  letter-spacing: 0.2px;
}}
.site {{
  position: absolute;
  bottom: 32px;
  right: 80px;
  font-size: 15px;
  color: #9b2335;
  font-weight: 600;
  letter-spacing: 0.3px;
}}
</style>
</head>
<body>
<div class="card">
  <div class="photo">
    <img src="{photo_uri}" alt="{name}"/>
  </div>
  <div class="text">
    <div class="name">{name}</div>
    {role_html}
    {tagline_html}
    <div class="divider"></div>
    {location_html}
  </div>
</div>
<div class="site">{website}</div>
</body>
</html>"""


def main():
    data = load_resume_data()
    photo_uri = photo_data_uri()

    name = data.get('name', 'Tom Irish')
    role = data['work_experience'][0]['role'] if data.get('work_experience') else ''
    tagline = data.get('tagline', '')
    location = data.get('location', '')
    website = data.get('website', {}).get('display', 'tom.irish')

    role_html = f'<div class="role">{role}</div>' if role else ''
    tagline_html = f'<div class="tagline">{tagline}</div>' if tagline else ''
    location_html = f'<div class="meta-item">{location}</div>' if location else ''

    html = HTML.format(
        photo_uri=photo_uri,
        name=name,
        role_html=role_html,
        tagline_html=tagline_html,
        location_html=location_html,
        website=website,
    )

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as f:
        f.write(html)
        tmp_path = f.name

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1200, "height": 630})
            page.goto(f"file://{tmp_path}")
            page.wait_for_load_state("networkidle")
            page.screenshot(path=str(OUT_PATH), type="jpeg", quality=92, full_page=False)
            browser.close()
    finally:
        os.unlink(tmp_path)

    print(f"Written: {OUT_PATH}")


if __name__ == "__main__":
    main()
