"""Test Finance services"""

import pytest
from backend.app.services.finance import analyze_transaction, forecast_monthly_revenue


def test_analyze_transaction():
    """Test transaction analysis"""
    transaction_data = {
        "transaction_type": "expense",
        "amount": 5000,
        "description": "Software licenses",
        "date": "2024-01-15T10:00:00"
    }
    
    result = analyze_transaction(transaction_data)
    
    assert "is_fraudulent" in result
    assert "fraud_score" in result
    assert "category" in result
    assert isinstance(result["is_fraudulent"], bool)


def test_forecast_revenue():
    """Test revenue forecasting"""
    historical_data = [2.0, 2.1, 2.3, 2.2, 2.4, 2.5]
    
    result = forecast_monthly_revenue(historical_data)
    
    assert "forecasts" in result
    assert len(result["forecasts"]) == 3
    assert all(isinstance(f, (int, float)) for f in result["forecasts"])
