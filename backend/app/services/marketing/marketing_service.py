"""Marketing & Growth Service - Campaign Optimization, Lead Scoring, SEO"""

from typing import Dict, List, Any
import random


class LeadScoringModel:
    """Lead scoring model"""
    
    @staticmethod
    def score_lead(lead_data: Dict[str, Any]) -> float:
        """Score a lead (0-100)"""
        score = 0
        
        # Company size
        company = lead_data.get('company', '')
        if company:
            score += 15
        
        # Email domain
        email = lead_data.get('email', '')
        if '@' in email:
            domain = email.split('@')[1]
            if domain not in ['gmail.com', 'yahoo.com', 'hotmail.com']:
                score += 20  # Business email
        
        # Source quality
        source = lead_data.get('source', '')
        source_scores = {
            'referral': 30,
            'organic': 25,
            'paid': 20,
            'social': 15,
            'other': 10
        }
        score += source_scores.get(source, 10)
        
        # Engagement
        engagement = lead_data.get('engagement_level', 0)
        score += min(engagement * 5, 35)
        
        return min(100, score)
    
    @staticmethod
    def predict_conversion_probability(lead_score: float) -> float:
        """Predict probability of conversion"""
        # Simple linear mapping
        probability = lead_score / 100 * 0.8  # Max 80% probability
        return round(probability, 2)


class CampaignOptimizer:
    """Optimize marketing campaigns"""
    
    @staticmethod
    def optimize_campaign(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide campaign optimization suggestions"""
        channel = campaign_data.get('channel', '')
        budget = campaign_data.get('budget', 0)
        current_roi = campaign_data.get('roi', 0)
        
        suggestions = []
        predicted_conversions = 0
        
        # Channel-specific optimizations
        if channel == 'email':
            suggestions.append("A/B test subject lines for higher open rates")
            suggestions.append("Personalize content based on user segments")
            predicted_conversions = budget * 0.05
        elif channel == 'social':
            suggestions.append("Focus on high-engagement time slots")
            suggestions.append("Use video content for better reach")
            predicted_conversions = budget * 0.03
        elif channel == 'ppc':
            suggestions.append("Optimize bidding strategy for high-intent keywords")
            suggestions.append("Improve landing page conversion rate")
            predicted_conversions = budget * 0.04
        
        # Budget optimization
        if current_roi < 2:
            suggestions.append("Consider reallocating budget to better-performing channels")
        
        optimization_score = min(100, (current_roi * 20) + (len(suggestions) * 10))
        
        return {
            'suggestions': suggestions,
            'predicted_conversions': round(predicted_conversions, 2),
            'optimization_score': round(optimization_score, 2),
            'recommended_budget': budget * 1.1 if current_roi > 3 else budget * 0.9
        }


class SEOPredictor:
    """SEO ranking prediction"""
    
    @staticmethod
    def predict_ranking(content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict SEO ranking potential"""
        score = 0
        
        # Content length
        word_count = content_data.get('word_count', 0)
        if word_count >= 2000:
            score += 30
        elif word_count >= 1000:
            score += 20
        elif word_count >= 500:
            score += 10
        
        # Keywords
        keyword_density = content_data.get('keyword_density', 0)
        if 0.01 <= keyword_density <= 0.03:
            score += 25
        
        # Backlinks
        backlinks = content_data.get('backlinks', 0)
        score += min(backlinks * 2, 30)
        
        # Meta tags
        if content_data.get('has_meta_description'):
            score += 10
        if content_data.get('has_title_tag'):
            score += 5
        
        ranking_prediction = "Top 10" if score >= 75 else "Top 20" if score >= 50 else "Top 50"
        
        return {
            'seo_score': score,
            'ranking_prediction': ranking_prediction,
            'recommendations': [
                "Add more quality backlinks" if backlinks < 10 else "",
                "Optimize keyword density" if keyword_density < 0.01 or keyword_density > 0.03 else "",
                "Increase content length to 1500+ words" if word_count < 1500 else ""
            ]
        }


def score_and_prioritize_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Score and prioritize a lead"""
    model = LeadScoringModel()
    
    lead_score = model.score_lead(lead_data)
    conversion_prob = model.predict_conversion_probability(lead_score)
    
    # Determine status
    if lead_score >= 70:
        status = "hot"
    elif lead_score >= 50:
        status = "warm"
    else:
        status = "cold"
    
    return {
        'lead_score': lead_score,
        'conversion_probability': conversion_prob,
        'status': status,
        'priority': 'high' if lead_score >= 70 else 'medium' if lead_score >= 50 else 'low'
    }
