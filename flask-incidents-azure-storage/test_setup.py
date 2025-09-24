#!/usr/bin/env python3
"""
Test rapide de l'application Flask sans connexion Azure
"""

import sys
import os

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Tester les imports principaux"""
    print("🔍 Test des imports...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__} - OK")
    except ImportError as e:
        print(f"❌ Flask - ERREUR: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy - OK")
    except ImportError as e:
        print(f"❌ Flask-SQLAlchemy - ERREUR: {e}")
        return False
    
    try:
        from azure.storage.blob import BlobServiceClient
        print("✅ Azure Storage Blob - OK")
    except ImportError as e:
        print(f"❌ Azure Storage Blob - ERREUR: {e}")
        return False
    
    try:
        from azure.identity import DefaultAzureCredential
        print("✅ Azure Identity - OK")
    except ImportError as e:
        print(f"❌ Azure Identity - ERREUR: {e}")
        return False
    
    try:
        import pyodbc
        print(f"✅ PyODBC - OK")
    except ImportError as e:
        print(f"❌ PyODBC - ERREUR: {e}")
        return False
    
    return True

def test_env_file():
    """Tester le fichier .env"""
    print("\n🔧 Test du fichier .env...")
    
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ Fichier {env_file} non trouvé")
        return False
    
    print(f"✅ Fichier {env_file} trouvé")
    
    # Charger les variables d'environnement
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Variables d'environnement chargées")
    except ImportError:
        print("⚠️  python-dotenv non installé")
    
    return True

def test_flask_creation():
    """Tester la création de l'app Flask"""
    print("\n🚀 Test de création Flask...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        app.config['TESTING'] = True
        print("✅ Application Flask créée")
        return True
    except Exception as e:
        print(f"❌ Erreur création Flask: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🧪 TEST RAPIDE - Flask Incidents Azure Storage")
    print("=" * 50)
    
    tests = [
        ("Imports des modules", test_imports),
        ("Fichier de configuration", test_env_file),
        ("Création Flask", test_flask_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERREUR dans {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
        if result:
            success_count += 1
    
    print(f"\n🎯 Résultat global: {success_count}/{len(results)} tests passés")
    
    if success_count == len(results):
        print("\n🎉 Tous les tests sont passés ! L'application devrait fonctionner.")
        print("💡 Pour démarrer l'application: python app.py")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return success_count == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)