#!/usr/bin/env python3
"""
Erstellt 52 Menüpläne für alle Kalenderwochen 2026
mit automatischer Rezeptzuweisung und Bestellvorschlägen
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Konfiguration
YEAR = 2026
PORTIONS_PER_MEAL = 80
MEAL_TYPES = ["Frühstück", "Mittagessen", "Abendessen"]
ORDER_LEAD_TIME_DAYS = 7  # 1 Woche Vorlauf

def get_week_dates(year, week):
    """Gibt Start- und Enddatum einer Kalenderwoche zurück"""
    # Erster Tag des Jahres
    jan_1 = datetime(year, 1, 1)
    # Finde den ersten Montag
    days_to_monday = (7 - jan_1.weekday()) % 7
    if days_to_monday == 0 and jan_1.weekday() != 0:
        days_to_monday = 7
    first_monday = jan_1 + timedelta(days=days_to_monday)
    
    # Berechne Start der gewünschten Woche
    week_start = first_monday + timedelta(weeks=week-1)
    week_end = week_start + timedelta(days=6)
    
    return week_start, week_end

def load_recipes():
    """Lädt die 300 Rezepte"""
    recipes_file = Path(__file__).parent.parent / "data" / "recipes_300.json"
    with open(recipes_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # recipes_300.json ist bereits eine Liste
        if isinstance(data, list):
            return data
        return data.get('recipes', [])

def create_menu_plan(week_number, recipes):
    """Erstellt einen Menüplan für eine Kalenderwoche"""
    week_start, week_end = get_week_dates(YEAR, week_number)
    
    menu_plan = {
        "name": f"KW {week_number:02d} - {YEAR}",
        "start_date": week_start.strftime("%Y-%m-%d"),
        "end_date": week_end.strftime("%Y-%m-%d"),
        "status": "Aktiv",
        "portions": PORTIONS_PER_MEAL,
        "days": []
    }
    
    # Erstelle 7 Tage (Montag bis Sonntag)
    for day_offset in range(7):
        day_date = week_start + timedelta(days=day_offset)
        day_name = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"][day_offset]
        
        day_data = {
            "date": day_date.strftime("%Y-%m-%d"),
            "day_name": day_name,
            "meals": []
        }
        
        # Erstelle 3 Mahlzeiten pro Tag
        for meal_type in MEAL_TYPES:
            # Wähle zufälliges Rezept
            recipe = random.choice(recipes)
            
            meal = {
                "meal_type": meal_type,
                "recipe_id": recipe.get("id", 0),
                "recipe_name": recipe.get("name", "Unbekannt"),
                "portions": PORTIONS_PER_MEAL,
                "notes": f"Automatisch generiert für {day_name}"
            }
            
            day_data["meals"].append(meal)
        
        menu_plan["days"].append(day_data)
    
    return menu_plan

def create_order_list(menu_plan, recipes):
    """Erstellt Bestellvorschlag mit 1 Woche Vorlauf"""
    week_start = datetime.strptime(menu_plan["start_date"], "%Y-%m-%d")
    order_date = week_start - timedelta(days=ORDER_LEAD_TIME_DAYS)
    
    # Aggregiere alle Zutaten
    ingredients_dict = {}
    
    for day in menu_plan["days"]:
        for meal in day["meals"]:
            recipe_id = meal["recipe_id"]
            portions = meal["portions"]
            
            # Finde Rezept
            recipe = next((r for r in recipes if r.get("id") == recipe_id), None)
            if not recipe:
                continue
            
            # Skaliere Zutaten
            recipe_portions = recipe.get("default_portions", 4)
            scale_factor = portions / recipe_portions
            
            for ingredient in recipe.get("ingredients", []):
                name = ingredient.get("name", "Unbekannt")
                amount = ingredient.get("amount", 0) * scale_factor
                unit = ingredient.get("unit", "")
                
                key = f"{name}_{unit}"
                if key in ingredients_dict:
                    ingredients_dict[key]["amount"] += amount
                else:
                    ingredients_dict[key] = {
                        "name": name,
                        "amount": amount,
                        "unit": unit,
                        "category": ingredient.get("category", "Sonstiges")
                    }
    
    # Erstelle Bestellliste
    order_list = {
        "name": f"Bestellung {menu_plan['name']}",
        "menu_plan_name": menu_plan["name"],
        "order_date": order_date.strftime("%Y-%m-%d"),
        "delivery_date": week_start.strftime("%Y-%m-%d"),
        "lead_time_days": ORDER_LEAD_TIME_DAYS,
        "status": "Entwurf",
        "items": list(ingredients_dict.values())
    }
    
    return order_list

def main():
    print(f"🚀 Erstelle 52 Menüpläne für {YEAR}...")
    
    # Lade Rezepte
    print("📚 Lade 300 Rezepte...")
    recipes = load_recipes()
    print(f"✅ {len(recipes)} Rezepte geladen")
    
    # Erstelle Menüpläne
    menu_plans = []
    order_lists = []
    
    for week in range(1, 53):
        print(f"📅 Erstelle KW {week:02d}...", end=" ")
        
        # Erstelle Menüplan
        menu_plan = create_menu_plan(week, recipes)
        menu_plans.append(menu_plan)
        
        # Erstelle Bestellvorschlag
        order_list = create_order_list(menu_plan, recipes)
        order_lists.append(order_list)
        
        print("✅")
    
    # Speichere Daten
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    menu_plans_file = output_dir / f"menu_plans_{YEAR}.json"
    with open(menu_plans_file, 'w', encoding='utf-8') as f:
        json.dump({"plans": menu_plans}, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Menüpläne gespeichert: {menu_plans_file}")
    
    order_lists_file = output_dir / f"order_lists_{YEAR}.json"
    with open(order_lists_file, 'w', encoding='utf-8') as f:
        json.dump({"orders": order_lists}, f, ensure_ascii=False, indent=2)
    print(f"✅ Bestelllisten gespeichert: {order_lists_file}")
    
    # Statistik
    total_meals = sum(len(plan["days"]) * len(MEAL_TYPES) for plan in menu_plans)
    total_portions = total_meals * PORTIONS_PER_MEAL
    
    print(f"\n📊 Statistik:")
    print(f"   Menüpläne: {len(menu_plans)}")
    print(f"   Tage: {sum(len(plan['days']) for plan in menu_plans)}")
    print(f"   Mahlzeiten: {total_meals}")
    print(f"   Portionen gesamt: {total_portions:,}")
    print(f"   Bestelllisten: {len(order_lists)}")
    print(f"\n🎉 Fertig!")

if __name__ == "__main__":
    main()

