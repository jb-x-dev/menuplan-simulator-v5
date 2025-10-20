"""
WSGI Entry Point für Produktions-Deployment
"""
from app import app

if __name__ == "__main__":
    app.run()

