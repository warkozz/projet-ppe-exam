# Application Lourde — Administration Desktop
## Football Manager 5v5 — BTS SIO SLAM

**Étudiant :** Hakim Rayane  
**Date :** Mars 2026 (initialisé Décembre 2025)  
**Dépôt :** https://github.com/warkozz/projet-ppe-exam

---

## 1. Présentation

L'application desktop **Football Manager 5v5** est l'**outil d'administration** du système Foot5. Destinée exclusivement aux gestionnaires et administrateurs, elle offre une interface native puissante permettant de gérer l'intégralité de la plateforme : utilisateurs, terrains et réservations.

### Caractéristiques principales
- Interface **native** (non-navigateur) avec Material Design thème football
- Accès **complet** à toutes les données de la plateforme
- **Gestion multi-rôles** : Superadmin, Admin, Utilisateur
- **Calendrier interactif** pour visualiser les réservations
- Tableau de bord avec statistiques en temps réel

### Rôles supportés

| Rôle | Droits |
|---|---|
| **Superadmin** | Accès total : gestion users + terrains + réservations + création admins |
| **Admin (Gestionnaire)** | Gestion des terrains et des réservations (sans gestion des users) |
| **User** | Consultation uniquement (accès limité) |

---

## 2. Fonctionnalités

### 2.1 Authentification

- Formulaire de connexion sécurisé (username + password)
- Vérification bcrypt (12 rounds) contre la table `users`
- Affichage du nom et du rôle dans l'interface après connexion
- Messages de bienvenue personnalisés selon le rôle
- **Limitation des tentatives** : blocage après 5 tentatives échouées
- Navigation par onglets conditionnelle au rôle

### 2.2 Tableau de Bord (Dashboard)

Vue synthétique de l'état de la plateforme :
- Nombre de **terrains actifs**
- Nombre de **réservations du jour**
- Nombre total d'**utilisateurs actifs**
- Nombre de **réservations actives en cours**
- Actualisation automatique toutes les **60 secondes**

### 2.3 Gestion des Utilisateurs (Superadmin)

| Action | Description |
|---|---|
| **Lister** | Tableau : ID, Nom, Email, Rôle, Statut (Actif/Inactif) |
| **Ajouter** | Formulaire modal (username, email, mot de passe, rôle) |
| **Modifier** | Modification des informations (email, rôle, statut) |
| **Supprimer** | Suppression avec confirmation modale (cascade BDD) |
| **Rechercher** | Filtre en temps réel par nom ou email |

**Règle métier :** seul le Superadmin peut créer d'autres admins.

### 2.4 Gestion des Terrains

| Action | Description |
|---|---|
| **Lister** | Tableau avec nom, localisation, statut (badge couleur), prix, capacité |
| **Ajouter** | Formulaire avec nom, localisation, prix/h, capacité de joueurs |
| **Modifier** | Mise à jour de toutes les propriétés |
| **Activer / Désactiver** | Toggle visuel (vert = actif, rouge = inactif) |
| **Supprimer** | Suppression avec confirmation (cascade réservations) |

### 2.5 Calendrier des Réservations

- **QCalendarWidget** personnalisé avec thème Material
- Points rouges sur les jours ayant des réservations
- Clic sur une date → affichage des réservations du jour
- Ajout direct d'une réservation depuis le calendrier

### 2.6 Gestion des Réservations

| Action | Description |
|---|---|
| **Lister** | Tableau : Utilisateur, Terrain, Date/Heure, Durée, Statut, Coût |
| **Ajouter** | Formulaire avec sélection user, terrain, créneau + validation conflit |
| **Modifier** | Modification des informations de la réservation |
| **Confirmer** | Passage du statut `pending` → `confirmed` |
| **Annuler** | Passage du statut → `cancelled` |
| **Supprimer** | Suppression définitive |
| **Filtrer** | Filtres par date, statut, terrain |
| **Détecter les conflits** | Validation en temps réel avant création |

---

## 3. Technologies

### 3.1 Stack Technique

```
┌─────────────────────────────────────────────────┐
│               APPLICATION DESKTOP               │
│                                                 │
│  Interface : PySide6 (Qt6)                      │
│  Thème : Material Design (sombre, vert football)│
│  Architecture : MVC (Model-View-Controller)     │
│                                                 │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │    Views     │  │      Controllers         │ │
│  │  login_view  │  │  auth_controller         │ │
│  │  dashboard   │  │  user_controller         │ │
│  │  user_view   │  │  terrain_controller      │ │
│  │  terrain_view│  │  reservation_controller  │ │
│  │  resv_view   │  └──────────┬───────────────┘ │
│  │  calendar    │             │                 │
│  └──────────────┘             │ SQLAlchemy ORM  │
│                               ▼                 │
│              ┌──────────────────────────────┐   │
│              │           Models             │   │
│              │  User ─ Terrain ─ Reservation│   │
│              └──────────────┬───────────────┘   │
└─────────────────────────────┼───────────────────┘
                              │ MySQL connector
                              ▼
                   Base MySQL "foot5" (partagée)
```

