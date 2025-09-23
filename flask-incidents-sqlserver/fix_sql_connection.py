"""
Script de résolution automatique des problèmes de connexion SQL Server
Teste différentes configurations et démarre les services nécessaires
"""

import subprocess
import sys
import time

def run_powershell_command(command, description, admin_required=False):
    """Exécute une commande PowerShell"""
    print(f"🔄 {description}...")
    
    if admin_required:
        print("⚠️  Cette commande nécessite des privilèges administrateur")
        # Commande pour élever les privilèges
        ps_command = f'Start-Process powershell -Verb runAs -ArgumentList "-Command", "{command}"'
    else:
        ps_command = command
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                print(f"   📄 Résultat: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Erreur")
            if result.stderr:
                print(f"   ⚠️  {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def check_and_fix_sql_services():
    """Vérifier et corriger les services SQL Server"""
    print("🔍 Diagnostic des services SQL Server\n")
    
    # 1. Vérifier l'état des services
    services_check = run_powershell_command(
        'Get-Service -Name "*SQL*" | Format-Table Name, Status -AutoSize',
        "Vérification des services SQL Server"
    )
    
    # 2. Vérifier SQLBrowser spécifiquement
    browser_status = run_powershell_command(
        'Get-Service -Name "SQLBrowser" | Select-Object -ExpandProperty Status',
        "Vérification du service SQLBrowser"
    )
    
    # 3. Démarrer SQLBrowser si nécessaire
    print("\n🔧 Tentative de démarrage de SQLBrowser...")
    browser_start = run_powershell_command(
        'Start-Service -Name "SQLBrowser"',
        "Démarrage du service SQLBrowser",
        admin_required=True
    )
    
    # 4. Vérifier les ports en écoute
    port_check = run_powershell_command(
        'netstat -an | Select-String ":1433"',
        "Vérification du port SQL Server (1433)"
    )
    
    return browser_start

def test_connection_methods():
    """Teste différentes méthodes de connexion"""
    print("\n🧪 Test des méthodes de connexion\n")
    
    # Méthodes de connexion à tester
    connection_methods = [
        ('sqlcmd -S localhost\\SQLEXPRESS -E -Q "SELECT @@SERVERNAME"', 'localhost\\SQLEXPRESS'),
        ('sqlcmd -S .\\SQLEXPRESS -E -Q "SELECT @@SERVERNAME"', '.\\SQLEXPRESS'),
        ('sqlcmd -S (local)\\SQLEXPRESS -E -Q "SELECT @@SERVERNAME"', '(local)\\SQLEXPRESS'),
        ('sqlcmd -S localhost,1433 -E -Q "SELECT @@SERVERNAME"', 'localhost,1433'),
        ('sqlcmd -S tcp:localhost,1433 -E -Q "SELECT @@SERVERNAME"', 'tcp:localhost,1433'),
    ]
    
    working_connections = []
    
    for command, server_name in connection_methods:
        print(f"🔄 Test: {server_name}")
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"   ✅ SUCCÈS: {result.stdout.strip()}")
                working_connections.append(server_name)
            else:
                print(f"   ❌ ÉCHEC")
                
        except Exception as e:
            print(f"   ❌ ERREUR: {str(e)[:50]}...")
        
        print()
    
    return working_connections

def update_app_config(working_server):
    """Met à jour la configuration de l'application"""
    if not working_server:
        return False
        
    print(f"📝 Mise à jour de la configuration avec: {working_server}")
    
    # Lire le fichier app.py actuel
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer la configuration du serveur
        old_line = "DB_SERVER = DB_CONFIGS[0]  # Configuration par défaut"
        new_line = f"DB_SERVER = '{working_server}'  # Configuration testée et fonctionnelle"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(content)
                
            print("✅ Configuration mise à jour dans app.py")
            return True
        else:
            print("⚠️  Configuration non mise à jour (structure du fichier différente)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Script de résolution des problèmes SQL Server Express")
    print("=" * 60)
    
    # Étape 1: Diagnostic et correction des services
    services_ok = check_and_fix_sql_services()
    
    # Attendre un peu que les services démarrent
    if services_ok:
        print("⏱️  Attente du démarrage des services (5 secondes)...")
        time.sleep(5)
    
    # Étape 2: Test des connexions
    working_connections = test_connection_methods()
    
    # Étape 3: Mettre à jour la configuration si nécessaire
    if working_connections:
        best_connection = working_connections[0]  # Prendre la première qui fonctionne
        print(f"\n🎉 Connexion trouvée: {best_connection}")
        
        # Mettre à jour app.py
        config_updated = update_app_config(best_connection)
        
        print(f"\n✅ Diagnostic terminé avec succès!")
        print(f"📝 Configuration recommandée: {best_connection}")
        print(f"🚀 Vous pouvez maintenant lancer: python app.py")
        
    else:
        print(f"\n❌ Aucune connexion fonctionnelle trouvée")
        print(f"\n🔧 Actions manuelles recommandées:")
        print(f"1. Ouvrir PowerShell en tant qu'administrateur")
        print(f"2. Exécuter: Start-Service -Name 'SQLBrowser'")
        print(f"3. Vérifier SQL Server Configuration Manager")
        print(f"4. Activer TCP/IP et Named Pipes")
        
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Script interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)