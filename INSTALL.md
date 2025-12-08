# 🔧 Guide d'Installation - Football Manager 5v5

> **Version 2.0 - Material Design Hybride**

Ce guide vous accompagne étape par étape dans l'installation et la configuration de l'application.

## 📋 Prérequis Système

### 🐍 Python
- **Version requise :** Python 3.10 ou supérieur (recommandé : **Python 3.13**)
- **Vérification :** `python --version` ou `python3 --version`
- **Installation :** [python.org](https://www.python.org/downloads/)

### 🗄️ Base de Données (au choix)
**Option 1 : XAMPP (Recommandé pour Windows)**
- Télécharger : [apachefriends.org](https://www.apachefriends.org/)
- Inclut MySQL/MariaDB + phpMyAdmin
- Installation simple et interface graphique

**Option 2 : MySQL/MariaDB autonome**
- [MySQL](https://dev.mysql.com/downloads/)
- [MariaDB](https://mariadb.org/download/)

**Option 3 : PostgreSQL**
- [PostgreSQL](https://www.postgresql.org/download/)

### 🔧 Outils Développement (optionnel)
- **Git** : Pour cloner le projet
- **IDE recommandé** : VS Code avec extension Python

## 🚀 Installation Rapide

### Windows - Script Automatique

```cmd
# 1. Cloner le projet
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam

# 2. Lancer l'installation automatique
run_hybrid.bat
```

Le script `run_hybrid.bat` effectue automatiquement :
- Activation de l'environnement virtuel
- Installation des dépendances
- Lancement de l'application hybride

### Linux/macOS - Installation Manuelle

```bash
# 1. Cloner le projet
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam

# 2. Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r logiciel-gestion/desktop_app/requirements.txt

# 4. Lancer l'application
python logiciel-gestion/desktop_app/hybrid_main.py
```

## 🛠️ Installation Manuelle Détaillée

### Étape 1 : Clonage du Projet

```bash
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam
```

### Étape 2 : Environnement Virtuel

**Windows (PowerShell) :**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt) :**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS :**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> **Erreur PowerShell ?**
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

### Étape 3 : Installation des Dépendances

```bash
cd logiciel-gestion/desktop_app
pip install -r requirements.txt
```

**Dépendances installées :**
- `PySide6` : Interface graphique Qt6
- `qt-material` : Thème Material Design
- `SQLAlchemy` : ORM base de données
- `PyMySQL` : Connecteur MySQL
- `psycopg2-binary` : Connecteur PostgreSQL  
- `bcrypt` : Chiffrement des mots de passe
- `python-dotenv` : Variables d'environnement

### Étape 4 : Configuration Base de Données

#### Option A : MySQL/MariaDB (Recommandé)

**1. Démarrer le serveur MySQL**

*Avec XAMPP :*
- Ouvrir XAMPP Control Panel
- Démarrer le module **MySQL**

*Serveur autonome :*
```bash
# Linux
sudo systemctl start mysql

# Windows (service)
net start mysql
```

**2. Créer la base de données**

```sql
-- Via phpMyAdmin ou ligne de commande MySQL
CREATE DATABASE football_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**3. Configurer la connexion**

Copier le fichier de configuration :
```bash
cp .env.example .env
```

Éditer `.env` :
```env
# Configuration base de données
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=football_manager
DB_USER=root
DB_PASSWORD=

# Configuration application
SECRET_KEY=your-secret-key-here
DEBUG=True
```

#### Option B : PostgreSQL

**1. Créer la base de données**
```sql
CREATE DATABASE football_manager;
```

**2. Configuration `.env`**
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=football_manager
DB_USER=postgres
DB_PASSWORD=your_password
```

### Étape 5 : Initialisation

**1. Créer les tables**
```bash
python create_superadmin.py
```

**2. Premier lancement**
```bash
python hybrid_main.py
```

## 🔐 Création du Super Administrateur

Lors du premier lancement, créez un compte super administrateur :

```bash
cd logiciel-gestion/desktop_app
python create_superadmin.py
```

**Informations demandées :**
- Nom d'utilisateur
- Email
- Mot de passe (minimum 8 caractères)

## ▶️ Lancement de l'Application

### Version Hybride (Recommandée)

**Windows :**
```cmd
run_hybrid.bat
```

**Linux/macOS :**
```bash
# Activer l'environnement
source .venv/bin/activate

# Lancer l'application
python logiciel-gestion/desktop_app/hybrid_main.py
```

### Versions Alternatives

**Version classique :**
```bash
python logiciel-gestion/desktop_app/app/main.py
```

## 🎨 Fonctionnalités Version Hybride

### Interface Material Design
- ✅ Thème **light_teal** avec couleurs football
- ✅ **HoverButton** avec effets de survol
- ✅ **Composants uniformisés** sur toute l'application
- ✅ **Navigation fluide** avec retour dashboard

### Améliorations Techniques
- ✅ **Gestion avancée des contraintes** DB avec rollback
- ✅ **Validation des doublons** username/email
- ✅ **Messages d'erreur contextuels**
- ✅ **Code optimisé** (30% fichiers obsolètes supprimés)

## 🔧 Dépannage

### Problèmes Courants

**Erreur "qt-material not found"**
```bash
pip install qt-material
```

**Erreur base de données MySQL**
```bash
# Installer le connecteur
pip install PyMySQL

# Vérifier le service MySQL
# Windows
net start mysql

# Linux  
sudo systemctl status mysql
```

**Erreur permissions PowerShell**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Module PySide6 non trouvé**
```bash
pip install --upgrade PySide6
```

### Vérification Installation

**Tester les imports Python :**
```python
import PySide6
import qt_material
import sqlalchemy
import bcrypt
print("✅ Toutes les dépendances sont installées")
```

**Vérifier la base de données :**
- Accéder à phpMyAdmin (http://localhost/phpmyadmin)
- Vérifier que la base `football_manager` existe
- Tester la connexion

## 📞 Support

En cas de problème :

1. **Vérifier les prérequis** (Python, base de données)
2. **Consulter les logs** dans la console
3. **Vérifier le fichier .env** 
4. **Tester l'installation étape par étape**

## 🔄 Mise à Jour

Pour mettre à jour vers une nouvelle version :

```bash
git pull origin main
pip install --upgrade -r logiciel-gestion/desktop_app/requirements.txt
```

---

> 🏆 **Application prête !** Vous pouvez maintenant utiliser Football Manager 5v5 avec sa nouvelle interface Material Design.