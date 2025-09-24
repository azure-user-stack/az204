#!/usr/bin/env python3
"""
Diagnostic pour Azure Blob Storage - Configuration et authentification
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def diagnose_azure_storage_config():
    """Diagnostiquer la configuration Azure Storage"""
    print("🔍 DIAGNOSTIC AZURE BLOB STORAGE")
    print("=" * 60)
    print(f"⏰ Diagnostic effectué le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Vérifier les variables d'environnement
    print("📋 VARIABLES D'ENVIRONNEMENT:")
    print("-" * 40)
    
    storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    storage_account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
    storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    
    print(f"AZURE_STORAGE_ACCOUNT_NAME: {storage_account_name}")
    print(f"AZURE_STORAGE_CONTAINER_NAME: {container_name}")
    
    if storage_account_key:
        if storage_account_key.startswith('https://'):
            print("❌ AZURE_STORAGE_ACCOUNT_KEY: ⚠️  Contient une URL SAS (invalide)")
            print(f"   Valeur: {storage_account_key[:50]}...")
            print("   💡 Solution: Remplacez par une vraie clé de compte ou utilisez AZURE_STORAGE_CONNECTION_STRING")
        else:
            print("✅ AZURE_STORAGE_ACCOUNT_KEY: Présent et semble valide")
            print(f"   Longueur: {len(storage_account_key)} caractères")
    else:
        print("❌ AZURE_STORAGE_ACCOUNT_KEY: Non défini")
    
    if storage_connection_string:
        print("✅ AZURE_STORAGE_CONNECTION_STRING: Présent")
        print(f"   Longueur: {len(storage_connection_string)} caractères")
    else:
        print("❌ AZURE_STORAGE_CONNECTION_STRING: Non défini")
    
    print()
    
    # 2. Analyser le type de configuration
    print("🔧 ANALYSE DE LA CONFIGURATION:")
    print("-" * 40)
    
    if storage_account_key and storage_account_key.startswith('https://'):
        print("❌ PROBLÈME DÉTECTÉ:")
        print("   La variable AZURE_STORAGE_ACCOUNT_KEY contient une URL SAS")
        print("   au lieu d'une clé de compte de stockage.")
        print()
        print("🔧 SOLUTIONS POSSIBLES:")
        print()
        print("OPTION 1 - Utiliser une clé de compte de stockage:")
        print("   1. Allez dans le portail Azure")
        print("   2. Ouvrez votre compte de stockage 'stappincidents'")
        print("   3. Allez dans 'Clés d'accès' (Access keys)")
        print("   4. Copiez une des clés (key1 ou key2)")
        print("   5. Remplacez AZURE_STORAGE_ACCOUNT_KEY par cette clé")
        print()
        print("OPTION 2 - Utiliser une chaîne de connexion:")
        print("   1. Dans le portail Azure, compte de stockage > Clés d'accès")
        print("   2. Copiez la 'Chaîne de connexion' complète")
        print("   3. Définissez AZURE_STORAGE_CONNECTION_STRING avec cette valeur")
        print("   4. Commentez ou supprimez AZURE_STORAGE_ACCOUNT_KEY")
        print()
        print("OPTION 3 - Utiliser un SAS Token (configuration avancée):")
        print("   1. Modifiez le code pour utiliser un SAS token")
        print("   2. Configurez l'URL SAS correctement dans l'application")
        
    elif storage_connection_string:
        print("✅ Configuration avec chaîne de connexion détectée")
        if "AccountKey=" in storage_connection_string:
            print("   Type: Authentification par clé")
        else:
            print("   Type: Autre méthode d'authentification")
            
    elif storage_account_name and storage_account_key:
        print("✅ Configuration avec nom de compte + clé détectée")
        
    else:
        print("❌ Configuration incomplète")
        print("   Il manque des informations d'authentification")
    
    print()
    
    # 3. Test de configuration
    print("🧪 TEST DE CONFIGURATION:")
    print("-" * 40)
    
    try:
        from azure.storage.blob import BlobServiceClient
        print("✅ Module azure.storage.blob importé avec succès")
        
        # Tenter de créer un client
        if storage_connection_string:
            print("🔄 Test avec chaîne de connexion...")
            try:
                client = BlobServiceClient.from_connection_string(storage_connection_string)
                print("✅ Client BlobServiceClient créé via connection string")
            except Exception as e:
                print(f"❌ Erreur avec connection string: {e}")
                
        elif storage_account_name and storage_account_key and not storage_account_key.startswith('https://'):
            print("🔄 Test avec nom de compte + clé...")
            try:
                account_url = f"https://{storage_account_name}.blob.core.windows.net"
                client = BlobServiceClient(account_url=account_url, credential=storage_account_key)
                print("✅ Client BlobServiceClient créé via account key")
            except Exception as e:
                print(f"❌ Erreur avec account key: {e}")
                
        else:
            print("❌ Configuration insuffisante pour créer un client")
            
    except ImportError as e:
        print(f"❌ Erreur d'import Azure Storage: {e}")
        print("   💡 Exécutez: pip install azure-storage-blob")
    
    print()
    print("=" * 60)
    print("✅ Diagnostic terminé")

if __name__ == "__main__":
    diagnose_azure_storage_config()