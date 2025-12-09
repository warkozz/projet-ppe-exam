# 📅 Calendrier des Réservations - Documentation

## Vue d'ensemble

Le **Calendrier des Réservations** est une nouvelle fonctionnalité interactive qui permet de visualiser toutes les réservations de terrains de football sur une interface calendaire moderne avec Material Design.

## Fonctionnalités principales

### 🗓️ Vue Calendaire Interactive
- **Calendrier mensuel** avec navigation par mois/année
- **Indicateurs visuels** sur les jours avec réservations :
  - 🟢 **Vert clair** : 1 réservation
  - 🟢 **Vert moyen** : 2-3 réservations  
  - 🟢 **Vert foncé** : 4+ réservations
  - 🟠 **Orange** : Aujourd'hui
  - 🔴 **Rouge-orange** : Aujourd'hui + réservations

### 📊 Panneau de Statistiques
- **Statistiques annuelles** en temps réel
- **Terrain le plus populaire** de l'année
- **Nombre total de réservations**
- **Jours avec réservations**

### 🔍 Systeme de Filtres
- **Filtre par utilisateur** : Voir les réservations d'un utilisateur spécifique
- **Filtre par terrain** : Voir les réservations d'un terrain spécifique
- **Sélecteur d'année** : Naviguer entre les différentes années

### 📋 Vue Détaillée des Jours
- **Clic sur une date** → Dialog avec tous les détails
- **Table des réservations** avec :
  - ⏰ Horaires de réservation
  - 🏟️ Terrain réservé
  - 👤 Nom de l'utilisateur
  - 📧 Email de contact
  - 📝 Notes de réservation
  - 📊 Statut (Actif/Annulé)

## Architecture Technique

### 📁 Structure des Fichiers

```
app/
├── services/
│   └── calendar_service.py      # Service de données calendrier
└── views/hybrid/
    └── calendar_view.py         # Interface utilisateur calendrier
```

### 🔧 Classes Principales

#### `CalendarService`
**Responsabilité** : Couche de service pour l'accès aux données de réservation
- `get_monthly_reservations()` : Récupère les réservations d'un mois
- `get_day_reservations()` : Détails d'une journée spécifique
- `get_yearly_overview()` : Vue d'ensemble annuelle
- `get_calendar_statistics()` : Statistiques globales
- `get_filtered_reservations()` : Filtrage avancé

#### `FootballCalendarWidget`
**Responsabilité** : Widget calendrier personnalisé avec thème football
- Hérite de `QCalendarWidget`
- Applique le style Material Design FootballTheme
- Gère les indicateurs visuels sur les dates
- Émet des signaux lors des clics sur dates

#### `HybridCalendarView`
**Responsabilité** : Interface principale du calendrier
- Layout avec splitter (calendrier + statistiques)
- Barre de contrôles avec filtres
- Intégration avec le dashboard principal

#### `ReservationDetailsDialog`
**Responsabilité** : Dialog modal pour afficher les détails d'un jour
- Table avec toutes les réservations
- Statistiques rapides du jour
- Bouton de fermeture

## 🎨 Design System

### Material Design Football Theme
- **Couleurs principales** : Palette verte (#4CAF50)
- **Typography** : Segoe UI, poids variables
- **Composants** : Cards, Buttons avec effet hover
- **Iconographie** : Emojis contextualisant les actions

### Responsive Layout
- **Splitter horizontal** : Calendrier (70%) + Statistiques (30%)
- **Contrôles en haut** : Faciles d'accès
- **Barre de statut** : Informations temps réel

## 🔌 Intégration Dashboard

### Bouton d'Accès
```python
# Dans dashboard_view.py - Actions rapides
calendar_btn = HoverButton("Calendrier des réservations", "📅")
calendar_btn.clicked.connect(self._open_calendar)
```

### Navigation
- **Bouton "Calendrier des réservations"** dans les actions rapides
- **Accessible à tous les rôles** (user, admin, superadmin)  
- **Bouton retour** vers le dashboard
- **Navigation intégrée** dans la même fenêtre

## 📋 Cas d'Usage

### Pour les **Utilisateurs**
1. **Consulter disponibilités** : Voir rapidement les jours libres/occupés
2. **Planifier réservations** : Identifier les créneaux disponibles
3. **Voir ses réservations** : Filtrer par son nom d'utilisateur

### Pour les **Administrateurs**  
1. **Vue d'ensemble globale** : Statistiques de fréquentation
2. **Gestion planning** : Identifier les pics d'activité
3. **Analyse terrains** : Quel terrain est le plus demandé
4. **Suivi annuel** : Évolution des réservations

## 🚀 Utilisation

### Accès depuis le Dashboard
1. Se connecter à l'application
2. Cliquer sur **"📅 Calendrier des réservations"** 
3. Explorer le calendrier interactif

### Navigation dans le Calendrier
1. **Changer de mois** : Flèches de navigation
2. **Changer d'année** : Dropdown en haut à droite
3. **Filtrer** : Utiliser les dropdowns utilisateur/terrain
4. **Voir détails** : Cliquer sur une date avec réservations
5. **Retour** : Bouton "🔙 Retour Dashboard"

### Lecture des Indicateurs
- **Aucune couleur** : Jour sans réservation
- **Vert de plus en plus foncé** : Plus de réservations
- **Orange** : Date d'aujourd'hui
- **Rouge-orange** : Aujourd'hui avec réservations

## 🔧 Maintenance & Extension

### Ajout de Fonctionnalités
- **Export PDF** : Calendrier mensuel imprimable
- **Vue semaine** : Mode d'affichage alternatif  
- **Notifications** : Alertes pour réservations proches
- **Statistiques avancées** : Graphiques de fréquentation

### Performance
- **Cache des données** : Optimisation requêtes base
- **Pagination** : Pour les années avec beaucoup de données
- **Lazy loading** : Chargement différé des détails

### Personnalisation
- **Thèmes alternatifs** : Autres palettes de couleurs
- **Langues** : Internationalisation des libellés
- **Formats dates** : Support différents formats régionaux

## ⚙️ Configuration

### Base de Données
Utilise les tables existantes :
- `reservations` : Données principales
- `users` : Informations utilisateurs  
- `terrains` : Détails des terrains

### Dépendances
- **PySide6** : Interface graphique Qt
- **SQLAlchemy** : ORM base de données
- **datetime** : Gestion des dates Python

### Paramètres
Aucune configuration spéciale requise, utilise la configuration existante de l'application.

---

**Version** : 2.0 Material Design
**Auteur** : Football Manager 5v5 Team  
**Date** : Décembre 2024