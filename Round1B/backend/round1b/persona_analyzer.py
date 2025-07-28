"""
Core PersonaAnalyzer for Round 1B standalone persona-aware document analyst.
Orchestrates PDF processing, NLP analysis, and intelligent section ranking.
"""
import logging
import time
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

from .pdf_processor import PDFProcessor
from .nlp_pipeline import NLPPipeline
from .section_ranker import SectionRanker

logger = logging.getLogger(__name__)


class PersonaAnalyzer:
    """
    Core analyzer that orchestrates persona-aware document analysis.
    Completely independent from Round 1A.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the persona analyzer.
        
        Args:
            model_name: Sentence transformer model name (default: all-MiniLM-L6-v2)
        """
        self.pdf_processor = PDFProcessor()
        self.nlp_pipeline = NLPPipeline(model_name)
        self.section_ranker = SectionRanker()
        
        logger.info("✅ PersonaAnalyzer initialized with standalone components")
    
    def analyze_documents(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze documents based on persona and job requirements.
        
        Args:
            input_data: Dictionary containing persona, job_to_be_done, and documents
            
        Returns:
            Analysis results with metadata, sections, and subsections
        """
        start_time = time.time()
        
        try:
            # Extract input parameters
            persona = input_data['persona']
            job_to_be_done = input_data['job_to_be_done']
            documents = input_data['documents']
            
            logger.info(f"Analyzing {len(documents)} documents for persona: {persona}")
            logger.info(f"Job to be done: {job_to_be_done}")
            
            # Process all documents
            all_sections = []
            document_names = []
            processing_errors = []
            
            for doc in documents:
                doc_name = doc['name']
                doc_path = doc['path']
                document_names.append(doc_name)
                
                try:
                    # Extract document structure
                    doc_structure = self.pdf_processor.extract_document_structure(doc_path)
                    
                    # Convert sections to analysis format
                    doc_sections = self._convert_sections_for_analysis(
                        doc_structure['sections'], doc_name
                    )
                    
                    all_sections.extend(doc_sections)
                    
                    logger.debug(f"Extracted {len(doc_sections)} sections from {doc_name}")
                    
                except Exception as e:
                    error_msg = f"Error processing {doc_name}: {str(e)}"
                    logger.error(error_msg)
                    processing_errors.append(error_msg)
                    
                    # Add fallback section for failed documents
                    fallback_section = {
                        'title': f"Error processing {doc_name}",
                        'level': 'H1',
                        'page': 1,
                        'confidence': 0.0,
                        'content_preview': f"Failed to process: {str(e)}",
                        'document_name': doc_name
                    }
                    all_sections.append(fallback_section)
            
            if not all_sections:
                logger.warning("No sections extracted from any document")
                return self._create_empty_result(persona, job_to_be_done, document_names, processing_errors)
            
            # Perform NLP-based ranking
            nlp_results = self.nlp_pipeline.rank_sections_by_relevance(
                all_sections, persona, job_to_be_done
            )
            
            # Extract NLP scores for multi-factor ranking
            nlp_scores = [score for _, score, _ in nlp_results]
            
            # Apply advanced multi-factor ranking
            ranked_sections = self.section_ranker.rank_sections(
                all_sections, persona, job_to_be_done, nlp_scores
            )
            
            # Select top sections and create subsection analysis
            top_sections = ranked_sections[:20]  # Top 20 sections
            subsection_analysis = self._create_subsection_analysis(top_sections[:10])  # Top 10 for detailed analysis
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create result structure
            result = {
                'metadata': {
                    'documents': document_names,
                    'persona': persona,
                    'job_to_be_done': job_to_be_done,
                    'processing_time': processing_time,
                    'nlp_model_info': self.nlp_pipeline.get_model_info(),
                    'errors': processing_errors if processing_errors else None
                },
                'sections': top_sections,
                'subsections': subsection_analysis
            }
            
            logger.info(f"✅ Analysis complete: {len(top_sections)} sections extracted")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Error during analysis: {e}")
            
            return {
                'metadata': {
                    'documents': input_data.get('documents', []),
                    'persona': input_data.get('persona', ''),
                    'job_to_be_done': input_data.get('job_to_be_done', ''),
                    'processing_time': processing_time,
                    'nlp_model_info': self.nlp_pipeline.get_model_info(),
                    'error': str(e)
                },
                'sections': [],
                'subsections': []
            }
    
    def _convert_sections_for_analysis(self, sections: List[Any], document_name: str) -> List[Dict[str, Any]]:
        """Convert PDF processor sections to analysis format."""
        converted_sections = []
        
        for section in sections:
            converted_section = {
                'title': section.title,
                'level': section.level,
                'page': section.page,
                'confidence': section.confidence,
                'content_preview': section.content_preview,
                'document_name': document_name
            }
            converted_sections.append(converted_section)
        
        return converted_sections
    
    def _create_subsection_analysis(self, top_sections: List[Tuple[Dict[str, Any], float, str]]) -> List[Tuple[Dict[str, Any], float, str]]:
        """Create detailed subsection analysis for top sections."""
        subsection_analysis = []
        
        for section_data, score, explanation in top_sections:
            # Create enhanced analysis for subsection
            enhanced_section = section_data.copy()
            
            # Add additional analysis metadata
            enhanced_section['analysis_type'] = 'detailed'
            enhanced_section['ranking_factors'] = self._extract_ranking_factors(explanation)
            
            subsection_analysis.append((enhanced_section, score, explanation))
        
        return subsection_analysis
    
    def _extract_ranking_factors(self, explanation: str) -> List[str]:
        """Extract ranking factors from explanation text."""
        factors = []
        
        if 'high semantic' in explanation:
            factors.append('semantic_similarity')
        if 'domain-specific' in explanation:
            factors.append('domain_relevance')
        if 'relevant to job' in explanation:
            factors.append('job_relevance')
        if 'early document' in explanation:
            factors.append('position_bonus')
        if 'importance section' in explanation:
            factors.append('section_importance')
        
        return factors
    
    def _create_empty_result(self, persona: str, job_to_be_done: str, 
                           document_names: List[str], errors: List[str]) -> Dict[str, Any]:
        """Create empty result structure when no sections are found."""
        return {
            'metadata': {
                'documents': document_names,
                'persona': persona,
                'job_to_be_done': job_to_be_done,
                'processing_time': 0.0,
                'nlp_model_info': self.nlp_pipeline.get_model_info(),
                'errors': errors
            },
            'sections': [],
            'subsections': []
        }
    
    def get_analysis_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the analysis results."""
        metadata = result.get('metadata', {})
        sections = result.get('sections', [])
        subsections = result.get('subsections', [])
        
        summary = {
            'documents_processed': len(metadata.get('documents', [])),
            'total_sections_analyzed': len(sections),
            'relevant_sections_extracted': len(sections),
            'subsections_analyzed': len(subsections),
            'processing_time': metadata.get('processing_time', 0.0),
            'nlp_model': metadata.get('nlp_model_info', {}).get('model_name', 'Unknown'),
            'top_sections': []
        }
        
        # Add top 3 sections to summary
        for i, (section_data, score, explanation) in enumerate(sections[:3]):
            summary['top_sections'].append({
                'rank': i + 1,
                'title': section_data.get('title', 'Unknown'),
                'score': round(score, 3),
                'explanation': explanation
            })
        
        return summary
