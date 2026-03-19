# 📚 Étape 8 : Documentation

## 📖 Documentation Complète du Projet

La documentation de Football Manager 5v5 est **exhaustive et professionnelle**, conçue pour faciliter l'installation, l'utilisation et la maintenance de l'application.

## 🚀 Manuel d'Installation

### Installation Express (5 minutes)

#### Prérequis Système
- **OS :** Windows 10+ (testé), Linux/macOS (compatible)
- **Python :** 3.8+ avec pip
- **XAMPP :** MySQL/Apache activés
- **Mémoire :** 4GB RAM minimum, 8GB recommandé
- **Stockage :** 500MB libres

#### Procédure Automatisée
```bash
# 1. Cloner le projet
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam

# 2. Installation automatique (Windows)
.\QUICKSTART.bat

# 3. Ou installation manuelle
pip install -r logiciel-gestion/desktop_app/requirements.txt
cd logiciel-gestion/desktop_app
python setup_admin.py
```

#### Vérification Installation
```bash
# Script de diagnostic complet
python check_install.py

# Résultats attendus:
✅ Python 3.8+ détecté
✅ Dépendances installées
✅ MySQL/XAMPP opérationnel  
✅ Base de données 'foot5' créée
✅ Données de test insérées
✅ Application prête à démarrer
```

### Configuration Base de Données

#### Paramètres MySQL (XAMPP Standard)
```python
# Configuration automatique - config.py
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'username': 'root',
    'password': '',  # Vide par défaut XAMPP
    'database': 'foot5',
    'charset': 'utf8mb4'
}
```

#### Structure Créée Automatiquement
- **Base :** foot5
- **Tables :** users, terrains, reservations
- **Index :** Optimisation requêtes fréquentes
- **Contraintes :** Intégrité référentielle
- **Données test :** Utilisateurs, terrains, réservations d'exemple

## 👥 Manuel Utilisateur

### Démarrage de l'Application

#### Lancement Standard
```bash
# Windows (recommandé)
cd logiciel-gestion/desktop_app
run.bat

# Ou directement avec Python
cd logiciel-gestion/desktop_app
python hybrid_main.py
```

#### Interface de Connexion
![Interface moderne avec thème Material Design]

**Comptes de démonstration :**
- **Superadmin :** `admin` / `admin123`
  - Accès complet, gestion utilisateurs
- **Gestionnaire :** `manager` / `manager123`  
  - Gestion terrains assignés
- **Utilisateur :** `user1` / `user123`
  - Création de réservations personnelles

### Navigation dans l'Application

#### Dashboard Principal
**Vue d'accueil avec métriques temps réel :**
- 📊 **Terrains actifs :** Nombre disponible
- 📅 **Réservations du jour :** Planning aujourd'hui  
- 👥 **Utilisateurs inscrits :** Total comptes
- 🔄 **Actualisation automatique :** Toutes les minutes

#### Onglets de Navigation
1. **Dashboard :** Vue d'ensemble et statistiques
2. **Utilisateurs :** Gestion comptes (Superadmin uniquement)
3. **Terrains :** Administration infrastructures
4. **Réservations :** Planification et gestion
5. **Calendrier :** Vue mensuelle interactive

### Guide par Fonctionnalité

#### 👤 Gestion des Utilisateurs (Superadmin)
**Création d'un nouvel utilisateur :**
1. Onglet "Utilisateurs" → Bouton "➕ Ajouter"
2. Formulaire complet :
   - Nom d'utilisateur (unique)
   - Email (validation automatique)
   - Mot de passe (8+ caractères)
   - Rôle (superadmin / admin / user)
3. "Sauvegarder" → Validation et création

**Modification utilisateur existant :**
1. Sélectionner ligne dans tableau
2. Bouton "✏️ Modifier" → Formulaire pré-rempli
3. Modifications → "Sauvegarder"

#### 🏟️ Gestion des Terrains
**Ajout nouveau terrain :**
1. Onglet "Terrains" → "➕ Nouveau terrain"
2. Informations :
   - Nom descriptif (ex: "Terrain A")
   - Localisation (ex: "Salle Nord")
   - Statut actif (par défaut)
3. "Créer" → Terrain disponible pour réservations

**Activation/Désactivation :**
- Toggle switch visuel par terrain
- Terrains inactifs = plus de nouvelles réservations
- Réservations existantes conservées

#### 📅 Système de Réservations
**Nouvelle réservation :**
1. Onglet "Réservations" → "➕ Nouvelle réservation"
2. Sélections obligatoires :
   - **Terrain :** Liste terrains actifs
   - **Date :** Calendrier interactif
   - **Heure début :** Sélecteur temps
   - **Heure fin :** Validation durée
   - **Utilisateur :** Si admin/gestionnaire
