# Application Flask - Incidents Réseau avec SQL Server

Cette application Flask se connecte à une base de données SQL Server on-premise pour afficher une liste d'incidents réseau avec 3 attributs pour chaque incident.

## 🏗️ Architecture

```
flask-incidents-sqlserver/
├── app.py                 # Application Flask avec SQLAlchemy
├── init_database.py       # Script d'initialisation de la DB
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
└── templates/            # Templates HTML
    ├── incidents.html    # Page principale avec la liste
    └── detail.html       # Page de détail d'un incident
```

## 🔧 Prérequis

### SQL Server
1. **SQL Server** installé et en cours d'exécution (Express, Developer, ou Standard)
2. **SQL Server Authentication** activée
3. **Utilisateur 'sa'** activé avec mot de passe défini
4. **ODBC Driver 17 for SQL Server** installé

### Python
- Python 3.7 ou plus récent
- pip (gestionnaire de paquets Python)

## 📊 Modèle de données

Chaque incident contient 3 attributs :
- **id** : Identifiant unique (auto-incrémenté)
- **titre** : Description de l'incident (string)
- **severite** : Niveau d'importance (Critique, Élevée, Moyenne, Faible)
- **date_incident** : Horodatage de l'incident (datetime)

## 🚀 Installation et Configuration

### 1. Installer les dépendances Python

#### 🚀 INSTALLATION RAPIDE avec packages pré-compilés (Recommandée)
Pour éviter les erreurs de compilation Visual C++ :

**Option 1 : Script automatique**
```cmd
# Installation complète automatique (recommandée)
install_precompiled.bat

# OU version Python
python install_precompiled.py
```

**Option 2 : Installation manuelle pré-compilée**
```bash
# Installation uniquement de binaires pré-compilés
pip install --only-binary=all -r requirements.txt

# OU installation package par package
pip install --only-binary=all Flask==2.3.3
pip install --only-binary=all SQLAlchemy==1.4.53  
pip install --only-binary=all Flask-SQLAlchemy==2.5.1
pip install --only-binary=all pyodbc==4.0.39
pip install --only-binary=all Werkzeug==2.3.7
```

#### ⚠️ PROBLÈME CONNU: Python 3.13 + SQLAlchemy 3.x
Si vous rencontrez l'erreur `AssertionError: Class SQLCoreOperations directly inherits TypingOnly...`:

**Solution automatique (Windows):**
```cmd
# Exécutez le script de correction
fix_sqlalchemy.bat
```

**Solution manuelle:**
```bash
cd flask-incidents-sqlserver

# 1. Désinstaller les versions problématiques
pip uninstall -y SQLAlchemy Flask-SQLAlchemy

# 2. Installer les versions compatibles
pip install SQLAlchemy==1.4.53
pip install Flask-SQLAlchemy==2.5.1
pip install Flask==2.3.3
pip install pyodbc==4.0.39
pip install Werkzeug==2.3.7
```

**Installation standard (si pas de conflit):**
```bash
cd flask-incidents-sqlserver
pip install -r requirements.txt
```

#### Option A: Configuration automatique avec le script
```bash
python init_database.py
```

#### Option B: Configuration manuelle
1. Connectez-vous à SQL Server Management Studio (SSMS)
2. Créez la base de données :
```sql
CREATE DATABASE IncidentsReseau;
```

3. Créez la table :
```sql
USE IncidentsReseau;

CREATE TABLE incidents (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titre NVARCHAR(200) NOT NULL,
    severite NVARCHAR(50) NOT NULL,
    date_incident DATETIME2 NOT NULL DEFAULT GETDATE()
);
```

4. Insérez des données d'exemple :
```sql
INSERT INTO incidents (titre, severite, date_incident) VALUES 
('Panne serveur principal', 'Critique', '2025-09-20 14:30:00'),
('Latence élevée sur le réseau', 'Moyenne', '2025-09-21 09:15:00'),
('Connexion intermittente WiFi', 'Faible', '2025-09-22 16:45:00'),
('Échec authentification VPN', 'Élevée', '2025-09-23 08:20:00'),
('Surcharge bande passante', 'Moyenne', '2025-09-23 11:10:00');
```

### 3. Configurer la connexion dans app.py

Modifiez les paramètres de connexion dans `app.py` :
```python
DB_SERVER = 'localhost'  # Votre serveur SQL Server
DB_DATABASE = 'IncidentsReseau'
DB_USERNAME = 'sa'  # Votre nom d'utilisateur
DB_PASSWORD = 'VotreMotDePasse'  # Votre mot de passe
```

### 4. Lancer l'application

```bash
python app.py
```

L'application sera accessible à : **http://localhost:5001**

## 🌐 Routes disponibles

- **/** : Page principale avec la liste des incidents
- **/incident/<id>** : Page de détail d'un incident
- **/api/incidents** : API REST retournant les incidents au format JSON
- **/test-db** : Test de connexion à la base de données

## 🔍 Dépannage

### Erreurs de connexion communes

#### 1. "Login failed for user 'sa'"
- Vérifiez que l'utilisateur 'sa' est activé
- Vérifiez le mot de passe
- Assurez-vous que SQL Server Authentication est activée

#### 2. "TCP/IP connection refused"
- Vérifiez que SQL Server est démarré
- Activez TCP/IP dans SQL Server Configuration Manager
- Vérifiez le port (1433 par défaut)

#### 3. "ODBC Driver not found"
Installez ODBC Driver 17 :
```bash
# Windows
# Téléchargez depuis Microsoft : https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

#### 4. Test de connexion
Utilisez la route de test : http://localhost:5001/test-db

## 🔐 Sécurité

⚠️ **Important** : 
- Ne jamais commiter les mots de passe dans le code
- Utilisez des variables d'environnement en production
- Configurez un utilisateur avec privilèges minimaux pour l'application

### Configuration sécurisée (recommandée)
```python
import os

DB_SERVER = os.environ.get('DB_SERVER', 'localhost')
DB_USERNAME = os.environ.get('DB_USERNAME', 'app_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
```

## 📋 Fonctionnalités

### ✅ Implémentées
- [x] Connexion SQL Server on-premise
- [x] Modèle ORM avec SQLAlchemy
- [x] Interface web responsive
- [x] API REST JSON
- [x] Gestion des erreurs
- [x] Script d'initialisation automatique
- [x] Pages de détail individuelles

### 🔄 Extensions possibles
- [ ] Authentification utilisateur
- [ ] CRUD complet (Create, Update, Delete)
- [ ] Filtres et recherche
- [ ] Pagination
- [ ] Export Excel/CSV
- [ ] Logs des actions

## 🛠️ Technologies utilisées

- **Flask** : Framework web Python
- **SQLAlchemy** : ORM Python
- **pyodbc** : Driver SQL Server pour Python
- **SQL Server** : Base de données relationnelle
- **HTML/CSS** : Interface utilisateur
- **Jinja2** : Moteur de templates

## 📚 Documentation SQL Server

- [Installation SQL Server Express](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- [ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [Configuration SQL Server Authentication](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/change-server-authentication-mode)

## 🤝 Support

Si vous rencontrez des problèmes :
1. Vérifiez les prérequis
2. Testez la connexion avec `/test-db`
3. Consultez les logs d'erreur
4. Vérifiez la configuration SQL Server

---

**Version SQL Server** - Application créée pour démontrer l'intégration Flask + SQL Server on-premise