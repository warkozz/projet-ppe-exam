# Manuel Utilisateur - Football Manager 5v5

## Installation rapide (5 minutes)
Consultez `QUICKSTART.md` dans le dossier principal pour une installation guidée en 5 étapes.

## Comptes par défaut
- **Superadmin** : `admin` / `admin123`
- **Gestionnaire** : `manager` / `manager123`  
- **Utilisateur** : `user1` / `user123`

## Guide d'utilisation

### 1. Premier lancement
- Lancez `run.bat` (Windows) ou suivez les étapes dans `INSTALL.md`
- L'application vérifie automatiquement l'installation
- Les données de test sont créées automatiquement

### 2. Connexion
- Interface de connexion moderne avec thème sombre
- Utilisez un des comptes par défaut ou créez-en un nouveau
- Authentification sécurisée avec bcrypt

### 3. Fonctionnalités par rôle

#### Superadmin
- Gestion complète des utilisateurs (CRUD)
- Gestion des terrains (création, modification, suppression)
- Vue d'ensemble de toutes les réservations
- Accès aux statistiques avancées

#### Gestionnaire
- Gestion des terrains assignés
- Vue des réservations de ses terrains
- Modification du statut des réservations

#### Utilisateur
- Création de réservations
- Visualisation de ses réservations
- Modification/annulation de ses réservations

### 4. Interface
- Design moderne avec Material Design
- Thème sombre professionnel
- Navigation intuitive par onglets
- Tableaux interactifs avec tri et filtres

### 5. Gestion des réservations
- Calendrier visuel pour sélectionner créneaux
- Validation automatique des conflits
- Statuts : En attente, Confirmée, Annulée
- Notifications en temps réel

### 6. Dépannage
- Utilisez `check_install.py` pour diagnostiquer les problèmes
- Consultez les logs dans le terminal
- Vérifiez que XAMPP/MySQL est démarré
