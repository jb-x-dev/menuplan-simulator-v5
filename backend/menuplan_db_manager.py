"""
Datenbank-basierter Menüplan-Manager
Verwendet SQLite statt JSON-Dateien
"""
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class MenuPlanMetadata:
    """Metadaten für einen gespeicherten Menüplan"""
    id: str
    name: str
    status: str
    created_at: str
    updated_at: str
    start_date: str
    end_date: str
    total_cost: float = 0.0
    bkt_average: float = 0.0
    description: str = ""
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class OrderListMetadata:
    """Metadaten für eine gespeicherte Bestellliste"""
    id: str
    name: str
    created_at: str
    menu_plan_id: str = ""
    menu_plan_name: str = ""
    start_date: str = ""
    end_date: str = ""
    total_items: int = 0
    total_cost: float = 0.0
    order_date: str = ""
    supplier: str = ""
    notes: str = ""


class MenuPlanDBManager:
    """Verwaltet Menüpläne und Bestelllisten in SQLite-Datenbank"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "recipe_selection.db"
        self.db_path = str(db_path)
    
    def _get_connection(self):
        """Erstellt Datenbankverbindung"""
        return sqlite3.connect(self.db_path)
    
    def save_menu_plan(self, plan: Dict, metadata: MenuPlanMetadata) -> str:
        """Speichert einen Menüplan"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Generiere ID falls nicht vorhanden
        if not metadata.id:
            metadata.id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Aktualisiere Zeitstempel
        metadata.updated_at = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO menu_plans (name, start_date, end_date, status, portions, days)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                metadata.name,
                metadata.start_date,
                metadata.end_date,
                metadata.status,
                plan.get('portions', 80),
                json.dumps(plan.get('days', []))
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            # Plan existiert bereits, update stattdessen
            cursor.execute("""
                UPDATE menu_plans 
                SET start_date = ?, end_date = ?, status = ?, portions = ?, days = ?, updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
            """, (
                metadata.start_date,
                metadata.end_date,
                metadata.status,
                plan.get('portions', 80),
                json.dumps(plan.get('days', [])),
                metadata.name
            ))
            conn.commit()
        
        conn.close()
        return metadata.id
    
    def load_menu_plan(self, plan_id: str) -> Optional[Dict]:
        """Lädt einen gespeicherten Menüplan"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Versuche als ID oder Name zu laden
        cursor.execute("""
            SELECT id, name, start_date, end_date, status, portions, days, created_at, updated_at
            FROM menu_plans 
            WHERE id = ? OR name = ?
        """, (plan_id, plan_id))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'metadata': {
                'id': str(row[0]),
                'name': row[1],
                'start_date': row[2],
                'end_date': row[3],
                'status': row[4],
                'created_at': row[7],
                'updated_at': row[8],
                'total_cost': 0.0,
                'bkt_average': 0.0
            },
            'plan': {
                'name': row[1],
                'start_date': row[2],
                'end_date': row[3],
                'status': row[4],
                'portions': row[5],
                'days': json.loads(row[6])
            }
        }
    
    def list_menu_plans(self, status: Optional[str] = None) -> List[MenuPlanMetadata]:
        """Listet alle gespeicherten Menüpläne auf"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT id, name, start_date, end_date, status, created_at, updated_at
                FROM menu_plans 
                WHERE status = ?
                ORDER BY created_at DESC
            """, (status,))
        else:
            cursor.execute("""
                SELECT id, name, start_date, end_date, status, created_at, updated_at
                FROM menu_plans 
                ORDER BY created_at DESC
            """)
        
        plans = []
        for row in cursor.fetchall():
            plans.append(MenuPlanMetadata(
                id=str(row[0]),
                name=row[1],
                start_date=row[2],
                end_date=row[3],
                status=row[4],
                created_at=row[5],
                updated_at=row[6],
                total_cost=0.0,
                bkt_average=0.0
            ))
        
        conn.close()
        return plans
    
    def update_menu_plan_status(self, plan_id: str, new_status: str) -> bool:
        """Ändert den Status eines Menüplans"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE menu_plans 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? OR name = ?
        """, (new_status, plan_id, plan_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_menu_plan(self, plan_id: str) -> bool:
        """Löscht einen Menüplan"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM menu_plans 
            WHERE id = ? OR name = ?
        """, (plan_id, plan_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def duplicate_menu_plan(self, plan_id: str, new_name: str) -> Optional[str]:
        """Dupliziert einen Menüplan"""
        plan_data = self.load_menu_plan(plan_id)
        
        if not plan_data:
            return None
        
        # Erstelle neue Metadaten
        new_metadata = MenuPlanMetadata(
            id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=new_name,
            start_date=plan_data['metadata']['start_date'],
            end_date=plan_data['metadata']['end_date'],
            status="Entwurf",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Speichere Duplikat
        return self.save_menu_plan(plan_data['plan'], new_metadata)
    
    def save_order_list(self, order_list: Dict, metadata: OrderListMetadata) -> str:
        """Speichert eine Bestellliste"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Generiere ID falls nicht vorhanden
        if not metadata.id:
            metadata.id = f"order_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            cursor.execute("""
                INSERT INTO order_lists (
                    name, menu_plan_name, order_date, delivery_date, 
                    lead_time_days, status, items
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                metadata.name,
                metadata.menu_plan_name,
                metadata.order_date,
                order_list.get('delivery_date', ''),
                order_list.get('lead_time_days', 7),
                'Entwurf',
                json.dumps(order_list.get('items', []))
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            # Bestellliste existiert bereits
            pass
        
        conn.close()
        return metadata.id
    
    def load_order_list(self, order_id: str) -> Optional[Dict]:
        """Lädt eine gespeicherte Bestellliste"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, menu_plan_name, order_date, delivery_date, 
                   lead_time_days, status, items, created_at
            FROM order_lists 
            WHERE id = ? OR name = ?
        """, (order_id, order_id))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'metadata': {
                'id': str(row[0]),
                'name': row[1],
                'menu_plan_name': row[2],
                'order_date': row[3],
                'created_at': row[8]
            },
            'order_list': {
                'name': row[1],
                'menu_plan_name': row[2],
                'order_date': row[3],
                'delivery_date': row[4],
                'lead_time_days': row[5],
                'status': row[6],
                'items': json.loads(row[7])
            }
        }
    
    def list_order_lists(self) -> List[OrderListMetadata]:
        """Listet alle gespeicherten Bestelllisten auf"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, menu_plan_name, order_date, delivery_date, created_at
            FROM order_lists 
            ORDER BY created_at DESC
        """)
        
        orders = []
        for row in cursor.fetchall():
            orders.append(OrderListMetadata(
                id=str(row[0]),
                name=row[1],
                menu_plan_name=row[2],
                order_date=row[3],
                start_date=row[4],
                created_at=row[5]
            ))
        
        conn.close()
        return orders
    
    def delete_order_list(self, order_id: str) -> bool:
        """Löscht eine Bestellliste"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM order_lists 
            WHERE id = ? OR name = ?
        """, (order_id, order_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success

