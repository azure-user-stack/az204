"""
🚀 Flask Incidents Réseau avec Azure Storage
============================================
Application Flask pour la gestion d'incidents réseau avec :
- Azure SQL Database pour les données
- Azure Blob Storage pour les documents
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.parse
import os
import uuid
import io
from werkzeug.utils import secure_filename
from sqlalchemy import text

# Azure Storage imports
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError

# Charger les variables d'environnement depuis le fichier .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("🔧 Variables d'environnement chargées depuis .env")
except ImportError:
    print("⚠️  python-dotenv non installé, utilisation des variables système uniquement")

app = Flask(__name__)

# ========================================
# CONFIGURATION AZURE SQL DATABASE
# ========================================

# Configuration Azure SQL Database
AZURE_SQL_SERVER = os.environ.get('AZURE_SQL_SERVER', 'votre-serveur.database.windows.net')
AZURE_SQL_DATABASE = os.environ.get('AZURE_SQL_DATABASE', 'IncidentsReseau')
AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME', 'votre-admin')
AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD', 'VotreMotDePasse123!')

# ========================================
# CONFIGURATION AZURE BLOB STORAGE
# ========================================

# Configuration Azure Storage Account
AZURE_STORAGE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', 'votre-storage-account')
AZURE_STORAGE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY', 'votre-cle-storage')
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME', 'incident-documents')

# Mode de stockage (mock pour tests, azure pour production)
AZURE_STORAGE_MODE = os.environ.get('AZURE_STORAGE_MODE', 'azure')

# Types de fichiers autorisés et taille max
ALLOWED_EXTENSIONS = {
    'documents': {'pdf', 'doc', 'docx', 'txt', 'md', 'rtf'},
    'images': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'},
    'spreadsheets': {'xls', 'xlsx', 'csv'},
    'presentations': {'ppt', 'pptx'},
    'archives': {'zip', 'rar', '7z'},
    'other': {'json', 'xml', 'log'}
}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

def create_azure_sql_connection_string():
    """Créer la chaîne de connexion Azure SQL Database"""
    
    # Récupérer la configuration depuis les variables d'environnement
    odbc_driver = os.environ.get('AZURE_ODBC_DRIVER', 'ODBC Driver 18 for SQL Server')
    encrypt = os.environ.get('AZURE_ENCRYPT', 'yes')
    trust_cert = os.environ.get('AZURE_TRUST_SERVER_CERTIFICATE', 'no')
    timeout = os.environ.get('AZURE_CONNECTION_TIMEOUT', '30')
    
    if AZURE_SQL_USERNAME and AZURE_SQL_PASSWORD:
        print("🔐 Utilisation de l'authentification SQL Server pour Azure")
        connection_params = urllib.parse.quote_plus(
            f"DRIVER={{{odbc_driver}}};"
            f"SERVER={AZURE_SQL_SERVER};"
            f"DATABASE={AZURE_SQL_DATABASE};"
            f"UID={AZURE_SQL_USERNAME};"
            f"PWD={AZURE_SQL_PASSWORD};"
            f"Encrypt={encrypt};"
            f"TrustServerCertificate={trust_cert};"
            f"Connection Timeout={timeout};"
        )
    else:
        print("⚠️  Variables d'environnement manquantes pour Azure SQL")
        raise ValueError("Configuration Azure SQL incomplète")
    
    return f"mssql+pyodbc:///?odbc_connect={connection_params}"

def create_blob_service_client():
    """Créer le client Azure Blob Storage"""
    try:
        if AZURE_STORAGE_CONNECTION_STRING:
            # Vérifier si c'est une URL SAS ou une vraie connection string
            if AZURE_STORAGE_CONNECTION_STRING.startswith('https://'):
                # C'est une URL SAS - utiliser l'URL directement
                print("🔗 Connexion Azure Blob Storage via SAS URL")
                # Extraire l'URL de base et le token SAS
                parts = AZURE_STORAGE_CONNECTION_STRING.split('?')
                if len(parts) == 2:
                    base_url = parts[0].replace('/appincidentsdocs', '')  # Enlever le container de l'URL
                    sas_token = parts[1]
                    blob_service_client = BlobServiceClient(account_url=base_url, credential=f"?{sas_token}")
                    print(f"🔑 SAS Token utilisé, expire probablement bientôt")
                else:
                    raise ValueError("URL SAS malformée")
            else:
                # Utilisation de la chaîne de connexion complète traditionnelle
                blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
                print("🔗 Connexion Azure Blob Storage via connection string")
        elif AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY:
            # Utilisation du nom de compte et de la clé
            account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
            blob_service_client = BlobServiceClient(account_url=account_url, credential=AZURE_STORAGE_ACCOUNT_KEY)
            print("🔑 Connexion Azure Blob Storage via account key")
        else:
            # Utilisation de l'authentification par défaut Azure (Managed Identity, Azure CLI, etc.)
            account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
            credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
            print("🎫 Connexion Azure Blob Storage via Default Azure Credential")
        
        return blob_service_client
    except Exception as e:
        print(f"❌ Erreur lors de la création du client Blob Storage: {e}")
        return None

# Configuration Flask
app.config['SQLALCHEMY_DATABASE_URI'] = create_azure_sql_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production')

# Initialisation de la base de données
db = SQLAlchemy(app)

# ========================================
# FILTRES JINJA2 PERSONNALISÉS
# ========================================

@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convertir les retours à la ligne en balises HTML <br>"""
    if not text:
        return text
    
    from markupsafe import Markup, escape
    # Échapper le texte pour éviter XSS, puis remplacer les \n par <br>
    escaped = escape(text)
    # Remplacer les retours à la ligne par <br>
    result = escaped.replace('\n', Markup('<br>'))
    return Markup(result)

