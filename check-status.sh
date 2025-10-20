#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🍽️  Menüplansimulator - Status Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Systemd Service Status
echo "📋 Systemd Service Status:"
sudo systemctl is-active menuplan-simulator > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Service läuft"
    echo "   PID: $(sudo systemctl show -p MainPID menuplan-simulator | cut -d= -f2)"
else
    echo "   ❌ Service läuft NICHT"
fi
echo ""

# 2. Port Check
echo "🔌 Port 5000 Status:"
sudo lsof -i :5000 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Port 5000 ist offen"
else
    echo "   ❌ Port 5000 ist NICHT offen"
fi
echo ""

# 3. API Test
echo "🌐 API Test:"
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/recipes)
if [ "$response" = "200" ]; then
    recipe_count=$(curl -s http://localhost:5000/api/recipes | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    echo "   ✅ API erreichbar (HTTP $response)"
    echo "   📊 $recipe_count Rezepte verfügbar"
else
    echo "   ❌ API nicht erreichbar (HTTP $response)"
fi
echo ""

# 4. Öffentlicher Zugriff
echo "🌍 Öffentlicher Zugriff:"
echo "   https://5000-is0b2qg2nn18hqovm2ro3-1c4a3e9a.manusvm.computer"
echo ""

# 5. Logs
echo "📝 Letzte Log-Einträge:"
tail -5 /var/log/menuplan-simulator.log 2>/dev/null | sed 's/^/   /'
echo ""

# 6. Ressourcen
echo "💻 Ressourcen-Nutzung:"
if sudo systemctl is-active menuplan-simulator > /dev/null 2>&1; then
    pid=$(sudo systemctl show -p MainPID menuplan-simulator | cut -d= -f2)
    if [ "$pid" != "0" ]; then
        mem=$(ps -p $pid -o rss= 2>/dev/null | awk '{printf "%.1f MB", $1/1024}')
        cpu=$(ps -p $pid -o %cpu= 2>/dev/null | awk '{printf "%.1f%%", $1}')
        echo "   Memory: $mem"
        echo "   CPU: $cpu"
    fi
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 Befehle:"
echo "   sudo systemctl status menuplan-simulator  # Detaillierter Status"
echo "   sudo systemctl restart menuplan-simulator # Neustart"
echo "   sudo journalctl -u menuplan-simulator -f  # Live-Logs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

