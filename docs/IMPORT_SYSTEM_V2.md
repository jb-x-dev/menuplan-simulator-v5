# Import System V2.0 - Dokumentation

## Überblick

Das neue Import-System (Version 2.0) optimiert den automatischen Import von Menüplänen und Bestelllisten mit drei Mechanismen:

1. **Lock-File Mechanismus** - Verhindert redundante Imports
2. **Datenbank-Tracking** - Markiert importierte Dateien
3. **Menge-100-Normalisierung** - Alle Berechnungen mit Standardmenge 100

## Funktionsweise

### 1. Lock-File Mechanismus

**Datei:** `data/.import_completed`

**Zweck:** Verhindert, dass der Import bei jedem Server-Start erneut läuft.

**Inhalt:**
```json
{
  "completed_at": "2025-10-26T13:30:00",
  "imported_plans": 52,
  "imported_orders": 0,
  "version": "2.0"
}
```

**Verhalten:**
- ✅ Lock-File existiert → Import wird übersprungen
- ❌ Lock-File fehlt → Import wird durchgeführt
- 🔄 Nach erfolgreichem Import → Lock-File wird erstellt

### 2. Datenbank-Tracking

**Zweck:** Tracking welche Dateien bereits importiert wurden.

**Implementierung:**
- Import-Metadaten werden in Plan-Metadata gespeichert
- `normalized_portions`: 100
- `normalized_at`: Zeitstempel der Normalisierung

**Vorteile:**
- Nachvollziehbarkeit
- Vermeidung von Duplikaten
- Audit-Trail

### 3. Menge-100-Normalisierung

**Zweck:** Alle Menüpläne mit einheitlicher Standardmenge für konsistente Berechnungen.

**Funktionsweise:**
```python
# Vor Normalisierung
meal['portions'] = 80  # Variable Menge

# Nach Normalisierung
meal['portions'] = 100  # Standardmenge
meal['calculated_cost'] = (base_cost / calculation_basis) * 100
```

**Vorteile:**
- Konsistente Berechnungen
- Einfache Skalierung
- Vergleichbarkeit zwischen Plänen

## Verwendung

### Automatischer Import beim Server-Start

```python
# backend/app.py
from backend.auto_import_v2 import auto_import_data

# Import läuft nur beim ersten Start
auto_import_data(plan_manager, data_dir, force=False)
```

**Verhalten:**
1. Server startet
2. Prüft Lock-File
3. Wenn Lock vorhanden → Skip
4. Wenn kein Lock → Import durchführen
5. Lock-File erstellen

### Manueller Import (Force)

```python
# Import erzwingen (ignoriert Lock-File)
auto_import_data(plan_manager, data_dir, force=True)
```

**Verwendung:**
- Nach Hinzufügen neuer Dateien
- Bei Datenbank-Reset
- Für Testing

### Lock-File zurücksetzen

```python
from backend.auto_import_v2 import reset_import_lock

# Entfernt Lock-File für erneuten Import
reset_import_lock()
```

## Migration existierender Daten

### Einmalige Migration zu Menge 100

**Script:** `scripts/migrate_to_quantity_100.py`

**Verwendung:**

```bash
# Vorschau (Dry-Run)
python3 scripts/migrate_to_quantity_100.py --dry-run

# Migration durchführen
python3 scripts/migrate_to_quantity_100.py
```

**Funktionen:**
- ✅ Lädt alle existierenden Menüpläne
- ✅ Normalisiert Portionen auf 100
- ✅ Aktualisiert Kostenberechnungen
- ✅ Speichert aktualisierte Pläne
- ✅ Erstellt Migrations-Log

**Ausgabe:**
```
======================================================================
MIGRATION: Menüpläne zu Menge 100 normalisieren
======================================================================

📋 Lade alle Menüpläne...
   Gefunden: 57 Pläne

[1/57] KW 01 - 2026
   🔄 21 Mahlzeiten aktualisiert
   ✅ Gespeichert

...

======================================================================
MIGRATIONS-ZUSAMMENFASSUNG
======================================================================
Gesamt:       57 Pläne
Migriert:     52 Pläne
Übersprungen: 5 Pläne
Fehler:       0 Pläne
Änderungen:   1092 Mahlzeiten

📝 Migrations-Log gespeichert: data/migration_log.json
✅ Migration abgeschlossen!
======================================================================
```

## Deployment-Prozess

### Erstmaliges Deployment

1. **Code deployen** mit neuen Dateien:
   - `backend/auto_import_v2.py`
   - `scripts/migrate_to_quantity_100.py`

2. **Server startet**:
   - Kein Lock-File vorhanden
   - Import läuft automatisch
   - Alle Pläne werden mit Menge 100 importiert
   - Lock-File wird erstellt

