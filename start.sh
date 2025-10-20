#!/bin/bash

echo "🚀 Starting Menüplansimulator..."

cd /home/ubuntu/menuplan-simulator/backend

# Prüfe ob Server bereits läuft
if pgrep -f "python3 app.py" > /dev/null; then
    echo "⚠️  Server is already running"
    echo "   PID: $(pgrep -f 'python3 app.py')"
else
    # Starte Server
    python3 app.py &
    
    # Warte kurz
    sleep 3
    
    echo ""
    echo "✅ Server started successfully!"
    echo ""
    echo "🌐 Access the application at:"
    echo "   Local: http://localhost:5000"
    echo "   Public: https://5000-is0b2qg2nn18hqovm2ro3-1c4a3e9a.manusvm.computer"
    echo ""
    echo "📖 API Documentation: /home/ubuntu/menuplan-simulator/README.md"
    echo ""
fi

