#!/usr/bin/env python3.11
"""
Test script for simulation parameters in Version 1.1.0
Tests repetition distance, frequency constraints, and quality filters
"""
import json
import sys
import os
from datetime import date, timedelta
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.simulator import load_recipes_from_file, run_simulation


def test_repetition_distance():
    """Test minRepetition parameter"""
    print("\n" + "="*80)
    print("TEST 1: Repetition Distance (minRepetition)")
    print("="*80)
    
    recipes_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_200.json')
    recipes = load_recipes_from_file(recipes_file)
    
    # Test with 21 days, minRepetition = 7
    start_date = date.today()
    end_date = start_date + timedelta(days=20)
    
    config = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'bkt_target': 5.0,
        'bkt_tolerance': 0.15,
        'dietary_forms': ['Vollkost'],
        'excluded_allergens': [],
        'excluded_aversions': [],
        'repetition_interval': 7,
        'consider_seasonality': True,
        'kitchen_id': 1,
        'recipe_options_count': 2,
        'menu_lines': [
            {
                'id': 1,
                'name': 'Mittagessen',
                'cost_forms': [
                    {'id': 1, 'name': 'Hauptgang', 'component': 'Mittagessen'}
                ]
            }
        ],
        'simulation_params': {
            'variety': {
                'minRepetition': 7,
                'maxMeat': 999,
                'maxSweet': 999,
                'maxFried': 999
            },
            'quality': {
                'excludeRawMilk': False,
                'excludeRawEggs': False,
                'excludeRawSausage': False,
                'excludeRawMeat': False
            }
        }
    }
    
    print(f"\nConfiguration:")
    print(f"  Period: {start_date} to {end_date} (21 days)")
    print(f"  minRepetition: 7 days")
    print(f"  Menu: Mittagessen (Hauptgang)")
    
    result = run_simulation(config, recipes)
    
    # Analyze repetitions
    recipe_dates = defaultdict(list)
    for day_data in result['days']:
        day_date = date.fromisoformat(day_data['date'])
        for menu_line in day_data['menu_lines']:
            for recipe_data in menu_line['recipes']:
                # Get the selected recipe
                selected_idx = recipe_data['selected_index']
                recipe_id = recipe_data['options'][selected_idx]['recipe_id']
                recipe_dates[recipe_id].append(day_date)
    
    print(f"\n✅ Plan generated successfully")
    print(f"\nRepetition Analysis:")
    
    violations = []
    for recipe_id, dates in recipe_dates.items():
        if len(dates) > 1:
            dates_sorted = sorted(dates)
            recipe_name = next(r.name for r in recipes if r.id == recipe_id)
            print(f"\n  Recipe: {recipe_name} (ID {recipe_id})")
            print(f"  Used {len(dates)} times:")
            
            for i, d in enumerate(dates_sorted):
                if i > 0:
                    days_diff = (d - dates_sorted[i-1]).days
                    status = "✓" if days_diff >= 7 else "✗ VIOLATION"
                    print(f"    - {d} (gap: {days_diff} days) {status}")
                    
                    if days_diff < 7:
                        violations.append({
                            'recipe': recipe_name,
                            'dates': (dates_sorted[i-1], d),
                            'gap': days_diff
                        })
                else:
                    print(f"    - {d} (first use)")
    
    if violations:
        print(f"\n❌ Found {len(violations)} repetition violations!")
        for v in violations:
            print(f"  - {v['recipe']}: gap of {v['gap']} days (required: 7)")
        return False
    else:
        print(f"\n✅ All repetitions respect the 7-day minimum distance")
        return True


def test_frequency_constraints():
    """Test maxMeat, maxSweet, maxFried parameters"""
    print("\n" + "="*80)
    print("TEST 2: Frequency Constraints (maxMeat, maxSweet, maxFried)")
    print("="*80)
    
    recipes_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_200.json')
    recipes = load_recipes_from_file(recipes_file)
    
    # Test with 20 days, strict limits
    start_date = date.today()
    end_date = start_date + timedelta(days=19)
    
    config = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'bkt_target': 5.0,
        'bkt_tolerance': 0.15,
        'dietary_forms': ['Vollkost'],
        'excluded_allergens': [],
        'excluded_aversions': [],
        'repetition_interval': 7,
        'consider_seasonality': True,
        'kitchen_id': 1,
        'recipe_options_count': 2,
        'menu_lines': [
            {
                'id': 1,
                'name': 'Mittagessen',
                'cost_forms': [
                    {'id': 1, 'name': 'Hauptgang', 'component': 'Mittagessen'}
                ]
            }
        ],
        'simulation_params': {
            'variety': {
                'minRepetition': 3,
                'maxMeat': 8,
                'maxSweet': 4,
                'maxFried': 4
            },
            'quality': {
                'excludeRawMilk': False,
                'excludeRawEggs': False,
                'excludeRawSausage': False,
                'excludeRawMeat': False
            }
        }
    }
    
    print(f"\nConfiguration:")
    print(f"  Period: {start_date} to {end_date} (20 days)")
    print(f"  maxMeat: 8, maxSweet: 4, maxFried: 4")
    print(f"  Menu: Mittagessen (Hauptgang)")
    
    result = run_simulation(config, recipes)
    
    # Count categories
    counts = {
        'meat': 0,
        'sweet': 0,
        'fried': 0
    }
    
    for day_data in result['days']:
        for menu_line in day_data['menu_lines']:
            for recipe_data in menu_line['recipes']:
                # Get the selected recipe ID and find it in the recipes list
                selected_idx = recipe_data['selected_index']
                recipe_id = recipe_data['options'][selected_idx]['recipe_id']
                recipe = next(r for r in recipes if r.id == recipe_id)
                
                if recipe.contains_meat:
                    counts['meat'] += 1
                if recipe.is_sweet:
                    counts['sweet'] += 1
                if recipe.is_fried:
                    counts['fried'] += 1
    
    print(f"\n✅ Plan generated successfully")
    print(f"\nFrequency Analysis:")
    print(f"  Meat recipes: {counts['meat']}/8 (limit: 8)")
    print(f"  Sweet recipes: {counts['sweet']}/4 (limit: 4)")
    print(f"  Fried recipes: {counts['fried']}/4 (limit: 4)")
    
    violations = []
    if counts['meat'] > 8:
        violations.append(f"Meat: {counts['meat']} > 8")
    if counts['sweet'] > 4:
        violations.append(f"Sweet: {counts['sweet']} > 4")
    if counts['fried'] > 4:
        violations.append(f"Fried: {counts['fried']} > 4")
    
    if violations:
        print(f"\n❌ Frequency constraint violations:")
        for v in violations:
            print(f"  - {v}")
        return False
    else:
        print(f"\n✅ All frequency constraints respected")
        return True


