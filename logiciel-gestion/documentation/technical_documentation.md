# Documentation Technique - Football Manager 5v5

## Architecture

### Modèle MVC
```
app/
├── models/          # Modèles de données (SQLAlchemy)
│   ├── db.py        # Configuration base de données  
│   ├── user.py      # Modèle utilisateur
│   ├── terrain.py   # Modèle terrain
│   └── reservation.py # Modèle réservation
├── controllers/     # Logique métier
│   ├── auth_controller.py
│   ├── terrain_controller.py
│   └── reservation_controller.py
├── views/           # Interface utilisateur (PySide6)
│   ├── login_view.py
│   └── dashboard_view.py
├── services/        # Services externes
│   └── cpp_bridge.py
└── utils/           # Utilitaires
    └── hashing.py   # Sécurité bcrypt
```

## Technologies

### Stack principal
- **Frontend** : PySide6 (Qt6) avec Material Design
- **Backend** : Python 3.8+ avec SQLAlchemy ORM
- **Base de données** : MySQL (via XAMPP)
- **Sécurité** : bcrypt pour les mots de passe
- **Module C++** : Optionnel pour calculs avancés

### Dépendances
```
PySide6>=6.5.0
SQLAlchemy>=2.0.0
bcrypt>=4.0.0
mysql-connector-python>=8.0.0
```

## Configuration

### Base de données
- **Serveur** : localhost:3306 (XAMPP)
- **Database** : foot5
- **Utilisateur** : root (pas de mot de passe par défaut)
- **Configuration** : `app/config.py`

### Scripts d'installation
- `setup_admin.py` : Création automatique des utilisateurs et données de test
- `check_install.py` : Vérification de l'installation
- `verify_install.sql` : Tests de la base de données

## Sécurité

### Authentification
- Hachage bcrypt avec salt automatique
- Sessions sécurisées 
- Validation des entrées utilisateur
- Gestion des rôles (superadmin, gestionnaire, utilisateur)

### Base de données
- Requêtes préparées (SQLAlchemy)
- Validation des données
- Transactions ACID

## Déploiement

### Installation automatisée
1. **QUICKSTART.md** - Guide 5 minutes
2. **INSTALL.md** - Installation détaillée  
3. **Scripts automatiques** - setup_admin.py + check_install.py

### Structure des fichiers
```
logiciel-gestion/
├── database/        # Scripts SQL
│   ├── schema_mysql.sql
│   └── seed_data_mysql_fixed.sql
├── desktop_app/     # Application principale
└── documentation/   # Cette documentation
```

## Tests et validation

### Vérification automatique
- `check_install.py` vérifie toutes les dépendances
- Tests de connexion base de données
- Validation du démarrage applicatif

### Données de test
- Utilisateurs par défaut avec vrais hachages bcrypt
- Terrains d'exemple (Terrain A, B, C)
- Réservations de démonstration

## Développement

### Environnement
- Python 3.8+ recommandé
- XAMPP pour MySQL local
- Git pour versioning (branche docs/update-documentation)

### Architecture des vues
- QMainWindow principal avec QTabWidget
- QTableWidget pour les listes
- QDialog pour les formulaires
- Thème sombre personnalisé

## Performance

### Optimisations
- Lazy loading des données
- Index sur les colonnes de recherche
- Cache des requêtes fréquentes
- Module C++ optionnel pour calculs lourds
