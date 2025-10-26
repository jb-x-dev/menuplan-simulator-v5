# Release Notes - Version 6.0.0 (STABLE)

**Release Date:** 2025-10-26  
**Status:** ✅ STABLE RELEASE  
**Git Tag:** `v6.0.0`  
**Commit:** `a3f65ca`

---

## 🎉 Highlights

### **52 Menüpläne für 2026**
- Alle Kalenderwochen (KW 01 - KW 52)
- 80 Portionen pro Mahlzeit
- Automatische Rezeptzuweisung aus 300 Rezepten
- **1.092 Mahlzeiten gesamt**
- **87.360 Portionen gesamt**

### **52 Bestelllisten**
- 1 Woche Vorlaufzeit
- Automatisch aus Menüplänen generiert
- Gruppierung nach Bestelltagen

### **Datenbank-basiertes System**
- SQLite-Tabellen: `menu_plans`, `order_lists`
- MenuPlanDBManager (zwingend DB-basiert)
- Automatische Initialisierung beim Start
- Persistente Datenspeicherung

---

## 🐛 Bug Fixes

### **procurement.html**
- **Problem:** `Cannot read properties of undefined (reading 'days')`
- **Ursache:** API lieferte flache Struktur, Code erwartete verschachtelte
- **Lösung:** Fallback hinzugefügt: `const plan = selectedPlan.plan || selectedPlan;`
- **Commit:** `8721e17`

### **Render.com Deployment**
- **Problem:** `Gunicorn: command not found`
- **Ursache:** Falsche Schreibweise in Start-Command
- **Lösung:** Korrektur auf `gunicorn` (Kleinbuchstabe) + PYTHONPATH
- **Commit:** `10ed45f`

---

## 🚀 Technical Improvements

### **Automatische Dateninitialisierung**
```python
# Prüft bei jedem Start auf 2026-Daten
cursor.execute("SELECT COUNT(*) FROM menu_plans WHERE name LIKE '%2026%'")
menu_plans_2026_count = cursor.fetchone()[0]

if menu_plans_2026_count < 52:
    # Importiere automatisch
    import_2026_data()
```

### **Manual Import API**
- `GET /api/admin/db-status` - Datenbank-Status prüfen
- `POST /api/admin/init-2026-data` - Manueller Import triggern

### **Verbesserte Fehlerbehandlung**
- Detaillierte Traceback-Ausgabe
- App startet trotz Init-Fehler
- Bessere Logging-Nachrichten

---

## 📊 Database Schema

### **menu_plans**
```sql
CREATE TABLE menu_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT DEFAULT 'Aktiv',
    portions INTEGER DEFAULT 80,
    days TEXT NOT NULL,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **order_lists**
```sql
CREATE TABLE order_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    menu_plan_name TEXT NOT NULL,
    order_date TEXT NOT NULL,
    delivery_date TEXT NOT NULL,
    lead_time_days INTEGER DEFAULT 7,
    status TEXT DEFAULT 'Entwurf',
    items TEXT NOT NULL,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔗 Live URLs

**Production:**
- **Frontend:** https://menuplan-simulator-v5.onrender.com/
- **API:** https://menuplan-simulator-v5.onrender.com/api/menu-plans
- **Admin Status:** https://menuplan-simulator-v5.onrender.com/api/admin/db-status

**GitHub:**
- **Repository:** https://github.com/jb-x-dev/menuplan-simulator-v5
- **Tag:** https://github.com/jb-x-dev/menuplan-simulator-v5/releases/tag/v6.0.0

---

## 📦 Git Commits

| Commit | Description |
|--------|-------------|
| `8721e17` | Fix procurement.html undefined error |
| `1c92a55` | Add database-based menu plan management |
| `f011a4e` | Add automatic database initialization |
| `f5f7f36` | Improve error handling |
| `47063f5` | Add manual import API |
| `535f6a4` | Force 2026 data import on every startup |
| `10ed45f` | Fix Render.com deployment (gunicorn) |
| `a3f65ca` | Release Version 6.0.0 - Stable Release |

---

## ✅ Verification

```bash
# API Test
curl https://menuplan-simulator-v5.onrender.com/api/menu-plans | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  print(f'Total: {len(data[\"plans\"])}'); \
  print(f'2026: {sum(1 for p in data[\"plans\"] if \"2026\" in p[\"name\"])}')"

# Expected Output:
# Total: 52
# 2026: 52
```

**Result:** ✅ PASSED

---

## 🎯 Next Steps

Diese stabile Version kann nun als Basis für weitere Entwicklungen verwendet werden:

1. **Migration zur neuen tRPC-Version** (menuplansimulator)
2. **V5-Features integrieren:**
   - Allergen-Informationen
   - Kostformen (1-4)
   - Menülinien (1-3)
   - Diätformen (Vegetarisch, Vegan, Vollkost)
   - BKT-Berechnungsfelder
3. **UI-Verbesserungen**
4. **Performance-Optimierungen**

---

## 📝 Notes

- Diese Version ist **produktionsbereit** und **stabil**
- Alle Features wurden getestet und verifiziert
- Datenbank-Schema ist finalisiert
- Deployment läuft automatisch auf Render.com
- GitHub Token wird für weitere Deployments benötigt

---

**Erstellt von:** Manus AI  
**Datum:** 2025-10-26  
**Version:** 6.0.0 (STABLE)