# ========================================
# MODÈLES DE DONNÉES
# ========================================

class Incident(db.Model):
    """Modèle pour les incidents réseau"""
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    severite = db.Column(db.String(50), nullable=False, default='Moyenne')
    date_incident = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation avec les documents
    documents = db.relationship('IncidentDocument', backref='incident', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Incident {self.id}: {self.titre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'severite': self.severite,
            'date_incident': self.date_incident.isoformat() if self.date_incident else None,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None,
            'documents_count': len(self.documents)
        }

class IncidentDocument(db.Model):
    """Modèle pour les documents attachés aux incidents"""
    __tablename__ = 'incident_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Nom original du fichier
    blob_name = db.Column(db.String(500), nullable=False)  # Nom unique dans le blob storage
    file_size = db.Column(db.Integer, nullable=False)  # Taille en bytes
    content_type = db.Column(db.String(100), nullable=False)  # Type MIME
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploaded_by = db.Column(db.String(100), default='System')  # Qui a uploadé le fichier
    
    def __repr__(self):
        return f'<Document {self.id}: {self.filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'filename': self.filename,
            'file_size': self.file_size,
            'content_type': self.content_type,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'uploaded_by': self.uploaded_by
        }

# ========================================
# FONCTIONS UTILITAIRES AZURE STORAGE
# ========================================

