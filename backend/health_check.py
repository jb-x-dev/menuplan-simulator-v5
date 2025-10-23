"""
Health Check Module für Menüplansimulator
Stellt Health-Check-Endpunkte bereit
"""

import os
import sys
from datetime import datetime
from flask import jsonify


def register_health_routes(app):
    """Registriert Health-Check-Routen in der Flask-App"""
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Basis Health Check
        Gibt den Status der Anwendung zurück
        """
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'menuplan-simulator',
            'version': '1.0.0'
        })
    
    @app.route('/api/health/detailed', methods=['GET'])
    def detailed_health_check():
        """
        Detaillierter Health Check
        Überprüft verschiedene Komponenten
        """
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'menuplan-simulator',
            'version': '1.0.0',
            'checks': {}
        }
        
        # Check: Rezepte geladen
        try:
            from backend.app import recipes
            health_status['checks']['recipes'] = {
                'status': 'healthy',
                'count': len(recipes),
                'message': f'{len(recipes)} recipes loaded'
            }
        except Exception as e:
            health_status['checks']['recipes'] = {
                'status': 'unhealthy',
                'message': str(e)
            }
            health_status['status'] = 'degraded'
        
        # Check: Static Files
        try:
            static_folder = app.static_folder
            static_exists = os.path.exists(static_folder)
            
            if static_exists:
                # Zähle HTML-Dateien
                html_files = [f for f in os.listdir(static_folder) if f.endswith('.html')]
                health_status['checks']['static_files'] = {
                    'status': 'healthy',
                    'folder': static_folder,
                    'html_files_count': len(html_files),
                    'html_files': html_files
                }
            else:
                health_status['checks']['static_files'] = {
                    'status': 'unhealthy',
                    'message': f'Static folder not found: {static_folder}'
                }
                health_status['status'] = 'unhealthy'
        except Exception as e:
            health_status['checks']['static_files'] = {
                'status': 'unhealthy',
                'message': str(e)
            }
            health_status['status'] = 'degraded'
        
        # Check: Kritische Dateien
        critical_files = [
            'index.html',
            'order-lists.html',
            'meal-plans.html',
            'recipes.html',
            'landing.html'
        ]
        
        missing_files = []
        for filename in critical_files:
            filepath = os.path.join(app.static_folder, filename)
            if not os.path.exists(filepath):
                missing_files.append(filename)
        
        if missing_files:
            health_status['checks']['critical_files'] = {
                'status': 'unhealthy',
                'missing': missing_files,
                'message': f'{len(missing_files)} critical files missing'
            }
            health_status['status'] = 'unhealthy'
        else:
            health_status['checks']['critical_files'] = {
                'status': 'healthy',
                'message': 'All critical files present'
            }
        
        # Check: Python Version
        health_status['checks']['python'] = {
            'status': 'healthy',
            'version': sys.version,
            'executable': sys.executable
        }
        
        return jsonify(health_status)
    
    @app.route('/api/health/files', methods=['GET'])
    def list_static_files():
        """
        Listet alle statischen Dateien auf
        Hilfreich für Debugging
        """
        try:
            static_folder = app.static_folder
            files = []
            
            for root, dirs, filenames in os.walk(static_folder):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    relpath = os.path.relpath(filepath, static_folder)
                    files.append({
                        'path': relpath,
                        'size': os.path.getsize(filepath),
                        'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    })
            
            return jsonify({
                'static_folder': static_folder,
                'total_files': len(files),
                'files': sorted(files, key=lambda x: x['path'])
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

