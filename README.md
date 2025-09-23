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
```bash
cd flask-incidents-sqlserver
pip install -r requirements.txt
python init_database.py  # Initialiser la DB
python app.py
# Accès : http://localhost:5001
```

## 🔧 Technologies utilisées

- **Flask** : Framework web Python
- **SQLAlchemy** : ORM Python (version SQL Server)
- **pyodbc** : Driver SQL Server
- **HTML/CSS** : Interface utilisateur responsive
- **Jinja2** : Moteur de templates
- **JavaScript** : Améliorations UX

## 📚 Documentation

Consultez les README.md dans chaque dossier pour des instructions détaillées :
- [Flask-Incidents-Reseau README](flask-incidents-reseau/README.md)
- [Flask-Incidents-SQLServer README](flask-incidents-sqlserver/README.md)
- [Configuration SQL Server](flask-incidents-sqlserver/config_sqlserver.md)

## 🚀 Déploiement

Ces applications sont prêtes pour :
- Déploiement local de développement
- Intégration avec Azure App Service
- Connexion aux bases de données Azure SQL
- Déploiement containerisé avec Docker

---

**Auteur** : Développé pour la formation AZ-900  
**Date** : Septembre 2025