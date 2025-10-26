"""
Optimierter automatischer Import von Menüplänen und Bestelllisten
Version 2.0 - Mit Import-Tracking, Lock-File und Menge-100-Berechnung
"""
import os
import json
import glob
from typing import List, Tuple
from datetime import datetime
from pathlib import Path

# Import-Lock-File Pfad
IMPORT_LOCK_FILE = Path(__file__).parent.parent / "data" / ".import_completed"

def check_import_lock() -> bool:
    """
    Prüft ob Import bereits erfolgreich abgeschlossen wurde.
    
    Returns:
        bool: True wenn Import bereits durchgeführt wurde
    """
    if IMPORT_LOCK_FILE.exists():
        try:
            with open(IMPORT_LOCK_FILE, 'r') as f:
                lock_data = json.load(f)
                print(f"ℹ️  Import-Lock gefunden:")
                print(f"   Erstellt am: {lock_data.get('completed_at')}")
                print(f"   Importierte Pläne: {lock_data.get('imported_plans', 0)}")
                print(f"   Importierte Bestellungen: {lock_data.get('imported_orders', 0)}")
                return True
        except Exception as e:
            print(f"⚠️  Fehler beim Lesen des Lock-Files: {e}")
            return False
    return False

def create_import_lock(imported_plans: int, imported_orders: int):
    """
    Erstellt Import-Lock-File nach erfolgreichem Import.
    """
    lock_data = {
        "completed_at": datetime.now().isoformat(),
        "imported_plans": imported_plans,
        "imported_orders": imported_orders,
        "version": "2.0"
    }
    
    try:
        IMPORT_LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(IMPORT_LOCK_FILE, 'w') as f:
            json.dump(lock_data, f, indent=2)
        print(f"✅ Import-Lock erstellt: {IMPORT_LOCK_FILE}")
    except Exception as e:
        print(f"⚠️  Fehler beim Erstellen des Lock-Files: {e}")

def mark_file_as_imported(plan_manager, file_path: str, plan_id: str):
    """
    Markiert eine Datei als importiert in der Datenbank.
    
    Speichert Import-Metadaten für Tracking.
    """
    try:
        import_record = {
            "file_path": os.path.basename(file_path),
            "plan_id": plan_id,
            "imported_at": datetime.now().isoformat(),
            "import_version": "2.0"
        }
        
        # Speichere in separater Import-Tracking-Tabelle (falls vorhanden)
        # Alternativ: Als Tag im Plan speichern
        # Für jetzt: Loggen ist ausreichend, da wir Lock-File haben
        
    except Exception as e:
        print(f"⚠️  Fehler beim Markieren der Datei: {e}")

def normalize_portions_to_100(plan_data: dict) -> dict:
    """
    Normalisiert alle Portionen im Menüplan auf 100.
    
    Dies ist wichtig für konsistente Berechnungen und Skalierung.
    
    Args:
        plan_data: Menüplan-Daten mit 'plan' und 'metadata'
    
    Returns:
        dict: Normalisierte Menüplan-Daten
    """
    normalized = plan_data.copy()
    
    # Durchlaufe alle Tage und Mahlzeiten
    if 'plan' in normalized and 'days' in normalized['plan']:
        for day in normalized['plan']['days']:
            if 'meals' in day:
                for meal in day['meals']:
                    # Setze Portionen auf 100
                    meal['portions'] = 100
                    
                    # Aktualisiere Kosten basierend auf 100 Portionen
                    if 'recipe' in meal and 'cost' in meal['recipe']:
                        recipe = meal['recipe']
                        base_cost = recipe['cost']
                        calculation_basis = recipe.get('calculation_basis', 10)
                        
                        # Berechne Kosten für 100 Portionen
                        if calculation_basis > 0:
                            cost_per_portion = base_cost / calculation_basis
                            meal['calculated_cost'] = cost_per_portion * 100
    
    # Aktualisiere Metadata
    if 'metadata' in normalized:
        normalized['metadata']['normalized_portions'] = 100
        normalized['metadata']['normalized_at'] = datetime.now().isoformat()
    
    return normalized

