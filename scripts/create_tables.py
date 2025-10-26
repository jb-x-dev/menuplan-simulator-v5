#!/usr/bin/env python3
"""
Erstellt die notwendigen Datenbank-Tabellen für Menüpläne und Bestelllisten
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "recipe_selection.db"

def create_tables():
    """Erstellt alle notwendigen Tabellen"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔧 Erstelle Datenbank-Tabellen...\n")
    
    # Tabelle für Menüpläne
    print("📅 Erstelle Tabelle: menu_plans")
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
    
    # Tabelle für Bestelllisten
    print("📦 Erstelle Tabelle: order_lists")
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
    
    # Index für schnellere Suche
    print("🔍 Erstelle Indizes...")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_menu_plans_dates 
        ON menu_plans(start_date, end_date)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_menu_plans_status 
        ON menu_plans(status)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_order_lists_dates 
        ON order_lists(order_date, delivery_date)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_order_lists_status 
        ON order_lists(status)
    """)
    
    conn.commit()
    conn.close()
    
    print("\n✅ Tabellen erfolgreich erstellt!")
    
    # Zeige alle Tabellen
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print(f"\n📊 Vorhandene Tabellen: {', '.join(tables)}")

if __name__ == "__main__":
    create_tables()

