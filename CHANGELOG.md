# 📋 Changelog - Football Manager 5v5

Toutes les modifications importantes du projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [2.2.0] - 2026-03-17

### 🔒 Security - Corrections de sécurité
- **Suppression de la backdoor de développement** dans `auth_controller.py` : connexion possible avec `admin/admin` ou `admin/test` sans DB était un risque critique
- **Correction fuite de session** dans `UserController` : `self.db` permanent remplacé par sessions par méthode avec `finally: db.close()`

### 🛠️ Fixed - Corrections BDD et modèles
- **ENUM statuts réservations** aligné sur les deux applis : `active/cancelled/completed` → `pending/confirmed/cancelled`, default `pending`
- **Modèle Reservation** : `status` default corrigé (`confirmed` → `pending`), `notes` passé de `String(250)` à `Text`
- **Modèles SQLAlchemy** : suppression des colonnes `created_at`/`updated_at` (inexistantes dans la DB réelle partagée)
- **`terrain.py`** : doublon `__repr__` supprimé
- **Compatibilité DB partagée** : ajout de `price`, `capacity` (terrains) et `total_cost` (reservations) dans les modèles desktop pour refléter les colonnes ajoutées par l'API web

### 📄 Fixed - Annexes PPE
- **MCD_MLD_Scripts.md** : rôles corrigés (`gestionnaire` → `admin`, `utilisateur` → `user`), champ `active` ajouté à `users`, `notes TEXT` ajouté à `reservations`, `email VARCHAR(100)` → `VARCHAR(120)`
- **MCD_Visuel_Template.md** : valeurs ENUM rôles alignées avec la DB réelle
- **06_Developpement.md**, **08_Documentation.md** : valeurs techniques des rôles corrigées

### 🗄️ Changed - Schémas SQL
- **schema_mysql.sql** : ENUM statuts corrigé, ajout `price`/`capacity` sur terrains, `total_cost` sur reservations
- **schema_postgres.sql** : réécriture complète alignée avec MySQL (types ENUM propres, index, contrainte `CHECK end > start`, colonnes manquantes ajoutées)

### 🌿 Git
- Branche `fix/bdd-models-annexes-alignment` créée depuis `PPE-EXAM`
- Mergée dans `develop` puis dans `main` (merge commits `--no-ff`)

## [2.1.1] - 2025-12-12

### 🚀 Added - Calendrier Interactif
- **Calendrier interactif des réservations** intégré au dashboard
- **Système de rafraîchissement instantané** du calendrier
- **Points rouges visuels** pour marquer les réservations sur le calendrier
- **Ajout direct de réservations** depuis le calendrier (commit 148378e)
- **Notifications système globales** pour toutes les opérations
- **Interface calendrier moderne** avec navigation mois/année

### 🔧 Changed - Performance Calendrier
- **Performance du calendrier** améliorée avec cache intelligent
- **Mise à jour instantanée** lors des ajouts/modifications de réservations
- **Interface calendrier** plus réactive et fluide
- **Gestion des instances** optimisée pour éviter les doublons
- **Navigation temporelle** fluide entre les mois

### 🛠️ Fixed - Corrections Calendrier
- **Mise à jour instantanée des points rouges** du calendrier (commit 11e1d27)
- **Système de refresh** corrigé pour les opérations calendrier (commit 5ee1c74)
- **Performance** améliorée lors des changements fréquents
- **Mémoire** mieux gérée avec réutilisation des instances
- **Synchronisation** parfaite entre calendrier et base de données

## [2.1.0] - 2025-12-12

### 🚀 Added - Installation et Documentation
- **Installation automatisée complète** avec `setup_admin.py`
- **Vérification système** avec `check_install.py`
- **Guide QUICKSTART.md** pour installation en 5 minutes
- **Guide d'évaluation EVALUATION.md** pour PPE/examens
- **Documentation technique complète** mise à jour
- **Manuel utilisateur détaillé** avec comptes par défaut
- **Scripts de validation** base de données (`verify_install.sql`)
- **Configuration XAMPP optimisée** pour nouveaux utilisateurs
- **Données de test robustes** avec vrais hachages bcrypt

