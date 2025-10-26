"""
Flask API Server für Menüplansimulator
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from whitenoise import WhiteNoise
from dataclasses import asdict
import json
import os
import sys

# Importiere Simulator
try:
    from backend.simulator import load_recipes_from_file, run_simulation, Recipe
    from backend.procurement import resolve_procurement
    from backend.recipe_selection_db import get_selected_recipe_ids
    from backend.pdf_export import create_menu_plan_pdf
    from backend.customer_pdf import generate_customer_pdf
    from backend.excel_export import create_excel_export
    from backend.health_check import register_health_routes
    from backend.recipe_selection_api import recipe_selection_bp
    from backend.version_api import get_version
    from backend.init_default_selection import init_default_selection
except ImportError:
    # Fallback für lokale Ausführung
    from simulator import load_recipes_from_file, run_simulation, Recipe
    from procurement import resolve_procurement
    from recipe_selection_db import get_selected_recipe_ids
    from pdf_export import create_menu_plan_pdf
    from customer_pdf import generate_customer_pdf
    from excel_export import create_excel_export
    from health_check import register_health_routes
    from recipe_selection_api import recipe_selection_bp
    from version_api import get_version
    from init_default_selection import init_default_selection

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Apply WhiteNoise middleware for production static file serving
app.wsgi_app = WhiteNoise(
    app.wsgi_app,
    root=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
    prefix='',
    autorefresh=True,
    max_age=31536000 if not app.debug else 0
)

CORS(app)

# Registriere Health Check Routes
register_health_routes(app)

# Registriere Recipe Selection API
app.register_blueprint(recipe_selection_bp)

# Rezept-Auswahl-System deaktiviert - alle Rezepte immer verfügbar
# init_default_selection()  # Nicht mehr benötigt

# Version API-Endpunkt
@app.route('/api/version', methods=['GET'])
def version():
    """Gibt die aktuelle Version zurück"""
    return jsonify({
        'version': get_version(),
        'name': 'Menüplansimulator',
        'status': 'production'
    })

# API-Endpunkt für verfügbare Mahlzeiten-Kategorien
@app.route('/api/meal-categories', methods=['GET'])
def get_meal_categories():
    """Gibt verfügbare Mahlzeiten-Kategorien aus den Rezepten zurück"""
    try:
        categories = {}
        for recipe in recipes:
            comp = recipe.menu_component
            if comp not in categories:
                categories[comp] = 0
            categories[comp] += 1
        
        result = [
            {'name': name, 'count': count}
            for name, count in sorted(categories.items())
        ]
        return jsonify({'success': True, 'categories': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Lade Rezepte beim Start (300 Rezepte)
recipes_file_300 = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_300.json')
recipes_file_200 = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_200.json')
recipes_file_extended = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_extended.json')
recipes_file_original = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')

# Versuche 300 Rezepte zu laden, sonst Fallback
if os.path.exists(recipes_file_300):
    recipes = load_recipes_from_file(recipes_file_300)
    print(f"✅ Loaded {len(recipes)} recipes from 300-recipe database")
elif os.path.exists(recipes_file_200):
    recipes = load_recipes_from_file(recipes_file_200)
    print(f"✅ Loaded {len(recipes)} recipes from 200-recipe database")
elif os.path.exists(recipes_file_extended):
    recipes = load_recipes_from_file(recipes_file_extended)
    print(f"✅ Loaded {len(recipes)} recipes from extended database")
else:
    recipes = load_recipes_from_file(recipes_file_original)
    print(f"✅ Loaded {len(recipes)} recipes from original database")


@app.route('/')
def index():
    """Serve Landing Page"""
    return send_from_directory(app.static_folder, 'landing.html')


@app.route('/index.html')
def main_app():
    """Serve Main Application"""
    response = send_from_directory(app.static_folder, 'index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/order-lists.html')
def order_lists():
    """Serve Order Lists Management Page"""
    import os
    file_path = os.path.join(app.static_folder, 'order-lists.html')
    print(f"DEBUG: Looking for order-lists.html at: {file_path}")
    print(f"DEBUG: File exists: {os.path.exists(file_path)}")
    print(f"DEBUG: static_folder: {app.static_folder}")
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, 'order-lists.html')
    else:
        return jsonify({'error': f'File not found at {file_path}'}), 404


@app.route('/meal-plans.html')
def meal_plans():
    """Serve Meal Plans Management Page"""
    import os
    file_path = os.path.join(app.static_folder, 'meal-plans.html')
    print(f"DEBUG: Looking for meal-plans.html at: {file_path}")
    print(f"DEBUG: File exists: {os.path.exists(file_path)}")
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, 'meal-plans.html')
    else:
        return jsonify({'error': f'File not found at {file_path}'}), 404


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Gibt alle Rezepte zurück"""
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'cost': r.cost,
        'allergens': r.allergens,
        'dietary_forms': r.dietary_forms,
        'category': r.category,
        'group': r.group,
        'menu_component': r.menu_component,
        'popularity': r.popularity,
        'is_enabled': r.is_enabled,
        'status': r.status,
        'additives': r.additives if hasattr(r, 'additives') else [],
        'description': r.description if hasattr(r, 'description') else '',
        'portion_size': r.portion_size if hasattr(r, 'portion_size') else '1 Portion',
        'nutritional_values': r.nutritional_values if hasattr(r, 'nutritional_values') else {},
        'ingredients': r.ingredients if hasattr(r, 'ingredients') else [],
        'processing_time': r.processing_time if hasattr(r, 'processing_time') else 0
    } for r in recipes])


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Führt Simulation aus"""
    try:
        config = request.json
        
        # Validierung
        required_fields = ['start_date', 'end_date', 'menu_lines', 'bkt_target']
        for field in required_fields:
            if field not in config:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Verwende ALLE Rezepte (Auswahlsystem deaktiviert)
        filtered_recipes = recipes
        print(f"✅ Using all {len(filtered_recipes)} recipes")
        
        # Führe Simulation mit allen Rezepten aus
        result = run_simulation(config, filtered_recipes)
        
        return jsonify({
            'success': True,
            'plan': result
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config/example', methods=['GET'])
def get_example_config():
    """Gibt Beispiel-Konfiguration zurück"""
    from datetime import date, timedelta
    
    start = date.today() + timedelta(days=7)
    end = start + timedelta(days=13)  # 2 Wochen
    
    return jsonify({
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'kitchen_id': 1,
        'menu_lines': [
            {
                'id': 1,
                'name': 'Vollkost',
                'cost_forms': [
                    {'id': 1, 'name': 'Mittagessen', 'component': 'Mittagessen'},
                    {'id': 2, 'name': 'Abendessen', 'component': 'Abendessen'}
                ]
            },
            {
                'id': 2,
                'name': 'Vegetarisch',
                'cost_forms': [
                    {'id': 3, 'name': 'Mittagessen', 'component': 'Mittagessen'}
                ]
            }
        ],
        'bkt_target': 8.0,
        'bkt_tolerance': 0.15,
        'dietary_forms': ['Vollkost', 'Vegetarisch'],
        'excluded_allergens': ['Gluten'],
        'excluded_aversions': [],
        'repetition_interval': 7,
        'consider_seasonality': True
    })


@app.route('/api/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    """Gibt detaillierte Informationen zu einem Rezept zurück"""
    try:
        recipe = next((r for r in recipes if r.id == recipe_id), None)
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        return jsonify({
            'success': True,
            'recipe': {
                'id': recipe.id,
                'name': recipe.name,
                'cost': recipe.cost,
                'allergens': recipe.allergens,
                'additives': recipe.additives,
                'dietary_forms': recipe.dietary_forms,
                'category': recipe.category,
                'group': recipe.group,
                'menu_component': recipe.menu_component,
                'description': recipe.description,
                'portion_size': recipe.portion_size,
                'nutritional_values': recipe.nutritional_values,
                'processing_time': recipe.processing_time,
                'calculation_basis': recipe.calculation_basis,
                'ingredients': recipe.ingredients,
                'popularity': recipe.popularity,
                'seasonality': recipe.seasonality
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recipes/by-component/<component>', methods=['GET'])
def get_recipes_by_component(component):
    """Gibt alle Rezepte für eine bestimmte Mahlzeit zurück"""
    try:
        filtered = [r for r in recipes if r.menu_component == component]
        return jsonify({
            'success': True,
            'count': len(filtered),
            'recipes': [{
                'id': r.id,
                'name': r.name,
                'cost': r.cost,
                'allergens': r.allergens,
                'dietary_forms': r.dietary_forms,
                'category': r.category,
                'popularity': r.popularity
            } for r in filtered]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/procurement', methods=['POST'])
def get_procurement():
    """Löst Menüplan in Beschaffungsbedarfe auf"""
    try:
        data = request.json
        
        if 'plan' not in data:
            return jsonify({'error': 'Missing field: plan'}), 400
        
        # Führe Beschaffungsauflösung aus
        result = resolve_procurement(data['plan'], recipes)
        
        return jsonify({
            'success': True,
            'procurement': result
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Exportiert Menüplan als PDF"""
    try:
        data = request.json
        
        if 'plan' not in data or 'config' not in data:
            return jsonify({'error': 'Missing plan or config'}), 400
        
        # Erstelle PDF
        pdf_buffer = create_menu_plan_pdf(data['plan'], data['config'])
        
        # Sende PDF
        from flask import send_file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"menuplan_{data['config']['start_date']}.pdf"
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/customer-pdf', methods=['POST'])
def export_customer_pdf():
    """
    Exportiert Menüplan als PDF für Abnehmer (ohne Preise)
    Zeigt nur Menüdaten, Allergene und Nährwerte für 7 Tage
    """
    try:
        data = request.json
        
        # Validierung
        if not data:
            return jsonify({'error': 'Keine Daten'}), 400
        
        # Extrahiere Plan und Orientierung
        plan_data = data.get('plan', data)  # Fallback für altes Format
        orientation = data.get('orientation', 'portrait')  # Default: Hochkant
        
        if 'days' not in plan_data:
            return jsonify({'error': 'Ungültige Plan-Daten'}), 400
        
        # Dateiname generieren
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'wochenplan_abnehmer_{timestamp}.pdf'
        output_path = f'/tmp/{filename}'
        
        # PDF generieren mit Orientierung
        generate_customer_pdf(plan_data, output_path, orientation=orientation)
        
        # PDF zurücksenden
        from flask import send_file
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/excel', methods=['POST'])
def export_excel():
    """
    Exportiert Menüplan als Excel-Datei mit ausgewählten Portionen
    """
    try:
        data = request.json
        
        # Validierung
        if not data:
            return jsonify({'error': 'Keine Daten'}), 400
        
        # Extrahiere Plan
        plan_data = data.get('plan', data)  # Fallback für altes Format
        
        if 'days' not in plan_data:
            return jsonify({'error': 'Ungültige Plan-Daten'}), 400
        
        # Excel-Datei generieren
        excel_buffer = create_excel_export(plan_data)
        
        # Dateiname generieren
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'menuplan_portionen_{timestamp}.xlsx'
        
        # Excel-Datei zurücksenden
        from flask import send_file
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🚀 Starting Menüplansimulator API on port {port}")
    print(f"📊 Loaded {len(recipes)} recipes")
    print(f"🌐 Access at: http://localhost:{port}\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)




@app.route('/api/update-selection', methods=['POST'])
def update_selection():
    """
    Aktualisiert die Rezeptauswahl für eine bestimmte Mahlzeit
    
    Request JSON:
    {
        "plan": {...},  # Der vollständige Plan
        "date": "2025-01-06",
        "menu_line_id": 1,
        "cost_form_id": 1,
        "new_index": 1  # Der neue selected_index (0 oder 1)
    }
    
    Response:
    {
        "success": true,
        "plan": {...}  # Der aktualisierte Plan mit neuen Statistiken
    }
    """
    try:
        data = request.json
        
        # Validierung
        required_fields = ['plan', 'date', 'menu_line_id', 'cost_form_id', 'new_index']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        plan = data['plan']
        target_date = data['date']
        menu_line_id = data['menu_line_id']
        cost_form_id = data['cost_form_id']
        new_index = data['new_index']
        
        # Finde den entsprechenden Tag und die Mahlzeit
        updated = False
        for day in plan['days']:
            if day['date'] == target_date:
                # menu_line_id ist jetzt der Array-Index (0-basiert)
                menu_line_idx = menu_line_id
                
                if menu_line_idx < 0 or menu_line_idx >= len(day['menu_lines']):
                    return jsonify({
                        'error': f'Invalid menu_line_id: {menu_line_idx}. Must be between 0 and {len(day["menu_lines"])-1}'
                    }), 400
                
                menu_line = day['menu_lines'][menu_line_idx]
                
                if len(menu_line['recipes']) > 0:
                    recipe_slot = menu_line['recipes'][0]  # Erstes Rezept
                    
                    # Validiere den neuen Index
                    if new_index < 0 or new_index >= len(recipe_slot['options']):
                        return jsonify({
                            'error': f'Invalid index: {new_index}. Must be between 0 and {len(recipe_slot["options"])-1}'
                        }), 400
                    
                    # Aktualisiere den selected_index
                    old_index = recipe_slot['selected_index']
                    recipe_slot['selected_index'] = new_index
                    recipe_slot['is_user_modified'] = True
                    
                    # Aktualisiere die Tageskosten
                    old_cost = recipe_slot['options'][old_index]['cost_per_serving']
                    new_cost = recipe_slot['options'][new_index]['cost_per_serving']
                    day['total_cost'] = day['total_cost'] - old_cost + new_cost
                    
                    updated = True
                    break
        
        if not updated:
            return jsonify({
                'error': f'Could not find meal for date {target_date}, menu_line_idx {menu_line_id}'
            }), 404
        
        # Berechne Statistiken neu
        total_cost = sum(day['total_cost'] for day in plan['days'])
        avg_daily_cost = total_cost / len(plan['days']) if plan['days'] else 0
        
        plan['statistics']['average_bkt'] = round(avg_daily_cost, 2)
        plan['statistics']['total_cost'] = round(total_cost, 2)
        plan['statistics']['within_budget'] = (
            plan['statistics']['bkt_min'] <= avg_daily_cost <= plan['statistics']['bkt_max']
        )
        
        return jsonify({
            'success': True,
            'plan': plan
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




# Removed old save_menu_plan endpoint (duplicate)
# Removed old get_menu_plans endpoint (duplicate)
@app.route('/api/procurement/from-plans', methods=['POST'])
def get_procurement_from_plans():
    """Erstellt Beschaffungsliste aus aktiven Menüplänen"""
    try:
        data = request.get_json()
        plan_ids = data.get('plan_ids', [])
        
        plans_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'menu_plans.json')
        if not os.path.exists(plans_file):
            return jsonify({'error': 'Keine Pläne gefunden'}), 404
        
        with open(plans_file, 'r', encoding='utf-8') as f:
            data_obj = json.load(f)
        
        # Handle both old and new format
        saved_plans = data_obj.get('plans', data_obj if isinstance(data_obj, list) else [])
        
        # Filtere gewählte Pläne
        selected_plans = [p for p in saved_plans if p.get('id') in plan_ids or p.get('name') in plan_ids]
        
        # Lade Rezeptdatenbank für Zutaten
        # Konvertiere Recipe-Objekte zu Dictionaries
        from dataclasses import asdict
        recipes_db = {}
        for r in recipes:
            if hasattr(r, '__dict__'):
                # Recipe Objekt
                recipes_db[r.id] = asdict(r)
            else:
                # Bereits Dictionary
                recipes_db[r['id']] = r
        
        # Sammle alle Rezepte aus den Plänen
        all_ingredients = {}
        recipes_by_day = {}
        recipe_breakdown = {}  # Zutat -> Liste von Rezepten
        
        for plan_entry in selected_plans:
            plan = plan_entry['plan']
            for day in plan.get('days', []):
                day_date = day.get('date')
                if day_date not in recipes_by_day:
                    recipes_by_day[day_date] = []
                
                # Unterstütze beide Strukturen
                menu_items = day.get('meals', day.get('menu_lines', []))
                
                for meal in menu_items:
                    # Wenn menu_lines direkt Rezepte enthält
                    if 'recipe_id' in meal:
                        recipe_id = meal.get('recipe_id')
                        portions = meal.get('quantity') or meal.get('portions', 1)
                        recipe_data = meal
                    else:
                        # Verschachtelte Struktur mit recipes Array
                        meal_recipes = meal.get('recipes', [])
                        if not meal_recipes and 'recipe' in meal:
                            meal_recipes = [meal['recipe']]
                        
                        if not meal_recipes:
                            continue
                        
                        recipe_data = meal_recipes[0]  # Nehme erstes Rezept
                        recipe_id = recipe_data.get('id') or recipe_data.get('recipe_id')
                        portions = recipe_data.get('portions') or recipe_data.get('target_count', 1)
                    
                    # Für beide Fälle: Speichere Rezept-Info
                    recipes_by_day[day_date].append({
                        'recipe': recipe_data,
                        'portions': portions
                    })
                    
                    # Lade vollständige Rezeptdaten aus Datenbank
                    # Konvertiere recipe_id zu int falls String
                    try:
                        recipe_id_int = int(recipe_id) if recipe_id else None
                    except (ValueError, TypeError):
                        recipe_id_int = recipe_id
                    
                    full_recipe = recipes_db.get(recipe_id_int)
                    if not full_recipe:
                        continue
                    
                    # Sammle Zutaten aus vollständigem Rezept
                    for ingredient in full_recipe.get('ingredients', []):
                        ing_name = ingredient.get('name')
                        if not ing_name:
                            continue
                        
                        ing_quantity = ingredient.get('quantity', 0)
                        ing_unit = ingredient.get('unit', '')
                        lead_time = ingredient.get('lead_time', 1)
                        
                        # Berechne Bestelltag (Rezept-Tag - Lead Time)
                        from datetime import datetime, timedelta
                        recipe_date = datetime.strptime(day_date, '%Y-%m-%d')
                        order_date = (recipe_date - timedelta(days=lead_time)).strftime('%Y-%m-%d')
                        
                        if order_date not in all_ingredients:
                            all_ingredients[order_date] = {}
                        
                        if ing_name not in all_ingredients[order_date]:
                            all_ingredients[order_date][ing_name] = {
                                'name': ing_name,
                                'quantity': 0,
                                'unit': ing_unit,
                                'lead_time': lead_time,
                                'ordered': False
                            }
                        
                        all_ingredients[order_date][ing_name]['quantity'] += ing_quantity * portions
                        
                        # Speichere Rezept-Breakdown
                        if ing_name not in recipe_breakdown:
                            recipe_breakdown[ing_name] = []
                        
                        recipe_breakdown[ing_name].append({
                            'recipe_name': recipe_data.get('recipe_name') or recipe_data.get('name', 'Unbekannt'),
                            'quantity': ing_quantity * portions,
                            'unit': ing_unit,
                            'portions': portions,
                            'day': day_date
                        })
        
        # Konvertiere zu Liste
        procurement_list = []
        components_by_day = {}
        for order_date, ingredients in sorted(all_ingredients.items()):
            procurement_list.append({
                'order_date': order_date,
                'ingredients': list(ingredients.values())
            })
            # Frontend-kompatibles Format
            components_by_day[order_date] = list(ingredients.values())
        
        return jsonify({
            'success': True,
            'procurement': procurement_list,
            'components_by_day': components_by_day,
            'recipes_by_day': recipes_by_day,
            'recipe_breakdown': recipe_breakdown
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/procurement/order', methods=['POST'])
def create_order():
    """Erstellt eine Bestellung und setzt Status auf 'bestellt'"""
    try:
        data = request.get_json()
        order_items = data.get('items', [])
        
        # Speichere Bestellung
        orders_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'orders.json')
        if os.path.exists(orders_file):
            with open(orders_file, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        else:
            orders = []
        
        from datetime import datetime
        order = {
            'id': len(orders) + 1,
            'created_at': datetime.now().isoformat(),
            'items': order_items,
            'status': 'bestellt'
        }
        
        orders.append(order)
        
        os.makedirs(os.path.dirname(orders_file), exist_ok=True)
        with open(orders_file, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'message': 'Bestellung erfolgreich erstellt'
        })
    
    except Exception as e:
        import traceback

# Add this to backend/app.py

@app.route('/api/statistics/recipe-usage')
def get_recipe_usage():
    """
    Gibt Statistiken über Rezept-Verwendung zurück
    """
    try:
        # Lade gespeicherte Menüpläne
        menu_plans_file = 'data/menu_plans.json'
        if not os.path.exists(menu_plans_file):
            return jsonify({'recipes': []})
        
        with open(menu_plans_file, 'r', encoding='utf-8') as f:
            menu_plans = json.load(f)
        
        # Zähle Rezept-Verwendung
        recipe_usage = {}
        
        for plan in menu_plans:
            plan_name = plan['name']
            plan_date = plan.get('created_at', '')
            
            # Durchlaufe alle Tage und Mahlzeiten
            for day in plan.get('plan', {}).get('days', []):
                for menu_line in day.get('menu_lines', []):
                    # Prüfe ob selected_option vorhanden
                    if menu_line.get('selected_option'):
                        recipe = menu_line['selected_option']
                        recipe_id = recipe.get('id')
                        recipe_name = recipe.get('name', 'Unbekannt')
                        
                        if recipe_id:
                            if recipe_id not in recipe_usage:
                                recipe_usage[recipe_id] = {
                                    'id': recipe_id,
                                    'name': recipe_name,
                                    'usage_count': 0,
                                    'menu_plans': []
                                }
                            
                            # Prüfe ob Plan schon gezählt wurde
                            if not any(p['name'] == plan_name for p in recipe_usage[recipe_id]['menu_plans']):
                                recipe_usage[recipe_id]['usage_count'] += 1
                                recipe_usage[recipe_id]['menu_plans'].append({
                                    'name': plan_name,
                                    'date': plan_date
                                })
        
        # Sortiere nach Verwendung (absteigend)
        recipes = sorted(recipe_usage.values(), key=lambda x: x['usage_count'], reverse=True)
        
        return jsonify({'recipes': recipes})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


        traceback.print_exc()
        return jsonify({'error': str(e)}), 500






# NEU: Menüplan-Management API-Endpunkte (v5.0 - Database-based)
# Verwende ZWINGEND Datenbank-basierten Manager
from backend.menuplan_db_manager import MenuPlanDBManager, MenuPlanMetadata, OrderListMetadata

plan_manager = MenuPlanDBManager()
print("✅ Using database-based MenuPlanDBManager (REQUIRED)")

# Auto-Import beim Start
try:
    from backend.auto_import import auto_import_data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    auto_import_data(plan_manager, data_dir)
except ImportError:
    # Fallback für lokale Ausführung
    try:
        from auto_import import auto_import_data
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        auto_import_data(plan_manager, data_dir)
    except Exception as e:
        print(f"Warning: Auto-import failed: {e}")

@app.route('/api/menu-plans', methods=['GET'])
def list_menu_plans():
    """Listet alle gespeicherten Menüpläne auf"""
    try:
        status = request.args.get('status')
        plans = plan_manager.list_menu_plans(status=status)
        return jsonify({
            'success': True,
            'plans': [asdict(p) for p in plans]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/menu-plans/<plan_id>', methods=['GET'])
def get_menu_plan(plan_id):
    """Lädt einen spezifischen Menüplan"""
    try:
        plan_data = plan_manager.load_menu_plan(plan_id)
        if not plan_data:
            return jsonify({'success': False, 'error': 'Plan not found'}), 404
        return jsonify({'success': True, 'data': plan_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/menu-plans', methods=['POST'])
def save_menu_plan():
    """Speichert einen Menüplan"""
    try:
        data = request.json
        metadata = MenuPlanMetadata(**data['metadata'])
        plan_id = plan_manager.save_menu_plan(data['plan'], metadata)
        return jsonify({'success': True, 'plan_id': plan_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/menu-plans/<plan_id>/status', methods=['PUT'])
def update_plan_status(plan_id):
    """Ändert den Status eines Menüplans"""
    try:
        data = request.json
        new_status = data.get('status')
        if not new_status:
            return jsonify({'success': False, 'error': 'Missing status'}), 400
        
        success = plan_manager.update_menu_plan_status(plan_id, new_status)
        if not success:
            return jsonify({'success': False, 'error': 'Plan not found'}), 404
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/menu-plans/<plan_id>', methods=['DELETE'])
def delete_menu_plan(plan_id):
    """Löscht einen Menüplan"""
    try:
        success = plan_manager.delete_menu_plan(plan_id)
        if not success:
            return jsonify({'success': False, 'error': 'Plan not found'}), 404
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/menu-plans/<plan_id>/duplicate', methods=['POST'])
def duplicate_menu_plan(plan_id):
    """Dupliziert einen Menüplan"""
    try:
        data = request.json
        new_name = data.get('name', 'Kopie')
        new_id = plan_manager.duplicate_menu_plan(plan_id, new_name)
        if not new_id:
            return jsonify({'success': False, 'error': 'Plan not found'}), 404
        return jsonify({'success': True, 'plan_id': new_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/order-lists', methods=['GET'])
def list_order_lists():
    """Listet alle gespeicherten Bestelllisten auf"""
    try:
        orders = plan_manager.list_order_lists()
        return jsonify({
            'success': True,
            'orders': [asdict(o) for o in orders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/order-lists/<order_id>', methods=['GET'])
def get_order_list(order_id):
    """Lädt eine spezifische Bestellliste"""
    try:
        order_data = plan_manager.load_order_list(order_id)
        if not order_data:
            return jsonify({'success': False, 'error': 'Order list not found'}), 404
        return jsonify({'success': True, 'data': order_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/order-lists', methods=['POST'])
def save_order_list():
    """Speichert eine Bestellliste"""
    try:
        data = request.json
        metadata = OrderListMetadata(**data['metadata'])
        order_id = plan_manager.save_order_list(data['order_list'], metadata)
        return jsonify({'success': True, 'order_id': order_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/order-lists/<order_id>', methods=['DELETE'])
def delete_order_list(order_id):
    """Löscht eine Bestellliste"""
    try:
        success = plan_manager.delete_order_list(order_id)
        if not success:
            return jsonify({'success': False, 'error': 'Order list not found'}), 404
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/menu-plans/<plan_id>/portions', methods=['PUT'])
def update_meal_portions(plan_id):
    """Aktualisiert die Portionen für eine Mahlzeit"""
    try:
        data = request.json
        day_index = data.get('day_index')
        meal_name = data.get('meal_name')
        portions = data.get('portions', 1)
        
        if day_index is None or not meal_name:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        # Lade Plan
        plan_data = plan_manager.load_menu_plan(plan_id)
        if not plan_data:
            return jsonify({'success': False, 'error': 'Plan not found'}), 404
        
        # Aktualisiere Portionen
        plan = plan_data['plan']
        if day_index < len(plan['days']):
            day = plan['days'][day_index]
            if meal_name in day.get('meals', {}):
                day['meals'][meal_name]['portions'] = portions
                
                # Speichere zurück
                metadata = MenuPlanMetadata(**plan_data['metadata'])
                plan_manager.save_menu_plan(plan, metadata)
                
                return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Invalid day or meal'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Catch-all route for static files - MUST be last!
@app.route('/<path:path>')
def serve_static_file(path):
    """Serve any static file from frontend folder"""
    import os
    
    print(f"\n=== CATCH-ALL ROUTE CALLED ===")
    print(f"Requested path: {path}")
    print(f"static_folder: {app.static_folder}")
    print(f"static_folder (absolute): {os.path.abspath(app.static_folder)}")
    
    # Don't serve API paths
    if path.startswith('api/'):
        print(f"Rejected: API path")
        return jsonify({'error': 'API endpoint not found'}), 404
    
    full_path = os.path.join(app.static_folder, path)
    print(f"Looking for file at: {full_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    
    if os.path.exists(full_path):
        print(f"File found! Serving {path}")
    else:
        print(f"File NOT found!")
        # List directory contents
        dir_path = os.path.dirname(full_path)
        if os.path.exists(dir_path):
            print(f"Directory contents of {dir_path}:")
            try:
                files = os.listdir(dir_path)
                for f in files[:20]:  # First 20 files
                    print(f"  - {f}")
            except Exception as e:
                print(f"  Error listing directory: {e}")
    
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        print(f"ERROR serving file: {e}")
        return jsonify({'error': f'File not found: {path}', 'details': str(e)}), 404

# Deployment trigger Wed Oct 22 22:40:49 EDT 2025


# NEU: Import-Endpunkte für Menüpläne und Bestelllisten
@app.route('/api/import/menu-plans', methods=['POST'])
def import_menu_plans():
    """Importiert alle JSON-Menüpläne aus dem data/ Ordner"""
    try:
        import glob
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        pattern = os.path.join(data_dir, 'menuplan_kw*.json')
        files = glob.glob(pattern)
        
        imported = []
        errors = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Speichere via MenuPlanManager
                metadata = MenuPlanMetadata(**data['metadata'])
                plan_id = plan_manager.save_menu_plan(data['plan'], metadata)
                imported.append({
                    'file': os.path.basename(file_path),
                    'plan_id': plan_id,
                    'name': metadata.name
                })
            except Exception as e:
                errors.append({
                    'file': os.path.basename(file_path),
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'imported': len(imported),
            'errors': len(errors),
            'details': {
                'imported': imported,
                'errors': errors
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/import/order-lists', methods=['POST'])
def import_order_lists():
    """Importiert alle JSON-Bestelllisten aus dem data/ Ordner"""
    try:
        import glob
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        pattern = os.path.join(data_dir, 'orderlist_kw*.json')
        files = glob.glob(pattern)
        
        imported = []
        errors = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Erstelle OrderListMetadata
                metadata = OrderListMetadata(
                    id=data['id'],
                    name=data['name'],
                    created_at=data['created_at'],
                    menu_plan_id=data.get('menu_plan_id', ''),
                    menu_plan_name=data.get('menu_plan_name', ''),
                    start_date=data.get('start_date', ''),
                    end_date=data.get('end_date', '')
                )
                
                # Speichere via MenuPlanManager
                order_id = plan_manager.save_order_list(data['items'], metadata)
                imported.append({
                    'file': os.path.basename(file_path),
                    'order_id': order_id,
                    'name': metadata.name
                })
            except Exception as e:
                errors.append({
                    'file': os.path.basename(file_path),
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'imported': len(imported),
            'errors': len(errors),
            'details': {
                'imported': imported,
                'errors': errors
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/deployment-version')
def deployment_version():
    """Serve deployment version file for verification"""
    try:
        version_file = os.path.join(os.path.dirname(__file__), '..', 'DEPLOYMENT_VERSION.txt')
        with open(version_file, 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return f"Error reading version file: {e}", 500
