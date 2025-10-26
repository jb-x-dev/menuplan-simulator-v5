#!/usr/bin/env python3
"""
Erstellt 5 Menüpläne für KW 43-47 (2025) mit jeweils 50 Personen
"""
import json
import requests
from datetime import datetime, timedelta
import sys

# API Base URL
API_BASE = "http://localhost:5000"

# Kalenderwoche zu Datum konvertieren
def kw_to_date(year, week):
    """Konvertiert KW zu Start- und Enddatum"""
    # Erster Tag des Jahres
    jan_1 = datetime(year, 1, 1)
    # Finde den ersten Montag
    days_to_monday = (7 - jan_1.weekday()) % 7
    if days_to_monday == 0 and jan_1.weekday() != 0:
        days_to_monday = 7
    first_monday = jan_1 + timedelta(days=days_to_monday)
    
    # Berechne Start der gewünschten KW
    start_date = first_monday + timedelta(weeks=week-1)
    end_date = start_date + timedelta(days=6)
    
    return start_date, end_date

# Generiere Menüplan via API
def generate_menu_plan(year, week, portions=50):
    """Generiert einen Menüplan via Backend-API"""
    print(f"\n📅 Generiere Menüplan für KW {week}/{year}...")
    
    start_date, end_date = kw_to_date(year, week)
    
    # Simulationsparameter
    config = {
        "year": year,
        "start_week": week,
        "num_weeks": 1,
        "target_bkt": 8.0,
        "tolerance": 15,
        "portions": portions,
        "meal_settings": [
            {"component": "Frühstück", "enabled": True, "cost_forms": ["Vollkost"]},
            {"component": "Mittagessen", "enabled": True, "cost_forms": ["Vollkost"]},
            {"component": "Abendessen", "enabled": True, "cost_forms": ["Vollkost"]},
            {"component": "Zwischenmahlzeit", "enabled": False, "cost_forms": []}
        ],
        "dietary_forms": ["Vollkost"],
        "excluded_allergens": [],
        "mode": "auto"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/simulate", json=config, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            plan = data.get('plan', {})
            print(f"✅ Menüplan generiert: {len(plan.get('days', []))} Tage")
            print(f"   Zeitraum: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
            print(f"   Gesamtkosten: {plan.get('statistics', {}).get('total_cost', 0):.2f}€")
            print(f"   Durchschnittlicher BKT: {plan.get('statistics', {}).get('avg_bkt', 0):.2f}€")
            return plan, start_date, end_date
        else:
            print(f"❌ Fehler bei Generierung: {data.get('error', 'Unbekannter Fehler')}")
            return None, None, None
    except Exception as e:
        print(f"❌ API-Fehler: {str(e)}")
        return None, None, None

# Speichere Menüplan via API
def save_menu_plan(plan, name, start_date, end_date):
    """Speichert einen Menüplan via Backend-API"""
    print(f"\n💾 Speichere Menüplan '{name}'...")
    
    metadata = {
        "id": f"plan_{int(datetime.now().timestamp())}",
        "name": name,
        "status": "Aktiv",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "total_cost": plan.get('statistics', {}).get('total_cost', 0),
        "bkt_average": plan.get('statistics', {}).get('avg_bkt', 0),
        "description": f"Automatisch generierter Menüplan für {name}",
        "tags": ["auto-generated", name.replace(" ", "-").lower()]
    }
    
    payload = {
        "plan": plan,
        "metadata": metadata
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/menu-plans", json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            plan_id = data.get('plan_id')
            print(f"✅ Menüplan gespeichert: ID = {plan_id}")
            return plan_id
        else:
            print(f"❌ Fehler beim Speichern: {data.get('error', 'Unbekannter Fehler')}")
            return None
    except Exception as e:
        print(f"❌ API-Fehler: {str(e)}")
        return None

# Hauptprogramm
def main():
    print("🍽️  Menüplan-Generator")
    print("=" * 60)
    print("Erstelle 5 Menüpläne für KW 43-47 (2025)")
    print("Portionen: 50 pro Woche")
    print("=" * 60)
    
    year = 2025
    created_plans = []
    
    for week in range(43, 48):  # KW 43-47
        plan, start_date, end_date = generate_menu_plan(year, week, portions=50)
        
        if plan:
            name = f"KW {week}"
            plan_id = save_menu_plan(plan, name, start_date, end_date)
            
            if plan_id:
                created_plans.append({
                    "id": plan_id,
                    "name": name,
                    "week": week,
                    "start_date": start_date.strftime('%Y-%m-%d'),
                    "end_date": end_date.strftime('%Y-%m-%d')
                })
    
    print("\n" + "=" * 60)
    print(f"✅ Erfolgreich {len(created_plans)} Menüpläne erstellt!")
    print("=" * 60)
    
    for plan in created_plans:
        print(f"  • {plan['name']}: {plan['start_date']} - {plan['end_date']}")
    
    # Speichere Übersicht
    with open('/home/ubuntu/menuplan-simulator-v5/data/created_plans.json', 'w') as f:
        json.dump(created_plans, f, indent=2)
    
    print(f"\n📄 Übersicht gespeichert: data/created_plans.json")
    
    return len(created_plans)

if __name__ == "__main__":
    try:
        count = main()
        sys.exit(0 if count == 5 else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Abgebrochen durch Benutzer")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        sys.exit(1)
