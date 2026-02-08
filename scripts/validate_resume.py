#!/usr/bin/env python3
"""
Validate resume.md format before building.
Checks for required sections and common formatting issues.
"""

import sys
import re

def read_file(filepath):
    """Read content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {filepath}")
        print("   Make sure resume.md exists in the repository root")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: Could not read {filepath}: {e}")
        sys.exit(1)

def validate_resume(content):
    """
    Validate the resume.md structure.
    Returns (is_valid, warnings, errors)
    """
    warnings = []
    errors = []
    
    # Required sections
    required_sections = [
        "## Professional Summary",
        "## Work Experience",
        "## Skills",
        "## Education"
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # Check for location
    if "**Location:**" not in content:
        warnings.append("Location not found - resume may not display location properly")
    
    # Check work experience format
    work_section = content.split("## Work Experience")
    if len(work_section) > 1:
        work_content = work_section[1].split("##")[0]  # Get content until next section
        
        # Count job entries (### headers)
        job_count = len(re.findall(r'^### .+', work_content, re.MULTILINE))
        if job_count == 0:
            warnings.append("No job entries found in Work Experience section")
        
        # Check for date format in job titles
        job_lines = re.findall(r'^### (.+)$', work_content, re.MULTILINE)
        for job_line in job_lines:
            if not re.search(r'\(.*?\)', job_line):
                warnings.append(f"Job entry missing dates: '{job_line[:50]}...'")
    
    # Check skills section
    skills_section = content.split("## Skills")
    if len(skills_section) > 1:
        skills_content = skills_section[1].split("##")[0]
        skill_count = len(re.findall(r'^[-*] ', skills_content, re.MULTILINE))
        if skill_count == 0:
            warnings.append("No skills found in Skills section")
    
    # Check education section
    education_section = content.split("## Education")
    if len(education_section) > 1:
        education_content = education_section[1].split("##")[0]
        school_count = len(re.findall(r'^### .+', education_content, re.MULTILINE))
        if school_count == 0:
            warnings.append("No schools found in Education section")
    
    # Check for common markdown issues
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Check for tabs (should use spaces)
        if '\t' in line:
            warnings.append(f"Line {i}: Contains tab character (use spaces instead)")
        
        # Check for trailing whitespace
        if line.rstrip() != line and line.strip():
            warnings.append(f"Line {i}: Has trailing whitespace")
        
        # Check for multiple consecutive blank lines
        if i > 1 and not line.strip() and not lines[i-2].strip():
            warnings.append(f"Line {i}: Multiple consecutive blank lines")
    
    return (len(errors) == 0, warnings, errors)

def main():
    """Main validation function"""
    print("🔍 Validating resume.md...")
    print()
    
    # Read resume
    content = read_file('resume.md')
    
    # Validate
    is_valid, warnings, errors = validate_resume(content)
    
    # Report errors
    if errors:
        print("❌ VALIDATION FAILED")
        print()
        print("Errors:")
        for error in errors:
            print(f"  • {error}")
        print()
        sys.exit(1)
    
    # Report warnings
    if warnings:
        print("⚠️  VALIDATION PASSED WITH WARNINGS")
        print()
        print("Warnings (non-blocking):")
        for warning in warnings:
            print(f"  • {warning}")
        print()
    else:
        print("✅ VALIDATION PASSED")
        print()
    
    # Summary
    lines = content.split('\n')
    sections = len(re.findall(r'^## ', content, re.MULTILINE))
    
    print("Resume Summary:")
    print(f"  • Total lines: {len(lines)}")
    print(f"  • Sections: {sections}")
    print(f"  • File size: {len(content)} bytes")
    print()
    
    sys.exit(0)

if __name__ == '__main__':
    main()
