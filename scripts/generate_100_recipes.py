#!/usr/bin/env python3
"""
Generiert 100 neue Rezepte für die Datenbank
"""
import json
import random

# Neue Rezepte (IDs 201-300)
new_recipes = []

# Frühstück (25 neue Rezepte, IDs 201-225)
fruehstueck_rezepte = [
    {"name": "Shakshuka", "cost": 3.20, "allergens": ["Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Eierspeisen", "popularity": 7, "description": "Pochierte Eier in würziger Tomatensauce mit Paprika"},
    {"name": "Congee (Reisbrei)", "cost": 1.90, "allergens": [], "dietary": ["Vollkost", "Vegan"], "group": "Brei", "popularity": 6, "description": "Asiatischer Reisbrei mit Gemüse und Sesam"},
    {"name": "Chilaquiles", "cost": 2.80, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Mexikanisch", "popularity": 6, "description": "Mexikanische Tortilla-Chips mit Salsa und Käse"},
    {"name": "Menemen", "cost": 2.90, "allergens": ["Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Eierspeisen", "popularity": 7, "description": "Türkisches Rührei mit Tomaten und Paprika"},
    {"name": "Smoothie Bowl Acai", "cost": 4.50, "allergens": ["Schalenfrüchte"], "dietary": ["Vollkost", "Vegan"], "group": "Smoothies", "popularity": 8, "description": "Acai-Bowl mit Früchten, Granola und Nüssen"},
    {"name": "Japanisches Frühstück", "cost": 5.20, "allergens": ["Fisch", "Soja", "Eier"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 5, "description": "Reis, gegrillter Lachs, Miso-Suppe und Tamagoyaki"},
    {"name": "Huevos Rancheros", "cost": 3.40, "allergens": ["Eier", "Gluten"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Mexikanisch", "popularity": 7, "description": "Eier auf Tortillas mit Bohnen und Salsa"},
    {"name": "Chia-Pudding", "cost": 2.10, "allergens": [], "dietary": ["Vollkost", "Vegan"], "group": "Pudding", "popularity": 8, "description": "Chia-Samen in Mandelmilch mit Früchten"},
    {"name": "Nasi Lemak", "cost": 4.80, "allergens": ["Fisch", "Schalenfrüchte"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 5, "description": "Malaysisches Kokosnuss-Reis-Gericht mit Anchovis"},
    {"name": "Crêpes mit Nutella", "cost": 2.60, "allergens": ["Gluten", "Milch", "Eier", "Schalenfrüchte"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Pfannkuchen", "popularity": 9, "description": "Dünne französische Pfannkuchen mit Haselnusscreme"},
    {"name": "Quinoa-Frühstücksbowl", "cost": 3.10, "allergens": ["Schalenfrüchte"], "dietary": ["Vollkost", "Vegan"], "group": "Bowls", "popularity": 7, "description": "Quinoa mit Früchten, Nüssen und Ahornsirup"},
    {"name": "Banh Mi Frühstück", "cost": 3.80, "allergens": ["Gluten", "Eier"], "dietary": ["Vollkost"], "group": "Sandwiches", "popularity": 6, "description": "Vietnamesisches Baguette mit Ei und Gemüse"},
    {"name": "Granola selbstgemacht", "cost": 2.40, "allergens": ["Gluten", "Schalenfrüchte"], "dietary": ["Vollkost", "Vegan"], "group": "Müsli", "popularity": 8, "description": "Gebackenes Müsli mit Honig und Nüssen"},
    {"name": "Türkischer Käse-Teller", "cost": 3.50, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Käse", "popularity": 7, "description": "Verschiedene Käsesorten mit Oliven und Brot"},
    {"name": "Tofu-Scramble", "cost": 2.70, "allergens": ["Soja"], "dietary": ["Vollkost", "Vegan"], "group": "Eierspeisen", "popularity": 6, "description": "Veganes Rührei aus Tofu mit Gemüse"},
    {"name": "Dim Sum Frühstück", "cost": 5.50, "allergens": ["Gluten", "Soja", "Fisch"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 7, "description": "Gedämpfte chinesische Teigtaschen"},
    {"name": "Protein-Pancakes", "cost": 3.30, "allergens": ["Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Pfannkuchen", "popularity": 8, "description": "Eiweißreiche Pfannkuchen mit Beeren"},
    {"name": "Falafel-Frühstück", "cost": 3.60, "allergens": ["Sesam"], "dietary": ["Vollkost", "Vegan"], "group": "Orientalisch", "popularity": 6, "description": "Kichererbsenbällchen mit Hummus und Gemüse"},
    {"name": "Kokos-Reis-Pudding", "cost": 2.20, "allergens": [], "dietary": ["Vollkost", "Vegan"], "group": "Pudding", "popularity": 7, "description": "Süßer Reispudding mit Kokosmilch"},
    {"name": "Eggs Benedict", "cost": 4.90, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost"], "group": "Eierspeisen", "popularity": 8, "description": "Pochierte Eier auf English Muffin mit Sauce Hollandaise"},
    {"name": "Matcha-Latte Bowl", "cost": 4.20, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Bowls", "popularity": 7, "description": "Grüntee-Pudding mit Früchten"},
    {"name": "Spanisches Tortilla", "cost": 2.90, "allergens": ["Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Eierspeisen", "popularity": 7, "description": "Kartoffel-Omelette nach spanischer Art"},
    {"name": "Overnight Oats Schoko", "cost": 2.30, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Müsli", "popularity": 8, "description": "Haferflocken mit Kakao über Nacht eingeweicht"},
    {"name": "Pho Bo Frühstück", "cost": 5.80, "allergens": ["Gluten"], "dietary": ["Vollkost"], "group": "Suppen", "popularity": 6, "description": "Vietnamesische Rindfleisch-Nudelsuppe"},
    {"name": "Avocado-Toast Premium", "cost": 4.10, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Toast", "popularity": 9, "description": "Sauerteigbrot mit Avocado, Tomaten und Microgreens"},
]

for i, rezept in enumerate(fruehstueck_rezepte, start=201):
    new_recipes.append({
        "id": i,
        "name": rezept["name"],
        "cost": rezept["cost"],
        "allergens": rezept["allergens"],
        "additives": [],
        "dietary_forms": rezept["dietary"],
        "category": "Frühstück",
        "group": rezept["group"],
        "menu_component": "Frühstück",
        "seasonality": list(range(1, 13)),
        "popularity": rezept["popularity"],
        "nutritional_values": {
            "calories": random.randint(250, 500),
            "fat": random.randint(5, 25),
            "carbs": random.randint(30, 60),
            "protein": random.randint(10, 30)
        },
        "is_enabled": True,
        "status": "Freigegeben",
        "calculation_basis": 10,
        "processing_time": round(random.uniform(0.3, 1.5), 1),
        "description": rezept["description"],
        "portion_size": "250g",
        "ingredients": []
    })

# Mittagessen (25 neue Rezepte, IDs 226-250)
mittagessen_rezepte = [
    {"name": "Pad Thai", "cost": 4.50, "allergens": ["Gluten", "Fisch", "Schalenfrüchte", "Eier"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 9, "description": "Thailändische gebratene Reisnudeln mit Garnelen"},
    {"name": "Moussaka", "cost": 5.20, "allergens": ["Milch", "Eier"], "dietary": ["Vollkost"], "group": "Auflauf", "popularity": 7, "description": "Griechischer Auberginen-Hackfleisch-Auflauf"},
    {"name": "Bibimbap", "cost": 4.80, "allergens": ["Soja", "Sesam", "Eier"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 8, "description": "Koreanische Reis-Bowl mit Gemüse und Ei"},
    {"name": "Paella Valenciana", "cost": 6.50, "allergens": ["Fisch", "Krebstiere"], "dietary": ["Vollkost"], "group": "Reisgerichte", "popularity": 8, "description": "Spanisches Reisgericht mit Meeresfrüchten"},
    {"name": "Ramen Premium", "cost": 5.90, "allergens": ["Gluten", "Soja", "Eier"], "dietary": ["Vollkost"], "group": "Suppen", "popularity": 9, "description": "Japanische Nudelsuppe mit Chashu-Schweinefleisch"},
    {"name": "Couscous Royal", "cost": 5.40, "allergens": ["Gluten"], "dietary": ["Vollkost"], "group": "Nordafrikanisch", "popularity": 7, "description": "Marokkanischer Couscous mit Lamm und Gemüse"},
    {"name": "Burritos Bowl", "cost": 4.20, "allergens": ["Milch"], "dietary": ["Vollkost"], "group": "Mexikanisch", "popularity": 9, "description": "Reis-Bowl mit Bohnen, Fleisch und Guacamole"},
    {"name": "Poke Bowl Lachs", "cost": 7.20, "allergens": ["Fisch", "Soja", "Sesam"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 8, "description": "Hawaiianische Reis-Bowl mit rohem Lachs"},
    {"name": "Tagine Lamm", "cost": 6.80, "allergens": [], "dietary": ["Vollkost"], "group": "Nordafrikanisch", "popularity": 6, "description": "Marokkanischer Lamm-Eintopf mit Aprikosen"},
    {"name": "Sushi-Platte", "cost": 8.50, "allergens": ["Fisch", "Soja", "Sesam"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 9, "description": "Verschiedene Sushi-Variationen"},
    {"name": "Osso Buco", "cost": 7.90, "allergens": [], "dietary": ["Vollkost"], "group": "Italienisch", "popularity": 7, "description": "Geschmorte Kalbshaxe mit Gremolata"},
    {"name": "Pho Ga", "cost": 4.60, "allergens": ["Gluten"], "dietary": ["Vollkost"], "group": "Suppen", "popularity": 8, "description": "Vietnamesische Hühner-Nudelsuppe"},
    {"name": "Falafel-Teller Premium", "cost": 4.90, "allergens": ["Sesam", "Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Orientalisch", "popularity": 8, "description": "Falafel mit Hummus, Tabouleh und Pita"},
    {"name": "Rendang Beef", "cost": 6.20, "allergens": ["Schalenfrüchte"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 7, "description": "Indonesisches Rindfleisch-Curry"},
    {"name": "Risotto Funghi Porcini", "cost": 5.80, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Reisgerichte", "popularity": 8, "description": "Cremiges Steinpilz-Risotto"},
    {"name": "Tandoori Chicken", "cost": 5.30, "allergens": ["Milch"], "dietary": ["Vollkost"], "group": "Indisch", "popularity": 8, "description": "Im Tandoor gegrilltes mariniertes Hähnchen"},
    {"name": "Shakshuka Mittagessen", "cost": 3.80, "allergens": ["Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Eierspeisen", "popularity": 7, "description": "Pochierte Eier in Tomatensauce mit Brot"},
    {"name": "Tom Yum Goong", "cost": 5.50, "allergens": ["Krebstiere", "Fisch"], "dietary": ["Vollkost"], "group": "Suppen", "popularity": 7, "description": "Thailändische sauer-scharfe Garnelensuppe"},
    {"name": "Enchiladas", "cost": 4.70, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost"], "group": "Mexikanisch", "popularity": 8, "description": "Gefüllte Tortillas mit Chili-Sauce überbacken"},
    {"name": "Laksa", "cost": 5.10, "allergens": ["Krebstiere", "Gluten"], "dietary": ["Vollkost"], "group": "Suppen", "popularity": 7, "description": "Malaysische Curry-Nudelsuppe"},
    {"name": "Gyros-Teller", "cost": 4.90, "allergens": [], "dietary": ["Vollkost"], "group": "Griechisch", "popularity": 9, "description": "Gegrilltes Schweinefleisch mit Tzatziki und Pommes"},
    {"name": "Butter Chicken", "cost": 5.60, "allergens": ["Milch"], "dietary": ["Vollkost"], "group": "Indisch", "popularity": 9, "description": "Hähnchen in cremiger Tomaten-Butter-Sauce"},
    {"name": "Ceviche", "cost": 6.90, "allergens": ["Fisch"], "dietary": ["Vollkost"], "group": "Lateinamerikanisch", "popularity": 6, "description": "Roher Fisch mariniert in Limettensaft"},
    {"name": "Massaman Curry", "cost": 5.20, "allergens": ["Schalenfrüchte"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 7, "description": "Thailändisches Curry mit Erdnüssen"},
    {"name": "Quinoa-Buddha-Bowl", "cost": 4.40, "allergens": ["Sesam"], "dietary": ["Vollkost", "Vegan"], "group": "Bowls", "popularity": 8, "description": "Quinoa mit geröstetem Gemüse und Tahini"},
]

for i, rezept in enumerate(mittagessen_rezepte, start=226):
    new_recipes.append({
        "id": i,
        "name": rezept["name"],
        "cost": rezept["cost"],
        "allergens": rezept["allergens"],
        "additives": [],
        "dietary_forms": rezept["dietary"],
        "category": "Mittagessen",
        "group": rezept["group"],
        "menu_component": "Mittagessen",
        "seasonality": list(range(1, 13)),
        "popularity": rezept["popularity"],
        "nutritional_values": {
            "calories": random.randint(400, 800),
            "fat": random.randint(15, 40),
            "carbs": random.randint(40, 80),
            "protein": random.randint(20, 50)
        },
        "is_enabled": True,
        "status": "Freigegeben",
        "calculation_basis": 10,
        "processing_time": round(random.uniform(1.0, 3.0), 1),
        "description": rezept["description"],
        "portion_size": "350g",
        "ingredients": []
    })

# Abendessen (25 neue Rezepte, IDs 251-275)
abendessen_rezepte = [
    {"name": "Tapas-Mix Premium", "cost": 5.80, "allergens": ["Fisch", "Milch"], "dietary": ["Vollkost"], "group": "Spanisch", "popularity": 8, "description": "Auswahl spanischer Häppchen"},
    {"name": "Sushi-Abend", "cost": 7.90, "allergens": ["Fisch", "Soja", "Sesam"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 9, "description": "Sushi-Platte mit Maki und Nigiri"},
    {"name": "Mezze-Platte Deluxe", "cost": 6.20, "allergens": ["Sesam", "Milch", "Gluten"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Orientalisch", "popularity": 8, "description": "Orientalische Vorspeisen-Auswahl"},
    {"name": "Charcuterie Board", "cost": 7.50, "allergens": ["Milch", "Schalenfrüchte"], "dietary": ["Vollkost"], "group": "Käse", "popularity": 8, "description": "Käse- und Wurstplatte mit Beilagen"},
    {"name": "Dim Sum Platte", "cost": 6.80, "allergens": ["Gluten", "Soja", "Krebstiere"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 7, "description": "Gedämpfte chinesische Teigtaschen"},
    {"name": "Antipasti Premium", "cost": 5.90, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 8, "description": "Italienische Vorspeisen mit Mozzarella"},
    {"name": "Poke Bowl Thunfisch", "cost": 6.90, "allergens": ["Fisch", "Soja", "Sesam"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 8, "description": "Hawaiianische Bowl mit rohem Thunfisch"},
    {"name": "Quiche Lorraine", "cost": 3.90, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost"], "group": "Französisch", "popularity": 7, "description": "Französischer Speckkuchen"},
    {"name": "Gazpacho mit Brot", "cost": 2.80, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Suppen", "popularity": 6, "description": "Kalte spanische Tomatensuppe"},
    {"name": "Crostini-Variation", "cost": 4.20, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 7, "description": "Geröstetes Brot mit verschiedenen Belägen"},
    {"name": "Sommer-Rollen", "cost": 3.60, "allergens": ["Krebstiere", "Gluten"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 7, "description": "Vietnamesische Reispapier-Rollen"},
    {"name": "Baba Ghanoush Platte", "cost": 3.40, "allergens": ["Sesam", "Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Orientalisch", "popularity": 6, "description": "Auberginen-Dip mit Pita-Brot"},
    {"name": "Vitello Tonnato", "cost": 6.50, "allergens": ["Fisch", "Eier"], "dietary": ["Vollkost"], "group": "Italienisch", "popularity": 7, "description": "Kalbfleisch mit Thunfisch-Kapern-Sauce"},
    {"name": "Wraps-Platte", "cost": 3.80, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "International", "popularity": 8, "description": "Verschiedene gefüllte Wraps"},
    {"name": "Sashimi-Platte", "cost": 9.20, "allergens": ["Fisch"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 7, "description": "Roher Fisch in dünnen Scheiben"},
    {"name": "Pincho-Spieße", "cost": 4.50, "allergens": [], "dietary": ["Vollkost"], "group": "Spanisch", "popularity": 8, "description": "Spanische Fleisch-Gemüse-Spieße"},
    {"name": "Caprese Premium", "cost": 4.80, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 8, "description": "Büffelmozzarella mit Tomaten und Basilikum"},
    {"name": "Edamame mit Meersalz", "cost": 2.50, "allergens": ["Soja"], "dietary": ["Vollkost", "Vegan"], "group": "Asiatisch", "popularity": 7, "description": "Gedämpfte grüne Sojabohnen"},
    {"name": "Tarte Flambée", "cost": 4.10, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost"], "group": "Französisch", "popularity": 8, "description": "Elsässischer Flammkuchen"},
    {"name": "Hummus-Trio", "cost": 3.70, "allergens": ["Sesam"], "dietary": ["Vollkost", "Vegan"], "group": "Orientalisch", "popularity": 7, "description": "Drei Hummus-Variationen mit Gemüse"},
    {"name": "Arancini", "cost": 3.90, "allergens": ["Gluten", "Milch", "Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 7, "description": "Frittierte sizilianische Reisbällchen"},
    {"name": "Pita-Taschen", "cost": 3.20, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Orientalisch", "popularity": 8, "description": "Gefüllte Pita-Brote mit Falafel"},
    {"name": "Onigiri-Set", "cost": 3.50, "allergens": ["Fisch", "Soja"], "dietary": ["Vollkost"], "group": "Asiatisch", "popularity": 6, "description": "Japanische Reis-Dreiecke mit Füllung"},
    {"name": "Bruschetta-Variation", "cost": 3.60, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Italienisch", "popularity": 8, "description": "Geröstetes Brot mit verschiedenen Toppings"},
    {"name": "Samosa-Platte", "cost": 3.40, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Indisch", "popularity": 7, "description": "Frittierte indische Teigtaschen"},
]

for i, rezept in enumerate(abendessen_rezepte, start=251):
    new_recipes.append({
        "id": i,
        "name": rezept["name"],
        "cost": rezept["cost"],
        "allergens": rezept["allergens"],
        "additives": [],
        "dietary_forms": rezept["dietary"],
        "category": "Abendessen",
        "group": rezept["group"],
        "menu_component": "Abendessen",
        "seasonality": list(range(1, 13)),
        "popularity": rezept["popularity"],
        "nutritional_values": {
            "calories": random.randint(300, 600),
            "fat": random.randint(10, 35),
            "carbs": random.randint(25, 55),
            "protein": random.randint(15, 35)
        },
        "is_enabled": True,
        "status": "Freigegeben",
        "calculation_basis": 10,
        "processing_time": round(random.uniform(0.5, 2.0), 1),
        "description": rezept["description"],
        "portion_size": "200g",
        "ingredients": []
    })

# Zwischenmahlzeit (25 neue Rezepte, IDs 276-300)
zwischenmahlzeit_rezepte = [
    {"name": "Mochi-Mix", "cost": 2.80, "allergens": ["Soja"], "dietary": ["Vollkost", "Vegan"], "group": "Asiatisch", "popularity": 7, "description": "Japanische Reiskuchen mit verschiedenen Füllungen"},
    {"name": "Churros mit Schokolade", "cost": 2.90, "allergens": ["Gluten", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Spanisch", "popularity": 9, "description": "Frittierte Teigstangen mit heißer Schokolade"},
    {"name": "Baklava", "cost": 3.20, "allergens": ["Gluten", "Schalenfrüchte"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Orientalisch", "popularity": 8, "description": "Türkisches Blätterteig-Gebäck mit Nüssen"},
    {"name": "Macarons-Box", "cost": 4.50, "allergens": ["Eier", "Schalenfrüchte", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Französisch", "popularity": 8, "description": "Französische Mandel-Baiser-Kekse"},
    {"name": "Taiyaki", "cost": 2.60, "allergens": ["Gluten", "Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Asiatisch", "popularity": 6, "description": "Japanischer fischförmiger Kuchen mit Füllung"},
    {"name": "Empanadas süß", "cost": 2.40, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Lateinamerikanisch", "popularity": 7, "description": "Gefüllte Teigtaschen mit Früchten"},
    {"name": "Tiramisu-Becher", "cost": 3.80, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 9, "description": "Italienisches Mascarpone-Dessert"},
    {"name": "Dorayaki", "cost": 2.50, "allergens": ["Gluten", "Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Asiatisch", "popularity": 6, "description": "Japanische Pfannkuchen mit roter Bohnenpaste"},
    {"name": "Panna Cotta", "cost": 3.10, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 8, "description": "Italienisches Sahne-Dessert"},
    {"name": "Bubble Tea", "cost": 3.50, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Asiatisch", "popularity": 9, "description": "Taiwanesisches Getränk mit Tapioka-Perlen"},
    {"name": "Crème Brûlée", "cost": 4.20, "allergens": ["Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Französisch", "popularity": 8, "description": "Französische Vanillecreme mit Karamellkruste"},
    {"name": "Mango Sticky Rice", "cost": 3.40, "allergens": [], "dietary": ["Vollkost", "Vegan"], "group": "Asiatisch", "popularity": 7, "description": "Thailändischer Klebreis mit Mango"},
    {"name": "Churros-Eis", "cost": 3.90, "allergens": ["Gluten", "Milch", "Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Spanisch", "popularity": 9, "description": "Churros mit Eiscreme"},
    {"name": "Dango-Spieße", "cost": 2.70, "allergens": ["Soja"], "dietary": ["Vollkost", "Vegan"], "group": "Asiatisch", "popularity": 6, "description": "Japanische Reismehl-Kugeln am Spieß"},
    {"name": "Loukoumades", "cost": 2.80, "allergens": ["Gluten"], "dietary": ["Vollkost", "Vegan"], "group": "Griechisch", "popularity": 7, "description": "Griechische Honigbällchen"},
    {"name": "Affogato", "cost": 3.60, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 7, "description": "Vanilleeis mit heißem Espresso"},
    {"name": "Gulab Jamun", "cost": 2.90, "allergens": ["Milch", "Gluten"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Indisch", "popularity": 6, "description": "Indische Milchbällchen in Sirup"},
    {"name": "Profiteroles", "cost": 3.70, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Französisch", "popularity": 8, "description": "Windbeutel mit Sahne und Schokolade"},
    {"name": "Kulfi", "cost": 3.20, "allergens": ["Milch", "Schalenfrüchte"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Indisch", "popularity": 6, "description": "Indisches Eis mit Pistazien"},
    {"name": "Beignets", "cost": 2.60, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Französisch", "popularity": 7, "description": "Französische Krapfen mit Puderzucker"},
    {"name": "Matcha-Kuchen", "cost": 3.50, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Asiatisch", "popularity": 7, "description": "Grüntee-Kuchen nach japanischer Art"},
    {"name": "Flan", "cost": 2.80, "allergens": ["Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Lateinamerikanisch", "popularity": 7, "description": "Karamell-Pudding"},
    {"name": "Cannoli", "cost": 3.40, "allergens": ["Gluten", "Milch", "Eier"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 8, "description": "Sizilianische Teigrollen mit Ricotta"},
    {"name": "Tres Leches Cake", "cost": 3.60, "allergens": ["Gluten", "Eier", "Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Lateinamerikanisch", "popularity": 7, "description": "Kuchen getränkt in drei Milchsorten"},
    {"name": "Gelato-Becher", "cost": 3.80, "allergens": ["Milch"], "dietary": ["Vollkost", "Vegetarisch"], "group": "Italienisch", "popularity": 9, "description": "Italienisches Eis in verschiedenen Sorten"},
]

for i, rezept in enumerate(zwischenmahlzeit_rezepte, start=276):
    new_recipes.append({
        "id": i,
        "name": rezept["name"],
        "cost": rezept["cost"],
        "allergens": rezept["allergens"],
        "additives": [],
        "dietary_forms": rezept["dietary"],
        "category": "Zwischenmahlzeit",
        "group": rezept["group"],
        "menu_component": "Zwischenmahlzeit",
        "seasonality": list(range(1, 13)),
        "popularity": rezept["popularity"],
        "nutritional_values": {
            "calories": random.randint(200, 400),
            "fat": random.randint(5, 20),
            "carbs": random.randint(30, 60),
            "protein": random.randint(3, 15)
        },
        "is_enabled": True,
        "status": "Freigegeben",
        "calculation_basis": 10,
        "processing_time": round(random.uniform(0.3, 1.5), 1),
        "description": rezept["description"],
        "portion_size": "150g",
        "ingredients": []
    })

# Speichere die neuen Rezepte
with open('/home/ubuntu/menuplan-simulator-v5/data/new_recipes_100.json', 'w', encoding='utf-8') as f:
    json.dump(new_recipes, f, ensure_ascii=False, indent=2)

print(f"✅ {len(new_recipes)} neue Rezepte erstellt!")
print(f"\nVerteilung:")
print(f"- Frühstück: {len([r for r in new_recipes if r['menu_component'] == 'Frühstück'])}")
print(f"- Mittagessen: {len([r for r in new_recipes if r['menu_component'] == 'Mittagessen'])}")
print(f"- Abendessen: {len([r for r in new_recipes if r['menu_component'] == 'Abendessen'])}")
print(f"- Zwischenmahlzeit: {len([r for r in new_recipes if r['menu_component'] == 'Zwischenmahlzeit'])}")
