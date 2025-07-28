"""
Title extraction logic for PDF documents.
"""
import re
from typing import List, Optional
from .pdf_extractor import TextBlock


class TitleExtractor:
    """Extracts document title using multiple heuristics."""
    
    def __init__(self):
        # Common title indicators
        self.title_keywords = {
            'title', 'report', 'paper', 'study', 'analysis', 'research',
            'guide', 'manual', 'handbook', 'documentation', 'specification'
        }
        
        # Words that typically don't appear in titles
        self.non_title_words = {
            'page', 'chapter', 'section', 'figure', 'table', 'appendix',
            'contents', 'index', 'bibliography', 'references', 'abstract',
            'introduction', 'conclusion', 'summary', 'acknowledgments'
        }
    
    def extract_title(self, text_blocks: List[TextBlock]) -> str:
        """Extract the document title using multiple strategies."""
        if not text_blocks:
            return "Untitled Document"
        
        # Strategy 1: Look for title on first page with largest font
        first_page_title = self._extract_from_first_page(text_blocks)
        if first_page_title:
            return first_page_title
        
        # Strategy 2: Look for text blocks that look like titles
        pattern_title = self._extract_by_patterns(text_blocks)
        if pattern_title:
            return pattern_title
        
        # Strategy 3: Use the first substantial text block
        fallback_title = self._extract_fallback(text_blocks)
        return fallback_title or "Untitled Document"
    
    def _extract_from_first_page(self, text_blocks: List[TextBlock]) -> Optional[str]:
        """Extract title from the first page using font size and positioning."""
        first_page_blocks = [block for block in text_blocks if block.page_num == 1]
        
        if not first_page_blocks:
            return None
        
        # Find the largest font size on first page
        max_font_size = max(block.font_size for block in first_page_blocks)
        
        # Get blocks with the largest font size
        largest_font_blocks = [
            block for block in first_page_blocks 
            if abs(block.font_size - max_font_size) < 0.1
        ]
        
        # Filter out blocks that are likely not titles
        title_candidates = []
        for block in largest_font_blocks:
            if self._is_likely_title(block):
                title_candidates.append(block)
        
        if not title_candidates:
            # If no good candidates, use the largest font blocks
            title_candidates = largest_font_blocks
        
        # Sort by vertical position (top to bottom) and take the first
        title_candidates.sort(key=lambda x: x.y_pos)
        
        # Combine multiple blocks if they seem to be part of the same title
        return self._combine_title_blocks(title_candidates[:3])  # Max 3 blocks
    
    def _extract_by_patterns(self, text_blocks: List[TextBlock]) -> Optional[str]:
        """Extract title using text patterns and keywords."""
        for block in text_blocks[:20]:  # Check first 20 blocks
            text = block.text.strip()
            
            # Skip very short or very long text
            if len(text) < 5 or len(text) > 200:
                continue
            
            # Check for title-like patterns
            if self._matches_title_pattern(text):
                return self._clean_title(text)
        
        return None
    
    def _extract_fallback(self, text_blocks: List[TextBlock]) -> Optional[str]:
        """Fallback strategy: use first substantial text block."""
        for block in text_blocks[:10]:  # Check first 10 blocks
            text = block.text.strip()
            
            # Look for substantial text that could be a title
            if (10 <= len(text) <= 150 and 
                not self._contains_non_title_words(text) and
                not re.match(r'^\d+$', text)):  # Not just numbers
                return self._clean_title(text)
        
        return None
    
    def _is_likely_title(self, block: TextBlock) -> bool:
        """Check if a text block is likely to be a title."""
        text = block.text.strip()
        
        # Length check
        if len(text) < 5 or len(text) > 200:
            return False
        
        # Position check (should be near top of page)
        if block.y_pos > 400:  # Assuming page height around 800
            return False
        
        # Content check
        if self._contains_non_title_words(text):
            return False
        
        # Pattern check
        if re.match(r'^(page|chapter|section)\s+\d+', text, re.IGNORECASE):
            return False
        
        return True
    
    def _matches_title_pattern(self, text: str) -> bool:
        """Check if text matches common title patterns."""
        text_lower = text.lower()
        
        # Contains title keywords
        words = set(text_lower.split())
        if words.intersection(self.title_keywords):
            return True
        
        # Title case pattern
        if self._is_title_case(text):
            return True
        
        # All caps (but not too long)
        if text.isupper() and 5 <= len(text) <= 100:
            return True
        
        return False
    
    def _is_title_case(self, text: str) -> bool:
        """Check if text is in title case."""
        words = text.split()
        if len(words) < 2:
            return False
        
        # Most words should start with capital letter
        capitalized_count = sum(1 for word in words if word[0].isupper())
        return capitalized_count >= len(words) * 0.7
    
    def _contains_non_title_words(self, text: str) -> bool:
        """Check if text contains words that typically don't appear in titles."""
        text_lower = text.lower()
        words = set(text_lower.split())
        return bool(words.intersection(self.non_title_words))
    
    def _combine_title_blocks(self, blocks: List[TextBlock]) -> str:
        """Combine multiple text blocks into a single title."""
        if not blocks:
            return ""
        
        # Sort by position (left to right, top to bottom)
        blocks.sort(key=lambda x: (x.y_pos, x.x_pos))
        
        # Combine text with appropriate spacing
        title_parts = []
        for i, block in enumerate(blocks):
            text = block.text.strip()
            if text:
                # Add space if this block is on the same line as previous
                if (i > 0 and 
                    abs(block.y_pos - blocks[i-1].y_pos) < block.font_size * 0.5):
                    title_parts.append(" " + text)
                else:
                    title_parts.append(text)
        
        return self._clean_title("".join(title_parts))
    
    def _clean_title(self, title: str) -> str:
        """Clean and normalize the extracted title."""
        # Remove extra whitespace
        title = re.sub(r'\s+', ' ', title.strip())
        
        # Remove common prefixes/suffixes
        title = re.sub(r'^(title:\s*|subject:\s*)', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*(\.pdf|\.doc|\.docx)$', '', title, flags=re.IGNORECASE)
        
        # Capitalize first letter if not already
        if title and title[0].islower():
            title = title[0].upper() + title[1:]
        
        return title.strip()
