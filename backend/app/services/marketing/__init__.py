"""Marketing service package"""

from .marketing_service import (
    LeadScoringModel,
    CampaignOptimizer,
    SEOPredictor,
    score_and_prioritize_lead
)

__all__ = [
    "LeadScoringModel",
    "CampaignOptimizer",
    "SEOPredictor",
    "score_and_prioritize_lead"
]
