#!/usr/bin/env python3
"""
Test Round1A integration manually.
"""
import sys
import os
from pathlib import Path

# Add Round1A to path
round1a_path = str(Path(__file__).parent.parent / "Round1A")
print(f"Adding Round1A path: {round1a_path}")
sys.path.append(round1a_path)

# Test if we can import Round1A
try:
    sys.path.append(str(Path(__file__).parent.parent / "Round1A" / "src"))
    from outline_extractor import OutlineExtractor
    print("✅ Successfully imported OutlineExtractor from Round1A")
    
    # Test extraction
    extractor = OutlineExtractor()
    pdf_path = "../Round1A/input/YugendraN_InternshalaResume.pdf"
    
    if os.path.exists(pdf_path):
        print(f"✅ PDF file found: {pdf_path}")
        
        # Extract outline
        result = extractor.extract_outline(pdf_path)
        print(f"✅ Extraction successful!")
        print(f"Title: {result['title']}")
        print(f"Sections found: {len(result['outline'])}")
        
        # Show first few sections
        for i, section in enumerate(result['outline'][:5]):
            print(f"  {i+1}. {section['level']}: {section['text']} (page {section['page']})")
        
        if len(result['outline']) > 5:
            print(f"  ... and {len(result['outline']) - 5} more sections")
            
    else:
        print(f"❌ PDF file not found: {pdf_path}")
        
except ImportError as e:
    print(f"❌ Failed to import Round1A: {e}")
except Exception as e:
    print(f"❌ Error during extraction: {e}")

# Test the actual path resolution
print(f"\nPath debugging:")
print(f"Current file: {__file__}")
print(f"Parent: {Path(__file__).parent}")
print(f"Parent.parent: {Path(__file__).parent.parent}")
print(f"Round1A path: {Path(__file__).parent.parent / 'Round1A'}")
print(f"Round1A exists: {(Path(__file__).parent.parent / 'Round1A').exists()}")
