# 🚀 Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Configuration](#configuration)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- Python 3.11 or higher
- Docker 20.10+
- Docker Compose 2.0+
- kubectl (for Kubernetes deployment)
- Git

### System Requirements
- Minimum 4GB RAM
- 10GB free disk space
- CPU: 2 cores minimum (4+ recommended)

## Local Development

### 1. Clone Repository
```bash
git clone https://github.com/ravigohel142996/AI-Enterprise-Command-System.git
cd AI-Enterprise-Command-System
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Initialize Database
```bash
python backend/init_db.py
```

### 5. Start Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Start Frontend (New Terminal)
```bash
streamlit run frontend/app.py
```

**Access:**
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:8501

## Docker Deployment

### Quick Start
```bash
# Using the provided script
./start.sh
```

### Manual Setup
```bash
# 1. Copy environment file
cp .env.example .env

# 2. Build and start services
docker-compose up -d --build

# 3. View logs
docker-compose logs -f

# 4. Stop services
docker-compose down
```

### Docker Services
- **postgres**: PostgreSQL database (port 5432)
- **mongodb**: MongoDB database (port 27017)
- **redis**: Redis cache (port 6379)
- **backend**: FastAPI backend (port 8000)
- **frontend**: Streamlit dashboard (port 8501)

### Docker Commands
```bash
# Rebuild specific service
docker-compose up -d --build backend

# View service logs
docker-compose logs backend
docker-compose logs frontend

# Access container shell
docker-compose exec backend bash

# Restart services
docker-compose restart

# Clean up (remove volumes)
docker-compose down -v
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.20+)
- kubectl configured
- Docker images built and pushed to registry

### 1. Build and Push Images
```bash
# Build backend
docker build -t your-registry/ai-enterprise-backend:latest -f deployment/docker/Dockerfile.backend .
docker push your-registry/ai-enterprise-backend:latest

# Build frontend
docker build -t your-registry/ai-enterprise-frontend:latest -f deployment/docker/Dockerfile.frontend .
docker push your-registry/ai-enterprise-frontend:latest
```

### 2. Update Image References
Edit `deployment/kubernetes/deployment.yaml` to use your registry URLs.

### 3. Create Secrets
```bash
kubectl create secret generic db-secrets \
  --from-literal=postgres-password=YOUR_PASSWORD \
  --from-literal=mongodb-password=YOUR_PASSWORD \
  --from-literal=redis-password=YOUR_PASSWORD \
  -n ai-enterprise
```

### 4. Deploy
```bash
kubectl apply -f deployment/kubernetes/deployment.yaml
```

### 5. Check Status
```bash
# Check pods
kubectl get pods -n ai-enterprise

# Check services
kubectl get services -n ai-enterprise

# View logs
kubectl logs -f deployment/backend-deployment -n ai-enterprise
```

### 6. Access Application
```bash
# Get external IP
kubectl get service backend-service -n ai-enterprise
kubectl get service frontend-service -n ai-enterprise
```

## Cloud Deployment

### AWS Deployment

#### Using ECS Fargate
```bash
# 1. Create ECR repositories
aws ecr create-repository --repository-name ai-enterprise-backend
aws ecr create-repository --repository-name ai-enterprise-frontend

# 2. Push images
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ECR_URL
docker tag ai-enterprise-backend:latest YOUR_ECR_URL/ai-enterprise-backend:latest
docker push YOUR_ECR_URL/ai-enterprise-backend:latest

# 3. Create ECS cluster
aws ecs create-cluster --cluster-name ai-enterprise-cluster

# 4. Create task definition (use AWS Console or CLI)
# 5. Create service
```

#### Using EKS
```bash
# 1. Create EKS cluster
eksctl create cluster --name ai-enterprise --region us-east-1

# 2. Update kubeconfig
aws eks update-kubeconfig --name ai-enterprise --region us-east-1

# 3. Deploy using kubectl
kubectl apply -f deployment/kubernetes/deployment.yaml
```

#### Database Setup
- **RDS PostgreSQL**: Create PostgreSQL instance
- **DocumentDB**: For MongoDB compatibility
- **ElastiCache**: Redis instance

### GCP Deployment

#### Using GKE
```bash
# 1. Create GKE cluster
gcloud container clusters create ai-enterprise \
  --zone us-central1-a \
  --num-nodes 3

# 2. Get credentials
gcloud container clusters get-credentials ai-enterprise

# 3. Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml
```

#### Database Setup
- **Cloud SQL**: PostgreSQL instance
- **Cloud Memorystore**: Redis instance
- **MongoDB Atlas**: For MongoDB

### Azure Deployment

#### Using AKS
```bash
# 1. Create resource group
az group create --name ai-enterprise-rg --location eastus

# 2. Create AKS cluster
az aks create \
  --resource-group ai-enterprise-rg \
  --name ai-enterprise-cluster \
  --node-count 3

# 3. Get credentials
az aks get-credentials --resource-group ai-enterprise-rg --name ai-enterprise-cluster

# 4. Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml
```

## Configuration

### Environment Variables

**Backend Configuration**
```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_enterprise_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ML Models
MODEL_STORAGE_PATH=./models
```

### Database Migration
```bash
# Using Alembic for migrations
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### SSL/TLS Configuration
For production, enable HTTPS:

**Using Nginx**
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Check services
docker-compose ps
kubectl get pods -n ai-enterprise
```

### Logging
```bash
# Docker logs
docker-compose logs -f backend

# Kubernetes logs
kubectl logs -f deployment/backend-deployment -n ai-enterprise

# Application logs
tail -f logs/app.log
```

### Metrics
- Prometheus metrics: http://localhost:9090
- Application metrics: http://localhost:8000/metrics

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find and kill process using port
lsof -ti:8000 | xargs kill -9
```

#### Database Connection Error
```bash
# Check database is running
docker-compose ps postgres

# Check connection
psql -h localhost -U postgres -d ai_enterprise_db
```

#### Docker Build Fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Kubernetes Pod Fails
```bash
# Describe pod for details
kubectl describe pod POD_NAME -n ai-enterprise

# Check logs
kubectl logs POD_NAME -n ai-enterprise

# Check events
kubectl get events -n ai-enterprise
```

### Performance Tuning

#### Backend Optimization
```bash
# Increase workers
uvicorn main:app --workers 4

# Enable caching
# Configure Redis TTL in .env
```

#### Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_employees_dept ON employees(department_id);

-- Analyze tables
ANALYZE users;
ANALYZE employees;
```

## Backup and Recovery

### Database Backup
```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U postgres ai_enterprise_db > backup.sql

# MongoDB backup
docker-compose exec mongodb mongodump --out /backup

# Restore PostgreSQL
docker-compose exec -T postgres psql -U postgres ai_enterprise_db < backup.sql
```

### Application Backup
```bash
# Backup models and data
tar -czf backup.tar.gz models/ data/ logs/

# Restore
tar -xzf backup.tar.gz
```

## Scaling

### Horizontal Scaling
```bash
# Docker Compose
docker-compose up -d --scale backend=3

# Kubernetes
kubectl scale deployment backend-deployment --replicas=5 -n ai-enterprise
```

### Load Balancing
Use Nginx or cloud load balancers to distribute traffic across backend instances.

## Security Checklist

- [ ] Change default passwords
- [ ] Use strong JWT secret keys
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Backup encryption keys
- [ ] Monitor security logs

## Support

For issues and questions:
- GitHub Issues: https://github.com/ravigohel142996/AI-Enterprise-Command-System/issues
- Email: support@ai-enterprise-os.com
- Documentation: /docs

---

**Last Updated:** February 2024
**Version:** 1.0.0
