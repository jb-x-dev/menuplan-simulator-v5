"""
Initialisiert Standard-Rezept-Auswahl für sofortige Nutzbarkeit
"""
import json
from backend.recipe_selection_db import select_recipe, get_selection_count

def init_default_selection():
    """
    Wählt automatisch eine ausgewogene Auswahl an Rezepten aus,
    falls noch keine Auswahl getroffen wurde.
    """
    # Prüfe ob bereits Rezepte ausgewählt sind
    current_count = get_selection_count()
    if current_count > 0:
        print(f"✅ {current_count} Rezepte bereits ausgewählt, überspringe Initialisierung")
        return
    
    print("🔄 Initialisiere Standard-Rezept-Auswahl...")
    
    # Lade alle Rezepte
    try:
        with open('data/recipes_200.json', 'r', encoding='utf-8') as f:
            all_recipes = json.load(f)
    except FileNotFoundError:
        print("❌ recipes_200.json nicht gefunden")
        return
    
    # Gruppiere nach Komponente
    by_component = {}
    for recipe in all_recipes:
        component = recipe.get('menu_component', 'Unknown')
        if component not in by_component:
            by_component[component] = []
        by_component[component].append(recipe)
    
    # Wähle ausgewogene Anzahl pro Komponente
    # Ziel: ~60-80 Rezepte total (30-40% der Gesamtmenge)
    target_per_component = {
        'Frühstück': 15,      # von 35 (43%)
        'Mittagessen': 40,    # von 105 (38%)
        'Abendessen': 15,     # von 33 (45%)
        'Zwischenmahlzeit': 10  # von 27 (37%)
    }
    
    selected_count = 0
    for component, recipes in by_component.items():
        target = target_per_component.get(component, 10)
        
        # Sortiere nach Status (Aktiv bevorzugen) und dann alphabetisch
        sorted_recipes = sorted(
            recipes,
            key=lambda r: (
                0 if r.get('status') == 'Aktiv' else 1,
                r.get('name', '')
            )
        )
        
        # Wähle die ersten N Rezepte
        selected = sorted_recipes[:target]
        
        for recipe in selected:
            select_recipe(
                recipe['id'],
                recipe['name'],
                recipe.get('menu_component', 'Unknown')
            )
            selected_count += 1
        
        print(f"  ✅ {component}: {len(selected)} von {len(recipes)} Rezepten ausgewählt")
    
    print(f"🎉 Standard-Auswahl initialisiert: {selected_count} Rezepte ausgewählt")
    print(f"   Diese Auswahl ermöglicht sofortige Menüplan-Generierung!")

if __name__ == '__main__':
    init_default_selection()

