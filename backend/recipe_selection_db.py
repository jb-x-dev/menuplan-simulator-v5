"""
Datenbank-Modul für Rezept-Auswahl
Speichert welche Rezepte für die automatische Generierung ausgewählt sind
"""
import sqlite3
import os
from typing import List, Set
from contextlib import contextmanager

# Datenbank-Pfad
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipe_selection.db')

@contextmanager
def get_db_connection():
    """Context Manager für Datenbankverbindung"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialisiert die Datenbank mit benötigten Tabellen"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tabelle für ausgewählte Rezepte
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selected_recipes (
                recipe_id INTEGER PRIMARY KEY,
                recipe_name TEXT,
                menu_component TEXT,
                selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Index für schnellere Abfragen
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_menu_component 
            ON selected_recipes(menu_component)
        ''')
        
        print(f"✅ Database initialized at {DB_PATH}")


def is_recipe_selected(recipe_id: int) -> bool:
    """Prüft ob ein Rezept ausgewählt ist"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT 1 FROM selected_recipes WHERE recipe_id = ?',
            (recipe_id,)
        )
        return cursor.fetchone() is not None


def get_selected_recipe_ids() -> Set[int]:
    """Gibt alle ausgewählten Rezept-IDs zurück"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT recipe_id FROM selected_recipes')
        return {row['recipe_id'] for row in cursor.fetchall()}


def get_selected_recipes_by_component(component: str) -> List[int]:
    """Gibt ausgewählte Rezept-IDs für eine bestimmte Komponente zurück"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT recipe_id FROM selected_recipes WHERE menu_component = ?',
            (component,)
        )
        return [row['recipe_id'] for row in cursor.fetchall()]


def select_recipe(recipe_id: int, recipe_name: str, menu_component: str):
    """Wählt ein Rezept aus"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO selected_recipes (recipe_id, recipe_name, menu_component)
            VALUES (?, ?, ?)
        ''', (recipe_id, recipe_name, menu_component))


def deselect_recipe(recipe_id: int):
    """Entfernt ein Rezept aus der Auswahl"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM selected_recipes WHERE recipe_id = ?', (recipe_id,))


def select_all_recipes(recipes: List[dict]):
    """Wählt alle Rezepte aus (für Migration/Reset)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for recipe in recipes:
            cursor.execute('''
                INSERT OR REPLACE INTO selected_recipes (recipe_id, recipe_name, menu_component)
                VALUES (?, ?, ?)
            ''', (recipe['id'], recipe['name'], recipe.get('menu_component', 'Unknown')))
    print(f"✅ Selected {len(recipes)} recipes")


def deselect_all_recipes():
    """Entfernt alle Rezepte aus der Auswahl"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM selected_recipes')
    print("✅ Deselected all recipes")


def get_selection_count() -> int:
    """Gibt die Anzahl ausgewählter Rezepte zurück"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM selected_recipes')
        return cursor.fetchone()['count']


def get_selection_stats() -> dict:
    """Gibt Statistiken über die Auswahl zurück"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                menu_component,
                COUNT(*) as count
            FROM selected_recipes
            GROUP BY menu_component
            ORDER BY menu_component
        ''')
        
        stats = {}
        for row in cursor.fetchall():
            stats[row['menu_component']] = row['count']
        
        return stats


# Initialisiere Datenbank beim Import
init_database()

