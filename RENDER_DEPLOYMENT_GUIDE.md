# 🚀 Render.com Deployment - Schritt-für-Schritt Anleitung

## Menuplansimulator v5.0 - Deployment Guide

**Repository**: https://github.com/jb-x-dev/menuplan-simulator-v5  
**Geschätzte Zeit**: 5-10 Minuten  
**Kosten**: Kostenlos (Free Tier)

---

## Voraussetzungen

- ✅ GitHub Account (bereits vorhanden)
- ✅ Repository ist öffentlich oder Render hat Zugriff
- ⏳ Render.com Account (wird erstellt)
- ⏳ Kreditkarte (für Free Tier Verifizierung, keine Kosten)

---

## Schritt 1: Render.com Account erstellen

### 1.1 Registrierung

1. Öffne https://render.com
2. Klicke auf **"Get Started for Free"**
3. Wähle **"Sign up with GitHub"**
4. Autorisiere Render für GitHub-Zugriff
5. Bestätige deine E-Mail-Adresse

### 1.2 Kreditkarte hinzufügen (für Free Tier)

1. Gehe zu **Account Settings** → **Billing**
2. Klicke auf **"Add Payment Method"**
3. Gib Kreditkartendaten ein
4. **Hinweis**: Free Tier bleibt kostenlos, Karte ist nur zur Verifizierung

---

## Schritt 2: Web Service erstellen

### 2.1 Neuen Service anlegen

1. Klicke auf **"New +"** (oben rechts)
2. Wähle **"Web Service"**
3. Verbinde dein GitHub Repository:
   - Klicke auf **"Connect a repository"**
   - Suche nach: `jb-x-dev/menuplan-simulator-v5`
   - Klicke auf **"Connect"**

### 2.2 Service konfigurieren

Render erkennt automatisch die `render.yaml` Konfiguration. Überprüfe folgende Einstellungen:

**Basic Settings:**
- **Name**: `menuplan-simulator-v5` (oder eigener Name)
- **Region**: `Frankfurt (EU Central)` (empfohlen für Europa)
- **Branch**: `main`
- **Root Directory**: (leer lassen)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`

**Instance Type:**
- **Plan**: `Free` (0 USD/Monat)
- **RAM**: 512 MB
- **CPU**: 0.1 vCPU

### 2.3 Environment Variables (optional)

Keine zusätzlichen Environment Variables erforderlich. Die Anwendung funktioniert out-of-the-box.

Optional kannst du hinzufügen:
- `FLASK_DEBUG=False` (für Produktion)
- `LOG_LEVEL=INFO`

### 2.4 Service erstellen

1. Scrolle nach unten
2. Klicke auf **"Create Web Service"**
3. Warte auf Deployment (~5-10 Minuten)

---

## Schritt 3: Deployment überwachen

### 3.1 Build-Prozess

Du siehst jetzt den Build-Log in Echtzeit:

```
==> Cloning from https://github.com/jb-x-dev/menuplan-simulator-v5...
==> Checking out commit f666835...
==> Running build command 'pip install -r requirements.txt'...
    Collecting Flask==3.0.0
    Collecting flask-cors==4.0.0
    Collecting gunicorn==21.2.0
    ...
