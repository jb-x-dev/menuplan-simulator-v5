def run_simulation(config_dict: Dict, recipes: List[Recipe]) -> Dict:
    """Führt Simulation aus"""
    # Debug logging
    print(f"DEBUG run_simulation - dietary_forms: {config_dict.get('dietary_forms')}")
    print(f"DEBUG run_simulation - menu_lines count: {len(config_dict.get('menu_lines', []))}")
    if config_dict.get('menu_lines'):
        for ml in config_dict['menu_lines']:
            print(f"DEBUG menu_line: {ml['name']}, cost_forms: {len(ml.get('cost_forms', []))}")
            for cf in ml.get('cost_forms', []):
                print(f"  DEBUG cost_form: {cf['name']}, component: {cf.get('component')}")
    
    config = SimulatorConfig(**config_dict)
    simulator = MenuPlanSimulator(config, recipes)
    return simulator.generate_plan()


