# Geplante Verbesserungen für Menuplansimulator v5

## Status: In Bearbeitung

### 1. Mehrere Rezepte pro Mahlzeit ✅ (Bereits implementiert)
- **Status**: Das System unterstützt bereits `MealSlot` mit mehreren Rezeptoptionen
- **Vorhanden**: `MealSlot` Klasse mit `options` Liste
- **Verbesserung**: UI-Integration für bessere Auswahl zwischen Optionen

### 2. Portionsanpassung (1-500) pro Rezept
- **Status**: Zu implementieren
- **Anforderung**: Individuelle Portionsanpassung für jedes Rezept
- **Umsetzung**:
  - Portionen-Feld zu jedem Rezept im Menüplan hinzufügen
  - Automatische Kostenberechnung basierend auf Portionen
  - UI: Input-Feld neben jedem Rezept

### 3. Menüplan-Status-System
- **Status**: Zu implementieren
- **Anforderung**: Status-Tracking für Menüpläne
- **Stati**:
  - `Entwurf` - In Bearbeitung
  - `Vorlage` - Wiederverwendbare Vorlage
  - `Aktiv` - Aktuell in Verwendung
  - `Archiviert` - Abgeschlossen
- **Umsetzung**:
  - Status-Feld zur Menüplan-Datenstruktur hinzufügen
  - Filter-Funktion nach Status
  - Status-Änderungs-Buttons im UI

### 4. Verbesserte BKT-Berechnung mit Toleranz
- **Status**: Zu implementieren
- **Anforderung**: BKT als Maximum pro Tag, Gesamt-BKT über Plan mit Toleranz
- **Umsetzung**:
  - Tages-BKT-Anzeige
  - Gesamt-BKT-Berechnung
  - Toleranz-Parameter (z.B. ±5%)
  - Warnung bei Überschreitung

### 5. Rezept-Info-Button
- **Status**: Zu implementieren
- **Anforderung**: Detaillierte Rezeptinformationen auf Knopfdruck
- **Umsetzung**:
  - Info-Icon (ℹ️) neben jedem Rezeptnamen
  - Modal/Popup mit vollständigen Rezeptdetails:
    - Zutaten
    - Allergene
    - Nährwerte
    - Zubereitungszeit
    - Beschreibung

### 6. Kollektive & Individuelle Mengensteuerung
- **Status**: Zu implementieren
- **Anforderung**: Globale Mengenanpassung mit selektiver Anwendung
- **Umsetzung**:
  - Globales Mengen-Eingabefeld im Header
  - Checkboxen neben jedem Rezept für selektive Anwendung
  - Radio-Button-Verhalten pro Mahlzeit (nur ein Rezept aktiv)
  - Optionen:
    - Auf alle anwenden
    - Nur auf billigstes Rezept
    - Nur auf teuerstes Rezept

### 7. Bestelllisten-Management
- **Status**: Teilweise vorhanden, zu erweitern
- **Vorhanden**: Bestelllisten-Generierung
- **Verbesserungen**:
  - Automatisches Zurücksetzen der Mengen nach Bestellung
  - Zeitstempel-basierte Speicherung
  - Dropdown-Menü im Header für gespeicherte Listen
  - Tabellarische Anzeige:
    - Menüplan-Tag, Rezept, Portionen
    - Komponenten gruppiert nach Bestelltag
  - Export-Funktionen (JSON, PDF, Excel)

### 8. Header-Menü für gespeicherte Elemente
- **Status**: Zu implementieren
- **Anforderung**: Schnellzugriff auf gespeicherte Menüpläne und Bestelllisten
- **Umsetzung**:
  - Dropdown "Gespeicherte Menüpläne"
  - Dropdown "Gespeicherte Bestelllisten"
  - Automatische Aktualisierung bei neuen Einträgen

### 9. Erweiterte Beschaffungsplanung
- **Status**: Vorhanden, zu optimieren
- **Vorhanden**: `procurement.py` mit Zutatenlisten
- **Verbesserungen**:
  - Berücksichtigung von Zubereitungszeiten
  - Vorlaufzeiten für Bestellauslösung
  - Gruppierung nach Komponenten
  - Anzeige pro Bestelltag

## Implementierungsreihenfolge

1. **Phase 1** (Kritisch):
   - Portionsanpassung pro Rezept
   - Rezept-Info-Button
   - Menüplan-Status-System

2. **Phase 2** (Wichtig):
   - Verbesserte BKT-Berechnung
   - Kollektive Mengensteuerung
   - Header-Menü für gespeicherte Elemente

3. **Phase 3** (Optimierung):
   - Erweiterte Bestelllisten-Verwaltung
   - Beschaffungsplanung mit Zeitkomponente
   - UI/UX Verbesserungen

## Technische Hinweise

### Backend (Python/Flask)
- Dateistruktur: JSON-basiert in `/data`
- Hauptlogik: `backend/simulator.py`
- API: `backend/app.py`

### Frontend (HTML/JS)
- Hauptdatei: `frontend/index.html`
- Verwaltungsseiten:
  - `meal-plans.html`
  - `order-lists.html`
  - `recipes.html`

### Datenbank-Alternative
- Aktuell: JSON-Dateien
- Zukünftig: SQLite für bessere Performance und Datenkonsistenz

## Testing-Strategie

1. Unit-Tests für neue Funktionen
2. Integration-Tests für API-Endpunkte
3. UI-Tests für Benutzerinteraktionen
4. Performance-Tests für große Datensätze (200+ Rezepte)

## Deployment

- Zielplattform: Render.com oder Vercel
- Konfiguration: `render.yaml` bereits vorhanden
- Monitoring: Health-Check-Endpunkte vorhanden

