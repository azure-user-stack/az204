import pyodbc
import sys

def test_windows_auth():
    """Test de connexion avec Windows Authentication"""
    try:
        # Configuration pour Windows Authentication
        server = 'localhost\\SQLEXPRESS'
        database = 'master'  # On teste d'abord avec la DB master
        
        connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
        )
        
        print("🔄 Test de connexion avec Windows Authentication...")
        print(f"📝 Serveur: {server}")
        
        conn = pyodbc.connect(connection_string, timeout=10)
        cursor = conn.cursor()
        
        # Test de base
        cursor.execute("SELECT @@SERVERNAME, DB_NAME(), SYSTEM_USER")
        result = cursor.fetchone()
        
        print("✅ Connexion Windows Authentication réussie !")
        print(f"🖥️  Serveur: {result[0]}")
        print(f"💾 Base courante: {result[1]}")
        print(f"👤 Utilisateur: {result[2]}")
        
        # Vérifier si la base IncidentsReseau existe
        cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'IncidentsReseau'")
        db_exists = cursor.fetchone()[0]
        
        if db_exists:
            print("✅ Base de données 'IncidentsReseau' trouvée")
            
            # Test de connexion à la base IncidentsReseau
            cursor.execute("USE IncidentsReseau")
            cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'incidents'")
            table_exists = cursor.fetchone()[0]
            
            if table_exists:
                print("✅ Table 'incidents' trouvée")
                cursor.execute("SELECT COUNT(*) FROM incidents")
                count = cursor.fetchone()[0]
                print(f"📊 Nombre d'incidents: {count}")
            else:
                print("⚠️  Table 'incidents' non trouvée - exécutez le script setup_database.sql")
        else:
            print("⚠️  Base 'IncidentsReseau' non trouvée - exécutez le script setup_database.sql")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\n🔍 Vérifications à faire:")
        print("1. SQL Server Express est-il démarré ?")
        print("2. ODBC Driver 17 est-il installé ?")
        print("3. Le nom du serveur est-il correct ?")
        return False

if __name__ == "__main__":
    success = test_windows_auth()
    if success:
        print(f"\n🎉 Votre configuration est prête !")
        print(f"🚀 Vous pouvez maintenant lancer l'application Flask")
    else:
        print(f"\n🔧 Résolvez les problèmes avant de continuer")