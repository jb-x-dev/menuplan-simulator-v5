# Deployment-Anleitung: Menuplansimulator v5

## 🎉 Neue Features in v5

Diese Version enthält umfangreiche Verbesserungen:

- **Portionsanpassung** (1-500) pro Rezept mit automatischer Kostenberechnung
- **Menüplan-Status-System** (Entwurf, Vorlage, Aktiv, Archiviert)
- **Erweiterte Menüplan-Verwaltung** (Speichern, Laden, Duplizieren, Löschen)
- **Bestelllisten-Management** mit Metadaten und Zeitstempel
- **BKT-Statistiken** mit Toleranz-Berechnung
- **12 neue API-Endpunkte** für vollständige CRUD-Operationen

## 🚀 Deployment auf Render.com (Empfohlen)

### Voraussetzungen
- GitHub Account mit Zugriff auf `jb-x-dev/menuplan-simulator-v5`
- Render.com Account (kostenlos, erfordert Kreditkarte)

### Schritt 1: Render.com Account erstellen
1. Gehen Sie zu https://render.com
2. Klicken Sie auf "Get Started for Free"
3. Melden Sie sich mit GitHub an
4. Fügen Sie eine Kreditkarte hinzu (für Free Tier erforderlich)

### Schritt 2: Web Service erstellen
1. Klicken Sie auf "New +" → "Web Service"
2. Verbinden Sie Ihr GitHub Repository:
   - Repository: `jb-x-dev/menuplan-simulator-v5`
   - Branch: `main`
3. Konfiguration:
   - **Name**: `menuplan-simulator-v5`
   - **Environment**: `Python 3`
   - **Region**: Wählen Sie die nächstgelegene Region
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
   - **Instance Type**: `Free`

### Schritt 3: Environment Variables (Optional)
Keine zusätzlichen Environment Variables erforderlich. Die Anwendung funktioniert out-of-the-box.

Optional können Sie setzen:
- `PYTHON_VERSION`: `3.11.0` (bereits in render.yaml definiert)

### Schritt 4: Deploy starten
1. Klicken Sie auf "Create Web Service"
2. Render startet automatisch den Build-Prozess
3. Warten Sie ~5-10 Minuten für den ersten Deploy
4. Die URL wird angezeigt: `https://menuplan-simulator-v5.onrender.com`

### Schritt 5: Testen
1. Öffnen Sie die Render-URL
2. Sie sollten die Landing Page sehen
3. Klicken Sie auf "Zur Anwendung" → Hauptseite öffnet sich
4. Testen Sie:
   - Automatische Menüplan-Generierung
   - Manuelle Menüplan-Erstellung
   - Rezeptverwaltung
   - Bestelllisten-Export

## 📊 Monitoring & Logs

### Render Dashboard
- **Logs**: Echtzeit-Logs im Render Dashboard
- **Metrics**: CPU, Memory, Response Time
- **Health Checks**: Automatisch über `/api/health`

### Health Check Endpunkt
```bash
curl https://menuplan-simulator-v5.onrender.com/api/health
```

Erwartete Antwort:
```json
{
  "status": "healthy",
  "version": "1.0.2",
  "recipes_loaded": 200,
  "timestamp": "2025-10-25T10:30:00Z"
}
```

## 🔄 Updates deployen

### Automatisches Deployment
Render deployed automatisch bei jedem Push zu `main`:

```bash
cd /path/to/menuplan-simulator-v5
git add .
git commit -m "feat: Add new feature"
git push origin main
```

Render erkennt den Push und startet automatisch einen neuen Deploy.

### Manuelles Deployment
Im Render Dashboard:
1. Gehen Sie zu Ihrem Service
2. Klicken Sie auf "Manual Deploy" → "Deploy latest commit"

## 🐛 Troubleshooting

### Problem: "Application failed to respond"
**Lösung**: 
- Prüfen Sie die Logs im Render Dashboard
- Stellen Sie sicher, dass `gunicorn` korrekt installiert ist
- Überprüfen Sie die `requirements.txt`

### Problem: "Port already in use"
**Lösung**:
- Render setzt automatisch `$PORT` Environment Variable
- Start Command muss `--bind 0.0.0.0:$PORT` enthalten

