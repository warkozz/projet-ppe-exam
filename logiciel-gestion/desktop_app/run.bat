@echo off
title Football Manager 5v5 - Setup et Lancement
echo 🏟️ Football Manager 5v5 - Configuration automatique
echo ================================================

echo 📦 Vérification de l'environnement virtuel...
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

echo 🔧 Activation de l'environnement...
call venv\Scripts\activate.bat

echo 📥 Installation/Mise à jour des dépendances...
pip install -r requirements.txt

echo 🗄️ Vérification de la configuration...
if not exist .env (
    echo Configuration par défaut utilisée
)

echo 🔍 Vérification de l'installation...
python check_install.py
if errorlevel 1 (
    echo.
    echo ❌ Des problèmes ont été détectés.
    echo Consultez les messages ci-dessus et:
    echo 1. Démarrez XAMPP MySQL
    echo 2. Exécutez: python setup_admin.py
    pause
    exit /b 1
)

echo.
echo ✅ Configuration validée!
echo 🚀 Lancement de l'application...
python hybrid_main.py

pause
