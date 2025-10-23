# Changelog - Menüplansimulator v1.0

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
