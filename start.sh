#!/bin/bash
# Start script for Render.com deployment

echo "🚀 Starting Menüplansimulator..."
echo "📂 Working directory: $(pwd)"
echo "🐍 Python version: $(python --version)"
echo "📦 Installed packages:"
pip list | grep -E "(Flask|gunicorn)"

echo ""
echo "🔧 Starting gunicorn with backend.app:app..."
exec gunicorn --config gunicorn.conf.py backend.app:app

