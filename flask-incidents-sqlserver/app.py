from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.parse
import os
from sqlalchemy import text

app = Flask(__name__)

# Configuration de la base de données SQL Server
# Nom de serveur correct détecté automatiquement
DB_SERVER = 'vmappincidents\\SQLEXPRESS'  # Nom réel du serveur détecté
DB_DATABASE = 'IncidentsReseau'           # Base de données existante

# Configurations alternatives si nécessaire
DB_CONFIGS_BACKUP = [
    'vmappincidents\\SQLEXPRESS',     # Configuration détectée (recommandée)
    '(local)\\SQLEXPRESS',            # Alternative locale
    '.\\SQLEXPRESS',                  # Notation point
]

# Option 1: Windows Authentication (Recommandée pour SQL Server Express)
# Chaîne de connexion avec Windows Authentication
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
    f"Connection Timeout=10;"
)

# Option 2: SQL Server Authentication (décommentez si vous préférez)
# DB_USERNAME = 'sa'
# DB_PASSWORD = 'VotreMotDePasse123!'
# params = urllib.parse.quote_plus(
#     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#     f"SERVER={DB_SERVER};"
#     f"DATABASE={DB_DATABASE};"
#     f"UID={DB_USERNAME};"
#     f"PWD={DB_PASSWORD};"
#     f"TrustServerCertificate=yes;"
# )

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

# Modèle de données pour les incidents réseau
class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    severite = db.Column(db.String(50), nullable=False)
    date_incident = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Incident {self.titre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'severite': self.severite,
            'date_incident': self.date_incident.strftime('%Y-%m-%d %H:%M')
        }

@app.route('/')
def index():
    try:
        # Récupérer tous les incidents depuis la base de données
        incidents = Incident.query.order_by(Incident.date_incident.desc()).all()
        return render_template('incidents.html', incidents=incidents)
    except Exception as e:
        return f"Erreur de connexion à la base de données: {str(e)}", 500

@app.route('/incident/<int:incident_id>')
def detail_incident(incident_id):
    try:
        # Récupérer un incident spécifique
        incident = Incident.query.get_or_404(incident_id)
        return render_template('detail.html', incident=incident)
    except Exception as e:
        return f"Erreur lors de la récupération de l'incident: {str(e)}", 500

@app.route('/api/incidents')
def api_incidents():
    """API endpoint pour récupérer tous les incidents au format JSON"""
    try:
        incidents = Incident.query.all()
        return jsonify([incident.to_dict() for incident in incidents])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-db')
def test_db():
    """Route de test pour vérifier la connexion à la base de données"""
    try:
        # Test simple de connexion
        result = db.session.execute(text('SELECT @@VERSION'))
        version = result.fetchone()[0]
        return f"Connexion réussie ! Version SQL Server: {version}"
    except Exception as e:
        return f"Erreur de connexion: {str(e)}", 500

def init_db():
    """Initialiser la base de données avec des données d'exemple"""
    try:
        # Créer les tables
        db.create_all()
        
        # Vérifier si des données existent déjà
        if Incident.query.count() == 0:
            # Ajouter des données d'exemple
            incidents_exemple = [
                Incident(
                    titre='Panne serveur principal',
                    severite='Critique',
                    date_incident=datetime(2025, 9, 20, 14, 30)
                ),
                Incident(
                    titre='Latence élevée sur le réseau',
                    severite='Moyenne',
                    date_incident=datetime(2025, 9, 21, 9, 15)
                ),
                Incident(
                    titre='Connexion intermittente WiFi',
                    severite='Faible',
                    date_incident=datetime(2025, 9, 22, 16, 45)
                ),
                Incident(
                    titre='Échec authentification VPN',
                    severite='Élevée',
                    date_incident=datetime(2025, 9, 23, 8, 20)
                ),
                Incident(
                    titre='Surcharge bande passante',
                    severite='Moyenne',
                    date_incident=datetime(2025, 9, 23, 11, 10)
                )
            ]
            
            for incident in incidents_exemple:
                db.session.add(incident)
            
            db.session.commit()
            print("Base de données initialisée avec succès !")
        else:
            print("Données existantes trouvées, pas d'initialisation nécessaire.")
            
    except Exception as e:
        print(f"Erreur lors de l'initialisation: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)