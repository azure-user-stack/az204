@echo off
echo 🚀 Script de configuration Flask-SQLServer (Windows)
echo 📝 Résolution du conflit Python 3.13/SQLAlchemy

echo.
echo 🔍 Vérification de l'environnement actuel...
python --version
echo.

echo ⚠️  IMPORTANT: SQLAlchemy 3.x n'est pas compatible avec Python 3.13
echo 💡 Solutions disponibles:
echo    1. Downgrade vers SQLAlchemy 1.4 (recommandé)
echo    2. Utiliser Python 3.11 dans un environnement virtuel
echo.

echo 🔧 Solution 1: Installation des versions compatibles...
echo Désinstallation des versions problématiques...
pip uninstall -y SQLAlchemy Flask-SQLAlchemy

echo Installation des versions compatibles...
pip install SQLAlchemy==1.4.53
pip install Flask-SQLAlchemy==2.5.1
pip install Flask==2.3.3
pip install pyodbc==4.0.39
pip install Werkzeug==2.3.7

echo.
echo ✅ Installation terminée!
echo.
echo 📋 Prochaines étapes:
echo 1. Testez la connexion: python test_windows_auth.py
echo 2. Créez la base: sqlcmd -S localhost\SQLEXPRESS -E -i setup_database.sql  
echo 3. Lancez l'app: python app.py
echo.
pause