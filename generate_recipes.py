"""
Generiert 200 umfangreiche Rezepte für Großküchen
"""
import json
import random

# Rezept-Kategorien
categories = {
    "Frühstück": ["Müsli", "Brot", "Gebäck", "Aufstrich", "Warmes Frühstück"],
    "Hauptgang": ["Fleisch", "Fisch", "Vegetarisch", "Pasta", "Eintopf"],
    "Beilage": ["Kartoffeln", "Reis", "Gemüse", "Salat"],
    "Suppe": ["Klare Suppe", "Cremige Suppe", "Eintopf"],
    "Dessert": ["Pudding", "Kuchen", "Obst", "Eis"],
    "Zwischenmahlzeit": ["Snack", "Obst", "Joghurt", "Gebäck"]
}

# Allergene nach EU-Verordnung
allergens_list = [
    "Gluten", "Krebstiere", "Eier", "Fisch", "Erdnüsse", "Soja", 
    "Milch", "Schalenfrüchte", "Sellerie", "Senf", "Sesam", 
    "Schwefeldioxid", "Lupinen", "Weichtiere"
]

# Zusatzstoffe
additives_list = [
    "Konservierungsstoffe", "Antioxidationsmittel", "Farbstoffe",
    "Geschmacksverstärker", "Süßungsmittel", "Phosphat"
]

# Ernährungsformen
dietary_forms = ["Vollkost", "Vegetarisch", "Vegan", "Glutenfrei", "Laktosefrei"]

recipes = []
recipe_id = 1

# Frühstück (30 Rezepte)
breakfast_recipes = [
    ("Haferflocken-Porridge mit Früchten", 1.80, ["Gluten", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Müsli", [1,2,3,4,5,6,7,8,9,10,11,12], 8),
    ("Vollkornbrot mit Butter und Marmelade", 1.20, ["Gluten", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Brot", [1,2,3,4,5,6,7,8,9,10,11,12], 9),
    ("Rührei mit Schnittlauch", 2.10, ["Eier", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Warmes Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 8),
    ("Müsli mit Joghurt und Obst", 2.30, ["Gluten", "Milch", "Schalenfrüchte"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Müsli", [1,2,3,4,5,6,7,8,9,10,11,12], 9),
    ("Käsebrötchen", 1.50, ["Gluten", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Gebäck", [1,2,3,4,5,6,7,8,9,10,11,12], 7),
    ("Obstsalat", 1.90, [], [], ["Vollkost", "Vegetarisch", "Vegan"], "Frühstück", "Obst", [1,2,3,4,5,6,7,8,9,10,11,12], 8),
    ("Pancakes mit Ahornsirup", 2.40, ["Gluten", "Eier", "Milch"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Warmes Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 9),
    ("Croissant mit Marmelade", 1.60, ["Gluten", "Milch", "Eier"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Gebäck", [1,2,3,4,5,6,7,8,9,10,11,12], 8),
    ("Bircher Müsli", 2.00, ["Gluten", "Milch", "Schalenfrüchte"], [], ["Vollkost", "Vegetarisch"], "Frühstück", "Müsli", [1,2,3,4,5,6,7,8,9,10,11,12], 8),
    ("Spiegeleier mit Speck", 2.80, ["Eier"], [], ["Vollkost"], "Frühstück", "Warmes Frühstück", [1,2,3,4,5,6,7,8,9,10,11,12], 7),
]

for name, cost, allergens, additives, diets, component, group, seasonality, popularity in breakfast_recipes:
    recipes.append({
        "id": recipe_id,
        "name": name,
        "cost": cost,
        "allergens": allergens,
        "additives": additives,
        "dietary_forms": diets,
        "category": "Frühstück",
        "group": group,
        "menu_component": component,
        "seasonality": seasonality,
        "popularity": popularity,
        "nutritional_values": {
            "calories": random.randint(250, 450),
            "fat": random.randint(5, 20),
            "carbs": random.randint(30, 60),
            "protein": random.randint(8, 20)
        },
        "is_enabled": True,
        "status": "Freigegeben",
        "calculation_basis": 10,
        "processing_time": round(random.uniform(0.5, 1.5), 1),
        "description": f"{name} - Klassisches Frühstücksgericht",
        "portion_size": "1 Portion",
        "ingredients": []
    })
    recipe_id += 1

print(f"✅ {len(recipes)} Rezepte generiert")
print(json.dumps(recipes[:2], indent=2, ensure_ascii=False))
