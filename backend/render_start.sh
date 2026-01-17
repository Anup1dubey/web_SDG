#!/bin/bash
# Render startup script for the backend

echo "🚀 Starting SDG Platform Backend on Render..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations if needed
echo "🗄️ Checking database..."
python -c "from database import init_db; init_db()" || echo "⚠️ Database initialization skipped"

# Start the server
echo "✅ Starting Uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
