"""
Automatischer Import von Menüplänen und Bestelllisten beim Server-Start
"""
import os
import json
import glob
from typing import List, Tuple

def auto_import_data(plan_manager, data_dir: str) -> Tuple[int, int]:
    """
    Importiert automatisch Menüpläne und Bestelllisten aus dem data/ Ordner,
    falls sie noch nicht in der Datenbank vorhanden sind.
    
    Returns:
        Tuple[int, int]: (imported_plans, imported_orders)
    """
    imported_plans = 0
    imported_orders = 0
    
    try:
        # Import Menüpläne
        print("🔍 Checking for menu plans to import...")
        pattern = os.path.join(data_dir, 'menuplan_kw*.json')
        files = glob.glob(pattern)
        
        # Hole existierende Plan-IDs
        existing_plans = plan_manager.list_menu_plans()
        existing_ids = {p.id for p in existing_plans}
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                plan_id = data['metadata']['id']
                
                # Prüfe ob bereits vorhanden
                if plan_id in existing_ids:
                    print(f"  ⏭️  Skipping {data['metadata']['name']} (already exists)")
                    continue
                
                # Importiere
                from backend.menuplan_manager import MenuPlanMetadata
                metadata = MenuPlanMetadata(**data['metadata'])
                plan_manager.save_menu_plan(data['plan'], metadata)
                print(f"  ✅ Imported {metadata.name}")
                imported_plans += 1
                
            except Exception as e:
                print(f"  ❌ Error importing {os.path.basename(file_path)}: {e}")
        
        # Import Bestelllisten
        print("🔍 Checking for order lists to import...")
        pattern = os.path.join(data_dir, 'orderlist_kw*.json')
        files = glob.glob(pattern)
        
        # Hole existierende Order-IDs
        existing_orders = plan_manager.list_order_lists()
        existing_order_ids = {o.id for o in existing_orders}
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                order_id = data['id']
                
                # Prüfe ob bereits vorhanden
                if order_id in existing_order_ids:
                    print(f"  ⏭️  Skipping {data['name']} (already exists)")
                    continue
                
                # Importiere
                from backend.menuplan_manager import OrderListMetadata
                metadata = OrderListMetadata(
                    id=data['id'],
                    name=data['name'],
                    created_at=data['created_at'],
                    menu_plan_id=data.get('menu_plan_id', ''),
                    menu_plan_name=data.get('menu_plan_name', ''),
                    start_date=data.get('start_date', ''),
                    end_date=data.get('end_date', '')
                )
                plan_manager.save_order_list(data['items'], metadata)
                print(f"  ✅ Imported {metadata.name}")
                imported_orders += 1
                
            except Exception as e:
                print(f"  ❌ Error importing {os.path.basename(file_path)}: {e}")
        
        if imported_plans > 0 or imported_orders > 0:
            print(f"\n✅ Auto-import completed: {imported_plans} menu plans, {imported_orders} order lists")
        else:
            print("✅ No new data to import (all up to date)")
        
    except Exception as e:
        print(f"❌ Auto-import failed: {e}")
    
    return imported_plans, imported_orders

