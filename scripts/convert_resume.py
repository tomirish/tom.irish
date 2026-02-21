#!/usr/bin/env python3
"""
Convert resume.md to HTML by dynamically regenerating all content sections.

Reads resume.md (the single source of truth) and index.html (the styled
template), then uses BeautifulSoup to replace every content section in the
HTML with whatever is currently in the markdown. The result is written back
to index.html. Styling and structure are preserved; only text content changes.

The script locates HTML elements by their id attributes. If the template is
modified and an expected id is missing, the script exits with a clear error
rather than silently producing broken output.

Usage:
    python3 scripts/convert_resume.py            # normal run, updates index.html
    python3 scripts/convert_resume.py --dry-run  # parse only, no files written
"""

import argparse
import re
import sys
from bs4 import BeautifulSoup

def read_file(filepath):
    """Read content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {filepath}")
        print(f"   Current directory should contain: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: Could not read {filepath}: {e}")
        sys.exit(1)

def write_file(filepath, content, dry_run=False):
    """Write content to a file, or skip writing if dry_run is True."""
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

def parse_markdown_resume(md_content):
    """
    Parse the markdown resume into structured sections.
    Returns a dict with all the resume data.
    """
    lines = md_content.split('\n')
    data = {
        'location': '',
        'summary': [],
        'work_experience': [],
        'skills': [],
        'education': [],
        'certifications': []
    }
    
    current_section = None
    current_job = None
    current_school = None
    summary_lines = []
    
    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        # Extract location from the header area
        if '**Location:**' in line:
            match = re.search(r'\*\*Location:\*\*\s*(.+)', line)
            if match:
                data['location'] = match.group(1).strip()
                print(f"  📍 Found location: {data['location']}")
        
        # Section headers
        elif line_stripped == '## Professional Summary':
            current_section = 'summary'
            summary_lines = []
            print(f"  📝 Parsing Professional Summary (line {line_num})")
        elif line_stripped == '## Work Experience':
            current_section = 'work'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
            # Finalize summary
            if summary_lines:
                data['summary'] = parse_summary_paragraphs(summary_lines)
            print(f"  💼 Parsing Work Experience (line {line_num})")
        elif line_stripped == '## Skills':
            current_section = 'skills'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
            print(f"  🛠️  Parsing Skills (line {line_num})")
        elif line_stripped == '## Education':
            current_section = 'education'
            if current_job:
                data['work_experience'].append(current_job)
                current_job = None
            print(f"  🎓 Parsing Education (line {line_num})")
        elif line_stripped == '## Certifications':
            current_section = 'certifications'
            if current_school:
                data['education'].append(current_school)
                current_school = None
            print(f"  📜 Parsing Certifications (line {line_num})")
        
        # Job titles in work experience
        elif current_section == 'work' and line.startswith('### '):
            if current_job:
                data['work_experience'].append(current_job)
            
            job_line = line.replace('### ', '').strip()
            # Parse: "Expeditors - Senior Manager (2025 - Present)"
            # Use a greedy first group so we always match the LAST set of parentheses.
            # This handles job titles that themselves contain parentheses, e.g.
            # "Manager (Operations) - ACME (2020 - 2022)" correctly captures
            # "Manager (Operations) - ACME" as title and "2020 - 2022" as dates.
            match = re.match(r'^(.*\S)\s*\(([^)]+)\)\s*$', job_line)
            if match:
                current_job = {
                    'title': match.group(1).strip(),
                    'dates': match.group(2).strip(),
                    'bullets': []
                }
                print(f"     • Job: {current_job['title']}")
            else:
                print(f"  ⚠️  Warning (line {line_num}): Job entry missing dates: {job_line}")
        
        # Education institutions
        elif current_section == 'education' and line.startswith('### '):
            if current_school:
                data['education'].append(current_school)
            
            school_line = line.replace('### ', '').strip()
            current_school = {
                'name': school_line,
                'items': []
            }
            print(f"     • School: {school_line}")
        
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            bullet = line[2:].strip()
            if current_section == 'work' and current_job:
                current_job['bullets'].append(bullet)
            elif current_section == 'skills':
                data['skills'].append(bullet)
            elif current_section == 'certifications':
                data['certifications'].append(bullet)
            elif current_section == 'education' and current_school:
                current_school['items'].append(bullet)
        
        # Regular paragraphs for summary
        elif current_section == 'summary':
            if line_stripped and not line.startswith('#') and not line.startswith('---') and not line.startswith('**'):
                summary_lines.append(line_stripped)
            elif not line_stripped and summary_lines and summary_lines[-1] != '':
                # Empty line = paragraph break
                summary_lines.append('')
    
    # Add last job if exists
    if current_job:
        data['work_experience'].append(current_job)
    
    # Add last school if exists
    if current_school:
        data['education'].append(current_school)
    
    # Finalize summary if we haven't hit another section
    if summary_lines and not data['summary']:
        data['summary'] = parse_summary_paragraphs(summary_lines)
    
    return data

def parse_summary_paragraphs(lines):
    """
    Parse summary lines into paragraphs, respecting blank line breaks.
    """
    paragraphs = []
    current_para = []
    
    for line in lines:
        if line == '':  # Empty line = paragraph break
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        else:
            current_para.append(line)
    
    # Add last paragraph
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs if paragraphs else ['']

def validate_html_structure(soup):
    """
    Validate that the HTML has all required elements for resume generation.
    Returns (is_valid, missing_elements)
    """
    required_ids = [
        'resume-buttons-contact-2',
        'resume-text-summary',
        'resume-section-work',
        'resume-divider-work',
        'resume-buttons-skills',
        'resume-section-education',
        'resume-divider-education',
        'resume-list-education-certifications'
    ]
    
    missing = []
    for elem_id in required_ids:
        if not soup.find(id=elem_id):
            missing.append(elem_id)
    
    return (len(missing) == 0, missing)

def update_html_with_data(html_content, data):
    """
    Update the HTML content using BeautifulSoup.
    Dynamically generates all work experience and education entries.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Validate HTML structure first
    print("\n🔍 Validating HTML structure...")
    is_valid, missing = validate_html_structure(soup)
    
    if not is_valid:
        print("❌ ERROR: HTML structure is missing required elements:")
        for elem_id in missing:
            print(f"   • Missing element with id='{elem_id}'")
        print("\n💡 Your index.html may have been modified.")
        print("   The conversion script expects specific HTML structure.")
        sys.exit(1)
    
    print("✅ HTML structure validated")
    
    print("\n🔄 Updating HTML sections...")
    
    # Update location
    location_elem = soup.find(id='resume-buttons-contact-2')
    if location_elem and data['location']:
        buttons = location_elem.find_all('a', class_='button')
        for btn in buttons:
            if not btn.get('href'):
                span = btn.find('span', class_='label')
                if span:
                    span.string = data['location']
                    print(f"  ✓ Updated location")
    
    # Update summary
    summary_elem = soup.find(id='resume-text-summary')
    if summary_elem and data['summary']:
        summary_elem.clear()
        for para in data['summary']:
            span = soup.new_tag('span', **{'class': 'p'})
            span.string = para
            summary_elem.append(span)
        print(f"  ✓ Updated summary ({len(data['summary'])} paragraphs)")
    
    # Update work experience - DYNAMIC GENERATION
    work_section = soup.find(id='resume-section-work')
    if work_section:
        hr = soup.find(id='resume-divider-work')
        if hr:
            # Remove all siblings after the hr
            for sibling in list(hr.find_next_siblings()):
                sibling.decompose()
            
            # Generate new work entries
            for job in data['work_experience']:
                # Create job title element
                h1 = soup.new_tag('h1', **{'class': 'style2'})
                span_outer = soup.new_tag('span', **{'class': 'p'})
                span_outer.string = job['title']
                span_outer.append(soup.new_tag('br'))
                
                span_inner = soup.new_tag('span', style='color: #474747')
                sup_tag = soup.new_tag('sup')
                sub_tag = soup.new_tag('sub')
                sub_tag.string = f"({job['dates']})"
                sup_tag.append(sub_tag)
                span_inner.append(sup_tag)
                span_outer.append(span_inner)
                h1.append(span_outer)
                
                # Insert after hr
                hr.insert_after(h1)
                
                # Create bullets element
                div = soup.new_tag('div', **{'class': 'style1 list'})
                ul = soup.new_tag('ul')
                for bullet in job['bullets']:
                    li = soup.new_tag('li')
                    p = soup.new_tag('p')
                    p.string = bullet
                    li.append(p)
                    ul.append(li)
                div.append(ul)
                
                # Insert after h1
                h1.insert_after(div)
                
                # Update hr reference for next iteration
                hr = div
            print(f"  ✓ Generated {len(data['work_experience'])} work entries")
    
    # Update skills
    skills_elem = soup.find(id='resume-buttons-skills')
    if skills_elem and data['skills']:
        skills_elem.clear()
        for i, skill in enumerate(data['skills'], 1):
            li = soup.new_tag('li')
            a = soup.new_tag('a', **{'class': f'button n{i:02d}', 'role': 'button'})
            a.string = skill
            li.append(a)
            skills_elem.append(li)
        print(f"  ✓ Updated skills ({len(data['skills'])} items)")
    
    # Update education - DYNAMIC GENERATION
    education_section = soup.find(id='resume-section-education')
    if education_section:
        hr = soup.find(id='resume-divider-education')
        if hr:
            # Remove all siblings after the hr (except certifications section)
            cert_header = soup.find(id='resume-text-education-certifications')
            
            # Remove everything between education hr and certifications
            for sibling in list(hr.find_next_siblings()):
                if sibling == cert_header:
                    break
                sibling.decompose()
            
            # Generate new education entries
            for school in data['education']:
                # Create school name element
                p = soup.new_tag('p', **{'class': 'style2'})
                p.string = school['name']
                hr.insert_after(p)
                
                # Create items list
                div = soup.new_tag('div', **{'class': 'style1 list'})
                ul = soup.new_tag('ul')
                for item in school['items']:
                    li = soup.new_tag('li')
                    p_item = soup.new_tag('p')
                    p_item.string = item
                    li.append(p_item)
                    ul.append(li)
                div.append(ul)
                
                # Insert after school name
                p.insert_after(div)
                
                # Update hr reference
                hr = div
            print(f"  ✓ Generated {len(data['education'])} education entries")
    
    # Update certifications
    cert_list = soup.find(id='resume-list-education-certifications')
    if cert_list and data['certifications']:
        cert_list.clear()
        ul = soup.new_tag('ul')
        for cert in data['certifications']:
            li = soup.new_tag('li')
            p = soup.new_tag('p')
            p.string = cert
            li.append(p)
            ul.append(li)
        cert_list.append(ul)
        print(f"  ✓ Updated certifications ({len(data['certifications'])} items)")
    
    return str(soup)

