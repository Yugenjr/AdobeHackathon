#!/usr/bin/env python3
"""
Basic test script to verify our PDF outline extraction works.
"""
import os
import sys
from src.outline_extractor import OutlineExtractor

def test_basic_functionality():
    """Test basic functionality without actual PDF files."""
    print("Testing PagePilot PDF Outline Extractor...")
    
    # Test initialization
    extractor = OutlineExtractor()
    print("✓ OutlineExtractor initialized successfully")
    
    # Test with empty input directory
    input_dir = "test_input"
    output_dir = "test_output"
    
    # Create test directories
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"✓ Test directories created: {input_dir}, {output_dir}")
    
    # Test processing empty directory
    extractor.process_directory(input_dir, output_dir)
    print("✓ Empty directory processing completed")
    
    # Clean up
    os.rmdir(input_dir)
    os.rmdir(output_dir)
    print("✓ Test directories cleaned up")
    
    print("\nBasic functionality test completed successfully!")

if __name__ == "__main__":
    test_basic_functionality()