### 🔧 Changed - Améliorations
- **Hachages bcrypt corrigés** dans tous les fichiers seed_data
- **Nom base de données unifié** : `foot5` (au lieu de football_manager)  
- **Configuration par défaut** optimisée pour XAMPP standard
- **Structure documentation** reorganisée et nettoyée
- **Gestion d'erreurs améliorée** dans l'installation
- **Messages utilisateur** plus clairs et informatifs
- **Navigation documentation** simplifiée

### 🛠️ Fixed - Corrections critiques
- **Hachages bcrypt invalides** remplacés par vrais hachages fonctionnels
- **Problèmes de connexion DB** résolus (nom database incorrect)
- **Configuration MySQL** adaptée à XAMPP par défaut
- **Dépendances manquantes** détectées et documentées
- **Erreurs première installation** complètement éliminées
- **Conflits de noms** base de données résolus

### 🧹 Removed - Nettoyage
- **Fichiers doublons** supprimés (README_HYBRIDE.md, VERSION_2.0.md, etc.)
- **seed_data.sql obsolètes** avec hachages invalides
- **Documentation redondante** consolidée
- **Fichiers temporaires** de développement nettoyés
- **CHANGELOG/INSTALL** doublons dans desktop_app/ supprimés

### 🔒 Security - Sécurité renforcée
- **Vrais hachages bcrypt** pour tous les comptes par défaut
- **Validation des mots de passe** avant insertion DB
- **Comptes sécurisés** : admin/admin123, manager/manager123, user1/user123
- **Configuration sécurisée** par défaut pour développement

### 📚 Documentation - PPE Ready
- **Guide complet d'évaluation** pour correcteurs BTS
- **Comptes de test documentés** avec mots de passe
- **Installation zero-config** pour démonstration
- **Tests de validation** automatisés inclus
- **Architecture technique** entièrement documentée

## [2.0.0] - 2025-12-08

