# Menuplansimulator v5 - TODO

## Bugs

- [ ] Fix: Mahlzeiten-Auswahl und Vorbelegung funktioniert nicht
  - Problem: Mahlzeiten werden nicht korrekt angezeigt/vorbelegt
  - Status: In Bearbeitung

- [x] Fix: Mahlzeiten-Auswahl aus Einstellungen berücksichtigen
  - Problem: Alle Mahlzeiten wurden verwendet, nicht nur die aktivierten
  - Lösung: Aktiv/Inaktiv-Toggle für jede Mahlzeit hinzugefügt
  - Nur aktive Mahlzeiten werden für Generierung verwendet
  - Standard: Frühstück, Mittagessen, Abendessen aktiv
  - Status: Behoben

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