### 3.2 Versions et Dépendances

**`requirements.txt` :**
```
PySide6>=6.4.0
SQLAlchemy>=2.0.0
PyMySQL>=1.0.0
bcrypt>=4.0.0
python-dotenv>=1.0.0
```

- **Python 3.8+**
- **PySide6** : framework UI Qt6 pour Python
- **SQLAlchemy 2.0** : ORM (Object-Relational Mapping)
- **PyMySQL** : connecteur MySQL pur Python
- **bcrypt** : hachage sécurisé des mots de passe

### 3.3 Architecture MVC

```
désktop_app/
├── hybrid_main.py              # Point d'entrée de l'application
├── app/
│   ├── config.py               # URL BDD, constantes
│   ├── models/
│   │   ├── db.py               # Engine SQLAlchemy, SessionLocal, Base
│   │   ├── user.py             # Modèle User (ORM)
│   │   ├── terrain.py          # Modèle Terrain (ORM)
│   │   └── reservation.py      # Modèle Reservation (ORM)
│   ├── controllers/
│   │   ├── auth_controller.py        # Login, rate limiting
│   │   ├── user_controller.py        # CRUD utilisateurs
│   │   ├── terrain_controller.py     # CRUD terrains
│   │   └── reservation_controller.py # CRUD + validation conflits
│   ├── views/
│   │   ├── login_view.py             # Écran de connexion
│   │   └── hybrid/
│   │       ├── dashboard_view.py     # Tableau de bord statistiques
│   │       ├── user_view.py          # Gestion des utilisateurs
│   │       ├── terrain_view.py       # Gestion des terrains
│   │       ├── reservation_view.py   # Gestion des réservations
│   │       └── calendar_view.py      # Calendrier interactif
│   ├── services/
│   │   ├── calendar_service.py       # Logique du calendrier
│   │   └── cpp_bridge.py             # Pont vers algorithme C++ (optimisation)
│   ├── styles/
│   │   └── theme.py                  # Thème Material Design
│   └── utils/
│       └── hashing.py                # Utilitaires bcrypt
```

### 3.4 Patterns de Conception Utilisés

| Pattern | Utilisation dans l'application |
|---|---|
| **MVC** | Architecture globale (Model/View/Controller séparés) |
| **Singleton** | Session BDD SQLAlchemy |
| **Observer** | Actualisation du dashboard (signal/slot Qt) |
| **Factory** | Création des widgets selon le rôle utilisateur |
| **Strategy** | Stratégies de validation des réservations |
| **Command** | Actions CRUD encapsulées dans les controllers |

---

## 4. Interfaces

### 4.1 Charte Graphique

| Élément | Valeur |
|---|---|
| Couleur primaire | #4CAF50 (Vert Football) |
| Couleur secondaire | #2E7D32 (Vert Foncé) |
| Couleur accent | #81C784 (Vert Clair) |
| Fond (Surface) | #1E1E1E (Thème Sombre) |
| Texte principal | #FFFFFF |
| Erreur | #F44336 (Rouge) |
| Typographie | Roboto (Material Design) 14–24px |

### 4.2 Écran de Connexion

```
┌─────────────────────────────────────────┐
│         Football Manager 5v5            │
│         ⚽ (logo Material Design)        │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │  Nom d'utilisateur              │   │
│   └─────────────────────────────────┘   │
│   ┌─────────────────────────────────┐   │
│   │  Mot de passe          [👁]     │   │
│   └─────────────────────────────────┘   │
│                                         │
│        [ SE CONNECTER ]                 │
│                                         │
│   ⚠ Message d'erreur (si erreur)       │
└─────────────────────────────────────────┘
```

### 4.3 Dashboard Principal

```
┌─────────────────────────────────────────┐
│ Football Manager 5v5 — Bienvenue, admin │
├──────────┬──────────┬──────────┬────────┤
│ Terrains │ Resas    │Utilisat. │ Total  │
│ actifs   │ du jour  │ actifs   │ resas  │
│   5      │    3     │   12     │  18    │
├──────────┴──────────┴──────────┴────────┤
│ [Dashboard][Users][Terrains][Resas][Cal]│
│    Onglets de navigation par rôle       │
└─────────────────────────────────────────┘
```

### 4.4 Gestion des Réservations