def allowed_file(filename):
    """Vérifier si le fichier est autorisé"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    all_extensions = set()
    for ext_group in ALLOWED_EXTENSIONS.values():
        all_extensions.update(ext_group)
    
    return extension in all_extensions

def get_file_category(filename):
    """Déterminer la catégorie du fichier"""
    if '.' not in filename:
        return 'other'
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if extension in extensions:
            return category
    
    return 'other'

def generate_blob_name(filename, incident_id):
    """Générer un nom unique pour le blob"""
    # Utiliser un UUID pour éviter les conflits
    unique_id = str(uuid.uuid4())
    safe_filename = secure_filename(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return f"incident_{incident_id}/{timestamp}_{unique_id}_{safe_filename}"

def upload_file_to_blob(file, filename, incident_id):
    """Uploader un fichier vers Azure Blob Storage"""
    try:
        # Mode mock pour tests
        if AZURE_STORAGE_MODE == 'mock':
            print(f"🧪 MODE MOCK: Simulation d'upload pour {filename}")
            file.seek(0)
            file_content = file.read()
            blob_name = generate_blob_name(filename, incident_id)
            print(f"✅ [MOCK] Fichier simulé: {blob_name} ({len(file_content)} bytes)")
            return blob_name, len(file_content)
        
        # Créer le client Blob Storage
        blob_service_client = create_blob_service_client()
        if not blob_service_client:
            raise Exception("Impossible de créer le client Blob Storage")
        
        # Générer un nom unique pour le blob
        blob_name = generate_blob_name(filename, incident_id)
        
        # Créer le conteneur s'il n'existe pas
        try:
            container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
            container_client.create_container()
        except Exception:
            # Le conteneur existe déjà ou autre erreur (on continue)
            pass
        
        # Uploader le fichier
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER_NAME, 
            blob=blob_name
        )
        
        # Lire le contenu du fichier
        file.seek(0)  # Retour au début du fichier
        file_content = file.read()
        
        # Upload avec métadonnées
        blob_client.upload_blob(
            file_content, 
            overwrite=True,
            metadata={
                'incident_id': str(incident_id),
                'original_filename': filename,
                'upload_date': datetime.utcnow().isoformat(),
                'uploaded_by': 'flask_app'
            }
        )
        
        print(f"✅ Fichier uploadé: {blob_name}")
        return blob_name, len(file_content)
        
    except AzureError as e:
        print(f"❌ Erreur Azure lors de l'upload: {e}")
        raise
    except Exception as e:
        print(f"❌ Erreur lors de l'upload: {e}")
        raise

def download_file_from_blob(blob_name):
    """Télécharger un fichier depuis Azure Blob Storage"""
    try:
        # Mode mock pour tests
        if AZURE_STORAGE_MODE == 'mock':
            print(f"🧪 MODE MOCK: Simulation de téléchargement pour {blob_name}")
            # Créer un fichier fictif pour le téléchargement
            mock_content = f"Contenu simulé du fichier {blob_name}\nGénéré en mode mock."
            return io.BytesIO(mock_content.encode('utf-8'))
        
        blob_service_client = create_blob_service_client()
        if not blob_service_client:
            raise Exception("Impossible de créer le client Blob Storage")
        
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER_NAME, 
            blob=blob_name
        )
        
        # Télécharger le blob
        download_stream = blob_client.download_blob()
        file_content = download_stream.readall()
        
        return io.BytesIO(file_content)
        
    except AzureError as e:
        print(f"❌ Erreur Azure lors du téléchargement: {e}")
        raise
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        raise

def delete_file_from_blob(blob_name):
    """Supprimer un fichier d'Azure Blob Storage"""
    try:
        # Mode mock pour tests
        if AZURE_STORAGE_MODE == 'mock':
            print(f"🧪 MODE MOCK: Simulation de suppression pour {blob_name}")
            print(f"✅ [MOCK] Fichier supprimé: {blob_name}")
            return
        
        blob_service_client = create_blob_service_client()
        if not blob_service_client:
            raise Exception("Impossible de créer le client Blob Storage")
        
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER_NAME, 
            blob=blob_name
        )
        
        blob_client.delete_blob()
        print(f"✅ Fichier supprimé: {blob_name}")
        
    except AzureError as e:
        print(f"❌ Erreur Azure lors de la suppression: {e}")
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        raise

# ========================================
# ROUTES FLASK
# ========================================

@app.route('/')
def index():
    """Page d'accueil avec la liste des incidents"""
    try:
        # Récupérer tous les incidents avec le nombre de documents
        incidents = db.session.query(Incident).order_by(Incident.date_incident.desc()).all()
        
        # Ajouter le nombre de documents à chaque incident
        for incident in incidents:
            incident.documents_count = len(incident.documents)
        
        return render_template('incidents.html', incidents=incidents)
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des incidents: {e}")
        # Mode dégradé avec des données de démonstration
        incidents_demo = [
            {'id': 1, 'titre': 'Connexion Azure en cours...', 'severite': 'Info', 
             'date_incident': datetime.now(), 'documents_count': 0}
        ]
        return render_template('incidents.html', incidents=incidents_demo)

@app.route('/incident/<int:id>')
def detail_incident(id):
    """Page de détail d'un incident avec ses documents"""
    try:
        incident = Incident.query.get_or_404(id)
        documents = IncidentDocument.query.filter_by(incident_id=id).order_by(IncidentDocument.upload_date.desc()).all()
        
        return render_template('detail.html', incident=incident, documents=documents)
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'incident {id}: {e}")
        flash(f'Erreur lors de la récupération de l\'incident: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/ajouter')
def ajouter_incident_form():
    """Formulaire d'ajout d'incident avec upload de documents"""
    return render_template('ajouter.html', 
                         max_file_size_mb=MAX_FILE_SIZE // (1024*1024),
                         allowed_extensions=ALLOWED_EXTENSIONS)

