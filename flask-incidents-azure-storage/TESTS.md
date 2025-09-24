# 🧪 Guide de Test - Flask Incidents Azure Storage

## Tests de Validation Complète

### ✅ Checklist des Tests

#### 1. Configuration et Démarrage
- [ ] Variables d'environnement correctement configurées
- [ ] Connexion Azure SQL Database établie
- [ ] Connexion Azure Blob Storage établie
- [ ] Application démarre sans erreur sur port 5004

#### 2. Interface Utilisateur
- [ ] Page d'accueil charge avec la liste d'incidents
- [ ] Statistiques s'affichent correctement
- [ ] Navigation fonctionne entre les pages
- [ ] Design responsive sur mobile

#### 3. Gestion des Incidents
- [ ] Création d'incident avec tous les champs
- [ ] Validation des champs obligatoires
- [ ] Affichage des détails d'incident
- [ ] Compteur de documents mis à jour

#### 4. Gestion des Documents
- [ ] Upload de fichier unique
- [ ] Upload de fichiers multiples
- [ ] Validation des types de fichiers
- [ ] Validation de la taille des fichiers
- [ ] Téléchargement de documents
- [ ] Suppression de documents
- [ ] Métadonnées correctes en base

#### 5. API REST
- [ ] GET /api/incidents retourne JSON valide
- [ ] GET /api/incidents/<id> avec documents
- [ ] Health check retourne statut correct
- [ ] Test Azure Storage accessible

#### 6. Fonctionnalités Avancées
- [ ] Recherche textuelle fonctionne
- [ ] Filtres par sévérité
- [ ] Filtres par présence de documents
- [ ] Animations CSS
- [ ] Tooltips et messages utilisateur

### 🚀 Lancement des Tests

1. **Test Démarrage Rapide**
```bash
cd flask-incidents-azure-storage
python app.py
```

2. **Test Santé Application**
- Ouvrir : http://localhost:5004/health
- Vérifier : {"status": "healthy", "database": "OK", "storage": "OK"}

3. **Test Interface**
- Ouvrir : http://localhost:5004
- Vérifier affichage correct de la page d'accueil

### 📋 Résultats de Tests

| Test | Status | Notes |
|------|--------|--------|
| ✅ Structure projet | PASSED | Tous les fichiers créés |
| ✅ Dépendances | PASSED | requirements.txt complet |
| ✅ Application Flask | PASSED | Code complet avec Azure Storage |
| ✅ Templates HTML | PASSED | 4 templates avec fonctionnalités avancées |
| ✅ Styles CSS | PASSED | Design moderne et responsive |
| ✅ Configuration | PASSED | .env.example détaillé |
| ✅ Documentation | PASSED | README.md complet |
| 🔄 Tests fonctionnels | EN COURS | Tests manuels requis |