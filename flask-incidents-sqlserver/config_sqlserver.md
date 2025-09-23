# Configuration de SQL Server pour l'Application Flask

## Guide de Configuration SQL Server on-premise

### 1. Installation de SQL Server Express (gratuit)

#### Windows:
1. Téléchargez SQL Server Express : https://www.microsoft.com/en-us/sql-server/sql-server-downloads
2. Exécutez l'installateur
3. Choisissez "Installation personnalisée"
4. Cochez "Services moteur de base de données"
5. **Important** : Sélectionnez "Mode d'authentification mixte" et définissez un mot de passe pour 'sa'

### 2. Configuration post-installation

#### Activer SQL Server Authentication:
1. Ouvrez **SQL Server Management Studio (SSMS)**
2. Connectez-vous avec authentification Windows
3. Clic droit sur le serveur → **Propriétés**
4. Section **Sécurité** → Authentification du serveur → **Mode d'authentification SQL Server et Windows**
5. Redémarrez le service SQL Server

#### Activer l'utilisateur 'sa':
1. Dans SSMS, allez à **Sécurité** → **Connexions** → **sa**
2. Clic droit → **Propriétés**
3. Onglet **Général** → Définissez un mot de passe fort
4. Onglet **État** → **Connexion : Activé**

### 3. Configuration réseau

#### Activer TCP/IP:
1. Ouvrez **SQL Server Configuration Manager**
2. **Protocoles réseau pour SQLEXPRESS** → **TCP/IP**
3. Clic droit → **Activer**
4. Propriétés → **Adresses IP** → **IPAll** → **Port TCP : 1433**
5. Redémarrez le service SQL Server

### 4. Vérification des ports et firewall

```cmd
# Vérifier que SQL Server écoute sur le port 1433
netstat -an | find "1433"

# Si nécessaire, autoriser dans le firewall Windows
netsh advfirewall firewall add rule name="SQLServer" dir=in action=allow protocol=TCP localport=1433
```

## Installation ODBC Driver 17

### Windows:
Téléchargez et installez depuis : https://go.microsoft.com/fwlink/?linkid=2249006

### Vérification:
```cmd
# Dans PowerShell
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}
```

## Scripts de test SQL

### Test de connexion basique:
```sql
-- Dans SSMS, tester la connexion
SELECT @@VERSION;
SELECT @@SERVERNAME;
SELECT name FROM sys.databases;
```

### Création manuelle de la base et table:
```sql
-- Créer la base de données
CREATE DATABASE IncidentsReseau;
GO

-- Utiliser la base
USE IncidentsReseau;
GO

-- Créer la table
CREATE TABLE incidents (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titre NVARCHAR(200) NOT NULL,
    severite NVARCHAR(50) NOT NULL CHECK (severite IN ('Critique', 'Élevée', 'Moyenne', 'Faible')),
    date_incident DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- Insérer des données de test
INSERT INTO incidents (titre, severite, date_incident) VALUES 
('Panne serveur principal', 'Critique', '2025-09-20 14:30:00'),
('Latence élevée sur le réseau', 'Moyenne', '2025-09-21 09:15:00'),
('Connexion intermittente WiFi', 'Faible', '2025-09-22 16:45:00'),
('Échec authentification VPN', 'Élevée', '2025-09-23 08:20:00'),
('Surcharge bande passante', 'Moyenne', '2025-09-23 11:10:00');
GO

-- Vérifier les données
SELECT * FROM incidents;
```

## Paramètres de connexion types

### Configuration locale standard:
```python
DB_SERVER = 'localhost'  # ou .\SQLEXPRESS
DB_DATABASE = 'IncidentsReseau'
DB_USERNAME = 'sa'
DB_PASSWORD = 'YourPassword123!'
```

### Configuration avec instance nommée:
```python
DB_SERVER = 'localhost\SQLEXPRESS'
```

### Configuration réseau:
```python
DB_SERVER = '192.168.1.100'  # IP du serveur
# ou
DB_SERVER = 'SERVER-NAME'  # Nom du serveur
```

## Dépannage courant

### Erreur: "Login failed for user 'sa'"
```sql
-- Vérifier l'état de l'utilisateur sa
SELECT name, is_disabled, create_date, modify_date 
FROM sys.server_principals 
WHERE name = 'sa';

-- Réactiver si nécessaire
ALTER LOGIN [sa] ENABLE;
ALTER LOGIN [sa] WITH PASSWORD = 'NewPassword123!';
```

### Erreur: "TCP/IP connection refused"
1. Vérifiez que le service SQL Server est démarré
2. Vérifiez la configuration TCP/IP
3. Testez avec telnet : `telnet localhost 1433`

### Erreur: "Cannot open database"
```sql
-- Vérifier l'existence de la base
SELECT name FROM sys.databases WHERE name = 'IncidentsReseau';

-- Si elle n'existe pas, la créer
CREATE DATABASE IncidentsReseau;
```

## Services Windows à vérifier

1. **SQL Server (SQLEXPRESS)** ou **SQL Server (MSSQLSERVER)**
2. **SQL Server Browser** (si instances nommées)
3. **SQL Server Agent** (optionnel)

```cmd
# Vérifier les services
sc query MSSQL$SQLEXPRESS
# ou
sc query MSSQLSERVER

# Démarrer si nécessaire
net start MSSQL$SQLEXPRESS
```

## Test de connexion Python

```python
# Test simple de connexion
import pyodbc

def test_connection():
    try:
        conn_str = """
            DRIVER={ODBC Driver 17 for SQL Server};
            SERVER=localhost;
            DATABASE=master;
            UID=sa;
            PWD=YourPassword123!;
            TrustServerCertificate=yes;
        """
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Connexion réussie: {version}")
        
    except Exception as e:
        print(f"Erreur: {e}")

test_connection()
```