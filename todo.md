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

## Features (aktuell)

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

