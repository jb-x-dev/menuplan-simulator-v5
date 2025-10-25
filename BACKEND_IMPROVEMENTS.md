# Backend-Verbesserungen - Menuplansimulator v5

## Implementierte Features

### 1. Portionsanpassung pro Rezept ✅

**Datei**: `backend/simulator.py`

**Änderungen**:
- `MealSlot` Klasse erweitert um `portions` Feld (1-500)
- `cost` Property berechnet jetzt automatisch basierend auf Portionen
- Formel: `(base_cost / calculation_basis) * portions`
- `to_dict()` Methode inkludiert jetzt Portionen

**Beispiel**:
```python
meal_slot = MealSlot(
    options=[recipe1, recipe2],
    selected_index=0,
    portions=50  # NEU: Portionsanzahl
)
# Kosten werden automatisch mit Portionen multipliziert
total_cost = meal_slot.cost  # (recipe.cost / recipe.calculation_basis) * 50
```

### 2. Menüplan-Management-System ✅

**Datei**: `backend/menuplan_manager.py` (NEU)

**Klassen**:
- `MenuPlanMetadata`: Metadaten für Menüpläne
  - `id`: Eindeutige ID
  - `name`: Name des Plans
  - `status`: 'Entwurf', 'Vorlage', 'Aktiv', 'Archiviert'
  - `created_at`, `updated_at`: Zeitstempel
  - `start_date`, `end_date`: Zeitraum
  - `total_cost`, `bkt_average`: Kostenstatistiken
  - `description`, `tags`: Zusätzliche Infos

- `OrderListMetadata`: Metadaten für Bestelllisten
  - `id`, `name`, `created_at`
  - `menu_plan_id`, `menu_plan_name`
  - `total_items`, `total_cost`
  - `order_date`, `supplier`, `notes`

- `MenuPlanManager`: Hauptklasse für Verwaltung
  - `save_menu_plan()`: Speichert Plan mit Metadaten
  - `load_menu_plan()`: Lädt gespeicherten Plan
  - `list_menu_plans()`: Listet alle Pläne (filterbar nach Status)
  - `update_menu_plan_status()`: Ändert Status
  - `delete_menu_plan()`: Löscht Plan
  - `duplicate_menu_plan()`: Dupliziert Plan
  - `save_order_list()`, `load_order_list()`, etc.
  - `calculate_bkt_statistics()`: Berechnet BKT-Statistiken

**Speicherung**:
- JSON-basiert in `data/menu_plans/` und `data/order_lists/`
- Automatische Verzeichniserstellung
- Zeitstempel-basierte IDs

### 3. Neue API-Endpunkte ✅

**Datei**: `backend/app.py`

**Menüplan-Endpunkte**:
- `GET /api/menu-plans`: Liste aller Pläne (optional: `?status=Aktiv`)
- `GET /api/menu-plans/<plan_id>`: Spezifischen Plan laden
- `POST /api/menu-plans`: Plan speichern
- `PUT /api/menu-plans/<plan_id>/status`: Status ändern
- `DELETE /api/menu-plans/<plan_id>`: Plan löschen
- `POST /api/menu-plans/<plan_id>/duplicate`: Plan duplizieren
- `PUT /api/menu-plans/<plan_id>/portions`: Portionen aktualisieren

**Bestelllisten-Endpunkte**:
- `GET /api/order-lists`: Liste aller Bestelllisten
- `GET /api/order-lists/<order_id>`: Spezifische Liste laden
- `POST /api/order-lists`: Liste speichern
- `DELETE /api/order-lists/<order_id>`: Liste löschen

**Beispiel-Requests**:

```javascript
// Plan speichern
fetch('/api/menu-plans', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    metadata: {
      id: '',
      name: 'KW 42 - Herbstmenü',
      status: 'Entwurf',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      start_date: '2025-10-20',
      end_date: '2025-10-26',
      total_cost: 1250.50,
      bkt_average: 3.50,
      description: 'Herbstliche Menüs mit regionalen Zutaten'
    },
    plan: { /* Menüplan-Daten */ }
  })
});

// Status ändern
fetch('/api/menu-plans/plan_20251025_120000/status', {
  method: 'PUT',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ status: 'Aktiv' })
});

// Portionen aktualisieren
fetch('/api/menu-plans/plan_20251025_120000/portions', {
  method: 'PUT',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    day_index: 0,
    meal_name: 'Mittagessen',
    portions: 75
  })
});
```

