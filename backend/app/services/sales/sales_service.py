"""Sales & CRM Service - Churn Prediction, Customer Lifetime Value, Deal Forecasting"""

from typing import Dict, List, Any


class ChurnPredictionModel:
    """Predict customer churn"""
    
    @staticmethod
    def predict_churn(customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict churn probability"""
        risk_score = 0.0
        
        # Activity level
        last_activity_days = customer_data.get('days_since_last_activity', 0)
        if last_activity_days > 90:
            risk_score += 0.4
        elif last_activity_days > 30:
            risk_score += 0.2
        
        # Support tickets
        support_tickets = customer_data.get('support_tickets', 0)
        if support_tickets > 5:
            risk_score += 0.2
        
        # Payment issues
        if customer_data.get('payment_failures', 0) > 0:
            risk_score += 0.3
        
        # Engagement score
        engagement = customer_data.get('engagement_score', 50)
        if engagement < 30:
            risk_score += 0.3
        
        churn_risk = min(1.0, risk_score)
        
        return {
            'churn_risk': round(churn_risk, 2),
            'risk_level': 'high' if churn_risk >= 0.7 else 'medium' if churn_risk >= 0.4 else 'low',
            'retention_actions': [
                'Offer discount or incentive' if churn_risk >= 0.5 else '',
                'Schedule check-in call' if churn_risk >= 0.4 else '',
                'Send engagement campaign' if churn_risk >= 0.3 else ''
            ]
        }


class CustomerLifetimeValueModel:
    """Calculate Customer Lifetime Value (CLV)"""
    
    @staticmethod
    def calculate_clv(customer_data: Dict[str, Any]) -> float:
        """Calculate CLV"""
        avg_purchase = customer_data.get('avg_purchase_value', 0)
        purchase_frequency = customer_data.get('purchase_frequency', 0)
        customer_lifespan_months = customer_data.get('customer_lifespan_months', 24)
        
        # CLV = Average Purchase Value × Purchase Frequency × Customer Lifespan
        clv = avg_purchase * purchase_frequency * (customer_lifespan_months / 12)
        
        return round(clv, 2)


class DealForecasting:
    """Forecast deal closure"""
    
    @staticmethod
    def forecast_deal(deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Forecast deal probability and timeline"""
        stage = deal_data.get('stage', 'initial')
        deal_value = deal_data.get('value', 0)
        days_in_pipeline = deal_data.get('days_in_pipeline', 0)
        
        # Stage-based probability
        stage_probabilities = {
            'initial': 0.10,
            'qualified': 0.25,
            'proposal': 0.50,
            'negotiation': 0.70,
            'closing': 0.90
        }
        
        base_probability = stage_probabilities.get(stage, 0.10)
        
        # Adjust for time in pipeline
        if days_in_pipeline > 90:
            base_probability *= 0.7  # Long deals less likely
        elif days_in_pipeline < 7:
            base_probability *= 0.9  # Very new deals uncertain
        
        # Estimated close date
        stage_days = {
            'initial': 60,
            'qualified': 45,
            'proposal': 30,
            'negotiation': 15,
            'closing': 7
        }
        
        days_to_close = stage_days.get(stage, 30)
        
        return {
            'close_probability': round(base_probability, 2),
            'estimated_days_to_close': days_to_close,
            'forecast_value': round(deal_value * base_probability, 2),
            'confidence': 'high' if stage in ['negotiation', 'closing'] else 'medium'
        }


def analyze_customer_health(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive customer health analysis"""
    churn_model = ChurnPredictionModel()
    clv_model = CustomerLifetimeValueModel()
    
    # Churn prediction
    churn_result = churn_model.predict_churn(customer_data)
    
    # CLV calculation
    clv = clv_model.calculate_clv(customer_data)
    
    # Overall health score
    health_score = 100 - (churn_result['churn_risk'] * 100)
    
    return {
        'customer_id': customer_data.get('customer_id'),
        'health_score': round(health_score, 2),
        'churn_risk': churn_result['churn_risk'],
        'risk_level': churn_result['risk_level'],
        'lifetime_value': clv,
        'retention_actions': churn_result['retention_actions']
    }
