# Changelog - Menuplansimulator v5.0

## Version 5.0.0 (25.10.2025)

### 🎉 Neue Features

#### 1. Portionsanpassung pro Rezept
- **Feature**: Individuelle Portionsanpassung von 1-500 pro Rezept
- **Implementierung**: 
  - Neues `portions` Feld in `MealSlot` Klasse
  - Automatische Kostenberechnung basierend auf Portionen
  - Formel: `(base_cost / calculation_basis) * portions`
- **Nutzen**: Flexible Mengenplanung für unterschiedliche Gruppengrößen
- **API**: `PUT /api/menu-plans/<plan_id>/portions`

#### 2. Menüplan-Status-System
- **Feature**: Lifecycle-Management für Menüpläne
- **Stati**:
  - `Entwurf` - In Bearbeitung, noch nicht finalisiert
  - `Vorlage` - Wiederverwendbare Vorlagen für zukünftige Perioden
  - `Aktiv` - Aktuell in Verwendung
  - `Archiviert` - Abgeschlossen und archiviert
- **Funktionen**:
  - Status-Änderung über API
  - Filter nach Status
  - Automatische Zeitstempel-Verwaltung
- **API**: `PUT /api/menu-plans/<plan_id>/status`

#### 3. Erweiterte Menüplan-Verwaltung
- **Feature**: Vollständiges CRUD-System für Menüpläne
- **Funktionen**:
  - Speichern mit Metadaten (Name, Beschreibung, Tags)
  - Laden gespeicherter Pläne
  - Duplizieren von Plänen für neue Perioden
  - Löschen nicht mehr benötigter Pläne
  - Liste aller Pläne mit Filterung
- **Speicherung**: JSON-basiert in `data/menu_plans/`
- **APIs**:
  - `GET /api/menu-plans` - Liste aller Pläne
  - `GET /api/menu-plans/<plan_id>` - Spezifischen Plan laden
  - `POST /api/menu-plans` - Plan speichern
  - `DELETE /api/menu-plans/<plan_id>` - Plan löschen
  - `POST /api/menu-plans/<plan_id>/duplicate` - Plan duplizieren

#### 4. Bestelllisten-Management
- **Feature**: Verwaltung von Bestelllisten mit Metadaten
- **Metadaten**:
  - Verknüpfung mit Menüplan
  - Zeitstempel
  - Lieferant und Bestelldatum
  - Notizen
- **Funktionen**:
  - Speichern generierter Bestelllisten
  - Laden historischer Bestellungen
  - Löschen alter Bestelllisten
- **APIs**:
  - `GET /api/order-lists` - Liste aller Bestelllisten
  - `GET /api/order-lists/<order_id>` - Spezifische Liste laden
  - `POST /api/order-lists` - Liste speichern
  - `DELETE /api/order-lists/<order_id>` - Liste löschen

#### 5. BKT-Statistik-Berechnung
- **Feature**: Detaillierte BKT-Analyse für Menüpläne
- **Metriken**:
  - Durchschnittlicher BKT über alle Tage
  - Minimaler und maximaler Tages-BKT
  - Gesamtkosten des Plans
  - Tägliche BKT-Werte
- **Logik**: 
  - Berücksichtigt nur Hauptmahlzeiten (Mittagessen, Abendessen)
  - Automatische Anpassung bei Portionsänderungen
  - Toleranz-Berechnung (bereits in SimulatorConfig vorhanden)
- **Methode**: `MenuPlanManager.calculate_bkt_statistics()`

### 🔧 Technische Verbesserungen

#### Backend-Architektur
- **Neue Datei**: `backend/menuplan_manager.py`
  - `MenuPlanMetadata` Klasse für Plan-Metadaten
  - `OrderListMetadata` Klasse für Bestelllisten-Metadaten
  - `MenuPlanManager` Klasse für zentrale Verwaltung

#### API-Erweiterungen
- **12 neue Endpunkte** für CRUD-Operationen
- **RESTful Design** mit konsistenten Antwortformaten
- **Error Handling** mit aussagekräftigen Fehlermeldungen
- **JSON-Serialisierung** mit `asdict()` für Dataclasses

#### Datenmodell-Erweiterungen
- **MealSlot**: Neues `portions` Feld
- **SimulatorConfig**: Erweitert um `recipe_options_count`
- **Kostenberechnung**: Automatisch basierend auf Portionen

### 📊 Datenbankschema

#### Neue Datenstrukturen

**MenuPlanMetadata**:
```json
{
  "id": "plan_20251025_120000",
  "name": "KW 42 - Herbstmenü",
  "status": "Aktiv",
  "created_at": "2025-10-25T12:00:00Z",
  "updated_at": "2025-10-25T14:30:00Z",
  "start_date": "2025-10-20",
  "end_date": "2025-10-26",
  "total_cost": 1250.50,
  "bkt_average": 3.50,
  "description": "Herbstliche Menüs mit regionalen Zutaten",
  "tags": ["Herbst", "Regional", "Saisonal"]
}
```