### 4. BKT-Statistik-Berechnung ✅

**Methode**: `MenuPlanManager.calculate_bkt_statistics()`

**Berechnet**:
- `average_bkt`: Durchschnittlicher BKT über alle Tage
- `min_bkt`: Niedrigster Tages-BKT
- `max_bkt`: Höchster Tages-BKT
- `total_cost`: Gesamtkosten des Plans
- `days_count`: Anzahl der Tage
- `daily_bkts`: Liste der BKT-Werte pro Tag

**Logik**:
- Berücksichtigt nur Hauptmahlzeiten (Mittagessen, Abendessen) für BKT
- Formel: `BKT = Tageskosten / Hauptmahlzeit-Portionen`
- Automatische Anpassung bei Portionsänderungen

### 5. Erweiterte SimulatorConfig ✅

**Datei**: `backend/simulator.py`

**Neue Eigenschaften**:
- `bkt_tolerance`: Toleranz für BKT-Abweichungen (bereits vorhanden)
- `bkt_min`, `bkt_max`: Berechnete Min/Max-Werte basierend auf Toleranz
- `recipe_options_count`: Anzahl der Rezeptoptionen pro Mahlzeit (Standard: 2)

## Nächste Schritte (Frontend-Integration)

### 1. Portionen-UI
- Input-Felder neben jedem Rezept
- Min: 1, Max: 500
- Automatische Kostenaktualisierung bei Änderung

### 2. Rezept-Info-Button
- Info-Icon (ℹ️) neben Rezeptnamen
- Modal mit vollständigen Rezeptdetails:
  - Zutaten
  - Allergene
  - Nährwerte
  - Zubereitungszeit
  - Beschreibung

### 3. Status-Management-UI
- Dropdown für Status-Auswahl
- Farbcodierung:
  - Entwurf: Grau
  - Vorlage: Blau
  - Aktiv: Grün
  - Archiviert: Orange
- Filter-Buttons im Header

### 4. Header-Menü
- Dropdown "Gespeicherte Menüpläne"
- Dropdown "Gespeicherte Bestelllisten"
- Automatische Aktualisierung

### 5. BKT-Anzeige
- Tages-BKT pro Tag anzeigen
- Gesamt-BKT mit Toleranzbereich
- Warnungen bei Überschreitung
- Farbcodierung (Grün/Gelb/Rot)

### 6. Kollektive Mengensteuerung
- Globales Eingabefeld im Header
- Checkboxen neben Rezepten
- Optionen:
  - "Auf alle anwenden"
  - "Nur auf billigstes"
  - "Nur auf teuerstes"

## Testing

### Unit-Tests erstellen für:
- `MealSlot.cost` mit verschiedenen Portionen
- `MenuPlanManager.save_menu_plan()`
- `MenuPlanManager.calculate_bkt_statistics()`
- API-Endpunkte (alle CRUD-Operationen)

### Integration-Tests:
- Vollständiger Workflow: Plan erstellen → Speichern → Laden → Status ändern → Löschen
- Portionen ändern → Kosten neu berechnen
- BKT-Statistiken mit verschiedenen Plänen

## Performance-Überlegungen

- JSON-Dateien funktionieren gut für <100 Pläne
- Bei >100 Plänen: Migration zu SQLite empfohlen
- Caching für häufig geladene Pläne implementieren
- Lazy-Loading für große Rezeptlisten

## Sicherheit

- Input-Validierung für alle API-Endpunkte
- Sanitization von Dateinamen (bereits durch Zeitstempel-IDs gelöst)
- Zugriffskontrolle (TODO: Multi-User-Support)

## Dokumentation

- API-Dokumentation mit Swagger/OpenAPI (TODO)
- Benutzerhandbuch für neue Features (TODO)
- Entwickler-Guide für Erweiterungen (TODO)

