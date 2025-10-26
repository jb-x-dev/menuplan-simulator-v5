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



- [x] Bestelllisten aus aktiven Menüplänen generieren
  - Neue Sektion auf order-lists.html implementiert
  - Lädt Menüpläne mit Status 'Aktiv' vom Backend (/api/menu-plans)
  - Checkboxen zur Auswahl mehrerer Menüpläne
  - Buttons: Alle auswählen/abwählen, Bestellliste generieren
  - Aggregiert Rezepte über alle ausgewählten Menüpläne
  - Erstellt Bestellliste mit Gesamtmengen pro Rezept
  - Speichert in localStorage
  - CSS-Styling mit Hover-Effekten
  - Status: Implementiert



- [ ] Fehler beim Speichern des Menüplans (persistent)
  - Backend-Endpunkt funktioniert korrekt (API-Test erfolgreich)
  - Problem: Frontend lädt alte JavaScript-Version (Browser-Cache)
  - Render.com Deployment noch nicht abgeschlossen (alter Timestamp: Oct 22)
  - Lösung: Warten auf Deployment oder aggressive Cache-Löschung
  - Status: Wartet auf Render.com Deployment



- [x] Rezeptdatenbank erweitern und pflegen
  - 100 neue Rezepte hinzugefügt (gesamt: 300 Rezepte) ✓
  - Verteilung: Frühstück 60, Mittagessen 130, Abendessen 58, Zwischenmahlzeit 52
  - Vegetarisch: 172 (57.3%), Vegan: 26 (8.7%) ✓
  - Preiskategorien: 1.10€ - 9.20€ (Durchschnitt: 3.44€) ✓
  - Internationale Küche integriert ✓
    * Asiatisch: Pad Thai, Ramen, Bibimbap, Sushi, Pho, Dim Sum, etc.
    * Mediterran: Paella, Moussaka, Tapas, Antipasti, etc.
    * Orientalisch: Shakshuka, Falafel, Mezze, Hummus, Baklava, etc.
    * Lateinamerikanisch: Chilaquiles, Burritos, Ceviche, Empanadas, etc.
  - Bestehende Rezepte geprüft (0 Verbesserungen nötig)
  - Backend aktualisiert: Lädt jetzt recipes_300.json
  - Scripts erstellt: generate_100_recipes.py, merge_and_improve_recipes.py
  - Status: Abgeschlossen



- [x] JavaScript-Fehler beim Speichern: orderListSelect is null
  - Fehlermeldung: "null is not an object (evaluating 'orderListSelect.innerHTML = ...')"
  - Ursache: headerOrderListSelect und headerMealPlanSelect existieren nicht im DOM
  - Lösung: Null-Prüfungen hinzugefügt (if (element) { ... })
  - Funktion populateHeaderDropdowns() korrigiert
  - Status: Behoben



- [x] Render.com Deployment-Fehler: ModuleNotFoundError
  - Fehler: "ModuleNotFoundError: No module named 'app'"
  - Ursache: Render.com verwendete alte Konfiguration (gunicorn app:app)
  - Lösung: start.sh Script erstellt mit explizitem backend.app:app
  - render.yaml aktualisiert: Verwendet jetzt ./start.sh
  - Status: Behoben



- [x] 5 Menüpläne erstellen und speichern
  - 5 Wochen: KW 43-47 (2025) ✓
  - Jeweils 7 Tage, 50 Personen, 3 Mahlzeiten/Tag ✓
  - Status: Aktiv ✓
  - Menüpläne:
    * KW 43: 27.10-02.11.2025 (380.00€, BKT 54.29€)
    * KW 44: 03.11-09.11.2025 (342.50€, BKT 48.93€)
    * KW 45: 10.11-16.11.2025 (414.00€, BKT 59.14€)
    * KW 46: 17.11-23.11.2025 (344.50€, BKT 49.21€)
    * KW 47: 24.11-30.11.2025 (324.50€, BKT 46.36€)
  - Bestelllisten aus jedem Menüplan generiert ✓
  - JSON-Dateien gespeichert in data/ ✓
  - Standalone Scripts erstellt ✓
  - Status: Abgeschlossen



- [x] API-Endpunkt für Import von Menüplänen und Bestelllisten
  - POST /api/import/menu-plans - Importiert alle menuplan_kw*.json ✓
  - POST /api/import/order-lists - Importiert alle orderlist_kw*.json ✓
  - Lädt Dateien aus data/ Ordner ✓
  - Speichert in Backend-Datenbank via MenuPlanManager ✓
  - Rückgabe: Import-Statistiken (imported count, errors) ✓
  - Status: Implementiert



- [ ] Automatischer Import beim Server-Start
  - Prüft ob Menüpläne/Bestelllisten bereits in DB
  - Importiert automatisch aus data/ wenn nicht vorhanden
  - Läuft beim Flask-App-Start
  - Status: In Bearbeitung

