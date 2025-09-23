import pyodbc
import sys

def test_sql_server_connections():
    """Test différentes méthodes de connexion à SQL Server Express"""
    
    test_configs = [
        {
            'name': 'localhost\\SQLEXPRESS avec TCP/IP',
            'server': 'localhost\\SQLEXPRESS',
            'protocol': ''
        },
        {
            'name': '.\\SQLEXPRESS avec Named Pipes',
            'server': '.\\SQLEXPRESS',
            'protocol': ''
        },
        {
            'name': 'localhost\\SQLEXPRESS,1433 avec TCP/IP',
            'server': 'localhost\\SQLEXPRESS,1433',
            'protocol': ''
        },
        {
            'name': '(local)\\SQLEXPRESS',
            'server': '(local)\\SQLEXPRESS',
            'protocol': ''
        },
        {
            'name': 'localhost avec TCP/IP forcé',
            'server': 'tcp:localhost\\SQLEXPRESS',
            'protocol': ''
        }
    ]
    
    print("🔍 Test de connexions SQL Server Express\n")
    
    successful_configs = []
    
    for config in test_configs:
        print(f"🔄 Test: {config['name']}")
        
        try:
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={config['server']};"
                f"DATABASE=master;"  # On teste avec master d'abord
                f"Trusted_Connection=yes;"
                f"Connection Timeout=5;"
            )
            
            print(f"   📝 Connection: {config['server']}")
            
            conn = pyodbc.connect(connection_string, timeout=5)
            cursor = conn.cursor()
            
            # Test simple
            cursor.execute("SELECT @@SERVERNAME, @@VERSION")
            result = cursor.fetchone()
            
            print(f"   ✅ SUCCÈS!")
            print(f"   🖥️  Serveur: {result[0]}")
            print(f"   📚 Version: {result[1][:80]}...")
            
            successful_configs.append({
                'config': config,
                'connection_string': connection_string
            })
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"   ❌ ÉCHEC: {str(e)[:100]}...")
        
        print()
    
    # Résultats
    print("=" * 50)
    if successful_configs:
        print("🎉 Connexions réussies:")
        for i, success in enumerate(successful_configs, 1):
            print(f"\n{i}. {success['config']['name']}")
            print(f"   Server: {success['config']['server']}")
        
        # Recommandation
        best_config = successful_configs[0]
        print(f"\n💡 Configuration recommandée:")
        print(f"   DB_SERVER = '{best_config['config']['server']}'")
        
        return best_config['config']['server']
    else:
        print("❌ Aucune connexion réussie!")
        print("\n🔧 Solutions à essayer:")
        print("1. Vérifier que SQL Server Browser est démarré:")
        print("   Get-Service -Name 'SQLBrowser'")
        print("2. Activer TCP/IP dans SQL Server Configuration Manager")
        print("3. Vérifier le port (par défaut 1433)")
        print("4. Redémarrer les services SQL Server")
        
        return None

def test_database_creation(server):
    """Test de création de base de données"""
    if not server:
        return False
        
    print(f"\n🗃️  Test de création de base IncidentsReseau...")
    
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE=master;"
            f"Trusted_Connection=yes;"
        )
        
        conn = pyodbc.connect(connection_string)
        conn.autocommit = True  # Important pour CREATE DATABASE
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'IncidentsReseau'")
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✅ Base 'IncidentsReseau' existe déjà")
        else:
            print("🔧 Création de la base 'IncidentsReseau'...")
            cursor.execute("CREATE DATABASE IncidentsReseau")
            print("✅ Base 'IncidentsReseau' créée avec succès")
        
        cursor.close()
        conn.close()
        
        # Test de connexion à la nouvelle base
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE=IncidentsReseau;"
            f"Trusted_Connection=yes;"
        )
        
        conn = pyodbc.connect(connection_string)
        print("✅ Connexion à IncidentsReseau réussie")
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Diagnostic complet SQL Server Express\n")
    
    # Test des connexions
    working_server = test_sql_server_connections()
    
    if working_server:
        # Test de création de base
        db_ok = test_database_creation(working_server)
        
        if db_ok:
            print(f"\n🎉 Configuration complète réussie!")
            print(f"📝 Utilisez cette configuration dans app.py:")
            print(f"   DB_SERVER = '{working_server}'")
            print(f"\n🚀 Vous pouvez maintenant lancer: python app.py")
        else:
            print(f"\n⚠️  Connexion OK mais problème de base de données")
    else:
        print(f"\n🔧 Résolvez les problèmes de connexion avant de continuer")
        sys.exit(1)