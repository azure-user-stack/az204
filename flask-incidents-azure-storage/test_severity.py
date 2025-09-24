#!/usr/bin/env python3
"""
Script de test pour vérifier les valeurs de sévérité
"""

import requests
import time
from datetime import datetime

def test_severity_values():
    """Tester les valeurs de sévérité permises"""
    base_url = "http://localhost:5004"
    
    # Valeurs de sévérité à tester
    severites_valides = ['Critique', 'Élevée', 'Moyenne', 'Faible']
    severites_invalides = ['Info', 'Urgente', 'Basse', 'Normal']
    
    print("🧪 Test des valeurs de sévérité")
    print("=" * 50)
    
    # Vérifier que le serveur répond
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            print("❌ Le serveur ne répond pas correctement")
            return
    except requests.exceptions.RequestException:
        print("❌ Impossible de se connecter au serveur sur http://localhost:5004")
        print("⚠️  Assurez-vous que l'application Flask est en cours d'exécution")
        return
    
    print("✅ Serveur accessible")
    
    # Test des valeurs valides
    print("\n🟢 Test des valeurs VALIDES:")
    for severite in severites_valides:
        test_data = {
            'titre': f'Test incident - {severite}',
            'description': f'Test pour vérifier la sévérité {severite}',
            'severite': severite
        }
        
        try:
            response = requests.post(f"{base_url}/ajouter-incident", data=test_data, timeout=10)
            if response.status_code == 302 or response.status_code == 200:
                print(f"   ✅ {severite}: Accepté")
            else:
                print(f"   ❌ {severite}: Rejeté (status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {severite}: Erreur - {e}")
        
        time.sleep(1)  # Petite pause entre les tests
    
    # Test des valeurs invalides
    print("\n🔴 Test des valeurs INVALIDES:")
    for severite in severites_invalides:
        test_data = {
            'titre': f'Test incident invalide - {severite}',
            'description': f'Test pour vérifier le rejet de la sévérité {severite}',
            'severite': severite
        }
        
        try:
            response = requests.post(f"{base_url}/ajouter-incident", data=test_data, timeout=10)
            if response.status_code == 302 or response.status_code == 200:
                print(f"   ❌ {severite}: Accepté (ne devrait pas l'être!)")
            else:
                print(f"   ✅ {severite}: Correctement rejeté (status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {severite}: Erreur - {e}")
        
        time.sleep(1)  # Petite pause entre les tests
    
    print("\n📊 Test terminé!")
    print("💡 Consultez l'interface web pour voir les incidents créés")
    print(f"🌐 URL: {base_url}")

if __name__ == "__main__":
    test_severity_values()