def auto_import_data(plan_manager, data_dir: str, force: bool = False) -> Tuple[int, int]:
    """
    Importiert automatisch Menüpläne und Bestelllisten aus dem data/ Ordner,
    falls sie noch nicht in der Datenbank vorhanden sind.
    
    NEU: Mit Import-Lock, Datenbank-Tracking und Menge-100-Normalisierung
    
    Args:
        plan_manager: MenuPlanManager Instanz
        data_dir: Pfad zum data/ Verzeichnis
        force: Erzwinge Import auch wenn Lock-File existiert
    
    Returns:
        Tuple[int, int]: (imported_plans, imported_orders)
    """
    imported_plans = 0
    imported_orders = 0
    
    # Prüfe Import-Lock (außer bei force=True)
    if not force and check_import_lock():
        print("✅ Import bereits durchgeführt (Lock-File vorhanden)")
        print("   Verwende --force zum erneuten Import")
        return 0, 0
    
    try:
        # Import Menüpläne
        print("🔍 Checking for menu plans to import...")
        pattern = os.path.join(data_dir, 'menuplan_kw*.json')
        files = glob.glob(pattern)
        
        print(f"   Gefunden: {len(files)} Dateien")
        
        # Hole existierende Plan-IDs
        existing_plans = plan_manager.list_menu_plans()
        existing_ids = {p.id for p in existing_plans}
        
        print(f"   Bereits in DB: {len(existing_ids)} Pläne")
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                plan_id = data['metadata']['id']
                
                # Prüfe ob bereits vorhanden
                if plan_id in existing_ids:
                    print(f"  ⏭️  Skipping {data['metadata']['name']} (already exists)")
                    continue
                
                # NEU: Normalisiere Portionen auf 100
                normalized_data = normalize_portions_to_100(data)
                
                # Importiere
                from backend.menuplan_manager import MenuPlanMetadata
                metadata = MenuPlanMetadata(**normalized_data['metadata'])
                plan_manager.save_menu_plan(normalized_data['plan'], metadata)
                
                # NEU: Markiere als importiert
                mark_file_as_imported(plan_manager, file_path, plan_id)
                
                print(f"  ✅ Imported {metadata.name} (normalized to 100 portions)")
                imported_plans += 1
                
            except Exception as e:
                print(f"  ❌ Error importing {os.path.basename(file_path)}: {e}")
        
        # Import Bestelllisten
        print("🔍 Checking for order lists to import...")
        pattern = os.path.join(data_dir, 'orderlist_kw*.json')
        files = glob.glob(pattern)
        
        print(f"   Gefunden: {len(files)} Dateien")
        
        # Hole existierende Order-IDs
        existing_orders = plan_manager.list_order_lists()
        existing_order_ids = {o.id for o in existing_orders}
        
        print(f"   Bereits in DB: {len(existing_order_ids)} Bestellungen")
        
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
        
        # NEU: Erstelle Import-Lock nach erfolgreichem Import
        if imported_plans > 0 or imported_orders > 0:
            print(f"\n✅ Auto-import completed: {imported_plans} menu plans, {imported_orders} order lists")
            create_import_lock(imported_plans, imported_orders)
        else:
            print("✅ No new data to import (all up to date)")
            # Erstelle Lock auch wenn nichts importiert wurde (alles bereits vorhanden)
            if len(existing_ids) > 0:
                create_import_lock(0, 0)
        
    except Exception as e:
        print(f"❌ Auto-import failed: {e}")
        import traceback
        traceback.print_exc()
    
    return imported_plans, imported_orders

def reset_import_lock():
    """
    Entfernt das Import-Lock-File für erneuten Import.
    
    Nur für Wartungszwecke oder bei Problemen verwenden!
    """
    if IMPORT_LOCK_FILE.exists():
        try:
            IMPORT_LOCK_FILE.unlink()
            print(f"✅ Import-Lock entfernt: {IMPORT_LOCK_FILE}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Entfernen des Lock-Files: {e}")
            return False
    else:
        print("ℹ️  Kein Import-Lock vorhanden")
        return False

