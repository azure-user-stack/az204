# Application Flask - Incidents Réseau

Cette application Flask simple affiche une liste d'incidents réseau avec 3 attributs pour chaque incident.

## Structure du projet

```
flask-incidents-reseau/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
└── templates/            # Templates HTML
    ├── incidents.html    # Page principale avec la liste des incidents
    └── detail.html       # Page de détail d'un incident
```

## Fonctionnalités

- **Page d'accueil** : Affiche une liste de 5 incidents réseau
- **Page de détail** : Affiche les détails complets d'un incident spécifique
- **Interface responsive** : Design adaptatif avec CSS moderne

## Attributs des incidents

Chaque incident contient 3 attributs :
1. **Titre** : Description de l'incident
2. **Sévérité** : Niveau d'importance (Critique, Élevée, Moyenne, Faible)
3. **Date incident** : Horodatage de l'incident

## Installation et exécution

### 1. Installer Python et pip
Assurez-vous d'avoir Python 3.7+ installé sur votre système.

### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
venv\Scripts\activate  # Sur Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
python app.py
```

### 5. Accéder à l'application
Ouvrez votre navigateur et allez à : http://localhost:5000

## Routes disponibles

- `/` : Page principale avec la liste des incidents
- `/incident/<id>` : Page de détail d'un incident spécifique

## Personnalisation

Vous pouvez facilement modifier les données d'incidents dans le fichier `app.py` en modifiant la liste `incidents_reseau`.

## Technologies utilisées

- **Flask** : Framework web Python
- **HTML/CSS** : Interface utilisateur
- **Jinja2** : Moteur de templates (intégré à Flask)

## Auteur

Application créée pour démontrer les fonctionnalités de base de Flask.