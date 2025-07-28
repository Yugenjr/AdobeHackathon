#!/usr/bin/env python3
"""
Debug the content extraction process to see why it's not finding content after headings.
"""

import fitz
import os

def debug_content_extraction():
    """Debug why content extraction after headings is failing."""
    pdf_path = 'input/Learn Acrobat - Fill and Sign.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"🔍 Debugging content extraction for: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        
        # Extract text blocks from first page
        text_blocks = []
        page = doc[0]  # First page
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            text_blocks.append({
                                'text': span["text"].strip(),
                                'font_size': span["size"],
                                'is_bold': bool(span["flags"] & 2**4),
                                'page_num': 1
                            })
        
        doc.close()
        
        print(f"📝 Found {len(text_blocks)} text blocks on first page")
        
        # Find the first heading
        avg_font_size = sum(b['font_size'] for b in text_blocks) / len(text_blocks)
        print(f"📊 Average font size: {avg_font_size:.1f}")
        
        heading_found = False
        for i, block in enumerate(text_blocks):
            is_heading = (
                (
                    (block['font_size'] > avg_font_size * 1.5 and block['is_bold']) or  # Large AND bold
                    (block['font_size'] > avg_font_size * 2.0) or  # Very large font
                    (block['is_bold'] and block['font_size'] > avg_font_size * 1.3 and len(block['text']) < 50)  # Bold, larger, and short
                ) and
                len(block['text']) > 5 and
                len(block['text']) < 100 and
                not block['text'].startswith('•') and
                not block['text'].endswith(':') and
                not block['text'].startswith('You can')  # Exclude instructional text
            )
            
            if is_heading and not heading_found:
                print(f"\n🎯 Found heading at index {i}: \"{block['text']}\"")
                print(f"   Font size: {block['font_size']:.1f}, Bold: {block['is_bold']}")
                
                # Show next 10 blocks after this heading
                print(f"\n📖 Next 10 blocks after heading:")
                for j in range(i + 1, min(i + 11, len(text_blocks))):
                    next_block = text_blocks[j]
                    is_next_heading = (
                        (
                            (next_block['font_size'] > avg_font_size * 1.5 and next_block['is_bold']) or
                            (next_block['font_size'] > avg_font_size * 2.0) or
                            (next_block['is_bold'] and next_block['font_size'] > avg_font_size * 1.3 and len(next_block['text']) < 50)
                        ) and
                        len(next_block['text']) > 5 and len(next_block['text']) < 100
                    )
                    marker = " [HEADING]" if is_next_heading else ""
                    print(f"   {j-i}. \"{next_block['text']}\" (size: {next_block['font_size']:.1f}){marker}")
                
                heading_found = True
                break
        
        if not heading_found:
            print("❌ No headings found!")
            
    except Exception as e:
        print(f"❌ Error during debugging: {e}")

if __name__ == "__main__":
    debug_content_extraction()
