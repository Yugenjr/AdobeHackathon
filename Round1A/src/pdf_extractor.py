"""
PDF text extraction module with font and positioning information.
"""
import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple
import re


class TextBlock:
    """Represents a text block with formatting information."""
    
    def __init__(self, text: str, font_size: float, font_name: str, 
                 font_flags: int, bbox: Tuple[float, float, float, float], 
                 page_num: int):
        self.text = text.strip()
        self.font_size = font_size
        self.font_name = font_name
        self.font_flags = font_flags
        self.bbox = bbox  # (x0, y0, x1, y1)
        self.page_num = page_num
        
        # Derived properties
        self.is_bold = bool(font_flags & 2**4)
        self.is_italic = bool(font_flags & 2**1)
        self.x_pos = bbox[0]
        self.y_pos = bbox[1]
        self.width = bbox[2] - bbox[0]
        self.height = bbox[3] - bbox[1]


class PDFExtractor:
    """Extracts structured text information from PDF files."""
    
    def __init__(self):
        self.text_blocks: List[TextBlock] = []
        
    def extract_text_blocks(self, pdf_path: str) -> List[TextBlock]:
        """Extract all text blocks with formatting information from PDF."""
        self.text_blocks = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get text with font information
                text_dict = page.get_text("dict")
                
                for block in text_dict["blocks"]:
                    if "lines" in block:  # Text block
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["text"].strip():  # Skip empty text
                                    text_block = TextBlock(
                                        text=span["text"],
                                        font_size=span["size"],
                                        font_name=span["font"],
                                        font_flags=span["flags"],
                                        bbox=span["bbox"],
                                        page_num=page_num + 1  # 1-based page numbering
                                    )
                                    self.text_blocks.append(text_block)
            
            doc.close()
            return self.text_blocks
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def get_page_text_blocks(self, page_num: int) -> List[TextBlock]:
        """Get all text blocks for a specific page."""
        return [block for block in self.text_blocks if block.page_num == page_num]
    
    def get_font_statistics(self) -> Dict[str, Any]:
        """Get statistics about fonts used in the document."""
        if not self.text_blocks:
            return {}
            
        font_sizes = [block.font_size for block in self.text_blocks]
        font_names = [block.font_name for block in self.text_blocks]
        
        return {
            "avg_font_size": sum(font_sizes) / len(font_sizes),
            "max_font_size": max(font_sizes),
            "min_font_size": min(font_sizes),
            "unique_font_sizes": sorted(list(set(font_sizes)), reverse=True),
            "unique_font_names": list(set(font_names)),
            "total_blocks": len(self.text_blocks)
        }
