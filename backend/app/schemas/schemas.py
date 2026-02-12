"""Pydantic Schemas for API validation"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    department: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: str = "user"


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# HR Schemas
class ResumeCreate(BaseModel):
    candidate_name: str
    email: EmailStr
    phone: Optional[str] = None
    resume_text: str
    skills: Optional[List[str]] = []
    experience_years: Optional[float] = 0
    education: Optional[str] = None


class ResumeResponse(BaseModel):
    id: int
    candidate_name: str
    email: str
    ml_score: Optional[float] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmployeeCreate(BaseModel):
    employee_id: str
    position: str
    department_id: int
    salary: float
    hire_date: datetime


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    position: str
    department_id: int
    performance_score: Optional[float] = None
    retention_risk: Optional[float] = None
    
    class Config:
        from_attributes = True


# Finance Schemas
class TransactionCreate(BaseModel):
    transaction_type: str
    amount: float
    description: str
    date: datetime


class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    transaction_type: str
    category: Optional[str] = None
    amount: float
    is_fraudulent: bool
    fraud_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    department_id: int
    year: int
    month: int
    allocated_amount: float


class BudgetResponse(BaseModel):
    id: int
    department_id: int
    year: int
    month: int
    allocated_amount: float
    spent_amount: float
    forecasted_spend: Optional[float] = None
    
    class Config:
        from_attributes = True


# Customer Support Schemas
class TicketCreate(BaseModel):
    customer_email: EmailStr
    subject: str
    description: str


class TicketResponse(BaseModel):
    id: int
    ticket_id: str
    customer_email: str
    subject: str
    category: Optional[str] = None
    priority: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Marketing Schemas
class CampaignCreate(BaseModel):
    name: str
    channel: str
    budget: float
    start_date: datetime
    end_date: datetime


class CampaignResponse(BaseModel):
    id: int
    name: str
    channel: str
    budget: float
    roi: Optional[float] = None
    predicted_conversions: Optional[float] = None
    optimization_score: Optional[float] = None
    status: str
    
    class Config:
        from_attributes = True


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    source: str


class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    lead_score: Optional[float] = None
    conversion_probability: Optional[float] = None
    status: str
    
    class Config:
        from_attributes = True


# Sales Schemas
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    industry: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    customer_id: str
    name: str
    email: str
    lifetime_value: Optional[float] = None
    churn_risk: Optional[float] = None
    is_active: bool
    
    class Config:
        from_attributes = True


# Cybersecurity Schemas
class SecurityAlertCreate(BaseModel):
    alert_type: str
    severity: str
    source_ip: str
    destination_ip: Optional[str] = None
    description: str


class SecurityAlertResponse(BaseModel):
    id: int
    alert_type: str
    severity: str
    is_threat: Optional[bool] = None
    threat_score: Optional[float] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ML Model Schemas
class MLModelCreate(BaseModel):
    name: str
    version: str
    model_type: str
    department: str
    accuracy: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = {}


class MLModelResponse(BaseModel):
    id: int
    name: str
    version: str
    model_type: str
    department: str
    accuracy: Optional[float] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardMetrics(BaseModel):
    """Dashboard metrics response"""
    total_employees: int
    total_revenue: float
    total_tickets: int
    active_campaigns: int
    security_alerts: int
    ml_models: int
    department_metrics: Dict[str, Any]
