# Monitoring-System für Menüplansimulator

## Übersicht

Das Monitoring-System überwacht kontinuierlich die Verfügbarkeit und Funktionalität der Anwendung.

## Komponenten

### 1. Link Monitor (`monitoring/link_monitor.py`)

**Zweck:** Automatisierte Überprüfung aller wichtigen URLs und API-Endpunkte

**Features:**
- ✅ Überprüft 8 HTML-Seiten
- ✅ Überprüft 2 API-Endpunkte
- ✅ Unterscheidet zwischen kritischen und nicht-kritischen Fehlern
- ✅ Speichert Ergebnisse in JSON
- ✅ Exit-Code für CI/CD-Integration

**Verwendung:**
```bash
# Produktions-Test
python3 monitoring/link_monitor.py https://menuplan-simulator-v5.onrender.com

# Lokaler Test
python3 monitoring/link_monitor.py http://localhost:5000
```

**Überwachte URLs:**
- `/` - Landing Page (kritisch)
- `/index.html` - Hauptanwendung (kritisch)
- `/order-lists.html` - Bestelllisten (kritisch)
- `/meal-plans.html` - Menüpläne (kritisch)
- `/recipes.html` - Rezeptverwaltung (kritisch)
- `/analytics.html` - Analytics
- `/procurement.html` - Beschaffung
- `/api/health` - Health Check API (kritisch)

**Überwachte API-Endpunkte:**
- `GET /api/recipes` - Rezepte API (kritisch)
- `GET /api/config/example` - Beispiel-Konfiguration

### 2. Health Check API (`backend/health_check.py`)

**Zweck:** Bereitstellung von Health-Check-Endpunkten für Monitoring-Tools

#### `/api/health`

Basis Health Check - gibt den Status der Anwendung zurück.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T23:10:00",
  "service": "menuplan-simulator",
  "version": "1.0.0"
}
```

#### `/api/health/detailed`

Detaillierter Health Check - überprüft:
- ✅ Rezepte geladen
- ✅ Static Files verfügbar
- ✅ Kritische Dateien vorhanden
- ✅ Python-Version

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T23:10:00",
  "checks": {
    "recipes": {
      "status": "healthy",
      "count": 200
    },
    "static_files": {
      "status": "healthy",
      "html_files_count": 14,
      "html_files": ["index.html", ...]
    },
    "critical_files": {
      "status": "healthy",
      "message": "All critical files present"
    }
  }
}
```

#### `/api/health/files`

Listet alle statischen Dateien auf - hilfreich für Debugging.

**Response:**
```json
{
  "static_folder": "/app/frontend",
  "total_files": 25,
  "files": [
    {
      "path": "index.html",
      "size": 257812,
      "modified": "2025-10-22T22:10:00"
    },
    ...
  ]
}
```

## Integration

### GitHub Actions

Erstellen Sie `.github/workflows/monitoring.yml`:

```yaml
name: Link Monitoring

on:
  schedule:
    - cron: '0 */6 * * *'  # Alle 6 Stunden
  workflow_dispatch:

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
        run: python monitoring/link_monitor.py https://menuplan-simulator-v5.onrender.com
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: monitoring-results
          path: monitoring_results.json
```

### Render.com Cron Job

Fügen Sie zu `render.yaml` hinzu:

```yaml
services:
  - type: cron
    name: menuplan-monitor
    env: python
    region: frankfurt
    schedule: "0 */6 * * *"  # Alle 6 Stunden
    buildCommand: pip install requests
    startCommand: python monitoring/link_monitor.py https://menuplan-simulator-v5.onrender.com
```

### UptimeRobot / Pingdom

Konfigurieren Sie externe Monitoring-Dienste:

**URLs zum Überwachen:**
- https://menuplan-simulator-v5.onrender.com/api/health
- https://menuplan-simulator-v5.onrender.com/
- https://menuplan-simulator-v5.onrender.com/index.html

**Intervall:** Alle 5 Minuten  
**Timeout:** 30 Sekunden  
**Erwarteter Status:** 200 OK

## Benachrichtigungen

### E-Mail-Benachrichtigung

