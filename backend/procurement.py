"""
Beschaffungsauflösung - Von Menüplan zu Bestellungen
"""
import math
from datetime import date, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Ingredient:
    id: int
    name: str
    quantity: float
    unit: str
    category: str  # ORDER, STOCK, NON_ORDER
    supplier_id: int
    lead_time: int
    price: float


@dataclass
class ShoppingCart:
    cart_id: str
    supplier_id: int
    supplier_name: str
    delivery_date: str
    order_date: str
    is_urgent: bool
    total_cost: float
    items: List[Dict]


class ProcurementResolver:
    """Löst Menüplan in Beschaffungsbedarfe auf"""
    
    def __init__(self, menu_plan: Dict, recipes: List):
        self.menu_plan = menu_plan
        self.recipes = {r.id: r for r in recipes}
        
    def resolve(self) -> Dict:
        """Hauptmethode zur Beschaffungsauflösung"""
        print("📦 Phase 1: Recipe explosion...")
        aggregated = self._aggregate_ingredients()
        
        print("📊 Phase 2: Categorization...")
        categorized = self._categorize_and_accumulate(aggregated)
        
        print("📅 Phase 3: Delivery date calculation...")
        with_dates = self._calculate_delivery_dates(categorized)
        
        print("📈 Phase 4: Quantity optimization...")
        optimized = self._optimize_quantities(with_dates)
        
        print("🛒 Phase 5: Shopping cart creation...")
        carts = self._create_shopping_carts(optimized)
        
        return {
            'shopping_carts': carts,
            'summary': self._create_summary(carts, optimized)
        }
    
    def _aggregate_ingredients(self) -> Dict:
        """Aggregiert alle Zutaten aus dem Menüplan"""
        aggregated = defaultdict(lambda: {
            'total_quantity': 0.0,
            'unit': None,
            'category': None,
            'supplier_id': None,
            'lead_time': 0,
            'price': 0.0,
            'positions': []
        })
        
        for day in self.menu_plan['days']:
            day_date = date.fromisoformat(day['date'])
            
            for menu_line in day['menu_lines']:
                for recipe_data in menu_line['recipes']:
                    recipe = self.recipes[recipe_data['recipe_id']]
                    
                    # Explode recipe (vereinfacht, keine Grundrezepte)
                    for ingredient in recipe.ingredients:
                        key = (day_date, ingredient['id'])
                        agg = aggregated[key]
                        
                        if agg['unit'] is None:
                            agg['unit'] = ingredient['unit']
                            agg['category'] = ingredient['category']
                            agg['supplier_id'] = ingredient['supplier_id']
                            agg['lead_time'] = ingredient['lead_time']
                            agg['price'] = ingredient['price']
                        
                        # Skalierung basierend auf calculation_basis
                        # Annahme: Rezept ist für 10 Personen, Plan ist für 50
                        scaling = 50 / recipe.calculation_basis
                        scaled_qty = ingredient['quantity'] * scaling
                        
                        agg['total_quantity'] += scaled_qty
                        agg['positions'].append({
                            'recipe': recipe.name,
                            'quantity': scaled_qty
                        })
        
        return aggregated
    
    def _categorize_and_accumulate(self, aggregated: Dict) -> Dict:
        """Kategorisiert nach Artikeltyp"""
        result = {
            'ORDER': {},    # Pro Tag
            'STOCK': {},    # Kumuliert
            'NON_ORDER': {} # Info
        }
        
        for (day_date, ingredient_id), data in aggregated.items():
            category = data['category']
            
            if category == 'ORDER':
                # Bestellartikel: Pro Tag separat
                key = (day_date, ingredient_id)
                result['ORDER'][key] = {
                    'date': day_date,
                    'ingredient_id': ingredient_id,
                    'quantity': data['total_quantity'],
                    'unit': data['unit'],
                    'supplier_id': data['supplier_id'],
                    'lead_time': data['lead_time'],
                    'price': data['price'],
                    'positions': data['positions']
                }
            
            elif category == 'STOCK':
                # Lagerartikel: Kumulieren
                key = ingredient_id
                
                if key not in result['STOCK']:
                    result['STOCK'][key] = {
                        'ingredient_id': ingredient_id,
                        'total_quantity': 0.0,
                        'unit': data['unit'],
                        'supplier_id': data['supplier_id'],
                        'lead_time': data['lead_time'],
                        'price': data['price'],
                        'usage_dates': [],
                        'positions': []
                    }
                
                result['STOCK'][key]['total_quantity'] += data['total_quantity']
                result['STOCK'][key]['usage_dates'].append(day_date)
                result['STOCK'][key]['positions'].extend(data['positions'])
            
            elif category == 'NON_ORDER':
                # Nicht-Bestellartikel: Nur Info
                key = ingredient_id
                
                if key not in result['NON_ORDER']:
                    result['NON_ORDER'][key] = {
                        'ingredient_id': ingredient_id,
                        'total_quantity': 0.0,
                        'unit': data['unit'],
                        'usage_dates': []
                    }
                
                result['NON_ORDER'][key]['total_quantity'] += data['total_quantity']
                result['NON_ORDER'][key]['usage_dates'].append(day_date)
        
        return result
    
    def _calculate_delivery_dates(self, categorized: Dict) -> Dict:
        """Berechnet Liefer- und Bestelldaten"""
        today = date.today()
        
        # Bestellartikel
        for key, item in categorized['ORDER'].items():
            need_date = item['date']
            
            # Vereinfacht: 1 Tag Bearbeitungszeit
            processing_days = 1
            delivery_date = need_date - timedelta(days=processing_days)
            order_date = delivery_date - timedelta(days=item['lead_time'])
            
            if order_date < today:
                item['is_urgent'] = True
                item['order_date'] = today
                item['delivery_date'] = today + timedelta(days=item['lead_time'])
            else:
                item['is_urgent'] = False
                item['order_date'] = order_date
                item['delivery_date'] = delivery_date
            
            item['need_date'] = need_date
        
        # Lagerartikel
        for key, item in categorized['STOCK'].items():
            first_use = min(item['usage_dates'])
            delivery_date = first_use - timedelta(days=7)
            order_date = delivery_date - timedelta(days=item['lead_time'])
            
            if order_date < today:
                item['is_urgent'] = True
                item['order_date'] = today
                item['delivery_date'] = today + timedelta(days=item['lead_time'])
            else:
                item['is_urgent'] = False
                item['order_date'] = order_date
                item['delivery_date'] = delivery_date
        
        return categorized
    
    def _optimize_quantities(self, categorized: Dict) -> Dict:
        """Optimiert Bestellmengen"""
        # Vereinfacht: Runde auf volle Einheiten
        for category in ['ORDER', 'STOCK']:
            for key, item in categorized[category].items():
                required = item['total_quantity'] if category == 'STOCK' else item['quantity']
                
                # Runde auf nächste 100g/ml auf
                if item['unit'] in ['g', 'ml']:
                    order_qty = math.ceil(required / 100) * 100
                elif item['unit'] == 'kg':
                    order_qty = math.ceil(required)
                elif item['unit'] == 'l':
                    order_qty = math.ceil(required)
                else:
                    order_qty = math.ceil(required)
                
                item['order_quantity'] = order_qty
                item['required_quantity'] = required
                item['surplus'] = order_qty - required
                item['total_cost'] = order_qty * item['price'] / 1000  # Preis ist pro kg/l
        
        return categorized
    
    def _create_shopping_carts(self, categorized: Dict) -> List[Dict]:
        """Erstellt Warenkörbe gruppiert nach Lieferant und Datum"""
        carts = defaultdict(lambda: {
            'supplier_id': None,
            'supplier_name': None,
            'delivery_date': None,
            'order_date': None,
            'items': [],
            'total_cost': 0.0,
            'is_urgent': False
        })
        
        # Bestellartikel
        for key, item in categorized['ORDER'].items():
            cart_key = (item['supplier_id'], item['delivery_date'])
            cart = carts[cart_key]
            
            if cart['supplier_id'] is None:
                cart['supplier_id'] = item['supplier_id']
                cart['supplier_name'] = f"Lieferant {item['supplier_id']}"
                cart['delivery_date'] = item['delivery_date'].isoformat()
                cart['order_date'] = item['order_date'].isoformat()
            
            cart['items'].append({
                'ingredient_id': item['ingredient_id'],
                'ingredient_name': self._get_ingredient_name(item['ingredient_id']),
                'order_quantity': item['order_quantity'],
                'unit': item['unit'],
                'need_date': item['need_date'].isoformat(),
                'required_quantity': item['required_quantity'],
                'surplus': item['surplus'],
                'price_per_unit': item['price'],
                'total_cost': item['total_cost']
            })
            
            cart['total_cost'] += item['total_cost']
            
            if item['is_urgent']:
                cart['is_urgent'] = True
        
        # Lagerartikel
        for key, item in categorized['STOCK'].items():
            cart_key = (item['supplier_id'], item['delivery_date'])
            cart = carts[cart_key]
            
            if cart['supplier_id'] is None:
                cart['supplier_id'] = item['supplier_id']
                cart['supplier_name'] = f"Lieferant {item['supplier_id']}"
                cart['delivery_date'] = item['delivery_date'].isoformat()
                cart['order_date'] = item['order_date'].isoformat()
            
            cart['items'].append({
                'ingredient_id': item['ingredient_id'],
                'ingredient_name': self._get_ingredient_name(item['ingredient_id']),
                'order_quantity': item['order_quantity'],
                'unit': item['unit'],
                'usage_dates': [d.isoformat() for d in item['usage_dates']],
                'required_quantity': item['total_quantity'],
                'surplus': item['surplus'],
                'price_per_unit': item['price'],
                'total_cost': item['total_cost'],
                'article_type': 'STOCK'
            })
            
            cart['total_cost'] += item['total_cost']
            
            if item['is_urgent']:
                cart['is_urgent'] = True
        
        # Konvertiere zu Liste
        result = []
        for (supplier_id, delivery_date), cart_data in carts.items():
            result.append({
                'cart_id': f"{supplier_id}_{delivery_date.isoformat() if isinstance(delivery_date, date) else delivery_date}",
                **cart_data
            })
        
        # Sortiere nach Bestelldatum
        result.sort(key=lambda x: x['order_date'])
        
        return result
    
    def _get_ingredient_name(self, ingredient_id: int) -> str:
        """Findet Zutatennamen"""
        for recipe in self.recipes.values():
            for ing in recipe.ingredients:
                if ing['id'] == ingredient_id:
                    return ing['name']
        return f"Zutat {ingredient_id}"
    
    def _create_summary(self, carts: List[Dict], categorized: Dict) -> Dict:
        """Erstellt Zusammenfassung"""
        total_cost = sum(cart['total_cost'] for cart in carts)
        urgent_carts = sum(1 for cart in carts if cart['is_urgent'])
        
        return {
            'total_shopping_carts': len(carts),
            'total_cost': round(total_cost, 2),
            'urgent_orders': urgent_carts,
            'order_articles': len(categorized['ORDER']),
            'stock_articles': len(categorized['STOCK']),
            'non_order_articles': len(categorized['NON_ORDER'])
        }


def resolve_procurement(menu_plan: Dict, recipes: List) -> Dict:
    """Wrapper-Funktion für Beschaffungsauflösung"""
    resolver = ProcurementResolver(menu_plan, recipes)
    return resolver.resolve()

