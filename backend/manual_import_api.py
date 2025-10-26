"""
Manueller Import-Endpoint für 2026-Daten
Kann aufgerufen werden um Daten zu importieren wenn Auto-Init fehlschlägt
"""

from flask import Blueprint, jsonify
import json
import sqlite3
from pathlib import Path

manual_import_bp = Blueprint('manual_import', __name__)

DB_PATH = Path(__file__).parent.parent / "data" / "recipe_selection.db"

@manual_import_bp.route('/api/admin/init-2026-data', methods=['POST'])
def init_2026_data():
    """Manueller Import der 2026-Daten"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        results = {
            'menu_plans': {'imported': 0, 'skipped': 0, 'errors': []},
            'order_lists': {'imported': 0, 'skipped': 0, 'errors': []}
        }
        
        # Import Menüpläne
        menu_plans_file = Path(__file__).parent.parent / "data" / "menu_plans_2026.json"
        if menu_plans_file.exists():
            with open(menu_plans_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                plans = data.get('plans', [])
            
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
                        results['menu_plans']['imported'] += 1
                    else:
                        results['menu_plans']['skipped'] += 1
                except Exception as e:
                    results['menu_plans']['errors'].append(f"{plan['name']}: {str(e)}")
        
        # Import Bestelllisten
        order_lists_file = Path(__file__).parent.parent / "data" / "order_lists_2026.json"
        if order_lists_file.exists():
            with open(order_lists_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                orders = data.get('orders', [])
            
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
                        results['order_lists']['imported'] += 1
                    else:
                        results['order_lists']['skipped'] += 1
                except Exception as e:
                    results['order_lists']['errors'].append(f"{order['name']}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        # Prüfe finale Anzahl
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM menu_plans")
        total_plans = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM order_lists")
        total_orders = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Import completed',
            'results': results,
            'totals': {
                'menu_plans': total_plans,
                'order_lists': total_orders
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@manual_import_bp.route('/api/admin/db-status', methods=['GET'])
def db_status():
    """Zeigt Datenbank-Status"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Zähle Einträge
        cursor.execute("SELECT COUNT(*) FROM menu_plans")
        menu_plans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM order_lists")
        order_lists_count = cursor.fetchone()[0]
        
        # Hole erste 5 Menüpläne
        cursor.execute("SELECT name, start_date, end_date FROM menu_plans ORDER BY start_date LIMIT 5")
        sample_plans = [{'name': row[0], 'start_date': row[1], 'end_date': row[2]} for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'database_path': str(DB_PATH),
            'database_exists': DB_PATH.exists(),
            'counts': {
                'menu_plans': menu_plans_count,
                'order_lists': order_lists_count
            },
            'sample_plans': sample_plans
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