### 🎨 Added - Nouvelles fonctionnalités
- **Interface Material Design** complète avec `qt-material` library
- **Thème football cohérent** avec palette de couleurs verte (#4CAF50)
- **HoverButton component** standardisé avec animations de survol
- **Dashboard hybride** avec statistiques en temps réel
- **Architecture hybride** combinant fonctionnalités stables + design moderne
- **Gestion avancée des contraintes** DB avec rollback automatique
- **Validation des doublons** username/email côté serveur
- **Messages d'erreur contextuels** et informatifs
- **Toggle buttons** visuels pour statuts actif/inactif
- **Vue dashboard** avec cartes de statistiques modernes
- **Navigation centralisée** avec retour dashboard fluide
- **Actualisation automatique** des données (toutes les minutes)
- **Nouveaux fichiers de documentation** (INSTALL.md, VERSION_2.0.md)

### 🔧 Changed - Modifications
- **Refonte complète de l'interface** utilisateur avec Material Design
- **Standardisation des composants** (boutons, listes, formulaires)
- **Amélioration de la gestion d'erreurs** avec rollback transactions
- **Optimisation de la structure** des fichiers du projet
- **Mise à jour du schéma DB** avec nouvelles contraintes et index
- **Migration vers PyMySQL** pour une meilleure compatibilité
- **Réorganisation des vues** dans `/app/views/hybrid/`
- **Amélioration des messages** utilisateur (succès, erreurs, warnings)

### 🛠️ Fixed - Corrections
- **Correction des erreurs de contraintes** database avec gestion IntegrityError
- **Fix des transactions rollback** en cas d'erreur DB
- **Correction de l'affichage** des listes de sélection
- **Fix des problèmes de navigation** entre vues
- **Correction des imports** et dépendances manquantes
- **Fix des problèmes de validation** formulaires
- **Correction des styles CSS** incohérents
- **Fix des erreurs de contraintes** email/username uniques

### 🧹 Removed - Suppressions
- **30% des fichiers obsolètes** supprimés pour optimisation
- **Dossier cpp/** complet (bridge C++ non utilisé)
- **Fichiers de migration** temporaires (generate_hash.py, update_*.py)
- **Components dupliqués** (modern_components.py)
- **Documentation redondante** (README_ADMIN.md, README_MODERN.md)
- **Dossier app/components/** complet
- **Fichiers de test** obsolètes
- **Code mort** et imports non utilisés

### 🔒 Security - Sécurité
- **Validation renforcée** des données utilisateur avant DB
- **Gestion robuste** des contraintes d'unicité
- **Protection contre** les doublons avec vérification préventive
- **Messages d'erreur sécurisés** sans exposition des détails techniques

## [1.0.0] - 2024-10-14

### 🎯 Added - Version initiale
- **Interface PySide6** fonctionnelle de base
- **Système d'authentification** avec bcrypt
- **CRUD complet** pour utilisateurs, terrains, réservations
- **Base de données** MySQL/PostgreSQL avec SQLAlchemy
- **Gestion des rôles** (superadmin, admin, user)
- **Système de réservations** avec vérification des conflits
- **Interface de gestion** multi-fenêtres
- **Scripts d'installation** et configuration
- **Documentation** de base (README.md)

---

## 📊 Statistiques de développement

### Métriques v2.1 vs v1.0

| Métrique | v1.0 | v2.1 | Évolution |
|----------|------|------|-----------|
| **Fichiers total** | ~150+ | ~95 | -37% 📉 |
| **Vues principales** | 4 | 6 | +50% 📈 |
| **Composants UI** | Standard Qt | Material Design + Calendrier | +150% 🎨 |
| **Lines of code** | ~6,000 | ~9,000+ | +50% 📈 |
| **Dependencies** | 5 | 6 | +20% |
| **Database tables** | 3 | 3 | → |
| **Documentation** | 1 file | 8 files | +700% 📚 |
| **Installation** | Manuel | Automatisé | +100% ⚡ |

### Impact des changements

**✅ Améliorations mesurables :**
- **Interface** : 100% des vues uniformisées avec Material Design
- **Performance** : Maintenue malgré les améliorations visuelles
- **Maintenance** : Code 30% plus léger, mieux organisé
- **UX** : Messages d'erreur clairs, navigation fluide
- **Robustesse** : Gestion d'erreurs avancée avec rollback

**🎯 Objectifs atteints :**
- [x] Interface moderne et cohérente
- [x] Compatibilité totale avec version précédente
- [x] Aucune perte de fonctionnalité
- [x] Code optimisé et maintenable
- [x] Documentation complète



## 🔮 Roadmap Future

### v2.2.0 - Prévu Q1 2026
- [ ] **Thème sombre** optionnel avec switch utilisateur
- [ ] **Graphiques statistiques** avec charts.js intégrés
- [ ] **Export PDF** des plannings mensuels/hebdomadaires
- [ ] **Recherche globale** avancée multi-critères
- [ ] **Backup automatique** des données

### v2.3.0 - Prévu Q2 2026
- [ ] **Multi-langues** (Français/Anglais/Espagnol)
- [ ] **API REST** pour intégrations externes
- [ ] **Module mobile** companion (PWA)
- [ ] **Système de notifications** push
- [ ] **Tableau de bord analytics** avec KPI avancés

### v3.0.0 - Vision long terme (2027+)
- [ ] **Architecture microservices** cloud-native
- [ ] **Interface web** progressive complète
- [ ] **Intégration cloud** multi-plateforme (AWS/Azure/GCP)
- [ ] **Intelligence artificielle** pour optimisation automatique des plannings
- [ ] **Module de facturation** et gestion commerciale intégrés
- [ ] **Multi-tenant** pour gestion de plusieurs centres sportifs

---

## 🏷️ Format des versions

Ce projet utilise le [Versioning Sémantique](https://semver.org/lang/fr/) :

- **MAJOR** (X.0.0) : Changements incompatibles de l'API
- **MINOR** (0.X.0) : Nouvelles fonctionnalités rétro-compatibles
- **PATCH** (0.0.X) : Corrections de bugs rétro-compatibles

### Types de changements

- `Added` ➕ pour les nouvelles fonctionnalités
- `Changed` 🔧 pour les modifications de fonctionnalités existantes
- `Deprecated` ⚠️ pour les fonctionnalités bientôt supprimées
- `Removed` ❌ pour les fonctionnalités supprimées
- `Fixed` 🐛 pour les corrections de bugs
- `Security` 🔒 pour les corrections de vulnérabilités

---

> 📝 **Note :** Ce changelog est maintenu manuellement et reflète les changements majeurs du projet. Pour un historique complet, consultez l'historique Git du projet.