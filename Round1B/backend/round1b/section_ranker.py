"""
Intelligent section ranking system with persona-aware scoring.
Combines NLP similarity with domain-specific heuristics for explainable results.
"""
import logging
import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class RankingFactors:
    """Factors contributing to section ranking."""
    nlp_score: float = 0.0
    domain_score: float = 0.0
    job_relevance_score: float = 0.0
    position_score: float = 0.0
    length_score: float = 0.0
    
    @property
    def total_score(self) -> float:
        """Calculate weighted total score."""
        return (
            self.nlp_score * 0.4 +           # 40% NLP similarity
            self.domain_score * 0.25 +       # 25% domain relevance
            self.job_relevance_score * 0.2 + # 20% job relevance
            self.position_score * 0.1 +      # 10% document position
            self.length_score * 0.05         # 5% content length
        )


class SectionRanker:
    """Advanced section ranking with explainable persona-aware scoring."""
    
    def __init__(self):
        # Enhanced domain-specific keywords for better relevance scoring
        self.domain_keywords = {
            "travel_planner": [
                "itinerary", "accommodation", "transportation", "activities", "attractions",
                "restaurants", "hotels", "booking", "budget", "schedule", "group",
                "friends", "vacation", "trip", "tour", "guide", "recommendations",
                "planning", "logistics", "destinations", "experiences", "adventure"
            ],
            "bioinformatics": [
                "sequence", "genome", "protein", "dna", "rna", "gene", "mutation",
                "alignment", "phylogeny", "annotation", "database", "algorithm",
                "blast", "fasta", "genomic", "transcriptome", "proteome"
            ],
            "machine_learning": [
                "model", "training", "algorithm", "neural", "network", "deep",
                "learning", "classification", "regression", "clustering", "feature",
                "dataset", "accuracy", "validation", "optimization", "gradient"
            ],
            "research": [
                "study", "analysis", "methodology", "experiment", "hypothesis",
                "results", "findings", "conclusion", "literature", "review",
                "survey", "evaluation", "assessment", "investigation", "research"
            ],
            "technical": [
                "implementation", "architecture", "design", "system", "framework",
                "technology", "software", "hardware", "development", "engineering",
                "programming", "coding", "algorithm", "optimization", "performance"
            ],
            "business": [
                "strategy", "market", "customer", "revenue", "profit", "growth",
                "analysis", "management", "operations", "finance", "investment",
                "roi", "kpi", "metrics", "performance", "competitive", "advantage"
            ]
        }
        
        # Enhanced job-specific keywords
        self.job_keywords = {
            "plan": ["plan", "organize", "schedule", "arrange", "coordinate", "prepare"],
            "trip": ["trip", "travel", "journey", "vacation", "tour", "visit", "explore"],
            "group": ["group", "friends", "party", "team", "collective", "together"],
            "days": ["days", "itinerary", "schedule", "timeline", "duration", "time"],
            "review": ["review", "evaluate", "assess", "analyze", "examine", "study"],
            "research": ["research", "investigate", "explore", "discover", "find"],
            "implement": ["implement", "build", "develop", "create", "design"],
            "optimize": ["optimize", "improve", "enhance", "refine", "upgrade"],
            "compare": ["compare", "contrast", "benchmark", "evaluate", "assess"]
        }
        
        # Section importance patterns
        self.important_sections = {
            "high": [
                "abstract", "summary", "introduction", "conclusion", "results",
                "findings", "methodology", "approach", "overview", "executive"
            ],
            "medium": [
                "background", "related work", "literature", "discussion", "analysis",
                "evaluation", "implementation", "design", "architecture"
            ],
            "low": [
                "acknowledgments", "references", "bibliography", "appendix",
                "footnotes", "index", "glossary"
            ]
        }
    
    def rank_sections(self, sections: List[Dict[str, Any]], persona: str, 
                     job_to_be_done: str, nlp_scores: List[float]) -> List[Tuple[Dict[str, Any], float, str]]:
        """
        Rank sections using multi-factor scoring with explainable results.
        
        Args:
            sections: List of section dictionaries
            persona: User persona description
            job_to_be_done: Job description
            nlp_scores: NLP similarity scores from pipeline
            
        Returns:
            List of tuples (section, final_score, explanation)
        """
        if not sections:
            return []
        
        ranked_results = []
        
        for i, (section, nlp_score) in enumerate(zip(sections, nlp_scores)):
            # Calculate all ranking factors
            factors = self._calculate_ranking_factors(
                section, persona, job_to_be_done, nlp_score, i, len(sections)
            )
            
            # Generate explanation
            explanation = self._generate_detailed_explanation(section, factors, persona, job_to_be_done)
            
            ranked_results.append((section, factors.total_score, explanation))
        
        # Sort by total score (descending)
        ranked_results.sort(key=lambda x: x[1], reverse=True)
        
        logger.debug(f"Ranked {len(sections)} sections with multi-factor scoring")
        
        return ranked_results
    
    def _calculate_ranking_factors(self, section: Dict[str, Any], persona: str,
                                 job_to_be_done: str, nlp_score: float,
                                 position: int, total_sections: int) -> RankingFactors:
        """Calculate all ranking factors for a section."""
        factors = RankingFactors()
        
        # NLP similarity score (already calculated)
        factors.nlp_score = nlp_score
        
        # Domain relevance score
        factors.domain_score = self._calculate_domain_score(section, persona)
        
        # Job relevance score
        factors.job_relevance_score = self._calculate_job_relevance_score(section, job_to_be_done)
        
        # Position score (earlier sections often more important)
        factors.position_score = self._calculate_position_score(position, total_sections)
        
        # Length score (moderate length often better)
        factors.length_score = self._calculate_length_score(section)
        
        return factors
    
    def _calculate_domain_score(self, section: Dict[str, Any], persona: str) -> float:
        """Calculate domain-specific relevance score."""
        title = section.get('title', '').lower()
        content = section.get('content_preview', '').lower()
        persona_lower = persona.lower()
        
        score = 0.0
        
        # Check for domain keywords in persona
        for domain, keywords in self.domain_keywords.items():
            if domain in persona_lower or any(kw in persona_lower for kw in keywords[:3]):
                # Found relevant domain, check section content
                matches = sum(1 for kw in keywords if kw in title or kw in content)
                score = max(score, min(matches / len(keywords), 1.0))
        
        # Boost for important section types
        for importance, section_types in self.important_sections.items():
            if any(st in title for st in section_types):
                if importance == "high":
                    score += 0.3
                elif importance == "medium":
                    score += 0.15
                # Low importance sections get no boost
                break
        
        return min(score, 1.0)
    
    def _calculate_job_relevance_score(self, section: Dict[str, Any], job_to_be_done: str) -> float:
        """Calculate job-specific relevance score."""
        title = section.get('title', '').lower()
        content = section.get('content_preview', '').lower()
        job_lower = job_to_be_done.lower()
        
        score = 0.0
        
        # Direct keyword matching
        job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_lower))
        title_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', title))
        content_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', content))
        
        # Calculate overlap
        title_overlap = len(job_words & title_words) / max(len(job_words), 1)
        content_overlap = len(job_words & content_words) / max(len(job_words), 1)
        
        score = max(title_overlap * 0.8, content_overlap * 0.4)
        
        # Check for job-specific patterns
        for job_type, keywords in self.job_keywords.items():
            if any(kw in job_lower for kw in keywords):
                # Found job type, check section relevance
                if any(kw in title or kw in content for kw in keywords):
                    score += 0.3
                break
        
        return min(score, 1.0)
    
    def _calculate_position_score(self, position: int, total_sections: int) -> float:
        """Calculate position-based score (earlier sections often more important)."""
        if total_sections <= 1:
            return 1.0
        
        # Normalize position (0 to 1, where 0 is first)
        normalized_position = position / (total_sections - 1)
        
        # Higher score for earlier positions, but not too steep
        score = 1.0 - (normalized_position * 0.5)
        
        return max(score, 0.5)  # Minimum score of 0.5
    
    def _calculate_length_score(self, section: Dict[str, Any]) -> float:
        """Calculate length-based score (moderate length often optimal)."""
        content = section.get('content_preview', '')
        title = section.get('title', '')
        
        total_length = len(content) + len(title)
        
        # Optimal length range: 50-500 characters
        if 50 <= total_length <= 500:
            return 1.0
        elif total_length < 50:
            return total_length / 50.0  # Penalty for too short
        else:
            return max(0.5, 500 / total_length)  # Penalty for too long
    
    def _generate_detailed_explanation(self, section: Dict[str, Any], factors: RankingFactors,
                                     persona: str, job_to_be_done: str) -> str:
        """Generate detailed explanation for section ranking."""
        explanations = []
        
        # NLP score explanation
        if factors.nlp_score > 0.7:
            explanations.append("high semantic similarity")
        elif factors.nlp_score > 0.4:
            explanations.append("moderate semantic similarity")
        else:
            explanations.append("low semantic similarity")
        
        # Domain score explanation
        if factors.domain_score > 0.5:
            explanations.append("domain-specific content")
        elif factors.domain_score > 0.2:
            explanations.append("some domain relevance")
        
        # Job relevance explanation
        if factors.job_relevance_score > 0.5:
            explanations.append("highly relevant to job")
        elif factors.job_relevance_score > 0.2:
            explanations.append("moderately relevant to job")
        
        # Position explanation
        if factors.position_score > 0.8:
            explanations.append("early document position")
        
        # Section type explanation
        title_lower = section.get('title', '').lower()
        if any(st in title_lower for st in self.important_sections["high"]):
            explanations.append("high-importance section type")
        elif any(st in title_lower for st in self.important_sections["medium"]):
            explanations.append("medium-importance section type")
        
        # Combine explanations
        if explanations:
            return "; ".join(explanations)
        else:
            return f"general content (score: {factors.total_score:.3f})"
    
    def get_ranking_breakdown(self, factors: RankingFactors) -> Dict[str, float]:
        """Get detailed breakdown of ranking factors."""
        return {
            "nlp_similarity": factors.nlp_score,
            "domain_relevance": factors.domain_score,
            "job_relevance": factors.job_relevance_score,
            "position_bonus": factors.position_score,
            "length_score": factors.length_score,
            "total_score": factors.total_score
        }
