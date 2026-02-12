# Database Schema Documentation

## PostgreSQL Tables

### Core Tables

#### users
Stores user authentication and profile information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role VARCHAR DEFAULT 'user',
    department VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### departments
Company departments information.

```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    head_user_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### HR Department Tables

#### employees
Employee records and HR data.

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    employee_id VARCHAR UNIQUE NOT NULL,
    position VARCHAR,
    department_id INTEGER REFERENCES departments(id),
    salary FLOAT,
    hire_date TIMESTAMP,
    performance_score FLOAT,
    retention_risk FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### resumes
Resume screening records.

```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    candidate_name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    resume_text TEXT,
    skills JSON,
    experience_years FLOAT,
    education VARCHAR,
    ml_score FLOAT,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Finance Department Tables

#### transactions
Financial transactions with fraud detection.

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR UNIQUE NOT NULL,
    transaction_type VARCHAR,
    category VARCHAR,
    amount FLOAT,
    description TEXT,
    date TIMESTAMP,
    is_fraudulent BOOLEAN DEFAULT FALSE,
    fraud_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### budgets
Department budget tracking.

```sql
CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES departments(id),
    year INTEGER,
    month INTEGER,
    allocated_amount FLOAT,
    spent_amount FLOAT DEFAULT 0,
    forecasted_spend FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Customer Support Tables

#### support_tickets
Customer support tickets with AI analysis.

```sql
CREATE TABLE support_tickets (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR UNIQUE NOT NULL,
    customer_email VARCHAR,
    subject VARCHAR,
    description TEXT,
    category VARCHAR,
    priority VARCHAR,
    sentiment VARCHAR,
    sentiment_score FLOAT,
    status VARCHAR DEFAULT 'open',
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

### Marketing Department Tables

#### campaigns
Marketing campaigns with optimization.

```sql
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    channel VARCHAR,
    budget FLOAT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    roi FLOAT,
    predicted_conversions FLOAT,
    optimization_score FLOAT,
    status VARCHAR DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### leads
Sales leads with scoring.

```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    company VARCHAR,
    source VARCHAR,
    lead_score FLOAT,
    conversion_probability FLOAT,
    status VARCHAR DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sales Department Tables

#### customers
Customer records with lifetime value.

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    email VARCHAR UNIQUE,
    company VARCHAR,
    industry VARCHAR,
    lifetime_value FLOAT,
    churn_risk FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Cybersecurity Tables

#### security_alerts
Security incidents and threat detection.

```sql
CREATE TABLE security_alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR,
    severity VARCHAR,
    source_ip VARCHAR,
    destination_ip VARCHAR,
    description TEXT,
    is_threat BOOLEAN,
    threat_score FLOAT,
    status VARCHAR DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ML Model Registry

#### ml_models
Machine learning model tracking.

```sql
CREATE TABLE ml_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    version VARCHAR NOT NULL,
    model_type VARCHAR,
    department VARCHAR,
    accuracy FLOAT,
    metrics JSON,
    file_path VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## MongoDB Collections

### Unstructured Data Storage

#### logs
System and application logs.

```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "level": "info|warning|error",
  "service": "string",
  "message": "string",
  "metadata": {}
}
```

#### analytics_events
User behavior and analytics events.

```json
{
  "_id": ObjectId,
  "event_type": "string",
  "user_id": "string",
  "timestamp": ISODate,
  "properties": {},
  "session_id": "string"
}
```

#### ml_experiments
ML experiment tracking.

```json
{
  "_id": ObjectId,
  "experiment_name": "string",
  "model_type": "string",
  "parameters": {},
  "metrics": {},
  "dataset_info": {},
  "created_at": ISODate
}
```

## Redis Cache Structure

### Cache Keys

- `user:session:{user_id}` - User session data
- `api:rate_limit:{ip}` - API rate limiting
- `cache:dashboard:{user_id}` - Dashboard metrics cache
- `ml:prediction:{model_name}:{input_hash}` - ML prediction cache

### TTL Settings

- User sessions: 30 minutes
- Rate limits: 1 minute
- Dashboard cache: 5 minutes
- ML predictions: 1 hour

## Indexes

### PostgreSQL Indexes

```sql
-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- Employees
CREATE INDEX idx_employees_employee_id ON employees(employee_id);
CREATE INDEX idx_employees_department ON employees(department_id);

-- Transactions
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_transactions_fraud ON transactions(is_fraudulent);

-- Support Tickets
CREATE INDEX idx_tickets_status ON support_tickets(status);
CREATE INDEX idx_tickets_priority ON support_tickets(priority);
CREATE INDEX idx_tickets_created ON support_tickets(created_at);

-- Customers
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_churn ON customers(churn_risk);
```

### MongoDB Indexes

```javascript
// Logs collection
db.logs.createIndex({ "timestamp": -1 });
db.logs.createIndex({ "level": 1, "timestamp": -1 });

// Analytics events
db.analytics_events.createIndex({ "user_id": 1, "timestamp": -1 });
db.analytics_events.createIndex({ "event_type": 1 });
```

## Relationships

```
users ──< employees
users ──< support_tickets (assigned_to)
departments ──< employees
departments ──< budgets
departments ─── users (head_user_id)
```

## Data Retention Policies

- **Logs**: 90 days
- **Analytics Events**: 1 year
- **Archived Tickets**: 2 years
- **Financial Records**: 7 years (compliance)
- **ML Model Artifacts**: Latest 5 versions per model

## Backup Strategy

- **PostgreSQL**: Daily full backups, hourly incremental
- **MongoDB**: Daily snapshots
- **Redis**: Persistence with AOF, snapshots every hour
- **Retention**: 30 days

## Security

- All passwords hashed with bcrypt
- PII encrypted at rest
- Row-level security for multi-tenant data
- Audit logging for sensitive operations
- Regular security scans
