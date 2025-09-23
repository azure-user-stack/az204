# ============================================
# Dockerfile pour Flask Incidents Réseau
# Version optimisée pour Azure Container Instances
# ============================================

# Utiliser une image Python officielle slim comme base
FROM python:3.13-slim

# Métadonnées de l'image
LABEL maintainer="votre-email@exemple.com"
LABEL version="1.0.0"
LABEL description="Flask Incidents Réseau - Application containerisée pour Azure"

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Variables d'environnement par défaut
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=80
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copier le fichier requirements.txt en premier pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY app.py .
COPY templates/ templates/

# Créer les répertoires nécessaires et ajuster les permissions
RUN mkdir -p /app/logs && \
    chown -R flaskuser:flaskuser /app

# Changer vers l'utilisateur non-root
USER flaskuser

# Exposer le port sur lequel l'application s'exécute
EXPOSE 80

# Vérification de santé du conteneur
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Commande par défaut pour lancer l'application
CMD ["python", "app.py"]

# ============================================
# Instructions de build et d'utilisation :
# ============================================
# 
# Build local :
# docker build -t flask-incidents:latest .
# 
# Run local :
# docker run -p 8080:80 flask-incidents:latest
# 
# Build pour Azure Container Registry :
# docker build -t votreregistry.azurecr.io/flask-incidents:v1.0 .
# 
# Push vers Azure Container Registry :
# docker push votreregistry.azurecr.io/flask-incidents:v1.0
# ============================================