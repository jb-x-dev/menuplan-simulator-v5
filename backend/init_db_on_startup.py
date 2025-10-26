#!/usr/bin/env python3
"""
Initialisiert die Datenbank beim Start
- Erstellt Tabellen falls nicht vorhanden
- Importiert 2026-Daten falls Tabellen leer sind
"""

import json
import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "recipe_selection.db"

def create_tables_if_not_exist():
    """Erstellt Tabellen falls sie nicht existieren"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔧 Checking database tables...")
    
    # Prüfe ob Tabellen existieren
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='menu_plans'")
    menu_plans_exists = cursor.fetchone() is not None
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='order_lists'")
    order_lists_exists = cursor.fetchone() is not None
    
    if menu_plans_exists and order_lists_exists:
        print("✅ Database tables already exist")
        conn.close()
        return True
    
    print("📅 Creating table: menu_plans")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT DEFAULT 'Aktiv',
            portions INTEGER DEFAULT 80,
            days TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    print("📦 Creating table: order_lists")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            menu_plan_name TEXT NOT NULL,
            order_date TEXT NOT NULL,
            delivery_date TEXT NOT NULL,
            lead_time_days INTEGER DEFAULT 7,
            status TEXT DEFAULT 'Entwurf',
            items TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    print("🔍 Creating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_menu_plans_dates ON menu_plans(start_date, end_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_menu_plans_status ON menu_plans(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_lists_dates ON order_lists(order_date, delivery_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_lists_status ON order_lists(status)")
    
    conn.commit()
    conn.close()
    
    print("✅ Tables created successfully")
    return False  # Tabellen wurden gerade erstellt

def import_2026_data_if_empty():
    """Importiert 2026-Daten falls Tabellen leer sind"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Prüfe ob Daten bereits vorhanden
    cursor.execute("SELECT COUNT(*) FROM menu_plans")
    menu_plans_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM order_lists")
    order_lists_count = cursor.fetchone()[0]
    
    if menu_plans_count > 0 and order_lists_count > 0:
        print(f"✅ Data already imported: {menu_plans_count} menu plans, {order_lists_count} order lists")
        conn.close()
        return
    
    print("📚 Importing 2026 data...")
    
    # Lade Menüpläne
    menu_plans_file = Path(__file__).parent.parent / "data" / "menu_plans_2026.json"
    if menu_plans_file.exists():
        with open(menu_plans_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            plans = data.get('plans', [])
        
        print(f"📅 Importing {len(plans)} menu plans...")
        imported = 0
        
        for plan in plans:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO menu_plans (name, start_date, end_date, status, portions, days)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    plan['name'],
                    plan['start_date'],
                    plan['end_date'],
                    plan['status'],
                    plan['portions'],
                    json.dumps(plan['days'])
                ))
                if cursor.rowcount > 0:
                    imported += 1
            except Exception as e:
                print(f"⚠️ Error importing {plan['name']}: {e}")
        
        print(f"✅ Imported {imported} menu plans")
    
    # Lade Bestelllisten
    order_lists_file = Path(__file__).parent.parent / "data" / "order_lists_2026.json"
    if order_lists_file.exists():
        with open(order_lists_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            orders = data.get('orders', [])
        
        print(f"📦 Importing {len(orders)} order lists...")
        imported = 0
        
        for order in orders:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO order_lists (
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
                if cursor.rowcount > 0:
                    imported += 1
            except Exception as e:
                print(f"⚠️ Error importing {order['name']}: {e}")
        
        print(f"✅ Imported {imported} order lists")
    
    conn.commit()
    conn.close()

def init_database():
    """Hauptfunktion für Datenbank-Initialisierung"""
    print("\n" + "="*60)
    print("🚀 Database Initialization")
    print("="*60 + "\n")
    
    try:
        # Erstelle Tabellen
        tables_existed = create_tables_if_not_exist()
        
        # Importiere Daten falls Tabellen neu erstellt oder leer
        import_2026_data_if_empty()
        
        print("\n" + "="*60)
        print("✅ Database initialization complete")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}\n")
        raise

if __name__ == "__main__":
    init_database()

