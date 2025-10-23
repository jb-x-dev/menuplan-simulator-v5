# CHANGELOG

## [Version 1.1.0] - 2025-10-23

### Hinzugefügt
- **Wiederholungsabstand (minRepetition)**: Rezepte können jetzt mit einem Mindestabstand von X Tagen zwischen Wiederholungen konfiguriert werden
- **Häufigkeitsbeschränkungen**: Maximale Anzahl von Fleisch-, Süß- und Frittier-Rezepten pro Planungszeitraum (maxMeat, maxSweet, maxFried)
- **Qualitätsfilter**: Ausschluss von Rezepten mit rohen Zutaten (Rohmilch, rohe Eier, Rohwurst, rohes Fleisch)
- **Automatische Rezept-Kategorisierung**: Script zur automatischen Klassifizierung von Rezepten basierend auf Inhaltsstoffen
- **Umfassende Tests**: Test-Suite für alle neuen Simulationsparameter

### Geändert
- **Recipe-Modell erweitert**: Neue Felder `contains_meat`, `is_sweet`, `is_fried`, `is_whole_grain`, `contains_raw_milk`, `contains_raw_eggs`, `contains_raw_sausage`, `contains_raw_meat`
- **Greedy-Konstruktion**: Berücksichtigt jetzt Wiederholungsabstand und Häufigkeitslimits bei der Rezeptauswahl
- **Filterlogik**: Erweitert um Qualitätsfilter in `_filter_recipes()` Methode
- **Local Search**: Wird automatisch deaktiviert wenn Häufigkeitsbeschränkungen oder Wiederholungsabstand aktiv sind (um Constraint-Verletzungen zu vermeiden)
- **Soft Constraints**: Erlaubt kleine Überschreitungen (+2) bei Häufigkeitslimits als Fallback-Strategie

### Behoben
- **Falsch-Positive bei Süß-Erkennung**: "eis" in "Reis" wird nicht mehr als "Eis" (Dessert) erkannt
- **Frittier-Erkennung**: Unterscheidet jetzt zwischen frittiert und gebraten (nur frittierte Gerichte werden gezählt)
- **Häufigkeits-Zähler**: Werden jetzt korrekt inkrementiert wenn Rezepte ausgewählt werden

### Technische Details
- `backend/simulator.py`: Erweiterte `_greedy_construct_plan()` Methode mit Constraint-Checking
- `data/recipes_200.json`: Alle 200 Rezepte wurden automatisch kategorisiert
  - 51 Fleisch-Rezepte (25.5%)
  - 34 Süß-Rezepte (17.0%)
  - 7 Frittier-Rezepte (3.5%)
  - 2 Rezepte mit rohen Eiern (1.0%)
- `scripts/categorize_recipes.py`: Automatische Kategorisierung basierend auf Namen, Beschreibung und Zutaten
- `scripts/test_simulation_params.py`: Umfassende Test-Suite mit 3 Tests

### Test-Ergebnisse
✅ **Wiederholungsabstand**: Alle Rezepte respektieren den 7-Tage-Mindestabstand  
✅ **Häufigkeitsbeschränkungen**: Exakt 8 Fleisch-Rezepte (Limit: 8), 0 Süß, 2 Frittiert  
✅ **Qualitätsfilter**: Keine rohen Zutaten im Plan

---

## [Version 1.0.2] - 2025-10-23

### Hinzugefügt
- **BKT-Berechnung nur für Hauptmahlzeiten**: Die BKT-Berechnung bezieht sich jetzt ausschließlich auf Hauptmahlzeiten (z.B. Mittagessen), nicht mehr auf alle Portionen
- **Verbessertes Simulationsparameter-Layout**: Bessere Struktur mit abgerundeten Ecken und Schatten
- **Bessere Button-Lesbarkeit**: Buttons "Automatisch" und "Manuell" haben jetzt bessere Kontraste im inaktiven Zustand

### Geändert
- `calculatePlanStatistics()`: BKT wird jetzt als `Gesamtkosten / Hauptmahlzeit-Portionen` berechnet
- Modal-Layout für Simulationsparameter optimiert (max-width: 900px, border-radius: 12px)
- Button-Styles: Inaktive Buttons haben jetzt Hintergrund #f5f5f5 und Textfarbe #666
- Aktive Buttons haben jetzt Hintergrund #667eea und weiße Schrift

### Technische Details
- Zeile 2893-2895: BKT pro Tag basiert auf Hauptmahlzeit-Portionen
- Zeile 2917-2919: Gesamt-BKT basiert auf Hauptmahlzeit-Portionen
- Zeile 47-62: Verbesserte CSS-Styles für .mode-btn und .mode-btn.active
- Zeile 1043: Optimiertes Modal-Layout für Simulationsparameter

---

## [Version 1.0.1 - Bugfix] - 2025-10-23

### Behoben
- **Kritischer Fehler bei "Automatisch generieren"**: Die rote Fehlerbox erscheint nicht mehr
- **Statistik-Berechnung**: `calculatePlanStatistics()` Funktion korrigiert (cost_forms Fehler behoben)
- **Doppelte Funktionsdefinition**: Zweite `updateStatisticsDisplay()` Funktion entfernt
- **Automatische Portionsinitialisierung**: Neue Funktion `initializeDefaultPortions()` hinzugefügt

### Geändert
- Frontend: `index.html` - Mehrere Korrekturen in der JavaScript-Logik
- Backend: `app.py` - Cache-Control Header für besseres Entwicklungserlebnis

### Technische Details
1. Entfernung der fehlerhaften `menuLine.cost_forms.some()` Prüfung
2. Automatische Initialisierung der Portionen auf Standard-Wert (50) nach Generierung
3. Korrektur der Statistik-Anzeige durch Entfernung der doppelten Funktion

### Ergebnis
- ✅ Gesamtkosten werden korrekt berechnet und angezeigt
- ✅ Portionen werden automatisch initialisiert
- ✅ BKT-Berechnung funktioniert einwandfrei
- ✅ Keine JavaScript-Fehler mehr

---

Für detaillierte Informationen siehe: BUGFIX_REPORT.md

