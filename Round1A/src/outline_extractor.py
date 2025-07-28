"""
Main outline extraction pipeline.
"""
import os
from typing import Dict, Any
from .pdf_extractor import PDFExtractor
from .heading_detector import HeadingDetector
from .title_extractor import TitleExtractor
from .output_formatter import OutputFormatter


class OutlineExtractor:
    """Main class that orchestrates the outline extraction process."""
    
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.heading_detector = HeadingDetector()
        self.title_extractor = TitleExtractor()
        self.output_formatter = OutputFormatter()
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Extract outline from a single PDF file."""
        try:
            # Step 1: Extract text blocks with formatting information
            text_blocks = self.pdf_extractor.extract_text_blocks(pdf_path)
            
            if not text_blocks:
                return {
                    "title": "Empty Document",
                    "outline": []
                }
            
            # Step 2: Extract title
            title = self.title_extractor.extract_title(text_blocks)
            
            # Step 3: Detect headings
            heading_candidates = self.heading_detector.detect_headings(text_blocks)
            
            # Step 4: Format output
            output_data = self.output_formatter.format_output(title, heading_candidates)
            
            return output_data
            
        except Exception as e:
            # Return error information in a structured way
            return {
                "title": f"Error processing document: {str(e)}",
                "outline": []
            }
    
    def process_directory(self, input_dir: str, output_dir: str) -> None:
        """Process all PDF files in the input directory."""
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all PDF files in input directory
        pdf_files = []
        if os.path.exists(input_dir):
            for filename in os.listdir(input_dir):
                if filename.lower().endswith('.pdf'):
                    pdf_files.append(filename)
        
        if not pdf_files:
            print(f"No PDF files found in {input_dir}")
            return
        
        print(f"Found {len(pdf_files)} PDF file(s) to process")
        
        # Process each PDF file
        for pdf_filename in pdf_files:
            try:
                pdf_path = os.path.join(input_dir, pdf_filename)
                
                # Generate output filename (replace .pdf with .json)
                json_filename = os.path.splitext(pdf_filename)[0] + '.json'
                json_path = os.path.join(output_dir, json_filename)
                
                print(f"Processing: {pdf_filename}")
                
                # Extract outline
                outline_data = self.extract_outline(pdf_path)
                
                # Save to JSON
                self.output_formatter.save_to_json(outline_data, json_path)
                
                print(f"Generated: {json_filename}")
                
            except Exception as e:
                print(f"Error processing {pdf_filename}: {str(e)}")
                
                # Create error output file
                error_data = {
                    "title": f"Error processing {pdf_filename}",
                    "outline": [],
                    "error": str(e)
                }
                
                json_filename = os.path.splitext(pdf_filename)[0] + '.json'
                json_path = os.path.join(output_dir, json_filename)
                
                try:
                    self.output_formatter.save_to_json(error_data, json_path)
                except:
                    pass  # If we can't even save the error, just continue
        
        print("Processing complete!")
