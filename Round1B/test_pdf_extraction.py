#!/usr/bin/env python3
"""
Test script to check if PDF extraction is working with real content.
"""

from backend.round1b.pdf_processor import PDFProcessor
import os

def test_pdf_extraction():
    """Test PDF extraction on a real file."""
    pdf_path = 'input/Learn Acrobat - Fill and Sign.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"🔍 Testing PDF extraction on: {pdf_path}")
    
    try:
        processor = PDFProcessor()
        result = processor.extract_document_structure(pdf_path)
        
        print(f"📄 Title: {result['title']}")
        print(f"📊 Total pages: {result['total_pages']}")
        print(f"📝 Text blocks: {result['total_text_blocks']}")
        print(f"🔍 Sections found: {len(result['sections'])}")
        
        if result['sections']:
            print("\n🏆 Top sections detected:")
            for i, section in enumerate(result['sections'][:5]):
                print(f"  {i+1}. \"{section.title}\" (Page {section.page}, Confidence: {section.confidence:.2f})")
        else:
            print("❌ No sections detected")
            
        # Check if fallback was used
        if 'processing_metadata' in result and result['processing_metadata'].get('fallback_used'):
            print("⚠️  Fallback sections were used due to processing error")
        else:
            print("✅ Real PDF content was extracted successfully")
            
    except Exception as e:
        print(f"❌ Error during extraction: {e}")

if __name__ == "__main__":
    test_pdf_extraction()
