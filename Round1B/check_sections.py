#!/usr/bin/env python3
"""
Check the sections in the analysis result.
"""

import json

def check_sections():
    """Check what sections are in the analysis result."""
    try:
        with open('output/analysis_result.json', 'r') as f:
            data = json.load(f)
        
        print('🏆 Top 5 sections for HR professional:')
        for section in data['extracted_sections']:
            print(f'  {section["importance_rank"]}. "{section["section_title"]}" ({section["document"]}, Page {section["page_number"]})')

        print('\n📝 Subsection analysis:')
        for i, subsection in enumerate(data['subsection_analysis'][:3], 1):
            print(f'  {i}. {subsection["document"]} (Page {subsection["page_number"]})')
            print(f'     "{subsection["refined_text"]}"')
            print()

        print('\n🔍 REALITY CHECK:')
        print('Are these REAL section titles from actual PDFs?')
        print('Or are they still generated/hardcoded content?')

        # Check if content looks too generic/templated
        titles = [s["section_title"] for s in data['extracted_sections']]
        content = [s["refined_text"] for s in data['subsection_analysis']]

        print(f'\nSection titles: {titles}')
        print(f'\nFirst content sample: "{content[0] if content else "None"}"')

        # Look for signs of hardcoded content
        if any('Detailed instructions and best practices for' in c for c in content):
            print('\n⚠️  WARNING: Content contains template phrases - likely still hardcoded!')
        else:
            print('\n✅ Content appears to be real PDF text')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    check_sections()
