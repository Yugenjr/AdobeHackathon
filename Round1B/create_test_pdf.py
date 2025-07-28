#!/usr/bin/env python3
"""
Create a simple test PDF for Round 1B testing.
"""
import fitz  # PyMuPDF
import os

def create_test_pdf():
    """Create a simple test PDF with sections."""
    
    # Create a new PDF document
    doc = fitz.open()
    
    # Add first page
    page1 = doc.new_page()
    
    # Add title
    page1.insert_text((50, 50), "Technical Resume", fontsize=20)
    
    # Add sections
    sections = [
        ("EDUCATION", 120, 16),
        ("Bachelor of Technology in Computer Science", 140, 12),
        ("University of Technology, 2020-2024", 155, 10),
        ("GPA: 8.5/10", 170, 10),
        
        ("TECHNICAL SKILLS", 200, 16),
        ("Programming Languages: Python, Java, JavaScript", 220, 12),
        ("Frameworks: React, Django, Flask", 235, 12),
        ("Databases: MySQL, MongoDB, PostgreSQL", 250, 12),
        ("Tools: Git, Docker, AWS", 265, 12),
        
        ("PROJECTS", 300, 16),
        ("Machine Learning Classifier", 320, 14),
        ("Built a sentiment analysis model using Python and scikit-learn", 335, 10),
        ("Achieved 92% accuracy on test dataset", 350, 10),
        
        ("Web Application Development", 380, 14),
        ("Developed a full-stack e-commerce platform", 395, 10),
        ("Used React frontend with Django backend", 410, 10),
        
        ("EXPERIENCE", 450, 16),
        ("Software Engineering Intern", 470, 14),
        ("Tech Company Inc., Summer 2023", 485, 12),
        ("Worked on backend API development", 500, 10),
    ]
    
    for text, y_pos, font_size in sections:
        page1.insert_text((50, y_pos), text, fontsize=font_size)
    
    # Add second page
    page2 = doc.new_page()
    
    more_sections = [
        ("CERTIFICATIONS", 50, 16),
        ("AWS Certified Cloud Practitioner", 70, 12),
        ("Google Analytics Certified", 85, 12),
        
        ("ACHIEVEMENTS", 120, 16),
        ("Dean's List for Academic Excellence", 140, 12),
        ("Winner of University Hackathon 2023", 155, 12),
        ("Published research paper on ML algorithms", 170, 12),
        
        ("ADDITIONAL INFORMATION", 210, 16),
        ("Strong problem-solving and analytical skills", 230, 12),
        ("Excellent communication and teamwork abilities", 245, 12),
        ("Passionate about emerging technologies", 260, 12),
    ]
    
    for text, y_pos, font_size in more_sections:
        page2.insert_text((50, y_pos), text, fontsize=font_size)
    
    # Save the PDF
    output_path = "input/test_resume.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    doc.close()
    
    print(f"✅ Test PDF created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_test_pdf()
