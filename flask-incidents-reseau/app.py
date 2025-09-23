from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'votre-cle-secrete-ici'  # Nécessaire pour les messages flash

# Liste des incidents réseau avec 3 attributs chacun
incidents_reseau = [
    {
        'id': 1,
        'titre': 'Panne serveur principal',
        'severite': 'Critique',
        'date_incident': '2025-09-20 14:30'
    },
    {
        'id': 2,
        'titre': 'Latence élevée sur le réseau',
        'severite': 'Moyenne',
        'date_incident': '2025-09-21 09:15'
    },
    {
        'id': 3,
        'titre': 'Connexion intermittente WiFi',
        'severite': 'Faible',
        'date_incident': '2025-09-22 16:45'
    },
    {
        'id': 4,
        'titre': 'Échec authentification VPN',
        'severite': 'Élevée',
        'date_incident': '2025-09-23 08:20'
    },
    {
        'id': 5,
        'titre': 'Surcharge bande passante',
        'severite': 'Moyenne',
        'date_incident': '2025-09-23 11:10'
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
        'date_incident': datetime.now().strftime('%Y-%m-%d %H:%M')
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)