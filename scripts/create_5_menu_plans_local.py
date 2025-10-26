#!/usr/bin/env python3
"""
Erstellt 5 Menüpläne lokal für KW 43-47 (2025)
"""
import json
import sys
import os
from datetime import datetime, timedelta

# Füge Backend-Pfad hinzu
sys.path.insert(0, '/home/ubuntu/menuplan-simulator-v5/backend')

from simulator import MenuPlanSimulator, SimulatorConfig, Recipe

# Lade Rezepte
def load_recipes():
    recipes_path = '/home/ubuntu/menuplan-simulator-v5/data/recipes_300.json'
    with open(recipes_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Konvertiere zu Recipe-Objekten
    return [Recipe(**r) for r in data]

# Kalenderwoche zu Datum
def kw_to_date(year, week):
    jan_1 = datetime(year, 1, 1)
    days_to_monday = (7 - jan_1.weekday()) % 7
    if days_to_monday == 0 and jan_1.weekday() != 0:
        days_to_monday = 7
    first_monday = jan_1 + timedelta(days=days_to_monday)
    start_date = first_monday + timedelta(weeks=week-1)
    end_date = start_date + timedelta(days=6)
    return start_date, end_date

# Hauptprogramm
def main():
    print("🍽️  Menüplan-Generator (Lokal)")
    print("=" * 60)
    
    recipes = load_recipes()
    print(f"✅ {len(recipes)} Rezepte geladen")
    
    year = 2025
    created_plans = []
    
    for week in range(43, 48):
        print(f"\n📅 Generiere Menüplan für KW {week}/{year}...")
        
        start_date, end_date = kw_to_date(year, week)
        
        # Erstelle SimulatorConfig
        config = SimulatorConfig(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            menu_lines=[
                {
                    "name": "Frühstück",
                    "component": "Frühstück",
                    "cost_forms": [{"name": "Vollkost", "portions": 50}]
                },
                {
                    "name": "Mittagessen",
                    "component": "Mittagessen",
                    "cost_forms": [{"name": "Vollkost", "portions": 50}]
                },
                {
                    "name": "Abendessen",
                    "component": "Abendessen",
                    "cost_forms": [{"name": "Vollkost", "portions": 50}]
                }
            ],
            bkt_target=8.0,
            bkt_tolerance=0.15,
            dietary_forms=["Vollkost"],
            excluded_allergens=[],
            repetition_interval=7,
            consider_seasonality=True,
            kitchen_id=1,
            recipe_options_count=2,
            simulation_params={}
        )
        
        # Simuliere
        simulator = MenuPlanSimulator(config, recipes)
        plan = simulator.generate_plan()
        
        if plan:
            stats = plan.get('statistics', {})
            print(f"✅ Menüplan generiert:")
            print(f"   Zeitraum: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
            print(f"   Tage: {len(plan.get('days', []))}")
            print(f"   Gesamtkosten: {stats.get('total_cost', 0):.2f}€")
            print(f"   Durchschnittlicher BKT: {stats.get('avg_bkt', 0):.2f}€")
            
            # Erstelle Metadaten
            plan_id = f"plan_kw{week}_{int(datetime.now().timestamp())}"
            metadata = {
                "id": plan_id,
                "name": f"KW {week}",
                "status": "Aktiv",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "total_cost": stats.get('total_cost', 0),
                "bkt_average": stats.get('avg_bkt', 0),
                "description": f"Automatisch generierter Menüplan für KW {week}",
                "tags": ["auto-generated", f"kw-{week}"]
            }
            
            # Speichere
            plan_data = {
                "plan": plan,
                "metadata": metadata
            }
            
            filename = f"/home/ubuntu/menuplan-simulator-v5/data/menuplan_kw{week}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(plan_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Gespeichert: {filename}")
            
            created_plans.append({
                "id": plan_id,
                "name": f"KW {week}",
                "week": week,
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "file": filename
            })
    
    print("\n" + "=" * 60)
    print(f"✅ Erfolgreich {len(created_plans)} Menüpläne erstellt!")
    print("=" * 60)
    
    for plan in created_plans:
        print(f"  • {plan['name']}: {plan['start_date']} - {plan['end_date']}")
    
    # Speichere Übersicht
    with open('/home/ubuntu/menuplan-simulator-v5/data/created_plans.json', 'w') as f:
        json.dump(created_plans, f, indent=2)
    
    print(f"\n📄 Übersicht: data/created_plans.json")
    
    return len(created_plans)

if __name__ == "__main__":
    try:
        count = main()
        sys.exit(0 if count == 5 else 1)
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
