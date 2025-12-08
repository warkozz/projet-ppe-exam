@echo off
title Football Manager 5v5 - Version Hybride
echo ========================================
echo   FOOTBALL MANAGER 5V5 - VERSION HYBRIDE
echo ========================================
echo.
echo Demarrage de l'application...
echo.

cd /d "C:\xampp\htdocs\projet-ppe-exam"
call .venv\Scripts\activate
python "logiciel-gestion\desktop_app\hybrid_main.py"

pause