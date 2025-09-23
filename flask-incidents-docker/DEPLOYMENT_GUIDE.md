# ============================================
# GUIDE DE DÉPLOIEMENT - Flask Incidents Docker
# ============================================

## 🚀 Guide Complet de Déploiement Azure

Ce projet Flask est conçu pour un déploiement sur Azure Container Registry et Azure Container Instances avec des outils automatisés complets.

## 📋 Prérequis

### 1. Outils requis
```powershell
# Azure CLI
az --version

# Docker
docker --version

# Git (optionnel pour CI/CD)
git --version
```

### 2. Configuration Azure
```powershell
# Connexion à Azure
az login

# Vérifier l'abonnement
az account show
```

## 🔧 Méthodes de Déploiement

### Option 1: Script PowerShell Automatique (Recommandé)
```powershell
# Exécution simple
.\deploy-azure.ps1

# Avec paramètres personnalisés
.\deploy-azure.ps1 -ResourceGroupName "mon-rg" -RegistryName "mon-registry" -Location "France Central"
```

### Option 2: Script Bash/Linux
```bash
# Rendre le script exécutable
chmod +x deploy-azure.sh

# Exécution
./deploy-azure.sh
```

### Option 3: Commandes Manuelles Étape par Étape

#### A. Créer les ressources Azure
```powershell
# Variables
$resourceGroup = "rg-flask-incidents"
$registryName = "flaskincidentsreg"
$containerName = "flask-incidents-app"
$location = "West Europe"

# Créer le groupe de ressources
az group create --name $resourceGroup --location $location

# Créer Azure Container Registry
az acr create --resource-group $resourceGroup --name $registryName --sku Basic --admin-enabled true
```

#### B. Build et Push de l'image Docker
```powershell
# Build de l'image
docker build -t flask-incidents:latest .

# Tag pour Azure Container Registry
docker tag flask-incidents:latest $registryName.azurecr.io/flask-incidents:v1.0

# Login au registre
az acr login --name $registryName

# Push de l'image
docker push $registryName.azurecr.io/flask-incidents:v1.0
```

#### C. Déploiement sur Azure Container Instances
```powershell
# Récupérer les credentials du registre
$acrCredentials = az acr credential show --name $registryName | ConvertFrom-Json

# Créer Container Instance
az container create `
  --resource-group $resourceGroup `
  --name $containerName `
  --image $registryName.azurecr.io/flask-incidents:v1.0 `
  --cpu 1 `
  --memory 1.5 `
  --registry-login-server $registryName.azurecr.io `
  --registry-username $acrCredentials.username `
  --registry-password $acrCredentials.passwords[0].value `
  --dns-name-label "flask-incidents-unique" `
  --ports 80 `
  --environment-variables FLASK_ENV=production PORT=80 `
  --secure-environment-variables FLASK_SECRET_KEY="votre-cle-secrete-ici"
```

### Option 4: Template YAML
```powershell
# Modifier le fichier container-instance.yml
# Puis déployer
az container create --resource-group rg-flask --file container-instance.yml
```

## 🔄 CI/CD avec GitHub Actions

### Configuration des Secrets GitHub
1. Allez dans Settings > Secrets and variables > Actions
2. Ajoutez ces secrets :

```yaml
AZURE_CREDENTIALS: # Service principal JSON
REGISTRY_LOGIN_SERVER: votreregistry.azurecr.io
REGISTRY_USERNAME: username du registre
REGISTRY_PASSWORD: password du registre
AZURE_RESOURCE_GROUP: nom de votre RG
FLASK_SECRET_KEY: clé secrète Flask
```

### Créer un Service Principal
```powershell
# Remplacez YOUR-SUBSCRIPTION-ID
az ad sp create-for-rbac --name "github-actions" `
  --role contributor `
  --scopes /subscriptions/YOUR-SUBSCRIPTION-ID `
  --sdk-auth
```

## 🧪 Tests et Validation

### Tests Locaux
```powershell
# Build et test local
docker build -t flask-incidents:test .
docker run -p 5000:80 flask-incidents:test

