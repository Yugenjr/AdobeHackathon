#!/usr/bin/env python3
"""
Round 1B: Standalone Persona-Aware Document Analyst
Main entry point for the completely independent persona-aware document analysis system.
"""
import argparse
import logging
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

from round1b.persona_analyzer import PersonaAnalyzer
from round1b.json_handler import JSONHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for Round 1B persona-aware document analyst."""
    parser = argparse.ArgumentParser(
        description="Round 1B: Standalone Persona-Aware Document Analyst",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --create-sample
  python main.py --input input/analysis_request.json --output output/analysis_result.json
  python main.py --input input/analysis_request.json --output output/analysis_result.json --verbose
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        default='input/analysis_request.json',
        help='Input JSON file with persona, job, and documents (default: input/analysis_request.json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output/analysis_result.json',
        help='Output JSON file for analysis results (default: output/analysis_result.json)'
    )
    
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample input JSON file and exit'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='all-MiniLM-L6-v2',
        help='Sentence transformer model name (default: all-MiniLM-L6-v2)'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Print header
    print("🧠 PagePilot Round 1B: Standalone Persona-Aware Document Analyst")
    print("=" * 70)
    
    # Handle sample creation
    if args.create_sample:
        json_handler = JSONHandler()
        try:
            json_handler.create_sample_input(args.input)
            print(f"✅ Sample input created: {args.input}")
            print("Edit the file with your persona, job, and document paths, then run again.")
            return 0
        except Exception as e:
            print(f"❌ Error creating sample: {e}")
            return 1
    
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print()
    
    try:
        # Initialize components
        print("📄 Parsing input...")
        json_handler = JSONHandler()
        input_data = json_handler.parse_input(args.input)
        
        print(f"Persona: {input_data['persona']}")
        print(f"Job: {input_data['job_to_be_done']}")
        print(f"Documents: {len(input_data['documents'])} files")
        print()
        
        # Initialize analyzer
        print("🧠 Initializing persona analyzer...")
        analyzer = PersonaAnalyzer(model_name=args.model)
        print()
        
        # Perform analysis
        print("🔍 Analyzing documents...")
        analysis_result = analyzer.analyze_documents(input_data)
        
        # Format output
        print("💾 Formatting and saving output...")
        print(f"🔍 Analysis result type: {type(analysis_result)}")
        if analysis_result:
            print(f"🔍 Analysis result keys: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not a dict'}")
        else:
            print("⚠️  Analysis result is None or empty")

        formatted_output = json_handler.format_output(analysis_result)
        print(f"🔍 Formatted output type: {type(formatted_output)}")
        json_handler.save_output(formatted_output, args.output)
        
        # Display summary
        summary = analyzer.get_analysis_summary(analysis_result)
        print()
        print("📊 Analysis Summary:")
        print("-" * 40)
        print(f"Documents processed: {summary['documents_processed']}")
        print(f"Total sections analyzed: {summary['total_sections_analyzed']}")
        print(f"Relevant sections extracted: {summary['relevant_sections_extracted']}")
        print(f"Subsections analyzed: {summary['subsections_analyzed']}")
        print(f"Processing time: {summary['processing_time']:.2f} seconds")
        print(f"NLP model: {summary['nlp_model']}")
        
        if summary['top_sections']:
            print()
            print(f"Top {len(summary['top_sections'])} most relevant sections:")
            for section in summary['top_sections']:
                print(f"  {section['rank']}. {section['title']} (score: {section['score']:.3f})")
        
        print()
        print(f"✅ Analysis complete! Results saved to: {args.output}")
        
        # Performance check
        if summary['processing_time'] <= 60:
            print(f"🚀 Performance: {summary['processing_time']:.1f}s (within 60s target)")
        else:
            print(f"⚠️  Performance: {summary['processing_time']:.1f}s (exceeds 60s target)")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Use --create-sample to generate a sample input file")
        return 1
    except ValueError as e:
        print(f"❌ Input validation error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.exception("Detailed error information:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
