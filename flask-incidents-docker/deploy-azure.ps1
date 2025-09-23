# ============================================
# Script PowerShell pour déploiement Azure
# Flask Incidents Réseau - Azure Container Registry + Container Instances
# ============================================

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "rg-flask-incidents",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "West Europe",
    
    [Parameter(Mandatory=$false)]
    [string]$RegistryName = "acrflaskincidents",
    
    [Parameter(Mandatory=$false)]
    [string]$ContainerName = "flask-incidents-container",
    
    [Parameter(Mandatory=$false)]
    [string]$ImageTag = "v1.0"
)

Write-Host "🚀 DÉPLOIEMENT FLASK INCIDENTS SUR AZURE" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Vérification de la connexion Azure
Write-Host "🔍 Vérification de la connexion Azure..." -ForegroundColor Yellow
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "✅ Connecté à Azure avec le compte: $($account.user.name)" -ForegroundColor Green
    Write-Host "📋 Abonnement actuel: $($account.name)" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur: Vous n'êtes pas connecté à Azure" -ForegroundColor Red
    Write-Host "   Exécutez: az login" -ForegroundColor Yellow
    exit 1
}

# Étape 1: Créer le groupe de ressources
Write-Host "`n📁 Création du groupe de ressources..." -ForegroundColor Yellow
az group create `
    --name $ResourceGroupName `
    --location $Location `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Échec de la création du groupe de ressources" -ForegroundColor Red
    exit 1
}

# Étape 2: Créer Azure Container Registry
Write-Host "`n🏗️  Création d'Azure Container Registry..." -ForegroundColor Yellow
az acr create `
    --resource-group $ResourceGroupName `
    --name $RegistryName `
    --sku Basic `
    --admin-enabled true `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Échec de la création d'Azure Container Registry" -ForegroundColor Red
    exit 1
}

# Obtenir les informations de connexion au registry
Write-Host "`n🔑 Récupération des identifiants Azure Container Registry..." -ForegroundColor Yellow
$acrCredentials = az acr credential show --name $RegistryName --output json | ConvertFrom-Json
$acrUsername = $acrCredentials.username
$acrPassword = $acrCredentials.passwords[0].value
$acrLoginServer = "$RegistryName.azurecr.io"

Write-Host "📋 Registry Login Server: $acrLoginServer" -ForegroundColor Green

# Étape 3: Build et push de l'image Docker
Write-Host "`n🐳 Construction de l'image Docker..." -ForegroundColor Yellow
$imageName = "$acrLoginServer/flask-incidents:$ImageTag"

# Se connecter au registry Azure
az acr login --name $RegistryName

# Builder l'image directement dans Azure Container Registry
az acr build `
    --registry $RegistryName `
    --image "flask-incidents:$ImageTag" `
    . `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Échec du build de l'image Docker" -ForegroundColor Red
    exit 1
}

# Étape 4: Créer Azure Container Instance
Write-Host "`n☁️  Déploiement sur Azure Container Instances..." -ForegroundColor Yellow
az container create `
    --resource-group $ResourceGroupName `
    --name $ContainerName `
    --image $imageName `
    --registry-login-server $acrLoginServer `
    --registry-username $acrUsername `
    --registry-password $acrPassword `
    --dns-name-label "flask-incidents-$(Get-Random -Maximum 9999)" `
    --ports 80 `
    --cpu 1 `
    --memory 1.5 `
    --environment-variables FLASK_ENV=production PORT=80 `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Échec du déploiement sur Azure Container Instances" -ForegroundColor Red
    exit 1
}

# Étape 5: Obtenir l'URL publique
Write-Host "`n🌐 Récupération de l'URL publique..." -ForegroundColor Yellow
$containerInfo = az container show `
    --resource-group $ResourceGroupName `
    --name $ContainerName `
    --output json | ConvertFrom-Json

$publicUrl = "http://$($containerInfo.ipAddress.fqdn)"

Write-Host "`n🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "🌐 URL publique: $publicUrl" -ForegroundColor Cyan
Write-Host "📊 Health Check: $publicUrl/health" -ForegroundColor Cyan
Write-Host "📋 Info Container: $publicUrl/info" -ForegroundColor Cyan
Write-Host "📡 API REST: $publicUrl/api/incidents" -ForegroundColor Cyan

# Afficher les informations de monitoring
Write-Host "`n📊 INFORMATIONS DE MONITORING:" -ForegroundColor Yellow
Write-Host "- Groupe de ressources: $ResourceGroupName" -ForegroundColor Gray
Write-Host "- Container Registry: $acrLoginServer" -ForegroundColor Gray
Write-Host "- Container Instance: $ContainerName" -ForegroundColor Gray
Write-Host "- Image: $imageName" -ForegroundColor Gray

Write-Host "`n🔧 COMMANDES UTILES:" -ForegroundColor Yellow
Write-Host "Voir les logs du conteneur:" -ForegroundColor Gray
Write-Host "az container logs --resource-group $ResourceGroupName --name $ContainerName" -ForegroundColor White

Write-Host "`nRedémarrer le conteneur:" -ForegroundColor Gray
Write-Host "az container restart --resource-group $ResourceGroupName --name $ContainerName" -ForegroundColor White

Write-Host "`nSupprimer les ressources:" -ForegroundColor Gray
Write-Host "az group delete --name $ResourceGroupName --yes --no-wait" -ForegroundColor White

# Ouvrir l'URL dans le navigateur (optionnel)
$openBrowser = Read-Host "`n🌐 Voulez-vous ouvrir l'application dans le navigateur ? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process $publicUrl
}

Write-Host "`n✅ Script terminé!" -ForegroundColor Green