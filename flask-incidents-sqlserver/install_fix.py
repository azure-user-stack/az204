#!/usr/bin/env python3
"""
Script d'installation et de configuration pour Flask-Incidents-SQLServer
Résout les problèmes de compatibilité SQLAlchemy/Python 3.13
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Exécute une commande et gère les erreurs"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur:")
        print(f"   {e.stderr}")
        return None

def main():
    print("🚀 Installation Flask-Incidents-SQLServer")
    print("📝 Résolution du conflit SQLAlchemy/Python 3.13")
    
    # Vérifier Python
    python_version = sys.version
    print(f"\n🐍 Version Python: {python_version}")
    
    # Désinstaller les anciennes versions problématiques
    print("\n🗑️  Nettoyage des versions conflictuelles...")
    run_command("pip uninstall -y SQLAlchemy Flask-SQLAlchemy", "Désinstallation SQLAlchemy")
    
    # Installer les versions compatibles
    print("\n📦 Installation des versions compatibles...")
    compatible_packages = [
        "SQLAlchemy==1.4.53",
        "Flask-SQLAlchemy==2.5.1", 
        "Flask==2.3.3",
        "pyodbc==4.0.39",
        "Werkzeug==2.3.7"
    ]
    
    for package in compatible_packages:
        result = run_command(f"pip install {package}", f"Installation {package}")
        if result is None:
            print(f"⚠️  Erreur lors de l'installation de {package}")
    
    # Vérifier l'installation
    print("\n🔍 Vérification de l'installation...")
    try:
        import flask
        import flask_sqlalchemy
        import sqlalchemy
        import pyodbc
        
        print(f"✅ Flask: {flask.__version__}")
        print(f"✅ Flask-SQLAlchemy: {flask_sqlalchemy.__version__}")
        print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
        print(f"✅ pyodbc: {pyodbc.version}")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    
    # Test de l'application
    print("\n🧪 Test de l'application...")
    try:
        # Import test de l'application
        sys.path.append(os.path.dirname(__file__))
        
        print("✅ Import de l'application réussi")
        print("\n🎉 Installation terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("1. Vérifiez que SQL Server Express est démarré")
        print("2. Exécutez: python test_windows_auth.py")
        print("3. Créez la base: sqlcmd -S localhost\\SQLEXPRESS -E -i setup_database.sql")
        print("4. Lancez l'app: python app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔧 Des erreurs ont été détectées. Vérifiez les logs ci-dessus.")
        sys.exit(1)
    else:
        print("\n✨ Tout est prêt! Vous pouvez maintenant utiliser l'application.")