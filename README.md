# Applications Flask - Incidents Réseau

Ce repository contient deux applications Flask pour la gestion d'incidents réseau :

## 📁 Structure du projet

```
codeaz900/
├── flask-incidents-reseau/      # Version avec données en mémoire
│   ├── app.py                   # Application Flask principale
│   ├── requirements.txt         # Dépendances Python
│   ├── README.md               # Documentation
│   └── templates/              # Templates HTML
│       ├── incidents.html      # Page principale
│       ├── detail.html        # Page de détail
│       └── ajouter.html       # Formulaire d'ajout
└── flask-incidents-sqlserver/   # Version avec SQL Server
    ├── app.py                   # Application Flask avec SQLAlchemy
    ├── init_database.py         # Script d'initialisation DB
    ├── requirements.txt         # Dépendances Python
    ├── README.md               # Documentation
    ├── config_sqlserver.md     # Guide configuration SQL Server
    └── templates/              # Templates HTML
        ├── incidents.html      # Page principale
        └── detail.html        # Page de détail
```

## 🚀 Applications disponibles

### 1. Flask-Incidents-Reseau
- **Port** : 5000
- **Stockage** : Données en mémoire
- **Fonctionnalités** :
  - ✅ Affichage liste d'incidents
  - ✅ Détail des incidents
  - ✅ Ajout de nouveaux incidents
  - ✅ Interface responsive

### 2. Flask-Incidents-SQLServer
- **Port** : 5001
- **Stockage** : Base de données SQL Server on-premise
- **Fonctionnalités** :
  - ✅ Connexion SQL Server avec SQLAlchemy
  - ✅ Modèle ORM pour les incidents
  - ✅ Script d'initialisation automatique
  - ✅ API REST JSON
  - ✅ Test de connexion DB

## 📊 Modèle de données

Chaque incident contient **3 attributs principaux** :
- **titre** : Description de l'incident
- **severite** : Niveau (Critique, Élevée, Moyenne, Faible)
- **date_incident** : Horodatage de l'incident

## 🛠️ Installation rapide

### Version mémoire :
```bash
cd flask-incidents-reseau
pip install -r requirements.txt
python app.py
# Accès : http://localhost:5000
```

### Version SQL Server :

#### 📋 Prérequis SQL Server
1. **SQL Server Express** installé et démarré
2. **ODBC Driver 17 for SQL Server** installé
3. **Microsoft Visual C++ 14.0** ou plus récent

Vérifiez que SQL Server est actif :
```powershell
Get-Service -Name "*SQL*" | Where-Object {$_.Status -eq "Running"}
```

#### 🔧 Configuration et installation
```bash
cd flask-incidents-sqlserver

# 1. Installation RAPIDE avec packages pré-compilés (recommandée)
pip install --only-binary=all -r requirements.txt

# OU installation standard si pas de problème de compilation
pip install -r requirements.txt

# 2. Tester la connexion SQL Server
python test_windows_auth.py

# 3. Créer la base de données (via SSMS ou sqlcmd)
sqlcmd -S localhost\SQLEXPRESS -E -i setup_database.sql

# 4. Lancer l'application
python app.py
# Accès : http://localhost:5001
```

#### 🚀 Installation ultra-rapide (sans compilation)
Pour éviter tout problème de compilation avec Visual C++ :
```bash
cd flask-incidents-sqlserver

# Installer uniquement des versions pré-compilées
pip install --only-binary=all Flask==2.3.3
pip install --only-binary=all Flask-SQLAlchemy==2.5.1  
pip install --only-binary=all SQLAlchemy==1.4.53
pip install --only-binary=all pyodbc==4.0.39
pip install --only-binary=all Werkzeug==2.3.7

# Ou utiliser le script automatique
fix_sqlalchemy.bat
```

#### 🔐 Méthodes d'authentification

