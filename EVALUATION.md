# Guide d'Évaluation - PPE BTS SIO SLAM

## 🚀 Installation Express (5 minutes)

### Prérequis
- XAMPP démarré (Apache + MySQL)
- Python 3.8+ installé

### Étapes
1. Cloner le projet : `git clone [URL]`
2. Aller dans le dossier : `cd projet-ppe-exam`
3. Lancer : `QUICKSTART.md` (guide automatisé)

## 👤 Comptes de Test

| Utilisateur | Mot de passe | Rôle | Fonctionnalités |
|-------------|--------------|------|-----------------|
| `admin` | `admin123` | Superadmin | Gestion complète |
| `manager` | `manager123` | Admin (gestionnaire) | Gestion terrains/réservations |
| `user1` | `user123` | User | Réservations personnelles |

## 📋 Points d'Évaluation

### Fonctionnalités Implémentées ✅
- ✅ Authentification sécurisée (bcrypt, sans backdoor dev)
- ✅ Gestion des utilisateurs (CRUD)
- ✅ Gestion des terrains (CRUD, price/capacity)
- ✅ Système de réservations (statuts pending/confirmed/cancelled)
- ✅ Interface moderne (PySide6/Qt6)
- ✅ Base de données relationnelle MySQL (partagée avec appli web)
- ✅ Architecture MVC
- ✅ Documentation complète et annexes PPE alignées
- ✅ Installation automatisée
- ✅ Compatibilité double projet (desktop + API web FastAPI)

### Technologies Utilisées
- **Langage** : Python 3.8+
- **Framework GUI** : PySide6 (Qt6)
- **ORM** : SQLAlchemy 2.0
- **Base de données** : MySQL
- **Sécurité** : bcrypt
- **Architecture** : MVC Pattern

### Livrables
- ✅ Code source complet
- ✅ Documentation technique
- ✅ Manuel utilisateur
- ✅ Scripts d'installation
- ✅ Base de données avec données de test
- ✅ Guide d'évaluation (ce fichier)

## 🔍 Tests Rapides

### Test 1: Connexion
1. Lancer l'app avec `run.bat`
2. Se connecter avec `admin/admin123`
3. ✅ Accès au dashboard avec tous les onglets

### Test 2: Gestion Terrains
1. Onglet "Terrains"
2. Créer un nouveau terrain
3. ✅ Terrain ajouté et visible dans la liste

### Test 3: Réservations
1. Se connecter avec `user1/user123`
2. Créer une réservation
3. ✅ Réservation créée avec validation des conflits

## 📊 Évaluation Technique

### Architecture
- Séparation MVC claire
- Modèles SQLAlchemy bien structurés
- Contrôleurs avec logique métier
- Vues PySide6 organisées

### Sécurité
- Authentification bcrypt
- Validation des entrées
- Gestion des sessions
- Requêtes préparées

### Interface
- Design moderne Material
- Ergonomie intuitive
- Thème sombre professionnel
- Réactivité

### Base de données
- Modèle relationnel normalisé (3 tables : users, terrains, reservations)
- Structure partagée avec l'API web FastAPI
- Contraintes d'intégrité (FK CASCADE, ENUM, UNIQUE)
- Index de performance
- Transactions avec rollback
- Colonnes communes web : price, capacity, total_cost

### Documentation
- Manuel utilisateur complet
- Documentation technique détaillée
- Guide d'installation
- Commentaires code

### Innovation
- Installation automatisée
- Scripts de vérification
- Guide d'évaluation
- Expérience utilisateur

## 💡 Points Forts du Projet

1. **Installation Zero-Config** : Un seul script pour tout installer
2. **Documentation Professionnelle** : Prête pour production
3. **Sécurité Réelle** : bcrypt, validation, sessions
4. **Interface Moderne** : Material Design avec Qt6
5. **Architecture Solide** : MVC, ORM, patterns
6. **Expérience Complète** : De l'installation à l'utilisation

## 📞 Contact Développeur
- **Nom** : Hakim Rayane
- **Formation** : BTS SIO SLAM
- **Projet** : PPE - Gestion Football 5v5
- **Date** : Décembre 2025