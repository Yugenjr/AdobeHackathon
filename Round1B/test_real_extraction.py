#!/usr/bin/env python3
"""
Test real PDF extraction with the processor.
"""

import fitz
import os
from backend.round1b.pdf_processor import PDFProcessor, DocumentSection

def test_real_extraction():
    """Test real PDF extraction step by step."""
    pdf_path = 'input/Learn Acrobat - Fill and Sign.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"🔍 Testing real PDF extraction: {pdf_path}")
    
    try:
        # Step 1: Basic PDF opening (we know this works)
        print("1. Opening PDF...")
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        print(f"   ✅ PDF opened: {page_count} pages")
        
        # Step 2: Extract text blocks manually
        print("2. Extracting text blocks manually...")
        text_blocks = []
        
        for page_num in range(min(3, page_count)):  # Test first 3 pages
            page = doc[page_num]
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip():
                                # Create a simple text block representation
                                text_block = {
                                    'text': span["text"].strip(),
                                    'font_size': span["size"],
                                    'is_bold': bool(span["flags"] & 2**4),
                                    'page_num': page_num + 1
                                }
                                text_blocks.append(text_block)
        
        print(f"   ✅ Extracted {len(text_blocks)} text blocks")
        
        # Step 3: Show real content
        print("3. Real content found:")
        for i, block in enumerate(text_blocks[:10]):
            bold_marker = " [BOLD]" if block['is_bold'] else ""
            print(f"   {i+1}. \"{block['text']}\" (Page {block['page_num']}, Size: {block['font_size']:.1f}){bold_marker}")
        
        # Step 4: Identify potential headings
        print("4. Potential headings (large/bold text):")
        headings = []
        avg_font_size = sum(b['font_size'] for b in text_blocks) / len(text_blocks) if text_blocks else 12
        
        for block in text_blocks:
            if (block['font_size'] > avg_font_size * 1.2 or block['is_bold']) and len(block['text']) > 5:
                headings.append(block)
        
        for i, heading in enumerate(headings[:10]):
            print(f"   {i+1}. \"{heading['text']}\" (Page {heading['page_num']}, Size: {heading['font_size']:.1f})")
        
        doc.close()
        print("✅ Real PDF content extraction successful!")
        
        return text_blocks, headings
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return [], []

if __name__ == "__main__":
    text_blocks, headings = test_real_extraction()