==> Build successful!
==> Deploying...
==> Your service is live 🎉
```

### 3.2 Deployment-Status

Oben rechts siehst du den Status:
- 🟡 **Building**: Build läuft
- 🟡 **Deploying**: Deployment läuft
- 🟢 **Live**: Service ist online

### 3.3 URL erhalten

Nach erfolgreichem Deployment siehst du die URL:
```
https://menuplan-simulator-v5.onrender.com
```

**Wichtig**: Beim ersten Aufruf kann es 30-60 Sekunden dauern (Cold Start).

---

## Schritt 4: Anwendung testen

### 4.1 Erste Schritte

1. Öffne die URL in deinem Browser
2. Warte auf Cold Start (beim ersten Mal)
3. Du solltest die Startseite sehen

### 4.2 Funktionen testen

**Automatische Generierung:**
1. Wähle Zeitraum (z.B. 2 Wochen)
2. Setze BKT-Ziel (z.B. 3.50 €)
3. Klicke auf **"🤖 Menüplan generieren"**
4. Warte auf Ergebnis (~5-10 Sekunden)

**Einstellungen:**
1. Klicke auf **"⚙️ Einstellungen"**
2. Modal sollte sich öffnen
3. Teste alle Tabs

**Export:**
1. Generiere einen Menüplan
2. Klicke auf **"📄 PDF exportieren"**
3. PDF sollte heruntergeladen werden

### 4.3 Erwartete Performance

- **Cold Start**: 30-60 Sekunden (nach 15 Min Inaktivität)
- **Warm Start**: < 2 Sekunden
- **API-Requests**: 2-5 Sekunden
- **PDF-Export**: 3-8 Sekunden

---

## Schritt 5: Automatische Deployments einrichten

### 5.1 Auto-Deploy aktivieren

Render deployed automatisch bei jedem Push zu `main`:

1. Gehe zu **Settings** → **Build & Deploy**
2. Stelle sicher, dass **"Auto-Deploy"** aktiviert ist
3. Branch: `main`

### 5.2 Deployment-Trigger

Jedes Mal, wenn du Code zu GitHub pushst:
```bash
git push origin main
```

Startet Render automatisch ein neues Deployment (~2-3 Minuten).

---

## Schritt 6: Monitoring & Logs

### 6.1 Logs anzeigen

1. Gehe zu **Logs** Tab
2. Sieh Live-Logs der Anwendung
3. Filtere nach Fehler/Warnungen

### 6.2 Metrics

1. Gehe zu **Metrics** Tab
2. Sieh CPU/RAM-Nutzung
3. Überwache Request-Zeiten

### 6.3 Events

1. Gehe zu **Events** Tab
2. Sieh Deployment-Historie
3. Rollback zu früheren Versionen möglich

---

## ⚠️ Wichtige Hinweise

### Datenpersistenz

**Problem**: Render Free Tier hat **keinen persistenten Storage**!

- Gespeicherte Menüpläne gehen bei Service-Neustart verloren
- Bestelllisten werden nicht dauerhaft gespeichert
- LocalStorage im Browser bleibt erhalten

**Lösung für Produktion**:
1. PostgreSQL Datenbank hinzufügen (Render bietet Free Tier)
2. Oder: S3-kompatiblen Storage nutzen
3. Oder: Upgrade auf kostenpflichtigen Plan mit Persistent Disk

### Performance

**Free Tier Limitierungen**:
- Service schläft nach 15 Minuten Inaktivität
- Cold Start: 30-60 Sekunden
- Shared CPU (0.1 vCPU)
- 512 MB RAM

**Für bessere Performance**:
- Upgrade auf **Starter Plan** ($7/Monat)
- Kein Sleep-Modus
- Dedicated CPU
- 1 GB RAM

### Custom Domain

**Eigene Domain verbinden**:
1. Gehe zu **Settings** → **Custom Domains**
2. Klicke auf **"Add Custom Domain"**
3. Gib deine Domain ein (z.B. `menuplan.example.com`)
4. Folge DNS-Anweisungen
5. SSL-Zertifikat wird automatisch erstellt

---

## 🔧 Troubleshooting

### Problem: Build schlägt fehl

**Fehler**: `ERROR: Could not find a version that satisfies the requirement`

**Lösung**:
1. Prüfe `requirements.txt` auf Tippfehler
2. Stelle sicher, dass Python 3.11 verwendet wird
3. Checke Build-Logs für Details

### Problem: Service startet nicht

**Fehler**: `Application failed to start`

**Lösung**:
1. Prüfe Start Command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
2. Stelle sicher, dass `backend/app.py` existiert
3. Checke Logs für Python-Fehler

### Problem: 502 Bad Gateway

**Fehler**: Service ist deployed, aber nicht erreichbar

**Lösung**:
1. Warte 2-3 Minuten (Deployment dauert)
2. Prüfe Logs auf Fehler
3. Restart Service manuell

### Problem: Sehr langsam

**Ursache**: Cold Start nach Inaktivität

**Lösung**:
1. Warte 30-60 Sekunden beim ersten Aufruf
2. Danach sollte es schneller sein
3. Oder: Upgrade auf kostenpflichtigen Plan

---

## 📊 Deployment-Checkliste

### Vor dem Deployment:
- ✅ Code zu GitHub gepusht
- ✅ `render.yaml` konfiguriert
- ✅ `requirements.txt` aktuell
- ✅ Bugs behoben
- ✅ Dokumentation erstellt

### Während des Deployments:
- ⏳ Render.com Account erstellen
- ⏳ Repository verbinden
- ⏳ Service konfigurieren
- ⏳ Build überwachen
- ⏳ Deployment abwarten

### Nach dem Deployment:
- ⏳ URL testen
- ⏳ Funktionen durchgehen
- ⏳ Performance prüfen
- ⏳ Logs überwachen
- ⏳ Auto-Deploy aktivieren

---

## 🎉 Fertig!

Dein Menuplansimulator ist jetzt live unter:
```
https://menuplan-simulator-v5.onrender.com
```

### Nächste Schritte:

1. **Teile die URL** mit Benutzern
2. **Sammle Feedback** zur Funktionalität
3. **Überwache Logs** auf Fehler
4. **Plane v5.1** mit Performance-Verbesserungen

### Support:

- **GitHub Issues**: https://github.com/jb-x-dev/menuplan-simulator-v5/issues
- **Render Docs**: https://render.com/docs
- **Render Support**: https://render.com/support

---

## 📚 Weitere Ressourcen

- **DEPLOYMENT_GUIDE_V5.md** - Technische Details
- **BUG_ANALYSIS.md** - Bekannte Probleme
- **V5_DEVELOPMENT_SUMMARY.md** - Entwicklungshistorie
- **README.md** - Feature-Übersicht

---

**Viel Erfolg mit deinem Menuplansimulator! 🍽️**

---

*Erstellt am: 25. Oktober 2025*  
*Version: 5.0*  
*Status: Deployment-Ready*