**Option 1 : Windows Authentication (Recommandée)**
- Utilise votre compte Windows actuel
- Configuration automatique dans `app.py`
- Pas de gestion de mots de passe

**Option 2 : SQL Server Authentication**
- Nécessite activation du mode mixte
- Création d'utilisateur SQL Server
- Script fourni : `enable_sql_authentication.sql`

#### ⚡ Scripts utiles disponibles
- `install_precompiled.bat/.py` : Installation rapide avec packages pré-compilés (évite Visual C++)
- `setup_database.sql` : Création complète de la base et des données
- `test_windows_auth.py` : Test de connexion
- `fix_sql_connection.py` : Diagnostic automatique des problèmes de connexion
- `check_authentication.sql` : Vérification du mode d'authentification
- `enable_sql_authentication.sql` : Activation de l'authentification SQL
- `fix_sqlalchemy.bat` : Correction automatique des versions SQLAlchemy/Python

## 🔧 Technologies utilisées

- **Flask** : Framework web Python
- **SQLAlchemy** : ORM Python (version SQL Server)
- **pyodbc** : Driver SQL Server pour Python
- **SQL Server Express** : Base de données relationnelle
- **ODBC Driver 17** : Connecteur SQL Server
- **HTML/CSS** : Interface utilisateur responsive
- **Jinja2** : Moteur de templates Flask
- **JavaScript** : Améliorations UX et validation
- **Windows Authentication** : Sécurité intégrée SQL Server

## 📚 Documentation

Consultez les README.md dans chaque dossier pour des instructions détaillées :
- [Flask-Incidents-Reseau README](flask-incidents-reseau/README.md)
- [Flask-Incidents-SQLServer README](flask-incidents-sqlserver/README.md)
- [Configuration SQL Server](flask-incidents-sqlserver/config_sqlserver.md)

## 🔍 Dépannage SQL Server

### Erreurs communes et solutions

#### ❌ "Login failed for user 'incident_user'"
**Solution :** Utilisez Windows Authentication (plus simple)
```python
# Dans app.py - Configuration Windows Auth
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=localhost\\SQLEXPRESS;"
    f"DATABASE=IncidentsReseau;"
    f"Trusted_Connection=yes;"
)
```

#### ❌ "Microsoft Visual C++ 14.0 required"
**Solutions :**
1. **Installer pyodbc pré-compilé (Recommandé)** :
   ```bash
   pip install --only-binary=all pyodbc
   ```
2. **Installation complète pré-compilée** :
   ```bash
   pip install --only-binary=all -r requirements.txt
   ```
3. **Installation depuis wheel pré-compilé** :
   ```bash
   pip install --find-links https://pypi.org/simple/ --only-binary=:all: pyodbc
   ```
4. **Alternative : Installer Microsoft C++ Build Tools** :
   - Télécharger : [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Sélectionner : "C++ build tools" + "MSVC v143" + "Windows SDK"
5. **Alternative : Visual Studio Community** (plus lourd mais complet)

**💡 Astuce :** La première option évite complètement le besoin de compiler et est la plus rapide !

#### ❌ "ODBC Driver not found"
**Solution :** Installer [ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

#### ❌ "Cannot open database IncidentsReseau"
**Solution :** Créer la base de données
```bash
sqlcmd -S localhost\SQLEXPRESS -E -i setup_database.sql
```

### 🧪 Tests de diagnostic
```bash
# Test de connexion Windows Auth
python test_windows_auth.py

# Vérification des services SQL Server
Get-Service -Name "*SQL*"

# Test de connexion via sqlcmd
sqlcmd -S localhost\SQLEXPRESS -E -Q "SELECT @@VERSION"
```

## 🚀 Déploiement

Ces applications sont prêtes pour :
- Déploiement local de développement
- Intégration avec Azure App Service
- Connexion aux bases de données Azure SQL
- Déploiement containerisé avec Docker

---

**Auteur** : Développé pour la formation AZ-900  
**Date** : Septembre 2025