# Tester les endpoints
curl http://localhost:5000/health
curl http://localhost:5000/info
curl http://localhost:5000/api/incidents
```

### Tests Post-Déploiement
```powershell
# Récupérer l'URL du container
$fqdn = az container show --resource-group rg-flask-incidents --name flask-incidents-app --query ipAddress.fqdn --output tsv

# Tests des endpoints
curl "http://$fqdn/health"
curl "http://$fqdn/info"
curl "http://$fqdn/api/incidents"
```

## 📊 Monitoring et Maintenance

### Logs du Container
```powershell
# Voir les logs en temps réel
az container logs --resource-group rg-flask-incidents --name flask-incidents-app --follow

# Logs complets
az container logs --resource-group rg-flask-incidents --name flask-incidents-app
```

### Statistiques d'Utilisation
```powershell
# État du container
az container show --resource-group rg-flask-incidents --name flask-incidents-app

# Métriques
az monitor metrics list --resource /subscriptions/YOUR-SUB/resourceGroups/rg-flask-incidents/providers/Microsoft.ContainerInstance/containerGroups/flask-incidents-app
```

### Redémarrage
```powershell
# Redémarrer le container
az container restart --resource-group rg-flask-incidents --name flask-incidents-app
```

## 🔒 Sécurité et Bonnes Pratiques

### Variables d'Environnement Sécurisées
```powershell
# Utiliser --secure-environment-variables pour les secrets
az container create ... `
  --secure-environment-variables FLASK_SECRET_KEY="your-secret" DB_PASSWORD="your-db-pass"
```

### Limitation des Ressources
```yaml
# Dans container-instance.yml
resources:
  requests:
    cpu: 0.5      # Minimum recommandé
    memoryInGb: 1.0  # Minimum recommandé
  limits:
    cpu: 1.0      # Maximum autorisé
    memoryInGb: 2.0  # Maximum autorisé
```

### Health Checks
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 80
  initialDelaySeconds: 30
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /health
    port: 80
  initialDelaySeconds: 15
  periodSeconds: 15
```

## 🛠️ Dépannage

### Problèmes Courants

#### Container ne démarre pas
```powershell
# Vérifier les logs
az container logs --resource-group rg-flask-incidents --name flask-incidents-app

# Vérifier l'état
az container show --resource-group rg-flask-incidents --name flask-incidents-app --query instanceView.state
```

#### Problème de registre
```powershell
# Tester la connexion au registre
az acr login --name votreregistry

# Vérifier les images
az acr repository list --name votreregistry
```

#### Problème de réseau
```powershell
# Vérifier l'IP publique
az container show --resource-group rg-flask-incidents --name flask-incidents-app --query ipAddress.ip

# Vérifier les ports
az container show --resource-group rg-flask-incidents --name flask-incidents-app --query ipAddress.ports
```

## 📞 Support et Documentation

### Ressources Utiles
- [Documentation Azure Container Instances](https://docs.microsoft.com/azure/container-instances/)
- [Documentation Azure Container Registry](https://docs.microsoft.com/azure/container-registry/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

### Commandes Utiles
```powershell
# Nettoyer toutes les ressources
az group delete --name rg-flask-incidents --yes --no-wait

# Supprimer juste le container
az container delete --resource-group rg-flask-incidents --name flask-incidents-app --yes

# Mise à jour de l'image
az container create --resource-group rg-flask-incidents --name flask-incidents-app --image registry.azurecr.io/flask-incidents:v2.0
```

## 🎯 Conclusion

Ce guide fournit toutes les méthodes pour déployer votre application Flask sur Azure. Choisissez la méthode qui convient le mieux à votre environnement :

- **Scripts automatiques** : Pour un déploiement rapide
- **Commandes manuelles** : Pour un contrôle total
- **GitHub Actions** : Pour CI/CD automatique
- **Template YAML** : Pour des déploiements reproductibles

L'application sera accessible via l'URL fournie après le déploiement avec tous les endpoints fonctionnels (/health, /info, /api/incidents).