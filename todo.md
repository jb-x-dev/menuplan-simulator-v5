# Menuplansimulator v5 - TODO

## Bugs

- [ ] Fix: Mahlzeiten-Auswahl stimmt nicht mit Rezept menu_component überein
  - Problem: "No recipes for Frühstück/Frühstück" Fehler
  - Ursache: Mahlzeiten-Einstellungen verwenden falsche Komponenten
  - Lösung: Mahlzeiten dynamisch aus verfügbaren Rezept-Kategorien laden

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

