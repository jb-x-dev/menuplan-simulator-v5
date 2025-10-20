#!/bin/bash

# Menüplansimulator v5.0 - Automatisches Deployment Script
# Dieses Script hilft beim schnellen Deployment auf verschiedenen Plattformen

echo "🚀 Menüplansimulator v5.0 - Deployment Helper"
echo "=============================================="
echo ""

# Prüfe ob Git installiert ist
if ! command -v git &> /dev/null; then
    echo "❌ Git ist nicht installiert!"
    echo "   Bitte installieren: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git ist installiert"
echo ""

# Menü anzeigen
echo "Wählen Sie eine Deployment-Option:"
echo ""
echo "1) GitHub Repository erstellen (manuell)"
echo "2) Render.com Deployment vorbereiten"
echo "3) Railway.app Deployment vorbereiten"
echo "4) Docker Container bauen"
echo "5) Lokaler Test-Server starten"
echo "6) Beenden"
echo ""

read -p "Ihre Wahl (1-6): " choice

case $choice in
    1)
        echo ""
        echo "📦 GitHub Repository Vorbereitung"
        echo "=================================="
        echo ""
        
        # Git initialisieren
        if [ ! -d .git ]; then
            echo "🔧 Git Repository initialisieren..."
            git init
            echo "✅ Git initialisiert"
        else
            echo "✅ Git bereits initialisiert"
        fi
        
        # .gitignore erstellen
        if [ ! -f .gitignore ]; then
            echo "🔧 .gitignore erstellen..."
            cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv
venv/
*.log
.DS_Store
EOF
            echo "✅ .gitignore erstellt"
        fi
        
        # Dateien hinzufügen
        echo "🔧 Dateien zum Repository hinzufügen..."
        git add .
        
        # Commit erstellen
        echo "🔧 Commit erstellen..."
        git commit -m "Initial commit - Menüplansimulator v5.0" 2>/dev/null || echo "✅ Bereits committed"
        
        echo ""
        echo "✅ Repository vorbereitet!"
        echo ""
        echo "📝 Nächste Schritte:"
        echo "1. Gehe zu: https://github.com/new"
        echo "2. Repository Name: menuplan-simulator"
        echo "3. Public oder Private wählen"
        echo "4. 'Create repository' klicken"
        echo "5. Führe diese Befehle aus:"
        echo ""
        echo "   git remote add origin https://github.com/IHR-USERNAME/menuplan-simulator.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo ""
        ;;
        
    2)
        echo ""
        echo "🌐 Render.com Deployment Vorbereitung"
        echo "====================================="
        echo ""
        
        # Prüfe ob render.yaml existiert
        if [ -f render.yaml ]; then
            echo "✅ render.yaml vorhanden"
        else
            echo "⚠️  render.yaml fehlt - wird erstellt..."
            cat > render.yaml << 'EOF'
services:
  - type: web
    name: menuplan-simulator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -c gunicorn.conf.py backend.app:app
EOF
            echo "✅ render.yaml erstellt"
        fi
        
        # Prüfe requirements.txt
        if [ -f requirements.txt ]; then
            echo "✅ requirements.txt vorhanden"
        else
            echo "❌ requirements.txt fehlt!"
        fi
        
        # Prüfe gunicorn.conf.py
        if [ -f gunicorn.conf.py ]; then
            echo "✅ gunicorn.conf.py vorhanden"
        else
            echo "❌ gunicorn.conf.py fehlt!"
        fi
        
        echo ""
        echo "✅ Render.com Deployment bereit!"
        echo ""
        echo "📝 Nächste Schritte:"
        echo "1. Code auf GitHub hochladen (Option 1)"
        echo "2. Gehe zu: https://render.com"
        echo "3. 'New +' → 'Web Service'"
        echo "4. GitHub Repository verbinden"
        echo "5. Konfiguration:"
        echo "   - Build: pip install -r requirements.txt"
        echo "   - Start: gunicorn -c gunicorn.conf.py backend.app:app"
        echo "6. 'Create Web Service' klicken"
        echo ""
        ;;
        
    3)
        echo ""
        echo "🚂 Railway.app Deployment Vorbereitung"
        echo "======================================"
        echo ""
        
        echo "✅ Railway erkennt Python automatisch!"
        echo ""
        echo "📝 Nächste Schritte:"
        echo "1. Code auf GitHub hochladen (Option 1)"
        echo "2. Gehe zu: https://railway.app"
        echo "3. 'Start a New Project'"
        echo "4. 'Deploy from GitHub repo'"
        echo "5. Repository auswählen"
        echo "6. Automatisches Deployment startet"
        echo "7. Settings → Generate Domain"
        echo ""
        ;;
        
    4)
        echo ""
        echo "🐳 Docker Container bauen"
        echo "========================="
        echo ""
        
        # Prüfe ob Docker installiert ist
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker ist nicht installiert!"
            echo "   Bitte installieren: https://www.docker.com/get-started"
            exit 1
        fi
        
        echo "✅ Docker ist installiert"
        echo ""
        
        # Prüfe Dockerfile
        if [ ! -f Dockerfile ]; then
            echo "❌ Dockerfile fehlt!"
            exit 1
        fi
        
        echo "🔧 Docker Image bauen..."
        docker build -t menuplan-simulator .
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Docker Image erfolgreich gebaut!"
            echo ""
            echo "📝 Container starten:"
            echo "   docker run -d -p 5000:5000 --name menuplan menuplan-simulator"
            echo ""
            echo "📝 Zugriff:"
            echo "   http://localhost:5000"
            echo ""
        else
            echo "❌ Docker Build fehlgeschlagen!"
        fi
        ;;
        
    5)
        echo ""
        echo "🖥️  Lokaler Test-Server"
        echo "======================"
        echo ""
        
        # Prüfe Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 ist nicht installiert!"
            exit 1
        fi
        
        echo "✅ Python 3 ist installiert"
        echo ""
        
        # Prüfe Abhängigkeiten
        echo "🔧 Abhängigkeiten prüfen..."
        pip3 install -q flask flask-cors reportlab gunicorn
        
        echo "✅ Abhängigkeiten installiert"
        echo ""
        echo "🚀 Server starten..."
        echo ""
        echo "   URL: http://localhost:5000"
        echo "   Zum Beenden: Strg+C"
        echo ""
        
        python3 backend/app.py
        ;;
        
    6)
        echo ""
        echo "👋 Auf Wiedersehen!"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ Ungültige Auswahl!"
        exit 1
        ;;
esac