@app.route('/ajouter-incident', methods=['POST'])
def ajouter_incident():
    """Traitement de l'ajout d'incident avec documents"""
    try:
        titre = request.form.get('titre', '').strip()
        description = request.form.get('description', '').strip()
        severite = request.form.get('severite', 'Moyenne')
        
        # Validation des données obligatoires
        if not titre:
            flash('Le titre de l\'incident est obligatoire', 'error')
            return redirect(url_for('ajouter_incident_form'))
        
        # Validation de la sévérité (doit correspondre aux contraintes de la base)
        severites_valides = ['Critique', 'Élevée', 'Moyenne', 'Faible']
        if severite not in severites_valides:
            flash(f'Sévérité invalide. Valeurs acceptées: {", ".join(severites_valides)}', 'error')
            return redirect(url_for('ajouter_incident_form'))
        
        # Créer le nouvel incident
        nouvel_incident = Incident(
            titre=titre,
            description=description,
            severite=severite,
            date_incident=datetime.now()
        )
        
        # Sauvegarder l'incident pour obtenir l'ID
        db.session.add(nouvel_incident)
        db.session.commit()
        incident_id = nouvel_incident.id
        
        # Traitement des fichiers uploadés
        uploaded_files = request.files.getlist('documents')
        uploaded_count = 0
        
        for file in uploaded_files:
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Vérifier la taille du fichier
                    file.seek(0, os.SEEK_END)
                    file_size = file.tell()
                    file.seek(0)
                    
                    if file_size > MAX_FILE_SIZE:
                        flash(f'Fichier {file.filename} trop volumineux (max {MAX_FILE_SIZE // (1024*1024)} MB)', 'warning')
                        continue
                    
                    # Uploader vers Azure Blob Storage
                    blob_name, actual_size = upload_file_to_blob(file, file.filename, incident_id)
                    
                    # Enregistrer la référence en base
                    document = IncidentDocument(
                        incident_id=incident_id,
                        filename=file.filename,
                        blob_name=blob_name,
                        file_size=actual_size,
                        content_type=file.content_type or 'application/octet-stream',
                        uploaded_by='User'
                    )
                    
                    db.session.add(document)
                    uploaded_count += 1
                    
                except Exception as e:
                    print(f"❌ Erreur lors de l'upload de {file.filename}: {e}")
                    flash(f'Erreur lors de l\'upload de {file.filename}: {str(e)}', 'warning')
        
        # Commit final
        db.session.commit()
        
        success_msg = f'Incident "{titre}" ajouté avec succès!'
        if uploaded_count > 0:
            success_msg += f' {uploaded_count} document(s) attaché(s).'
        
        flash(success_msg, 'success')
        return redirect(url_for('detail_incident', id=incident_id))
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors de l'ajout de l'incident: {e}")
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'error')
        return redirect(url_for('ajouter_incident_form'))

@app.route('/document/<int:doc_id>/download')
def download_document(doc_id):
    """Télécharger un document depuis Azure Blob Storage"""
    try:
        document = IncidentDocument.query.get_or_404(doc_id)
        
        # Télécharger depuis Azure Blob Storage
        file_stream = download_file_from_blob(document.blob_name)
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=document.filename,
            mimetype=document.content_type
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement du document {doc_id}: {e}")
        flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/document/<int:doc_id>/delete', methods=['POST'])
def delete_document(doc_id):
    """Supprimer un document"""
    try:
        document = IncidentDocument.query.get_or_404(doc_id)
        incident_id = document.incident_id
        
        # Supprimer de Azure Blob Storage
        delete_file_from_blob(document.blob_name)
        
        # Supprimer de la base de données
        db.session.delete(document)
        db.session.commit()
        
        flash(f'Document "{document.filename}" supprimé avec succès', 'success')
        return redirect(url_for('detail_incident', id=incident_id))
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors de la suppression du document {doc_id}: {e}")
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
        return redirect(url_for('index'))

# ========================================
# API REST
# ========================================

@app.route('/api/incidents')
def api_incidents():
    """API REST - Liste des incidents avec informations documents"""
    try:
        incidents = Incident.query.order_by(Incident.date_incident.desc()).all()
        return jsonify([incident.to_dict() for incident in incidents])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/incidents/<int:id>')
