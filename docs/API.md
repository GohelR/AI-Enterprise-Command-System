# API Documentation

## Overview

The AI Enterprise Operating System provides a comprehensive REST API for managing all company departments using AI and machine learning.

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** JWT Bearer Token

## Authentication

### Register User
Creates a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "role": "user",
  "department": "Engineering"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00"
}
```

### Login
Authenticates user and returns JWT tokens.

**Endpoint:** `POST /auth/login?email=user@example.com&password=SecurePassword123!`

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Human Resources

### Screen Resume
AI-powered resume screening and scoring.

**Endpoint:** `POST /hr/resume/screen`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "candidate_name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "resume_text": "Senior Software Engineer with 5+ years...",
  "skills": ["Python", "Machine Learning", "AWS"],
  "experience_years": 5,
  "education": "Master's in Computer Science"
}
```

**Response:**
```json
{
  "candidate_name": "Jane Smith",
  "email": "jane@example.com",
  "ml_score": 85.5,
  "skills": ["Python", "Machine Learning", "AWS", "Docker"],
  "status": "shortlisted",
  "recommendation": "Score: 85.5/100 - Shortlisted"
}
```

### Analyze Employee Retention
Predict employee retention risk.

**Endpoint:** `POST /hr/employee/retention-risk`

**Request Body:**
```json
{
  "performance_score": 85,
  "salary": 75000,
  "tenure_years": 3
}
```

**Response:**
```json
{
  "retention_risk": 0.25,
  "risk_level": "low",
  "recommendations": [
    "Employee likely to stay",
    "Continue regular check-ins"
  ]
}
```

## Finance & Accounting

### Analyze Transaction
Detect fraud and classify expenses.

**Endpoint:** `POST /finance/transaction/analyze`

**Request Body:**
```json
{
  "transaction_type": "expense",
  "amount": 5000,
  "description": "Software licenses for development team",
  "date": "2024-01-15T10:00:00"
}
```

**Response:**
```json
{
  "is_fraudulent": false,
  "fraud_score": 0.15,
  "category": "technology",
  "confidence": "high"
}
```

### Forecast Revenue
Predict future revenue based on historical data.

**Endpoint:** `POST /finance/revenue/forecast`

**Request Body:**
```json
[2.0, 2.1, 2.3, 2.2, 2.4, 2.5]
```

**Response:**
```json
{
  "forecasts": [2.6, 2.7, 2.8],
  "period": "monthly",
  "confidence_interval": [2.34, 2.43, 2.52],
  "trend": "increasing"
}
```

## Customer Support

### Analyze Support Ticket
Classify and analyze customer support tickets.

**Endpoint:** `POST /support/ticket/analyze`

**Request Body:**
```json
{
  "customer_email": "customer@example.com",
  "subject": "Unable to login to account",
  "description": "I've been trying to login but keep getting an error message"
}
```

**Response:**
```json
{
  "category": "account",
  "priority": "high",
  "sentiment": "negative",
  "sentiment_score": 0.35
}
```

### AI Chatbot
Get AI-powered responses to customer queries.

**Endpoint:** `POST /support/chatbot?message=How do I reset my password`

**Response:**
```json
{
  "user_message": "How do I reset my password",
  "bot_response": "I can help with technical issues. To reset your password, please click on 'Forgot Password' on the login page..."
}
```

## Marketing & Growth

### Score Lead
AI-powered lead scoring and prioritization.

**Endpoint:** `POST /marketing/lead/score`

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@techcorp.com",
  "company": "Tech Corp",
  "source": "referral"
}
```

**Response:**
```json
{
  "lead_score": 75,
  "conversion_probability": 0.65,
  "status": "hot",
  "priority": "high"
}
```

### Optimize Campaign
Get campaign optimization suggestions.

**Endpoint:** `POST /marketing/campaign/optimize`

**Request Body:**
```json
{
  "name": "Q1 Email Campaign",
  "channel": "email",
  "budget": 10000,
  "roi": 2.5
}
```

**Response:**
```json
{
  "suggestions": [
    "A/B test subject lines",
    "Personalize content by segment"
  ],
  "predicted_conversions": 500,
  "optimization_score": 87,
  "recommended_budget": 11000
}
```

## Sales & CRM

### Analyze Customer Health
Comprehensive customer health analysis.

**Endpoint:** `POST /sales/customer/health`

**Request Body:**
```json
{
  "customer_id": "CUST001",
  "days_since_last_activity": 15,
  "support_tickets": 2,
  "engagement_score": 75,
  "avg_purchase_value": 5000,
  "purchase_frequency": 6,
  "customer_lifespan_months": 24
}
```

**Response:**
```json
{
  "customer_id": "CUST001",
  "health_score": 82,
  "churn_risk": 0.18,
  "risk_level": "low",
  "lifetime_value": 60000,
  "retention_actions": []
}
```

### Forecast Deal
Predict deal closure probability.

**Endpoint:** `POST /sales/deal/forecast`

**Request Body:**
```json
{
  "value": 50000,
  "stage": "proposal",
  "days_in_pipeline": 30
}
```

**Response:**
```json
{
  "close_probability": 0.50,
  "estimated_days_to_close": 30,
  "forecast_value": 25000,
  "confidence": "medium"
}
```

## Cybersecurity

### Analyze Security Alert
Analyze security threats and anomalies.

**Endpoint:** `POST /security/alert/analyze`

**Request Body:**
```json
{
  "alert_type": "intrusion",
  "severity": "high",
  "source_ip": "203.0.113.45",
  "destination_ip": "192.168.1.100",
  "description": "Multiple failed login attempts"
}
```

**Response:**
```json
{
  "is_threat": true,
  "threat_score": 0.75,
  "severity": "high"
}
```

## Dashboard Metrics

### Get Dashboard Metrics
Retrieve real-time metrics for all departments.

**Endpoint:** `GET /dashboard/metrics`

**Response:**
```json
{
  "total_employees": 1234,
  "total_revenue": 2400000,
  "total_tickets": 89,
  "active_campaigns": 24,
  "security_alerts": 7,
  "ml_models": 12,
  "department_metrics": {
    "hr": {"employees": 1234},
    "finance": {"revenue": 2400000},
    "support": {"tickets": 89},
    "marketing": {"campaigns": 24},
    "security": {"alerts": 7}
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user

## Pagination

For list endpoints:
```
GET /api/v1/resource?page=1&per_page=20
```

## Webhooks

Configure webhooks for real-time notifications:

```json
{
  "event": "ticket.created",
  "url": "https://your-domain.com/webhook",
  "secret": "your_webhook_secret"
}
```

## SDK Examples

### Python
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    params={"email": "user@example.com", "password": "password"}
)
token = response.json()["access_token"]

# Use API
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/api/v1/hr/resume/screen",
    headers=headers,
    json={"candidate_name": "John", "email": "john@example.com", ...}
)
print(response.json())
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login?email=user@example.com&password=password', {
  method: 'POST'
});
const { access_token } = await loginResponse.json();

// Use API
const response = await fetch('http://localhost:8000/api/v1/hr/resume/screen', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    candidate_name: 'John',
    email: 'john@example.com',
    ...
  })
});
const data = await response.json();
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

---

**Version:** 1.0.0
**Last Updated:** February 2024
