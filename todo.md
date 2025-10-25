# Menuplansimulator v5 - TODO

## Bugs

- [ ] Fix: Mahlzeiten-Auswahl stimmt nicht mit Rezept menu_component überein
  - Problem: "No recipes for Frühstück/Frühstück" Fehler weiterhin vorhanden
  - Ursache: Matching zwischen cost_form component und recipe menu_component schlägt fehl
  - Lösung: Direktes Matching im Simulator-Code korrigieren
  - Status: In Bearbeitung - API-Endpunkt erstellt, aber Matching funktioniert noch nicht

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

