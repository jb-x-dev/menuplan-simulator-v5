#!/usr/bin/env python3
"""
Einmalige Migration: Aktualisiere alle existierenden Menüpläne auf Menge 100

Dieses Script:
1. Lädt alle existierenden Menüpläne aus der Datenbank
2. Normalisiert alle Portionen auf 100
3. Aktualisiert die Berechnungen
4. Speichert die aktualisierten Pläne zurück
5. Erstellt ein Migrations-Log

Verwendung:
    python3 scripts/migrate_to_quantity_100.py
    python3 scripts/migrate_to_quantity_100.py --dry-run  # Nur Vorschau
"""
import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Füge backend zum Python-Path hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.menuplan_manager import MenuPlanDBManager

def normalize_plan_to_100(plan_data: dict) -> dict:
    """
    Normalisiert alle Portionen im Menüplan auf 100.
    """
    normalized = plan_data.copy()
    changes_made = 0
    
    # Durchlaufe alle Tage und Mahlzeiten
    if 'days' in normalized:
        for day in normalized['days']:
            if 'meals' in day:
                for meal in day['meals']:
                    old_portions = meal.get('portions', 80)
                    
                    # Setze Portionen auf 100
                    if old_portions != 100:
                        meal['portions'] = 100
                        changes_made += 1
                        
                        # Aktualisiere Kosten basierend auf 100 Portionen
                        if 'recipe' in meal and 'cost' in meal['recipe']:
                            recipe = meal['recipe']
                            base_cost = recipe['cost']
                            calculation_basis = recipe.get('calculation_basis', 10)
                            
                            # Berechne Kosten für 100 Portionen
                            if calculation_basis > 0:
                                cost_per_portion = base_cost / calculation_basis
                                meal['calculated_cost'] = cost_per_portion * 100
    
    return normalized, changes_made

def migrate_menu_plans(dry_run: bool = False):
    """
    Migriert alle Menüpläne zu Menge 100.
    """
    print("=" * 70)
    print("MIGRATION: Menüpläne zu Menge 100 normalisieren")
    print("=" * 70)
    print()
    
    if dry_run:
        print("⚠️  DRY-RUN Modus - Keine Änderungen werden gespeichert")
        print()
    
    # Initialisiere Manager
    manager = MenuPlanDBManager()
    
    # Hole alle Menüpläne
    print("📋 Lade alle Menüpläne...")
    all_plans = manager.list_menu_plans()
    print(f"   Gefunden: {len(all_plans)} Pläne")
    print()
    
    if len(all_plans) == 0:
        print("ℹ️  Keine Menüpläne zum Migrieren gefunden")
        return
    
    # Migrations-Statistiken
    migrated_count = 0
    skipped_count = 0
    error_count = 0
    total_changes = 0
    
    migration_log = []
    
    # Migriere jeden Plan
    for i, plan_meta in enumerate(all_plans, 1):
        print(f"[{i}/{len(all_plans)}] {plan_meta.name}")
        
        try:
            # Lade vollständigen Plan
            plan_data = manager.get_menu_plan(plan_meta.id)
            
            if not plan_data:
                print(f"   ⚠️  Plan nicht gefunden, überspringe")
                skipped_count += 1
                continue
            
            # Prüfe ob bereits migriert
            if plan_meta.normalized_portions == 100:
                print(f"   ✅ Bereits migriert (Menge 100)")
                skipped_count += 1
                continue
            
            # Normalisiere
            normalized_plan, changes = normalize_plan_to_100(plan_data)
            
            if changes == 0:
                print(f"   ℹ️  Keine Änderungen nötig")
                skipped_count += 1
                continue
            
            print(f"   🔄 {changes} Mahlzeiten aktualisiert")
            
            # Aktualisiere Metadata
            plan_meta.normalized_portions = 100
            plan_meta.normalized_at = datetime.now().isoformat()
            
            # Speichere (nur wenn nicht dry-run)
            if not dry_run:
                manager.save_menu_plan(normalized_plan, plan_meta)
                print(f"   ✅ Gespeichert")
            else:
                print(f"   ⚠️  Nicht gespeichert (Dry-Run)")
            
            migrated_count += 1
            total_changes += changes
            
            # Log-Eintrag
            migration_log.append({
                "plan_id": plan_meta.id,
                "plan_name": plan_meta.name,
                "changes": changes,
                "migrated_at": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            error_count += 1
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 70)
    print("MIGRATIONS-ZUSAMMENFASSUNG")
    print("=" * 70)
    print(f"Gesamt:      {len(all_plans)} Pläne")
    print(f"Migriert:    {migrated_count} Pläne")
    print(f"Übersprungen: {skipped_count} Pläne")
    print(f"Fehler:      {error_count} Pläne")
    print(f"Änderungen:  {total_changes} Mahlzeiten")
    print()
    
    # Speichere Migrations-Log
    if not dry_run and migrated_count > 0:
        log_file = Path(__file__).parent.parent / "data" / "migration_log.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            "migration_date": datetime.now().isoformat(),
            "migrated_plans": migrated_count,
            "total_changes": total_changes,
            "details": migration_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"📝 Migrations-Log gespeichert: {log_file}")
        print()
    
    if dry_run:
        print("⚠️  DRY-RUN abgeschlossen - Keine Änderungen wurden gespeichert")
        print("   Führe das Script ohne --dry-run aus, um zu migrieren")
    else:
        print("✅ Migration abgeschlossen!")
    
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description="Migriert alle Menüpläne zu Menge 100"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Vorschau ohne Änderungen zu speichern'
    )
    
    args = parser.parse_args()
    
    try:
        migrate_menu_plans(dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration abgebrochen durch Benutzer")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Migration fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

