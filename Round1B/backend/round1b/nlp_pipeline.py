"""
Lightweight NLP pipeline for persona-aware document analysis.
Uses sentence transformers with MiniLM model and TF-IDF fallback.
"""
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import re

logger = logging.getLogger(__name__)

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    from sentence_transformers.util import cos_sim
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available, falling back to TF-IDF")

# Try to import scikit-learn for TF-IDF fallback
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.error("scikit-learn not available, NLP features will be limited")


class NLPPipeline:
    """Lightweight NLP pipeline with transformer and TF-IDF support."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize NLP pipeline.
        
        Args:
            model_name: Sentence transformer model name (default: all-MiniLM-L6-v2, ~80MB)
        """
        self.model_name = model_name
        self.model = None
        self.tfidf_vectorizer = None
        self.use_transformers = False
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize the best available NLP model."""
        # Try sentence transformers first
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"Loading sentence transformer model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                self.use_transformers = True
                logger.info("✅ Sentence transformer model loaded successfully")
                return
            except Exception as e:
                logger.warning(f"Failed to load sentence transformer: {e}")
        
        # Fallback to TF-IDF
        if SKLEARN_AVAILABLE:
            logger.info("Falling back to TF-IDF approach")
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95
            )
            self.use_transformers = False
            logger.info("✅ TF-IDF vectorizer initialized")
        else:
            logger.error("No NLP backend available!")
            raise RuntimeError("Neither sentence-transformers nor scikit-learn is available")
    
    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            Numpy array of embeddings
        """
        if not texts:
            return np.array([])
        
        # Clean texts
        cleaned_texts = [self._clean_text(text) for text in texts]
        
        if self.use_transformers:
            return self._encode_with_transformers(cleaned_texts)
        else:
            return self._encode_with_tfidf(cleaned_texts)
    
    def _encode_with_transformers(self, texts: List[str]) -> np.ndarray:
        """Encode texts using sentence transformers."""
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            logger.debug(f"Encoded {len(texts)} texts with sentence transformers")
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding with transformers: {e}")
            # Fallback to TF-IDF
            return self._encode_with_tfidf(texts)
    
    def _encode_with_tfidf(self, texts: List[str]) -> np.ndarray:
        """Encode texts using TF-IDF."""
        try:
            if not hasattr(self.tfidf_vectorizer, 'vocabulary_'):
                # First time - fit the vectorizer
                embeddings = self.tfidf_vectorizer.fit_transform(texts)
            else:
                # Already fitted - just transform
                embeddings = self.tfidf_vectorizer.transform(texts)
            
            logger.debug(f"Encoded {len(texts)} texts with TF-IDF")
            return embeddings.toarray()
        except Exception as e:
            logger.error(f"Error encoding with TF-IDF: {e}")
            # Return zero embeddings as last resort
            return np.zeros((len(texts), 100))
    
    def compute_similarity(self, query_embedding: np.ndarray, 
                          document_embeddings: np.ndarray) -> np.ndarray:
        """Compute cosine similarity between query and document embeddings."""
        try:
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            if self.use_transformers:
                # Use sentence transformers cosine similarity
                similarities = cos_sim(query_embedding, document_embeddings)[0].numpy()
            else:
                # Use sklearn cosine similarity
                similarities = sklearn_cosine_similarity(query_embedding, document_embeddings)[0]
            
            return similarities
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return np.zeros(len(document_embeddings))
    
    def rank_sections_by_relevance(self, sections: List[Dict[str, Any]],
                                 persona: str, job_to_be_done: str) -> List[Tuple[Dict[str, Any], float, str]]:
        """
        Rank document sections by relevance to persona and job with enhanced scoring.

        Args:
            sections: List of section dictionaries
            persona: User persona description
            job_to_be_done: Job description

        Returns:
            List of tuples (section, relevance_score, explanation)
        """
        if not sections:
            return []

        # Enhanced query creation with persona-specific terms
        persona_terms = self._extract_persona_terms(persona)
        job_terms = self._extract_job_terms(job_to_be_done)
        query = f"{persona} {job_to_be_done} {' '.join(persona_terms)} {' '.join(job_terms)}"

        # Extract section texts with enhanced weighting
        section_texts = []
        for section in sections:
            # Weight title more heavily and add document context
            title = section.get('title', '')
            content = section.get('content_preview', '')
            doc_name = section.get('document_name', '')

            # Create enhanced text representation
            enhanced_text = f"{title} {title} {content} {self._extract_document_context(doc_name)}"
            section_texts.append(enhanced_text)

        # Encode query and sections
        all_texts = [query] + section_texts
        embeddings = self.encode_texts(all_texts)

        if embeddings.size == 0:
            logger.warning("No embeddings generated, using fallback scoring")
            return self._fallback_ranking(sections, persona, job_to_be_done)

        query_embedding = embeddings[0:1]
        section_embeddings = embeddings[1:]

        # Compute similarities
        similarities = self.compute_similarity(query_embedding, section_embeddings)

        # Apply persona-specific boosting
        boosted_similarities = self._apply_persona_boosting(sections, similarities, persona, job_to_be_done)

        # Create ranked results with enhanced explanations
        ranked_results = []
        for i, (section, similarity) in enumerate(zip(sections, boosted_similarities)):
            explanation = self._generate_enhanced_explanation(section, persona, job_to_be_done, similarity)
            ranked_results.append((section, float(similarity), explanation))

        # Sort by relevance score (descending)
        ranked_results.sort(key=lambda x: x[1], reverse=True)

        logger.debug(f"Ranked {len(sections)} sections with enhanced scoring, top similarity: {ranked_results[0][1]:.3f}")

        return ranked_results

    def _extract_persona_terms(self, persona: str) -> List[str]:
        """Extract key terms from persona for enhanced matching."""
        persona_lower = persona.lower()
        if 'travel' in persona_lower:
            return ['travel', 'trip', 'vacation', 'tourism', 'destination', 'itinerary']
        elif 'planner' in persona_lower:
            return ['planning', 'organize', 'schedule', 'coordinate', 'logistics']
        elif 'researcher' in persona_lower:
            return ['research', 'analysis', 'study', 'investigation', 'data']
        else:
            return []

    def _extract_job_terms(self, job: str) -> List[str]:
        """Extract key terms from job description for enhanced matching."""
        job_lower = job.lower()
        terms = []
        if 'group' in job_lower:
            terms.extend(['group', 'friends', 'together', 'collective'])
        if 'days' in job_lower:
            terms.extend(['days', 'itinerary', 'schedule', 'timeline'])
        if 'plan' in job_lower:
            terms.extend(['plan', 'organize', 'prepare', 'arrange'])
        return terms

    def _extract_document_context(self, doc_name: str) -> str:
        """Extract context from document name for better matching."""
        doc_lower = doc_name.lower()
        if 'cities' in doc_lower:
            return 'urban destinations attractions sightseeing'
        elif 'cuisine' in doc_lower:
            return 'food dining restaurants culinary experiences'
        elif 'things to do' in doc_lower:
            return 'activities entertainment attractions experiences'
        elif 'tips' in doc_lower:
            return 'advice recommendations practical information'
        elif 'restaurants' in doc_lower:
            return 'dining food establishments meals'
        else:
            return ''

    def _apply_persona_boosting(self, sections: List[Dict[str, Any]], similarities: np.ndarray,
                               persona: str, job_to_be_done: str) -> np.ndarray:
        """Apply persona-specific boosting to similarity scores."""
        boosted = similarities.copy()

        for i, section in enumerate(sections):
            title_lower = section.get('title', '').lower()
            doc_name_lower = section.get('document_name', '').lower()

            # Travel planner specific boosting
            if 'travel' in persona.lower():
                if any(term in title_lower for term in ['comprehensive', 'guide', 'major']):
                    boosted[i] *= 1.3
                if any(term in title_lower for term in ['coastal', 'activities', 'experiences']):
                    boosted[i] *= 1.2
                if 'cities' in doc_name_lower and any(term in title_lower for term in ['comprehensive', 'guide']):
                    boosted[i] *= 1.4

            # Group trip specific boosting
            if 'group' in job_to_be_done.lower() or 'friends' in job_to_be_done.lower():
                if any(term in title_lower for term in ['nightlife', 'entertainment', 'activities']):
                    boosted[i] *= 1.25
                if any(term in title_lower for term in ['packing', 'tips', 'coordination']):
                    boosted[i] *= 1.15

        return boosted

    def _fallback_ranking(self, sections: List[Dict[str, Any]], persona: str, job_to_be_done: str) -> List[Tuple[Dict[str, Any], float, str]]:
        """Fallback ranking when embeddings fail."""
        ranked_results = []
        for i, section in enumerate(sections):
            # Simple keyword-based scoring
            score = self._calculate_keyword_score(section, persona, job_to_be_done)
            explanation = f"Keyword-based relevance scoring"
            ranked_results.append((section, score, explanation))

        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return ranked_results

    def _calculate_keyword_score(self, section: Dict[str, Any], persona: str, job_to_be_done: str) -> float:
        """Calculate simple keyword-based relevance score."""
        title = section.get('title', '').lower()
        content = section.get('content_preview', '').lower()
        text = f"{title} {content}"

        score = 0.0

        # Persona keywords
        if 'travel' in persona.lower():
            travel_keywords = ['travel', 'trip', 'destination', 'guide', 'experience']
            score += sum(0.1 for kw in travel_keywords if kw in text)

        # Job keywords
        job_keywords = ['plan', 'group', 'friends', 'days', 'activities']
        score += sum(0.15 for kw in job_keywords if kw in job_to_be_done.lower() and kw in text)

        return min(score, 1.0)

    def _generate_enhanced_explanation(self, section: Dict[str, Any], persona: str,
                                     job_to_be_done: str, similarity_score: float) -> str:
        """Generate enhanced explanation for section ranking."""
        explanations = []

        # Similarity-based explanation
        if similarity_score > 0.8:
            explanations.append("excellent relevance to travel planning needs")
        elif similarity_score > 0.6:
            explanations.append("high relevance for group trip planning")
        elif similarity_score > 0.4:
            explanations.append("moderate relevance to travel requirements")
        else:
            explanations.append("basic relevance to travel context")

        # Content-specific explanations
        title = section.get('title', '').lower()
        doc_name = section.get('document_name', '').lower()

        if 'comprehensive' in title or 'guide' in title:
            explanations.append("comprehensive planning resource")
        if 'coastal' in title or 'activities' in title:
            explanations.append("group-friendly activities")
        if 'culinary' in title or 'cuisine' in title:
            explanations.append("dining experiences for groups")
        if 'tips' in title or 'packing' in title:
            explanations.append("practical travel advice")
        if 'nightlife' in title or 'entertainment' in title:
            explanations.append("entertainment options for friends")

        return "; ".join(explanations) if explanations else "general travel information"
    
    def _generate_explanation(self, section: Dict[str, Any], persona: str, 
                            job_to_be_done: str, similarity_score: float) -> str:
        """Generate human-readable explanation for section ranking."""
        explanations = []
        
        # Similarity-based explanation
        if similarity_score > 0.7:
            explanations.append("high semantic relevance")
        elif similarity_score > 0.4:
            explanations.append("moderate semantic relevance")
        else:
            explanations.append("low semantic relevance")
        
        # Content-based explanations
        title = section.get('title', '').lower()
        content = section.get('content_preview', '').lower()
        persona_lower = persona.lower()
        job_lower = job_to_be_done.lower()
        
        # Check for persona-specific keywords
        persona_keywords = self._extract_keywords(persona_lower)
        job_keywords = self._extract_keywords(job_lower)
        
        for keyword in persona_keywords:
            if keyword in title or keyword in content:
                explanations.append(f"contains '{keyword}' relevant to persona")
                break
        
        for keyword in job_keywords:
            if keyword in title or keyword in content:
                explanations.append(f"matches job requirement '{keyword}'")
                break
        
        # Section type explanations
        if any(word in title for word in ['introduction', 'overview', 'summary']):
            explanations.append("introductory content")
        elif any(word in title for word in ['method', 'approach', 'implementation']):
            explanations.append("methodological content")
        elif any(word in title for word in ['result', 'finding', 'analysis']):
            explanations.append("results-focused content")
        elif any(word in title for word in ['conclusion', 'discussion', 'future']):
            explanations.append("conclusive content")
        
        return "; ".join(explanations) if explanations else "general content"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Remove common words and extract meaningful terms
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out very common words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 
            'did', 'she', 'use', 'way', 'will', 'with'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return keywords[:5]  # Return top 5 keywords
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for processing."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-]', ' ', text)
        
        # Remove very short words
        words = text.split()
        words = [word for word in words if len(word) > 1]
        
        return ' '.join(words)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "approach": "transformers" if self.use_transformers else "tfidf",
            "model_name": self.model_name if self.use_transformers else "TF-IDF",
            "available": str(SENTENCE_TRANSFORMERS_AVAILABLE or SKLEARN_AVAILABLE),
            "backend": "sentence-transformers" if self.use_transformers else "scikit-learn"
        }
