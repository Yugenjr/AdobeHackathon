#!/usr/bin/env python3
"""
Simple test to check if we can read PDF content at all.
"""

import fitz
import os

def simple_pdf_test():
    """Test basic PDF reading."""
    pdf_path = 'input/Learn Acrobat - Fill and Sign.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"🔍 Testing basic PDF reading: {pdf_path}")
    
    try:
        # Try to open the PDF
        print("1. Opening PDF...")
        doc = fitz.open(pdf_path)
        print(f"   ✅ PDF opened successfully")
        
        # Try to get page count
        print("2. Getting page count...")
        try:
            page_count = len(doc)
            print(f"   ✅ Page count: {page_count}")
        except Exception as e:
            print(f"   ❌ Error getting page count: {e}")
            doc.close()
            return
        
        # Try to get first page
        print("3. Getting first page...")
        try:
            page = doc[0]
            print(f"   ✅ First page accessed")
        except Exception as e:
            print(f"   ❌ Error accessing first page: {e}")
            doc.close()
            return
        
        # Try to extract simple text
        print("4. Extracting simple text...")
        try:
            text = page.get_text()
            print(f"   ✅ Text extracted: {len(text)} characters")
            if text.strip():
                lines = text.strip().split('\n')[:5]
                print("   📝 First 5 lines:")
                for i, line in enumerate(lines, 1):
                    print(f"      {i}. {line[:80]}...")
            else:
                print("   ⚠️  No text found")
        except Exception as e:
            print(f"   ❌ Error extracting text: {e}")
        
        # Try to extract structured text
        print("5. Extracting structured text...")
        try:
            text_dict = page.get_text("dict")
            print(f"   ✅ Structured text extracted")
            
            # Count text blocks
            block_count = 0
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    block_count += 1
            print(f"   📊 Text blocks found: {block_count}")
            
            # Show first few text spans
            span_count = 0
            print("   📝 First few text spans:")
            for block in text_dict.get("blocks", []):
                if "lines" in block and span_count < 5:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip() and span_count < 5:
                                print(f"      {span_count + 1}. \"{span['text'].strip()}\" (size: {span['size']:.1f})")
                                span_count += 1
                                
        except Exception as e:
            print(f"   ❌ Error extracting structured text: {e}")
        
        doc.close()
        print("✅ PDF processing completed successfully")
        
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")

if __name__ == "__main__":
    simple_pdf_test()
