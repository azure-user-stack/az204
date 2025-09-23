#!/usr/bin/env python3
"""
Installation automatique de Flask-SQLServer avec packages pré-compilés
Évite les problèmes de compilation Microsoft Visual C++ 14.0
"""

import subprocess
import sys
import os

def run_pip_command(package, description):
    """Installe un package avec --only-binary=all"""
    print(f"📌 {description}...")
    
    cmd = [sys.executable, "-m", "pip", "install", "--only-binary=all", package]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"   ✅ {package} installé avec succès")
            return True
        else:
            print(f"   ❌ Erreur lors de l'installation de {package}")
            print(f"   📄 Erreur: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  Timeout lors de l'installation de {package}")
        return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def verify_imports():
    """Vérifie que tous les modules peuvent être importés"""
    print("\n✅ Vérification des installations...")
    
    modules_to_test = [
        ("flask", "Flask"),
        ("sqlalchemy", "SQLAlchemy"), 
        ("flask_sqlalchemy", "Flask-SQLAlchemy"),
        ("pyodbc", "pyodbc")
    ]
    
    all_ok = True
    
    for module_name, display_name in modules_to_test:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'version non disponible')
            print(f"   ✅ {display_name}: {version}")
        except ImportError as e:
            print(f"   ❌ {display_name}: Import failed - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Fonction principale d'installation"""
    print("🚀 Installation Flask-SQLServer avec packages pré-compilés")
    print("=" * 60)
    print("💡 Cette méthode évite les problèmes Visual C++ 14.0")
    print("⚡ Installation uniquement de wheels (packages pré-compilés)")
    print()
    
    # Packages à installer dans l'ordre
    packages = [
        ("Flask==2.3.3", "Installation Flask"),
        ("SQLAlchemy==1.4.53", "Installation SQLAlchemy"),
        ("Flask-SQLAlchemy==2.5.1", "Installation Flask-SQLAlchemy"),
        ("pyodbc==4.0.39", "Installation pyodbc (CRITIQUE)"),
        ("Werkzeug==2.3.7", "Installation Werkzeug")
    ]
    
    # Désinstallation optionnelle des versions existantes
    print("🔧 Nettoyage des versions existantes...")
    subprocess.run([
        sys.executable, "-m", "pip", "uninstall", "-y", 
        "Flask", "Flask-SQLAlchemy", "SQLAlchemy", "pyodbc", "Werkzeug"
    ], capture_output=True)
    
    print("\n📦 Installation des packages pré-compilés...")
    
    # Installation de chaque package
    failed_packages = []
    for package, description in packages:
        success = run_pip_command(package, description)
        if not success:
            failed_packages.append(package)
    
    # Vérification des imports
    imports_ok = verify_imports()
    
    # Résultats finaux
    print("\n" + "=" * 60)
    if not failed_packages and imports_ok:
        print("🎉 Installation terminée avec SUCCÈS!")
        print("\n📋 Prochaines étapes:")
        print("   1. Vérifiez SQL Server: Get-Service -Name '*SQL*'")
        print("   2. Testez la connexion: python test_windows_auth.py")
        print("   3. Lancez l'application: python app.py")
        
    else:
        print("⚠️  Installation terminée avec des problèmes:")
        if failed_packages:
            print("   ❌ Packages non installés:", ", ".join(failed_packages))
        if not imports_ok:
            print("   ❌ Certains modules ne peuvent pas être importés")
        
        print("\n🔧 Solutions de dépannage:")
        print("   1. Essayez: pip install --find-links https://pypi.org/simple/ --only-binary=:all: pyodbc")
        print("   2. Vérifiez votre connexion internet")
        print("   3. Mettez à jour pip: python -m pip install --upgrade pip")
        
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\nAppuyez sur Entrée pour fermer...")
            sys.exit(1)
        else:
            input("\nInstallation réussie! Appuyez sur Entrée pour fermer...")
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)