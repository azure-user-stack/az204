#!/usr/bin/env python3
"""
Script de lancement de l'application Flask Incidents Azure Storage
"""

import os
import sys
import subprocess

def main():
    """Lancer l'application Flask"""
    print("🚀 Lancement de Flask Incidents Azure Storage")
    print("=" * 50)
    
    # Obtenir le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(script_dir, "app.py")
    
    print(f"📁 Répertoire: {script_dir}")
    print(f"📄 Fichier app: {app_file}")
    
    # Vérifier que app.py existe
    if not os.path.exists(app_file):
        print(f"❌ ERREUR: {app_file} non trouvé")
        return False
    
    # Changer vers le répertoire de l'application
    os.chdir(script_dir)
    print(f"✅ Répertoire de travail: {os.getcwd()}")
    
    # Lancer l'application
    print("\n🌐 Démarrage de l'application...")
    print("📍 URL: http://localhost:5004")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        # Utiliser exec plutôt que subprocess pour un meilleur contrôle
        exec(open(app_file).read())
    except KeyboardInterrupt:
        print("\n⏹️  Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    input("\n🔄 Appuyez sur Entrée pour continuer...")
    sys.exit(0 if success else 1)