### Problem: "Module not found"
**Lösung**:
- Prüfen Sie `requirements.txt` auf fehlende Dependencies
- Trigger einen neuen Deploy: "Clear build cache & deploy"

### Problem: "Static files not loading"
**Lösung**:
- Flask serviert statische Dateien über WhiteNoise
- Prüfen Sie, ob `frontend/` Verzeichnis vorhanden ist
- Logs prüfen auf Fehler beim Laden von Dateien

## 📁 Datenpersistenz

### JSON-basierte Speicherung
Die Anwendung speichert Daten in JSON-Dateien:
- `data/menu_plans/` - Gespeicherte Menüpläne
- `data/order_lists/` - Gespeicherte Bestelllisten
- `data/recipes_200.json` - Rezeptdatenbank

### Wichtig für Render.com
⚠️ **Render Free Tier hat keinen persistenten Storage!**

Daten gehen verloren bei:
- Service-Neustart
- Neuer Deployment
- Inaktivität (Service schläft ein)

### Lösungen für Datenpersistenz

#### Option 1: Externe Datenbank (Empfohlen für Produktion)
Migrieren Sie zu PostgreSQL oder MongoDB:
- Render bietet PostgreSQL als Managed Service
- Kostenloser Plan: 90 Tage, dann $7/Monat
- Persistent und zuverlässig

#### Option 2: Cloud Storage
Nutzen Sie S3-kompatiblen Storage:
- AWS S3
- Cloudflare R2
- Backblaze B2

#### Option 3: Lokale Installation
Für persistente Daten ohne Cloud-Kosten:
```bash
git clone https://github.com/jb-x-dev/menuplan-simulator-v5.git
cd menuplan-simulator-v5
pip install -r requirements.txt
python backend/app.py
# Öffnen Sie http://localhost:5000
```

## 🔒 Sicherheit

### Produktions-Empfehlungen
1. **HTTPS**: Render bietet automatisch SSL-Zertifikate
2. **Secrets**: Nutzen Sie Render Environment Variables für sensible Daten
3. **CORS**: Konfigurieren Sie CORS für spezifische Domains
4. **Rate Limiting**: Implementieren Sie Rate Limiting für API-Endpunkte

### Environment Variables sicher setzen
Im Render Dashboard:
1. Gehen Sie zu "Environment" Tab
2. Klicken Sie auf "Add Environment Variable"
3. Setzen Sie Key/Value
4. Klicken Sie auf "Save Changes"

## 📈 Performance-Optimierung

### Render Free Tier Limits
- **CPU**: Shared
- **RAM**: 512 MB
- **Bandwidth**: 100 GB/Monat
- **Inaktivität**: Service schläft nach 15 Minuten ein
- **Kaltstart**: ~30 Sekunden

### Optimierungen
1. **Caching**: Implementieren Sie Redis für häufige Abfragen
2. **CDN**: Nutzen Sie Cloudflare für statische Assets
3. **Lazy Loading**: Laden Sie Rezepte on-demand statt alle auf einmal
4. **Kompression**: Aktivieren Sie gzip-Kompression (bereits in WhiteNoise)

## 🎯 Nächste Schritte nach Deployment

1. **Testen Sie alle Features**:
   - Automatische Generierung
   - Manuelle Erstellung
   - Menüplan speichern/laden
   - Status ändern
   - Bestelllisten generieren

2. **Monitoring einrichten**:
   - Render Metrics beobachten
   - Error Tracking (z.B. Sentry)
   - Uptime Monitoring (z.B. UptimeRobot)

3. **Feedback sammeln**:
   - Benutzer testen lassen
   - Bugs dokumentieren
   - Feature-Requests sammeln

4. **Dokumentation aktualisieren**:
   - API-Dokumentation mit Swagger
   - Benutzerhandbuch
   - Video-Tutorials

## 📞 Support

Bei Problemen:
- **GitHub Issues**: https://github.com/jb-x-dev/menuplan-simulator-v5/issues
- **Render Support**: https://render.com/docs
- **Community**: Render Community Forum

## 🎊 Deployment erfolgreich!

Ihre Menuplansimulator v5 Anwendung ist jetzt live und bereit für den Einsatz!

**Live-URL**: https://menuplan-simulator-v5.onrender.com (nach Deployment)

Viel Erfolg mit Ihrer Menüplanung! 🍽️

