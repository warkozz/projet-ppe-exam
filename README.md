# ⚽ Football Manager 5v5 - Gestion de Terrains

> **Version 2.0 - Material Design Hybride** 🎨

Application desktop moderne de gestion de terrains de football à 5 avec interface Material Design, système de réservations intelligent, gestion multi-utilisateurs et contrôle des disponibilités en temps réel.

## 🚀 Nouveautés Version 2.0

- ✨ **Interface Material Design** avec qt-material
- 🎨 **Thème football uniforme** (couleurs vertes cohérentes)
- 🔄 **Architecture hybride** combinant ancien fonctionnel + nouveau design
- 🛡️ **Gestion avancée des contraintes** de base de données
- 🧹 **Code optimisé et nettoyé** (suppression de 30% des fichiers obsolètes)
- 📱 **Interface responsive** et moderne

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Premier Lancement](#premier-lancement)
- [Création du Superadmin](#création-du-superadmin)
- [Utilisation](#utilisation)
- [Gestion des Rôles](#gestion-des-rôles)
- [Module C++ (Optionnel)](#module-c-optionnel)
- [Structure du Projet](#structure-du-projet)
- [Technologies Utilisées](#technologies-utilisées)

## ✨ Fonctionnalités

### 🏆 Gestion des Réservations
- ✅ **Création, modification et annulation** de réservations
- ✅ **Vérification automatique des conflits** avec validation
- ✅ **Filtrage intelligent** par utilisateur, date et terrain
- ✅ **Recherche d'utilisateurs en temps réel** avec suggestions
- ✅ **Créneaux horaires dynamiques** (8h-20h par tranches de 2h)
- ✅ **Gestion des statuts** (active, cancelled) avec historique
- ✅ **Interface hybrid moderne** avec boutons Material Design

### 🏟️ Gestion des Terrains
- ✅ **CRUD complet** : Ajout, modification, suppression
- ✅ **Système actif/inactif** avec boutons toggle visuels
- ✅ **Descriptions et emplacements** détaillés
- ✅ **Interface unifiée** avec HoverButton et style football
- ✅ **Validation des données** avant opérations

### 👥 Gestion des Utilisateurs
- ✅ **Système de rôles complet** (superadmin, admin, user)
- ✅ **Authentification sécurisée** bcrypt + validation avancée
- ✅ **Gestion des contraintes** username/email uniques
- ✅ **Interface moderne** avec toggle actif/inactif
- ✅ **Protection contre les doublons** avec rollback automatique
- ✅ **Messages d'erreur contextuels** et informatifs

### 🎨 Interface Utilisateur 2.0
- ✅ **Material Design** avec qt-material et thème light_teal
- ✅ **Thème football cohérent** (PRIMARY: #4CAF50, tons verts)
- ✅ **HoverButton standardisés** avec effets de survol
- ✅ **Dashboard hybride** avec statistiques en temps réel
- ✅ **Navigation fluide** avec retour au dashboard
- ✅ **Composants uniformisés** (boutons, listes, formulaires)
- ✅ **Style CSS cohérent** sur toute l'application

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.10+** (recommandé : Python 3.13)
- **MySQL/MariaDB** (avec XAMPP recommandé) ou **PostgreSQL** (base de données)
- **Git** (pour cloner le projet)
- **CMake + compilateur C++** (optionnel, pour le module C++ de vérification de conflits)
  - Linux : `sudo apt install cmake g++`
  - Windows : Visual Studio Build Tools ou MinGW

### Vérification de Python

```bash
python --version
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/)

### Option XAMPP (Recommandé pour Windows)

XAMPP inclut MySQL/MariaDB et phpMyAdmin pour une gestion facile :
- Téléchargez XAMPP depuis [apachefriends.org](https://www.apachefriends.org/)
- Installez et démarrez le module MySQL

## 📦 Installation

### 🚀 Méthode Rapide - Version Hybride (Recommandée)

**Windows :**
```cmd
# 1. Cloner le projet
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam

# 2. Lancer le script d'installation automatique
run_hybrid.bat
```

**Linux/Mac :**
```bash
# 1. Cloner le projet
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam

# 2. Créer l'environnement virtuel et installer
python -m venv .venv
source .venv/bin/activate
pip install -r logiciel-gestion/desktop_app/requirements.txt

# 3. Lancer l'application hybride
python logiciel-gestion/desktop_app/hybrid_main.py
```

### 🛠️ Installation Manuelle Détaillée

### 1. Cloner le projet

```bash
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam
```

### 2. Créer un environnement virtuel

#### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> **Note :** Si vous rencontrez une erreur de politique d'exécution sous PowerShell :
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

### 3. Installer les dépendances

```bash
cd logiciel-gestion/desktop_app
pip install -r requirements.txt
```

> **Note :** PyMySQL est déjà inclus dans requirements.txt pour MySQL/MariaDB

## ⚙️ Configuration

### 1. Configuration de la base de données

#### Option A : MySQL/MariaDB avec XAMPP (recommandé pour Windows)

1. **Démarrer XAMPP**
   - Lancez le Control Panel XAMPP
   - Démarrez le module MySQL
   - Vérifiez que le statut est "Running" (vert)

2. **Créer la base de données via phpMyAdmin**
   - Ouvrez phpMyAdmin : http://localhost/phpmyadmin
   - Cliquez sur "Nouvelle base de données" (ou "New")
   - Nom : `foot5`
   - Interclassement : `utf8mb4_unicode_ci`
   - Cliquez sur "Créer"

3. **Importer le schéma**
   - Dans phpMyAdmin, sélectionnez la base `foot5`
   - Cliquez sur l'onglet "Importer"
   - Cliquez sur "Choisir un fichier"
   - Sélectionnez `logiciel-gestion/database/schema_mysql.sql`
   - Cliquez sur "Exécuter" en bas de la page

4. **Importer les données de test**
   - Toujours dans l'onglet "Importer"
   - Sélectionnez `logiciel-gestion/database/seed_data_mysql.sql`
   - Cliquez sur "Exécuter"
   - ✅ Vous devriez voir "Importation réussie"

#### Option B : MySQL en ligne de commande

```bash
# Depuis le dossier racine du projet
mysql -u root -p foot5 < logiciel-gestion/database/schema_mysql.sql
mysql -u root -p foot5 < logiciel-gestion/database/seed_data_mysql.sql
```

#### Option C : PostgreSQL

```bash
# Créer la base
createdb foot5

# Importer le schéma et les données
psql -U postgres -d foot5 -f logiciel-gestion/database/schema_postgres.sql
psql -U postgres -d foot5 -f logiciel-gestion/database/seed_data.sql
```

### 2. Configuration des variables d'environnement

Créez un fichier `.env` dans le dossier `logiciel-gestion/desktop_app/` :

**Pour XAMPP (MySQL sans mot de passe par défaut) :**
```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/foot5
SECRET_KEY=votre-cle-secrete-unique-a-changer
```

**Pour MySQL avec mot de passe :**
```env
DATABASE_URL=mysql+pymysql://root:votremotdepasse@localhost:3306/foot5
SECRET_KEY=votre-cle-secrete-unique-a-changer
```

**Pour PostgreSQL :**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/foot5
SECRET_KEY=votre-cle-secrete-unique-a-changer
```

> **Important :** 
> - Pour XAMPP par défaut, laissez le mot de passe vide (`:@localhost`)
> - Si vous avez défini un mot de passe MySQL, remplacez `:@` par `:votremotdepasse@`
> - Changez `SECRET_KEY` par une valeur unique et sécurisée

### 3. Créer un fichier .env rapidement

```bash
# Windows
copy logiciel-gestion\desktop_app\.env.example logiciel-gestion\desktop_app\.env

# Linux/macOS
cp logiciel-gestion/desktop_app/.env.example logiciel-gestion/desktop_app/.env
```

## 🚀 Premier Lancement

### Procédure complète pour la première utilisation

#### 1. Activer l'environnement virtuel

**Windows PowerShell :**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows CMD :**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS :**
```bash
source .venv/bin/activate
```

> **Note :** Si vous obtenez une erreur de politique d'exécution sous PowerShell :
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> .\.venv\Scripts\Activate.ps1
> ```

#### 2. Se placer dans le bon dossier

```bash
cd logiciel-gestion/desktop_app
```

#### 3. Lancer l'application

```bash
python -m app.main
```

L'interface graphique devrait s'ouvrir. Si une erreur apparaît, vérifiez :
- ✅ XAMPP/MySQL est démarré
- ✅ La base de données `foot5` existe et contient les tables
- ✅ Le fichier `.env` est correctement configuré
- ✅ Toutes les dépendances sont installées

#### 4. Connexion initiale

Si vous avez importé les données de test, utilisez ces identifiants :

**👑 Superadmin** (accès complet)
- Username : `admin`
- Password : `admin123`
- Email : `admin@foot5.com`

**🔑 Manager** (gestion terrains et réservations)
- Username : `manager` 
- Password : `manager123`
- Email : `manager@foot5.com`

**👤 Utilisateur standard** (consultation)
- Username : `user1`
- Password : `user123`
- Email : `user1@foot5.com`

> **⚠️ Sécurité :** Changez ces mots de passe par défaut dès la première connexion !

### 5. Initialiser les données (RECOMMANDÉ)

**Option A : Script automatique (recommandé)**
```bash
# Depuis le dossier logiciel-gestion/desktop_app
python setup_admin.py
```
Ce script crée automatiquement :
- ✅ Toutes les tables de base de données
- ✅ Utilisateurs par défaut avec mots de passe sécurisés
- ✅ Terrains d'exemple
- ✅ Quelques réservations de test

**Option B : Import SQL manuel**
Dans phpMyAdmin :
1. Sélectionner la base `foot5`
2. Importer `logiciel-gestion/database/seed_data_mysql_fixed.sql`

**Option C : Création manuelle du superadmin**
```bash
# Si vous voulez seulement créer un admin
python -c "
from app.models.db import SessionLocal
from app.models.user import User
from app.utils.hashing import hash_password

db = SessionLocal()
admin = User(
    username='admin',
    email='admin@foot5.com',
    password_hash=hash_password('admin123'),
    role='superadmin'
)
db.add(admin)
db.commit()
db.close()
print('✅ Superadmin créé!')
"
```

## 📖 Utilisation

### Système de rôles

L'application gère trois niveaux d'accès :

- **👑 superadmin** : Accès total (gestion utilisateurs, terrains, réservations)
- **🔑 admin** : Gestion des terrains et réservations uniquement
- **👤 user** : Consultation uniquement

### Dashboard Principal

Après connexion, vous accédez au dashboard avec les modules suivants (selon votre rôle) :

#### 1. **Gestion des Réservations**
   - Créer une nouvelle réservation
   - Modifier une réservation existante
   - Annuler une réservation
   - Filtrer par utilisateur, date ou terrain
   - Rechercher un utilisateur
   - Afficher toutes les réservations
   - Interface moderne avec filtres avancés

#### 2. **Gestion des Terrains**
   - Ajouter un nouveau terrain
   - Modifier les informations d'un terrain
   - Activer/désactiver un terrain
   - Supprimer un terrain
   - Gestion de la disponibilité

#### 3. **Gestion des Utilisateurs** (superadmin uniquement)
   - Créer un nouvel utilisateur
   - Modifier les informations d'un utilisateur
   - Supprimer un utilisateur
   - Gérer les rôles (superadmin, admin, user)
   - Recherche et filtrage d'utilisateurs

### Bouton Déconnexion

Un bouton "Déconnexion" permet de changer d'utilisateur sans fermer l'application.

### Fonctionnalités avancées

#### Déconnexion
Un bouton "Déconnexion" permet de changer d'utilisateur sans fermer l'application.

#### Vérification des conflits
L'application vérifie automatiquement les conflits de réservation et désactive les terrains non disponibles pour un créneau donné.

### Raccourcis Clavier

- `Ctrl+Q` : Quitter l'application
- `Entrée` : Confirmer/Rechercher
- `Échap` : Annuler

## 🔐 Gestion des Rôles

L'application gère trois niveaux de droits :

### Superadmin
- ✅ Accès total à toutes les fonctionnalités
- ✅ Gestion des utilisateurs (création, modification, suppression)
- ✅ Gestion des terrains
- ✅ Gestion des réservations
- ✅ Attribution des rôles

### Admin
- ✅ Gestion des terrains
- ✅ Gestion des réservations
- ❌ Pas d'accès à la gestion des utilisateurs

### User (Utilisateur standard)
- ✅ Consultation des réservations
- ✅ Création de réservations pour soi-même
- ❌ Pas d'accès à la gestion des terrains
- ❌ Pas d'accès à la gestion des utilisateurs

> **Note :** Seul un superadmin peut créer d'autres comptes via l'interface "Gestion utilisateurs".

## � Module C++ (Optionnel)

Le projet inclut un module C++ optionnel pour optimiser la vérification des conflits de réservation.

### Prérequis

- **CMake** (version 3.10+)
- **Compilateur C++**
  - Linux : `g++` (GNU Compiler Collection)
  - Windows : Visual Studio Build Tools ou MinGW
  - macOS : Xcode Command Line Tools

### Installation des prérequis

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install cmake g++ build-essential
```

#### Windows
- Option 1 : Visual Studio Build Tools
  - Téléchargez depuis [visualstudio.microsoft.com](https://visualstudio.microsoft.com/downloads/)
  - Installez "Desktop development with C++"

- Option 2 : MinGW
  - Téléchargez depuis [mingw-w64.org](https://www.mingw-w64.org/)
  - Ajoutez le dossier `bin` au PATH

#### macOS
```bash
xcode-select --install
brew install cmake
```

### Compilation du module

```bash
# Depuis la racine du projet
cd logiciel-gestion/cpp

# Créer le dossier build
mkdir build
cd build

# Générer les fichiers de build
cmake ..

# Compiler
# Linux/macOS
make

# Windows (Visual Studio)
cmake --build . --config Release
```

### Utilisation

Une fois compilé, le module sera automatiquement utilisé par l'application pour :
- Vérifier les conflits de réservation plus rapidement
- Optimiser les requêtes de disponibilité des terrains

Si le module n'est pas compilé, l'application utilisera une version Python (légèrement plus lente mais fonctionnelle).

## �📁 Structure du Projet

```
projet-ppe-exam/
├── logiciel-gestion/
│   ├── database/
│   │   ├── schema_mysql.sql         # Schéma MySQL
│   │   ├── schema_postgres.sql      # Schéma PostgreSQL
│   │   ├── seed_data_mysql.sql      # Données de test MySQL
│   │   └── seed_data.sql            # Données de test PostgreSQL
│   ├── desktop_app/
│   │   ├── app/
│   │   │   ├── controllers/         # Logique métier
│   │   │   │   ├── auth_controller.py
│   │   │   │   ├── reservation_controller.py
│   │   │   │   ├── terrain_controller.py
│   │   │   │   └── user_controller.py
│   │   │   ├── models/              # Modèles de données
│   │   │   │   ├── db.py
│   │   │   │   ├── user.py
│   │   │   │   ├── terrain.py
│   │   │   │   └── reservation.py
│   │   │   ├── views/               # Interfaces utilisateur
│   │   │   │   ├── login_view.py
│   │   │   │   ├── dashboard_view.py
│   │   │   │   ├── reservation_management_view.py
│   │   │   │   ├── terrain_management_view.py
│   │   │   │   └── user_management_view.py
│   │   │   ├── services/            # Services techniques
│   │   │   │   └── cpp_bridge.py
│   │   │   ├── utils/               # Utilitaires
│   │   │   │   └── hashing.py
│   │   │   ├── config.py            # Configuration
│   │   │   ├── app.py               # Application principale
│   │   │   └── main.py              # Point d'entrée
│   │   ├── requirements.txt         # Dépendances Python
│   │   ├── create_superadmin.py     # Script création superadmin
│   │   └── README.md                # Documentation (obsolète - voir README principal)
│   ├── cpp/                         # Module C++ (optionnel)
│   └── documentation/
└── README.md                        # Ce fichier
```

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.13** - Langage principal
- **SQLAlchemy** - ORM pour la base de données
- **bcrypt** - Hachage sécurisé des mots de passe
- **python-dotenv** - Gestion des variables d'environnement

### Frontend
- **PySide6** - Framework Qt pour l'interface graphique
- **Qt Designer** - Pour la conception d'interface (optionnel)

### Base de données
- **MySQL** / **PostgreSQL** - Stockage des données
- **PyMySQL** / **psycopg2** - Connecteurs de base de données

### Architecture
- **MVC (Model-View-Controller)** - Pattern architectural
- **SQLAlchemy ORM** - Abstraction de la base de données

## 🐛 Résolution des problèmes courants

### Erreur : "Module 'app' not found"
```bash
# Assurez-vous d'être dans le bon dossier
cd logiciel-gestion/desktop_app
python -m app.main
```

### Erreur : "Can't connect to MySQL server"
1. Vérifiez que MySQL/PostgreSQL est démarré
2. Vérifiez les identifiants dans le fichier `.env`
3. Testez la connexion :
   ```bash
   mysql -u root -p
   ```

### Erreur : "ExecutionPolicy" (Windows PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### Erreur : "No module named 'PySide6'"
```bash
# Vérifiez que l'environnement virtuel est activé
pip install -r requirements.txt
```

### L'interface ne s'affiche pas correctement
- Vérifiez que vous utilisez Python 3.8+
- Réinstallez PySide6 :
  ```bash
  pip uninstall PySide6
  pip install PySide6
  ```

## 📝 Notes de développement

### Créer un utilisateur superadmin manuellement

Si vous n'avez pas importé les données de test :

```python
python -c "
from app.models.db import SessionLocal
from app.models.user import User
from app.utils.hashing import hash_password

db = SessionLocal()
admin = User(
    username='admin',
    email='admin@foot5.com',
    password_hash=hash_password('admin123'),
    role='superadmin'
)
db.add(admin)
db.commit()
print('Superadmin créé avec succès!')
"
```

### Réinitialiser la base de données

**Avec phpMyAdmin (XAMPP) :**
1. Ouvrez phpMyAdmin : http://localhost/phpmyadmin
2. Sélectionnez la base `foot5`
3. Cliquez sur "Supprimer" pour la base entière
4. Créez une nouvelle base `foot5`
5. Réimportez les fichiers SQL (schema puis seed_data)

**En ligne de commande :**

```bash
# MySQL/XAMPP
mysql -u root -p -e "DROP DATABASE IF EXISTS foot5; CREATE DATABASE foot5;"
mysql -u root -p foot5 < logiciel-gestion/database/schema_mysql.sql
mysql -u root -p foot5 < logiciel-gestion/database/seed_data_mysql.sql

# PostgreSQL
dropdb foot5
createdb foot5
psql foot5 < logiciel-gestion/database/schema_postgres.sql
psql foot5 < logiciel-gestion/database/seed_data.sql
```

## ▶️ Lancement de l'Application

### 🚀 Version 2.0 Hybride (Recommandée)

**Méthode rapide - Windows :**
```cmd
run_hybrid.bat
```

**Méthode manuelle :**
```bash
# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# OU
source .venv/bin/activate      # Linux/macOS

# Lancer l'application hybride Material Design
python logiciel-gestion/desktop_app/hybrid_main.py
```

### 📱 Interface Version 2.0

**Au lancement, vous verrez :**
- 🎨 **Interface Material Design** avec thème football vert
- 🏠 **Dashboard moderne** avec statistiques en temps réel
- 📊 **Cartes informatives** (terrains actifs, réservations du jour)
- 🎯 **Navigation centralisée** avec boutons Material

**Connexion :**
- Utilisez le **superadmin créé** lors de l'installation
- Interface de connexion **intégrée au thème**
- Messages d'erreur **contextuels et informatifs**

## 🔄 Commandes Utiles

### Lancement rapide (après installation initiale)

```bash
# Windows - Version hybride
run_hybrid.bat

# Linux/macOS - Version hybride
source .venv/bin/activate
python logiciel-gestion/desktop_app/hybrid_main.py
```

### Versions disponibles

```bash
# Version 2.0 - Hybride Material Design (RECOMMANDÉE)
python hybrid_main.py

# Version 1.0 - Classic (si nécessaire)
python -m app.main
```

### Mettre à jour les dépendances

```bash
pip install --upgrade -r requirements.txt
```

### Vérifier la connexion à la base

```bash
python -c "from app.models.db import SessionLocal; db = SessionLocal(); print('✅ Connexion réussie!'); db.close()"
```

## 🤝 Contribution

Ce projet est un Projet Personnel Encadré (PPE). Pour toute question ou suggestion, contactez l'équipe de développement.

## 📄 Licence

Ce projet est développé dans le cadre d'un projet éducatif.

## 👥 Auteurs

- **Développement** - Équipe PPE Exam 2025
- **Encadrement** - Établissement scolaire

## 📞 Support

Pour toute question ou problème :
1. Consultez la section [Résolution des problèmes](#résolution-des-problèmes-courants)
2. Vérifiez les logs de l'application
3. Contactez votre encadrant

## 📚 Documentation Complémentaire

- 📋 **[INSTALL.md](INSTALL.md)** - Guide d'installation détaillé
- 🚀 **[VERSION_2.0.md](VERSION_2.0.md)** - Nouveautés et changelog v2.0
- 🎨 **[THEME_UNIFORME.md](THEME_UNIFORME.md)** - Documentation du design system
- 🏗️ **[README_HYBRIDE.md](README_HYBRIDE.md)** - Architecture hybride

## 📊 Statistiques du Projet

- **📝 Lignes de code :** ~8,000+ lignes Python
- **🎨 Fichiers interface :** 5 vues principales Material Design
- **🗄️ Tables DB :** 3 tables principales avec contraintes
- **📦 Dépendances :** 6 packages Python principaux
- **🧹 Optimisation :** 30% de réduction de fichiers v2.0

## 🏆 Fonctionnalités Avancées v2.0

### Material Design
- ✅ Thème `light_teal` avec couleurs football
- ✅ HoverButton avec animations fluides
- ✅ Components standardisés et réutilisables

### Gestion Robuste
- ✅ Validation contraintes DB avec rollback automatique
- ✅ Messages d'erreur contextuels et informatifs  
- ✅ Interface toggle pour statuts actif/inactif

### Dashboard Intelligence
- ✅ Statistiques temps réel (terrains, réservations)
- ✅ Navigation centralisée avec retour dashboard
- ✅ Actualisation automatique toutes les minutes

---

**Dernière mise à jour :** Décembre 2024  
**Version :** 2.0.0 - Material Design Hybride  
**Statut :** ✅ Production Ready
