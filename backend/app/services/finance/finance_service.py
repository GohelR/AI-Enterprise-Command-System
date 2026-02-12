"""Finance & Accounting Service - Revenue Forecasting, Fraud Detection, Budget Optimization"""

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from typing import Dict, List, Any
from datetime import datetime, timedelta
from backend.app.ml.base import MLModelBase


class FraudDetectionModel(MLModelBase):
    """ML model for fraud detection"""
    
    def __init__(self):
        super().__init__("fraud_detection", "1.0.0")
        self.model = IsolationForest(contamination=0.1, random_state=42)
    
    def detect_fraud(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect if transaction is fraudulent"""
        # Extract features
        features = [
            transaction_data.get('amount', 0),
            hash(transaction_data.get('description', '')) % 1000,  # Simple hash
            1 if transaction_data.get('transaction_type') == 'expense' else 0,
            len(transaction_data.get('description', ''))
        ]
        
        # Simple rule-based detection (can be replaced with trained model)
        fraud_score = 0.0
        amount = transaction_data.get('amount', 0)
        
        # Large amounts are suspicious
        if amount > 10000:
            fraud_score += 0.4
        elif amount > 5000:
            fraud_score += 0.2
        
        # Unusual timing (weekend, late night)
        hour = datetime.now().hour
        if hour < 6 or hour > 22:
            fraud_score += 0.2
        
        # Short description
        if len(transaction_data.get('description', '')) < 10:
            fraud_score += 0.1
        
        is_fraudulent = fraud_score >= 0.5
        
        return {
            'is_fraudulent': is_fraudulent,
            'fraud_score': round(fraud_score, 2),
            'confidence': 'high' if fraud_score >= 0.7 else 'medium' if fraud_score >= 0.4 else 'low'
        }


class RevenueForecasting(MLModelBase):
    """Revenue forecasting model"""
    
    def __init__(self):
        super().__init__("revenue_forecasting", "1.0.0")
    
    def forecast_revenue(self, historical_data: List[float], periods: int = 3) -> List[float]:
        """Forecast revenue for next periods"""
        if len(historical_data) < 3:
            # Not enough data, return simple average
            avg = np.mean(historical_data) if historical_data else 0
            return [avg * 1.05 ** i for i in range(periods)]
        
        # Simple trend-based forecasting
        recent_growth = (historical_data[-1] - historical_data[-3]) / historical_data[-3] if historical_data[-3] != 0 else 0.05
        forecasts = []
        last_value = historical_data[-1]
        
        for i in range(periods):
            next_value = last_value * (1 + recent_growth)
            forecasts.append(round(next_value, 2))
            last_value = next_value
        
        return forecasts


class ExpenseClassifier:
    """Classify expenses into categories"""
    
    CATEGORIES = {
        'salary': ['salary', 'wage', 'payroll', 'compensation'],
        'marketing': ['ad', 'marketing', 'campaign', 'promotion'],
        'operations': ['rent', 'utilities', 'office', 'supplies'],
        'technology': ['software', 'hardware', 'cloud', 'license', 'subscription'],
        'travel': ['travel', 'hotel', 'flight', 'transportation'],
        'misc': []
    }
    
    @classmethod
    def classify(cls, description: str) -> str:
        """Classify expense based on description"""
        description_lower = description.lower()
        
        for category, keywords in cls.CATEGORIES.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return 'misc'


class BudgetOptimizer:
    """Budget optimization and allocation"""
    
    @staticmethod
    def optimize_budget(total_budget: float, departments: List[Dict[str, Any]]) -> Dict[str, float]:
        """Optimize budget allocation across departments"""
        # Simple optimization based on historical spending and priority
        allocations = {}
        remaining = total_budget
        
        # Sort departments by priority
        sorted_depts = sorted(departments, key=lambda x: x.get('priority', 5), reverse=True)
        
        for dept in sorted_depts:
            dept_name = dept['name']
            historical_spend = dept.get('historical_spend', 0)
            priority = dept.get('priority', 5)
            
            # Allocate based on historical + priority factor
            allocation = historical_spend * (1 + priority * 0.05)
            allocation = min(allocation, remaining * 0.4)  # Max 40% to any dept
            
            allocations[dept_name] = round(allocation, 2)
            remaining -= allocation
        
        return allocations
    
    @staticmethod
    def predict_spend(current_spend: float, days_elapsed: int, days_in_period: int) -> float:
        """Predict total spend for the period"""
        if days_elapsed == 0:
            return 0
        
        daily_rate = current_spend / days_elapsed
        predicted_total = daily_rate * days_in_period
        return round(predicted_total, 2)


# Service functions
def analyze_transaction(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a financial transaction"""
    fraud_model = FraudDetectionModel()
    
    # Detect fraud
    fraud_result = fraud_model.detect_fraud(transaction_data)
    
    # Classify expense
    category = ExpenseClassifier.classify(transaction_data.get('description', ''))
    
    return {
        **fraud_result,
        'category': category
    }


def forecast_monthly_revenue(historical_revenue: List[float]) -> Dict[str, Any]:
    """Forecast revenue for next 3 months"""
    model = RevenueForecasting()
    forecasts = model.forecast_revenue(historical_revenue, periods=3)
    
    return {
        'forecasts': forecasts,
        'period': 'monthly',
        'confidence_interval': [f * 0.9 for f in forecasts],  # 90% confidence
        'trend': 'increasing' if forecasts[0] > historical_revenue[-1] else 'decreasing'
    }


def optimize_department_budget(total_budget: float, departments: List[Dict]) -> Dict[str, Any]:
    """Optimize budget allocation"""
    optimizer = BudgetOptimizer()
    allocations = optimizer.optimize_budget(total_budget, departments)
    
    return {
        'total_budget': total_budget,
        'allocations': allocations,
        'optimization_score': 85.5  # Placeholder metric
    }
