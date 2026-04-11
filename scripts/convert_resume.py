#!/usr/bin/env python3
"""
Convert resume.md to HTML using Jinja2 templates.

Reads resume.md (single source of truth) and renders two Jinja2 templates:
  - index.template.html  → index.html  (web site)
  - resume.template.html → resume.html (PDF input for generate_pdf_browser.py)

Usage:
    python3 scripts/convert_resume.py            # writes both HTML files
    python3 scripts/convert_resume.py --dry-run  # parse only, no files written
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
ALLOWED_URL_SCHEMES = {'http', 'https', 'mailto', 'tel'}


def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: Could not read {filepath}: {e}")
        sys.exit(1)


def write_file(filepath, content, dry_run=False):
    if dry_run:
        print(f"🔍 DRY RUN: Would write {len(content)} bytes to {filepath} (skipped)")
        return
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Wrote {len(content)} bytes to {filepath}")
    except Exception as e:
        print(f"❌ ERROR: Could not write {filepath}: {e}")
        sys.exit(1)


def _parse_link(line):
    """Extract display text and href from a markdown link on a line."""
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
    if m and urlparse(m.group(2)).scheme in ALLOWED_URL_SCHEMES:
        return {'display': m.group(1), 'href': m.group(2)}
    return {'display': '', 'href': ''}


def parse_markdown_resume(md_content):
    """Parse resume.md into a structured dict for template rendering."""
    lines = md_content.split('\n')
    data = {
        'name': '',
        'email': {'display': '', 'href': ''},
        'phone': {'display': '', 'href': ''},
        'website': {'display': '', 'href': ''},
        'linkedin': {'display': '', 'href': ''},
        'github': {'display': '', 'href': ''},
        'location': '',
        'summary': [],
        'achievements': [],
        'work_experience': [],
        'skills': [],
        'education': [],
        'certifications': [],
    }

    current_section = None
    current_job = None
    current_school = None
    summary_lines = []

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        # Name
        if line.startswith('# ') and not data['name']:
            data['name'] = line[2:].strip()

        # Contact fields
        elif '**Email:**' in line:
            data['email'] = _parse_link(line)
        elif '**Mobile:**' in line:
            data['phone'] = _parse_link(line)
        elif '**Website:**' in line:
            data['website'] = _parse_link(line)
        elif '**LinkedIn:**' in line:
            data['linkedin'] = _parse_link(line)
        elif '**GitHub:**' in line:
            data['github'] = _parse_link(line)
        elif '**Location:**' in line:
            m = re.search(r'\*\*Location:\*\*\s*(.+)', line)
            if m:
                data['location'] = m.group(1).strip()

        # Section headers — finalize any in-progress job/school first
        elif stripped == '## Professional Summary':
            current_section = 'summary'
            summary_lines = []
        elif stripped == '## Key Achievements':
            current_section = 'achievements'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
            if summary_lines:
                data['summary'] = _parse_paragraphs(summary_lines)
        elif stripped == '## Work Experience':
            current_section = 'work'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
            if summary_lines:
                data['summary'] = _parse_paragraphs(summary_lines)
        elif stripped == '## Skills':
            current_section = 'skills'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
        elif stripped == '## Education':
            current_section = 'education'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
        elif stripped == '## Certifications':
            current_section = 'certifications'
            if current_school:
                data['education'].append(current_school)
                current_school = None

        # Job entries
        elif current_section == 'work' and line.startswith('### '):
            if current_job:
                data['work_experience'].append(current_job)
            job_line = line[4:].strip()
            match = re.match(r'^(.*\S)\s*\(([^)]+)\)\s*$', job_line)
            if match:
                full_title = match.group(1).strip()
                if ' - ' in full_title:
                    parts = full_title.split(' - ', 1)
                    company, role = parts[0].strip(), parts[1].strip()
                else:
                    company = role = full_title
                current_job = {
                    'title': full_title,
                    'company': company,
                    'role': role,
                    'dates': match.group(2).strip(),
                    'bullets': [],
                }
            else:
                print(f"  ⚠️  Warning (line {line_num}): Job entry missing dates: {job_line}")

        # Education entries
        elif current_section == 'education' and line.startswith('### '):
            if current_school:
                data['education'].append(current_school)
            current_school = {'name': line[4:].strip(), 'items': []}

        # Bullets
        elif line.startswith('- ') or line.startswith('* '):
            bullet = line[2:].strip()
            if current_section == 'work' and current_job:
                current_job['bullets'].append(bullet)
            elif current_section == 'achievements':
                data['achievements'].append(bullet)
            elif current_section == 'skills':
                group_match = re.match(r'^\*\*([^*]+):\*\*\s*(.+)$', bullet)
                if group_match:
                    label = group_match.group(1).strip()
                    items = [i.strip() for i in group_match.group(2).split(',') if i.strip()]
                    data['skills'].append({'type': 'group', 'label': label, 'items': items})
                else:
                    data['skills'].append({'type': 'flat', 'label': bullet})
            elif current_section == 'certifications':
                data['certifications'].append(bullet)
            elif current_section == 'education' and current_school:
                current_school['items'].append(bullet)

        # Summary paragraphs
        elif current_section == 'summary':
            if stripped and not line.startswith('#') and not stripped.startswith('---') and not line.startswith('**'):
                summary_lines.append(stripped)
            elif not stripped and summary_lines and summary_lines[-1] != '':
                summary_lines.append('')

    # Finalize trailing items
    if current_job:
        data['work_experience'].append(current_job)
    if current_school:
        data['education'].append(current_school)
    if summary_lines and not data['summary']:
        data['summary'] = _parse_paragraphs(summary_lines)

    return data


def _parse_paragraphs(lines):
    """Split summary lines into paragraphs on blank lines."""
    paragraphs, current = [], []
    for line in lines:
        if line == '':
            if current:
                paragraphs.append(' '.join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(' '.join(current))
    return paragraphs if paragraphs else ['']


# Keep old name as alias so existing tests importing parse_summary_paragraphs still work
parse_summary_paragraphs = _parse_paragraphs


def _build_info():
    """Return (sha, build_time) for template injection."""
    sha = os.environ.get('GITHUB_SHA', 'local')
    if sha != 'local':
        sha = sha[:7]
    build_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return sha, build_time


def render_templates(data, index_out='index.html', resume_out='resume.html', dry_run=False):
    """Render both Jinja2 templates with resume data and write output files."""
    env = Environment(loader=FileSystemLoader(REPO_ROOT), autoescape=True)
    sha, build_time = _build_info()

    context = {**data, 'build_sha': sha, 'build_time': build_time}

    index_tmpl = env.get_template('index.template.html')
    write_file(index_out, index_tmpl.render(**context), dry_run=dry_run)

    resume_tmpl = env.get_template('resume.template.html')
    write_file(resume_out, resume_tmpl.render(**context), dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser(description='Convert resume.md to HTML.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Parse and validate without writing files.')
    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - no files will be written\n")

    print("🚀 Starting resume conversion...\n")

    md_content = read_file(os.path.join(REPO_ROOT, 'resume.md'))
    print("📊 Parsing resume.md...")
    data = parse_markdown_resume(md_content)

    print("\n🔄 Rendering templates...")
    render_templates(
        data,
        index_out=os.path.join(REPO_ROOT, 'index.html'),
        resume_out=os.path.join(REPO_ROOT, 'resume.html'),
        dry_run=args.dry_run,
    )

    print("\n" + "=" * 50)
    print("✨ DRY RUN COMPLETE" if args.dry_run else "✨ SUCCESS")
    print("=" * 50)
    print(f"  👤 Name: {data['name'] or '(not set)'}")
    print(f"  📍 Location: {data['location'] or '(not set)'}")
    print(f"  📝 Summary: {len(data['summary'])} paragraph(s)")
    print(f"  🏆 Key Achievements: {len(data['achievements'])} item(s)")
    print(f"  💼 Work Experience: {len(data['work_experience'])} job(s)")
    print(f"  🛠️  Skills: {len(data['skills'])} item(s)")
    print(f"  🎓 Education: {len(data['education'])} school(s)")
    print(f"  📜 Certifications: {len(data['certifications'])} item(s)")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    main()
