"""HR Tech Service - Resume Screening, Performance Analytics, Retention Modeling"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Any
from backend.app.ml.base import MLModelBase


class ResumeScreeningModel(MLModelBase):
    """ML model for resume screening"""
    
    def __init__(self):
        super().__init__("resume_screening", "1.0.0")
        self.vectorizer = TfidfVectorizer(max_features=100)
        
    def train(self, resume_texts: List[str], labels: List[int]):
        """Train resume screening model"""
        from sklearn.ensemble import RandomForestClassifier
        
        # Vectorize resume texts
        X = self.vectorizer.fit_transform(resume_texts).toarray()
        
        # Train classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, labels)
        
        self.save_model()
        return self.model.score(X, labels)
    
    def score_resume(self, resume_text: str) -> float:
        """Score a resume (0-100)"""
        if self.model is None:
            self.load_model()
        
        # Simple scoring based on keywords and length
        keywords = ['python', 'java', 'machine learning', 'ai', 'ml', 'data science', 
                   'experience', 'project', 'leadership', 'team', 'bachelor', 'master', 'phd']
        
        text_lower = resume_text.lower()
        keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Calculate score
        score = min(100, (keyword_count * 8) + (len(resume_text.split()) / 10))
        return round(score, 2)
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """Extract skills from resume"""
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'aws', 'azure', 'gcp',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'docker', 'kubernetes', 'tensorflow', 'pytorch', 'scikit-learn'
        ]
        
        text_lower = resume_text.lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]
        return found_skills


class EmployeeRetentionModel(MLModelBase):
    """ML model for employee retention prediction"""
    
    def __init__(self):
        super().__init__("employee_retention", "1.0.0")
    
    def predict_retention_risk(self, employee_data: Dict[str, Any]) -> float:
        """Predict employee retention risk (0-1, higher = more risk)"""
        # Simple rule-based model (can be replaced with trained ML model)
        risk_score = 0.0
        
        # Performance score (lower performance = higher risk)
        performance = employee_data.get('performance_score', 50)
        if performance < 50:
            risk_score += 0.3
        elif performance < 70:
            risk_score += 0.2
        
        # Salary (below market = higher risk)
        salary = employee_data.get('salary', 50000)
        if salary < 60000:
            risk_score += 0.2
        
        # Tenure (very short or very long = higher risk)
        tenure_years = employee_data.get('tenure_years', 2)
        if tenure_years < 1:
            risk_score += 0.3
        elif tenure_years > 5:
            risk_score += 0.1
        
        return min(1.0, risk_score)


class PerformanceAnalytics:
    """Employee performance analytics"""
    
    @staticmethod
    def calculate_performance_score(metrics: Dict[str, float]) -> float:
        """Calculate overall performance score"""
        weights = {
            'productivity': 0.3,
            'quality': 0.25,
            'collaboration': 0.2,
            'innovation': 0.15,
            'punctuality': 0.1
        }
        
        score = sum(metrics.get(key, 50) * weight for key, weight in weights.items())
        return round(score, 2)
    
    @staticmethod
    def predict_promotion_readiness(employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict if employee is ready for promotion"""
        performance = employee_data.get('performance_score', 50)
        tenure = employee_data.get('tenure_years', 0)
        
        readiness_score = 0
        if performance >= 80:
            readiness_score += 40
        elif performance >= 70:
            readiness_score += 25
        
        if tenure >= 2:
            readiness_score += 30
        elif tenure >= 1:
            readiness_score += 15
        
        recommendations = []
        if readiness_score >= 60:
            recommendations.append("Ready for promotion consideration")
        else:
            if performance < 70:
                recommendations.append("Focus on improving performance metrics")
            if tenure < 2:
                recommendations.append("Gain more experience in current role")
        
        return {
            'readiness_score': readiness_score,
            'is_ready': readiness_score >= 60,
            'recommendations': recommendations
        }


# Service functions
def screen_resume(resume_text: str, candidate_name: str, email: str) -> Dict[str, Any]:
    """Screen a resume and return results"""
    model = ResumeScreeningModel()
    
    score = model.score_resume(resume_text)
    skills = model.extract_skills(resume_text)
    
    # Determine status based on score
    if score >= 70:
        status = "shortlisted"
    elif score >= 50:
        status = "pending"
    else:
        status = "rejected"
    
    return {
        'candidate_name': candidate_name,
        'email': email,
        'ml_score': score,
        'skills': skills,
        'status': status,
        'recommendation': f"Score: {score}/100 - {status.capitalize()}"
    }


def analyze_employee_retention(employee_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze employee retention risk"""
    model = EmployeeRetentionModel()
    risk = model.predict_retention_risk(employee_data)
    
    risk_level = "high" if risk >= 0.7 else "medium" if risk >= 0.4 else "low"
    
    return {
        'retention_risk': risk,
        'risk_level': risk_level,
        'recommendations': [
            "Consider salary adjustment" if risk >= 0.5 else "",
            "Schedule 1-on-1 meeting" if risk >= 0.4 else "",
            "Review career development plan" if risk >= 0.3 else ""
        ]
    }
