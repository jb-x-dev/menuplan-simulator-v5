# Erstellte Menüpläne und Bestelllisten

## Übersicht

**5 Menüpläne** und **5 Bestelllisten** für KW 43-47 (2025) wurden erfolgreich erstellt.

### Menüpläne

| KW | Zeitraum | Tage | Mahlzeiten | Portionen | Gesamtkosten | Durchschn. BKT | Datei |
|----|----------|------|------------|-----------|--------------|----------------|-------|
| 43 | 27.10-02.11.2025 | 7 | 21 | 1050 | 380.00€ | 54.29€ | `data/menuplan_kw43.json` |
| 44 | 03.11-09.11.2025 | 7 | 21 | 1050 | 342.50€ | 48.93€ | `data/menuplan_kw44.json` |
| 45 | 10.11-16.11.2025 | 7 | 21 | 1050 | 414.00€ | 59.14€ | `data/menuplan_kw45.json` |
| 46 | 17.11-23.11.2025 | 7 | 21 | 1050 | 344.50€ | 49.21€ | `data/menuplan_kw46.json` |
| 47 | 24.11-30.11.2025 | 7 | 21 | 1050 | 324.50€ | 46.36€ | `data/menuplan_kw47.json` |

**Gesamt:** 35 Tage, 105 Mahlzeiten, 5250 Portionen, **1805.50€**

### Bestelllisten

| KW | Rezepte | Portionen | Gesamtkosten | Datei |
|----|---------|-----------|--------------|-------|
| 43 | 21 | 1050 | 380.00€ | `data/orderlist_kw43.json` |
| 44 | 20 | 1050 | 342.50€ | `data/orderlist_kw44.json` |
| 45 | 20 | 1050 | 414.00€ | `data/orderlist_kw45.json` |
| 46 | 20 | 1050 | 344.50€ | `data/orderlist_kw46.json` |
| 47 | 18 | 1050 | 324.50€ | `data/orderlist_kw47.json` |

**Gesamt:** 99 eindeutige Rezepte, 5250 Portionen, **1805.50€**

## Struktur der Menüpläne

Jeder Menüplan enthält:
- **Metadaten:** ID, Name, Status, Zeitraum, Kosten, BKT
- **Tage:** 7 Tage mit Datum und Wochentag
- **Mahlzeiten pro Tag:**
  - Frühstück (50 Portionen)
  - Mittagessen (50 Portionen)
  - Abendessen (50 Portionen)
- **Statistiken:** Gesamtkosten, durchschnittlicher BKT, Anzahl Tage/Mahlzeiten

## Struktur der Bestelllisten

Jede Bestellliste enthält:
- **Metadaten:** ID, Name, Erstellungsdatum, Referenz zum Menüplan
- **Items:** Aggregierte Rezepte mit:
  - Rezept-ID und Name
  - Komponente (Frühstück/Mittagessen/Abendessen)
  - Anzahl Verwendungen
  - Gesamtportionen
  - Gesamtkosten
  - Allergene und Ernährungsformen
- **Statistiken:** Anzahl Rezepte, Gesamtportionen, Gesamtkosten

## Verwendung

### Menüpläne laden
```javascript
// Im Frontend
fetch('/data/menuplan_kw43.json')
  .then(res => res.json())
  .then(data => {
    console.log(data.metadata);
    console.log(data.plan);
  });
```

### Bestelllisten laden
```javascript
// Im Frontend
fetch('/data/orderlist_kw43.json')
  .then(res => res.json())
  .then(data => {
    console.log(data.items);
    console.log(data.statistics);
  });
```

## Generierungs-Scripts

- **`create_menu_plans_standalone.py`:** Erstellt 5 Menüpläne
- **`create_order_lists.py`:** Erstellt 5 Bestelllisten aus Menüplänen

## Übersichtsdateien

- **`data/created_plans.json`:** Liste aller erstellten Menüpläne
- **`data/created_order_lists.json`:** Liste aller erstellten Bestelllisten
