"""Database Models"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.db.database import Base


class User(Base):
    """User Model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="user")  # admin, manager, user, analyst
    department = Column(String)  # HR, Finance, Marketing, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Department(Base):
    """Department Model"""
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    head_user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# HR Models
class Employee(Base):
    """Employee Model"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(String, unique=True, index=True)
    position = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    salary = Column(Float)
    hire_date = Column(DateTime)
    performance_score = Column(Float)
    retention_risk = Column(Float)  # ML prediction
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Resume(Base):
    """Resume Screening Model"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String)
    email = Column(String)
    phone = Column(String)
    resume_text = Column(Text)
    skills = Column(JSON)
    experience_years = Column(Float)
    education = Column(String)
    ml_score = Column(Float)  # ML screening score
    status = Column(String, default="pending")  # pending, shortlisted, rejected, hired
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Finance Models
class Transaction(Base):
    """Financial Transaction Model"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    transaction_type = Column(String)  # income, expense
    category = Column(String)  # ML classified
    amount = Column(Float)
    description = Column(Text)
    date = Column(DateTime)
    is_fraudulent = Column(Boolean, default=False)  # ML prediction
    fraud_score = Column(Float)  # ML fraud detection score
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Budget(Base):
    """Budget Model"""
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    year = Column(Integer)
    month = Column(Integer)
    allocated_amount = Column(Float)
    spent_amount = Column(Float, default=0)
    forecasted_spend = Column(Float)  # ML prediction
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Customer Support Models
class SupportTicket(Base):
    """Support Ticket Model"""
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    customer_email = Column(String)
    subject = Column(String)
    description = Column(Text)
    category = Column(String)  # ML classified
    priority = Column(String)  # low, medium, high, critical
    sentiment = Column(String)  # positive, neutral, negative (ML)
    sentiment_score = Column(Float)
    status = Column(String, default="open")  # open, in_progress, resolved, closed
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime)


# Marketing Models
class Campaign(Base):
    """Marketing Campaign Model"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    channel = Column(String)  # email, social, ppc, seo
    budget = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    roi = Column(Float)
    predicted_conversions = Column(Float)  # ML prediction
    optimization_score = Column(Float)  # ML optimization
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Lead(Base):
    """Sales Lead Model"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    company = Column(String)
    source = Column(String)
    lead_score = Column(Float)  # ML prediction
    conversion_probability = Column(Float)  # ML prediction
    status = Column(String, default="new")  # new, qualified, contacted, converted, lost
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Sales Models
class Customer(Base):
    """Customer Model"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    company = Column(String)
    industry = Column(String)
    lifetime_value = Column(Float)  # ML prediction
    churn_risk = Column(Float)  # ML prediction
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Cybersecurity Models
class SecurityAlert(Base):
    """Security Alert Model"""
    __tablename__ = "security_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)  # intrusion, anomaly, breach
    severity = Column(String)  # low, medium, high, critical
    source_ip = Column(String)
    destination_ip = Column(String)
    description = Column(Text)
    is_threat = Column(Boolean)  # ML prediction
    threat_score = Column(Float)  # ML anomaly score
    status = Column(String, default="open")  # open, investigating, resolved, false_positive
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ML Model Registry
class MLModel(Base):
    """ML Model Registry"""
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    model_type = Column(String)  # classification, regression, nlp, etc.
    department = Column(String)
    accuracy = Column(Float)
    metrics = Column(JSON)
    file_path = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
