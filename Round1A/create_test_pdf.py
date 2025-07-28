#!/usr/bin/env python3
"""
Create a test PDF file for testing our PagePilot extractor.
"""
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

import os

def create_simple_test_pdf():
    """Create a simple test PDF using basic text formatting."""
    if not REPORTLAB_AVAILABLE:
        print("ReportLab not available. Let me show you how to add a PDF manually...")
        print("\n📁 Manual PDF Addition Steps:")
        print("1. Find any PDF file on your computer")
        print("2. Copy it to: Documents\\augment-projects\\PagePilot\\input\\")
        print("3. Run: python main.py")
        print("4. Check the output folder for the generated JSON")
        print("\n💡 You can also download a sample PDF from:")
        print("   - https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")
        print("   - Any research paper from arXiv.org")
        print("   - Any document you have saved as PDF")
        return False
    
    # Create test PDF
    filename = "input/sample_document.pdf"
    os.makedirs("input", exist_ok=True)
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title (large font)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 100, "Understanding Machine Learning")
    
    # H1 heading
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 180, "1. Introduction")
    
    # Regular text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 220, "Machine learning is a subset of artificial intelligence that enables")
    c.drawString(50, height - 240, "computers to learn and improve from experience without being explicitly programmed.")
    
    # H2 heading
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 300, "1.1 Types of Machine Learning")
    
    # Regular text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 340, "There are three main types of machine learning:")
    c.drawString(70, height - 360, "• Supervised Learning")
    c.drawString(70, height - 380, "• Unsupervised Learning") 
    c.drawString(70, height - 400, "• Reinforcement Learning")
    
    # H3 heading
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 450, "1.1.1 Supervised Learning")
    
    # Regular text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 490, "Supervised learning uses labeled training data to learn a mapping function")
    c.drawString(50, height - 510, "from input variables to output variables.")
    
    # New page
    c.showPage()
    
    # Page 2 content
    # H1 heading
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 100, "2. Deep Learning")
    
    # Regular text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, "Deep learning is a subset of machine learning that uses neural networks")
    c.drawString(50, height - 160, "with multiple layers to model and understand complex patterns.")
    
    # H2 heading
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 220, "2.1 Neural Networks")
    
    # Regular text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 260, "Neural networks are computing systems inspired by biological neural networks.")
    
    # H2 heading
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 320, "2.2 Applications")
    
    # Regular text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 360, "Deep learning has applications in:")
    c.drawString(70, height - 380, "• Computer Vision")
    c.drawString(70, height - 400, "• Natural Language Processing")
    c.drawString(70, height - 420, "• Speech Recognition")
    
    c.save()
    print(f"✅ Created test PDF: {filename}")
    return True

if __name__ == "__main__":
    print("Creating test PDF for PagePilot...")
    if create_simple_test_pdf():
        print("\n🚀 Now run: python main.py")
        print("📄 Check the output folder for the generated JSON!")
    else:
        print("\n📝 Please add a PDF file manually to the input folder.")
