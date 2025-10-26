#!/bin/bash
# Start script for Render.com deployment

echo "🚀 Starting Menüplansimulator..."
echo "📂 Working directory: $(pwd)"
echo "📁 Directory contents:"
ls -la

echo ""
echo "🐍 Python version: $(python --version)"
echo "📦 Installed packages:"
pip list | grep -E "(Flask|gunicorn)" || echo "No Flask/gunicorn found"

echo ""
echo "🔍 Checking backend directory:"
ls -la backend/ || echo "No backend directory!"

echo ""
echo "🔧 Starting gunicorn..."
echo "Command: gunicorn --bind 0.0.0.0:\$PORT backend.app:app"

# Set PYTHONPATH to include current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

exec gunicorn --bind 0.0.0.0:$PORT backend.app:app

