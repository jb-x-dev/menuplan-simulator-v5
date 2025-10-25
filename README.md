# 🍽️ Menüplansimulator v5.0

Professionelle Menüplanerstellung für Großküchen und Catering-Unternehmen mit erweiterten Management-Features.

## 🌟 Features

### Kern-Features
- **Automatische Menüplan-Generierung** mit KI-gestützter Rezeptauswahl
- **Manuelle Menüplan-Erstellung** mit flexibler Rezeptauswahl
- **BKT-Berechnung** (Rohkostbudget pro Tag) basierend auf Hauptmahlzeiten
- **Bestelllisten-Generierung** für Lieferanten
- **PDF-Export** für Menüpläne und Bestelllisten
- **Excel-Export** für Portionsübersichten
- **Simulationsparameter** für detaillierte Menüplanung
- **Allergene-Verwaltung** und Ernährungsformen
- **Rezeptverwaltung** mit Kosten- und Nährwertinformationen (200 Rezepte)

### ✨ Neu in v5.0
- **Portionsanpassung** (1-500) pro Rezept mit automatischer Kostenberechnung
- **Menüplan-Status-System** (Entwurf, Vorlage, Aktiv, Archiviert)
- **Erweiterte Menüplan-Verwaltung** (Speichern, Laden, Duplizieren, Löschen)
- **Bestelllisten-Management** mit Metadaten und Zeitstempel
- **BKT-Statistiken** mit detaillierter Analyse und Toleranz-Berechnung
- **12 neue API-Endpunkte** für vollständige CRUD-Operationen

## 🚀 Live-Demo

Die Anwendung kann auf Render.com deployed werden. Siehe [DEPLOYMENT_GUIDE_V5.md](DEPLOYMENT_GUIDE_V5.md) für Details.

## 📋 Voraussetzungen

- Python 3.11+
- Flask 3.0.0
- Weitere Abhängigkeiten siehe `requirements.txt`

## 🛠️ Installation

### Lokale Installation

```bash
# Repository klonen
git clone https://github.com/IHR-USERNAME/menuplan-simulator.git
cd menuplan-simulator

# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
python3 backend/app.py

# Browser öffnen: http://localhost:5000
```

### Deployment auf Render.com

1. Repository auf GitHub pushen
2. Bei Render.com anmelden
3. "New Web Service" erstellen
4. Repository verbinden
5. Render erkennt automatisch die `render.yaml` Konfiguration
6. Deploy starten

## 📁 Projektstruktur

```
menuplan-simulator-v1.0/
├── backend/
│   ├── app.py              # Flask-Server
│   ├── recipes.json        # Rezeptdatenbank
│   └── ...
├── frontend/
│   ├── index.html          # Hauptseite
│   └── ...
├── requirements.txt        # Python-Abhängigkeiten
├── render.yaml            # Render.com Konfiguration
├── CHANGELOG.md           # Änderungshistorie
└── README.md              # Diese Datei
```

## 🎯 Verwendung

### Automatische Generierung

1. Modus "Automatisch" wählen
2. Zeitraum konfigurieren (Jahr, KW, Dauer)
3. Budget (BKT) festlegen
4. Mahlzeiten und Ernährungsformen auswählen
5. "Automatisch generieren" klicken

### Manuelle Erstellung

1. Modus "Manuell" wählen
2. "Leeren Plan erstellen"
3. Rezepte für jeden Tag manuell auswählen
4. Bestellmengen anpassen
5. Plan speichern oder exportieren

## 📊 BKT-Berechnung

Die BKT-Berechnung (Rohkostbudget pro Tag) basiert ausschließlich auf **Hauptmahlzeiten**:

```
BKT = Gesamtkosten / Hauptmahlzeit-Portionen
```

Dies ermöglicht eine realistische Kostenplanung für Großküchen.

## 🔄 Versionsverlauf

### Version 1.0.2 (23.10.2025)
- ✅ BKT-Berechnung nur für Hauptmahlzeiten
- ✅ Simulationsparameter-Layout verbessert
- ✅ Button-Lesbarkeit verbessert

### Version 1.0.1 (23.10.2025)
- ✅ Kritischer Fehler bei "Automatisch generieren" behoben
- ✅ Statistik-Berechnung korrigiert

Siehe [CHANGELOG.md](CHANGELOG.md) für Details.

## 📚 Dokumentation

- **[DEPLOYMENT_GUIDE_V5.md](DEPLOYMENT_GUIDE_V5.md)** - Vollständige Deployment-Anleitung
- **[CHANGELOG_V5.md](CHANGELOG_V5.md)** - Detaillierte Änderungshistorie
- **[BACKEND_IMPROVEMENTS.md](BACKEND_IMPROVEMENTS.md)** - Technische Backend-Dokumentation
- **[PLANNED_IMPROVEMENTS.md](PLANNED_IMPROVEMENTS.md)** - Roadmap für zukünftige Features

## 🔧 API-Endpunkte (v5.0)

### Menüplan-Management
- `GET /api/menu-plans` - Liste aller Menüpläne
- `GET /api/menu-plans/<plan_id>` - Spezifischen Plan laden
- `POST /api/menu-plans` - Plan speichern
- `PUT /api/menu-plans/<plan_id>/status` - Status ändern
- `DELETE /api/menu-plans/<plan_id>` - Plan löschen
- `POST /api/menu-plans/<plan_id>/duplicate` - Plan duplizieren
- `PUT /api/menu-plans/<plan_id>/portions` - Portionen aktualisieren

### Bestelllisten-Management
- `GET /api/order-lists` - Liste aller Bestelllisten
- `GET /api/order-lists/<order_id>` - Spezifische Liste laden
- `POST /api/order-lists` - Liste speichern
- `DELETE /api/order-lists/<order_id>` - Liste löschen

### Bestehende Endpunkte
- `GET /api/recipes` - Alle Rezepte
- `GET /api/recipes/<recipe_id>` - Spezifisches Rezept
- `POST /api/simulate` - Menüplan generieren
- `POST /api/procurement` - Beschaffungsbedarfe auflösen
- `POST /api/export/pdf` - PDF exportieren
- `POST /api/export/excel` - Excel exportieren

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 📧 Kontakt

Bei Fragen oder Problemen:
- GitHub Issues: https://github.com/jb-x-dev/menuplan-simulator-v5/issues
- Repository: https://github.com/jb-x-dev/menuplan-simulator-v5

---

**Entwickelt mit ❤️ für bessere Menüplanung**
