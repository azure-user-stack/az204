from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'votre-cle-secrete-ici')

# Liste des incidents réseau avec 3 attributs chacun
incidents_reseau = [
    {
        'id': 1,
        'titre': 'Panne serveur principal',
        'severite': 'Critique',
        'date_incident': '2025-09-20 14:30',
        'description': 'Interruption complète du serveur principal. Services indisponibles.'
    },
    {
        'id': 2,
        'titre': 'Latence élevée sur le réseau',
        'severite': 'Moyenne',
        'date_incident': '2025-09-21 09:15',
        'description': 'Temps de réponse anormalement élevé sur les connexions réseau.'
    },
    {
        'id': 3,
        'titre': 'Connexion intermittente WiFi',
        'severite': 'Faible',
        'date_incident': '2025-09-22 16:45',
        'description': 'Déconnexions sporadiques du réseau WiFi dans certaines zones.'
    },
    {
        'id': 4,
        'titre': 'Échec authentification VPN',
        'severite': 'Élevée',
        'date_incident': '2025-09-23 08:20',
        'description': 'Impossible de se connecter au VPN d\'entreprise depuis ce matin.'
    },
    {
        'id': 5,
        'titre': 'Surcharge bande passante',
        'severite': 'Moyenne',
        'date_incident': '2025-09-23 11:10',
        'description': 'Utilisation de la bande passante à 95% causant des ralentissements.'
    }
]

@app.route('/')
def index():
    return render_template('incidents.html', incidents=incidents_reseau)

@app.route('/ajouter')
def ajouter_incident_form():
    return render_template('ajouter.html')

@app.route('/ajouter-incident', methods=['POST'])
def ajouter_incident():
    # Récupérer les données du formulaire
    titre = request.form.get('titre')
    severite = request.form.get('severite')
    description = request.form.get('description', '')
    
    # Validation des données
    if not titre or not severite:
        flash('Veuillez remplir tous les champs obligatoires.', 'error')
        return redirect(url_for('ajouter_incident_form'))
    
    # Générer un nouvel ID (prendre le max + 1)
    nouveau_id = max([inc['id'] for inc in incidents_reseau]) + 1 if incidents_reseau else 1
    
    # Créer le nouvel incident
    nouvel_incident = {
        'id': nouveau_id,
        'titre': titre.strip(),
        'severite': severite,
        'date_incident': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'description': description.strip()
    }
    
    # Ajouter à la liste
    incidents_reseau.append(nouvel_incident)
    
    # Message de confirmation
    flash(f'Incident "{titre}" ajouté avec succès !', 'success')
    
    # Rediriger vers la page principale
    return redirect(url_for('index'))

@app.route('/incident/<int:incident_id>')
def detail_incident(incident_id):
    incident = next((inc for inc in incidents_reseau if inc['id'] == incident_id), None)
    if incident:
        return render_template('detail.html', incident=incident)
    return "Incident non trouvé", 404

# API REST pour les incidents
@app.route('/api/incidents', methods=['GET'])
def api_incidents():
    return jsonify({
        'incidents': incidents_reseau,
        'count': len(incidents_reseau),
        'container_info': {
            'hostname': os.environ.get('HOSTNAME', 'unknown'),
            'app_version': '1.0.0-docker'
        }
    })

# Route de santé pour Docker/Azure
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-docker',
        'incidents_count': len(incidents_reseau)
    })

# Route d'information sur le conteneur
@app.route('/info')
def container_info():
    return jsonify({
        'container_id': os.environ.get('HOSTNAME', 'unknown'),
        'app_name': 'Flask Incidents Réseau',
        'version': '1.0.0-docker',
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'port': os.environ.get('PORT', '5000'),
        'python_version': os.sys.version
    })

if __name__ == '__main__':
    # Configuration pour Docker et Azure Container Instances
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )