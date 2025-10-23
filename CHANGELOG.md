# Changelog - Menüplansimulator v1.0

## [Bugfix] - 2025-10-23

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
