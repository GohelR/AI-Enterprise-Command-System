#!/bin/bash
# Streamlit startup script with health check

set -e

echo "========================================="
echo "Starting AI Enterprise Operating System"
echo "========================================="
echo ""

# Set environment variables
export PYTHONUNBUFFERED=1

# Start Streamlit
echo "Launching Streamlit app..."
streamlit run frontend/app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false

echo "App started successfully!"
