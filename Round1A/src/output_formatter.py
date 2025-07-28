"""
JSON output formatter for the extracted outline.
"""
import json
from typing import List, Dict, Any
from .heading_detector import HeadingCandidate


class OutputFormatter:
    """Formats the extracted title and headings into the required JSON structure."""
    
    def format_output(self, title: str, headings: List[HeadingCandidate]) -> Dict[str, Any]:
        """Format the output according to the required JSON structure."""
        # Sort headings by page number and position
        sorted_headings = sorted(headings, key=lambda x: (x.page, x.text_block.y_pos))
        
        # Create outline entries
        outline = []
        for heading in sorted_headings:
            outline_entry = {
                "level": heading.level,
                "text": self._clean_heading_text(heading.text),
                "page": heading.page
            }
            outline.append(outline_entry)
        
        return {
            "title": title,
            "outline": outline
        }
    
    def save_to_json(self, output_data: Dict[str, Any], output_path: str) -> None:
        """Save the formatted output to a JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error saving JSON output: {str(e)}")
    
    def _clean_heading_text(self, text: str) -> str:
        """Clean heading text for output."""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common numbering patterns if they make the text unclear
        # But keep them if they're part of the semantic meaning
        cleaned = text.strip()
        
        return cleaned
