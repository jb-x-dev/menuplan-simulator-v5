# 🍽️ Menüplansimulator

Automatische und manuelle Menüplanerstellung für Großküchen und Catering-Unternehmen.

## 🌟 Features

- **Automatische Menüplan-Generierung** mit KI-gestützter Rezeptauswahl
- **Manuelle Menüplan-Erstellung** mit flexibler Rezeptauswahl
- **BKT-Berechnung** (Rohkostbudget pro Tag) basierend auf Hauptmahlzeiten
- **Bestelllisten-Generierung** für Lieferanten
- **PDF-Export** für Menüpläne und Bestelllisten
- **Excel-Export** für Portionsübersichten
- **Simulationsparameter** für detaillierte Menüplanung
- **Allergene-Verwaltung** und Ernährungsformen
- **Rezeptverwaltung** mit Kosten- und Nährwertinformationen

## 🚀 Live-Demo

Die Anwendung ist live verfügbar unter: **[Wird nach Deployment aktualisiert]**

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

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 📧 Kontakt

Bei Fragen oder Problemen:
- GitHub Issues: [Repository Issues]
- E-Mail: [Ihre E-Mail]

---

**Entwickelt mit ❤️ für bessere Menüplanung**