3. **Validation automatique :**
   - Vérification conflits existants
   - Cohérence horaire (fin > début)
   - Disponibilité terrain
4. "Confirmer" → Réservation créée (statut "En attente")

**Gestion des réservations :**
- **Filtres :** Date, statut, terrain, utilisateur
- **Actions :** Modifier, confirmer, annuler
- **Statuts visuels :**
  - 🟡 En attente (Orange)
  - 🟢 Confirmée (Vert)  
  - 🔴 Annulée (Rouge)

#### 📅 Calendrier Interactif
**Navigation temporelle :**
- Flèches mois précédent/suivant
- Sélection directe mois/année
- Bouton "Aujourd'hui" retour rapide

**Marqueurs visuels :**
- **Points rouges :** Jours avec réservations
- **Clic sur date :** Liste réservations du jour
- **Ajout direct :** Double-clic → Formulaire réservation

**Synchronisation temps réel :**
- Mise à jour automatique lors des modifications
- Actualisation cache intelligent
- Performance optimisée

### Raccourcis Clavier

| Raccourci | Action |
|-----------|--------|
| **Ctrl+1** | Onglet Dashboard |
| **Ctrl+2** | Onglet Utilisateurs |
| **Ctrl+3** | Onglet Terrains |
| **Ctrl+4** | Onglet Réservations |
| **Ctrl+5** | Onglet Calendrier |
| **Ctrl+N** | Nouvelle réservation |
| **Ctrl+R** | Actualiser données |
| **F5** | Rafraîchir vue active |
| **Échap** | Fermer formulaire/modal |

## 🔧 Documentation Technique

### Architecture Logicielle

#### Pattern MVC Implémenté
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     MODÈLE      │    │   CONTRÔLEUR     │    │      VUE        │
│                 │    │                  │    │                 │
│ • User          │◄──►│ • AuthController │◄──►│ • LoginView     │
│ • Terrain       │    │ • TerrainCtrl    │    │ • DashboardView │
│ • Reservation   │    │ • ReservCtrl     │    │ • CalendarView  │
│ • Database      │    │ • Business Logic │    │ • Material UI   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

#### Technologies et Versions
- **Python :** 3.8+ (orienté objet, type hints)
- **PySide6 :** 6.5+ (Qt6 framework GUI)
- **SQLAlchemy :** 2.0+ (ORM moderne, async ready)
- **MySQL :** 8.0+ (base de données relationnelle)
- **qt-material :** Theme Material Design
- **bcrypt :** 4.0+ (hachage sécurisé)

#### Structure des Modules
```python
# Exemple d'organisation - models/reservation.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Reservation(Base):
    """
    Modèle de réservation avec validation métier
    
    Attributs:
        id: Clé primaire auto-incrémentée
        user_id: Référence utilisateur (FK)  
        terrain_id: Référence terrain (FK)
        start: Date/heure début (DATETIME)
        end: Date/heure fin (DATETIME)
        status: Statut (ENUM)
    
    Relations:
        user: Many-to-One vers User
        terrain: Many-to-One vers Terrain
    
    Méthodes:
        validate_time_slot(): Validation cohérence temporelle
        check_conflicts(): Détection conflits réservations
        to_dict(): Sérialisation pour API/UI
    """
    __tablename__ = 'reservations'
    
    # Définition colonnes avec contraintes
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # ... autres colonnes
    
    # Relations ORM avec lazy loading
    user = relationship("User", back_populates="reservations", 
                       lazy="select")
    terrain = relationship("Terrain", back_populates="reservations",
                          lazy="select")
```

### Sécurité Implémentée

#### Authentification Robuste
```python
# Hachage bcrypt avec salt - utils/hashing.py
import bcrypt

def hash_password(password: str) -> str:
    """
    Hache un mot de passe avec bcrypt
    
    Args:
        password: Mot de passe en clair
    
    Returns:
        str: Hash bcrypt avec salt (coût 12)
        
    Security:
        - Salt automatique unique par hash
        - Cost factor 12 (sécurisé 2025)
        - Résistant aux attaques par dictionnaire
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
```

#### Protection des Données
- **Validation entrées :** Sanitization systématique
- **Requêtes préparées :** Protection SQL injection via ORM
- **Sessions sécurisées :** Tokens avec expiration
- **Logs d'audit :** Traçabilité des actions sensibles

### Performance et Optimisation

