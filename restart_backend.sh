#!/bin/bash

echo "🔄 Restarting Backend Server..."

# Kill existing uvicorn process
pkill -f "uvicorn app.main:app"
sleep 2

# Activate virtual environment and start backend
source venv/bin/activate
echo "✅ Starting backend on port 8000..."
uvicorn app.main:app --reload --port 8000
