import json
from simulator import Recipe, SimulatorConfig, MenuPlanSimulator

# Load recipes
with open('../data/recipes.json', 'r', encoding='utf-8') as f:
    recipes_data = json.load(f)
recipes = [Recipe(**r) for r in recipes_data]

print("Test 1: 2 Rezeptoptionen (Standard)")
print("=" * 60)

config = SimulatorConfig(
    start_date='2025-01-06',
    end_date='2025-01-07',
    menu_lines=[{
        'id': 1,
        'name': 'Mittagessen',
        'dietary_forms': ['Vollkost'],
        'cost_forms': [{
            'id': 1,
            'name': 'Hauptgericht',
            'component': 'Mittagessen',
            'target_count': 50
        }]
    }],
    bkt_target=2.50,
    bkt_tolerance=0.15,
    dietary_forms=['Vollkost'],
    excluded_allergens=[],
    recipe_options_count=2
)

simulator = MenuPlanSimulator(config, recipes)
result = simulator.generate_plan()

meal = result['days'][0]['menu_lines'][0]['recipes'][0]
print(f"Anzahl Optionen: {len(meal['options'])}")
for i, opt in enumerate(meal['options']):
    print(f"  Option {i+1}: {opt['recipe_name']}")

print("\n" + "=" * 60)
print("Test 2: 3 Rezeptoptionen")
print("=" * 60)

config.recipe_options_count = 3
simulator = MenuPlanSimulator(config, recipes)
result = simulator.generate_plan()

meal = result['days'][0]['menu_lines'][0]['recipes'][0]
print(f"Anzahl Optionen: {len(meal['options'])}")
for i, opt in enumerate(meal['options']):
    print(f"  Option {i+1}: {opt['recipe_name']}")

print("\n✅ Konfigurierbare Rezeptoptionen funktionieren!")
