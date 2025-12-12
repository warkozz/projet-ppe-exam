# 🚀 Installation Rapide - Football Manager 5v5

## ⚡ Setup en 5 minutes

### 1️⃣ Prérequis
- **Python 3.10+** : [Télécharger Python](https://www.python.org/downloads/)
- **XAMPP** : [Télécharger XAMPP](https://www.apachefriends.org/fr/)

### 2️⃣ Installation XAMPP
1. Installez XAMPP
2. Démarrez le **Control Panel XAMPP**
3. Cliquez sur **"Start"** pour **MySQL** (statut doit être vert)

### 3️⃣ Cloner le projet
```bash
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam
```

### 4️⃣ Setup automatique
```bash
# Windows
run_hybrid.bat

# Linux/macOS
./setup.sh
```

### 5️⃣ Première connexion
L'application va s'ouvrir. Connectez-vous avec :

**👑 Superadmin (accès total)**
- Username: `admin`
- Password: `admin123`

**🔑 Manager (gestion)**  
- Username: `manager`
- Password: `manager123`

**👤 Utilisateur (consultation)**
- Username: `user1`
- Password: `user123`

## 🔧 Installation Manuelle (si problème)

### 1. Créer l'environnement virtuel
```bash
python -m venv .venv
```

### 2. Activer l'environnement
```bash
# Windows
.venv\Scripts\activate

# Linux/macOS  
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
cd logiciel-gestion/desktop_app
pip install -r requirements.txt
```

### 4. Créer la base de données
Dans phpMyAdmin (http://localhost/phpmyadmin) :
1. Créer une base nommée `foot5`
2. Importer `logiciel-gestion/database/schema_mysql.sql`

### 5. Initialiser les données
```bash
python setup_admin.py
```

### 6. Lancer l'application
```bash
python hybrid_main.py
```

## ❌ Résolution de Problèmes

### Erreur "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erreur "Connection refused" (Base de données)
1. Vérifiez que XAMPP MySQL est démarré (vert)
2. Vérifiez que la base `foot5` existe
3. Exécutez `python setup_admin.py`

### Erreur "bcrypt" ou "qt-material"  
```bash
pip install --upgrade pip
pip install bcrypt qt-material
```

### Interface ne s'affiche pas
```bash
pip install --upgrade PySide6
```

## 📞 Support

- **Documentation complète** : `README.md`
- **Installation détaillée** : `INSTALL.md`
- **Changements** : `CHANGELOG.md`

## ✅ Vérification Fonctionnelle

Après installation, vérifiez que :
- ✅ L'application se lance sans erreur
- ✅ Connexion avec admin/admin123 fonctionne
- ✅ Le calendrier affiche des réservations d'exemple
- ✅ Les points rouges apparaissent sur les dates avec réservations
- ✅ Vous pouvez créer une nouvelle réservation
- ✅ Les statistiques du dashboard s'affichent

🎉 **Installation terminée !** L'application est prête à utiliser.