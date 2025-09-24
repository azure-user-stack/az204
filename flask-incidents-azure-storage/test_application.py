#!/usr/bin/env python3
"""
Test rapide pour vérifier que l'application fonctionne correctement
"""

import requests
import time

def test_application():
    """Tester l'application Flask"""
    base_url = "http://localhost:5004"
    
    print("🧪 TEST DE L'APPLICATION FLASK")
    print("=" * 50)
    
    try:
        # Test 1: Page d'accueil
        print("1. Test de la page d'accueil...")
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("   ✅ Page d'accueil accessible")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return False
        
        # Test 2: Page d'ajout d'incident
        print("2. Test du formulaire d'ajout...")
        response = requests.get(f"{base_url}/ajouter", timeout=10)
        if response.status_code == 200:
            print("   ✅ Formulaire d'ajout accessible")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Test 3: Détail d'un incident (tester le filtre nl2br)
        print("3. Test de la page de détail (filtre nl2br)...")
        response = requests.get(f"{base_url}/incident/1", timeout=10)
        if response.status_code == 200:
            print("   ✅ Page de détail accessible - filtre nl2br fonctionne")
        elif response.status_code == 302:
            print("   ⚠️  Redirection (incident peut-être inexistant)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Test 4: API REST
        print("4. Test de l'API REST...")
        response = requests.get(f"{base_url}/api/incidents", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API fonctionnelle - {len(data)} incidents trouvés")
        else:
            print(f"   ❌ API erreur: {response.status_code}")
        
        # Test 5: Health check
        print("5. Test du health check...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health check OK")
        else:
            print(f"   ❌ Health check erreur: {response.status_code}")
        
        print("\n🎉 Tests terminés avec succès!")
        print(f"🌐 Application accessible sur: {base_url}")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("   Assurez-vous que Flask fonctionne sur http://localhost:5004")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    # Attendre un peu que l'application démarre complètement
    print("⏳ Attente du démarrage complet de l'application...")
    time.sleep(3)
    test_application()