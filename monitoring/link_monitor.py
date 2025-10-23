#!/usr/bin/env python3
"""
Link Monitoring Script für Menüplansimulator
Überprüft regelmäßig alle wichtigen URLs und meldet Fehler
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

# Basis-URL (kann über Umgebungsvariable überschrieben werden)
BASE_URL = "https://menuplan-simulator-v5.onrender.com"

# URLs die überwacht werden sollen
MONITORED_URLS = [
    {"path": "/", "name": "Landing Page", "critical": True},
    {"path": "/index.html", "name": "Hauptanwendung", "critical": True},
    {"path": "/order-lists.html", "name": "Bestelllisten", "critical": True},
    {"path": "/meal-plans.html", "name": "Menüpläne", "critical": True},
    {"path": "/recipes.html", "name": "Rezeptverwaltung", "critical": True},
    {"path": "/analytics.html", "name": "Analytics", "critical": False},
    {"path": "/procurement.html", "name": "Beschaffung", "critical": False},
    {"path": "/api/health", "name": "Health Check API", "critical": True},
]

# API-Endpunkte die getestet werden sollen
API_ENDPOINTS = [
    {"path": "/api/recipes", "method": "GET", "name": "Rezepte API", "critical": True},
    {"path": "/api/config/example", "method": "GET", "name": "Beispiel-Konfiguration", "critical": False},
]


class LinkMonitor:
    """Überwacht Links und API-Endpunkte"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results = []
        
    def check_url(self, url_info: Dict) -> Tuple[bool, int, str]:
        """
        Überprüft eine einzelne URL
        
        Returns:
            (success, status_code, message)
        """
        url = f"{self.base_url}{url_info['path']}"
        try:
            response = requests.get(url, timeout=10)
            success = response.status_code == 200
            return success, response.status_code, "OK" if success else f"HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return False, 0, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, 0, "Connection Error"
        except Exception as e:
            return False, 0, str(e)
    
    def check_api(self, api_info: Dict) -> Tuple[bool, int, str]:
        """
        Überprüft einen API-Endpunkt
        
        Returns:
            (success, status_code, message)
        """
        url = f"{self.base_url}{api_info['path']}"
        try:
            if api_info['method'] == 'GET':
                response = requests.get(url, timeout=10)
            elif api_info['method'] == 'POST':
                response = requests.post(url, json={}, timeout=10)
            else:
                return False, 0, f"Unsupported method: {api_info['method']}"
            
            success = 200 <= response.status_code < 300
            return success, response.status_code, "OK" if success else f"HTTP {response.status_code}"
        except Exception as e:
            return False, 0, str(e)
    
    def run_checks(self) -> Dict:
        """
        Führt alle Checks durch
        
        Returns:
            Dictionary mit Ergebnissen
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "urls": [],
            "apis": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "critical_failed": 0
            }
        }
        
        # URL-Checks
        print(f"\n🔍 Überprüfe URLs auf {self.base_url}...")
        for url_info in MONITORED_URLS:
            success, status_code, message = self.check_url(url_info)
            
            result = {
                "name": url_info['name'],
                "path": url_info['path'],
                "critical": url_info['critical'],
                "success": success,
                "status_code": status_code,
                "message": message
            }
            results["urls"].append(result)
            results["summary"]["total"] += 1
            
            if success:
                results["summary"]["passed"] += 1
                print(f"  ✅ {url_info['name']}: {status_code}")
            else:
                results["summary"]["failed"] += 1
                if url_info['critical']:
                    results["summary"]["critical_failed"] += 1
                    print(f"  ❌ {url_info['name']}: {message} (CRITICAL)")
                else:
                    print(f"  ⚠️  {url_info['name']}: {message}")
        
        # API-Checks
        print(f"\n🔍 Überprüfe API-Endpunkte...")
        for api_info in API_ENDPOINTS:
            success, status_code, message = self.check_api(api_info)
            
            result = {
                "name": api_info['name'],
                "path": api_info['path'],
                "method": api_info['method'],
                "critical": api_info['critical'],
                "success": success,
                "status_code": status_code,
                "message": message
            }
            results["apis"].append(result)
            results["summary"]["total"] += 1
            
            if success:
                results["summary"]["passed"] += 1
                print(f"  ✅ {api_info['name']}: {status_code}")
            else:
                results["summary"]["failed"] += 1
                if api_info['critical']:
                    results["summary"]["critical_failed"] += 1
                    print(f"  ❌ {api_info['name']}: {message} (CRITICAL)")
                else:
                    print(f"  ⚠️  {api_info['name']}: {message}")
        
        return results
    
    def print_summary(self, results: Dict):
        """Gibt eine Zusammenfassung aus"""
        summary = results["summary"]
        print(f"\n{'='*60}")
        print(f"📊 ZUSAMMENFASSUNG")
        print(f"{'='*60}")
        print(f"Gesamt:           {summary['total']}")
        print(f"✅ Erfolgreich:   {summary['passed']}")
        print(f"❌ Fehlgeschlagen: {summary['failed']}")
        print(f"🚨 Kritisch:      {summary['critical_failed']}")
        print(f"{'='*60}\n")
        
        if summary['critical_failed'] > 0:
            print("⚠️  WARNUNG: Kritische Fehler gefunden!")
            return False
        elif summary['failed'] > 0:
            print("⚠️  Einige nicht-kritische Fehler gefunden")
            return True
        else:
            print("✅ Alle Checks erfolgreich!")
            return True
    
    def save_results(self, results: Dict, filename: str = "monitoring_results.json"):
        """Speichert Ergebnisse in JSON-Datei"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📝 Ergebnisse gespeichert in: {filename}")


def main():
    """Hauptfunktion"""
    import sys
    import os
    
    # Basis-URL aus Umgebungsvariable oder Argument
    base_url = os.environ.get('MONITOR_BASE_URL', BASE_URL)
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"🚀 Starte Link-Monitoring für: {base_url}")
    print(f"⏰ Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    monitor = LinkMonitor(base_url)
    results = monitor.run_checks()
    success = monitor.print_summary(results)
    
    # Speichere Ergebnisse
    monitor.save_results(results)
    
    # Exit-Code: 0 = success, 1 = failure
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

