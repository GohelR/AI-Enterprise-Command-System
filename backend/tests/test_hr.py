"""Test HR services"""

import pytest
from backend.app.services.hr import screen_resume, analyze_employee_retention


def test_screen_resume():
    """Test resume screening"""
    resume_text = """
    Senior Software Engineer with 5 years of experience.
    Skills: Python, Machine Learning, AWS, Docker, SQL
    Education: Master's degree in Computer Science
    """
    
    result = screen_resume(resume_text, "John Doe", "john@example.com")
    
    assert "ml_score" in result
    assert result["ml_score"] > 0
    assert "skills" in result
    assert len(result["skills"]) > 0
    assert result["status"] in ["shortlisted", "pending", "rejected"]


def test_analyze_employee_retention():
    """Test employee retention analysis"""
    employee_data = {
        "performance_score": 85,
        "salary": 75000,
        "tenure_years": 3
    }
    
    result = analyze_employee_retention(employee_data)
    
    assert "retention_risk" in result
    assert 0 <= result["retention_risk"] <= 1
    assert "risk_level" in result
    assert result["risk_level"] in ["high", "medium", "low"]