Erweitern Sie `link_monitor.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(results):
    if results['summary']['critical_failed'] == 0:
        return
    
    sender = "monitor@example.com"
    recipient = "admin@example.com"
    
    msg = MIMEMultipart()
    msg['Subject'] = f"🚨 Menüplansimulator: {results['summary']['critical_failed']} Critical Failures"
    msg['From'] = sender
    msg['To'] = recipient
    
    body = f"""
    Monitoring Alert
    
    Zeitpunkt: {results['timestamp']}
    Basis-URL: {results['base_url']}
    
    Zusammenfassung:
    - Gesamt: {results['summary']['total']}
    - Erfolgreich: {results['summary']['passed']}
    - Fehlgeschlagen: {results['summary']['failed']}
    - Kritisch: {results['summary']['critical_failed']}
    
    Fehlerhafte URLs:
    """
    
    for url in results['urls']:
        if not url['success'] and url['critical']:
            body += f"\\n- {url['name']}: {url['message']}"
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, "your-app-password")
        server.send_message(msg)
```

### Slack-Benachrichtigung

```python
import requests

def send_slack_alert(results):
    if results['summary']['critical_failed'] == 0:
        return
    
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        return
    
    failed_urls = [
        f"• {url['name']}: {url['message']}"
        for url in results['urls']
        if not url['success'] and url['critical']
    ]
    
    message = {
        "text": f"🚨 *Menüplansimulator Monitoring Alert*",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{results['summary']['critical_failed']} kritische Fehler gefunden*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Gesamt:*\\n{results['summary']['total']}"},
                    {"type": "mrkdwn", "text": f"*Fehlgeschlagen:*\\n{results['summary']['failed']}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\\n".join(failed_urls)
                }
            }
        ]
    }
    
    requests.post(webhook_url, json=message)
```

## Troubleshooting

### Problem: order-lists.html und meal-plans.html geben 404

**Diagnose:**
```bash
# 1. Prüfen Sie, welche Dateien vorhanden sind
curl https://menuplan-simulator-v5.onrender.com/api/health/files

# 2. Prüfen Sie den detaillierten Health Check
curl https://menuplan-simulator-v5.onrender.com/api/health/detailed

# 3. Prüfen Sie die Render.com Logs
```

**Mögliche Ursachen:**
1. Dateien wurden nicht deployed
2. Flask findet das static_folder nicht
3. Routen sind falsch konfiguriert
4. Gunicorn-Konfiguration stimmt nicht

**Lösung:**
1. Überprüfen Sie, ob die Dateien im Git-Repository sind: `git ls-files frontend/`
2. Prüfen Sie die Flask-Konfiguration: `static_folder='../frontend'`
3. Prüfen Sie die Render.com Build-Logs
4. Triggern Sie ein neues Deployment

### Problem: Health Check API gibt 404

**Diagnose:**
```bash
# Prüfen Sie, ob die Route registriert ist
curl https://menuplan-simulator-v5.onrender.com/api/health
```

**Lösung:**
1. Stellen Sie sicher, dass `register_health_routes(app)` aufgerufen wird
2. Prüfen Sie, ob `health_check.py` deployed wurde
3. Prüfen Sie die Import-Statements in `app.py`

## Best Practices

1. **Regelmäßige Überwachung:** Führen Sie das Monitoring mindestens alle 6 Stunden aus
2. **Benachrichtigungen:** Richten Sie E-Mail- oder Slack-Benachrichtigungen ein
3. **Logs aufbewahren:** Speichern Sie Monitoring-Ergebnisse für historische Analysen
4. **Externe Monitoring-Dienste:** Verwenden Sie zusätzlich UptimeRobot oder Pingdom
5. **Deployment-Tests:** Führen Sie Monitoring nach jedem Deployment aus

## Metriken

Das Monitoring-System erfasst folgende Metriken:

- **Verfügbarkeit:** Prozentsatz erfolgreicher Checks
- **Response-Zeit:** Zeit bis zur Antwort (in Zukunft)
- **Fehlerrate:** Anzahl fehlgeschlagener Checks
- **Kritische Fehler:** Anzahl kritischer Ausfälle

## Zukünftige Erweiterungen

- [ ] Response-Zeit-Messung
- [ ] Performance-Metriken
- [ ] Datenbank-Health-Checks
- [ ] Memory/CPU-Überwachung
- [ ] Historische Trend-Analyse
- [ ] Dashboard-Visualisierung
- [ ] Automatische Wiederherstellung

