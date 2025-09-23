#!/bin/bash

# ============================================
# Script Bash pour déploiement Azure
# Flask Incidents Réseau - Azure Container Registry + Container Instances
# ============================================

# Configuration par défaut
RESOURCE_GROUP_NAME="${1:-rg-flask-incidents}"
LOCATION="${2:-westeurope}"
REGISTRY_NAME="${3:-acrflaskincidents}"
CONTAINER_NAME="${4:-flask-incidents-container}"
IMAGE_TAG="${5:-v1.0}"

echo "🚀 DÉPLOIEMENT FLASK INCIDENTS SUR AZURE"
echo "======================================="

# Vérification de la connexion Azure
echo "🔍 Vérification de la connexion Azure..."
if ! az account show > /dev/null 2>&1; then
    echo "❌ Erreur: Vous n'êtes pas connecté à Azure"
    echo "   Exécutez: az login"
    exit 1
fi

ACCOUNT_INFO=$(az account show --output tsv --query '[user.name,name]')
echo "✅ Connecté à Azure avec le compte: $(echo $ACCOUNT_INFO | cut -f1)"
echo "📋 Abonnement actuel: $(echo $ACCOUNT_INFO | cut -f2)"

# Étape 1: Créer le groupe de ressources
echo ""
echo "📁 Création du groupe de ressources..."
az group create \
    --name $RESOURCE_GROUP_NAME \
    --location $LOCATION \
    --output table

if [ $? -ne 0 ]; then
    echo "❌ Échec de la création du groupe de ressources"
    exit 1
fi

# Étape 2: Créer Azure Container Registry
echo ""
echo "🏗️  Création d'Azure Container Registry..."
az acr create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $REGISTRY_NAME \
    --sku Basic \
    --admin-enabled true \
    --output table

if [ $? -ne 0 ]; then
    echo "❌ Échec de la création d'Azure Container Registry"
    exit 1
fi

# Obtenir les informations de connexion au registry
echo ""
echo "🔑 Récupération des identifiants Azure Container Registry..."
ACR_CREDENTIALS=$(az acr credential show --name $REGISTRY_NAME --output json)
ACR_USERNAME=$(echo $ACR_CREDENTIALS | jq -r '.username')
ACR_PASSWORD=$(echo $ACR_CREDENTIALS | jq -r '.passwords[0].value')
ACR_LOGIN_SERVER="${REGISTRY_NAME}.azurecr.io"

echo "📋 Registry Login Server: $ACR_LOGIN_SERVER"

# Étape 3: Build et push de l'image Docker
echo ""
echo "🐳 Construction de l'image Docker..."
IMAGE_NAME="$ACR_LOGIN_SERVER/flask-incidents:$IMAGE_TAG"

# Se connecter au registry Azure
az acr login --name $REGISTRY_NAME

# Builder l'image directement dans Azure Container Registry
az acr build \
    --registry $REGISTRY_NAME \
    --image "flask-incidents:$IMAGE_TAG" \
    . \
    --output table

if [ $? -ne 0 ]; then
    echo "❌ Échec du build de l'image Docker"
    exit 1
fi

# Étape 4: Créer Azure Container Instance
echo ""
echo "☁️  Déploiement sur Azure Container Instances..."
DNS_LABEL="flask-incidents-$RANDOM"

az container create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $CONTAINER_NAME \
    --image $IMAGE_NAME \
    --registry-login-server $ACR_LOGIN_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password "$ACR_PASSWORD" \
    --dns-name-label $DNS_LABEL \
    --ports 80 \
    --cpu 1 \
    --memory 1.5 \
    --environment-variables FLASK_ENV=production PORT=80 \
    --output table

if [ $? -ne 0 ]; then
    echo "❌ Échec du déploiement sur Azure Container Instances"
    exit 1
fi

# Étape 5: Obtenir l'URL publique
echo ""
echo "🌐 Récupération de l'URL publique..."
CONTAINER_INFO=$(az container show \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $CONTAINER_NAME \
    --output json)

FQDN=$(echo $CONTAINER_INFO | jq -r '.ipAddress.fqdn')
PUBLIC_URL="http://$FQDN"

echo ""
echo "🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!"
echo "================================="
echo "🌐 URL publique: $PUBLIC_URL"
echo "📊 Health Check: $PUBLIC_URL/health"
echo "📋 Info Container: $PUBLIC_URL/info"
echo "📡 API REST: $PUBLIC_URL/api/incidents"

# Afficher les informations de monitoring
echo ""
echo "📊 INFORMATIONS DE MONITORING:"
echo "- Groupe de ressources: $RESOURCE_GROUP_NAME"
echo "- Container Registry: $ACR_LOGIN_SERVER"
echo "- Container Instance: $CONTAINER_NAME"
echo "- Image: $IMAGE_NAME"

echo ""
echo "🔧 COMMANDES UTILES:"
echo "Voir les logs du conteneur:"
echo "az container logs --resource-group $RESOURCE_GROUP_NAME --name $CONTAINER_NAME"
echo ""
echo "Redémarrer le conteneur:"
echo "az container restart --resource-group $RESOURCE_GROUP_NAME --name $CONTAINER_NAME"
echo ""
echo "Supprimer les ressources:"
echo "az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait"

echo ""
echo "✅ Script terminé!"

# Tenter d'ouvrir l'URL dans le navigateur par défaut
if command -v xdg-open > /dev/null; then
    echo "🌐 Ouverture de l'application dans le navigateur..."
    xdg-open $PUBLIC_URL
elif command -v open > /dev/null; then
    echo "🌐 Ouverture de l'application dans le navigateur..."
    open $PUBLIC_URL
fi