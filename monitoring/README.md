# Monitoring für Menüplansimulator

Dieses Verzeichnis enthält Monitoring-Tools zur Überwachung der Anwendung.

## Link Monitor

Das `link_monitor.py` Script überprüft regelmäßig alle wichtigen URLs und API-Endpunkte.

### Installation

```bash
pip install requests
```

### Verwendung

**Lokaler Test:**
```bash
python3 monitoring/link_monitor.py http://localhost:5000
```

**Produktions-Test:**
```bash
python3 monitoring/link_monitor.py https://menuplan-simulator-v5.onrender.com
```

**Mit Umgebungsvariable:**
```bash
export MONITOR_BASE_URL=https://menuplan-simulator-v5.onrender.com
python3 monitoring/link_monitor.py
```

### Ausgabe

Das Script gibt eine detaillierte Übersicht aller geprüften URLs aus:

```
🔍 Überprüfe URLs auf https://menuplan-simulator-v5.onrender.com...
  ✅ Landing Page: 200
  ✅ Hauptanwendung: 200
  ❌ Bestelllisten: HTTP 404 (CRITICAL)
  ...

📊 ZUSAMMENFASSUNG
============================================================
Gesamt:           10
✅ Erfolgreich:   8
❌ Fehlgeschlagen: 2
🚨 Kritisch:      1
============================================================
```

### Exit Codes

- `0`: Alle Checks erfolgreich (oder nur nicht-kritische Fehler)
- `1`: Kritische Fehler gefunden

### Ergebnisse

Die Ergebnisse werden in `monitoring_results.json` gespeichert.

## Health Check API

Die Anwendung stellt mehrere Health-Check-Endpunkte bereit:

### `/api/health`

Basis Health Check - gibt den Status der Anwendung zurück.

**Beispiel:**
```bash
curl https://menuplan-simulator-v5.onrender.com/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T23:10:00",
  "service": "menuplan-simulator",
  "version": "1.0.0"
}
```

### `/api/health/detailed`

Detaillierter Health Check - überprüft verschiedene Komponenten.

**Beispiel:**
```bash
curl https://menuplan-simulator-v5.onrender.com/api/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T23:10:00",
  "service": "menuplan-simulator",
  "version": "1.0.0",
  "checks": {
    "recipes": {
      "status": "healthy",
      "count": 200,
      "message": "200 recipes loaded"
    },
    "static_files": {
      "status": "healthy",
      "folder": "/app/frontend",
      "html_files_count": 14,
      "html_files": ["index.html", "order-lists.html", ...]
    },
    "critical_files": {
      "status": "healthy",
      "message": "All critical files present"
    }
  }
}
```

### `/api/health/files`

Listet alle statischen Dateien auf - hilfreich für Debugging.

**Beispiel:**
```bash
curl https://menuplan-simulator-v5.onrender.com/api/health/files
```

## Automatisches Monitoring

### Mit Cron (Linux/Mac)

Fügen Sie einen Cron-Job hinzu, um das Monitoring regelmäßig auszuführen:

```bash
# Jeden Tag um 6:00 Uhr
0 6 * * * cd /path/to/project && python3 monitoring/link_monitor.py >> monitoring/logs/monitor.log 2>&1
```

### Mit GitHub Actions

Erstellen Sie `.github/workflows/monitoring.yml`:

```yaml
name: Link Monitoring

on:
  schedule:
    - cron: '0 */6 * * *'  # Alle 6 Stunden
  workflow_dispatch:  # Manuell auslösbar

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests
      - name: Run monitoring
        run: python monitoring/link_monitor.py
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: monitoring-results
          path: monitoring_results.json
```

### Mit Render.com Cron Job

Erstellen Sie einen separaten Cron-Job-Service in `render.yaml`:

```yaml
services:
  - type: cron
    name: link-monitor
    env: python
    schedule: "0 */6 * * *"  # Alle 6 Stunden
    buildCommand: pip install requests
    startCommand: python monitoring/link_monitor.py
```

## Benachrichtigungen

### E-Mail-Benachrichtigung

Erweitern Sie das Script um E-Mail-Versand bei Fehlern:

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(results):
    if results['summary']['critical_failed'] > 0:
        msg = MIMEText(f"Critical failures detected: {results}")
        msg['Subject'] = '🚨 Menüplansimulator: Critical Failures'
        msg['From'] = 'monitor@example.com'
        msg['To'] = 'admin@example.com'
        
        with smtplib.SMTP('smtp.example.com') as server:
            server.send_message(msg)
```

### Slack-Benachrichtigung

```python
import requests

def send_slack_alert(results):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    message = {
        "text": f"🚨 Monitoring Alert: {results['summary']['critical_failed']} critical failures"
    }
    requests.post(webhook_url, json=message)
```

## Troubleshooting

### Timeout-Fehler

Wenn Sie Timeout-Fehler erhalten, erhöhen Sie den Timeout-Wert:

```python
response = requests.get(url, timeout=30)  # 30 Sekunden
```

### Connection-Fehler

Überprüfen Sie:
1. Ist die Anwendung erreichbar?
2. Ist die Firewall korrekt konfiguriert?
3. Läuft der Service auf Render.com?

### 404-Fehler

Wenn bestimmte Seiten 404 zurückgeben:
1. Prüfen Sie `/api/health/files` um zu sehen, welche Dateien vorhanden sind
2. Prüfen Sie `/api/health/detailed` um zu sehen, ob kritische Dateien fehlen
3. Überprüfen Sie die Render.com Logs