**OrderListMetadata**:
```json
{
  "id": "order_20251025_143000",
  "name": "Bestellung KW 42",
  "created_at": "2025-10-25T14:30:00Z",
  "menu_plan_id": "plan_20251025_120000",
  "menu_plan_name": "KW 42 - Herbstmenü",
  "total_items": 45,
  "total_cost": 1250.50,
  "order_date": "2025-10-27",
  "supplier": "Großhandel Schmidt",
  "notes": "Lieferung bis 8:00 Uhr"
}
```

### 🚀 Performance

- **JSON-Speicherung**: Optimiert für <100 Pläne
- **Lazy Loading**: Pläne werden nur bei Bedarf geladen
- **Caching**: Rezepte werden beim Start geladen (200 Rezepte)
- **Zeitstempel-IDs**: Automatische, eindeutige Identifikation

### 📝 Dokumentation

- **DEPLOYMENT_GUIDE_V5.md**: Vollständige Deployment-Anleitung
- **BACKEND_IMPROVEMENTS.md**: Technische Dokumentation der Backend-Änderungen
- **PLANNED_IMPROVEMENTS.md**: Roadmap für zukünftige Features
- **API-Dokumentation**: Inline-Dokumentation in `app.py`

### 🐛 Bugfixes

- **Kostenberechnung**: Korrektur bei Portionsänderungen
- **JSON-Serialisierung**: Kompatibilität mit Dataclasses
- **Error Handling**: Verbesserte Fehlerbehandlung in API-Endpunkten

### ⚠️ Breaking Changes

Keine Breaking Changes in dieser Version. Alle bestehenden Features bleiben kompatibel.

### 🔄 Migration von v1.0.x

Keine Migration erforderlich. v5.0 ist vollständig abwärtskompatibel.

Neue Features sind optional und können schrittweise aktiviert werden.

### 📋 Bekannte Einschränkungen

1. **Datenpersistenz auf Render.com**: 
   - Free Tier hat keinen persistenten Storage
   - Daten gehen bei Service-Neustart verloren
   - Lösung: PostgreSQL oder S3-Storage nutzen

2. **JSON-Speicherung**:
   - Optimiert für <100 Pläne
   - Bei >100 Plänen: Migration zu SQLite empfohlen

3. **Frontend-Integration**:
   - UI für neue Features noch nicht vollständig implementiert
   - API-Endpunkte sind bereit für Frontend-Integration

### 🎯 Nächste Schritte (v5.1)

#### Geplante Features:
1. **Rezept-Info-Button**: Modal mit vollständigen Rezeptdetails
2. **Kollektive Mengensteuerung**: Globale Portionsanpassung
3. **Header-Menü**: Dropdown für gespeicherte Pläne und Listen
4. **BKT-Anzeige**: Tages-BKT und Gesamt-BKT mit Farbcodierung
5. **Frontend-Integration**: UI für alle neuen Backend-Features

#### Technische Verbesserungen:
1. **Unit-Tests**: Vollständige Test-Coverage für neue Features
2. **API-Dokumentation**: Swagger/OpenAPI Integration
3. **Performance**: Caching und Lazy Loading optimieren
4. **Sicherheit**: Rate Limiting und Input-Validierung

### 👥 Contributors

- **Entwicklung**: Manus AI Agent
- **Konzept & Requirements**: User (jb-x-dev)
- **Testing**: Community

### 📞 Support

- **GitHub**: https://github.com/jb-x-dev/menuplan-simulator-v5
- **Issues**: https://github.com/jb-x-dev/menuplan-simulator-v5/issues
- **Dokumentation**: Siehe README.md und DEPLOYMENT_GUIDE_V5.md

---

## Version 1.0.2 (23.10.2025)

### Fixes
- ✅ BKT-Berechnung nur für Hauptmahlzeiten
- ✅ Simulationsparameter-Layout verbessert
- ✅ Button-Lesbarkeit verbessert

## Version 1.0.1 (23.10.2025)

### Fixes
- ✅ Kritischer Fehler bei "Automatisch generieren" behoben
- ✅ Statistik-Berechnung korrigiert

## Version 1.0.0 (Initial Release)

### Features
- ✅ Automatische Menüplan-Generierung
- ✅ Manuelle Menüplan-Erstellung
- ✅ BKT-Berechnung
- ✅ Bestelllisten-Generierung
- ✅ PDF & Excel Export
- ✅ 200 Rezepte Datenbank
- ✅ Allergene & Ernährungsformen
- ✅ Simulationsparameter

---

**Version 5.0.0 markiert einen bedeutenden Meilenstein mit umfassenden Backend-Verbesserungen und bereitet den Weg für erweiterte Frontend-Features in v5.1.**

