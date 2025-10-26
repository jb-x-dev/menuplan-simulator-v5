#!/usr/bin/env python3
"""
Führt bestehende und neue Rezepte zusammen und verbessert sie
"""
import json

# Lade bestehende Rezepte
with open('/home/ubuntu/menuplan-simulator-v5/data/recipes_200.json', 'r', encoding='utf-8') as f:
    existing_recipes = json.load(f)

# Lade neue Rezepte
with open('/home/ubuntu/menuplan-simulator-v5/data/new_recipes_100.json', 'r', encoding='utf-8') as f:
    new_recipes = json.load(f)

print(f"📚 Geladen: {len(existing_recipes)} bestehende + {len(new_recipes)} neue Rezepte")

# Verbessere bestehende Rezepte
improved_count = 0
for recipe in existing_recipes:
    changed = False
    
    # Stelle sicher, dass alle Felder vorhanden sind
    if 'allergens' not in recipe:
        recipe['allergens'] = []
        changed = True
    
    if 'additives' not in recipe:
        recipe['additives'] = []
        changed = True
    
    if 'dietary_forms' not in recipe:
        recipe['dietary_forms'] = ["Vollkost"]
        changed = True
    
    if 'nutritional_values' not in recipe:
        recipe['nutritional_values'] = {
            "calories": 0,
            "fat": 0,
            "carbs": 0,
            "protein": 0
        }
        changed = True
    
    if 'processing_time' not in recipe:
        recipe['processing_time'] = 1.0
        changed = True
    
    if 'portion_size' not in recipe:
        if recipe['menu_component'] == 'Frühstück':
            recipe['portion_size'] = '250g'
        elif recipe['menu_component'] == 'Mittagessen':
            recipe['portion_size'] = '350g'
        elif recipe['menu_component'] == 'Abendessen':
            recipe['portion_size'] = '200g'
        else:
            recipe['portion_size'] = '150g'
        changed = True
    
    if 'ingredients' not in recipe:
        recipe['ingredients'] = []
        changed = True
    
    # Korrigiere "Zwischengang" zu "Zwischenmahlzeit"
    if recipe.get('menu_component') == 'Zwischengang':
        recipe['menu_component'] = 'Zwischenmahlzeit'
        changed = True
    
    if recipe.get('category') == 'Zwischengang':
        recipe['category'] = 'Zwischenmahlzeit'
        changed = True
    
    if changed:
        improved_count += 1

print(f"✨ {improved_count} bestehende Rezepte verbessert")

# Zusammenführen
all_recipes = existing_recipes + new_recipes

# Sortiere nach ID
all_recipes.sort(key=lambda r: r['id'])

# Speichere als recipes_300.json
with open('/home/ubuntu/menuplan-simulator-v5/data/recipes_300.json', 'w', encoding='utf-8') as f:
    json.dump(all_recipes, f, ensure_ascii=False, indent=2)

print(f"\n✅ Gespeichert: {len(all_recipes)} Rezepte in recipes_300.json")

# Statistiken
from collections import Counter

print("\n📊 Finale Statistiken:")
print(f"\nVerteilung nach Kategorie:")
counts = Counter(r['menu_component'] for r in all_recipes)
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}")

print(f"\nPreis-Statistiken:")
costs = [r['cost'] for r in all_recipes]
print(f"  Min: {min(costs):.2f}€")
print(f"  Max: {max(costs):.2f}€")
print(f"  Durchschnitt: {sum(costs)/len(costs):.2f}€")

print(f"\nErnährungsformen:")
dietary_counts = Counter()
for r in all_recipes:
    for d in r.get('dietary_forms', []):
        dietary_counts[d] += 1
for k, v in sorted(dietary_counts.items()):
    print(f"  {k}: {v}")

print(f"\nVegetarisch/Vegan:")
veg_count = len([r for r in all_recipes if 'Vegetarisch' in r.get('dietary_forms', [])])
vegan_count = len([r for r in all_recipes if 'Vegan' in r.get('dietary_forms', [])])
print(f"  Vegetarisch: {veg_count} ({veg_count/len(all_recipes)*100:.1f}%)")
print(f"  Vegan: {vegan_count} ({vegan_count/len(all_recipes)*100:.1f}%)")
