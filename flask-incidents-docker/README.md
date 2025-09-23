# Flask Incidents Réseau - Version Docker 🐳

## 📖 Description

Application Flask containerisée pour la gestion d'incidents réseau, optimisée pour le déploiement sur Azure Container Registry et Azure Container Instances.

## 🏗️ Architecture

```
flask-incidents-docker/
├── app.py                    # Application Flask avec health checks
├── Dockerfile               # Configuration Docker optimisée
├── docker-compose.yml       # Développement local
├── requirements.txt         # Dépendances Python
├── container-instance.yml   # Template Azure Container Instances
├── deploy-azure.ps1         # Script de déploiement PowerShell
├── deploy-azure.sh          # Script de déploiement Bash
├── .github/workflows/       # CI/CD GitHub Actions
│   └── deploy.yml
├── templates/               # Templates HTML avec thème Docker
│   ├── base.html
│   ├── incidents.html
│   ├── detail.html
│   └── ajouter.html
├── static/                  # Ressources statiques
└── DEPLOYMENT_GUIDE.md      # Guide complet de déploiement
```

## 🚀 Démarrage Rapide

### Option 1: Déploiement Azure (Recommandé)
```powershell
# Clone et déploiement automatique
git clone <votre-repo>
cd flask-incidents-docker
.\deploy-azure.ps1
```

### Option 2: Développement Local
```bash
# Avec Docker Compose
docker-compose up -d

# Ou directement avec Docker
docker build -t flask-incidents .
docker run -p 5000:80 flask-incidents
```

### Option 3: Installation Python
```bash
pip install -r requirements.txt
python app.py
```

## 🔧 Configuration

### Variables d'Environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `FLASK_ENV` | Environnement Flask | `production` |
| `FLASK_DEBUG` | Mode debug | `False` |
| `PORT` | Port d'écoute | `80` |
| `FLASK_SECRET_KEY` | Clé secrète Flask | *généré automatiquement* |

### Configuration Docker

Le container est configuré avec :
- **Base** : Python 3.13-slim (sécurisé)
- **Utilisateur** : Non-root pour la sécurité
- **Health Check** : Endpoint `/health` intégré
- **Port** : 80 (production) ou 5000 (dev)
- **Logs** : JSON structuré

## 📊 Endpoints Disponibles

### API Principale
- `GET /` : Page d'accueil des incidents
- `GET /incident/<id>` : Détail d'un incident
- `GET /ajouter` : Formulaire d'ajout
- `POST /ajouter` : Création d'incident

### API REST
- `GET /api/incidents` : Liste JSON des incidents
- `GET /api/incidents/<id>` : Détail JSON d'un incident

### Monitoring
- `GET /health` : Health check (pour Docker/K8s)
- `GET /info` : Informations système et container

## 🐳 Fonctionnalités Docker

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:80/health || exit 1
```

### Sécurité
- Utilisateur non-root (`appuser`)
- Image minimale (Python slim)
- Variables sécurisées
- Ports exposés limités

### Performance
- Multi-stage build
- Cache des layers optimisé
- Gunicorn pour la production
- Configuration WSGI optimisée

## ☁️ Déploiement Azure

### Prérequis
```powershell
# Azure CLI
az login

# Docker
docker --version

# Vérification de l'abonnement
az account show
```

### Méthodes de Déploiement

#### 1. Script Automatique (PowerShell)
```powershell
.\deploy-azure.ps1 -ResourceGroupName "mon-rg" -RegistryName "mon-registry"
```

#### 2. Script Automatique (Bash)
```bash
./deploy-azure.sh
```

#### 3. Template YAML
```powershell
az container create --resource-group rg-flask --file container-instance.yml
```

#### 4. GitHub Actions CI/CD
Push vers `main` déclenche le déploiement automatique.

### Ressources Créées

- **Resource Group** : `rg-flask-incidents`
- **Container Registry** : `flaskincidentsreg.azurecr.io`
- **Container Instance** : `flask-incidents-app`
- **Public IP** : DNS automatique
- **Monitoring** : Logs et métriques intégrés

## 🔍 Monitoring et Debugging

### Logs en Temps Réel
```powershell
# Logs du container Azure
az container logs --resource-group rg-flask-incidents --name flask-incidents-app --follow

# Logs Docker local
docker logs -f <container_id>
```

### Health Monitoring
```bash
# Test de santé
curl http://your-container-url.westeurope.azurecontainer.io/health

# Informations système
curl http://your-container-url.westeurope.azurecontainer.io/info
```

### Métriques Disponibles
- CPU et mémoire utilisés
- Nombre de requêtes
- Temps de réponse
- Status des health checks

## 🛠️ Développement

### Structure du Code
```python
# app.py - Points clés
@app.route('/health')          # Health check Docker
@app.route('/info')            # Info système
@app.route('/api/incidents')   # API REST

# Configuration adaptative
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Tests Locaux
```bash
# Build et test
docker build -t flask-incidents:test .
docker run -p 5000:80 flask-incidents:test

# Tests des endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/incidents
```

## 🔒 Sécurité

### Bonnes Pratiques Implémentées
- Utilisateur non-root dans le container
- Variables d'environnement sécurisées
- Base image minimale et récente
- Health checks pour la stabilité
- Logs structurés sans secrets

### Secrets Management
```yaml
# Pour Azure Container Instances
secure-environment-variables:
  FLASK_SECRET_KEY: "your-secure-key"
  DB_PASSWORD: "your-db-password"
```

## 📚 Documentation Complète

Consultez `DEPLOYMENT_GUIDE.md` pour :
- Guide détaillé de déploiement
- Configuration avancée
- Dépannage des problèmes courants
- Monitoring et maintenance
- Sécurité et bonnes pratiques

## 🤝 Contribution

1. Fork le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📞 Support

- **Issues** : Utilisez l'onglet Issues de GitHub
- **Documentation** : Consultez `DEPLOYMENT_GUIDE.md`
- **Logs** : Utilisez `az container logs` pour Azure
- **Monitoring** : Endpoint `/health` et `/info`

## 🏆 Fonctionnalités Principales

✅ **Containerisation Docker**
- Multi-stage build optimisé
- Security hardening
- Health checks intégrés

✅ **Déploiement Azure**  
- Azure Container Registry
- Azure Container Instances
- Scripts automatisés

✅ **CI/CD GitHub Actions**
- Build automatique
- Tests de sécurité
- Déploiement automatique

✅ **Monitoring Intégré**
- Health endpoints
- Logs structurés  
- Métriques système

✅ **Production Ready**
- Gunicorn WSGI server
- Configuration sécurisée
- Documentation complète

---

**Version** : 1.0  
**License** : MIT  
**Auteur** : Développeur Azure  
**Dernière mise à jour** : 2024