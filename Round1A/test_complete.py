#!/usr/bin/env python3
"""
Complete test to verify all components work together.
"""
import json
import os
from src.pdf_extractor import TextBlock
from src.heading_detector import HeadingDetector
from src.title_extractor import TitleExtractor
from src.output_formatter import OutputFormatter

def create_mock_text_blocks():
    """Create mock text blocks that simulate a PDF document."""
    blocks = [
        # Title (large font, page 1)
        TextBlock("Understanding Artificial Intelligence", 24.0, "Arial-Bold", 16, (50, 100, 400, 130), 1),
        
        # H1 heading (large font, bold)
        TextBlock("1. Introduction", 18.0, "Arial-Bold", 16, (50, 200, 200, 220), 1),
        
        # Regular text
        TextBlock("This document provides an overview of artificial intelligence concepts.", 12.0, "Arial", 0, (50, 240, 500, 260), 1),
        
        # H2 heading
        TextBlock("1.1 What is AI?", 16.0, "Arial-Bold", 16, (50, 300, 250, 320), 1),
        
        # More regular text
        TextBlock("Artificial Intelligence refers to machine intelligence.", 12.0, "Arial", 0, (50, 340, 450, 360), 1),
        
        # H1 heading on page 2
        TextBlock("2. Machine Learning", 18.0, "Arial-Bold", 16, (50, 100, 300, 120), 2),
        
        # H2 heading
        TextBlock("2.1 Supervised Learning", 16.0, "Arial-Bold", 16, (50, 160, 350, 180), 2),
        
        # H3 heading
        TextBlock("2.1.1 Classification", 14.0, "Arial-Bold", 16, (50, 220, 280, 240), 2),
        
        # Regular text
        TextBlock("Classification is a type of supervised learning.", 12.0, "Arial", 0, (50, 260, 400, 280), 2),
    ]
    return blocks

def test_complete_pipeline():
    """Test the complete pipeline with mock data."""
    print("Testing Complete PagePilot Pipeline...")
    
    # Create mock text blocks
    text_blocks = create_mock_text_blocks()
    print(f"✓ Created {len(text_blocks)} mock text blocks")
    
    # Test title extraction
    title_extractor = TitleExtractor()
    title = title_extractor.extract_title(text_blocks)
    print(f"✓ Extracted title: '{title}'")
    
    # Test heading detection
    heading_detector = HeadingDetector()
    headings = heading_detector.detect_headings(text_blocks)
    print(f"✓ Detected {len(headings)} headings")
    
    for heading in headings:
        print(f"  - {heading.level}: '{heading.text}' (page {heading.page}, confidence: {heading.confidence:.2f})")
    
    # Test output formatting
    output_formatter = OutputFormatter()
    output_data = output_formatter.format_output(title, headings)
    print("✓ Formatted output data")
    
    # Save test output
    test_output_path = "test_output.json"
    output_formatter.save_to_json(output_data, test_output_path)
    print(f"✓ Saved test output to {test_output_path}")
    
    # Verify output format
    with open(test_output_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    
    print("\n--- Generated JSON Output ---")
    print(json.dumps(saved_data, indent=2))
    
    # Verify structure
    assert "title" in saved_data
    assert "outline" in saved_data
    assert isinstance(saved_data["outline"], list)
    
    for item in saved_data["outline"]:
        assert "level" in item
        assert "text" in item
        assert "page" in item
        assert item["level"] in ["H1", "H2", "H3"]
    
    print("\n✓ Output format validation passed")
    
    # Clean up
    os.remove(test_output_path)
    print("✓ Test file cleaned up")
    
    print("\n🎉 Complete pipeline test passed successfully!")

if __name__ == "__main__":
    test_complete_pipeline()
