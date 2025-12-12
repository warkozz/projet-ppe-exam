# 🎨 Étape 2 : Maquettes des Interfaces Utilisateur

## 📱 Vue d'Ensemble des Interfaces

L'application Football Manager 5v5 comprend **6 interfaces principales** conçues avec une approche Material Design et un thème football cohérent.

## 🔐 Interface de Connexion

### Description
Interface d'authentification sécurisée avec design moderne et thème sombre.

### Fonctionnalités
- Champs **Nom d'utilisateur** et **Mot de passe**
- Bouton **Se connecter** avec animation
- **Messages d'erreur** contextuels
- **Logo Football Manager 5v5** centré
- **Validation en temps réel** des champs

### Éléments Visuels
- Palette verte (#4CAF50) cohérente avec le thème football
- Champs de saisie avec bordures arrondies
- Icônes Material Design (utilisateur, cadenas)
- Animations de survol et focus

---

## 📊 Dashboard Principal

### Description
Tableau de bord central avec cartes statistiques et navigation par onglets.

### Fonctionnalités
- **Cartes statistiques** :
  - Nombre de terrains actifs
  - Réservations du jour
  - Total des utilisateurs
  - Revenus mensuels (si applicable)
- **Navigation par onglets** vers toutes les fonctionnalités
- **Actualisation automatique** (toutes les minutes)
- **Messages de bienvenue** personnalisés par rôle

### Éléments Visuels
- Layout en grille responsive 2x2 pour les cartes
- Icônes Material pour chaque métrique
- Couleurs différenciées par type de donnée
- Animations de chargement élégantes

---

## 👥 Gestion des Utilisateurs

### Description
Interface CRUD complète pour la gestion des comptes utilisateurs.

### Fonctionnalités
- **Tableau utilisateurs** avec colonnes :
  - ID, Nom d'utilisateur, Email, Rôle, Statut
- **Boutons d'action** :
  - ➕ Ajouter utilisateur
  - ✏️ Modifier utilisateur sélectionné
  - 🗑️ Supprimer utilisateur sélectionné
- **Formulaires modaux** pour ajout/modification
- **Filtres et recherche** en temps réel
- **Validation des données** avant soumission

### Éléments Visuels
- TableWidget avec alternance de couleurs
- Boutons avec icônes Material Design
- Formulaires dans des QDialog modales
- Indicateurs visuels pour les statuts

---

## 🏟️ Gestion des Terrains

### Description
Module de gestion des infrastructures sportives disponibles.

### Fonctionnalités
- **Liste des terrains** avec informations :
  - Nom du terrain, Localisation, Statut (Actif/Inactif)
- **Actions disponibles** :
  - ➕ Créer nouveau terrain
  - ✏️ Modifier terrain existant
  - 🔄 Activer/Désactiver terrain
  - 🗑️ Supprimer terrain
- **Toggle buttons** visuels pour l'activation
- **Formulaires de saisie** avec validation

### Éléments Visuels
- Icônes terrain de football pour identification visuelle
- Badges colorés pour les statuts (Vert=Actif, Rouge=Inactif)
- Formulaires avec disposition claire et logique
- Confirmation modales pour les suppressions

---

## 📅 Calendrier des Réservations

### Description
Interface calendrier interactive pour visualiser et gérer les réservations.

### Fonctionnalités
- **Calendrier mensuel** avec navigation
- **Points rouges** indiquant les jours avec réservations
- **Clic sur date** pour voir les réservations du jour
- **Ajout direct** de réservations depuis le calendrier
- **Synchronisation temps réel** avec la base de données

### Éléments Visuels
- QCalendarWidget personnalisé avec thème Material
- Marqueurs visuels pour les réservations
- Navigation fluide entre mois/années
- Intégration harmonieuse dans le design global

---

## 📋 Gestion des Réservations

### Description
Module central pour administrer toutes les réservations.

### Fonctionnalités
- **Tableau des réservations** avec :
  - Utilisateur, Terrain, Date/Heure, Durée, Statut
- **Filtres avancés** :
  - Par date (aujourd'hui, semaine, mois)
  - Par statut (En attente, Confirmée, Annulée)
  - Par terrain
- **Actions de gestion** :
  - ➕ Nouvelle réservation
  - ✏️ Modifier réservation
  - ✅ Confirmer réservation
  - ❌ Annuler réservation
- **Validation des conflits** automatique
- **Notifications** pour les changements d'état

### Éléments Visuels
- Codes couleurs pour les statuts :
  - 🟡 En attente (Orange)
  - 🟢 Confirmée (Vert)
  - 🔴 Annulée (Rouge)
- Icônes contextuelles pour chaque action
- Messages de confirmation et d'erreur
- Animations de mise à jour des listes

---

## 🎨 Charte Graphique

### Palette de Couleurs
- **Primaire :** #4CAF50 (Vert Football)
- **Secondaire :** #2E7D32 (Vert Foncé)
- **Accent :** #81C784 (Vert Clair)
- **Surface :** #1E1E1E (Thème Sombre)
- **Texte :** #FFFFFF (Blanc)
- **Erreur :** #F44336 (Rouge)
- **Succès :** #4CAF50 (Vert)

### Typographie
- **Police principale :** Roboto (Material Design)
- **Tailles :** 
  - Titres : 18-24px
  - Texte standard : 14px
  - Labels : 12px

### Iconographie
- **Bibliothèque :** Material Design Icons
- **Style :** Outline pour cohérence
- **Couleurs :** Blanc ou vert selon contexte

## 🔄 Navigation entre Écrans

### Flux Principal
1. **Connexion** → Dashboard
2. **Dashboard** → Navigation onglets vers modules
3. **Modules** → Retour Dashboard via bouton dédié
4. **Calendrier** ↔ **Réservations** (navigation bidirectionnelle)

### Cohérence d'Interface
- **Header uniforme** avec titre et logo
- **Onglets persistants** pour navigation rapide
- **Boutons d'action standardisés** avec mêmes couleurs/icônes
- **Messages d'état cohérents** dans toute l'application

---

**Note :** Ces maquettes ont été implémentées avec PySide6 et qt-material pour obtenir le rendu Material Design décrit. L'interface finale correspond fidèlement à ces spécifications.