```
Filtres : [Date       ▼] [Statut ▼] [Terrain ▼]
┌────┬──────────┬──────────┬──────────────┬───────────┬──────────┐
│ ID │ Client   │ Terrain  │ Date/Heure   │ Statut    │ Actions  │
├────┼──────────┼──────────┼──────────────┼───────────┼──────────┤
│  1 │ user1    │ Terrain A│ 30/03 14h-16h│ 🟡 Attente│[✓][✗][✏]│
│  2 │ test2    │ Terrain B│ 30/03 18h-20h│ 🟢 Confirmé│[✗][✏]  │
│  3 │ user1    │ Terrain C│ 31/03 10h-12h│ 🔴 Annulé │[🗑]      │
└────┴──────────┴──────────┴──────────────┴───────────┴──────────┘
```

---

## 5. Sécurité

### 5.1 Authentification

- Vérification du hash bcrypt : `bcrypt.checkpw(password.encode(), hash.encode())`
- **Rate limiting** : blocage automatique après 5 tentatives échouées en moins de 10 minutes
- Déconnexion propre avec nettoyage de la session en mémoire

### 5.2 Contrôle d'Accès RBAC

```python
# Vérification des droits dans les controllers
def require_role(user, required_roles):
    if user.role not in required_roles:
        raise PermissionError("Accès non autorisé")

# Exemple d'utilisation
def delete_user(current_user, user_id):
    require_role(current_user, ['superadmin'])
    # ... suppression
```

### 5.3 Validation des Données

- **Côté application** : validation Python avant toute écriture en BDD
- **Côté BDD** : contraintes SQL (UNIQUE, FK, ENUM, UNIQUE KEY anti-conflit)
- **Détection de conflit** : requête SQL + validation Python en double

### 5.4 Sécurité des Mots de Passe

```python
# Création (hashing)
import bcrypt
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

# Vérification (login)
bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
```

---

## 6. Tests

### 6.1 Résultats Globaux

| Catégorie | Résultat |
|---|---|
| Tests unitaires | 124/124 passent ✅ |
| Tests d'intégration | 18/18 réussis ✅ |
| Tests fonctionnels | 15/15 scénarios validés ✅ |
| Couverture globale | **87%** |
| Crash en 48h de test | 0 ✅ |

### 6.2 Tests Unitaires (exemples)

```python
class TestUserModel(unittest.TestCase):
    def test_password_hashing(self):
        # le hash doit être différent du mot de passe en clair
        hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt(12))
        self.assertNotEqual(hash, "admin123".encode())
        self.assertTrue(bcrypt.checkpw("admin123".encode(), hash))

    def test_user_validation(self):
        # username trop court → ValueError
        with self.assertRaises(ValueError):
            create_user(username="ab", email="test@test.com")

class TestReservationModel(unittest.TestCase):
    def test_time_validation(self):
        # end avant start → erreur
        with self.assertRaises(ValueError):
            create_reservation(start="14:00", end="13:00")

    def test_conflict_detection(self):
        # deux réservations sur le même terrain/créneau
        self.assertTrue(reservation1.conflicts_with(reservation2))
```

### 6.3 Couverture par Module

| Module | Couverture |
|---|---|
| `models/user.py` | 95% |
| `models/terrain.py` | 92% |
| `models/reservation.py` | 88% |
| `controllers/` | 85% |
| `views/` | 78% |
| `utils/` | 90% |
| **TOTAL** | **87%** |

### 6.4 Tests de Performance

| Opération | Cible | Mesuré | Statut |
|---|---|---|---|
| Connexion (login) | < 1s | 0.3s | ✅ |
| Chargement dashboard | < 2s | 1.2s | ✅ |
| Création réservation | < 2s | 0.8s | ✅ |
| Requête conflits | < 1s | 0.4s | ✅ |
| Rafraîchissement calendrier | < 1s | 0.6s | ✅ |

---

## 7. Installation et Démarrage

### Prérequis
- Python 3.8+
- XAMPP avec MySQL (base `foot5` initialisée)
- Droits d'écriture sur le dossier d'installation

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam/logiciel-gestion/desktop_app

# 2. Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser la base de données
# Exécuter schema_mysql.sql puis seed_data_mysql_fixed.sql dans phpMyAdmin (XAMPP)

# 5. Lancer l'application
python hybrid_main.py
```

### Comptes par défaut

| Compte | Mot de passe | Rôle |
|---|---|---|
| admin | admin123 | Superadmin |
| manager | manager123 | Admin (Gestionnaire) |
| user1 | user123 | Utilisateur |

---

*Hakim Rayane — BTS SIO SLAM — PPE Foot5 — Mars 2026*
