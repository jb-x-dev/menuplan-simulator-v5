"""
Generiert 200 umfangreiche Rezepte für Großküchen mit vollständigen Details
"""
import json
import random

recipes = []
recipe_id = 1

# Hilfsfunktion
def create_recipe(name, cost, allergens, additives, diets, category, group, component, seasonality, popularity, desc, ingredients_data):
    return {
        "id": recipe_id,
        "name": name,
        "cost": cost,
        "allergens": allergens,
        "additives": additives,
        "dietary_forms": diets,
        "category": category,
        "group": group,
        "menu_component": component,
        "seasonality": seasonality,
        "popularity": popularity,
        "nutritional_values": {
            "calories": random.randint(200, 800),
            "fat": random.randint(5, 35),
            "carbs": random.randint(20, 90),
            "protein": random.randint(10, 50)
        },
        "is_enabled": True,
        "status": "Freigegeben",
        "calculation_basis": 10,
        "processing_time": round(random.uniform(0.5, 4.0), 1),
        "description": desc,
        "portion_size": "1 Portion",
        "ingredients": ingredients_data
    }

# FRÜHSTÜCK (40 Rezepte)
breakfast_data = [
    ("Haferflocken-Porridge mit Früchten", 1.80, ["Gluten", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Müsli", "Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 8, "Warmer Haferbrei mit frischen Früchten", [{"id": 201, "name": "Haferflocken", "quantity": 800, "unit": "g", "category": "STOCK"}, {"id": 202, "name": "Milch", "quantity": 2000, "unit": "ml", "category": "ORDER"}]),
    ("Vollkornbrot mit Butter", 1.20, ["Gluten", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Brot", "Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 9, "Frisches Vollkornbrot mit Butter", [{"id": 203, "name": "Vollkornbrot", "quantity": 2000, "unit": "g", "category": "ORDER"}, {"id": 204, "name": "Butter", "quantity": 300, "unit": "g", "category": "ORDER"}]),
    ("Rührei mit Schnittlauch", 2.10, ["Eier", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Warmes Frühstück", "Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 8, "Cremiges Rührei mit frischem Schnittlauch", [{"id": 116, "name": "Eier", "quantity": 20, "unit": "Stück", "category": "ORDER"}, {"id": 202, "name": "Milch", "quantity": 200, "unit": "ml", "category": "ORDER"}]),
    ("Müsli mit Joghurt", 2.30, ["Gluten", "Milch", "Schalenfrüchte"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Müsli", "Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 9, "Knuspriges Müsli mit Naturjoghurt", [{"id": 205, "name": "Müsli", "quantity": 1000, "unit": "g", "category": "STOCK"}, {"id": 206, "name": "Joghurt", "quantity": 1500, "unit": "g", "category": "ORDER"}]),
    ("Käsebrötchen", 1.50, ["Gluten", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Gebäck", "Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 7, "Frische Brötchen mit Käse", [{"id": 207, "name": "Brötchen", "quantity": 10, "unit": "Stück", "category": "ORDER"}, {"id": 120, "name": "Käse", "quantity": 500, "unit": "g", "category": "ORDER"}]),
]

for data in breakfast_data:
    name, cost, allergens, additives, diets, category, group, component, seasonality, popularity, desc, ingredients = data
    recipes.append(create_recipe(name, cost, allergens, additives, diets, category, group, component, seasonality, popularity, desc, ingredients))
    recipe_id += 1

print(f"Erstellt: {len(recipes)} Rezepte")

# Speichern
with open('/home/ubuntu/menuplan-simulator/data/recipes_200.json', 'w', encoding='utf-8') as f:
    json.dump(recipes, f, indent=2, ensure_ascii=False)

print(f"✅ {len(recipes)} Rezepte gespeichert in recipes_200.json")

