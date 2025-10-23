#!/usr/bin/env python3.11
"""
Script to automatically categorize recipes with new fields:
- contains_meat: Recipe contains meat
- is_sweet: Recipe is a dessert or sweet dish
- is_fried: Recipe involves frying
- is_whole_grain: Recipe contains whole grain products
- contains_raw_milk: Recipe contains raw milk products
- contains_raw_eggs: Recipe contains raw eggs
- contains_raw_sausage: Recipe contains raw sausage
- contains_raw_meat: Recipe contains raw meat
"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def categorize_recipe(recipe):
    """Automatically categorize a recipe based on its attributes"""
    name = recipe.get('name', '').lower()
    group = recipe.get('group', '').lower()
    category = recipe.get('category', '').lower()
    description = recipe.get('description', '').lower()
    ingredients = recipe.get('ingredients', [])
    
    # Initialize all new fields
    recipe['contains_meat'] = False
    recipe['is_sweet'] = False
    recipe['is_fried'] = False
    recipe['is_whole_grain'] = False
    recipe['contains_raw_milk'] = False
    recipe['contains_raw_eggs'] = False
    recipe['contains_raw_sausage'] = False
    recipe['contains_raw_meat'] = False
    
    # Meat detection
    meat_keywords = [
        'fleisch', 'hähnchen', 'huhn', 'chicken', 'rind', 'schwein', 'pork', 'beef',
        'schnitzel', 'steak', 'wurst', 'sausage', 'schinken', 'ham', 'bacon',
        'hackfleisch', 'gulasch', 'braten', 'lamm', 'lamb', 'ente', 'duck',
        'pute', 'turkey', 'kalb', 'veal', 'frikadelle', 'burger', 'bolognese'
    ]
    meat_groups = ['fleisch', 'geflügel', 'meat', 'poultry']
    
    if any(keyword in name for keyword in meat_keywords) or \
       any(keyword in group for keyword in meat_groups) or \
       any(keyword in description for keyword in meat_keywords):
        recipe['contains_meat'] = True
    
    # Check ingredients for meat
    for ingredient in ingredients:
        ing_name = ingredient.get('name', '').lower()
        if any(keyword in ing_name for keyword in meat_keywords):
            recipe['contains_meat'] = True
            break
    
    # Sweet detection
    sweet_keywords = [
        'kuchen', 'cake', 'dessert', 'pudding', 'mousse', 'ice cream',
        'süß', 'sweet', 'schokolade', 'chocolate', 'vanille', 'vanilla',
        'kompott', 'obstsalat', 'fruit salad', 'tiramisu', 'brownie',
        'muffin', 'cookie', 'keks', 'torte', 'creme', 'cream', 'zucker',
        'apfelstrudel', 'kaiserschmarrn', 'palatschinken', 'crêpe'
    ]
    # Special keywords that need word boundary check (to avoid "reis" matching "eis")
    sweet_keywords_boundary = ['eis', 'speiseeis']
    sweet_categories = ['dessert', 'nachspeise', 'süßspeise']
    
    is_sweet = False
    if any(keyword in name for keyword in sweet_keywords) or \
       any(keyword in category for keyword in sweet_categories) or \
       any(keyword in description for keyword in sweet_keywords):
        is_sweet = True
    
    # Check boundary keywords (must be standalone words)
    import re
    for keyword in sweet_keywords_boundary:
        if re.search(r'\b' + keyword + r'\b', name) or \
           re.search(r'\b' + keyword + r'\b', description):
            is_sweet = True
            break
    
    recipe['is_sweet'] = is_sweet
    
    # Fried detection (focus on deep-fried, not pan-fried)
    fried_keywords = [
        'frittiert', 'fritiert', 'deep fried', 'schnitzel', 'pommes', 'fries',
        'kroketten', 'nuggets', 'paniert', 'breaded', 'ausgebacken',
        'rösti', 'hash brown', 'tempura', 'fish and chips', 'backfisch',
        'chicken wings', 'hähnchen wings', 'churros', 'donut'
    ]
    
    if any(keyword in name for keyword in fried_keywords) or \
       any(keyword in description for keyword in fried_keywords):
        recipe['is_fried'] = True
    
    # Whole grain detection
    whole_grain_keywords = [
        'vollkorn', 'whole grain', 'wholemeal', 'vollwert', 'hafer',
        'oat', 'dinkel', 'spelt', 'roggen', 'rye', 'quinoa', 'buchweizen'
    ]
    
    if any(keyword in name for keyword in whole_grain_keywords) or \
       any(keyword in description for keyword in whole_grain_keywords):
        recipe['is_whole_grain'] = True
    
    # Check ingredients for whole grain
    for ingredient in ingredients:
        ing_name = ingredient.get('name', '').lower()
        if any(keyword in ing_name for keyword in whole_grain_keywords):
            recipe['is_whole_grain'] = True
            break
    
    # Raw milk detection
    raw_milk_keywords = [
        'rohmilch', 'raw milk', 'unpasteurisiert', 'unpasteurized',
        'frischmilch', 'vorzugsmilch'
    ]
    
    if any(keyword in name for keyword in raw_milk_keywords) or \
       any(keyword in description for keyword in raw_milk_keywords):
        recipe['contains_raw_milk'] = True
    
    # Raw eggs detection (e.g., in Tiramisu, Mayonnaise)
    raw_egg_dishes = [
        'tiramisu', 'mayonnaise', 'mayo', 'aioli', 'mousse au chocolat',
        'zabaione', 'eggnog', 'hollandaise'
    ]
    
    if any(dish in name for dish in raw_egg_dishes) or \
       any(dish in description for dish in raw_egg_dishes):
        recipe['contains_raw_eggs'] = True
    
    # Raw sausage detection
    raw_sausage_keywords = [
        'mettwurst', 'teewurst', 'mett', 'rohwurst', 'salami',
        'chorizo', 'cervelat', 'landjäger'
    ]
    
    if any(keyword in name for keyword in raw_sausage_keywords) or \
       any(keyword in description for keyword in raw_sausage_keywords):
        recipe['contains_raw_sausage'] = True
    
    # Raw meat detection (e.g., Carpaccio, Tartare)
    raw_meat_dishes = [
        'carpaccio', 'tartare', 'tartar', 'mett', 'sushi', 'sashimi',
        'ceviche', 'roh'
    ]
    
    if any(dish in name for dish in raw_meat_dishes):
        recipe['contains_raw_meat'] = True
    
    return recipe


def main():
    """Main function to categorize all recipes"""
    # Load recipes
    recipes_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_200.json')
    
    if not os.path.exists(recipes_file):
        print(f"❌ Error: {recipes_file} not found")
        return 1
    
    with open(recipes_file, 'r', encoding='utf-8') as f:
        recipes = json.load(f)
    
    print(f"📊 Processing {len(recipes)} recipes...")
    
    # Categorize each recipe
    categorized_count = {
        'contains_meat': 0,
        'is_sweet': 0,
        'is_fried': 0,
        'is_whole_grain': 0,
        'contains_raw_milk': 0,
        'contains_raw_eggs': 0,
        'contains_raw_sausage': 0,
        'contains_raw_meat': 0
    }
    
    for recipe in recipes:
        recipe = categorize_recipe(recipe)
        
        # Count categorizations
        for key in categorized_count:
            if recipe.get(key, False):
                categorized_count[key] += 1
    
    # Save updated recipes
    output_file = recipes_file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully categorized {len(recipes)} recipes")
    print(f"\n📈 Categorization Statistics:")
    for key, count in categorized_count.items():
        percentage = (count / len(recipes)) * 100
        print(f"  - {key}: {count} recipes ({percentage:.1f}%)")
    
    print(f"\n💾 Updated file: {output_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

