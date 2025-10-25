"""
API-Endpunkt für Versions-Informationen
"""
import os

def get_version():
    """Liest Version aus VERSION Datei"""
    version_file = os.path.join(os.path.dirname(__file__), '..', 'VERSION')
    try:
        with open(version_file, 'r') as f:
            version = f.read().strip()
            return version
    except FileNotFoundError:
        return "5.0.0"  # Fallback
    except Exception as e:
        print(f"Error reading version: {e}")
        return "unknown"

