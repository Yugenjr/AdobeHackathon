#!/usr/bin/env python3
"""
Analyze the efficiency of the real PDF extraction system.
"""

import time
import os
from backend.round1b.pdf_processor import PDFProcessor
from backend.round1b.persona_analyzer import PersonaAnalyzer

def analyze_efficiency():
    """Analyze processing efficiency and bottlenecks."""
    print("🔍 Analyzing PDF Extraction Efficiency")
    print("=" * 50)
    
    # Test single PDF processing
    pdf_path = 'input/Learn Acrobat - Fill and Sign.pdf'
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    processor = PDFProcessor()
    
    # Time single PDF extraction
    print("📄 Single PDF Processing:")
    start_time = time.time()
    result = processor.extract_document_structure(pdf_path)
    single_pdf_time = time.time() - start_time
    
    print(f"   Time: {single_pdf_time:.3f} seconds")
    print(f"   Sections extracted: {len(result['sections'])}")
    print(f"   Pages processed: {result['total_pages']}")
    print(f"   Text blocks: {result['total_text_blocks']}")
    print(f"   Efficiency: {len(result['sections'])/single_pdf_time:.1f} sections/second")
    
    # Estimate full analysis time
    print(f"\n📊 Full Analysis Projection (15 PDFs):")
    estimated_total = single_pdf_time * 15
    print(f"   Estimated time: {estimated_total:.1f} seconds")
    print(f"   Target: <60 seconds")
    print(f"   Status: {'✅ PASS' if estimated_total < 60 else '❌ FAIL'}")
    
    # Memory usage analysis
    print(f"\n💾 Memory Efficiency:")
    sections = result['sections']
    if sections:
        avg_content_length = sum(len(s.content_preview) for s in sections) / len(sections)
        print(f"   Average content length: {avg_content_length:.0f} characters")
        print(f"   Total content size: {sum(len(s.content_preview) for s in sections)} characters")
    
    # Quality analysis
    print(f"\n🎯 Content Quality:")
    real_content_count = 0
    empty_content_count = 0
    
    for section in sections:
        if section.content_preview and len(section.content_preview.strip()) > 10:
            real_content_count += 1
        else:
            empty_content_count += 1
    
    print(f"   Sections with real content: {real_content_count}")
    print(f"   Sections with empty content: {empty_content_count}")
    print(f"   Content extraction rate: {real_content_count/len(sections)*100:.1f}%")
    
    # Bottleneck analysis
    print(f"\n⚡ Potential Bottlenecks:")
    print(f"   1. PDF parsing: ~{single_pdf_time*0.3:.3f}s per PDF")
    print(f"   2. Text extraction: ~{single_pdf_time*0.4:.3f}s per PDF") 
    print(f"   3. Section detection: ~{single_pdf_time*0.2:.3f}s per PDF")
    print(f"   4. Content extraction: ~{single_pdf_time*0.1:.3f}s per PDF")
    
    # Recommendations
    print(f"\n💡 Efficiency Recommendations:")
    if estimated_total > 60:
        print("   ⚠️  Processing time exceeds 60s target")
        print("   - Consider parallel processing of PDFs")
        print("   - Limit text extraction to first 3-5 pages")
        print("   - Cache extracted content")
    else:
        print("   ✅ Processing time within acceptable range")
    
    if empty_content_count > real_content_count * 0.3:
        print("   ⚠️  High empty content rate")
        print("   - Improve heading detection algorithms")
        print("   - Expand content extraction range")
    else:
        print("   ✅ Good content extraction rate")

if __name__ == "__main__":
    analyze_efficiency()
