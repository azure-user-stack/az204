# 🔧 GUIDE DE RÉSOLUTION - Azure Blob Storage Authentication

## ❌ Problème Actuel

Votre SAS token actuel a seulement des permissions de **lecture** (`sp=r`), mais l'application a besoin de permissions d'**écriture** pour télécharger des fichiers.

**SAS Token actuel:**
```
https://stappincidents.blob.core.windows.net/appincidentsdocs?sp=r&st=2025-09-24T01:05:25Z&se=2025-09-24T09:20:25Z&sv=2024-11-04&sr=c&sig=hCt4IgMvWSACWYgqflnSQQ4C5uWVAqaggEZ3TgYpaZo%3D
```

**Analyse des permissions:**
- `sp=r` = Lecture seulement ❌
- `sr=c` = Container level ✅
- `se=2025-09-24T09:20:25Z` = Expire dans quelques heures ⚠️

## ✅ Solutions

### SOLUTION 1: Générer un nouveau SAS Token avec permissions d'écriture

1. **Aller dans le portail Azure**
   - Connectez-vous à https://portal.azure.com
   - Naviguez vers votre compte de stockage `stappincidents`

2. **Générer un SAS Token**
   - Cliquez sur "Shared access signature" dans le menu de gauche
   - **Permissions requises:** Cochez `Read`, `Write`, `Delete`, `List`
   - **Services:** Cochez `Blob`
   - **Resource types:** Cochez `Container` et `Object`
   - **Expiration:** Définissez une date d'expiration appropriée
   - Cliquez sur "Generate SAS and connection string"

3. **Récupérer le SAS Token**
   - Copiez la "SAS token" (qui commence par `?sv=...`)
   - OU copiez l'"Connection string" complète

4. **Mettre à jour la configuration**
   
   **Option A - Utiliser le SAS Token:**
   ```env
   AZURE_STORAGE_CONNECTION_STRING="https://stappincidents.blob.core.windows.net?VOTRE_NOUVEAU_SAS_TOKEN"
   ```
   
   **Option B - Utiliser la Connection String:**
   ```env
   AZURE_STORAGE_CONNECTION_STRING="VOTRE_CONNECTION_STRING_COMPLETE"
   ```

### SOLUTION 2: Utiliser la clé de compte de stockage (Plus simple)

1. **Dans le portail Azure, compte de stockage `stappincidents`**
   - Allez dans "Access keys" (Clés d'accès)
   - Copiez "Connection string" de Key1 ou Key2

2. **Mettre à jour le .env**
   ```env
   # Commenter la ligne actuelle
   # AZURE_STORAGE_CONNECTION_STRING="https://stappincidents.blob.core.windows.net/appincidentsdocs?sp=r..."
   
   # Ajouter la vraie connection string
   AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=stappincidents;AccountKey=VOTRE_CLE;EndpointSuffix=core.windows.net"
   ```

### SOLUTION 3: Configuration pour le développement local (Émulateur)

Si vous voulez tester localement sans Azure:

```env
# Pour Azurite (émulateur local)
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
```

## 🧪 Test de la configuration

Une fois la configuration mise à jour, redémarrez l'application et testez:

1. **Redémarrer Flask:**
   ```bash
   python app.py
   ```

2. **Tester l'upload:**
   - Allez sur http://localhost:5004/ajouter
   - Essayez de télécharger un fichier

3. **Vérifier les logs:**
   Les logs devraient afficher:
   ```
   ✅ Connexion Azure Blob Storage via connection string
   ```
   ou
   ```
   🔗 Connexion Azure Blob Storage via SAS URL
   ```

## 📋 Actions immédiates recommandées

1. **Générer un nouveau SAS Token** avec permissions `rwdl` (read, write, delete, list)
2. **Définir une expiration** d'au moins 24-48 heures pour les tests
3. **Mettre à jour le .env** avec la nouvelle configuration
4. **Redémarrer l'application**

## ⚠️ Notes importantes

- **Sécurité:** Ne commitez jamais les vraies clés dans Git
- **Expiration:** Les SAS tokens expirent, planifiez le renouvellement
- **Permissions:** Utilisez le principe du moindre privilège
- **Monitoring:** Surveillez l'utilisation de votre stockage Azure

---

**Status**: Configuration à corriger pour permettre l'upload de fichiers.
**Priority**: Haute - bloque les fonctionnalités d'upload