def main():
    """Main function to convert resume.md to update index.html.

    Supports --dry-run to validate and simulate conversion without writing any files.
    """
    parser = argparse.ArgumentParser(
        description='Convert resume.md to HTML by updating index.html.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse and validate resume.md without writing index.html. '
             'Useful for checking your resume locally before committing.'
    )
    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - no files will be written\n")

    print("🚀 Starting resume conversion...\n")

    try:
        # Read files
        print("📖 Reading files...")
        html_content = read_file('index.html')
        md_content = read_file('resume.md')

        # Parse markdown
        print("\n📊 Parsing resume.md...")
        data = parse_markdown_resume(md_content)

        # Update HTML
        updated_html = update_html_with_data(html_content, data)

        # Write output (skipped in dry-run mode)
        print("\n💾 Writing output...")
        write_file('index.html', updated_html, dry_run=args.dry_run)

        # Summary
        print("\n" + "="*50)
        if args.dry_run:
            print("✨ DRY RUN COMPLETE - conversion would succeed")
        else:
            print("✨ SUCCESS! Resume converted successfully")
        print("="*50)
        print(f"  📍 Location: {data['location'] or '(not set)'}")
        print(f"  📝 Summary: {len(data['summary'])} paragraph(s)")
        print(f"  💼 Work Experience: {len(data['work_experience'])} job(s)")
        print(f"  🛠️  Skills: {len(data['skills'])} item(s)")
        print(f"  🎓 Education: {len(data['education'])} school(s)")
        print(f"  📜 Certifications: {len(data['certifications'])} item(s)")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
