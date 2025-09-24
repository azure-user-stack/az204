# 📁 Flask Incidents Réseau avec Azure Storage

> Application Flask moderne pour la gestion d'incidents réseau avec upload de documents dans Azure Blob Storage

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Azure](https://img.shields.io/badge/Azure-SQL%20%2B%20Storage-blue.svg)](https://azure.microsoft.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

## 📋 Aperçu

Cette application Flask permet de gérer les incidents réseau avec la possibilité d'attacher des documents qui sont automatiquement stockés dans Azure Blob Storage. Elle utilise Azure SQL Database pour les métadonnées et Azure Blob Storage pour le stockage des fichiers.

### ✨ Fonctionnalités principales

- 🔥 **Gestion d'incidents** : Créer, consulter et gérer des incidents réseau
- 📎 **Upload de documents** : Attacher des fichiers aux incidents (PDF, Word, Excel, images, etc.)
- ☁️ **Azure Blob Storage** : Stockage sécurisé et scalable des documents
- 🗄️ **Azure SQL Database** : Base de données cloud pour les métadonnées
- 📱 **Interface responsive** : Design moderne avec Bootstrap 5
- 🔍 **Recherche et filtres** : Recherche textuelle et filtres par sévérité/documents
- 📊 **API REST** : Endpoints JSON pour intégration externe
- 🏥 **Health checks** : Surveillance de l'état de l'application et des services Azure
- 🎨 **Interface moderne** : Design professionnel avec animations CSS

## 🏗️ Architecture

```
Flask Application
├── Frontend (HTML/CSS/JS)
│   ├── Bootstrap 5 UI
│   ├── Responsive Design
│   └── JavaScript Interactions
├── Backend (Python/Flask)
│   ├── SQLAlchemy ORM
│   ├── Azure SDK Integration
│   └── RESTful API
├── Azure SQL Database
│   ├── Incidents Table
│   └── Documents Metadata Table
└── Azure Blob Storage
    └── Document Files Storage
```

## 📦 Installation et Configuration

### 1. Prérequis

- **Python 3.12+** installé
- **Compte Azure** avec accès aux services suivants :
  - Azure SQL Database
  - Azure Blob Storage
- **Git** pour cloner le projet
- **Visual Studio Code** (recommandé)

### 2. Cloner le projet

```bash
git clone https://github.com/votre-username/flask-incidents-azure-storage.git
cd flask-incidents-azure-storage
```

### 3. Environnement virtuel Python

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate
```

### 4. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 5. Configuration Azure

#### 5.1. Créer les ressources Azure

**Option A: Via le portail Azure**
1. Connectez-vous au [portail Azure](https://portal.azure.com)
2. Créez un **Groupe de ressources** (ex: `incidents-rg`)
3. Créez une **Azure SQL Database** :
   - Nom du serveur : `incidents-server-[unique]`
   - Base de données : `IncidentsReseau`
   - Configuration : Basic ou Standard
4. Créez un **Compte de stockage** :
   - Nom : `incidentsstorage[unique]`
   - Type : General Purpose v2
   - Réplication : LRS (Local Redundant Storage)

**Option B: Via Azure CLI**
```bash
# Créer le groupe de ressources
az group create --name incidents-rg --location francecentral

# Créer le serveur SQL
az sql server create \
  --name incidents-server-unique \
  --resource-group incidents-rg \
  --location francecentral \
  --admin-user adminuser \
  --admin-password \"ComplexPassword123!\"

# Créer la base de données
az sql db create \
  --resource-group incidents-rg \
  --server incidents-server-unique \
  --name IncidentsReseau \
  --service-objective Basic

# Créer le compte de stockage
az storage account create \
  --name incidentsstorageunique \
  --resource-group incidents-rg \
  --location francecentral \
  --sku Standard_LRS
```

#### 5.2. Configuration du firewall SQL

```bash
# Autoriser votre IP actuelle
az sql server firewall-rule create \
  --resource-group incidents-rg \
  --server incidents-server-unique \
  --name AllowMyIP \
  --start-ip-address [VOTRE_IP] \
  --end-ip-address [VOTRE_IP]

# Autoriser les services Azure
az sql server firewall-rule create \
  --resource-group incidents-rg \
  --server incidents-server-unique \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### 6. Configuration de l'application

```bash
# Copier le fichier d'exemple
copy .env.example .env

# Éditer le fichier .env avec vos valeurs
notepad .env
```

**Exemple de fichier .env :**
```env
# Flask
FLASK_SECRET_KEY=your-super-secret-key-here
FLASK_PORT=5004
FLASK_DEBUG=True

# Azure SQL Database
AZURE_SQL_SERVER=incidents-server-unique.database.windows.net
AZURE_SQL_DATABASE=IncidentsReseau
AZURE_SQL_USERNAME=adminuser
AZURE_SQL_PASSWORD=ComplexPassword123!

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT_NAME=incidentsstorageunique
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key-here
AZURE_STORAGE_CONTAINER_NAME=incident-documents
```

### 7. Test de la configuration

```bash
# Tester la connexion SQL
python -c "from app import db; db.create_all(); print('✅ Connexion SQL réussie')"

# Tester la connexion Storage
python -c "from app import create_blob_service_client; client = create_blob_service_client(); print('✅ Connexion Storage réussie' if client else '❌ Erreur Storage')"
```

## 🚀 Utilisation

### Démarrage de l'application

```bash
python app.py
```

L'application sera accessible sur : http://localhost:5004

### Interface utilisateur

#### 📊 **Page d'accueil** - `/`
- Vue d'ensemble des incidents avec statistiques
- Filtres par sévérité et présence de documents
- Recherche textuelle dans les titres et descriptions
- Cards colorées selon la sévérité

#### ➕ **Créer un incident** - `/ajouter`
- Formulaire avec titre, description et sévérité
- Upload multiple de fichiers (jusqu'à 16 MB par fichier)
- Types supportés : PDF, Word, Excel, images, archives, etc.
- Aperçu des fichiers sélectionnés avant soumission

#### 🔍 **Détail incident** - `/incident/<id>`
- Informations complètes de l'incident
- Liste des documents avec icônes selon le type
- Téléchargement et suppression de documents
- Statistiques des fichiers attachés

### API REST

#### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/incidents` | Liste tous les incidents avec compteurs de documents |
| GET | `/api/incidents/<id>` | Détail d'un incident avec ses documents |
| GET | `/health` | Health check de l'application et services Azure |
| GET | `/storage-test` | Test détaillé de la connexion Azure Storage |

#### Exemples d'utilisation

```bash
# Lister tous les incidents
curl http://localhost:5004/api/incidents

# Détail d'un incident
curl http://localhost:5004/api/incidents/1

# Health check
curl http://localhost:5004/health
```

## 📁 Types de fichiers supportés

### 📄 Documents
- **PDF** : `.pdf`
- **Word** : `.doc`, `.docx`
- **Texte** : `.txt`, `.md`, `.rtf`

### 🖼️ Images
- **Standard** : `.jpg`, `.jpeg`, `.png`, `.gif`
- **Avancé** : `.bmp`, `.tiff`

### 📊 Tableurs
- **Excel** : `.xls`, `.xlsx`
- **CSV** : `.csv`

### 📈 Présentations
- **PowerPoint** : `.ppt`, `.pptx`

### 📦 Archives
- **Compression** : `.zip`, `.rar`, `.7z`

### 💾 Autres
- **Data** : `.json`, `.xml`, `.log`

## 🏗️ Architecture technique

### Structure du projet

```
flask-incidents-azure-storage/
├── app.py                          # Application Flask principale
├── requirements.txt                # Dépendances Python
├── .env.example                   # Exemple de configuration
├── README.md                      # Documentation
├── templates/                     # Templates Jinja2
│   ├── layout.html               #   Template de base
│   ├── incidents.html           #   Liste des incidents
│   ├── ajouter.html             #   Formulaire d'ajout
│   └── detail.html              #   Détail incident
├── static/                        # Ressources statiques
│   └── css/
│       └── style.css            #   Styles personnalisés
└── venv/                         # Environnement virtuel (git-ignoré)
```

### Modèles de données

#### Table `incidents`
```sql
CREATE TABLE incidents (
    id INT PRIMARY KEY IDENTITY(1,1),
    titre NVARCHAR(200) NOT NULL,
    description NTEXT,
    severite NVARCHAR(50) NOT NULL DEFAULT 'Moyenne',
    date_incident DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    date_creation DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    date_modification DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
```

#### Table `incident_documents`
```sql
CREATE TABLE incident_documents (
    id INT PRIMARY KEY IDENTITY(1,1),
    incident_id INT NOT NULL,
    filename NVARCHAR(255) NOT NULL,
    blob_name NVARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    content_type NVARCHAR(100) NOT NULL,
    upload_date DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    uploaded_by NVARCHAR(100) DEFAULT 'System',
    FOREIGN KEY (incident_id) REFERENCES incidents(id)
);
```

### Intégration Azure

#### Azure SQL Database
- **SQLAlchemy** : ORM pour interactions base de données
- **ODBC Driver 18** : Pilote pour connexions SQL Server
- **Connection String** : Configuration sécurisée via variables d'environnement

#### Azure Blob Storage
- **BlobServiceClient** : Client officiel Azure pour Python
- **Conteneurs** : Organisation des fichiers par incident
- **Métadonnées** : Informations sur les fichiers stockées en SQL
- **Sécurité** : Accès via clés de compte ou Managed Identity

## 🔧 Configuration avancée

### Variables d'environnement complètes

```env
# Configuration Flask
FLASK_SECRET_KEY=your-secret-key
FLASK_PORT=5004
FLASK_DEBUG=False

# Azure SQL Database
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=IncidentsReseau
AZURE_SQL_USERNAME=admin-user
AZURE_SQL_PASSWORD=complex-password
AZURE_ODBC_DRIVER=ODBC Driver 18 for SQL Server
AZURE_ENCRYPT=yes
AZURE_TRUST_SERVER_CERTIFICATE=no
AZURE_CONNECTION_TIMEOUT=30

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER_NAME=incident-documents
```

### Sécurité en production

#### 🔒 Recommandations de sécurité

1. **Secrets Management**
   ```bash
   # Utiliser Azure Key Vault
   az keyvault create --name incidents-kv --resource-group incidents-rg
   az keyvault secret set --vault-name incidents-kv --name sql-password --value \"ComplexPassword123!\"
   ```

2. **Managed Identity** (recommandé pour la production)
   ```python
   from azure.identity import DefaultAzureCredential
   credential = DefaultAzureCredential()
   blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
   ```

3. **Firewall SQL restrictif**
   ```bash
   # Autoriser seulement les IPs spécifiques
   az sql server firewall-rule create --resource-group incidents-rg --server your-server --name CompanyNetwork --start-ip-address 203.0.113.0 --end-ip-address 203.0.113.255
   ```

4. **HTTPS uniquement**
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   app.config['SESSION_COOKIE_HTTPONLY'] = True
   ```

## 🐳 Déploiement

### Option 1: Azure App Service

```bash
# Créer l'App Service
az webapp create \
  --resource-group incidents-rg \
  --plan incidents-plan \
  --name incidents-app-unique \
  --runtime \"PYTHON|3.12\"

# Configurer les variables d'environnement
az webapp config appsettings set \
  --resource-group incidents-rg \
  --name incidents-app-unique \
  --settings FLASK_SECRET_KEY=\"your-secret\" AZURE_SQL_SERVER=\"your-server.database.windows.net\"

# Déployer depuis Git
az webapp deployment source config \
  --resource-group incidents-rg \
  --name incidents-app-unique \
  --repo-url https://github.com/your-username/flask-incidents-azure-storage.git \
  --branch main
```

### Option 2: Conteneur Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD [\"gunicorn\", \"--bind\", \"0.0.0.0:5000\", \"app:app\"]
```

```bash
# Construire l'image
docker build -t flask-incidents .

# Exécuter le conteneur
docker run -p 5000:5000 --env-file .env flask-incidents
```

## 🧪 Tests et validation

### Tests manuels

1. **Créer un incident**
   - Aller sur `/ajouter`
   - Remplir le formulaire
   - Attacher des fichiers de différents types
   - Vérifier la création

2. **Consulter les détails**
   - Cliquer sur un incident
   - Vérifier les informations affichées
   - Télécharger un document
   - Supprimer un document

3. **Tester les filtres**
   - Utiliser la barre de recherche
   - Filtrer par sévérité
   - Filtrer par présence de documents

### Tests API

```bash
# Test de la liste d'incidents
curl -H \"Accept: application/json\" http://localhost:5004/api/incidents

# Test du health check
curl http://localhost:5004/health

# Test Azure Storage
curl http://localhost:5004/storage-test
```

### Tests de charge

```python
import requests
import concurrent.futures

def test_endpoint(url):
    response = requests.get(url)
    return response.status_code

# Test concurrent
urls = [\"http://localhost:5004/\" for _ in range(10)]
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(test_endpoint, urls))
    
print(f\"Succès: {results.count(200)}/{len(results)}\")
```

## 📊 Monitoring et maintenance

### Health checks

L'application fournit plusieurs endpoints pour le monitoring :

- **`/health`** : État global (base de données + stockage)
- **`/storage-test`** : Test détaillé d'Azure Storage
- **Application Insights** : Intégration possible pour le monitoring Azure

### Logs et debugging

```python
import logging

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('incidents.log'),
        logging.StreamHandler()
    ]
)
```

### Sauvegarde

1. **Base de données Azure SQL**
   ```bash
   az sql db export \
     --resource-group incidents-rg \
     --server your-server \
     --name IncidentsReseau \
     --admin-user adminuser \
     --admin-password \"ComplexPassword123!\" \
     --storage-key \"your-storage-key\" \
     --storage-key-type StorageAccessKey \
     --storage-uri \"https://yourstorageaccount.blob.core.windows.net/backups/incidents-backup.bacpac\"
   ```

2. **Azure Blob Storage**
   - Configuration de la réplication géographique
   - Snapshots automatiques des blobs
   - Politiques de rétention

## 🤝 Contribution

### Développement local

1. Fork du projet
2. Créer une branche feature : `git checkout -b feature/nouvelle-fonctionnalite`
3. Faire les modifications
4. Tester les changements
5. Commit : `git commit -m \"Ajout nouvelle fonctionnalité\"`
6. Push : `git push origin feature/nouvelle-fonctionnalite`
7. Créer une Pull Request

### Standards de code

- **PEP 8** : Respect des conventions Python
- **Type hints** : Utilisation des annotations de type
- **Docstrings** : Documentation des fonctions
- **Tests** : Couverture de code minimale

## 🆘 Dépannage

### Problèmes courants

#### 1. Erreur de connexion SQL Database

```
OperationalError: ('08001', '[08001] [Microsoft][ODBC Driver 18 for SQL Server]...')
```

**Solutions :**
- Vérifier les règles de firewall Azure SQL
- Tester la connectivité réseau
- Vérifier les identifiants dans `.env`

#### 2. Erreur Azure Blob Storage

```
ClientAuthenticationError: The request authorization credentials are invalid
```

**Solutions :**
- Vérifier la clé de stockage Azure
- Vérifier le nom du compte de stockage
- Tester avec Azure Storage Explorer

#### 3. Erreur d'upload de fichier

```
RequestEntityTooLarge: The request entity body is too large
```

**Solutions :**
- Vérifier la taille du fichier (max 16 MB)
- Configurer `MAX_CONTENT_LENGTH` dans Flask
- Optimiser les images avant upload

### Debug mode

```bash
# Activer le debug détaillé
export FLASK_DEBUG=True
export PYTHONPATH=\".\"
python app.py
```

### Logs utiles

```bash
# Logs Azure SQL
SELECT TOP 10 * FROM sys.dm_exec_requests WHERE status = 'running';

# Logs Azure Storage via Azure CLI
az storage blob list --account-name your-account --container-name incident-documents
```

## 📚 Ressources

### Documentation officielle

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure SQL Database](https://docs.microsoft.com/azure/azure-sql/database/)
- [Azure Blob Storage](https://docs.microsoft.com/azure/storage/blobs/)
- [SQLAlchemy](https://sqlalchemy.org/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)

### Tutoriels et guides

- [Python on Azure](https://docs.microsoft.com/azure/developer/python/)
- [Flask + Azure SQL](https://docs.microsoft.com/azure/app-service/tutorial-python-postgresql-app)
- [Azure Storage SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Développement initial* - [VotreGitHub](https://github.com/votre-username)

## 🙏 Remerciements

- Microsoft Azure pour les services cloud
- Flask community pour le framework web
- Bootstrap team pour l'interface utilisateur
- SQLAlchemy pour l'ORM Python

---

## 📞 Support

Pour toute question ou problème :

1. 📖 Consultez d'abord cette documentation
2. 🔍 Recherchez dans les [Issues GitHub](https://github.com/votre-username/flask-incidents-azure-storage/issues)
3. 🆕 Créez une nouvelle issue si nécessaire
4. 💬 Discutez dans les [Discussions GitHub](https://github.com/votre-username/flask-incidents-azure-storage/discussions)

---

*Application développée avec ❤️ pour la gestion moderne des incidents réseau*