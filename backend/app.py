"""
Flask API Server für Menüplansimulator
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys

# Importiere Simulator
from backend.simulator import load_recipes_from_file, run_simulation, Recipe
from backend.procurement import resolve_procurement
from backend.pdf_export import create_menu_plan_pdf
from backend.customer_pdf import generate_customer_pdf
from backend.excel_export import create_excel_export

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
# Lade Rezepte beim Start (200 Rezepte)
recipes_file_200 = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_200.json')
recipes_file_extended = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_extended.json')
recipes_file_original = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')

# Versuche 200 Rezepte zu laden, sonst Fallback
if os.path.exists(recipes_file_200):
    recipes = load_recipes_from_file(recipes_file_200)
    print(f"\u2705 Loaded {len(recipes)} recipes from 200-recipe database")
elif os.path.exists(recipes_file_extended):
    recipes = load_recipes_from_file(recipes_file_extended)
    print(f"\u2705 Loaded {len(recipes)} recipes from extended database")
else:
    recipes = load_recipes_from_file(recipes_file_original)
    print(f"\u2705 Loaded {len(recipes)} recipes from original database")


@app.route('/')
def index():
    """Serve Frontend"""
    return send_from_directory(app.static_folder, 'index.html')


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
        
        # Führe Simulation aus
        result = run_simulation(config, recipes)
        
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

