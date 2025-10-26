#!/usr/bin/env python3
"""
Importiert die 52 Menüpläne und Bestelllisten für 2026 in die Datenbank
"""

import json
import sys
import sqlite3
from pathlib import Path

# Direkter Zugriff auf Datenbank
DB_PATH = Path(__file__).parent.parent / "data" / "recipe_selection.db"

def get_db_connection():
    """Erstellt Datenbankverbindung"""
    return sqlite3.connect(DB_PATH)

def import_menu_plans():
    """Importiert Menüpläne in die Datenbank"""
    data_file = Path(__file__).parent.parent / "data" / "menu_plans_2026.json"
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        plans = data.get('plans', [])
    
    print(f"📚 Importiere {len(plans)} Menüpläne...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for plan in plans:
        try:
            # Prüfe ob Plan bereits existiert
            cursor.execute(
                "SELECT id FROM menu_plans WHERE name = ?",
                (plan['name'],)
            )
            existing = cursor.fetchone()
            
            if existing:
                print(f"⏭️  {plan['name']} existiert bereits")
                skipped += 1
                continue
            
            # Füge Menüplan ein
            cursor.execute("""
                INSERT INTO menu_plans (name, start_date, end_date, status, portions, days)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                plan['name'],
                plan['start_date'],
                plan['end_date'],
                plan['status'],
                plan['portions'],
                json.dumps(plan['days'])
            ))
            
            imported += 1
            print(f"✅ {plan['name']}")
            
        except Exception as e:
            print(f"❌ Fehler bei {plan['name']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Menüpläne: {imported} importiert, {skipped} übersprungen")
    return imported

def import_order_lists():
    """Importiert Bestelllisten in die Datenbank"""
    data_file = Path(__file__).parent.parent / "data" / "order_lists_2026.json"
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        orders = data.get('orders', [])
    
    print(f"\n📦 Importiere {len(orders)} Bestelllisten...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for order in orders:
        try:
            # Prüfe ob Bestellliste bereits existiert
            cursor.execute(
                "SELECT id FROM order_lists WHERE name = ?",
                (order['name'],)
            )
            existing = cursor.fetchone()
            
            if existing:
                print(f"⏭️  {order['name']} existiert bereits")
                skipped += 1
                continue
            
            # Füge Bestellliste ein
            cursor.execute("""
                INSERT INTO order_lists (
                    name, menu_plan_name, order_date, delivery_date, 
                    lead_time_days, status, items
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order['name'],
                order['menu_plan_name'],
                order['order_date'],
                order['delivery_date'],
                order['lead_time_days'],
                order['status'],
                json.dumps(order['items'])
            ))
            
            imported += 1
            print(f"✅ {order['name']}")
            
        except Exception as e:
            print(f"❌ Fehler bei {order['name']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Bestelllisten: {imported} importiert, {skipped} übersprungen")
    return imported

def main():
    print("🚀 Starte Import der 2026-Daten...\n")
    
    # Importiere Menüpläne
    menu_plans_imported = import_menu_plans()
    
    # Importiere Bestelllisten
    order_lists_imported = import_order_lists()
    
    print(f"\n🎉 Import abgeschlossen!")
    print(f"   Menüpläne: {menu_plans_imported}")
    print(f"   Bestelllisten: {order_lists_imported}")

if __name__ == "__main__":
    main()