#### Stratégies de Cache
```python
# Cache intelligent - controllers/base.py
from functools import lru_cache
from datetime import datetime, timedelta

class BaseController:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {}
    
    def get_cached_data(self, key: str, ttl_minutes: int = 5):
        """
        Récupération avec cache TTL
        
        Args:
            key: Clé de cache
            ttl_minutes: Durée de validité (minutes)
            
        Returns:
            Données mises en cache ou None si expirées
        """
        if key not in self.cache:
            return None
            
        if key in self.cache_ttl:
            expiry = self.cache_ttl[key]
            if datetime.now() > expiry:
                del self.cache[key]
                del self.cache_ttl[key]
                return None
        
        return self.cache[key]
```

#### Optimisations Base de Données
- **Index composites :** Requêtes de recherche accélérées
- **Lazy loading :** Relations chargées à la demande
- **Query batching :** Regroupement des requêtes
- **Connection pooling :** Réutilisation des connexions

### Extensibilité et Maintenance

#### Patterns de Conception Utilisés
1. **Singleton :** Configuration globale
2. **Observer :** Notifications temps réel
3. **Factory :** Création des contrôleurs
4. **Strategy :** Validation des données
5. **Command :** Actions utilisateur annulables

#### Points d'Extension Préparés
```python
# Interface pour extensions - interfaces/plugin.py
from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """Interface standard pour plugins d'extension"""
    
    @abstractmethod
    def initialize(self, app_context):
        """Initialisation du plugin"""
        pass
    
    @abstractmethod  
    def get_menu_items(self):
        """Éléments de menu à ajouter"""
        pass
    
    @abstractmethod
    def handle_event(self, event_type, data):
        """Traitement des événements application"""
        pass

# Exemple d'extension - plugins/reporting.py
class ReportingPlugin(PluginInterface):
    """Plugin de génération de rapports PDF"""
    
    def initialize(self, app_context):
        self.app = app_context
        
    def get_menu_items(self):
        return [
            ("Rapport mensuel", self.generate_monthly_report),
            ("Export planning", self.export_schedule)
        ]
```

## 📸 Captures d'Écran Commentées

### Interface de Connexion
```
[Capture écran login]
- Design Material Dark avec thème vert football
- Champs username/password avec validation temps réel
- Bouton connexion avec animation hover
- Messages d'erreur contextuels en rouge
- Logo "Football Manager 5v5" centré
```

### Dashboard Principal  
```
[Capture écran dashboard]
- 4 cartes métriques en disposition grille 2x2
- Onglets de navigation Material en haut
- Palette cohérente verte (#4CAF50) 
- Icônes Material Design pour clarté visuelle
- Actualisation automatique visible (spinner)
```

### Gestion des Réservations
```
[Capture écran réservations]
- Tableau interactif avec tri/filtres
- Codes couleurs par statut (Orange/Vert/Rouge)  
- Boutons d'action avec icônes explicites
- Formulaire modal pour nouvelle réservation
- Validation conflits en temps réel
```

### Calendrier Interactif
```
[Capture écran calendrier]
- QCalendarWidget personnalisé thème dark
- Points rouges sur dates avec réservations
- Navigation fluide mois précédent/suivant
- Liste réservations du jour sélectionné
- Intégration harmonieuse design global
```

## 🚀 Guide de Déploiement

### Environnement de Production

#### Prérequis Serveur
```bash
# Configuration serveur Ubuntu 20.04 LTS
sudo apt update && sudo apt upgrade -y
sudo apt install python3.8 python3-pip mysql-server nginx
pip3 install virtualenv

# Configuration MySQL production
sudo mysql_secure_installation
# Création utilisateur dédié avec permissions limitées
```

#### Déploiement Automatisé
```bash
# Script de déploiement - deploy.sh
#!/bin/bash
echo "🚀 Déploiement Football Manager 5v5"

# Environnement virtuel
python3 -m venv /opt/football-manager/
source /opt/football-manager/bin/activate

# Installation dépendances
pip install -r requirements-prod.txt

# Configuration base de données
mysql -u deploy_user -p < database/schema_mysql.sql
python setup_admin.py --production

# Configuration service systemd
sudo cp football-manager.service /etc/systemd/system/
sudo systemctl enable football-manager
sudo systemctl start football-manager

echo "✅ Déploiement terminé"
```

### Monitoring et Logs
```python
# Configuration logging - config/logging.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configuration logs rotatifs pour production"""
    
    # Handler fichier avec rotation
    file_handler = RotatingFileHandler(
        'logs/football-manager.log',
        maxBytes=10*1024*1024,  # 10MB max
        backupCount=5
    )
    
    # Format détaillé avec timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Configuration logger racine
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
```

---

**Documentation maintenue par :** Hakim Rayane  
**Dernière mise à jour :** Décembre 2025  
**Version application :** 2.1.1  
**Statut :** Production Ready ✅