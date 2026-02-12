#!/bin/bash

# AI Enterprise Operating System - Quick Start Script

echo "🏢 AI Enterprise Operating System - Setup"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Copy .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your configuration."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data models logs

# Build and start services
echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "✅ Services started!"
echo ""
echo "Access the application:"
echo "  📊 Dashboard: http://localhost:8501"
echo "  🌐 API: http://localhost:8000"
echo "  📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Default admin credentials:"
echo "  Email: admin@ai-enterprise.com"
echo "  Password: admin123"
echo ""
echo "⚠️  Please change the admin password after first login!"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
