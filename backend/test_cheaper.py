import json
from simulator import Recipe, SimulatorConfig, MenuPlanSimulator

# Load recipes
with open('../data/recipes.json', 'r', encoding='utf-8') as f:
    recipes_data = json.load(f)
recipes = [Recipe(**r) for r in recipes_data]

# Create config
config = SimulatorConfig(
    start_date='2025-01-06',
    end_date='2025-01-08',
    menu_lines=[
        {
            'id': 1,
            'name': 'Mittagessen',
            'dietary_forms': ['Vollkost'],
            'cost_forms': [{
                'id': 1,
                'name': 'Hauptgericht',
                'component': 'Mittagessen',
                'target_count': 50
            }]
        }
    ],
    bkt_target=2.50,
    bkt_tolerance=0.15,
    dietary_forms=['Vollkost'],
    excluded_allergens=[]
)

# Run simulation
simulator = MenuPlanSimulator(config, recipes)
result = simulator.generate_plan()

print('Test: Günstigeres Rezept wird ausgewählt')
print('=' * 60)

for day in result['days']:
    meal = day['menu_lines'][0]['recipes'][0]
    if 'options' in meal and len(meal['options']) >= 2:
        opt1 = meal['options'][0]
        opt2 = meal['options'][1]
        selected_idx = meal['selected_index']
        selected = meal['options'][selected_idx]
        
        print(f"\nTag: {day['date']}")
        print(f"  Option 1: {opt1['recipe_name']} - {opt1['cost_per_serving']:.2f}€")
        print(f"  Option 2: {opt2['recipe_name']} - {opt2['cost_per_serving']:.2f}€")
        print(f"  Ausgewählt (Index {selected_idx}): {selected['recipe_name']} - {selected['cost_per_serving']:.2f}€")
        
        # Prüfe ob das günstigere ausgewählt ist
        cheaper_cost = min(opt1['cost_per_serving'], opt2['cost_per_serving'])
        if selected['cost_per_serving'] == cheaper_cost:
            print(f"  ✅ Günstigeres Rezept ist ausgewählt")
        else:
            print(f"  ❌ FEHLER: Teureres Rezept ist ausgewählt")
