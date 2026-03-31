# Tableau de Synthèse — Projet PPE Foot5
**Étudiant :** Hakim Rayane — BTS SIO SLAM  
**Date :** Mars 2026

---

> **Phrase clé du projet :**  
> "Le projet Foot5 repose sur une architecture composée de deux applications complémentaires : une application web destinée aux clients et une application lourde destinée à l'administration, partageant une base de données commune."

---

## Vue d'Ensemble des Deux Applications

| Critère | Application Légère (Web) | Application Lourde (Admin) |
|---|---|---|
| **Nom** | Foot5 — Extension Web | Football Manager 5v5 — Desktop |
| **Type** | Application web (SPA) | Application desktop |
| **Public cible** | Clients / utilisateurs finaux | Administrateurs / gestionnaires |
| **Rôle** | Interface de réservation côté client | Gestion complète de la plateforme |
| **Déploiement** | Navigateur web (localhost:3000) | Installé sur poste admin |
| **GitHub** | [projet-ppe-foot5-web](https://github.com/warkozz/projet-ppe-foot5-web) | [projet-ppe-exam](https://github.com/warkozz/projet-ppe-exam) |

---

## Technologies

| Composant | Application Légère (Web) | Application Lourde (Admin) |
|---|---|---|
| **Frontend** | React 18 + TypeScript + Tailwind CSS | PySide6 (Qt6) — interface native |
| **Backend** | FastAPI (Python) | — (accès direct BDD via SQLAlchemy) |
| **ORM** | SQLAlchemy 2.0 | SQLAlchemy 2.0 |
| **Base de données** | MySQL `foot5` (partagée) | MySQL `foot5` (partagée) |
| **Authentification** | JWT (JSON Web Token) | Session locale (bcrypt) |
| **Hachage mdp** | bcrypt (12 rounds) | bcrypt (12 rounds) |
| **Tests** | pytest + requests (API) | unittest + pytest (unitaires/intégration) |
| **Langage principal** | TypeScript / Python | Python 3.8+ |

---

## Fonctionnalités

| Fonctionnalité | App Légère (Web) | App Lourde (Admin) |
|---|---|---|
| Connexion / Authentification | ✅ Via JWT | ✅ Via session bcrypt |
| Inscription utilisateur | ✅ | ❌ (créé par admin) |
| Réserver un terrain | ✅ | ✅ |
| Voir ses réservations | ✅ (Mon Espace) | ✅ (toutes) |
| Annuler une réservation | ✅ | ✅ |
| Confirmer une réservation | ❌ | ✅ (admin/superadmin) |
| Gestion des utilisateurs (CRUD) | ❌ | ✅ |
| Gestion des terrains (CRUD) | ❌ | ✅ |
| Activer / désactiver terrain | ❌ | ✅ |
| Calendrier des réservations | ❌ | ✅ (calendrier interactif) |
| Tableau de bord statistiques | ❌ | ✅ |
| Détection conflits horaires | ✅ (API) | ✅ (BDD + service) |
| Quota réservations hebdo | ✅ (2/semaine max) | ❌ (admin sans limite) |
| Calcul coût total | ✅ (tarif horaire) | ✅ |
| Gestion des rôles | Lecture (user/admin) | Écriture (superadmin/admin/user) |

---

## Architecture Partagée

```
Clients (navigateur)          Admins (poste)
        │                           │
        ▼                           ▼
 App Légère (Web)         App Lourde (Desktop)
 React + FastAPI          Python + PySide6
        │                           │
        └──────────┬────────────────┘
                   │
                   ▼
          Base MySQL "foot5"
          ┌──────────────┐
          │ users        │
          │ terrains     │
          │ reservations │
          └──────────────┘
```

---

## Rôles Utilisateurs

| Rôle | App Web | App Desktop |
|---|---|---|
| **user** | Réserve, consulte son espace | Limité (pas d'accès admin) |
| **admin** | Voir toutes les réservations, confirmer | Gestion réservations + terrains |
| **superadmin** | — | Accès total : users + terrains + réservations |

---

## Points Forts du Projet

| Aspect | Détail |
|---|---|
| **Cohérence** | BDD unique partagée entre les deux apps |
| **Complémentarité** | Client léger (web) + outil admin puissant |
| **Sécurité** | bcrypt 12 rounds + JWT + validation métier |
| **Architecture** | MVC côté desktop, REST API côté web |
| **Qualité code** | 87% couverture tests, PEP8, TypeScript strict |
| **Performance** | < 2 secondes pour toutes les opérations clés |

---

*Hakim Rayane — BTS SIO SLAM — PPE Foot5 — Mars 2026*