def api_incident_detail(id):
    """API REST - Détail d'un incident avec ses documents"""
    try:
        incident = Incident.query.get_or_404(id)
        documents = IncidentDocument.query.filter_by(incident_id=id).all()
        
        result = incident.to_dict()
        result['documents'] = [doc.to_dict() for doc in documents]
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========================================
# ROUTES DE DIAGNOSTIC
# ========================================

@app.route('/health')
def health_check():
    """Health check pour monitoring"""
    try:
        # Test de connexion base de données
        db.session.execute(text('SELECT 1'))
        
        # Test de connexion Azure Storage
        blob_service_client = create_blob_service_client()
        if blob_service_client:
            # Tenter de lister les conteneurs pour vérifier la connexion
            try:
                containers = list(blob_service_client.list_containers(max_results=1))
                storage_status = "OK"
            except:
                storage_status = "ERROR"
        else:
            storage_status = "ERROR"
        
        return jsonify({
            'status': 'healthy',
            'database': 'OK',
            'storage': storage_status,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/storage-test')
def storage_test():
    """Test de la connexion Azure Storage"""
    try:
        blob_service_client = create_blob_service_client()
        if not blob_service_client:
            return jsonify({'error': 'Impossible de créer le client Blob Storage'}), 500
        
        # Informations sur le compte de stockage
        account_info = blob_service_client.get_account_information()
        
        # Liste des conteneurs
        containers = list(blob_service_client.list_containers())
        
        return jsonify({
            'status': 'success',
            'account_kind': account_info.get('account_kind'),
            'sku_name': account_info.get('sku_name'),
            'containers': [c.name for c in containers],
            'target_container': AZURE_STORAGE_CONTAINER_NAME,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# ========================================
# INITIALISATION ET DÉMARRAGE
# ========================================

def init_database():
    """Initialiser la base de données avec les nouvelles tables"""
    try:
        print("🔧 Initialisation de la base de données...")
        
        # Créer les tables si elles n'existent pas
        db.create_all()
        
        # Vérifier si la table incidents contient des données
        incidents_count = Incident.query.count()
        documents_count = IncidentDocument.query.count()
        
        print(f"📊 Base de données initialisée: {incidents_count} incident(s), {documents_count} document(s)")
        
        if incidents_count == 0:
            print("📝 Ajout de données de démonstration...")
            demo_incidents = [
                Incident(titre="Panne réseau principal", severite="Critique", 
                        description="Perte de connectivité sur le réseau principal"),
                Incident(titre="Serveur web lent", severite="Moyenne",
                        description="Ralentissement constaté sur le serveur web"),
                Incident(titre="Mise à jour sécurité planifiée", severite="Faible",
                        description="Maintenance programmée pour mise à jour sécurité")
            ]
            
            for incident in demo_incidents:
                db.session.add(incident)
            
            db.session.commit()
            print("✅ Données de démonstration ajoutées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Démarrage Flask - Incidents Réseau avec Azure Storage")
    print("=" * 70)
    print(f"☁️  Serveur Azure SQL: {AZURE_SQL_SERVER}")
    print(f"💾 Base de données: {AZURE_SQL_DATABASE}")
    print(f"👤 Utilisateur: {AZURE_SQL_USERNAME}")
    print(f"📦 Storage Account: {AZURE_STORAGE_ACCOUNT_NAME}")
    print(f"🗂️  Container: {AZURE_STORAGE_CONTAINER_NAME}")
    print("=" * 70)
    print("📋 Routes disponibles:")
    print("   📊 / - Liste des incidents avec documents")
    print("   ➕ /ajouter - Ajouter un incident avec fichiers")
    print("   🔍 /incident/<id> - Détail incident et téléchargements")
    print("   📡 /api/incidents - API REST avec infos documents")
    print("   🔧 /health - Health check (DB + Storage)")
    print("   🧪 /storage-test - Test Azure Storage")
    print("=" * 70)
    
    # Initialiser la base de données
    if init_database():
        print("🌐 Application accessible sur: http://localhost:5004")
        
        # Démarrage de l'application
        port = int(os.environ.get('FLASK_PORT', 5004))
        debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
        
        app.run(host='0.0.0.0', port=port, debug=debug)
    else:
        print("❌ Impossible de démarrer l'application - problème de base de données")