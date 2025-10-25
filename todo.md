# Menuplansimulator v5 - TODO

## Bugs

- [x] Systematische Fehlersuche und Behebung
  - self.recipes vs self.all_recipes Inkonsistenz behoben
  - Statistik-Feldnamen korrigiert (avg_bkt, min_bkt, max_bkt)
  - Debug-Logging verbessert
  - Menüplan-Generierung funktioniert end-to-end
  - Status: Abgeschlossen

- [x] Fix: Mahlzeiten-Auswahl und Vorbelegung funktioniert nicht
  - Problem: Dynamisches API-Laden verursachte Probleme
  - Lösung: Hardcoded Werte die EXAKT mit Rezept-Daten übereinstimmen
  - 4 Mahlzeiten: Frühstück, Mittagessen, Abendessen (aktiv), Zwischenmahlzeit (inaktiv)
  - Status: Behoben

- [x] Fix: Mahlzeiten-Auswahl aus Einstellungen berücksichtigen
  - Problem: Alle Mahlzeiten wurden verwendet, nicht nur die aktivierten
  - Lösung: Aktiv/Inaktiv-Toggle für jede Mahlzeit hinzugefügt
  - Nur aktive Mahlzeiten werden für Generierung verwendet
  - Standard: Frühstück, Mittagessen, Abendessen aktiv
  - Status: Behoben

## Bugs

- [x] "No recipes for Frühstück/Frühstück" Fehler beheben
  - Ursache: LocalStorage hatte alte dietary_forms ohne 'Vegan'
  - Vegane Frühstücks-Rezepte wurden ausgefiltert
  - Lösung: Alle 3 Formen beim Laden erzwingen
  - localStorage.removeItem('selectedDietaryForms')
  - Status: Behoben

- [x] Allergene standardmäßig deselektieren
  - selectedAllergens = [] beim Laden erzwungen
  - LocalStorage für Allergene gelöscht
  - Status: Behoben

- [x] "Zwischengang" vs "Zwischenmahlzeit" Naming-Mismatch
  - Ursache: Browser-Cache hatte alte mealSettings
  - Lösung 1: localStorage für mealSettings ignorieren
  - Lösung 2: Settings-Versionierung (v5.0.1) mit automatischem Cache-Clear
  - Debug-Spam im Backend entfernt
  - Erfolgreich getestet auf Live-Site
  - Status: Behoben

## Features (aktuell)

- [x] Automatische Menüplan-Generierung beim Seitenaufruf
  - Menüplan wird automatisch beim Laden generiert
  - Kein manueller Klick auf "Generieren" nötig
  - Sofort gefüllter Menüplan sichtbar
  - 500ms Verzögerung für Initialisierung
  - window.addEventListener('load') + btn.click()
  - Status: Abgeschlossen

- [x] Rezept-Auswahl und Menülinien aus Einstellungen entfernen
  - Entfernt: Rezept-Auswahl Tab + Menülinien Tab
  - Behalten: Alle anderen Tabs (Laufzeiten, Allergene, Ernährungsformen, Rezeptgruppen, Garmethoden, Abneigungen, Standardwerte)
  - Alle 200 Rezepte immer verfügbar (kein Auswahlsystem mehr)
  - Auto-Initialisierung deaktiviert
  - UX vereinfacht
  - Status: Abgeschlossen

- [x] Auto-Generierung sofort funktionsfähig machen
  - Standard-Rezepte vorausgewählt: 80 Rezepte (40% der Gesamtmenge)
  - Ausgewogene Verteilung: Frühstück 15, Mittagessen 40, Abendessen 15, Zwischenmahlzeit 10
  - BKT-Zielwert: 5.50€ (realistisch)
  - BKT-Toleranz: 10%
  - Automatische Initialisierung beim ersten Start
  - Status: Abgeschlossen

- [x] Versionsanzeige unter Menüpunkt Start
  - Version aus VERSION Datei laden
  - API-Endpunkt: GET /api/version
  - Anzeige unter Header (kleine graue Schrift)
  - Auto-Load beim Seitenaufruf
  - Status: Abgeschlossen

- [x] Rezept-Auswahl-System implementieren
  - SQLite Datenbank für persistente Speicherung
  - 8 neue API-Endpunkte
  - Alle Rezepte standardmäßig nicht ausgewählt
  - Nur explizit ausgewählte Rezepte werden bei Generierung verwendet
  - Auswahl-UI in Einstellungen mit Filter und Suche
  - Status: Abgeschlossen

## Features (für v5.1)

- [ ] Performance-Optimierung für API-Requests
- [ ] Input-Validierung für Portionen und BKT
- [ ] Ladeanimationen während Requests
- [ ] LocalStorage Quota-Prüfung
- [ ] Timeout-Handling bei Netzwerkfehlern

## Deployment

- [x] AssertionError bei doppelten Endpunkten behoben
- [x] Render.com Deployment erfolgreich
- [x] Service läuft auf Render.com



- [x] Fehler beim Speichern des Menüplans
  - Ursache: Falscher API-Endpunkt (/api/menu-plans/save statt /api/menu-plans)
  - Ursache 2: Falsche Datenstruktur (fehlte metadata-Objekt)
  - Lösung: Korrigierte URL und Datenstruktur
  - Metadaten werden jetzt aus currentPlan berechnet
  - Status: Behoben



- [ ] Bestelllisten aus aktiven Menüplänen generieren
  - Auf Bestelllisten-Seite (📋 Bestelllisten)
  - Liste aller Menüpläne mit Status "Aktiv" anzeigen
  - Checkboxen zur Auswahl mehrerer Menüpläne
  - Button "Bestellliste generieren"
  - Aggregierte Bestellliste erstellen:
    * Alle Rezepte aus ausgewählten Menüplänen
    * Gesamtmengen pro Rezept/Zutat
    * Nach Kategorien gruppiert
  - Status: In Bearbeitung

