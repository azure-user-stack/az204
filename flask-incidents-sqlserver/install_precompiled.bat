@echo off
echo 🚀 Installation rapide Flask-SQLServer avec pyodbc pré-compilé
echo =========================================================
echo.

echo 💡 Cette méthode évite les problèmes de compilation Visual C++
echo ⚡ Installation uniquement de packages pré-compilés (wheels)
echo.

cd /d "%~dp0"

echo 🔧 1. Désinstallation des versions existantes (si nécessaire)...
pip uninstall -y Flask Flask-SQLAlchemy SQLAlchemy pyodbc Werkzeug 2>nul

echo.
echo 📦 2. Installation des packages pré-compilés...
echo.

echo    📌 Installation Flask (pré-compilé)...
pip install --only-binary=all Flask==2.3.3
if %errorlevel% neq 0 (
    echo    ❌ Erreur installation Flask
    pause
    exit /b 1
)

echo    📌 Installation SQLAlchemy (pré-compilé)...
pip install --only-binary=all SQLAlchemy==1.4.53
if %errorlevel% neq 0 (
    echo    ❌ Erreur installation SQLAlchemy
    pause
    exit /b 1
)

echo    📌 Installation Flask-SQLAlchemy (pré-compilé)...
pip install --only-binary=all Flask-SQLAlchemy==2.5.1
if %errorlevel% neq 0 (
    echo    ❌ Erreur installation Flask-SQLAlchemy
    pause
    exit /b 1
)

echo    📌 Installation pyodbc (pré-compilé) - CRITIQUE...
pip install --only-binary=all pyodbc==4.0.39
if %errorlevel% neq 0 (
    echo    ❌ Erreur installation pyodbc
    echo    💡 Essayez: pip install --find-links https://pypi.org/simple/ --only-binary=:all: pyodbc
    pause
    exit /b 1
)

echo    📌 Installation Werkzeug (pré-compilé)...
pip install --only-binary=all Werkzeug==2.3.7
if %errorlevel% neq 0 (
    echo    ❌ Erreur installation Werkzeug
    pause
    exit /b 1
)

echo.
echo ✅ 3. Vérification des installations...
python -c "import flask; print('✅ Flask:', flask.__version__)" 2>nul || echo "❌ Flask non importable"
python -c "import sqlalchemy; print('✅ SQLAlchemy:', sqlalchemy.__version__)" 2>nul || echo "❌ SQLAlchemy non importable"
python -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy:', flask_sqlalchemy.__version__)" 2>nul || echo "❌ Flask-SQLAlchemy non importable"
python -c "import pyodbc; print('✅ pyodbc:', pyodbc.version)" 2>nul || echo "❌ pyodbc non importable"

echo.
echo 🎉 Installation terminée avec succès!
echo.
echo 📋 Prochaines étapes:
echo    1. Vérifiez SQL Server: Get-Service -Name "*SQL*"
echo    2. Testez la connexion: python test_windows_auth.py
echo    3. Lancez l'app: python app.py
echo.
echo 💡 Si vous rencontrez encore des erreurs, essayez:
echo    pip install --find-links https://pypi.org/simple/ --only-binary=:all: pyodbc
echo.
pause