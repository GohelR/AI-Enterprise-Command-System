"""Main FastAPI Application"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn

from backend.app.core.config import settings
from backend.app.core.security import get_current_user, create_access_token, create_refresh_token, get_password_hash, verify_password
from backend.app.db.database import Base, get_engine, get_db
from backend.app.models.models import User
from backend.app.schemas.schemas import (
    Token, UserCreate, UserResponse,
    ResumeCreate, ResumeResponse,
    TransactionCreate, TransactionResponse,
    TicketCreate, TicketResponse,
    CampaignCreate, LeadCreate,
    CustomerCreate, SecurityAlertCreate,
    DashboardMetrics
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import services at module level (lazy instantiation happens within functions)
from backend.app.services.hr import screen_resume, analyze_employee_retention
from backend.app.services.finance import analyze_transaction, forecast_monthly_revenue
from backend.app.services.customer_support import analyze_support_ticket, process_chatbot_message
from backend.app.services.marketing import score_and_prioritize_lead, CampaignOptimizer
from backend.app.services.sales import analyze_customer_health, DealForecasting
from backend.app.services.cybersecurity import analyze_security_alert

# Create tables only if database is available
try:
    engine = get_engine()
    if engine:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
except Exception as e:
    logger.warning(f"Could not create database tables: {e}")

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Enterprise Operating System - Managing all company departments with AI"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Enterprise Operating System",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Authentication endpoints
@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role,
        department=user.department
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.post("/api/v1/auth/login", response_model=Token)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Create tokens
    access_token = create_access_token({"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# HR Department endpoints
@app.post("/api/v1/hr/resume/screen")
async def screen_resume_endpoint(resume: ResumeCreate, current_user: dict = Depends(get_current_user)):
    """Screen a resume"""
    result = screen_resume(resume.resume_text, resume.candidate_name, resume.email)
    return result


@app.post("/api/v1/hr/employee/retention-risk")
async def analyze_retention(employee_data: dict, current_user: dict = Depends(get_current_user)):
    """Analyze employee retention risk"""
    result = analyze_employee_retention(employee_data)
    return result


# Finance Department endpoints
@app.post("/api/v1/finance/transaction/analyze")
async def analyze_transaction_endpoint(transaction: TransactionCreate, current_user: dict = Depends(get_current_user)):
    """Analyze financial transaction"""
    transaction_data = {
        'transaction_type': transaction.transaction_type,
        'amount': transaction.amount,
        'description': transaction.description,
        'date': transaction.date
    }
    result = analyze_transaction(transaction_data)
    return result


@app.post("/api/v1/finance/revenue/forecast")
async def forecast_revenue(historical_data: list, current_user: dict = Depends(get_current_user)):
    """Forecast revenue"""
    result = forecast_monthly_revenue(historical_data)
    return result


# Customer Support endpoints
@app.post("/api/v1/support/ticket/analyze")
async def analyze_ticket(ticket: TicketCreate, current_user: dict = Depends(get_current_user)):
    """Analyze support ticket"""
    result = analyze_support_ticket(ticket.subject, ticket.description, ticket.customer_email)
    return result


@app.post("/api/v1/support/chatbot")
async def chatbot(message: str):
    """AI Chatbot"""
    result = process_chatbot_message(message)
    return result


# Marketing Department endpoints
@app.post("/api/v1/marketing/lead/score")
async def score_lead(lead: LeadCreate, current_user: dict = Depends(get_current_user)):
    """Score a lead"""
    lead_data = {
        'name': lead.name,
        'email': lead.email,
        'company': lead.company,
        'source': lead.source
    }
    result = score_and_prioritize_lead(lead_data)
    return result


@app.post("/api/v1/marketing/campaign/optimize")
async def optimize_campaign(campaign_data: dict, current_user: dict = Depends(get_current_user)):
    """Optimize marketing campaign"""
    optimizer = CampaignOptimizer()
    result = optimizer.optimize_campaign(campaign_data)
    return result


# Sales Department endpoints
@app.post("/api/v1/sales/customer/health")
async def customer_health(customer_data: dict, current_user: dict = Depends(get_current_user)):
    """Analyze customer health"""
    result = analyze_customer_health(customer_data)
    return result


@app.post("/api/v1/sales/deal/forecast")
async def forecast_deal(deal_data: dict, current_user: dict = Depends(get_current_user)):
    """Forecast deal closure"""
    forecaster = DealForecasting()
    result = forecaster.forecast_deal(deal_data)
    return result


# Cybersecurity endpoints
@app.post("/api/v1/security/alert/analyze")
async def analyze_alert(alert: SecurityAlertCreate, current_user: dict = Depends(get_current_user)):
    """Analyze security alert"""
    alert_data = {
        'type': alert.alert_type,
        'severity': alert.severity,
        'source_ip': alert.source_ip,
        'destination_ip': alert.destination_ip,
        'description': alert.description
    }
    result = analyze_security_alert(alert_data)
    return result


# Dashboard endpoint
@app.get("/api/v1/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get dashboard metrics"""
    from backend.app.models.models import Employee, Transaction, SupportTicket, Campaign, SecurityAlert, MLModel
    
    # Get counts
    total_employees = db.query(Employee).count()
    total_tickets = db.query(SupportTicket).count()
    active_campaigns = db.query(Campaign).filter(Campaign.status == "active").count()
    security_alerts = db.query(SecurityAlert).filter(SecurityAlert.status == "open").count()
    ml_models = db.query(MLModel).filter(MLModel.is_active == True).count()
    
    # Calculate total revenue
    total_revenue = db.query(Transaction).filter(Transaction.transaction_type == "income").count() * 1000  # Placeholder
    
    return {
        "total_employees": total_employees,
        "total_revenue": total_revenue,
        "total_tickets": total_tickets,
        "active_campaigns": active_campaigns,
        "security_alerts": security_alerts,
        "ml_models": ml_models,
        "department_metrics": {
            "hr": {"employees": total_employees},
            "finance": {"revenue": total_revenue},
            "support": {"tickets": total_tickets},
            "marketing": {"campaigns": active_campaigns},
            "security": {"alerts": security_alerts}
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
