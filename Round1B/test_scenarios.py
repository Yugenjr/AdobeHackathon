#!/usr/bin/env python3
"""
Test scenarios for Round1B persona-aware document analyst.
"""
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from persona_analyzer import PersonaAnalyzer
from json_handler import JSONHandler


def create_test_scenarios():
    """Create different test scenarios for validation."""
    
    scenarios = [
        {
            "name": "Technical Recruiter - Resume Review",
            "input": {
                "persona": "Technical Recruiter and Career Advisor",
                "job_to_be_done": "Review resume for technical skills and project experience evaluation",
                "documents": [
                    {
                        "name": "YugendraN_InternshalaResume.pdf",
                        "path": "../Round1A/input/YugendraN_InternshalaResume.pdf"
                    }
                ]
            },
            "expected_sections": ["EDUCATION", "SKILLS", "PROJECTS", "TRAININGS", "PORTFOLIO"],
            "expected_relevance": "High relevance for education, skills, and projects sections"
        },
        {
            "name": "PhD Researcher - Academic Review",
            "input": {
                "persona": "PhD Researcher in Computer Science",
                "job_to_be_done": "Analyze academic background and research potential",
                "documents": [
                    {
                        "name": "YugendraN_InternshalaResume.pdf",
                        "path": "../Round1A/input/YugendraN_InternshalaResume.pdf"
                    }
                ]
            },
            "expected_sections": ["EDUCATION", "PROJECTS", "TRAININGS"],
            "expected_relevance": "High relevance for education and technical projects"
        },
        {
            "name": "Project Manager - Team Assessment",
            "input": {
                "persona": "Project Manager and Team Lead",
                "job_to_be_done": "Evaluate candidate for team collaboration and project management skills",
                "documents": [
                    {
                        "name": "YugendraN_InternshalaResume.pdf",
                        "path": "../Round1A/input/YugendraN_InternshalaResume.pdf"
                    }
                ]
            },
            "expected_sections": ["PROJECTS", "EXTRA CURRICULAR ACTIVITIES", "SKILLS"],
            "expected_relevance": "High relevance for projects and teamwork sections"
        }
    ]
    
    return scenarios


def run_test_scenario(scenario, analyzer, json_handler):
    """Run a single test scenario and analyze results."""
    print(f"\n🧪 Testing: {scenario['name']}")
    print("=" * 60)
    
    # Run analysis
    try:
        result = analyzer.analyze_documents(scenario['input'])
        formatted_result = json_handler.format_output(result)
        
        # Display results
        print(f"✅ Analysis completed successfully")
        print(f"📊 Sections found: {len(formatted_result['extracted_sections'])}")
        print(f"⏱️  Processing time: {formatted_result['metadata'].get('processing_time_seconds', 0):.3f}s")
        print(f"🧠 NLP Model: {formatted_result['metadata']['nlp_model_info']['model_name']}")
        
        # Show top sections
        sections = formatted_result['extracted_sections']
        if sections:
            print(f"\n📋 Top {min(5, len(sections))} Relevant Sections:")
            for i, section in enumerate(sections[:5], 1):
                print(f"  {i}. {section['section_title']} (page {section['page']}, score: {section['relevance_score']:.3f})")
                if 'ranking_explanation' in section:
                    print(f"     Reason: {section['ranking_explanation']}")
        
        # Validation against expectations
        print(f"\n🔍 Validation:")
        found_sections = [s['section_title'] for s in sections]
        expected = scenario['expected_sections']
        
        matches = [exp for exp in expected if any(exp.lower() in found.lower() for found in found_sections)]
        print(f"  Expected sections: {expected}")
        print(f"  Found matches: {matches}")
        print(f"  Match rate: {len(matches)}/{len(expected)} ({len(matches)/len(expected)*100:.1f}%)")
        
        return formatted_result, True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None, False


def validate_output_format(result):
    """Validate that output matches required JSON format."""
    print(f"\n🔍 Format Validation:")
    
    required_fields = {
        'metadata': ['documents', 'persona', 'job', 'timestamp', 'total_sections_analyzed'],
        'extracted_sections': ['document_name', 'page', 'section_title', 'importance_rank', 'relevance_score'],
        'subsection_analysis': ['document', 'refined_text', 'page', 'original_title', 'relevance_score']
    }
    
    validation_passed = True
    
    # Check top-level structure
    for field in ['metadata', 'extracted_sections', 'subsection_analysis']:
        if field not in result:
            print(f"  ❌ Missing top-level field: {field}")
            validation_passed = False
        else:
            print(f"  ✅ Found: {field}")
    
    # Check metadata fields
    if 'metadata' in result:
        for field in required_fields['metadata']:
            if field not in result['metadata']:
                print(f"  ❌ Missing metadata field: {field}")
                validation_passed = False
    
    # Check extracted sections format
    if 'extracted_sections' in result and result['extracted_sections']:
        section = result['extracted_sections'][0]
        for field in required_fields['extracted_sections']:
            if field not in section:
                print(f"  ❌ Missing section field: {field}")
                validation_passed = False
    
    # Check subsection analysis format
    if 'subsection_analysis' in result and result['subsection_analysis']:
        subsection = result['subsection_analysis'][0]
        for field in required_fields['subsection_analysis']:
            if field not in subsection:
                print(f"  ❌ Missing subsection field: {field}")
                validation_passed = False
    
    if validation_passed:
        print(f"  ✅ All format validations passed!")
    
    return validation_passed


def main():
    """Run comprehensive tests."""
    print("🧪 Round1B Comprehensive Testing Suite")
    print("=" * 60)
    
    # Initialize components
    analyzer = PersonaAnalyzer()
    json_handler = JSONHandler()
    
    # Get test scenarios
    scenarios = create_test_scenarios()
    
    results = []
    passed_tests = 0
    
    # Run each scenario
    for scenario in scenarios:
        result, success = run_test_scenario(scenario, analyzer, json_handler)
        if success:
            passed_tests += 1
            results.append(result)
            
            # Validate format
            format_valid = validate_output_format(result)
            if not format_valid:
                print("  ⚠️  Format validation issues detected")
    
    # Summary
    print(f"\n📊 Test Summary:")
    print("=" * 40)
    print(f"Total scenarios: {len(scenarios)}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(scenarios) - passed_tests}")
    print(f"Success rate: {passed_tests/len(scenarios)*100:.1f}%")
    
    if results:
        # Performance analysis
        times = [r['metadata'].get('processing_time_seconds', 0) for r in results]
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        print(f"\n⚡ Performance Analysis:")
        print(f"Average processing time: {avg_time:.3f}s")
        print(f"Maximum processing time: {max_time:.3f}s")
        print(f"Target compliance (≤60s): {'✅' if max_time <= 60 else '❌'}")
    
    print(f"\n🎯 Testing complete!")


if __name__ == "__main__":
    main()
