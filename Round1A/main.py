#!/usr/bin/env python3
"""
PagePilot PDF Outline Extractor
Main entry point for the application.
"""
import os
import sys
from src.outline_extractor import OutlineExtractor


def main():
    """Main function to process PDFs from input directory to output directory."""
    # Default paths for Docker container
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # For local development, use relative paths if Docker paths don't exist
    if not os.path.exists(input_dir):
        input_dir = "input"
    if not os.path.exists(output_dir):
        output_dir = "output"
    
    print("PagePilot PDF Outline Extractor")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create extractor and process files
    extractor = OutlineExtractor()
    extractor.process_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