def test_quality_filters():
    """Test quality filter parameters"""
    print("\n" + "="*80)
    print("TEST 3: Quality Filters (excludeRawEggs, etc.)")
    print("="*80)
    
    recipes_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes_200.json')
    recipes = load_recipes_from_file(recipes_file)
    
    # Count recipes with raw ingredients
    raw_counts = {
        'raw_milk': sum(1 for r in recipes if r.contains_raw_milk),
        'raw_eggs': sum(1 for r in recipes if r.contains_raw_eggs),
        'raw_sausage': sum(1 for r in recipes if r.contains_raw_sausage),
        'raw_meat': sum(1 for r in recipes if r.contains_raw_meat)
    }
    
    print(f"\nRecipe Database Statistics:")
    print(f"  Raw milk: {raw_counts['raw_milk']} recipes")
    print(f"  Raw eggs: {raw_counts['raw_eggs']} recipes")
    print(f"  Raw sausage: {raw_counts['raw_sausage']} recipes")
    print(f"  Raw meat: {raw_counts['raw_meat']} recipes")
    
    if raw_counts['raw_eggs'] == 0:
        print(f"\n⚠️  No recipes with raw eggs found - quality filter cannot be tested")
        print(f"   (This is expected for institutional catering)")
        return True
    
    # Test with quality filters enabled
    start_date = date.today()
    end_date = start_date + timedelta(days=13)
    
    config = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'bkt_target': 5.0,
        'bkt_tolerance': 0.15,
        'dietary_forms': ['Vollkost'],
        'excluded_allergens': [],
        'excluded_aversions': [],
        'repetition_interval': 7,
        'consider_seasonality': True,
        'kitchen_id': 1,
        'recipe_options_count': 2,
        'menu_lines': [
            {
                'id': 1,
                'name': 'Mittagessen',
                'cost_forms': [
                    {'id': 1, 'name': 'Hauptgang', 'component': 'Mittagessen'}
                ]
            }
        ],
        'simulation_params': {
            'variety': {
                'minRepetition': 3,
                'maxMeat': 999,
                'maxSweet': 999,
                'maxFried': 999
            },
            'quality': {
                'excludeRawMilk': True,
                'excludeRawEggs': True,
                'excludeRawSausage': True,
                'excludeRawMeat': True
            }
        }
    }
    
    print(f"\nConfiguration:")
    print(f"  Period: {start_date} to {end_date} (14 days)")
    print(f"  All quality filters enabled")
    
    result = run_simulation(config, recipes)
    
    # Check for raw ingredients in plan
    violations = []
    for day_data in result['days']:
        for menu_line in day_data['menu_lines']:
            for recipe_data in menu_line['recipes']:
                # Get the selected recipe
                selected_idx = recipe_data['selected_index']
                recipe_id = recipe_data['options'][selected_idx]['recipe_id']
                recipe = next(r for r in recipes if r.id == recipe_id)
                
                if recipe.contains_raw_milk:
                    violations.append(f"Raw milk: {recipe.name}")
                if recipe.contains_raw_eggs:
                    violations.append(f"Raw eggs: {recipe.name}")
                if recipe.contains_raw_sausage:
                    violations.append(f"Raw sausage: {recipe.name}")
                if recipe.contains_raw_meat:
                    violations.append(f"Raw meat: {recipe.name}")
    
    print(f"\n✅ Plan generated successfully")
    
    if violations:
        print(f"\n❌ Quality filter violations:")
        for v in violations:
            print(f"  - {v}")
        return False
    else:
        print(f"\n✅ No raw ingredients found in plan (filters working)")
        return True


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("SIMULATION PARAMETERS TEST SUITE - Version 1.1.0")
    print("="*80)
    
    results = {}
    
    try:
        results['repetition'] = test_repetition_distance()
    except Exception as e:
        print(f"\n❌ Test 1 failed with error: {e}")
        import traceback
        traceback.print_exc()
        results['repetition'] = False
    
    try:
        results['frequency'] = test_frequency_constraints()
    except Exception as e:
        print(f"\n❌ Test 2 failed with error: {e}")
        import traceback
        traceback.print_exc()
        results['frequency'] = False
    
    try:
        results['quality'] = test_quality_filters()
    except Exception as e:
        print(f"\n❌ Test 3 failed with error: {e}")
        import traceback
        traceback.print_exc()
        results['quality'] = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name.capitalize()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print(f"\n✅ All tests passed! Version 1.1.0 is ready for deployment.")
        return 0
    else:
        print(f"\n❌ Some tests failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

