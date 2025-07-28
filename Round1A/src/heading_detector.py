"""
Intelligent heading detection using multiple heuristics.
"""
import re
from typing import List, Dict, Optional, Tuple
from .pdf_extractor import TextBlock


class HeadingCandidate:
    """Represents a potential heading with confidence score."""
    
    def __init__(self, text_block: TextBlock, level: str, confidence: float):
        self.text_block = text_block
        self.level = level  # H1, H2, H3
        self.confidence = confidence
        self.text = text_block.text
        self.page = text_block.page_num


class HeadingDetector:
    """Detects headings using multiple heuristics beyond just font size."""
    
    def __init__(self):
        self.heading_patterns = [
            # Chapter/Section patterns
            r'^(chapter|section|part)\s+\d+',
            r'^\d+\.\s+',  # 1. Introduction
            r'^\d+\.\d+\s+',  # 1.1 Overview
            r'^\d+\.\d+\.\d+\s+',  # 1.1.1 Details
            r'^[A-Z][A-Z\s]{2,}$',  # ALL CAPS headings
            r'^[A-Z][a-z]+(\s+[A-Z][a-z]+)*$',  # Title Case
        ]
        
        # Common heading keywords
        self.heading_keywords = {
            'introduction', 'conclusion', 'abstract', 'summary', 'overview',
            'background', 'methodology', 'results', 'discussion', 'references',
            'appendix', 'acknowledgments', 'bibliography', 'contents', 'index'
        }
    
    def detect_headings(self, text_blocks: List[TextBlock]) -> List[HeadingCandidate]:
        """Detect headings using multiple heuristics."""
        if not text_blocks:
            return []
        
        # Get font statistics for relative comparison
        font_stats = self._get_font_statistics(text_blocks)
        
        candidates = []
        
        for i, block in enumerate(text_blocks):
            confidence = self._calculate_heading_confidence(
                block, text_blocks, i, font_stats
            )
            
            if confidence > 0.5:  # Threshold for considering as heading
                level = self._determine_heading_level(block, font_stats, confidence)
                candidates.append(HeadingCandidate(block, level, confidence))
        
        # Post-process to ensure logical hierarchy
        return self._refine_heading_hierarchy(candidates)
    
    def _calculate_heading_confidence(self, block: TextBlock, all_blocks: List[TextBlock], 
                                    index: int, font_stats: Dict) -> float:
        """Calculate confidence score for a text block being a heading."""
        confidence = 0.0
        
        # Font size heuristic (relative to document average)
        if block.font_size > font_stats['avg_font_size'] * 1.2:
            confidence += 0.3
        if block.font_size > font_stats['avg_font_size'] * 1.5:
            confidence += 0.2
        
        # Bold text heuristic
        if block.is_bold:
            confidence += 0.25
        
        # Position heuristic (left-aligned, not indented much)
        if block.x_pos < 100:  # Assuming left margin
            confidence += 0.1
        
        # Length heuristic (headings are usually shorter)
        if len(block.text) < 100:
            confidence += 0.1
        if len(block.text) < 50:
            confidence += 0.1
        
        # Pattern matching heuristic
        text_lower = block.text.lower().strip()
        for pattern in self.heading_patterns:
            if re.match(pattern, block.text, re.IGNORECASE):
                confidence += 0.3
                break
        
        # Keyword heuristic
        words = set(text_lower.split())
        if words.intersection(self.heading_keywords):
            confidence += 0.2
        
        # Standalone line heuristic (not part of paragraph)
        if self._is_standalone_line(block, all_blocks, index):
            confidence += 0.15
        
        # Case pattern heuristic
        if self._has_heading_case_pattern(block.text):
            confidence += 0.15
        
        return min(confidence, 1.0)
    
    def _determine_heading_level(self, block: TextBlock, font_stats: Dict, 
                               confidence: float) -> str:
        """Determine the heading level (H1, H2, H3) based on font size and other factors."""
        font_size_ratio = block.font_size / font_stats['avg_font_size']
        
        # Primary determination by font size
        if font_size_ratio >= 1.8 or block.font_size >= font_stats['max_font_size'] * 0.9:
            return "H1"
        elif font_size_ratio >= 1.4:
            return "H2"
        else:
            return "H3"
    
    def _is_standalone_line(self, block: TextBlock, all_blocks: List[TextBlock], 
                          index: int) -> bool:
        """Check if the text block is a standalone line (not part of a paragraph)."""
        # Check if there's significant vertical space before/after
        threshold = block.font_size * 0.5
        
        # Check previous block
        if index > 0:
            prev_block = all_blocks[index - 1]
            if (prev_block.page_num == block.page_num and 
                abs(block.y_pos - prev_block.y_pos) < threshold):
                return False
        
        # Check next block
        if index < len(all_blocks) - 1:
            next_block = all_blocks[index + 1]
            if (next_block.page_num == block.page_num and 
                abs(next_block.y_pos - block.y_pos) < threshold):
                return False
        
        return True
    
    def _has_heading_case_pattern(self, text: str) -> bool:
        """Check if text follows common heading case patterns."""
        # Title Case pattern
        words = text.split()
        if len(words) > 1:
            title_case = all(word[0].isupper() if word[0].isalpha() else True 
                           for word in words if len(word) > 3)  # Ignore short words
            if title_case:
                return True
        
        # ALL CAPS pattern
        if text.isupper() and len(text) > 3:
            return True
        
        return False
    
    def _get_font_statistics(self, text_blocks: List[TextBlock]) -> Dict:
        """Get font statistics for the document."""
        font_sizes = [block.font_size for block in text_blocks]
        
        return {
            'avg_font_size': sum(font_sizes) / len(font_sizes),
            'max_font_size': max(font_sizes),
            'min_font_size': min(font_sizes),
        }
    
    def _refine_heading_hierarchy(self, candidates: List[HeadingCandidate]) -> List[HeadingCandidate]:
        """Refine heading hierarchy to ensure logical structure."""
        if not candidates:
            return candidates
        
        # Sort by page and position
        candidates.sort(key=lambda x: (x.page, x.text_block.y_pos))
        
        # Ensure we have at least one H1
        if not any(c.level == "H1" for c in candidates):
            # Promote the highest confidence candidate to H1
            highest_conf = max(candidates, key=lambda x: x.confidence)
            highest_conf.level = "H1"
        
        return candidates
