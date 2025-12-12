@echo off
title Football Manager 5v5 - Version Hybride
echo ========================================
echo   FOOTBALL MANAGER 5V5 - VERSION HYBRIDE
echo ========================================
echo.

echo 🔧 Activation de l'environnement virtuel...
cd /d "C:\xampp\htdocs\projet-ppe-exam"

if not exist .venv (
    echo ❌ Environnement virtuel non trouvé!
    echo Créez-le avec: python -m venv .venv
    pause
    exit /b 1
)

call .venv\Scripts\activate

echo 📦 Vérification des dépendances...
cd logiciel-gestion\desktop_app
python -c "import PySide6, qt_material, sqlalchemy, pymysql, bcrypt, dotenv" 2>nul
if errorlevel 1 (
    echo ⚠️ Installation des dépendances manquantes...
    pip install -r requirements.txt
)

echo 🗄️ Vérification de la base de données...
python -c "from app.models.db import check_db_connection; exit(0 if check_db_connection() else 1)" 2>nul
if errorlevel 1 (
    echo.
    echo ❌ Connexion à la base de données échouée!
    echo.
    echo 📋 ACTIONS REQUISES:
    echo 1. Démarrez XAMPP et activez MySQL
    echo 2. Créez la base 'foot5' dans phpMyAdmin
    echo 3. Exécutez: python setup_admin.py
    echo.
    pause
    exit /b 1
)

echo ✅ Tout est prêt!
echo 🚀 Lancement de l'application...
python hybrid_main.py

if errorlevel 1 (
    echo.
    echo ❌ L'application s'est fermée avec une erreur.
    pause
)