3. **Migration ausführen** (falls alte Daten vorhanden):
   ```bash
   python3 scripts/migrate_to_quantity_100.py
   ```

### Folgende Deployments

1. **Server startet**:
   - Lock-File vorhanden
   - Import wird übersprungen
   - Server startet schnell

2. **Neue Daten hinzufügen**:
   - Neue JSON-Dateien zu `data/` hinzufügen
   - Lock-File löschen ODER `force=True` verwenden
   - Import läuft erneut

## Dateistruktur

```
menuplan-simulator-v5/
├── backend/
│   ├── auto_import.py          # Alt (deprecated)
│   ├── auto_import_v2.py       # NEU: Optimiertes Import-System
│   └── app.py                  # Verwendet auto_import_v2
├── scripts/
│   └── migrate_to_quantity_100.py  # Migrations-Script
├── data/
│   ├── .import_completed       # Lock-File (wird automatisch erstellt)
│   ├── migration_log.json      # Migrations-Log
│   ├── menuplan_kw01_2026.json
│   ├── menuplan_kw02_2026.json
│   └── ...
└── docs/
    └── IMPORT_SYSTEM_V2.md     # Diese Dokumentation
```

## API-Änderungen

### Keine Breaking Changes

Das neue System ist vollständig rückwärtskompatibel:
- ✅ Bestehende API-Endpunkte unverändert
- ✅ Datenbank-Schema unverändert
- ✅ Frontend-Code unverändert

### Neue Metadata-Felder

```python
class MenuPlanMetadata:
    # ... bestehende Felder ...
    
    # NEU:
    normalized_portions: int = 100
    normalized_at: str = ""
```

## Vorteile

### Performance

**Vorher:**
```
Server-Start: 5-10 Sekunden
- Import prüft alle 57 Dateien
- Lädt und vergleicht Daten
- Jedes Mal beim Start
```

**Nachher:**
```
Server-Start: 1-2 Sekunden
- Lock-File Check (instant)
- Import wird übersprungen
- Nur beim ersten Start
```

### Konsistenz

**Vorher:**
```
- Variable Portionen (80, 100, 120, ...)
- Inkonsistente Berechnungen
- Schwierige Vergleichbarkeit
```

**Nachher:**
```
- Einheitliche Menge 100
- Konsistente Berechnungen
- Einfache Skalierung
```

### Wartbarkeit

**Vorher:**
```
- Kein Tracking
- Keine Audit-Trail
- Schwierige Fehlersuche
```

**Nachher:**
```
- Lock-File Tracking
- Migrations-Log
- Nachvollziehbare Historie
```

## Troubleshooting

### Problem: Import läuft nicht

**Lösung 1:** Lock-File prüfen
```bash
ls -la data/.import_completed
```

**Lösung 2:** Lock-File löschen
```bash
rm data/.import_completed
```

**Lösung 3:** Force-Import
```python
auto_import_data(plan_manager, data_dir, force=True)
```

### Problem: Alte Daten nicht migriert

**Lösung:** Migrations-Script ausführen
```bash
python3 scripts/migrate_to_quantity_100.py
```

### Problem: Import-Fehler

**Debug-Schritte:**
1. Server-Logs prüfen
2. Lock-File prüfen
3. Datenbank-Verbindung testen
4. JSON-Dateien validieren

## Best Practices

### 1. Neue Daten hinzufügen

```bash
# 1. Neue JSON-Dateien zu data/ hinzufügen
cp new_menuplan.json data/

# 2. Lock-File löschen
rm data/.import_completed

# 3. Server neu starten (Import läuft automatisch)
```

### 2. Datenbank zurücksetzen

```bash
# 1. Datenbank löschen
rm menuplan.db

# 2. Lock-File löschen
rm data/.import_completed

# 3. Server starten (Import läuft automatisch)
```

### 3. Testing

```python
# Dry-Run Migration
python3 scripts/migrate_to_quantity_100.py --dry-run

# Force-Import für Testing
auto_import_data(plan_manager, data_dir, force=True)
```

## Changelog

### Version 2.0 (2025-10-26)

**Neue Features:**
- ✅ Lock-File Mechanismus
- ✅ Datenbank-Tracking
- ✅ Menge-100-Normalisierung
- ✅ Migrations-Script
- ✅ Verbesserte Logging

**Breaking Changes:**
- Keine

**Migration:**
- Automatisch beim ersten Start
- Optional: `migrate_to_quantity_100.py` für alte Daten

## Support

Bei Fragen oder Problemen:
1. Diese Dokumentation lesen
2. Server-Logs prüfen
3. Migrations-Log prüfen (`data/migration_log.json`)
4. Issue erstellen mit Details

