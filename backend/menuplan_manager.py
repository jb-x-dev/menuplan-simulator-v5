"""
Menüplan-Management - Erweiterte Funktionen für Menüplan-Verwaltung
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class MenuPlanMetadata:
    """Metadaten für einen gespeicherten Menüplan"""
    id: str
    name: str
    status: str  # 'Entwurf', 'Vorlage', 'Aktiv', 'Archiviert'
    created_at: str
    updated_at: str
    start_date: str
    end_date: str
    total_cost: float
    bkt_average: float
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
    menu_plan_id: str
    menu_plan_name: str
    total_items: int
    total_cost: float
    order_date: str = ""
    supplier: str = ""
    notes: str = ""


class MenuPlanManager:
    """Verwaltet Menüpläne und Bestelllisten"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.plans_dir = os.path.join(data_dir, "menu_plans")
        self.orders_dir = os.path.join(data_dir, "order_lists")
        
        # Erstelle Verzeichnisse falls nicht vorhanden
        os.makedirs(self.plans_dir, exist_ok=True)
        os.makedirs(self.orders_dir, exist_ok=True)
    
    def save_menu_plan(self, plan: Dict, metadata: MenuPlanMetadata) -> str:
        """Speichert einen Menüplan mit Metadaten"""
        # Generiere ID falls nicht vorhanden
        if not metadata.id:
            metadata.id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Aktualisiere Zeitstempel
        metadata.updated_at = datetime.now().isoformat()
        
        # Speichere Plan
        plan_file = os.path.join(self.plans_dir, f"{metadata.id}.json")
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': asdict(metadata),
                'plan': plan
            }, f, indent=2, ensure_ascii=False)
        
        return metadata.id
    
    def load_menu_plan(self, plan_id: str) -> Optional[Dict]:
        """Lädt einen gespeicherten Menüplan"""
        plan_file = os.path.join(self.plans_dir, f"{plan_id}.json")
        
        if not os.path.exists(plan_file):
            return None
        
        with open(plan_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_menu_plans(self, status: Optional[str] = None) -> List[MenuPlanMetadata]:
        """Listet alle gespeicherten Menüpläne auf"""
        plans = []
        
        for filename in os.listdir(self.plans_dir):
            if not filename.endswith('.json'):
                continue
            
            plan_file = os.path.join(self.plans_dir, filename)
            with open(plan_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                metadata = MenuPlanMetadata(**data['metadata'])
                
                # Filter nach Status
                if status is None or metadata.status == status:
                    plans.append(metadata)
        
        # Sortiere nach Erstellungsdatum (neueste zuerst)
        plans.sort(key=lambda x: x.created_at, reverse=True)
        return plans
    
    def update_menu_plan_status(self, plan_id: str, new_status: str) -> bool:
        """Ändert den Status eines Menüplans"""
        plan_data = self.load_menu_plan(plan_id)
        
        if not plan_data:
            return False
        
        # Aktualisiere Status
        plan_data['metadata']['status'] = new_status
        plan_data['metadata']['updated_at'] = datetime.now().isoformat()
        
        # Speichere zurück
        plan_file = os.path.join(self.plans_dir, f"{plan_id}.json")
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def delete_menu_plan(self, plan_id: str) -> bool:
        """Löscht einen Menüplan"""
        plan_file = os.path.join(self.plans_dir, f"{plan_id}.json")
        
        if not os.path.exists(plan_file):
            return False
        
        os.remove(plan_file)
        return True
    
    def duplicate_menu_plan(self, plan_id: str, new_name: str) -> Optional[str]:
        """Dupliziert einen Menüplan"""
        plan_data = self.load_menu_plan(plan_id)
        
        if not plan_data:
            return None
        
        # Erstelle neue Metadaten
        new_metadata = MenuPlanMetadata(**plan_data['metadata'])
        new_metadata.id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_metadata.name = new_name
        new_metadata.status = "Entwurf"
        new_metadata.created_at = datetime.now().isoformat()
        new_metadata.updated_at = datetime.now().isoformat()
        
        # Speichere Duplikat
        return self.save_menu_plan(plan_data['plan'], new_metadata)
    
    def save_order_list(self, order_list: Dict, metadata: OrderListMetadata) -> str:
        """Speichert eine Bestellliste"""
        # Generiere ID falls nicht vorhanden
        if not metadata.id:
            metadata.id = f"order_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Speichere Bestellliste
        order_file = os.path.join(self.orders_dir, f"{metadata.id}.json")
        with open(order_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': asdict(metadata),
                'order_list': order_list
            }, f, indent=2, ensure_ascii=False)
        
        return metadata.id
    
    def load_order_list(self, order_id: str) -> Optional[Dict]:
        """Lädt eine gespeicherte Bestellliste"""
        order_file = os.path.join(self.orders_dir, f"{order_id}.json")
        
        if not os.path.exists(order_file):
            return None
        
        with open(order_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_order_lists(self) -> List[OrderListMetadata]:
        """Listet alle gespeicherten Bestelllisten auf"""
        orders = []
        
        for filename in os.listdir(self.orders_dir):
            if not filename.endswith('.json'):
                continue
            
            order_file = os.path.join(self.orders_dir, filename)
            with open(order_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                metadata = OrderListMetadata(**data['metadata'])
                orders.append(metadata)
        
        # Sortiere nach Erstellungsdatum (neueste zuerst)
        orders.sort(key=lambda x: x.created_at, reverse=True)
        return orders
    
    def delete_order_list(self, order_id: str) -> bool:
        """Löscht eine Bestellliste"""
        order_file = os.path.join(self.orders_dir, f"{order_id}.json")
        
        if not os.path.exists(order_file):
            return False
        
        os.remove(order_file)
        return True
    
    def calculate_bkt_statistics(self, plan: Dict) -> Dict:
        """Berechnet BKT-Statistiken für einen Menüplan"""
        days = plan.get('days', [])
        
        if not days:
            return {
                'average_bkt': 0.0,
                'min_bkt': 0.0,
                'max_bkt': 0.0,
                'total_cost': 0.0,
                'days_count': 0
            }
        
        daily_costs = []
        daily_main_portions = []
        
        for day in days:
            day_cost = 0.0
            main_portions = 0
            
            for meal_name, meal_slot in day.get('meals', {}).items():
                # Hole Kosten aus MealSlot
                cost = meal_slot.get('cost', 0.0)
                day_cost += cost
                
                # Zähle Portionen nur für Hauptmahlzeiten
                if meal_name in ['Mittagessen', 'Abendessen']:
                    portions = meal_slot.get('portions', 1)
                    main_portions += portions
            
            daily_costs.append(day_cost)
            daily_main_portions.append(main_portions if main_portions > 0 else 1)
        
        # Berechne BKT pro Tag
        daily_bkts = [cost / portions for cost, portions in zip(daily_costs, daily_main_portions)]
        
        return {
            'average_bkt': sum(daily_bkts) / len(daily_bkts) if daily_bkts else 0.0,
            'min_bkt': min(daily_bkts) if daily_bkts else 0.0,
            'max_bkt': max(daily_bkts) if daily_bkts else 0.0,
            'total_cost': sum(daily_costs),
            'days_count': len(days),
            'daily_bkts': daily_bkts
        }

