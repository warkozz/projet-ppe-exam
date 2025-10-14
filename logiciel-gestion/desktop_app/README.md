# Guide de lancement de l'application avec XAMPP (MySQL)

## Prérequis
- XAMPP (MySQL/MariaDB et phpMyAdmin)
- Python 3.13+ et pip
- Les dépendances Python (voir ci-dessous)

## 1. Préparer la base de données avec XAMPP/phpMyAdmin
1. Lancez XAMPP et démarrez le module MySQL.
2. Ouvrez phpMyAdmin (http://localhost/phpmyadmin).
3. Créez une base de données nommée `foot5`.
4. Importez le fichier `database/schema_mysql.sql` pour créer les tables.
5. Importez le fichier `database/seed_data_mysql.sql` pour insérer les données de test.

## 2. Installer les dépendances Python
Ouvrez un terminal dans le dossier `desktop_app` et exécutez :
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install pymysql
```

## 3. Configurer la connexion à la base
- Copiez `.env.example` en `.env` et adaptez la ligne `DATABASE_URL` avec votre mot de passe MySQL :
	```
	DATABASE_URL=mysql+pymysql://root:motdepasse@localhost:3306/foot5
	```
	(remplacez `motdepasse` par votre mot de passe MySQL, ou laissez vide si aucun mot de passe)

## 4. Lancer l'application
Dans le dossier `desktop_app`, lancez :
```powershell
python -m app.main
```

L'interface graphique devrait s'ouvrir. Si une erreur apparaît, vérifiez la configuration de la base et les dépendances.

# Gestion des utilisateurs et rôles

L'application gère trois niveaux de droits :
- **superadmin** : accès total (gestion utilisateurs, terrains, réservations)
- **admin** : gestion terrains et réservations
- **user** : consultation uniquement

Un bouton "Déconnexion" permet de changer d'utilisateur sans fermer l'application.

Pour créer un superadmin :
1. Activez l'environnement virtuel : `.venv\Scripts\activate`
2. Lancez : `python create_superadmin.py`
3. Identifiants :
	- Nom d'utilisateur : **Administrateur**
	- Mot de passe : **admin123**

Pour créer d'autres comptes, utilisez l'interface "Gestion utilisateurs" (réservée au superadmin).

---
Pour toute question, consultez la documentation ou contactez l'équipe projet.
# Desktop App - Foot5 (Gestion interne)

Application desktop multiplateforme (Windows/Linux) pour la gestion interne d'un terrain foot 5x5 en salle.

## Prérequis
- Python 3.10+
- PostgreSQL (ou adapter DATABASE_URL pour MySQL)
- CMake + compilateur C++ (g++ sous Linux / MSVC sous Windows)

## Installation rapide
1. Créer un env virtuel : `python -m venv venv` puis activer.
2. `pip install -r requirements.txt`
3. Configurer `.env` (copier `.env.example` et modifier).
4. Initialiser la BD : `psql -U <user> -d postgres -f database/schema_postgres.sql` puis créer la DB et exécuter `seed_data.sql`.
5. Compiler le module C++ (optionnel) : `cd desktop_app/cpp && mkdir build && cd build && cmake .. && make`
6. Lancer : `python desktop_app/app/main.py`
