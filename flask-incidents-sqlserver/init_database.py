"""
Script d'initialisation de la base de données SQL Server
pour l'application Flask Incidents Réseau

Exécutez ce script pour :
1. Créer la base de données IncidentsReseau
2. Créer la table incidents
3. Insérer les données d'exemple

Prérequis :
- SQL Server installé et en cours d'exécution
- Utilisateur sa activé avec mot de passe configuré
- ou un utilisateur avec les privilèges CREATE DATABASE
"""

import pyodbc
from datetime import datetime

# Configuration de connexion (modifiez selon votre environnement)
SERVER = 'localhost'  # ou l'adresse IP de votre serveur SQL Server
USERNAME = 'sa'
PASSWORD = 'YourPassword123!'  # Remplacez par votre mot de passe
DATABASE = 'IncidentsReseau'

def create_database():
    """Créer la base de données IncidentsReseau si elle n'existe pas"""
    try:
        # Connexion à la base master pour créer la DB
        conn_str = f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={SERVER};
            DATABASE=master;
            UID={USERNAME};
            PWD={PASSWORD};
            TrustServerCertificate=yes;
        """
        
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute("""
            SELECT database_id 
            FROM sys.databases 
            WHERE Name = ?
        """, DATABASE)
        
        if cursor.fetchone() is None:
            print(f"Création de la base de données {DATABASE}...")
            cursor.execute(f"CREATE DATABASE {DATABASE}")
            print(f"Base de données {DATABASE} créée avec succès !")
        else:
            print(f"Base de données {DATABASE} existe déjà.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erreur lors de la création de la base : {e}")
        return False

def create_table_and_insert_data():
    """Créer la table incidents et insérer les données d'exemple"""
    try:
        # Connexion à la base IncidentsReseau
        conn_str = f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={SERVER};
            DATABASE={DATABASE};
            UID={USERNAME};
            PWD={PASSWORD};
            TrustServerCertificate=yes;
        """
        
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Créer la table incidents
        print("Création de la table incidents...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='incidents' AND xtype='U')
            CREATE TABLE incidents (
                id INT IDENTITY(1,1) PRIMARY KEY,
                titre NVARCHAR(200) NOT NULL,
                severite NVARCHAR(50) NOT NULL,
                date_incident DATETIME2 NOT NULL DEFAULT GETDATE()
            )
        """)
        
        # Vérifier si des données existent
        cursor.execute("SELECT COUNT(*) FROM incidents")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Insertion des données d'exemple...")
            
            # Données d'exemple
            incidents_data = [
                ('Panne serveur principal', 'Critique', '2025-09-20 14:30:00'),
                ('Latence élevée sur le réseau', 'Moyenne', '2025-09-21 09:15:00'),
                ('Connexion intermittente WiFi', 'Faible', '2025-09-22 16:45:00'),
                ('Échec authentification VPN', 'Élevée', '2025-09-23 08:20:00'),
                ('Surcharge bande passante', 'Moyenne', '2025-09-23 11:10:00')
            ]
            
            for titre, severite, date_str in incidents_data:
                cursor.execute("""
                    INSERT INTO incidents (titre, severite, date_incident)
                    VALUES (?, ?, ?)
                """, titre, severite, date_str)
            
            print(f"Insertion de {len(incidents_data)} incidents terminée !")
        else:
            print(f"Table incidents contient déjà {count} enregistrements.")
        
        # Vérification des données
        cursor.execute("SELECT id, titre, severite, date_incident FROM incidents")
        rows = cursor.fetchall()
        
        print("\n=== Données dans la table incidents ===")
        print("ID | Titre | Sévérité | Date")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erreur lors de la création de la table/insertion : {e}")
        return False

def test_connection():
    """Tester la connexion à SQL Server"""
    try:
        conn_str = f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={SERVER};
            DATABASE=master;
            UID={USERNAME};
            PWD={PASSWORD};
            TrustServerCertificate=yes;
        """
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print("=== Test de connexion réussi ! ===")
        print(f"Version SQL Server : {version[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erreur de connexion à SQL Server : {e}")
        print("\nVérifiez :")
        print("1. Que SQL Server est démarré")
        print("2. Que l'utilisateur 'sa' est activé")
        print("3. Que le mot de passe est correct")
        print("4. Que ODBC Driver 17 for SQL Server est installé")
        return False

if __name__ == '__main__':
    print("=== Initialisation de la base de données ===\n")
    
    # 1. Test de connexion
    if not test_connection():
        exit(1)
    
    # 2. Création de la base
    if not create_database():
        exit(1)
    
    # 3. Création table et données
    if not create_table_and_insert_data():
        exit(1)
    
    print("\n=== Initialisation terminée avec succès ! ===")
    print("Vous pouvez maintenant lancer l'application Flask avec : python app.py")