#!/usr/bin/env python3
"""
Debug script to check if content is coming from real PDF extraction or hardcoded fallback.
"""

from backend.round1b.pdf_processor import PDFProcessor
import os

def debug_content_source():
    """Debug where the content is actually coming from."""
    pdf_path = 'input/Learn Acrobat - Fill and Sign.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"🔍 Debugging content source for: {pdf_path}")
    
    try:
        processor = PDFProcessor()
        result = processor.extract_document_structure(pdf_path)
        
        print(f"📊 Processing metadata:")
        print(f"   Real content used: {result['processing_metadata'].get('real_content_used', False)}")
        print(f"   Fallback used: {result['processing_metadata'].get('fallback_used', False)}")
        print(f"   Error: {result['processing_metadata'].get('error', 'None')}")
        
        print(f"\n📝 First 3 sections:")
        for i, section in enumerate(result['sections'][:3], 1):
            print(f"   {i}. \"{section.title}\" (Page {section.page})")
            print(f"      Content: \"{section.content_preview[:100]}...\"")
            
            # Check if content looks hardcoded
            if "Detailed instructions and best practices for" in section.content_preview:
                print(f"      ⚠️  HARDCODED TEMPLATE DETECTED!")
            elif "To create an interactive form" in section.content_preview:
                print(f"      ⚠️  HARDCODED TEMPLATE DETECTED!")
            elif section.content_preview.startswith("Adobe Acrobat functionality"):
                print(f"      ⚠️  HARDCODED TEMPLATE DETECTED!")
            else:
                print(f"      ✅ Appears to be real PDF content")
            print()
            
    except Exception as e:
        print(f"❌ Error during debugging: {e}")

if __name__ == "__main__":
    debug_content_source()
