"""
API-Endpunkte für Rezept-Auswahl
"""
from flask import Blueprint, request, jsonify
from backend.recipe_selection_db import (
    is_recipe_selected,
    get_selected_recipe_ids,
    get_selected_recipes_by_component,
    select_recipe,
    deselect_recipe,
    select_all_recipes,
    deselect_all_recipes,
    get_selection_count,
    get_selection_stats
)

recipe_selection_bp = Blueprint('recipe_selection', __name__)


@recipe_selection_bp.route('/api/recipe-selection/status', methods=['GET'])
def get_selection_status():
    """Gibt den Status der Rezept-Auswahl zurück"""
    try:
        selected_ids = get_selected_recipe_ids()
        stats = get_selection_stats()
        count = get_selection_count()
        
        return jsonify({
            'success': True,
            'selected_count': count,
            'selected_ids': list(selected_ids),
            'stats_by_component': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/check/<int:recipe_id>', methods=['GET'])
def check_recipe_selection(recipe_id):
    """Prüft ob ein Rezept ausgewählt ist"""
    try:
        selected = is_recipe_selected(recipe_id)
        return jsonify({'success': True, 'selected': selected})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/select', methods=['POST'])
def select_recipe_endpoint():
    """Wählt ein Rezept aus"""
    try:
        data = request.json
        recipe_id = data.get('recipe_id')
        recipe_name = data.get('recipe_name', '')
        menu_component = data.get('menu_component', 'Unknown')
        
        if not recipe_id:
            return jsonify({'success': False, 'error': 'recipe_id required'}), 400
        
        select_recipe(recipe_id, recipe_name, menu_component)
        return jsonify({'success': True, 'message': f'Recipe {recipe_id} selected'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/deselect', methods=['POST'])
def deselect_recipe_endpoint():
    """Entfernt ein Rezept aus der Auswahl"""
    try:
        data = request.json
        recipe_id = data.get('recipe_id')
        
        if not recipe_id:
            return jsonify({'success': False, 'error': 'recipe_id required'}), 400
        
        deselect_recipe(recipe_id)
        return jsonify({'success': True, 'message': f'Recipe {recipe_id} deselected'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/toggle', methods=['POST'])
def toggle_recipe_selection():
    """Togglet die Auswahl eines Rezepts"""
    try:
        data = request.json
        recipe_id = data.get('recipe_id')
        recipe_name = data.get('recipe_name', '')
        menu_component = data.get('menu_component', 'Unknown')
        
        if not recipe_id:
            return jsonify({'success': False, 'error': 'recipe_id required'}), 400
        
        if is_recipe_selected(recipe_id):
            deselect_recipe(recipe_id)
            selected = False
        else:
            select_recipe(recipe_id, recipe_name, menu_component)
            selected = True
        
        return jsonify({
            'success': True,
            'selected': selected,
            'message': f'Recipe {recipe_id} {"selected" if selected else "deselected"}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/select-all', methods=['POST'])
def select_all_endpoint():
    """Wählt alle Rezepte aus"""
    try:
        data = request.json
        recipes = data.get('recipes', [])
        
        if not recipes:
            return jsonify({'success': False, 'error': 'recipes list required'}), 400
        
        select_all_recipes(recipes)
        return jsonify({
            'success': True,
            'message': f'{len(recipes)} recipes selected'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/deselect-all', methods=['POST'])
def deselect_all_endpoint():
    """Entfernt alle Rezepte aus der Auswahl"""
    try:
        deselect_all_recipes()
        return jsonify({'success': True, 'message': 'All recipes deselected'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recipe_selection_bp.route('/api/recipe-selection/by-component/<component>', methods=['GET'])
def get_selected_by_component(component):
    """Gibt ausgewählte Rezepte für eine Komponente zurück"""
    try:
        recipe_ids = get_selected_recipes_by_component(component)
        return jsonify({
            'success': True,
            'component': component,
            'recipe_ids': recipe_ids,
            'count': len(recipe_ids)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

